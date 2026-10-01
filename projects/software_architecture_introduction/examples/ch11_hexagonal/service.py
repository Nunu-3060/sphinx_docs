"""アプリケーションサービス: ユースケースを実装します.

保存先はポート（TaskRepository）としてだけ知っており、具体的な保存方法
（メモリ、JSON ファイル、データベース）には依存しません。
"""

from .domain import Task, TaskError
from .ports import TaskRepository


class TaskService:
    """タスクの追加、完了、一覧のユースケースです."""

    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def add(self, title: str) -> Task:
        """タスクを追加します."""
        task = Task(self._repository.next_id(), title)
        self._repository.save(task)
        return task

    def complete(self, task_id: int) -> Task:
        """タスクを完了にします."""
        task = self._repository.get(task_id)
        if task is None:
            raise TaskError(f"タスク {task_id} はありません")
        task.complete()
        self._repository.save(task)
        return task

    def list_all(self) -> list[Task]:
        """すべてのタスクを返します."""
        return self._repository.list_all()
