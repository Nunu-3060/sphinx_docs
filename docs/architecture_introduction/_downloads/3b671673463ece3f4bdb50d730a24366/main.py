"""レイヤードアーキテクチャの ToDo アプリを、決まったコマンドで実行します."""

from .application import TaskService
from .infrastructure import TaskTable
from .presentation import TaskCli

COMMANDS = ["add 牛乳を買う", "add 報告書を書く", "done 1", "done 1", "list"]


def main() -> None:
    """各層のオブジェクトを組み立て、コマンドを順に実行します."""
    cli = TaskCli(TaskService(TaskTable()))
    for command in COMMANDS:
        print(f"> {command}")
        print(cli.handle(command))


if __name__ == "__main__":
    main()
