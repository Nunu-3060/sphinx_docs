"""基本 COCOMO による工数と開発期間の見積もり（第 11 章）.

工数 E（人月）と開発期間 D（月）を次の式で求める。

* E = a * KLOC ** b
* D = c * E ** d

係数はプロジェクトの種類（モード）によって異なる（Boehm, 1981）。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Coefficients:
    """基本 COCOMO の係数."""

    a: float
    b: float
    c: float
    d: float


MODES: dict[str, Coefficients] = {
    "organic": Coefficients(2.4, 1.05, 2.5, 0.38),
    "semi-detached": Coefficients(3.0, 1.12, 2.5, 0.35),
    "embedded": Coefficients(3.6, 1.20, 2.5, 0.32),
}


def estimate(kloc: float, mode: str) -> tuple[float, float]:
    """規模 ``kloc``（千行）とモードから (工数, 開発期間) を返す."""
    if kloc <= 0:
        raise ValueError("規模は正の値を指定すること")
    k = MODES[mode]
    effort = k.a * kloc**k.b
    duration = k.c * effort**k.d
    return effort, duration


if __name__ == "__main__":
    for mode in MODES:
        effort, duration = estimate(kloc=50, mode=mode)
        staff = effort / duration
        print(
            f"{mode}: 工数 {effort:.1f} 人月, "
            f"期間 {duration:.1f} か月, 平均要員 {staff:.1f} 人"
        )
