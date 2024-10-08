# QueueTeePie

**QueueTeePie** is a lightweight Python library for background task processing. It provides an easy way to enqueue tasks, handle task retries, scheduling, and task priorities, and run workers to process tasks in the background.

## Features

- **Task Scheduling**: Set `run_at` for delayed task execution.
- **Retry Logic**: Retry tasks on failure with configurable backoff.
- **Task Priority**: Prioritize tasks for execution.
- **Task Expiration**: Set expiration times for tasks.
- **SQLite-based Storage**: Persistent storage for task data using SQLite.
- **Pluggable Storage**: Support for different storage backends (e.g., Redis, MongoDB).
