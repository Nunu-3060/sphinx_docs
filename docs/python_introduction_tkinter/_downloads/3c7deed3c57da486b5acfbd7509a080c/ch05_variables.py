"""第 5 章: 変数クラス (StringVar) と trace_add のサンプルです。

Entry に入力した文字列が、Label にそのまま反映されます。
入力のたびに文字数も更新します。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """入力内容と文字数をリアルタイムに表示するウィンドウを表示します。"""
    root = tk.Tk()
    root.title("変数クラスのサンプル")

    # 変数クラスは Tk オブジェクトを作成した後に作ります
    name = tk.StringVar(value="tkinter")
    length_message = tk.StringVar()

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    # Entry と Label が同じ StringVar を共有します
    ttk.Entry(frame, textvariable=name, width=30).pack(fill="x")
    ttk.Label(frame, textvariable=name).pack(anchor="w", pady=(10, 0))
    ttk.Label(frame, textvariable=length_message).pack(anchor="w")

    def update_length(*args: object) -> None:
        """name の値が変わるたびに呼ばれ、文字数の表示を更新します。

        trace_add から渡される 3 つの引数は使わないため、*args で受け取ります。
        """
        length_message.set(f"{len(name.get())} 文字")

    name.trace_add("write", update_length)
    update_length()  # 初期値の文字数を表示します

    root.mainloop()


if __name__ == "__main__":
    main()
