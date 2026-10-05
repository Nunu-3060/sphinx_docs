"""第 11 章: 2 水準 3 因子の要因実験で、主効果と交互作用を求める。

接着剤の硬化条件として、次の 3 因子を 2 水準ずつ変え、全 8 通りの
条件で接着強度を測定した、という想定です。

* A: 硬化温度 (低 / 高)
* B: 硬化時間 (短 / 長)
* C: 塗布量 (少 / 多)

各効果は「その因子が + 水準のときの平均 - 水準のときの平均」で
求めます。

実行例::

    python ch11_doe.py
"""

from __future__ import annotations

import itertools
import statistics

FACTORS = ("A", "B", "C")

# 条件 (A, B, C の水準: -1 または +1) と、測定した接着強度 [MPa]
RESULTS: dict[tuple[int, int, int], float] = {
    (-1, -1, -1): 47.1,
    (+1, -1, -1): 49.0,
    (-1, +1, -1): 43.2,
    (+1, +1, -1): 57.3,
    (-1, -1, +1): 46.6,
    (+1, -1, +1): 49.5,
    (-1, +1, +1): 42.9,
    (+1, +1, +1): 56.8,
}


def effect(columns: tuple[int, ...]) -> float:
    """指定した因子 (の積) の効果を計算する。

    columns が (0,) なら A の主効果、(0, 1) なら A と B の交互作用です。
    """
    plus: list[float] = []
    minus: list[float] = []
    for levels, value in RESULTS.items():
        sign = 1
        for column in columns:
            sign *= levels[column]
        (plus if sign > 0 else minus).append(value)
    return statistics.mean(plus) - statistics.mean(minus)


def main() -> None:
    print("実験条件と結果")
    print("   A   B   C   強度[MPa]")
    for (a, b, c), value in RESULTS.items():
        print(f"  {a:+d}  {b:+d}  {c:+d}   {value:6.1f}")

    print("\n効果の大きさ (絶対値の大きい順)")
    effects = {}
    for size in (1, 2, 3):
        for columns in itertools.combinations(range(3), size):
            name = "×".join(FACTORS[c] for c in columns)
            effects[name] = effect(columns)
    for name, value in sorted(effects.items(), key=lambda e: -abs(e[1])):
        print(f"  {name:6s}: {value:+6.2f} MPa")


if __name__ == "__main__":
    main()
