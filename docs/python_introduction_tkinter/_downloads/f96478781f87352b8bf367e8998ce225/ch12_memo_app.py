"""第 12 章: 簡易メモ帳アプリケーションです。

これまでの章で学んだ内容を組み合わせ、次の機能を持つテキストエディターを作ります。

* ファイルの新規作成、読み込み、保存 (文字コードは UTF-8)
* 元に戻す、やり直し、切り取り、コピー、貼り付け、すべて選択
* 右端での折り返しの切り替え
* キーボードショートカット
* カーソル位置を表示するステータスバー
* 未保存の変更がある場合の確認
"""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from functools import partial
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

APP_NAME = "簡易メモ帳"
ENCODING = "utf-8"
FILE_TYPES = [("テキストファイル", "*.txt"), ("すべてのファイル", "*.*")]


class MemoApp:
    """簡易メモ帳のアプリケーションです。"""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        # 編集中のファイル (一度も保存していない場合は None)
        self.file_path: Path | None = None
        self.status = tk.StringVar()
        self.wrap = tk.BooleanVar(value=False)

        self.root.geometry("640x480")
        self.root.option_add("*tearOff", False)
        self._create_widgets()
        self._create_menu()
        self._bind_shortcuts()
        # ウィンドウの閉じるボタンでも、未保存の変更を確認します
        self.root.protocol("WM_DELETE_WINDOW", self.quit)

        self._update_title()
        self._update_status()
        self.text.focus_set()

    # ------------------------------------------------------------
    # 画面の構築
    # ------------------------------------------------------------
    def _create_widgets(self) -> None:
        """テキスト領域、スクロールバー、ステータスバーを作成します。"""
        # ウィンドウを縮めても消えないように、ステータスバーを先に配置します
        statusbar = ttk.Label(
            self.root, textvariable=self.status, anchor="w", padding=(5, 2)
        )
        statusbar.pack(side="bottom", fill="x")

        frame = ttk.Frame(self.root)
        frame.pack(side="top", fill="both", expand=True)

        # undo=True で「元に戻す」と「やり直し」が使えるようになります
        self.text = tk.Text(frame, wrap="none", undo=True)
        y_scroll = ttk.Scrollbar(
            frame, orient="vertical", command=self.text.yview
        )
        x_scroll = ttk.Scrollbar(
            frame, orient="horizontal", command=self.text.xview
        )
        self.text.configure(
            yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set
        )

        self.text.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        # <<Modified>> は、変更フラグ (edit_modified) が切り替わったときに発生します
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<KeyRelease>", self._on_cursor_moved)
        self.text.bind("<ButtonRelease-1>", self._on_cursor_moved)

    def _create_menu(self) -> None:
        """メニューバーを作成します。"""
        menubar = tk.Menu(self.root)
        self.root.configure(menu=menubar)

        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(
            label="新規", accelerator="Ctrl+N", command=self.new_file
        )
        file_menu.add_command(
            label="開く...", accelerator="Ctrl+O", command=self.open_file
        )
        file_menu.add_command(
            label="保存", accelerator="Ctrl+S", command=self.save_file
        )
        file_menu.add_command(
            label="名前を付けて保存...",
            accelerator="Ctrl+Shift+S",
            command=self.save_file_as,
        )
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.quit)

        edit_menu = tk.Menu(menubar)
        menubar.add_cascade(label="編集", menu=edit_menu)
        # Text ウィジェットに標準で用意されている仮想イベントを発生させます
        edit_menu.add_command(
            label="元に戻す",
            accelerator="Ctrl+Z",
            command=self._event("<<Undo>>"),
        )
        edit_menu.add_command(
            label="やり直し",
            accelerator="Ctrl+Y",
            command=self._event("<<Redo>>"),
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="切り取り",
            accelerator="Ctrl+X",
            command=self._event("<<Cut>>"),
        )
        edit_menu.add_command(
            label="コピー",
            accelerator="Ctrl+C",
            command=self._event("<<Copy>>"),
        )
        edit_menu.add_command(
            label="貼り付け",
            accelerator="Ctrl+V",
            command=self._event("<<Paste>>"),
        )
        edit_menu.add_separator()
        edit_menu.add_command(
            label="すべて選択", accelerator="Ctrl+A", command=self.select_all
        )

        view_menu = tk.Menu(menubar)
        menubar.add_cascade(label="表示", menu=view_menu)
        view_menu.add_checkbutton(
            label="右端で折り返す",
            variable=self.wrap,
            command=self._apply_wrap,
        )

    def _event(self, virtual_event: str) -> Callable[[], None]:
        """Text に仮想イベントを発生させる関数を返します (メニューの command 用)。"""

        def generate() -> None:
            self.text.event_generate(virtual_event)
            self._update_status()  # 貼り付けなどでカーソルが動くため

        return generate

    def _bind_shortcuts(self) -> None:
        """キーボードショートカットを登録します。"""
        shortcuts: dict[str, Callable[[], object]] = {
            "<Control-n>": self.new_file,
            "<Control-o>": self.open_file,
            "<Control-s>": self.save_file,
            "<Control-Shift-S>": self.save_file_as,
            "<Control-a>": self.select_all,
        }
        # Text ウィジェットには Ctrl+O (改行の挿入) などの標準の動作があります。
        # Text 自体に bind し、"break" を返して標準の動作を止めます。
        for sequence, command in shortcuts.items():
            self.text.bind(sequence, partial(self._on_shortcut, command))

    @staticmethod
    def _on_shortcut(
        command: Callable[[], object], event: tk.Event[tk.Misc]
    ) -> str:
        """ショートカットに対応する処理を実行し、標準の動作を止めます。"""
        command()
        return "break"

    # ------------------------------------------------------------
    # ファイル操作
    # ------------------------------------------------------------
    def new_file(self) -> None:
        """編集中の内容を破棄して、新しい文書を開始します。"""
        if not self._confirm_discard():
            return
        self._set_content("", None)

    def open_file(self) -> None:
        """ファイルを選択して読み込みます。"""
        if not self._confirm_discard():
            return
        path_str = filedialog.askopenfilename(
            parent=self.root, filetypes=FILE_TYPES
        )
        if not path_str:
            return
        path = Path(path_str)
        try:
            content = path.read_text(encoding=ENCODING)
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror(
                APP_NAME,
                f"ファイルを開けませんでした。\n{error}",
                parent=self.root,
            )
            return
        self._set_content(content, path)

    def save_file(self) -> bool:
        """上書き保存します。保存できた場合は True を返します。"""
        if self.file_path is None:
            return self.save_file_as()
        return self._write(self.file_path)

    def save_file_as(self) -> bool:
        """保存先を選択して保存します。保存できた場合は True を返します。"""
        path_str = filedialog.asksaveasfilename(
            parent=self.root, filetypes=FILE_TYPES, defaultextension=".txt"
        )
        if not path_str:
            return False
        return self._write(Path(path_str))

    def quit(self) -> None:
        """未保存の変更を確認してから終了します。"""
        if self._confirm_discard():
            self.root.destroy()

    def _write(self, path: Path) -> bool:
        """テキストの内容をファイルに書き込みます。成功した場合は True を返します。"""
        # "end" の直前には Text が自動で付ける改行があるため、"end-1c" までを取得します
        content = self.text.get("1.0", "end-1c")
        try:
            path.write_text(content, encoding=ENCODING)
        except OSError as error:
            messagebox.showerror(
                APP_NAME, f"保存できませんでした。\n{error}", parent=self.root
            )
            return False
        self.file_path = path
        self.text.edit_modified(False)
        self._update_title()
        return True

    def _set_content(self, content: str, path: Path | None) -> None:
        """テキストの内容を置き換え、編集状態を初期化します。"""
        self.text.delete("1.0", "end")
        self.text.insert("1.0", content)
        self.text.mark_set("insert", "1.0")
        self.text.see("insert")
        self.text.edit_reset()  # 元に戻す履歴を消去します
        self.text.edit_modified(False)
        self.file_path = path
        self._update_title()
        self._update_status()

    def _confirm_discard(self) -> bool:
        """未保存の変更があれば保存するかを確認します。

        処理を続けてよい場合は True、キャンセルされた場合は False を返します。
        """
        if not self.text.edit_modified():
            return True
        answer = messagebox.askyesnocancel(
            APP_NAME, "変更内容を保存しますか？", parent=self.root
        )
        if answer is None:  # キャンセル
            return False
        if answer:  # はい
            return self.save_file()
        return True  # いいえ (保存せずに続行)

    # ------------------------------------------------------------
    # 編集と表示
    # ------------------------------------------------------------
    def select_all(self) -> None:
        """すべての文字列を選択します。"""
        self.text.tag_add("sel", "1.0", "end-1c")
        self.text.mark_set("insert", "end-1c")
        self._update_status()

    def _apply_wrap(self) -> None:
        """折り返しの設定をテキスト領域に反映します。"""
        self.text.configure(wrap="char" if self.wrap.get() else "none")

    def _on_modified(self, event: tk.Event[tk.Misc]) -> None:
        """変更フラグが切り替わったときに、タイトルを更新します。"""
        self._update_title()

    def _on_cursor_moved(self, event: tk.Event[tk.Misc]) -> None:
        """キー入力やクリックの後に、ステータスバーを更新します。"""
        self._update_status()

    def _update_title(self) -> None:
        """ファイル名と変更の有無をタイトルバーに表示します。"""
        name = self.file_path.name if self.file_path else "無題"
        mark = "*" if self.text.edit_modified() else ""
        self.root.title(f"{mark}{name} - {APP_NAME}")

    def _update_status(self) -> None:
        """カーソルの位置 (行と列) をステータスバーに表示します。"""
        # index は "行.列" の形式の文字列を返します。行は 1 から、列は 0 から数えます。
        line, column = self.text.index("insert").split(".")
        self.status.set(
            f"{line} 行、{int(column) + 1} 列 | {ENCODING.upper()}"
        )


def main() -> None:
    """簡易メモ帳を起動します。"""
    root = tk.Tk()
    MemoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
