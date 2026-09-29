"""第 1 章: tkinter が使えるかを確認するサンプルです。

Tcl/Tk のバージョンをコンソールに表示し、同じ内容を小さなウィンドウにも表示します。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """バージョン情報をコンソールとウィンドウに表示します。"""
    message = (
        f"Tcl のバージョン: {tk.TclVersion}\nTk のバージョン: {tk.TkVersion}"
    )
    print(message)

    root = tk.Tk()
    root.title("バージョン確認")

    label = ttk.Label(root, text=message, padding=20)
    label.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
