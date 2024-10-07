import sqlite3


class SQLiteStorage:
    def __init__(self, db_name="queue_tee_pie.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS task_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_data TEXT NOT NULL,
                status TEXT DEFAULT 'PENDING'
            )
        """
        )
        self.conn.commit()

    def save_task(self, task):
        self.conn.execute("INSERT INTO task_queue (task_data) VALUES (?)", (task,))
        self.conn.commit()

    def get_next_task(self):
        cursor = self.conn.execute(
            'SELECT id, task_data FROM task_queue WHERE status="PENDING" LIMIT 1'
        )
        row = cursor.fetchone()
        if row:
            task_id, task_data = row
            self.conn.execute(
                'UPDATE task_queue SET status="IN_PROGRESS" WHERE id=?', (task_id,)
            )
            self.conn.commit()
            return task_id, task_data
        return None
