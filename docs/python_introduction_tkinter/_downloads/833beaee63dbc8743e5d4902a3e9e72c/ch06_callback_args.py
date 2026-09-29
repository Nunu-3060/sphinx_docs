"""第 6 章: コールバック関数に引数を渡すサンプルです。

lambda と functools.partial の 2 通りの方法で、押されたボタンの数字を渡します。
"""

import tkinter as tk
from functools import partial
from tkinter import ttk


def main() -> None:
    """数字ボタンを並べた簡易テンキーを表示します。"""
    root = tk.Tk()
    root.title("コールバック関数への引数")

    display = tk.StringVar()
    ttk.Entry(
        root, textvariable=display, justify="right", state="readonly"
    ).grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

    def append_digit(digit: int) -> None:
        """押された数字を表示欄の末尾に追加します。"""
        display.set(display.get() + str(digit))

    # 方法 1: functools.partial で引数を固定した関数を作ります
    for digit in range(1, 10):
        row, column = divmod(digit - 1, 3)
        button = ttk.Button(
            root,
            text=str(digit),
            width=4,
            command=partial(append_digit, digit),
        )
        button.grid(row=row + 1, column=column, padx=2, pady=2)

    # 方法 2: lambda で引数付きの呼び出しを包みます
    zero = ttk.Button(root, text="0", width=4, command=lambda: append_digit(0))
    zero.grid(row=4, column=0, padx=2, pady=2)

    clear = ttk.Button(root, text="クリア", command=lambda: display.set(""))
    clear.grid(row=4, column=1, columnspan=2, sticky="ew", padx=2, pady=2)

    root.mainloop()


if __name__ == "__main__":
    main()
