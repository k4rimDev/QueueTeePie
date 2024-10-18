import time
import unittest

from queue_tee_pie.core import TaskQueue
from queue_tee_pie.queue_tee_pie.utils.serializer import TaskSerializer


class TestTaskQueueRedis(unittest.TestCase):
    def setUp(self):
        self.queue = TaskQueue(storage_backend='redis', host='localhost', port=6379, db=0)

    def test_enqueue_and_dequeue_task(self):
        task_data = {'task_name': 'redis_task', 'params': {'param1': 'value1'}}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))

        task = self.queue.dequeue_task()
        self.assertIsNotNone(task)
        task_id, task_data = task
        self.assertEqual(TaskSerializer.deserialize(task_data), {'task_name': 'redis_task', 'params': {'param1': 'value1'}})

    def test_task_expiration(self):
        task_data = {'task_name': 'expired_task'}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data), expiration=time.time() - 10)

        task = self.queue.dequeue_task()
        self.assertIsNone(task)

    def test_task_retry(self):
        task_data = {'task_name': 'retry_task'}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))

        task = self.queue.dequeue_task()
        self.assertIsNotNone(task)
        task_id, task_data = task

        self.queue.retry_task(task_id)
        tasks = self.queue.get_all_tasks()
        retry_count = [int(task["retries"]) for task in tasks]
        self.assertIn(1, retry_count)

    def test_mark_task_done(self):
        task_data = {'task_name': 'complete_task'}
        self.queue.enqueue_task(TaskSerializer.serialize(task_data))

        task = self.queue.dequeue_task()
        self.assertIsNotNone(task)
        task_id, task_data = task

        self.queue.mark_task_done(task_id)

        active_tasks = self.queue.storage.redis.zrange(self.queue.storage.queue_key, 0, -1)
        self.assertNotIn(task_id, active_tasks)

        task_info = self.queue.storage.redis.hgetall(task_id)
        self.assertEqual(task_info, {})

    def tearDown(self):
        for task in self.queue.storage.redis.keys("queue_tee_pie:task:*"):
            self.queue.storage.redis.delete(task)
        self.queue.storage.redis.zremrangebyrank(self.queue.storage.queue_key, 0, -1)
        del self.queue


if __name__ == '__main__':
    unittest.main()
