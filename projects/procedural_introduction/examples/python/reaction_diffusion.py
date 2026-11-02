"""第 5 章「規則から生まれる模様」: 反応拡散（Gray-Scott モデル）の図と動画を作る。

* rd_presets.png: パラメーター F, k を変えた 6 種類の模様
* rd_steps.png: 模様が育つ途中の様子（同じ F, k で時刻を変える）
* rd_growth.mp4: 模様が育つ様子の動画（6 秒）
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from scipy import ndimage

from color import gradient_map, hex_to_rgb
from common import FloatArray, output_dir, setup_matplotlib
from texture import show_panels
from video import VideoWriter, find_ffmpeg

Grid = NDArray[np.float32]  # 濃度の格子（計算を速くするため 32 bit の浮動小数点数を使う）

# 拡散係数（U は V の 2 倍速く広がる）と時間の刻み
DIFFUSION_U = 1.0
DIFFUSION_V = 0.5
DT = 1.0

# 名前、F（U の供給率）、k（V の除去率）
PRESETS = [
    ("斑点", 0.0367, 0.0649),
    ("迷路", 0.029, 0.057),
    ("サンゴ", 0.0545, 0.062),
    ("穴", 0.039, 0.058),
    ("短い縞", 0.058, 0.065),
    ("混沌", 0.022, 0.051),
]

COLORS = [(0.0, hex_to_rgb("#0b1d3a")), (0.25, hex_to_rgb("#1f6f8b")), (0.5, hex_to_rgb("#99d5c9")),
          (1.0, hex_to_rgb("#fff6d5"))]


# ラプラシアン（周囲との差）の重み。上下左右 0.2、斜め 0.05、中心 -1 で、合計は 0 になる。
KERNEL = np.array([[0.05, 0.2, 0.05], [0.2, -1.0, 0.2], [0.05, 0.2, 0.05]], dtype=np.float32)


def laplacian(a: Grid) -> Grid:
    """3 × 3 の重み KERNEL によるラプラシアン。端は反対側とつながる（周期境界）。

    最後の 2 軸を画像の縦横とみなすので、複数の画像を重ねた (N, H, W) の配列もまとめて計算できる。
    """
    kernel = KERNEL.reshape((1,) * (a.ndim - 2) + (3, 3))
    result: Grid = ndimage.convolve(a, kernel, mode="wrap")
    return result


def step(u: Grid, v: Grid, feed: Grid | float, kill: Grid | float) -> None:
    """Gray-Scott モデルを 1 歩進める（u, v をその場で書き換える）。

    反応 U + 2V → 3V で U が V に変わり、U は外から F の割合で補給され、V は F + k の割合で取り除かれる。
    """
    reaction = u * v * v
    u += DT * (DIFFUSION_U * laplacian(u) - reaction + feed * (1.0 - u))
    v += DT * (DIFFUSION_V * laplacian(v) + reaction - (feed + kill) * v)


def initial_state(count: int, size: int, seed: int = 0) -> tuple[Grid, Grid]:
    """全体を U = 1, V = 0 とし、ランダムな位置に V の小さな正方形を置く。"""
    rng = np.random.default_rng(seed)
    # 計算を速くするため 32 bit の浮動小数点数を使う（GPU と同じ精度）。
    u = np.ones((count, size, size), dtype=np.float32)
    v = np.zeros((count, size, size), dtype=np.float32)
    for _ in range(12):
        y, x = rng.integers(0, size - 8, size=2)
        u[:, y:y + 8, x:x + 8] = 0.5
        v[:, y:y + 8, x:x + 8] = 0.25
    v += 0.02 * rng.random((count, size, size), dtype=np.float32)  # 小さな揺らぎで対称性を崩す
    return u, v


def colorize(v: Grid) -> FloatArray:
    """V の濃度（おおむね 0〜0.4）を色にする。"""
    return gradient_map(np.clip(v.astype(np.float64) / 0.4, 0.0, 1.0), COLORS)


def draw_presets(file_name: str, size: int = 128, steps: int = 5000) -> None:
    """6 種類の F, k を、(6, size, size) の配列でまとめてシミュレーションする。"""
    u, v = initial_state(len(PRESETS), size, seed=1)
    feed = np.array([f for _, f, _ in PRESETS], dtype=np.float32)[:, None, None]
    kill = np.array([k for _, _, k in PRESETS], dtype=np.float32)[:, None, None]
    for _ in range(steps):
        step(u, v, feed, kill)
    images = [colorize(v[index]) for index in range(len(PRESETS))]
    titles = [f"{name}（F = {f}, k = {k}）" for name, f, k in PRESETS]
    show_panels(images, titles, output_dir(__file__) / file_name, columns=3)


def draw_steps(file_name: str, size: int = 128) -> None:
    u, v = initial_state(1, size, seed=2)
    _, feed, kill = PRESETS[2]
    checkpoints = (300, 1000, 2500, 6000)
    images = []
    done = 0
    for checkpoint in checkpoints:
        for _ in range(checkpoint - done):
            step(u, v, feed, kill)
        done = checkpoint
        images.append(colorize(v[0]))
    show_panels(images, [f"{n} 歩" for n in checkpoints], output_dir(__file__) / file_name)


def write_video(file_name: str, seconds: int = 6, fps: int = 30, steps_per_frame: int = 25) -> None:
    """320 × 180 の格子で計算し、2 倍に拡大して 640 × 360 の動画にする。"""
    height, width = 180, 320
    rng = np.random.default_rng(3)
    u = np.ones((height, width), dtype=np.float32)
    v = np.zeros((height, width), dtype=np.float32)
    for _ in range(6):
        y = int(rng.integers(10, height - 18))
        x = int(rng.integers(10, width - 18))
        u[y:y + 8, x:x + 8] = 0.5
        v[y:y + 8, x:x + 8] = 0.25
    v += 0.02 * rng.random((height, width), dtype=np.float32)
    _, feed, kill = PRESETS[0]
    with VideoWriter(output_dir(__file__) / file_name, width * 2, height * 2, fps=fps) as writer:
        for _ in range(seconds * fps):
            for _ in range(steps_per_frame):
                step(u, v, feed, kill)
            frame = colorize(v)
            writer.write(np.repeat(np.repeat(frame, 2, axis=0), 2, axis=1))


def main() -> None:
    setup_matplotlib()
    draw_presets("rd_presets.png")
    draw_steps("rd_steps.png")
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    write_video("rd_growth.mp4")


if __name__ == "__main__":
    main()
