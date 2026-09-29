"""第 6 章: bind によるイベント処理のサンプルです。

マウスの位置、クリック、キー入力の情報を画面に表示します。
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def main() -> None:
    """マウスとキーボードのイベントを表示するウィンドウを表示します。"""
    root = tk.Tk()
    root.title("イベントのサンプル")

    area = tk.Frame(
        root, width=360, height=200, bg="white", cursor="crosshair"
    )
    area.pack(padx=10, pady=10)

    position = tk.StringVar(value="マウスを白い領域に入れてください")
    last_event = tk.StringVar(value="クリックするか、キーを押してください")
    ttk.Label(root, textvariable=position).pack(anchor="w", padx=10)
    ttk.Label(root, textvariable=last_event).pack(
        anchor="w", padx=10, pady=(0, 10)
    )

    def on_motion(event: tk.Event[tk.Misc]) -> None:
        """マウスが動いたとき、領域内の座標を表示します。"""
        position.set(f"座標: x={event.x}, y={event.y}")

    def on_leave(event: tk.Event[tk.Misc]) -> None:
        """マウスが領域の外に出たときに呼ばれます。"""
        position.set("マウスが領域の外に出ました")

    def on_click(event: tk.Event[tk.Misc]) -> None:
        """クリックされたボタンの番号と座標を表示します。"""
        last_event.set(
            f"ボタン {event.num} をクリック: ({event.x}, {event.y})"
        )

    def on_double_click(event: tk.Event[tk.Misc]) -> None:
        """左ボタンがダブルクリックされたときに呼ばれます。"""
        last_event.set("左ボタンをダブルクリックしました")

    def on_key(event: tk.Event[tk.Misc]) -> None:
        """押されたキーの名前 (keysym) と入力された文字 (char) を表示します。"""
        last_event.set(f"キー: keysym={event.keysym!r}, char={event.char!r}")

    def on_ctrl_s(event: tk.Event[tk.Misc]) -> None:
        """Ctrl + S が押されたときに呼ばれます。

        <Key> よりも条件が詳しい <Control-s> が優先されるため、
        Ctrl + S では on_key は呼ばれません。
        """
        last_event.set("Ctrl + S が押されました")

    area.bind("<Motion>", on_motion)
    area.bind("<Leave>", on_leave)
    area.bind("<ButtonPress>", on_click)
    area.bind("<Double-Button-1>", on_double_click)

    # キーボードのイベントは、フォーカスを持つウィジェットに届きます。
    # ウィンドウ全体で受け取るため、root に bind します。
    root.bind("<Key>", on_key)
    root.bind("<Control-s>", on_ctrl_s)

    root.mainloop()


if __name__ == "__main__":
    main()
