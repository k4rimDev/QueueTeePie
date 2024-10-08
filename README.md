# QueueTeePie

QueueTeePie is a lightweight, pluggable Python library for background task processing.
It includes features such as task scheduling, retry logic, task prioritization, and expiration handling.

## Features
- **Task Scheduling**: Schedule tasks to run at a later time.
- **Retry Logic**: Retry tasks on failure.
- **Task Priority**: Higher-priority tasks are executed first.
- **Task Expiration**: Expired tasks are removed from the queue.
- **Background Workers**: Process tasks asynchronously in the background.
- **SQLite Storage**: Default persistent storage.

## Installation

Clone the repository and install the dependencies with `Poetry`:

```bash
git clone https://github.com/yourusername/queue_tee_pie.git
cd queue_tee_pie
poetry install
```

## Basic Usage

#### Enqueue a Task

```py
from queue_tee_pie.core import TaskQueue

task_queue = TaskQueue()
task_queue.enqueue_task({'task_name': 'send_email', 'email': 'example@example.com'})
```

#### Start the Worker

```py
from queue_tee_pie.core import TaskQueue
from queue_tee_pie.workers.worker import WorkerThread

task_queue = TaskQueue()
worker = WorkerThread(task_queue)
worker.start()

# Stop the worker gracefully
worker.stop()
worker.join()
```

#### Running the Worker Script

You can run the worker from the command line using the `run_worker.py` script:

```sh
python run_worker.py
```

## License

This project is licensed under the Apache License.

---

This setup includes all of the essential components you need to get started with **QueueTeePie** as a lightweight background task processor. Let me know if you need further enhancements or specific adjustments!
