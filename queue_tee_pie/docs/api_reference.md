# API Reference

This document outlines the API for **QueueTeePie** and provides details on the methods available for managing and processing tasks in the queue.

## TaskQueue Class

### `enqueue_task(self, task_data, priority=1, run_at=None, expiration=None)`
- **Description**: Enqueues a new task to the queue.
- **Parameters**:
  - `task_data`: The data of the task to be serialized and stored.
  - `priority`: Priority of the task (default is 1).
  - `run_at`: (Optional) A timestamp to schedule the task for execution in the future.
  - `expiration`: (Optional) A timestamp for when the task should expire.

### `dequeue_task(self)`
- **Description**: Dequeues the next task from the queue, considering priority and scheduling.
- **Returns**: A tuple `(task_id, task_data)` or `None` if no task is available.

### `mark_task_done(self, task_id)`
- **Description**: Marks a task as done.

### `mark_task_failed(self, task_id)`
- **Description**: Marks a task as failed.

### `retry_task(self, task_id)`
- **Description**: Retries a task after a failure.

### `get_all_tasks(self)`
- **Description**: Retrieves all tasks from the queue.

## WorkerThread Class

### `run(self)`
- **Description**: The main loop where the worker continuously pulls tasks from the queue.

### `process_task(self, task_data)`
- **Description**: The logic for processing a single task.

### `stop(self)`
- **Description**: Stops the worker thread.
