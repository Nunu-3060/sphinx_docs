"""ドメイン層: タスクとその規則を表します."""

from dataclasses import dataclass

MAX_TITLE_LENGTH = 50


class TaskError(Exception):
    """タスクの規則に反する操作をしたときに送出します."""


@dataclass
class Task:
    """タスクです."""

    task_id: int
    title: str
    done: bool = False

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise TaskError("タイトルが空です")
        if len(self.title) > MAX_TITLE_LENGTH:
            raise TaskError(f"タイトルは {MAX_TITLE_LENGTH} 文字以内です")

    def complete(self) -> None:
        """タスクを完了にします."""
        if self.done:
            raise TaskError(f"タスク {self.task_id} は完了済みです")
        self.done = True
