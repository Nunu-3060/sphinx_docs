"""第 14 章「映像の生成」: 動画の形式と圧縮の設定による容量の違いを測る。

内容の異なる 2 本の 10 秒のクリップ（640 × 360、30 fps）を作り、いったん劣化のない形式で保存してから、
H.264（MP4）・VP9（WebM）・GIF に、さまざまな設定で書き出して容量を測る。

* 滑らかな模様: ゆっくり動くグラデーション
* 細かい粒: 同じ模様に、フレームごとに変わる細かい粒（フィルムグレインのような乱れ）を加えたもの

* format_sizes.png: 形式ごとの容量
* compression_params.png: CRF・プリセット・解像度とフレームレートと容量の関係
* sample.gif: 比較用の小さな GIF（滑らかな模様の先頭 3 秒、320 px、10 fps、64 色）

測った値は標準出力にも表示する。容量と時間は ffmpeg の版や計算機によって変わる。
"""

from __future__ import annotations

import tempfile
import time
from pathlib import Path

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from video import find_ffmpeg, run_ffmpeg, to_gif, to_webm

WIDTH, HEIGHT, FPS, DURATION = 640, 360, 30, 10.0


_Y, _X = np.mgrid[0:HEIGHT, 0:WIDTH] / WIDTH


def smooth_frame(t: float) -> FloatArray:
    """滑らかな模様: 位置と時刻の sin を重ねた、ゆっくり動くグラデーション。"""
    value = np.sin(6.0 * _X + 1.3 * t) + np.sin(5.0 * _Y - 0.9 * t) + np.sin(4.0 * (_X + _Y) + 0.7 * t)
    phase = value[..., None] * 0.6 + np.array([0.0, 2.0, 4.0])
    result: FloatArray = 0.5 + 0.4 * np.cos(phase)
    return result


def make_sources(folder: Path) -> dict[str, Path]:
    """2 本の元のクリップを作る。

    フレームを生の画素列（rgb24）のファイルに書き、ffmpeg で劣化のない H.264（CRF 0）にする。
    細かい粒は、滑らかな模様にフレームごとに変わる乱数の粒を加えたもの。
    """
    rng = np.random.default_rng(0)
    raw = {"滑らかな模様": folder / "smooth.rgb", "細かい粒": folder / "grainy.rgb"}
    with raw["滑らかな模様"].open("wb") as smooth, raw["細かい粒"].open("wb") as grainy:
        for frame in range(int(DURATION * FPS)):
            image = (smooth_frame(frame / FPS) * 255.0).astype(np.int16)
            grain = rng.integers(-12, 13, (HEIGHT, WIDTH, 1), dtype=np.int16)
            smooth.write(image.astype(np.uint8).tobytes())
            grainy.write(np.clip(image + grain, 0, 255).astype(np.uint8).tobytes())
    paths = {}
    for name, path in raw.items():
        paths[name] = path.with_suffix(".mp4")
        run_ffmpeg(["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", str(path),
                    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "0", "-pix_fmt", "yuv420p", str(paths[name])])
    return paths


def h264(source: Path, target: Path, crf: int = 23, preset: str = "slow", scale: int | None = None,
         fps: int | None = None) -> float:
    """H.264 の MP4 に書き出し、かかった時間 [s] を返す。"""
    filters = []
    if scale is not None:
        filters.append(f"scale={scale}:-2:flags=lanczos")
    if fps is not None:
        filters.append(f"fps={fps}")
    arguments = ["-i", str(source)] + (["-vf", ",".join(filters)] if filters else [])
    arguments += ["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p",
                  "-movflags", "+faststart", "-an", str(target)]
    start = time.perf_counter()
    run_ffmpeg(arguments)
    return time.perf_counter() - start


def megabytes(path: Path) -> float:
    return path.stat().st_size / 1024 / 1024


def measure(folder: Path, sources: dict[str, Path]) -> dict[str, dict[str, float]]:
    """設定ごとの容量 [MB]（とかかった時間）を測る。"""
    results: dict[str, dict[str, float]] = {}
    for name, source in sources.items():
        sizes: dict[str, float] = {}
        for crf in [18, 23, 28, 33]:
            target = folder / f"{source.stem}_crf{crf}.mp4"
            h264(source, target, crf=crf)
            sizes[f"crf{crf}"] = megabytes(target)
        if name == "滑らかな模様":  # VP9 は書き出しに時間がかかるので、細かい粒では測らない
            target = folder / f"{source.stem}.webm"
            sizes["webm_time"] = time.perf_counter()
            to_webm(source, target, crf=40)
            sizes["webm_time"] = time.perf_counter() - sizes["webm_time"]
            sizes["webm40"] = megabytes(target)
        target = folder / f"{source.stem}.gif"
        to_gif(source, target, fps=15, width=480, colors=128)
        sizes["gif"] = megabytes(target)
        results[name] = sizes
    smooth = sources["滑らかな模様"]
    extra: dict[str, float] = {}
    for preset in ["ultrafast", "veryfast", "medium", "slow", "veryslow"]:
        target = folder / f"preset_{preset}.mp4"
        extra[f"time_{preset}"] = h264(smooth, target, crf=23, preset=preset)
        extra[f"size_{preset}"] = megabytes(target)
    for width in [640, 480, 320]:
        target = folder / f"scale_{width}.mp4"
        h264(smooth, target, crf=28, scale=width)
        extra[f"scale_{width}"] = megabytes(target)
    target = folder / "fps15.mp4"
    h264(smooth, target, crf=28, fps=15)
    extra["fps15"] = megabytes(target)
    results["その他"] = extra
    return results


def draw_formats(results: dict[str, dict[str, float]], file_name: str) -> None:
    import matplotlib.pyplot as plt

    names = {"crf23": "MP4 CRF 23", "crf28": "MP4 CRF 28", "webm40": "WebM CRF 40", "gif": "GIF 480 px\n15 fps 128 色"}
    colors = {"crf23": "#4c72b0", "crf28": "#4c72b0", "webm40": "#55a868", "gif": "#dd8452"}
    figure, axes = plt.subplots(1, 2, figsize=(12, 3.4))
    for ax, name in zip(axes, ["滑らかな模様", "細かい粒"]):
        keys = [key for key in names if key in results[name]]  # 細かい粒では WebM を測っていない
        values = [results[name][key] for key in keys]
        bars = ax.barh([names[key] for key in keys], values, color=[colors[key] for key in keys])
        ax.bar_label(bars, [f"{v:.2f} MB" for v in values], padding=3, fontsize=9)
        ax.set_xscale("log")
        ax.set_xlim(min(values) / 2, max(values) * 6)
        ax.invert_yaxis()
        ax.set_xlabel("容量 [MB]（対数）")
        ax.set_title(f"{name}（640 × 360、30 fps、10 秒）", fontsize=11)
        ax.grid(alpha=0.3, axis="x")
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_params(results: dict[str, dict[str, float]], file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 3, figsize=(13, 3.6))
    crfs = [18, 23, 28, 33]
    for name in ["滑らかな模様", "細かい粒"]:
        axes[0].semilogy(crfs, [results[name][f"crf{c}"] for c in crfs], "-o", label=name)
    axes[0].set_xticks(crfs)
    axes[0].set_xlabel("CRF（preset slow）")
    axes[0].set_ylabel("容量 [MB]（対数）")
    axes[0].set_title("CRF と容量")
    axes[0].legend(fontsize=9)
    axes[0].grid(alpha=0.3, which="both")

    extra = results["その他"]
    presets = ["ultrafast", "veryfast", "medium", "slow", "veryslow"]
    sizes = [extra[f"size_{p}"] for p in presets]
    times = [extra[f"time_{p}"] for p in presets]
    axes[1].bar(presets, sizes, color="#4c72b0")
    axes[1].set_ylabel("容量 [MB]", color="#4c72b0")
    twin = axes[1].twinx()
    twin.plot(presets, times, "-o", color="#dd8452")
    twin.set_ylabel("書き出しの時間 [s]", color="#dd8452")
    twin.set_ylim(0.0, max(times) * 1.2)
    axes[1].set_title("プリセット（滑らかな模様、CRF 23）")
    axes[1].tick_params(axis="x", labelsize=8)

    labels = ["640×360\n30 fps", "480×270\n30 fps", "320×180\n30 fps", "640×360\n15 fps"]
    values = [extra["scale_640"], extra["scale_480"], extra["scale_320"], extra["fps15"]]
    bars = axes[2].bar(labels, values, color="#55a868")
    axes[2].bar_label(bars, [f"{v:.2f}" for v in values], fontsize=9)
    axes[2].set_ylabel("容量 [MB]")
    axes[2].set_title("解像度とフレームレート（CRF 28）")
    axes[2].tick_params(axis="x", labelsize=8)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        sources = make_sources(folder)
        results = measure(folder, sources)
        # 本文に載せる比較用の小さな GIF（先頭 3 秒だけを切り出してから変換する）
        clip = folder / "clip.mp4"
        run_ffmpeg(["-i", str(sources["滑らかな模様"]), "-t", "3", "-c:v", "libx264", "-crf", "0", str(clip)])
        to_gif(clip, output_dir(__file__) / "sample.gif", fps=10, width=320, colors=64)
    draw_formats(results, "format_sizes.png")
    draw_params(results, "compression_params.png")
    for name, values in results.items():
        print(name, ", ".join(f"{key} {value:.3f}" for key, value in values.items()))
    print(f"sample.gif {megabytes(output_dir(__file__) / 'sample.gif'):.3f} MB")


if __name__ == "__main__":
    main()
