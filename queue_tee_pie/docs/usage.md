# Usage Guide

## Installation

To install **QueueTeePie**, clone the repository and install the dependencies using `Poetry`.

```bash
git clone https://github.com/k4rimDev/QueueTeePie.git
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
