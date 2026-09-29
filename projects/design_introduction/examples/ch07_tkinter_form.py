"""第 7 章: 同じ入力フォームを、UI の原則を意識せずに作った例と意識した例。

実行例::

    python ch07_tkinter_form.py --variant bad
    python ch07_tkinter_form.py --variant good

--screenshot を指定すると、ウィンドウを表示した直後に画面を撮影して
PNG で保存し、プログラムを終了します (Windows と macOS で動作します)。

    python ch07_tkinter_form.py --variant good --screenshot good.png

--demo-error を指定すると、誤った入力で「登録する」を押した状態を再現します。
"""

from __future__ import annotations

import argparse
import re
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from PIL import ImageDraw, ImageGrab

SPACE = 8  # 余白の基本単位 (px)。余白はすべてこの倍数にする

COLOR_PRIMARY = "#1f5fbf"
COLOR_PRIMARY_ACTIVE = "#174a94"
COLOR_TEXT = "#222222"
COLOR_SUBTEXT = "#555555"
COLOR_ERROR = "#c0392b"
COLOR_SUCCESS = "#1e7b34"
COLOR_BACKGROUND = "#ffffff"
FONT_FAMILY = "Yu Gothic UI" if sys.platform == "win32" else "TkDefaultFont"

DEPARTMENTS = ["開発部", "営業部", "総務部"]
NAME_HINT = "例: 山田 太郎"
EMAIL_HINT = "例: taro@example.com"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class BadForm(tk.Frame):
    """UI の原則を意識せずに作ったフォーム。"""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        # ラベルの揃え方、余白、入力欄の幅がばらばら
        tk.Label(self, text="名前").grid(row=0, column=0, padx=3, pady=7)
        self.name = tk.Entry(self, width=30)
        self.name.grid(row=0, column=1, padx=11, pady=2)
        tk.Label(self, text="メール").grid(row=1, column=0, sticky="e")
        self.email = tk.Entry(self, width=18)
        self.email.grid(row=1, column=1, sticky="w", pady=9)
        tk.Label(self, text="部署").grid(row=2, column=0, sticky="w")
        self.department = tk.Entry(self, width=24)  # 選択肢があるのに自由入力
        self.department.grid(row=2, column=1, padx=5)
        self.notify = tk.IntVar()
        tk.Checkbutton(self, text="通知", variable=self.notify).grid(
            row=3, column=1, sticky="e")

        # 重要度の異なるボタンが同じ見た目で並び、取り消せない操作が隣にある
        buttons = tk.Frame(self)
        buttons.grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(buttons, text="OK", command=self.submit).pack(side="left")
        tk.Button(buttons, text="クリア", command=self.clear).pack(
            side="left")
        tk.Button(buttons, text="キャンセル", command=master.destroy).pack(
            side="left")

    def submit(self) -> None:
        """入力を確認する。ただし、どこが悪いのかを伝えない。"""
        if not self.name.get() or "@" not in self.email.get():
            messagebox.showerror("エラー", "入力エラーです。")

    def clear(self) -> None:
        """確認せずに、すべての入力を消す。"""
        for entry in (self.name, self.email, self.department):
            entry.delete(0, tk.END)


class GoodForm(ttk.Frame):
    """UI の原則に沿って作ったフォーム。"""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=SPACE * 3, style="Form.TFrame")
        self.columnconfigure(0, weight=1)
        self.row = 0  # 次に部品を置く行
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        self.department = tk.StringVar(value=DEPARTMENTS[0])
        self.notify = tk.BooleanVar(value=True)

        self._place(ttk.Label(self, text="ユーザー登録",
                              style="Title.TLabel"))
        self._place(ttk.Label(self, text="* の付いた項目は入力が必要です。",
                              style="Sub.TLabel"), pady=(0, SPACE * 2))

        # ラベルは入力欄の上に置き、すべての部品の左端を揃える
        name_entry, self.name_message = self._add_field(
            "氏名 *", self.name, hint=NAME_HINT)
        _, self.email_message = self._add_field(
            "メールアドレス *", self.email, hint=EMAIL_HINT)

        # 選択肢が決まっている項目は、自由入力ではなく選択式にする
        self._place(ttk.Label(self, text="所属部署", style="Form.TLabel"))
        self._place(ttk.Combobox(self, textvariable=self.department,
                                 values=DEPARTMENTS, state="readonly"),
                    sticky="ew", pady=(SPACE // 2, SPACE * 2))
        self._place(ttk.Checkbutton(self, text="お知らせをメールで受け取る",
                                    variable=self.notify,
                                    style="Form.TCheckbutton"),
                    pady=(0, SPACE * 3))

        # 主要な操作は右下に置き、色で強調する
        buttons = ttk.Frame(self, style="Form.TFrame")
        ttk.Button(buttons, text="キャンセル", command=master.destroy).pack(
            side="left", padx=(0, SPACE))
        ttk.Button(buttons, text="登録する", style="Primary.TButton",
                   command=self.submit).pack(side="left")
        self._place(buttons, sticky="e")

        # 操作の結果は、画面内の決まった場所に表示する
        self.status = ttk.Label(self, text="", style="Success.TLabel")
        self._place(self.status, sticky="e", pady=(SPACE, 0))

        master.bind("<Return>", lambda _event: self.submit())
        master.bind("<Escape>", lambda _event: master.destroy())
        name_entry.focus_set()  # 最初の入力欄にフォーカスを置く

    def _place(self, widget: tk.Widget, sticky: str = "w",
               pady: int | tuple[int, int] = 0) -> None:
        """部品を次の行に配置する。"""
        widget.grid(row=self.row, column=0, sticky=sticky, pady=pady)
        self.row += 1

    def _add_field(self, label: str, variable: tk.StringVar,
                   hint: str = "") -> tuple[ttk.Entry, ttk.Label]:
        """ラベル・入力欄・メッセージ欄を縦に並べる。

        メッセージ欄には、普段は補足 (hint) を、誤りがあれば理由を表示する。
        """
        self._place(ttk.Label(self, text=label, style="Form.TLabel"))
        entry = ttk.Entry(self, textvariable=variable, width=36)
        self._place(entry, sticky="ew", pady=(SPACE // 2, 0))
        message = ttk.Label(self, text=hint, style="Sub.TLabel")
        self._place(message, pady=(SPACE // 2, SPACE * 2))
        return entry, message

    def submit(self) -> None:
        """入力を検証し、問題があれば該当する項目の下に理由を表示する。"""
        name_ok = bool(self.name.get().strip())
        email_ok = bool(EMAIL_PATTERN.match(self.email.get().strip()))

        if name_ok:
            self.name_message.configure(text=NAME_HINT, style="Sub.TLabel")
        else:
            self.name_message.configure(text="氏名を入力してください。",
                                        style="Error.TLabel")
        if email_ok:
            self.email_message.configure(text=EMAIL_HINT, style="Sub.TLabel")
        else:
            # メッセージが長いとウィンドウの幅が変わるので、短く具体的に書く
            self.email_message.configure(
                text="メールアドレスの形式が正しくありません。",
                style="Error.TLabel")
        self.status.configure(text="登録しました。" if name_ok and email_ok
                              else "")


def setup_style(root: tk.Tk) -> None:
    """GoodForm で使うスタイルを定義する。"""
    style = ttk.Style(root)
    style.theme_use("clam")  # OS によらず色を指定できるテーマ
    base = (FONT_FAMILY, 10)
    style.configure("Form.TFrame", background=COLOR_BACKGROUND)
    style.configure("Form.TLabel", background=COLOR_BACKGROUND,
                    foreground=COLOR_TEXT, font=base)
    style.configure("Form.TCheckbutton", background=COLOR_BACKGROUND,
                    foreground=COLOR_TEXT, font=base)
    style.configure("Title.TLabel", background=COLOR_BACKGROUND,
                    foreground=COLOR_TEXT, font=(FONT_FAMILY, 16, "bold"))
    style.configure("Sub.TLabel", background=COLOR_BACKGROUND,
                    foreground=COLOR_SUBTEXT, font=(FONT_FAMILY, 9))
    style.configure("Error.TLabel", background=COLOR_BACKGROUND,
                    foreground=COLOR_ERROR, font=(FONT_FAMILY, 9))
    style.configure("Success.TLabel", background=COLOR_BACKGROUND,
                    foreground=COLOR_SUCCESS, font=base)
    style.configure("TButton", font=base, padding=(SPACE * 2, SPACE // 2))
    style.configure("Primary.TButton", background=COLOR_PRIMARY,
                    foreground="white", bordercolor=COLOR_PRIMARY)
    style.map("Primary.TButton",
              background=[("active", COLOR_PRIMARY_ACTIVE)])


def capture(root: tk.Tk, path: Path) -> None:
    """ウィンドウの表示内容を撮影して保存し、ウィンドウを閉じる。"""
    root.update()
    x, y = root.winfo_rootx(), root.winfo_rooty()
    width, height = root.winfo_width(), root.winfo_height()
    image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
    # Windows 11 ではウィンドウの下端の角が丸く、背後の画面が写り込む。
    # 角の部分を、少し内側の画素の色で塗りつぶす。
    corner = 12
    draw = ImageDraw.Draw(image)
    for left in (0, image.width - corner):
        inner_x = corner if left == 0 else image.width - corner - 1
        color = image.getpixel((inner_x, image.height - corner - 1))
        draw.rectangle((left, image.height - corner, left + corner - 1,
                        image.height - 1), fill=color)
    image.save(path)
    root.destroy()


def enable_dpi_awareness() -> None:
    """Windows で、画面の拡大率を考慮した実際の座標を使うようにする。

    これを行わないと、拡大率が 100 % 以外のときに撮影範囲がずれる。
    """
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=["bad", "good"], default="good",
                        help="表示するフォーム")
    parser.add_argument("--screenshot", type=Path, default=None,
                        help="撮影した画像の保存先 (指定すると自動で終了)")
    parser.add_argument("--demo-error", action="store_true",
                        help="誤った入力で送信した状態を表示する (good のみ)")
    args = parser.parse_args()

    if args.screenshot is not None:
        enable_dpi_awareness()
    root = tk.Tk()
    root.title("ユーザー登録")
    root.resizable(False, False)
    if args.variant == "good":
        setup_style(root)
        root.configure(background=COLOR_BACKGROUND)
        form = GoodForm(root)
        form.pack(fill="both", expand=True)
        if args.demo_error:
            form.email.set("taro@example")
            form.submit()
    else:
        BadForm(root).pack()

    if args.screenshot is not None:
        screenshot: Path = args.screenshot
        root.attributes("-topmost", True)  # ほかのウィンドウが写り込まないように
        root.after(800, lambda: capture(root, screenshot))
    root.mainloop()


if __name__ == "__main__":
    main()
