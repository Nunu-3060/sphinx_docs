"""第 3 章: Entry と Text を使うサンプルです。

Entry に入力した 1 行の文字列を、ボタンで Text の末尾に追加します。
"""

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """入力欄と複数行テキストを持つウィンドウを表示します。"""
    root = tk.Tk()
    root.title("Entry と Text")

    entry = ttk.Entry(root, width=40)
    entry.pack(padx=10, pady=(10, 5))
    entry.focus_set()  # 起動直後から入力できるようにします

    text = tk.Text(root, width=40, height=8)
    text.pack(padx=10, pady=5)

    def add_line() -> None:
        """Entry の内容を Text の末尾に追加し、Entry を空にします。"""
        value = entry.get()
        if value:
            text.insert("end", value + "\n")
            entry.delete(0, "end")

    def show_length() -> None:
        """Text に入力されている文字数をタイトルバーに表示します。"""
        # "end" は末尾の改行も含むため "end-1c" (末尾の 1 文字手前) までを取得します
        content = text.get("1.0", "end-1c")
        root.title(f"Entry と Text ({len(content)} 文字)")

    add_button = ttk.Button(root, text="追加", command=add_line)
    add_button.pack(side="left", padx=(10, 5), pady=(5, 10))

    length_button = ttk.Button(root, text="文字数", command=show_length)
    length_button.pack(side="left", padx=5, pady=(5, 10))

    root.mainloop()


if __name__ == "__main__":
    main()
