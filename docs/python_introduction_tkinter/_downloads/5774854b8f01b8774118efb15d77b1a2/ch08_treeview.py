"""第 8 章: Treeview のサンプルです。

左側に木構造 (分類)、右側に表形式 (一覧) の Treeview を並べます。
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

# (分類, 商品名, 価格, 在庫数) の一覧です
PRODUCTS: list[tuple[str, str, int, int]] = [
    ("果物", "りんご", 150, 30),
    ("果物", "バナナ", 100, 50),
    ("果物", "ぶどう", 400, 10),
    ("野菜", "キャベツ", 200, 15),
    ("野菜", "にんじん", 80, 40),
    ("飲料", "お茶", 120, 60),
]


def main() -> None:
    """木構造と表形式の Treeview を表示します。"""
    root = tk.Tk()
    root.title("Treeview のサンプル")

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    # 木構造: 分類ごとに商品を子要素として追加します
    tree = ttk.Treeview(frame, height=10)
    tree.heading("#0", text="分類")
    tree.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

    categories: dict[str, str] = {}
    for category, name, _price, _stock in PRODUCTS:
        if category not in categories:
            # 親要素は "" です。戻り値の ID を子要素の追加に使います。
            categories[category] = tree.insert(
                "", "end", text=category, open=True
            )
        tree.insert(categories[category], "end", text=name)

    # 表形式: show="headings" で先頭の木構造の列を非表示にします
    columns = ("name", "price", "stock")
    table = ttk.Treeview(
        frame, columns=columns, show="headings", height=10, selectmode="browse"
    )
    table.heading("name", text="商品名")
    table.heading("price", text="価格 (円)")
    table.heading("stock", text="在庫数")
    table.column("name", width=120)
    table.column("price", width=80, anchor="e")
    table.column("stock", width=80, anchor="e")
    table.grid(row=0, column=1, sticky="nsew")

    for _category, name, price, stock in PRODUCTS:
        table.insert("", "end", values=(name, price, stock))

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    scrollbar.grid(row=0, column=2, sticky="ns")
    table.configure(yscrollcommand=scrollbar.set)

    status = tk.StringVar(value="表の行を選択してください")
    ttk.Label(frame, textvariable=status).grid(
        row=1, column=0, columnspan=3, sticky="w", pady=(5, 0)
    )

    def on_select(event: tk.Event[tk.Misc]) -> None:
        """選択された行の値を表示します。"""
        selected = table.selection()  # 選択された行の ID のタプル
        if not selected:
            return
        item_id = selected[0]
        # set(行の ID, 列名) で、その行の指定した列の値を取得します
        name = table.set(item_id, "name")
        price = table.set(item_id, "price")
        stock = table.set(item_id, "stock")
        status.set(f"{name}: {price} 円、在庫 {stock} 個")

    table.bind("<<TreeviewSelect>>", on_select)

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    root.mainloop()


if __name__ == "__main__":
    main()
