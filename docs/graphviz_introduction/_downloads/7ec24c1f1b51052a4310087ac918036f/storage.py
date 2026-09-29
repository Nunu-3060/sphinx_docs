"""タスクを保存する."""

from . import models


class MemoryStorage:
    """タスクをメモリー上のリストに保存する."""

    def __init__(self) -> None:
        """空の保存先を作る."""
        self._tasks: list[models.Task] = []

    def add(self, task: models.Task) -> None:
        """タスクを保存する."""
        self._tasks.append(task)

    def all(self) -> list[models.Task]:
        """保存されているすべてのタスクを返す."""
        return list(self._tasks)
