"""ポート: アプリケーションが外部に求める機能のインターフェースです."""

from typing import Protocol

from .domain import Task


class TaskRepository(Protocol):
    """タスクの保存先のポートです（駆動される側）."""

    def next_id(self) -> int:
        """次に使う ID を返します."""
        ...

    def save(self, task: Task) -> None:
        """タスクを保存します（同じ ID があれば上書きします）."""
        ...

    def get(self, task_id: int) -> Task | None:
        """ID に一致するタスクを返します. なければ None を返します."""
        ...

    def list_all(self) -> list[Task]:
        """すべてのタスクを ID の順に返します."""
        ...
