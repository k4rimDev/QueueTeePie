import json

from typing import Any


class TaskSerializer:
    """Handles serialization and deserialization of tasks."""

    @staticmethod
    def serialize(task_data: Any) -> str:
        """Serialize task data to a JSON string."""
        try:
            if isinstance(task_data, str):
                return task_data
            return json.dumps(task_data)
        except (TypeError, ValueError) as e:
            raise Exception(f"Task serialization failed: {e}") from e

    @staticmethod
    def deserialize(task_data: str) -> Any:
        """Deserialize task data from a JSON string."""
        try:
            if isinstance(task_data, dict):
                return task_data
            return json.loads(task_data)
        except (TypeError, ValueError) as e:
            raise Exception(f"Task deserialization failed: {e}") from e
