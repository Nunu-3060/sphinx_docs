"""第 4 章: Frame の入れ子と、ウィンドウサイズの変更に追従するレイアウトのサンプルです。

上部のツールバー (pack) と、下部の編集領域 (grid) を Frame で分けて配置します。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """サイズ変更に追従するウィンドウを表示します。"""
    root = tk.Tk()
    root.title("サイズ変更に追従するレイアウト")
    root.geometry("480x320")

    # ツールバー: ボタンを横一列に並べるので pack を使います
    toolbar = ttk.Frame(root, padding=5)
    toolbar.pack(side="top", fill="x")
    for caption in ["新規", "開く", "保存"]:
        ttk.Button(toolbar, text=caption).pack(side="left", padx=2)

    # 編集領域: Text と Scrollbar を並べるので grid を使います
    body = ttk.Frame(root, padding=5)
    body.pack(side="top", fill="both", expand=True)

    text = tk.Text(body, wrap="none")
    text.grid(row=0, column=0, sticky="nsew")

    y_scroll = ttk.Scrollbar(body, orient="vertical", command=text.yview)
    y_scroll.grid(row=0, column=1, sticky="ns")
    text.configure(yscrollcommand=y_scroll.set)

    # 0 行 0 列 (Text のセル) だけが余った領域を受け取ります
    body.rowconfigure(0, weight=1)
    body.columnconfigure(0, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
