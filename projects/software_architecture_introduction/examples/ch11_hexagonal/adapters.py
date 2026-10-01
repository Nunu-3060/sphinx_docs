"""アダプター: ポートと外部の世界をつなぎます.

* InMemoryTaskRepository, JsonFileTaskRepository: 保存先のアダプター
  （アプリケーションから駆動される側）
* TextCommandAdapter: 文字列のコマンドを受け付けるアダプター
  （アプリケーションを駆動する側）
"""

import copy
import json
from pathlib import Path

from .domain import Task, TaskError
from .service import TaskService


class InMemoryTaskRepository:
    """タスクをメモリ上に保存します."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}

    def next_id(self) -> int:
        return max(self._tasks, default=0) + 1

    def save(self, task: Task) -> None:
        self._tasks[task.task_id] = copy.copy(task)

    def get(self, task_id: int) -> Task | None:
        task = self._tasks.get(task_id)
        return copy.copy(task) if task is not None else None

    def list_all(self) -> list[Task]:
        return [copy.copy(self._tasks[key]) for key in sorted(self._tasks)]


class JsonFileTaskRepository:
    """タスクを JSON ファイルに保存します."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def next_id(self) -> int:
        return max((task.task_id for task in self.list_all()), default=0) + 1

    def save(self, task: Task) -> None:
        tasks = {item.task_id: item for item in self.list_all()}
        tasks[task.task_id] = task
        data = [
            {"task_id": item.task_id, "title": item.title, "done": item.done}
            for item in sorted(tasks.values(), key=lambda t: t.task_id)
        ]
        self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                              encoding="utf-8")

    def get(self, task_id: int) -> Task | None:
        for task in self.list_all():
            if task.task_id == task_id:
                return task
        return None

    def list_all(self) -> list[Task]:
        if not self._path.exists():
            return []
        data = json.loads(self._path.read_text(encoding="utf-8"))
        return [Task(item["task_id"], item["title"], item["done"])
                for item in data]


class TextCommandAdapter:
    """「add タイトル」「done 番号」「list」の 3 つのコマンドを受け付けます."""

    def __init__(self, service: TaskService) -> None:
        self._service = service

    def handle(self, line: str) -> str:
        """1 行のコマンドを実行し、表示する文字列を返します."""
        command, _, argument = line.partition(" ")
        try:
            if command == "add":
                task = self._service.add(argument)
                return f"追加しました: {_format(task)}"
            if command == "done":
                task = self._service.complete(int(argument))
                return f"完了にしました: {_format(task)}"
            if command == "list":
                tasks = self._service.list_all()
                return "\n".join(_format(task) for task in tasks) or "（なし）"
            return f"不明なコマンドです: {command}"
        except (TaskError, ValueError) as error:
            return f"エラー: {error}"


def _format(task: Task) -> str:
    mark = "x" if task.done else " "
    return f"[{mark}] {task.task_id}. {task.title}"
