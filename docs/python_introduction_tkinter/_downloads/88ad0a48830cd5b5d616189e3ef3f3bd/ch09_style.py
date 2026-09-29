"""第 9 章: ttk.Style とフォントのサンプルです。

テーマの切り替え、独自スタイルの定義、状態に応じた外観の変更を試します。
"""

import tkinter as tk
from tkinter import font, ttk


def main() -> None:
    """テーマとスタイルを切り替えるウィンドウを表示します。"""
    root = tk.Tk()
    root.title("スタイルのサンプル")

    style = ttk.Style(root)

    # 名前付きフォントを作ります。
    # 後から設定を変えると、このフォントを使う全ウィジェットに反映されます。
    title_font = font.Font(root, family="Helvetica", size=14, weight="bold")

    def define_styles() -> None:
        """独自スタイルを定義します。

        スタイルの設定は使用中のテーマに対して行われるため、
        テーマを切り替えるたびに呼び出します。
        """
        # 「任意の名前.既定のスタイル名」の形式で定義します
        style.configure("Title.TLabel", font=title_font, foreground="navy")
        style.configure("Danger.TButton", foreground="red")
        # 状態 (マウスが乗っている "active" など) に応じて値を変えます
        style.map("Danger.TButton", foreground=[("active", "darkred")])

    define_styles()

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="スタイルのサンプル", style="Title.TLabel").pack(
        anchor="w"
    )

    # 利用できるテーマの一覧から選べるようにします
    theme = tk.StringVar(value=style.theme_use())
    theme_frame = ttk.Frame(frame)
    theme_frame.pack(fill="x", pady=10)
    ttk.Label(theme_frame, text="テーマ").pack(side="left", padx=(0, 10))
    theme_box = ttk.Combobox(
        theme_frame,
        textvariable=theme,
        values=style.theme_names(),
        state="readonly",
    )
    theme_box.pack(side="left")

    def change_theme(*args: object) -> None:
        """選ばれたテーマに切り替えます。"""
        style.theme_use(theme.get())
        define_styles()  # 新しいテーマにも独自スタイルを設定します

    theme.trace_add("write", change_theme)

    # 見た目を比べるためのウィジェットです
    ttk.Button(frame, text="通常のボタン").pack(fill="x", pady=2)
    ttk.Button(
        frame, text="削除 (Danger.TButton)", style="Danger.TButton"
    ).pack(fill="x", pady=2)
    # variable を指定しないと、初期状態が「未確定」の表示になることがあります
    checked = tk.BooleanVar(value=True)
    ttk.Checkbutton(frame, text="チェックボタン", variable=checked).pack(
        anchor="w", pady=2
    )
    ttk.Entry(frame).pack(fill="x", pady=2)

    def enlarge_font() -> None:
        """名前付きフォントの大きさを 2 ポイント大きくします。"""
        title_font.configure(size=title_font.cget("size") + 2)

    ttk.Button(frame, text="見出しを大きくする", command=enlarge_font).pack(
        fill="x", pady=(10, 2)
    )

    root.mainloop()


if __name__ == "__main__":
    main()
