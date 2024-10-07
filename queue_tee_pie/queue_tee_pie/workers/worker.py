import threading
import time

from queue_tee_pie.core import TaskQueue
from queue_tee_pie.queue_tee_pie.utils.logger import setup_logger


class WorkerThread(threading.Thread):
    def __init__(self, task_queue: TaskQueue, logger=None, sleep_interval=5):
        """Initialize the worker thread to process tasks."""
        super().__init__()
        self.task_queue = task_queue
        self.sleep_interval = sleep_interval
        self.stop_event = threading.Event()
        self.logger = logger or setup_logger("worker", "worker.log")

    def run(self):
        """Process tasks in a loop."""
        self.logger.info("Worker thread started")
        while not self.stop_event.is_set():
            if task := self.task_queue.dequeue_task():
                task_id, task_data = task
                self.logger.info(f"Processing task {task_id}: {task_data}")
                try:
                    self.process_task(task_data)
                    self.task_queue.mark_task_done(task_id)
                    self.logger.info(f"Task {task_id} completed successfully")
                except Exception as e:
                    self.logger.error(f"Task {task_id} failed: {e}")
            else:
                self.logger.info("No tasks found, sleeping for a while...")
                time.sleep(self.sleep_interval)

    def process_task(self, task_data):
        """Simulate processing of a task (this could be extended)."""
        self.logger.info(f"Executing task: {task_data}")
        time.sleep(2)  # Simulate task processing time

    def stop(self):
        """Gracefully stop the worker."""
        self.logger.info("Stopping worker thread")
        self.stop_event.set()
