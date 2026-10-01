"""プレゼンテーション層: 利用者の入力を受け取り、結果を表示します."""

from .application import TaskService
from .domain import Task, TaskError


class TaskCli:
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
