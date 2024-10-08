from queue_tee_pie.core import TaskQueue
from queue_tee_pie.queue_tee_pie.workers.worker import WorkerThread


task_queue = TaskQueue()


worker = WorkerThread(task_queue)
worker.start()


try:
    while True:
        pass
except KeyboardInterrupt:
    worker.stop()
    worker.join()
