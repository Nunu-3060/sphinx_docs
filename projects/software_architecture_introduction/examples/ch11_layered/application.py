"""アプリケーション層: ユースケースを実装します.

下位のインフラストラクチャ層の TaskTable に直接依存しています。
保存先を変えると、この層も変更する必要があります。
"""

from .domain import Task, TaskError
from .infrastructure import TaskRow, TaskTable


class TaskService:
    """タスクの追加、完了、一覧のユースケースです."""

    def __init__(self, table: TaskTable) -> None:
        self._table = table

    def add(self, title: str) -> Task:
        """タスクを追加します."""
        task = Task(self._table.next_id(), title)
        self._table.upsert(_to_row(task))
        return task

    def complete(self, task_id: int) -> Task:
        """タスクを完了にします."""
        row = self._table.select(task_id)
        if row is None:
            raise TaskError(f"タスク {task_id} はありません")
        task = _to_task(row)
        task.complete()
        self._table.upsert(_to_row(task))
        return task

    def list_all(self) -> list[Task]:
        """すべてのタスクを返します."""
        return [_to_task(row) for row in self._table.select_all()]


def _to_row(task: Task) -> TaskRow:
    """タスクをテーブルの行に変換します."""
    return {"task_id": task.task_id, "title": task.title, "done": task.done}


def _to_task(row: TaskRow) -> Task:
    """テーブルの行をタスクに変換します."""
    return Task(row["task_id"], row["title"], row["done"])
