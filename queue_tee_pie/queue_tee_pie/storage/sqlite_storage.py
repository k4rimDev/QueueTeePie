import time
import sqlite3

from queue_tee_pie.storage import BaseStorage


class SQLiteStorage(BaseStorage):
    def __init__(self, db_name="queue_tee_pie.db"):
        """Initialize the SQLite storage with the database file name."""
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        print("sasfasfds")
        self._create_table()

    def _create_table(self):
        """Create the task queue table if it does not exist."""
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS task_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_data TEXT NOT NULL,
                status TEXT DEFAULT 'PENDING',
                retries INTEGER DEFAULT 0,
                priority INTEGER DEFAULT 1,
                run_at REAL DEFAULT NULL,
                expiration REAL DEFAULT NULL
            )
        """
        )
        print("asfasdf")
        self.conn.commit()

    def save_task(self, task_data, priority=1, run_at=None, expiration=None):
        """
        Save a new task to the SQLite storage with optional
        priority,
        run_at,
        and expiration.
        """
        self.conn.execute(
            """
            INSERT INTO task_queue (task_data, priority, run_at, expiration)
            VALUES (?, ?, ?, ?)
            """,
            (task_data, priority, run_at, expiration),
        )
        self.conn.commit()

    def get_next_task(self):
        """Retrieve the next pending task based on priority and scheduled time."""
        cursor = self.conn.execute(
            """
            SELECT id, task_data, retries, run_at, expiration
            FROM task_queue
            WHERE status = 'PENDING'
            AND (run_at IS NULL OR run_at <= ?)
            ORDER BY priority DESC, run_at ASC
            LIMIT 1
        """,
            (time.time(),),
        )
        if row := cursor.fetchone():
            task_id, task_data, retries, run_at, expiration = row
            return task_id, task_data, retries, run_at, expiration

        return None

    def mark_task_in_progress(self, task_id):
        """Mark a task as in progress."""
        self.conn.execute(
            "UPDATE task_queue SET status = ? WHERE id = ?", ("IN_PROGRESS", task_id)
        )
        self.conn.commit()

    def mark_task_done(self, task_id):
        """Mark a task as done."""
        self.conn.execute(
            "UPDATE task_queue SET status = ? WHERE id = ?", ("DONE", task_id)
        )
        self.conn.commit()

    def mark_task_failed(self, task_id):
        """Mark a task as failed."""
        self.conn.execute(
            "UPDATE task_queue SET status = ? WHERE id = ?", ("FAILED", task_id)
        )
        self.conn.commit()

    def increment_task_retries(self, task_id):
        """Increment the retry count for a task."""
        self.conn.execute(
            "UPDATE task_queue SET retries = retries + 1 WHERE id = ?", (task_id,)
        )
        self.conn.commit()

    def get_all_tasks(self):
        """Retrieve all tasks with their current status."""
        cursor = self.conn.execute(
            """
            SELECT id, task_data, status, retries, priority, run_at, expiration
            FROM task_queue
        """
        )
        return cursor.fetchall()

    def requeue_task(self, task_id):
        """Requeue a task by resetting its status to 'PENDING'."""
        self.conn.execute(
            "UPDATE task_queue SET status = ?, retries = retries + 1 WHERE id = ?",
            ("PENDING", task_id),
        )
        self.conn.commit()
