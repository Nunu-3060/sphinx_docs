"""第 8 章: Notebook と Progressbar のサンプルです。

2 つのタブに、2 種類のモードの Progressbar をそれぞれ配置します。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """タブ付きのウィンドウを表示します。"""
    root = tk.Tk()
    root.title("Notebook と Progressbar")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # タブ 1: determinate モード (進み具合が分かる処理に使います)
    tab1 = ttk.Frame(notebook, padding=10)
    notebook.add(tab1, text="determinate")

    progress = tk.IntVar(value=0)
    ttk.Progressbar(
        tab1,
        orient="horizontal",
        length=240,
        mode="determinate",
        maximum=100,
        variable=progress,
    ).pack(pady=5)
    ttk.Label(tab1, textvariable=progress).pack()

    def step_forward() -> None:
        """進捗を 10 進めます。100 を超えたら 0 に戻します。"""
        progress.set((progress.get() + 10) % 110)

    ttk.Button(tab1, text="10 進める", command=step_forward).pack(pady=5)

    # タブ 2: indeterminate モード (終わりが分からない処理に使います)
    tab2 = ttk.Frame(notebook, padding=10)
    notebook.add(tab2, text="indeterminate")

    busy = ttk.Progressbar(
        tab2, orient="horizontal", length=240, mode="indeterminate"
    )
    busy.pack(pady=5)

    buttons = ttk.Frame(tab2)
    buttons.pack(pady=5)
    # start の引数は、バーを動かす間隔 (ミリ秒) です
    ttk.Button(buttons, text="開始", command=lambda: busy.start(20)).pack(
        side="left"
    )
    ttk.Button(buttons, text="停止", command=busy.stop).pack(side="left")

    root.mainloop()


if __name__ == "__main__":
    main()
