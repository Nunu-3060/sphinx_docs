"""第 10 章: 時間のかかる処理をスレッドで実行するサンプルです。

「フリーズする実行」ボタンでは、処理中に画面が反応しなくなります。
「スレッドで実行」ボタンでは、処理中も画面を操作でき、進捗も表示されます。
"""

import queue
import threading
import time
import tkinter as tk
from tkinter import ttk

STEPS = 50  # 重い処理の段階数
POLL_INTERVAL_MS = 100  # キューを確認する間隔 (ミリ秒)


def heavy_task(report: queue.Queue[int] | None = None) -> None:
    """時間のかかる処理の代わりに、少しずつ待機します (合計 5 秒)。

    report が指定された場合は、1 段階終わるごとに完了した段階数を入れます。
    この関数の中ではウィジェットを操作しません。
    """
    for step in range(1, STEPS + 1):
        time.sleep(0.1)
        if report is not None:
            report.put(step)


def main() -> None:
    """2 種類の実行方法を比べるウィンドウを表示します。"""
    root = tk.Tk()
    root.title("スレッドのサンプル")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    progress = tk.IntVar(value=0)
    status = tk.StringVar(value="待機中")
    ttk.Progressbar(frame, length=300, maximum=STEPS, variable=progress).pack(
        pady=5
    )
    ttk.Label(frame, textvariable=status).pack()

    # 処理中も画面が動いていることを確かめるための入力欄です
    ttk.Entry(frame).pack(fill="x", pady=5)

    progress_queue: queue.Queue[int] = queue.Queue()

    def set_buttons_enabled(enabled: bool) -> None:
        """2 つの実行ボタンを、まとめて操作可能または操作不可にします。"""
        for button in (blocking_button, thread_button):
            button.state(["!disabled"] if enabled else ["disabled"])

    def run_blocking() -> None:
        """メインスレッドで重い処理を実行します。終わるまで画面は反応しません。"""
        status.set("実行中 (フリーズします)")
        root.update_idletasks()  # 上の表示を反映させてから処理を始めます
        heavy_task()
        status.set("完了")

    def run_in_thread() -> None:
        """別スレッドで重い処理を実行し、進捗の確認を開始します。"""
        set_buttons_enabled(False)  # 処理の重複実行を防ぎます
        status.set("実行中 (操作できます)")
        progress.set(0)
        worker = threading.Thread(
            target=heavy_task, args=(progress_queue,), daemon=True
        )
        worker.start()
        check_queue(worker)

    def check_queue(worker: threading.Thread) -> None:
        """キューに届いた進捗を画面に反映します。メインスレッドで実行されます。"""
        # 先に生存を確認します。キューを空にした後に確認すると、その間に
        # 届いた最後の進捗を取りこぼすことがあるためです。
        alive = worker.is_alive()
        while True:
            try:
                progress.set(progress_queue.get_nowait())
            except queue.Empty:
                break
        if alive:
            root.after(POLL_INTERVAL_MS, check_queue, worker)
        else:
            status.set("完了")
            set_buttons_enabled(True)

    blocking_button = ttk.Button(
        frame, text="フリーズする実行", command=run_blocking
    )
    blocking_button.pack(fill="x", pady=2)
    thread_button = ttk.Button(
        frame, text="スレッドで実行", command=run_in_thread
    )
    thread_button.pack(fill="x", pady=2)

    root.mainloop()


if __name__ == "__main__":
    main()
