"""第 4 章: pack によるレイアウトのサンプルです。

side, fill, expand の違いを色付きのラベルで確認します。
"""

import tkinter as tk


def main() -> None:
    """pack の主なオプションを使ったウィンドウを表示します。"""
    root = tk.Tk()
    root.title("pack のサンプル")
    root.geometry("360x240")

    # 背景色を付けるため、ここでは ttk ではなく tk の Label を使います
    top = tk.Label(root, text="side=top, fill=x", bg="lightblue")
    top.pack(side="top", fill="x")

    bottom = tk.Label(root, text="side=bottom, fill=x", bg="lightgreen")
    bottom.pack(side="bottom", fill="x")

    left = tk.Label(root, text="side=left\nfill=y", bg="khaki")
    left.pack(side="left", fill="y")

    center = tk.Label(root, text="fill=both, expand=True", bg="lightpink")
    center.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
