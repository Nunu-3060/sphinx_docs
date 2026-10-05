"""第 2 章: 次元を持つ量を計算し、単位の取り違えを検出する。

物理量を「数値」と「次元 (長さ L、質量 M、時間 T、電流 I の指数)」の組で
表す小さなクラスを作り、次の 3 点を確かめます。

* 掛け算・割り算では次元の指数が足し引きされること
* 次元の異なる量どうしの足し算はエラーになること
* ポンド重秒 (lbf·s) とニュートン秒 (N·s) を取り違えると、
  数値が約 4.45 倍ずれること

実行例::

    python ch02_dimension.py
"""

from __future__ import annotations

from dataclasses import dataclass

# 次元の指数 (L, M, T, I) の組
Dimension = tuple[int, int, int, int]

DIMENSIONLESS: Dimension = (0, 0, 0, 0)
LENGTH: Dimension = (1, 0, 0, 0)
MASS: Dimension = (0, 1, 0, 0)
TIME: Dimension = (0, 0, 1, 0)
CURRENT: Dimension = (0, 0, 0, 1)

# 1 lbf (ポンド重) をニュートンに換算する係数
NEWTON_PER_POUND_FORCE = 4.4482216152605


class DimensionError(ValueError):
    """次元が合わない演算をしたときに送出する例外。"""


def format_dimension(dim: Dimension) -> str:
    """次元の指数を ``L^1 M^1 T^-2`` のような文字列に変換する。"""
    symbols = ("L", "M", "T", "I")
    parts = [f"{s}^{e}" for s, e in zip(symbols, dim) if e != 0]
    return " ".join(parts) if parts else "無次元"


@dataclass(frozen=True)
class Quantity:
    """SI 単位で表した数値と、その次元の組。"""

    value: float
    dim: Dimension

    def __add__(self, other: Quantity) -> Quantity:
        if self.dim != other.dim:
            raise DimensionError(
                f"次元が異なる量は足せません: {format_dimension(self.dim)}"
                f" + {format_dimension(other.dim)}")
        return Quantity(self.value + other.value, self.dim)

    def __mul__(self, other: Quantity) -> Quantity:
        dim = tuple(a + b for a, b in zip(self.dim, other.dim))
        return Quantity(self.value * other.value, _as_dimension(dim))

    def __truediv__(self, other: Quantity) -> Quantity:
        dim = tuple(a - b for a, b in zip(self.dim, other.dim))
        return Quantity(self.value / other.value, _as_dimension(dim))

    def __str__(self) -> str:
        return f"{self.value:.6g} [{format_dimension(self.dim)}]"


def _as_dimension(values: tuple[int, ...]) -> Dimension:
    """長さ 4 のタプルを Dimension 型として返す。"""
    length, mass, time, current = values
    return (length, mass, time, current)


def main() -> None:
    mass = Quantity(1200.0, MASS)            # 自動車の質量 1200 kg
    distance = Quantity(100.0, LENGTH)       # 100 m
    duration = Quantity(4.0, TIME)           # 4 s

    # 速度 = 距離 / 時間、運動エネルギー = 質量 × 速度^2 / 2
    velocity = distance / duration
    half = Quantity(0.5, DIMENSIONLESS)
    energy = half * mass * velocity * velocity
    print(f"速度: {velocity}")
    print(f"運動エネルギー: {energy}  (L^2 M^1 T^-2 = J)")

    # 次元の異なる量を足すとエラーになる
    try:
        print(distance + duration)
    except DimensionError as error:
        print(f"エラーを検出しました: {error}")

    # 同じ次元でも単位を取り違えると検出できない
    impulse_lbf_s = 100.0  # 本当は lbf·s で計算した値
    impulse_n_s = impulse_lbf_s * NEWTON_PER_POUND_FORCE
    print(f"{impulse_lbf_s} lbf・s = {impulse_n_s:.1f} N・s")
    print("lbf・s の値を N・s と解釈すると、"
          f"力積を {NEWTON_PER_POUND_FORCE:.2f} 分の 1 に見積もります。")


if __name__ == "__main__":
    main()
