"""ヘキサゴナルアーキテクチャの ToDo アプリを実行します.

同じアプリケーションサービスを、2 種類の保存先のアダプターと組み合わせて
実行します。アプリケーションサービスのコードは変更しません。
"""

import tempfile
from pathlib import Path

from .adapters import (InMemoryTaskRepository, JsonFileTaskRepository,
                       TextCommandAdapter)
from .ports import TaskRepository
from .service import TaskService

COMMANDS = ["add 牛乳を買う", "add 報告書を書く", "done 2", "list"]


def run(repository: TaskRepository) -> None:
    """指定した保存先でアプリケーションを組み立て、コマンドを実行します."""
    adapter = TextCommandAdapter(TaskService(repository))
    for command in COMMANDS:
        print(f"> {command}")
        print(adapter.handle(command))


def main() -> None:
    """メモリと JSON ファイルの 2 種類の保存先で実行します."""
    print("=== メモリに保存 ===")
    run(InMemoryTaskRepository())

    print("=== JSON ファイルに保存 ===")
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "tasks.json"
        run(JsonFileTaskRepository(path))
        print(f"--- {path.name} の内容 ---")
        print(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
