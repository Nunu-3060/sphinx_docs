"""ハッチング（線の密度による陰影）と SVG への書き出し。

画像の暗さを、平行線を重ねる本数で表す。暗さのしきい値を段階的に
設け、しきい値を超えた場所にだけ、向きの異なる平行線の層を重ねる。
明るい場所には線を引かず、暗い場所ほど多くの層が重なって、網目の
ように細かくなる（クロスハッチング）。

線は画素ではなく「線分の端点の座標」として求め、SVG（Scalable Vector
Graphics）形式のファイルに書き出す。SVG は拡大しても劣化せず、
ペンプロッターでそのまま描かせることもできる。SVG はテキスト形式の
XML なので、専用のライブラリを使わずに文字列として組み立てられる。
"""

from pathlib import Path

import numpy as np
from PIL import Image

# 各層の線の向き（度）と、その層を引き始める暗さのしきい値（0〜1）。
_LAYERS: list[tuple[float, float]] = [
    (45.0, 0.3),
    (-45.0, 0.5),
    (0.0, 0.7),
    (90.0, 0.85),
]


def load_darkness(path: Path) -> np.ndarray:
    """画像を読み込み、各画素の暗さ（0〜1、黒が 1）の配列を返す。

    元の画像の明るさの幅が狭くても全ての層が使われるよう、最も明るい
    画素が 0、最も暗い画素が 1 になるように引き伸ばす。
    """
    image: Image.Image = Image.open(path).convert("L")
    darkness: np.ndarray = 1.0 - np.asarray(image, dtype=float) / 255.0
    result: np.ndarray = (darkness - darkness.min()) / (darkness.max() - darkness.min())
    return result


def hatch_layer(
    darkness: np.ndarray, angle_deg: float, threshold: float, spacing: float
) -> list[tuple[float, float, float, float]]:
    """1 つの層の線分を返す。

    画面全体に角度 ``angle_deg`` の平行線を間隔 ``spacing`` で引き、
    各線を 1 ピクセルごとの点に分けて、暗さが ``threshold`` を超える
    点が続く区間だけを線分として残す。戻り値は (x0, y0, x1, y1) の
    リスト。
    """
    height: int = darkness.shape[0]
    width: int = darkness.shape[1]
    angle: float = np.radians(angle_deg)
    direction: np.ndarray = np.array([np.cos(angle), np.sin(angle)])
    normal: np.ndarray = np.array([-direction[1], direction[0]])
    center: np.ndarray = np.array([width / 2, height / 2])
    # 画面の対角線の半分あれば、どの向きの線も画面を横切れる。
    half: float = float(np.hypot(width, height)) / 2 + 1
    ts: np.ndarray = np.arange(-half, half, 1.0)  # 線に沿った位置

    segments: list[tuple[float, float, float, float]] = []
    for offset in np.arange(-half, half, spacing):
        points: np.ndarray = center + offset * normal + ts[:, np.newaxis] * direction
        inside: np.ndarray = (
            (points[:, 0] >= 0) & (points[:, 0] < width)
            & (points[:, 1] >= 0) & (points[:, 1] < height)
        )
        dark: np.ndarray = np.zeros(len(ts), dtype=bool)
        cols: np.ndarray = points[inside, 0].astype(np.int64)
        rows: np.ndarray = points[inside, 1].astype(np.int64)
        dark[inside] = darkness[rows, cols] > threshold

        # dark が True の区間の始まりと終わりを求める。
        edges: np.ndarray = np.diff(np.concatenate([[0], dark.astype(np.int8), [0]]))
        starts: np.ndarray = np.flatnonzero(edges == 1)
        ends: np.ndarray = np.flatnonzero(edges == -1) - 1
        for s, e in zip(starts, ends):
            if e - s < 2:
                continue  # 短すぎる線分は点のように見えるので省く
            x0, y0 = points[s]
            x1, y1 = points[e]
            segments.append((float(x0), float(y0), float(x1), float(y1)))
    return segments


def hatch(
    darkness: np.ndarray, spacing: float = 5.0
) -> list[tuple[float, float, float, float]]:
    """全ての層の線分をまとめて返す。"""
    segments: list[tuple[float, float, float, float]] = []
    for angle_deg, threshold in _LAYERS:
        segments += hatch_layer(darkness, angle_deg, threshold, spacing)
    return segments


def to_svg(
    segments: list[tuple[float, float, float, float]],
    width: int,
    height: int,
    stroke_width: float = 0.8,
) -> str:
    """線分の一覧を SVG の文字列に変換する。

    線分は 1 つの ``path`` 要素にまとめる。``M x y`` でペンを持ち上げて
    移動し、``L x y`` でそこまで線を引く、という命令を並べたもので、
    ペンプロッターの動きにそのまま対応する。
    """
    commands: str = " ".join(
        f"M{x0:.1f} {y0:.1f}L{x1:.1f} {y1:.1f}" for x0, y0, x1, y1 in segments
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        f'<rect width="{width}" height="{height}" fill="#f5f1e8"/>\n'
        f'<path d="{commands}" fill="none" stroke="#1e3250" '
        f'stroke-width="{stroke_width}" stroke-linecap="round"/>\n'
        "</svg>\n"
    )


def main() -> None:
    gallery: Path = Path("source/_static/gallery")
    darkness: np.ndarray = load_darkness(gallery / "raymarching.png")
    segments: list[tuple[float, float, float, float]] = hatch(darkness)
    print(f"segments: {len(segments)}")
    svg: str = to_svg(segments, darkness.shape[1], darkness.shape[0])
    Path("hatching.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
