import time

from queue_tee_pie.storage.sqlite_storage import SQLiteStorage
from queue_tee_pie.utils.serializer import TaskSerializer


class TaskQueue:
    def __init__(self, storage_backend=None, max_retries=3, retry_backoff=5):
        """
        Initialize the task queue with a storage backend.

        :param storage_backend: Optional storage backend (SQLiteStorage by default)
        :param max_retries: Number of times a task can be retried on failure
        :param retry_backoff: Time to wait between retries, in seconds
        """
        self.storage = storage_backend or SQLiteStorage()
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff

    def enqueue_task(self, task_data, priority=1, run_at=None, expiration=None):
        """
        Enqueue a task to the queue with optional scheduling, priority, and expiration.

        :param task_data: Task data to be serialized and saved
        :param priority: Task priority (higher number = higher priority)
        :param run_at: Optional timestamp for delayed execution
        :param expiration: Optional expiration timestamp
        """
        serialized_task = TaskSerializer.serialize(task_data)
        self.storage.save_task(serialized_task, priority, run_at, expiration)

    def dequeue_task(self):
        """
        Dequeue the first pending task, handling retries if the task fails.

        :return: Tuple of (task_id, task_data), or None if no task is found
        """
        if task := self.storage.get_next_task():
            task_id, serialized_task, retries, run_at, expiration = task
            if self.is_task_expired(expiration):
                self.storage.mark_task_done(task_id)
                return None

            if retries >= self.max_retries:
                self.storage.mark_task_failed(task_id)
                return None

            self.storage.mark_task_in_progress(task_id)
            task_data = TaskSerializer.deserialize(serialized_task)
            return task_id, task_data
        return None

    def mark_task_done(self, task_id):
        """Mark a task as completed."""
        self.storage.mark_task_done(task_id)

    def mark_task_failed(self, task_id):
        """Mark a task as failed after retry limits are reached."""
        self.storage.mark_task_failed(task_id)

    def retry_task(self, task_id):
        """Requeue the task after a failure with a backoff."""
        self.storage.increment_task_retries(task_id)
        time.sleep(self.retry_backoff)

    def is_task_expired(self, expiration):
        """
        Check if a task has expired.

        :param expiration: Expiration timestamp of the task
        :return: True if the task is expired, False otherwise
        """
        return bool(expiration and time.time() > expiration)

    def get_all_tasks(self):
        """
        Retrieve all tasks for monitoring or debugging purposes.

        :return: List of all tasks with their current status
        """
        return self.storage.get_all_tasks()


# Example usage of TaskQueue
if __name__ == "__main__":
    task_queue = TaskQueue()

    # Add a task to the queue
    task_data = {"task_name": "example_task", "params": {"param1": "value1"}}
    task_queue.enqueue_task(task_data, priority=2)

    if task := task_queue.dequeue_task():
        task_id, task_data = task
        print(f"Processing task {task_id}: {task_data}")
        task_queue.mark_task_done(task_id)
