from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def save_task(self, task_data, priority=1, run_at=None, expiration=None):
        """
        Save a new task to the storage with optional priority,
        run_at (schedule time), and expiration.

        :param task_data: Serialized task data to be stored.
        :param priority: Task priority (higher numbers = higher priority).
        :param run_at: Timestamp for scheduled execution (None means immediate execution).
        :param expiration: Timestamp for when the task expires (None means no expiration).
        """
        pass

    @abstractmethod
    def get_next_task(self):
        """
        Get the next pending task from the storage.

        The task should be selected based on its priority and scheduling time (run_at).
        Only tasks whose run_at time has passed should be considered.

        :return: Tuple (task_id, task_data, retries, run_at, expiration), or None
        if no task is available.
        """
        pass

    @abstractmethod
    def mark_task_in_progress(self, task_id):
        """
        Mark the task as in-progress in the storage.

        :param task_id: The ID of the task to mark as in-progress.
        """
        pass

    @abstractmethod
    def mark_task_done(self, task_id):
        """
        Mark the task as done in the storage.

        :param task_id: The ID of the task to mark as done.
        """
        pass

    @abstractmethod
    def mark_task_failed(self, task_id):
        """
        Mark the task as failed in the storage.

        This method is called when a task has exceeded its retry limit
        or encounters an unrecoverable error.

        :param task_id: The ID of the task to mark as failed.
        """
        pass

    @abstractmethod
    def increment_task_retries(self, task_id):
        """
        Increment the retry count of the task in the storage.

        :param task_id: The ID of the task whose retries need to be incremented.
        """
        pass

    @abstractmethod
    def get_all_tasks(self):
        """
        Retrieve all tasks from the storage, including their
        status, retries, priority, run_at, and expiration.

        :return: List of tuples containing all task details.
        """
        pass

    @abstractmethod
    def requeue_task(self, task_id):
        """
        Requeue a task by resetting its status to 'PENDING' and incrementing its retries.

        :param task_id: The ID of the task to be requeued.
        """
        pass
