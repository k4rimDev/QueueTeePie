import unittest

from queue_tee_pie.queue_tee_pie.storage.sqlite_storage import SQLiteStorage
from queue_tee_pie.queue_tee_pie.utils.serializer import TaskSerializer


class TestSQLiteStorage(unittest.TestCase):
    def setUp(self):
        self.storage = SQLiteStorage(":memory:")  # Use in-memory SQLite for testing

    def test_save_task(self):
        task_data = TaskSerializer.serialize({"task_name": "test_task"})
        self.storage.save_task(task_data)

        task = self.storage.get_next_task()
        self.assertIsNotNone(task)
        task_id, task_data, retries, run_at, expiration = task
        self.assertEqual(
            TaskSerializer.deserialize(task_data), {"task_name": "test_task"}
        )

    def test_mark_task_in_progress(self):
        task_data = TaskSerializer.serialize({"task_name": "test_task"})
        self.storage.save_task(task_data)

        task = self.storage.get_next_task()
        task_id, task_data, retries, run_at, expiration = task

        self.storage.mark_task_in_progress(task_id)
        tasks = self.storage.get_all_tasks()
        self.assertTrue(any(task[2] == "IN_PROGRESS" for task in tasks))

    def test_mark_task_done(self):
        task_data = TaskSerializer.serialize({"task_name": "test_task"})
        self.storage.save_task(task_data)

        task = self.storage.get_next_task()
        task_id, task_data, retries, run_at, expiration = task

        self.storage.mark_task_done(task_id)
        tasks = self.storage.get_all_tasks()
        self.assertTrue(any(task[2] == "DONE" for task in tasks))

    def test_mark_task_failed(self):
        task_data = TaskSerializer.serialize({"task_name": "test_task"})
        self.storage.save_task(task_data)

        task = self.storage.get_next_task()
        task_id, task_data, retries, run_at, expiration = task

        self.storage.mark_task_failed(task_id)
        tasks = self.storage.get_all_tasks()
        self.assertTrue(any(task[2] == "FAILED" for task in tasks))

    def test_increment_task_retries(self):
        task_data = TaskSerializer.serialize({"task_name": "test_task"})
        self.storage.save_task(task_data)

        task = self.storage.get_next_task()
        task_id, task_data, retries, run_at, expiration = task

        self.storage.increment_task_retries(task_id)
        tasks = self.storage.get_all_tasks()
        retry_counts = [task[3] for task in tasks]
        self.assertTrue(1 in retry_counts)


if __name__ == "__main__":
    unittest.main()
