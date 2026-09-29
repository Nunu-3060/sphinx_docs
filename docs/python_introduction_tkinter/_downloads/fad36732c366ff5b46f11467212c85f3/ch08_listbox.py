"""第 8 章: Listbox と Scrollbar のサンプルです。

項目の追加と削除ができるリストを作ります。
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """項目を編集できるリストを表示します。"""
    root = tk.Tk()
    root.title("Listbox のサンプル")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    # exportselection=False: Entry で文字列を選択しても、リストの選択を解除しません
    listbox = tk.Listbox(
        frame, height=8, selectmode="extended", exportselection=False
    )
    listbox.grid(row=0, column=0, columnspan=2, sticky="nsew")

    # Scrollbar と Listbox を互いに連携させます
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=listbox.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")
    listbox.configure(yscrollcommand=scrollbar.set)

    fruits = ["りんご", "みかん", "ぶどう", "もも", "なし", "かき", "いちご"]
    for fruit in fruits:
        listbox.insert("end", fruit)

    entry = ttk.Entry(frame)
    entry.grid(row=1, column=0, sticky="ew", pady=(5, 0))

    status = tk.StringVar(value="項目を選択してください")
    ttk.Label(frame, textvariable=status).grid(
        row=2, column=0, columnspan=3, sticky="w", pady=(5, 0)
    )

    def add_item() -> None:
        """入力欄の文字列をリストの末尾に追加します。"""
        value = entry.get().strip()
        if value:
            listbox.insert("end", value)
            listbox.see("end")  # 追加した項目が見えるようにスクロールします
            entry.delete(0, "end")

    def delete_selected() -> None:
        """選択されている項目をすべて削除します。"""
        # 前から削除すると後ろの番号がずれるため、後ろから削除します
        for index in reversed(listbox.curselection()):
            listbox.delete(index)
        # プログラムから削除しても <<ListboxSelect>> は発生しないため、
        # 表示を自分で更新します
        show_selection()

    def show_selection() -> None:
        """選択中の項目をラベルに表示します。"""
        selected = [listbox.get(index) for index in listbox.curselection()]
        if selected:
            status.set("選択中: " + "、".join(selected))
        else:
            status.set("項目を選択してください")

    def on_select(event: tk.Event[tk.Misc]) -> None:
        """選択が変わったときに呼ばれます。"""
        show_selection()

    ttk.Button(frame, text="追加", command=add_item).grid(
        row=1, column=1, columnspan=2, sticky="ew", padx=(5, 0), pady=(5, 0)
    )
    ttk.Button(frame, text="選択した項目を削除", command=delete_selected).grid(
        row=3, column=0, columnspan=3, sticky="ew", pady=(5, 0)
    )
    listbox.bind("<<ListboxSelect>>", on_select)

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
