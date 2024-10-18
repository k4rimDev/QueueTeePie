import redis
import json
import time

from queue_tee_pie.queue_tee_pie.storage import BaseStorage


class RedisStorage(BaseStorage):
    def __init__(self, host='localhost', port=6379, db=0):
        """Initialize Redis connection."""
        self.redis = redis.StrictRedis(host=host, port=6379, db=db, decode_responses=True)
        self.queue_key = "queue_tee_pie:task_queue"
        self.task_prefix = "queue_tee_pie:task:"

    def _sanitize_task_info(self, task_info):
        """Convert None values to empty strings or remove them."""
        return {k: (v if v is not None else '') for k, v in task_info.items()}

    def save_task(self, task_data, priority=1, run_at=None, expiration=None):
        """Save a new task to the Redis queue."""
        task_id = f"{self.task_prefix}{int(time.time() * 1000)}"
        task_info = {
            "task_data": task_data,
            "status": "PENDING",
            "retries": 0,
            "priority": priority,
            "run_at": run_at if run_at else time.time(),
            "expiration": expiration
        }

        # Sanitize task info to ensure no None values
        sanitized_task_info = self._sanitize_task_info(task_info)
        self.redis.hset(task_id, mapping=sanitized_task_info)
        self.redis.zadd(self.queue_key, {task_id: priority})

    def get_next_task(self):
        """Retrieve the next task from the Redis queue based on priority."""
        task_ids = self.redis.zrange(self.queue_key, 0, 0)
        if not task_ids:
            return None
        task_id = task_ids[0]
        task_info = self.redis.hgetall(task_id)

        if task_info:
            if task_info.get("expiration") and float(task_info["expiration"]) < time.time():
                self.redis.zrem(self.queue_key, task_id)
                self.redis.delete(task_id)
                return None

            if float(task_info.get("run_at", 0)) > time.time():
                return None

            return task_id, json.loads(task_info["task_data"]), int(task_info["retries"]), task_info["run_at"], task_info["expiration"]

        return None

    def mark_task_in_progress(self, task_id):
        """Mark a task as in-progress."""
        self.redis.hset(task_id, "status", "IN_PROGRESS")

    def mark_task_done(self, task_id):
        """Mark a task as done and remove it from the Redis queue."""
        self.redis.hset(task_id, "status", "DONE")
        self.redis.zrem(self.queue_key, task_id)
        self.redis.delete(task_id)

    def mark_task_failed(self, task_id):
        """Mark a task as failed."""
        self.redis.hset(task_id, "status", "FAILED")
        self.redis.zrem(self.queue_key, task_id)

    def increment_task_retries(self, task_id):
        """Increment the retry count of a task."""
        self.redis.hincrby(task_id, "retries", 1)

    def get_all_tasks(self):
        """Get all tasks for monitoring or debugging."""
        task_ids = self.redis.zrange(self.queue_key, 0, -1)
        tasks = [self.redis.hgetall(task_id) for task_id in task_ids]
        return tasks

    def requeue_task(self, task_id):
        """Requeue a failed task by resetting its status and incrementing retries."""
        self.increment_task_retries(task_id)
        self.redis.hset(task_id, "status", "PENDING")
        self.redis.zadd(self.queue_key, {task_id: self.redis.hget(task_id, "priority")})
