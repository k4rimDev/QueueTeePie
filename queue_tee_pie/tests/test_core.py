import unittest

from queue_tee_pie.core import TaskQueue


class TestTaskQueue(unittest.TestCase):
    def setUp(self):
        self.queue = TaskQueue()

    def test_enqueue_task(self):
        self.queue.enqueue_task("Task 1")
        task = self.queue.dequeue_task()
        self.assertIsNotNone(task)
        self.assertEqual(task[1], "Task 1")

    def test_dequeue_empty_queue(self):
        task = self.queue.dequeue_task()
        self.assertIsNone(task)


if __name__ == "__main__":
    unittest.main()
