"""第 2 章: ウィンドウを表示し、タイトルやサイズを設定するサンプルです。"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """設定を加えたウィンドウを表示します。"""
    root = tk.Tk()

    # ウィンドウの設定
    root.title("はじめてのウィンドウ")  # タイトルバーの文字列
    root.geometry("400x200+100+100")  # 幅 x 高さ + x 座標 + y 座標
    root.minsize(300, 150)  # ユーザーが縮められる最小サイズ
    root.resizable(True, False)  # 横方向のみサイズ変更を許可

    label = ttk.Label(root, text="Hello, tkinter!")
    label.pack(expand=True)

    # イベントループを開始します。ウィンドウを閉じるまでここで待ちます。
    root.mainloop()


if __name__ == "__main__":
    main()
