"""アプリケーションの入口.

examples/py フォルダーで python -m sample_app.main を実行すると動作する。
"""

from . import services, storage


def main() -> None:
    """タスクを追加し、未完了のタスクを表示する."""
    service = services.TaskService(storage.MemoryStorage())
    service.add("資料を作る")
    service.add("レビューを受ける")
    for task in service.pending():
        print(task.title)


if __name__ == "__main__":
    main()
