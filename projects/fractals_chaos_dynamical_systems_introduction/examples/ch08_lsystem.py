"""L-system（リンデンマイヤー・システム）: 文字列の書き換えでフラクタル図形を描く.

1. 初期の文字列（公理）に、書き換え規則を全文字同時に適用することを繰り返す。
2. できた文字列を、タートルグラフィックスの命令として解釈して線を引く。

  F, G : 前に進みながら線を引く
  +    : 左に angle 度回る
  -    : 右に angle 度回る
  [    : 現在の位置と向きをスタックに積む（枝分かれの始まり）
  ]    : スタックから位置と向きを取り出す（枝の付け根に戻る）
  その他の文字（X など）: 描画には使わず、書き換えのためだけに使う

使い方: python ch08_lsystem.py [--save DIR]
"""

import math
from dataclasses import dataclass

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.figure import Figure

import plot_util

Segment = tuple[tuple[float, float], tuple[float, float]]


@dataclass
class LSystem:
    """L-system の定義."""

    name: str
    axiom: str
    rules: dict[str, str]
    angle: float  # 回転角（度）
    iterations: int
    start_heading: float = 0.0  # 最初の向き（度、右向きが 0）


def rewrite(axiom: str, rules: dict[str, str], iterations: int) -> str:
    """書き換え規則を iterations 回適用した文字列を返す（規則がない文字はそのまま残す）."""
    s = axiom
    for _ in range(iterations):
        s = "".join(rules.get(ch, ch) for ch in s)
    return s


def turtle_segments(commands: str, angle: float, heading: float = 0.0) -> list[Segment]:
    """タートルグラフィックスの命令列を解釈し、引いた線分の一覧を返す."""
    x, y = 0.0, 0.0
    stack: list[tuple[float, float, float]] = []
    segments: list[Segment] = []
    for ch in commands:
        if ch in "FG":
            nx = x + math.cos(math.radians(heading))
            ny = y + math.sin(math.radians(heading))
            segments.append(((x, y), (nx, ny)))
            x, y = nx, ny
        elif ch == "+":
            heading += angle
        elif ch == "-":
            heading -= angle
        elif ch == "[":
            stack.append((x, y, heading))
        elif ch == "]":
            x, y, heading = stack.pop()
    return segments


EXAMPLES = [
    LSystem("コッホ曲線", "F", {"F": "F+F--F+F"}, 60.0, 4),
    LSystem("ドラゴン曲線", "F", {"F": "F+G", "G": "F-G"}, 90.0, 12),
    LSystem("シェルピンスキーの矢じり曲線", "F", {"F": "G-F-G", "G": "F+G+F"}, 60.0, 7),
    LSystem("植物", "X", {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}, 25.0, 6, 75.0),
]


def create_figures() -> dict[str, Figure]:
    """4 種類の L-system の図を並べる（gallery）."""
    fig, axes = plt.subplots(1, 4, figsize=(14.0, 4.2))
    for ax, system in zip(axes, EXAMPLES):
        commands = rewrite(system.axiom, system.rules, system.iterations)
        segments = turtle_segments(commands, system.angle, system.start_heading)
        color = "#2e7d32" if system.name == "植物" else "k"
        ax.add_collection(LineCollection(segments, colors=color, linewidths=0.6))
        ax.autoscale()
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{system.name}（{system.iterations} 回）")
    fig.tight_layout()
    return {"gallery": fig}


def report() -> None:
    """植物の例で、書き換えのたびに文字列が長くなる様子を表示する."""
    system = EXAMPLES[3]
    for n in range(4):
        s = rewrite(system.axiom, system.rules, n)
        preview = s if len(s) <= 60 else s[:60] + "..."
        print(f"{n} 回: 長さ {len(s):5d}  {preview}")


def main() -> None:
    plot_util.run_sample(__doc__ or "", create_figures, report)


if __name__ == "__main__":
    main()
