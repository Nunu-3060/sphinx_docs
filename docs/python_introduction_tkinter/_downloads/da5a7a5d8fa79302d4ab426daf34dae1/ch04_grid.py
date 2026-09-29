"""第 4 章: grid によるレイアウトのサンプルです。

ラベルと入力欄を表形式に並べた入力フォームを作ります。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """grid で配置した入力フォームを表示します。"""
    root = tk.Tk()
    root.title("grid のサンプル")

    form = ttk.Frame(root, padding=10)
    form.grid(row=0, column=0, sticky="nsew")

    labels = ["氏名", "メールアドレス", "電話番号"]
    for row, caption in enumerate(labels):
        label = ttk.Label(form, text=caption)
        label.grid(row=row, column=0, sticky="w", padx=(0, 10), pady=3)

        entry = ttk.Entry(form, width=30)
        entry.grid(row=row, column=1, sticky="ew", pady=3)

    # 2 列にまたがるボタンを右寄せで配置します
    submit = ttk.Button(form, text="送信")
    submit.grid(
        row=len(labels), column=0, columnspan=2, sticky="e", pady=(10, 0)
    )

    # ウィンドウを広げたとき、入力欄の列だけが伸びるようにします
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    form.columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
