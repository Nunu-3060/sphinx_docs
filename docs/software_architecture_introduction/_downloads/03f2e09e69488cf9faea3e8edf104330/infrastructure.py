"""インフラストラクチャ層: データの保存を受け持ちます.

ここでは、データベースのテーブルの代わりに辞書を使います。
"""

from typing import TypedDict


class TaskRow(TypedDict):
    """テーブルの 1 行です."""

    task_id: int
    title: str
    done: bool


class TaskTable:
    """タスクを保存するテーブルです."""

    def __init__(self) -> None:
        self._rows: dict[int, TaskRow] = {}

    def next_id(self) -> int:
        """次に使う ID を返します."""
        return max(self._rows, default=0) + 1

    def upsert(self, row: TaskRow) -> None:
        """行を追加または更新します."""
        self._rows[row["task_id"]] = row.copy()

    def select(self, task_id: int) -> TaskRow | None:
        """ID に一致する行を返します. なければ None を返します."""
        row = self._rows.get(task_id)
        return row.copy() if row is not None else None

    def select_all(self) -> list[TaskRow]:
        """すべての行を ID の順に返します."""
        return [self._rows[key].copy() for key in sorted(self._rows)]
