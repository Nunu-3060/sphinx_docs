"""第 8 章: Canvas のサンプルです。

図形を描画し、マウスのドラッグで線を描けるようにします。
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


def draw_circle(
    canvas: tk.Canvas, cx: float, cy: float, r: float, color: str
) -> int:
    """中心 (cx, cy)、半径 r の円を描き、図形の ID を返します。

    create_oval は外接する四角形の左上と右下の座標で指定します。
    """
    return canvas.create_oval(
        cx - r, cy - r, cx + r, cy + r, fill=color, outline=""
    )


def main() -> None:
    """図形とお絵かき機能を持つ Canvas を表示します。"""
    root = tk.Tk()
    root.title("Canvas のサンプル")

    canvas = tk.Canvas(root, width=400, height=300, bg="white")
    canvas.pack(padx=10, pady=10)

    def draw_shapes() -> None:
        """基本的な図形を描画します。"""
        canvas.create_line(20, 20, 180, 20, width=3, fill="gray")
        canvas.create_rectangle(
            20, 40, 120, 100, fill="lightblue", outline="blue"
        )
        draw_circle(canvas, 180, 70, 30, "orange")
        canvas.create_polygon(250, 100, 290, 30, 330, 100, fill="lightgreen")
        canvas.create_text(
            200, 140, text="ドラッグで線を描けます", fill="black"
        )

    last_point: tuple[int, int] | None = None

    def on_press(event: tk.Event[tk.Misc]) -> None:
        """ドラッグの開始位置を記録します。"""
        nonlocal last_point
        last_point = (event.x, event.y)

    def on_drag(event: tk.Event[tk.Misc]) -> None:
        """前回の位置から現在の位置まで線を引きます。"""
        nonlocal last_point
        if last_point is not None:
            x0, y0 = last_point
            canvas.create_line(
                x0,
                y0,
                event.x,
                event.y,
                width=2,
                capstyle="round",
                tags="drawing",
            )
        last_point = (event.x, event.y)

    def clear_drawing() -> None:
        """マウスで描いた線 (タグ "drawing" の図形) だけを削除します。"""
        canvas.delete("drawing")

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)

    ttk.Button(root, text="描いた線を消す", command=clear_drawing).pack(
        pady=(0, 10)
    )

    draw_shapes()
    root.mainloop()


if __name__ == "__main__":
    main()
