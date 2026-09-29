"""第 5 章: 選択用ウィジェットのサンプルです。

Checkbutton, Radiobutton, Combobox, Scale, Spinbox で飲み物を注文する画面を作ります。
"""

import tkinter as tk
from tkinter import messagebox, ttk


def main() -> None:
    """注文画面を表示します。"""
    root = tk.Tk()
    root.title("注文フォーム")

    size = tk.StringVar(value="M")
    drink = tk.StringVar(value="コーヒー")
    sugar = tk.IntVar(value=0)
    quantity = tk.IntVar(value=1)
    takeout = tk.BooleanVar(value=False)

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    # Combobox: 決められた候補から 1 つを選びます
    ttk.Label(frame, text="飲み物").grid(row=0, column=0, sticky="w", pady=3)
    drink_box = ttk.Combobox(
        frame,
        textvariable=drink,
        values=["コーヒー", "紅茶", "緑茶"],
        state="readonly",  # 候補以外の文字列を入力できないようにします
        width=12,
    )
    drink_box.grid(row=0, column=1, sticky="w", pady=3)

    # Radiobutton: 同じ変数を共有するボタンのうち 1 つだけが選ばれます
    ttk.Label(frame, text="サイズ").grid(row=1, column=0, sticky="w", pady=3)
    size_frame = ttk.Frame(frame)
    size_frame.grid(row=1, column=1, sticky="w", pady=3)
    for value in ["S", "M", "L"]:
        ttk.Radiobutton(
            size_frame, text=value, value=value, variable=size
        ).pack(side="left")

    # Scale: スライダーで数値を選びます
    ttk.Label(frame, text="砂糖 (g)").grid(row=2, column=0, sticky="w", pady=3)
    sugar_frame = ttk.Frame(frame)
    sugar_frame.grid(row=2, column=1, sticky="w", pady=3)
    ttk.Label(sugar_frame, textvariable=sugar, width=3).pack(side="right")

    def round_sugar(value: str) -> None:
        """ttk.Scale は小数を返すため、整数に丸めて変数に設定します。"""
        sugar.set(round(float(value)))

    ttk.Scale(
        sugar_frame,
        from_=0,
        to=10,
        variable=sugar,
        command=round_sugar,
        length=120,
    ).pack(side="left")

    # Spinbox: 矢印ボタンで数値を増減します
    ttk.Label(frame, text="数量").grid(row=3, column=0, sticky="w", pady=3)
    ttk.Spinbox(
        frame, from_=1, to=10, textvariable=quantity, width=5, state="readonly"
    ).grid(row=3, column=1, sticky="w", pady=3)

    # Checkbutton: オンとオフを切り替えます
    ttk.Checkbutton(frame, text="持ち帰り", variable=takeout).grid(
        row=4, column=0, columnspan=2, sticky="w", pady=3
    )

    def confirm() -> None:
        """選択内容をまとめてメッセージボックスに表示します。"""
        place = "持ち帰り" if takeout.get() else "店内"
        summary = (
            f"{drink.get()} ({size.get()} サイズ) x {quantity.get()}\n"
            f"砂糖 {sugar.get()} g / {place}"
        )
        messagebox.showinfo("注文内容", summary)

    ttk.Button(frame, text="確認", command=confirm).grid(
        row=5, column=0, columnspan=2, pady=(10, 0)
    )

    root.mainloop()


if __name__ == "__main__":
    main()
