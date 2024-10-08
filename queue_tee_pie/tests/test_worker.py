import time
import unittest

from queue_tee_pie.core import TaskQueue
from queue_tee_pie.queue_tee_pie.workers.worker import WorkerThread
from queue_tee_pie.queue_tee_pie.utils.serializer import TaskSerializer


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.queue = TaskQueue()

    def test_worker_processes_task(self):
        task_data = {"task_name": "test_task"}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))

        worker = WorkerThread(self.queue)
        worker.start()

        time.sleep(1)

        task = self.queue.dequeue_task()
        self.assertIsNone(task)

        worker.stop()
        worker.join()

    def test_worker_retries_failed_task(self):
        def failing_task(task_data):
            raise Exception("Simulated task failure")

        task_data = {"task_name": "test_task"}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))

        worker = WorkerThread(self.queue)
        worker.process_task = failing_task

        worker.start()
        retries_checked = False
        for _ in range(10):
            time.sleep(1)
            tasks = self.queue.get_all_tasks()
            retry_count = [task[3] for task in tasks]
            if 1 in retry_count:
                retries_checked = True
                break
        self.assertTrue(
            retries_checked, "The worker did not retry the task as expected."
        )
        worker.stop()
        worker.join()


if __name__ == "__main__":
    unittest.main()
