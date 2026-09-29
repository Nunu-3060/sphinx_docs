"""第 7 章: メニューと標準ダイアログのサンプルです。

メニューバー、右クリックメニュー、messagebox, filedialog, simpledialog,
colorchooser を使います。
"""

from __future__ import annotations

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog


def main() -> None:
    """メニューとダイアログを試すウィンドウを表示します。"""
    root = tk.Tk()
    root.title("メニューとダイアログ")
    root.geometry("400x240")

    # メニューの点線 (切り離し機能) を無効にします。メニューを作る前に設定します。
    root.option_add("*tearOff", False)

    # 背景色を変更するため、tk の Label を使います
    label = tk.Label(root, text="メニューを選んでください", bg="white")
    label.pack(fill="both", expand=True)

    def open_file() -> None:
        """ファイル選択ダイアログを表示し、選ばれたパスを表示します。"""
        path = filedialog.askopenfilename(
            title="ファイルを開く",
            filetypes=[
                ("テキストファイル", "*.txt"),
                ("すべてのファイル", "*.*"),
            ],
        )
        if path:  # キャンセルされた場合は空文字列が返ります
            label.configure(text=f"選択: {path}")

    def change_name() -> None:
        """文字列を入力するダイアログを表示します。"""
        name = simpledialog.askstring(
            "名前の入力", "名前を入力してください", parent=root
        )
        if name is not None:  # キャンセルされた場合は None が返ります
            label.configure(text=f"こんにちは、{name} さん")

    def change_color() -> None:
        """色選択ダイアログを表示し、ラベルの背景色を変更します。"""
        _rgb, color = colorchooser.askcolor(title="背景色の選択", parent=root)
        if color is not None:
            label.configure(bg=color)

    def show_about() -> None:
        """情報メッセージを表示します。"""
        messagebox.showinfo(
            "バージョン情報", "メニューとダイアログのサンプル 1.0"
        )

    def quit_app() -> None:
        """確認ダイアログで「はい」が選ばれたら終了します。"""
        if messagebox.askyesno("終了の確認", "終了しますか？"):
            root.destroy()

    # メニューバーを作り、ウィンドウに設定します
    menubar = tk.Menu(root)
    root.configure(menu=menubar)

    file_menu = tk.Menu(menubar)
    menubar.add_cascade(label="ファイル", menu=file_menu)
    file_menu.add_command(label="開く...", command=open_file)
    file_menu.add_separator()
    file_menu.add_command(label="終了", command=quit_app)

    settings_menu = tk.Menu(menubar)
    menubar.add_cascade(label="設定", menu=settings_menu)
    settings_menu.add_command(label="名前の入力...", command=change_name)
    settings_menu.add_command(label="背景色...", command=change_color)

    help_menu = tk.Menu(menubar)
    menubar.add_cascade(label="ヘルプ", menu=help_menu)
    help_menu.add_command(label="バージョン情報", command=show_about)

    # 右クリックで表示するメニュー (コンテキストメニュー) です
    context_menu = tk.Menu(root)
    context_menu.add_command(label="背景色...", command=change_color)
    context_menu.add_command(label="バージョン情報", command=show_about)

    def show_context_menu(event: tk.Event[tk.Misc]) -> None:
        """マウスポインターの位置にコンテキストメニューを表示します。"""
        context_menu.tk_popup(event.x_root, event.y_root)

    # Windows と Linux の右クリックは <Button-3> です (macOS では <Button-2>)
    label.bind("<Button-3>", show_context_menu)

    # ウィンドウの閉じるボタン (x) が押されたときも確認します
    root.protocol("WM_DELETE_WINDOW", quit_app)

    root.mainloop()


if __name__ == "__main__":
    main()
