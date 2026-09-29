"""第 7 章: Toplevel で独自のダイアログを作るサンプルです。

モーダルダイアログ (閉じるまで元のウィンドウを操作できないダイアログ) を作り、
入力された値を呼び出し元に返します。
"""

import tkinter as tk
from tkinter import ttk


def ask_age(parent: tk.Misc) -> int | None:
    """年齢を入力するモーダルダイアログを表示します。

    OK が押された場合は入力された年齢を、キャンセルされた場合は None を返します。
    """
    dialog = tk.Toplevel(parent)
    dialog.title("年齢の入力")
    dialog.resizable(False, False)
    dialog.transient(parent.winfo_toplevel())  # 親ウィンドウの手前に表示します

    age = tk.IntVar(value=20)
    result: int | None = None

    frame = ttk.Frame(dialog, padding=10)
    frame.pack()
    ttk.Label(frame, text="年齢").grid(row=0, column=0, padx=(0, 10))
    spinbox = ttk.Spinbox(frame, from_=0, to=120, textvariable=age, width=5)
    spinbox.grid(row=0, column=1)

    def on_ok() -> None:
        """入力値を結果に設定してダイアログを閉じます。"""
        nonlocal result
        try:
            value = age.get()
        except tk.TclError:  # 数値以外が入力された場合
            value = -1  # 範囲外の値として扱います
        if not 0 <= value <= 120:
            spinbox.focus_set()
            return
        result = value
        dialog.destroy()

    buttons = ttk.Frame(frame)
    buttons.grid(row=1, column=0, columnspan=2, pady=(10, 0))
    ttk.Button(buttons, text="OK", command=on_ok).pack(side="left", padx=2)
    ttk.Button(buttons, text="キャンセル", command=dialog.destroy).pack(
        side="left", padx=2
    )

    spinbox.focus_set()
    dialog.wait_visibility()  # grab_set は表示後でないと失敗することがあります
    dialog.grab_set()  # 他のウィンドウへの操作を受け付けないようにします
    dialog.wait_window()  # ダイアログが閉じられるまで待ちます
    return result


def main() -> None:
    """ダイアログを呼び出すボタンを持つウィンドウを表示します。"""
    root = tk.Tk()
    root.title("独自ダイアログ")

    message = tk.StringVar(value="ボタンを押してください")
    ttk.Label(root, textvariable=message, padding=10).pack()

    def on_click() -> None:
        """ダイアログを表示し、結果をラベルに反映します。"""
        age = ask_age(root)
        if age is None:
            message.set("キャンセルされました")
        else:
            message.set(f"{age} 歳が入力されました")

    ttk.Button(root, text="年齢を入力...", command=on_click).pack(pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
