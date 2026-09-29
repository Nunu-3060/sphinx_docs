"""第 4 章: place によるレイアウトのサンプルです。

絶対座標による配置と、ウィンドウに対する相対位置による配置を比較します。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """place で配置したウィジェットを表示します。"""
    root = tk.Tk()
    root.title("place のサンプル")
    root.geometry("360x240")

    # 左上から (20, 20) の位置に固定します。ウィンドウの大きさを変えても動きません。
    fixed = ttk.Label(root, text="x=20, y=20")
    fixed.place(x=20, y=20)

    # ウィンドウの中央に配置します。ウィンドウの大きさに合わせて移動します。
    center = ttk.Button(root, text="relx=0.5, rely=0.5")
    center.place(relx=0.5, rely=0.5, anchor="center")

    # 右下の角から 10 ピクセル内側に配置します
    corner = ttk.Label(root, text="右下")
    corner.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

    root.mainloop()


if __name__ == "__main__":
    main()
