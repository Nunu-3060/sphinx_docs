"""第 11 章: クラスを使ってアプリケーションを設計するサンプルです。

摂氏温度を華氏温度に変換するアプリケーションを作ります。
計算処理 (celsius_to_fahrenheit) と画面 (ConverterApp) を分けて実装します。
"""

import tkinter as tk
from tkinter import ttk


def celsius_to_fahrenheit(celsius: float) -> float:
    """摂氏温度を華氏温度に変換します。

    画面に依存しない関数なので、tkinter を使わずにテストできます。
    """
    return celsius * 9 / 5 + 32


class ConverterApp(ttk.Frame):
    """温度変換アプリケーションの画面です。"""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=10)
        self.celsius = tk.StringVar(value="0")
        self.result = tk.StringVar()
        self._create_widgets()
        self.convert()

    def _create_widgets(self) -> None:
        """ウィジェットを作成して配置します。"""
        ttk.Label(self, text="摂氏 (℃)").grid(row=0, column=0, sticky="w")
        entry = ttk.Entry(self, textvariable=self.celsius, width=10)
        entry.grid(row=0, column=1, padx=5)
        entry.bind("<Return>", lambda event: self.convert())
        entry.focus_set()

        ttk.Button(self, text="変換", command=self.convert).grid(
            row=0, column=2
        )
        ttk.Label(self, textvariable=self.result).grid(
            row=1, column=0, columnspan=3, sticky="w", pady=(10, 0)
        )

    def convert(self) -> None:
        """入力値を変換して結果を表示します。"""
        try:
            celsius = float(self.celsius.get())
        except ValueError:
            self.result.set("数値を入力してください")
            return
        fahrenheit = celsius_to_fahrenheit(celsius)
        self.result.set(f"華氏: {fahrenheit:.1f} ℉")


def main() -> None:
    """アプリケーションを起動します。"""
    root = tk.Tk()
    root.title("温度変換")
    app = ConverterApp(root)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
