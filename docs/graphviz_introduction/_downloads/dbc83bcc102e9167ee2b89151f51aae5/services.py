"""タスクの追加や検索などの処理をまとめる."""

from . import models, storage


class TaskService:
    """タスクを操作する処理を提供する."""

    def __init__(self, store: storage.MemoryStorage) -> None:
        """タスクの保存先を受け取る."""
        self._store = store

    def add(self, title: str) -> models.Task:
        """タスクを追加し、追加したタスクを返す."""
        task = models.Task(title)
        self._store.add(task)
        return task

    def pending(self) -> list[models.Task]:
        """完了していないタスクを返す."""
        return [task for task in self._store.all() if not task.done]
