"""第 10 章: after による定期処理のサンプルです。

0.1 秒ごとに表示を更新するストップウォッチを作ります。
"""

import time
import tkinter as tk
from tkinter import ttk

INTERVAL_MS = 100  # 表示を更新する間隔 (ミリ秒)


def main() -> None:
    """ストップウォッチを表示します。"""
    root = tk.Tk()
    root.title("ストップウォッチ")

    display = tk.StringVar(value="0.0 秒")
    ttk.Label(
        root, textvariable=display, font=("Courier", 24), padding=10
    ).pack()

    start_time = 0.0  # 計測を開始した時刻
    after_id: str | None = None  # 予約中の処理の ID (停止中は None)

    def tick() -> None:
        """経過時間を表示し、INTERVAL_MS ミリ秒後に自分自身を再び予約します。"""
        nonlocal after_id
        elapsed = time.perf_counter() - start_time
        display.set(f"{elapsed:.1f} 秒")
        after_id = root.after(INTERVAL_MS, tick)

    def start() -> None:
        """計測を開始します。すでに動いている場合は何もしません。"""
        nonlocal start_time
        if after_id is None:
            start_time = time.perf_counter()
            tick()

    def stop() -> None:
        """予約中の処理を取り消して計測を止めます。"""
        nonlocal after_id
        if after_id is not None:
            root.after_cancel(after_id)
            after_id = None

    buttons = ttk.Frame(root, padding=(10, 0, 10, 10))
    buttons.pack()
    ttk.Button(buttons, text="開始", command=start).pack(side="left", padx=2)
    ttk.Button(buttons, text="停止", command=stop).pack(side="left", padx=2)

    root.mainloop()


if __name__ == "__main__":
    main()
