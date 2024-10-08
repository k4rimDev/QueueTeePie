import time
import unittest

from queue_tee_pie.core import TaskQueue
from queue_tee_pie.queue_tee_pie.utils.serializer import TaskSerializer


class TestTaskQueue(unittest.TestCase):
    def setUp(self):
        self.queue = TaskQueue()

    def test_enqueue_task(self):
        task_data = {"task_name": "test_task"}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))

        task = self.queue.dequeue_task()
        self.assertIsNotNone(task)
        task_id, task_data = task
        self.assertEqual(
            TaskSerializer.deserialize(task_data), {"task_name": "test_task"}
        )

    def test_dequeue_empty_queue(self):
        task = self.queue.dequeue_task()
        self.assertIsNone(task)

    def test_mark_task_done(self):
        task_data = {"task_name": "test_task"}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))

        task = self.queue.dequeue_task()
        self.assertIsNotNone(task)
        task_id, task_data = task

        self.queue.mark_task_done(task_id)
        tasks = self.queue.get_all_tasks()
        self.assertTrue(any(task[2] == "DONE" for task in tasks))

    def test_retry_task(self):
        task_data = {"task_name": "test_task"}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))
        task = self.queue.dequeue_task()
        self.assertIsNotNone(task)
        task_id, task_data = task
        self.queue.retry_task(task_id)
        tasks = self.queue.get_all_tasks()
        retries = [task[3] for task in tasks]
        self.assertIn(1, retries)

    def test_expired_task(self):
        task_data = {"task_name": "test_task"}
        self.queue.enqueue_task(
            TaskSerializer.serialize(task_data), expiration=time.time() - 60
        )

        task = self.queue.dequeue_task()
        self.assertIsNone(task)


if __name__ == "__main__":
    unittest.main()
