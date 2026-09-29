"""第 3 章: Label と Button を使うサンプルです。

ボタンを押した回数をラベルに表示します。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """クリック回数を数えるウィンドウを表示します。"""
    root = tk.Tk()
    root.title("Label と Button")

    count = 0

    label = ttk.Label(root, text="ボタンを押してください")
    label.pack(padx=20, pady=10)

    def on_click() -> None:
        """ボタンが押されたときに呼ばれ、回数を 1 増やして表示します。"""
        nonlocal count
        count += 1
        label.configure(text=f"{count} 回押されました")

    # command には関数そのものを渡します。on_click() と書かないことに注意します。
    count_button = ttk.Button(root, text="押す", command=on_click)
    count_button.pack(padx=20, pady=5)

    quit_button = ttk.Button(root, text="終了", command=root.destroy)
    quit_button.pack(padx=20, pady=(5, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
