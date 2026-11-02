"""第 14 章「映像の生成」: モーショングラフィックス（イージング、時間差、合成）。

フレームは、時刻 t を受け取って画像を返す純粋な関数 render(t) で作る。前のフレームの状態を
持たないので、どの時刻からでも描け（シーク）、フレームを並列に描け、何度描いても同じ結果になる。

* stagger_timeline.png: イージング関数と、時間差を付けた各要素の進み具合
* motion.mp4: 円の格子と文字が時間差で現れて消える 6 秒のループ
"""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw

from color import cosine_palette
from common import FloatArray, output_dir, save_figure, setup_matplotlib
from draw2d import load_font
from video import VideoWriter, find_ffmpeg

WIDTH, HEIGHT, FPS, DURATION = 640, 360, 30, 6.0
TEXT = "PROCEDURAL"


def clamp01(x: float) -> float:
    return min(max(x, 0.0), 1.0)


def ease_out_cubic(x: float) -> float:
    """速く動き出し、ゆっくり止まる。"""
    return 1.0 - (1.0 - clamp01(x)) ** 3


def ease_in_cubic(x: float) -> float:
    """ゆっくり動き出し、速いまま終わる（退場に使う）。"""
    return clamp01(x) ** 3


def ease_out_back(x: float, overshoot: float = 1.70158) -> float:
    """目標を少し行き過ぎてから戻る。overshoot が大きいほど大きく行き過ぎる。"""
    x = clamp01(x) - 1.0
    return 1.0 + (overshoot + 1.0) * x ** 3 + overshoot * x ** 2


def progress(t: float, start: float, duration: float) -> float:
    """時刻 t における、start に始まり duration 秒かかる動きの進み具合（0〜1、イージング前）。"""
    return clamp01((t - start) / duration)


def over(background: FloatArray, color: FloatArray, alpha: FloatArray) -> FloatArray:
    """アルファ合成（over 演算）: 不透明度 alpha の color を background の上に重ねる。"""
    result: FloatArray = color * alpha[..., None] + background * (1.0 - alpha[..., None])
    return result


# 円の格子: 各円の位置と、中央からの距離で決める時間差（中央から外へ波のように広がる）
COLUMNS, ROWS, SPACING = 9, 4, 64.0
CIRCLES = [
    (WIDTH / 2 + (c - (COLUMNS - 1) / 2) * SPACING, HEIGHT / 2 + (r - (ROWS - 1) / 2) * SPACING)
    for r in range(ROWS) for c in range(COLUMNS)
]
CENTER_DISTANCE = [math.hypot(x - WIDTH / 2, y - HEIGHT / 2) / SPACING for x, y in CIRCLES]


def circle_layer(image: FloatArray, t: float) -> FloatArray:
    """円の格子を描く。現れるときは ease_out_back で膨らみ、消えるときは ease_in で縮む。"""
    for index, ((cx, cy), distance) in enumerate(zip(CIRCLES, CENTER_DISTANCE)):
        enter = ease_out_back(progress(t, 0.2 + 0.12 * distance, 0.7))
        leave = ease_in_cubic(progress(t, 4.3 + 0.08 * (5.0 - distance), 0.5))
        radius = 24.0 * enter * (1.0 - leave)
        if radius <= 0.0:
            continue
        # 円の周りの四角形の範囲だけを計算する。縁は 1 画素の幅でなめらかにする（距離関数、第 9 章）。
        left, right = int(max(cx - radius - 2, 0)), int(min(cx + radius + 2, WIDTH))
        top, bottom = int(max(cy - radius - 2, 0)), int(min(cy + radius + 2, HEIGHT))
        ys, xs = np.mgrid[top:bottom, left:right] + 0.5
        alpha = np.clip(radius - np.hypot(xs - cx, ys - cy) + 0.5, 0.0, 1.0) * 0.9
        color = cosine_palette(np.array(index / len(CIRCLES) * 0.5 + 0.1 * t), d=(0.0, 0.15, 0.3))
        image[top:bottom, left:right] = over(image[top:bottom, left:right], color, alpha)
    return image


def text_layer(image: FloatArray, t: float) -> FloatArray:
    """文字を 1 文字ずつ時間差で、下から浮き上がらせて表示する。"""
    font = load_font(56)
    mask = Image.new("L", (WIDTH, HEIGHT), 0)
    draw = ImageDraw.Draw(mask)
    widths = [draw.textlength(letter, font=font) for letter in TEXT]
    x = (WIDTH - sum(widths)) / 2
    for index, (letter, width) in enumerate(zip(TEXT, widths)):
        enter = ease_out_cubic(progress(t, 1.3 + 0.06 * index, 0.6))
        leave = ease_in_cubic(progress(t, 3.9 + 0.04 * index, 0.4))
        offset = 30.0 * (1.0 - enter) - 30.0 * leave
        opacity = enter * (1.0 - leave)
        draw.text((x, HEIGHT / 2 + offset), letter, fill=int(255 * opacity), font=font, anchor="lm")
        x += width
    alpha = np.asarray(mask, dtype=np.float64) / 255.0
    # 文字の下に半透明の帯を敷き、その上に白い文字を重ねる。
    band = ease_out_cubic(progress(t, 1.0, 0.6)) * (1.0 - ease_in_cubic(progress(t, 4.1, 0.5)))
    band_alpha = np.zeros((HEIGHT, WIDTH))
    half = int(WIDTH / 2 * band)
    band_alpha[HEIGHT // 2 - 40:HEIGHT // 2 + 40, WIDTH // 2 - half:WIDTH // 2 + half] = 0.75
    image = over(image, np.array([0.05, 0.06, 0.12]), band_alpha)
    return over(image, np.array([1.0, 1.0, 1.0]), alpha)


def render(t: float) -> FloatArray:
    """時刻 t のフレーム (HEIGHT, WIDTH, 3)。背景・円・文字の順に重ねる。"""
    y = np.linspace(0.0, 1.0, HEIGHT)[:, None, None]
    image = np.broadcast_to(np.array([0.10, 0.12, 0.22]) * (1.0 - y) + np.array([0.04, 0.04, 0.08]) * y,
                            (HEIGHT, WIDTH, 3)).copy()
    image = circle_layer(image, t)
    return text_layer(image, t)


def draw_timeline(file_name: str) -> None:
    import matplotlib.pyplot as plt

    x = np.linspace(0.0, 1.0, 200)
    figure, axes = plt.subplots(1, 2, figsize=(12, 3.8), gridspec_kw={"width_ratios": [1.0, 1.5]})
    for name, function in [("ease_out_cubic", ease_out_cubic), ("ease_in_cubic", ease_in_cubic),
                           ("ease_out_back", ease_out_back)]:
        axes[0].plot(x, [function(v) for v in x], label=name)
    axes[0].set_title("イージング関数")
    axes[0].set_xlabel("進み具合（イージング前）")
    axes[0].set_ylabel("出力")
    axes[0].legend(fontsize=9)
    axes[0].grid(alpha=0.3)
    times = np.linspace(1.0, 2.6, 400)
    for index in range(len(TEXT)):
        values = [ease_out_cubic(progress(t, 1.3 + 0.06 * index, 0.6)) for t in times]
        axes[1].plot(times, values, color=plt.get_cmap("viridis")(index / len(TEXT)), label=TEXT[index])
    axes[1].set_title("文字ごとの進み具合（時間差 0.06 秒、長さ 0.6 秒）")
    axes[1].set_xlabel("時刻 t [s]")
    axes[1].legend(fontsize=8, ncol=5, loc="upper left")
    axes[1].set_ylim(-0.05, 1.35)
    axes[1].grid(alpha=0.3)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_timeline("stagger_timeline.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    with VideoWriter(output_dir(__file__) / "motion.mp4", WIDTH, HEIGHT, fps=FPS) as writer:
        for frame in range(int(DURATION * FPS)):
            writer.write(render(frame / FPS))


if __name__ == "__main__":
    main()
