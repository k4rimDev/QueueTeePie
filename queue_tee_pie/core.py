from queue_tee_pie.queue_tee_pie.storage.sqlite_storage import SQLiteStorage


class TaskQueue:
    def __init__(self, storage_backend=None):
        # Use SQLite as default storage backend
        self.storage = storage_backend or SQLiteStorage()

    def enqueue_task(self, task):
        """Enqueue a task to the queue."""
        self.storage.save_task(task)

    def dequeue_task(self):
        """Dequeue the first pending task."""
        return self.storage.get_next_task()
