"""資源の流れとフィードバックループのシミュレーション。

2 人のプレイヤーが毎ターンさいころを振って金貨を得る、という単純な経済を考え、
次の 3 つのルールで「2 人の所持金の差」がどう変わるかを比べる。

* fixed    : 収入はさいころの目だけ（フィードバックなし）
* positive : 所持金の 10 % が利子として増える（正のフィードバック）
* rubber   : positive に加え、負けている側が差の 20 % を補助として受け取る（負のフィードバック）

実行例:
    python resource_flow.py                  # グラフを画面に表示する
    python resource_flow.py --output gap.png # グラフを画像として保存する
"""

from __future__ import annotations

import argparse
import random
from collections.abc import Callable

import matplotlib.pyplot as plt

TURNS = 30
RUNS = 2000
INTEREST_RATE = 0.10
CATCH_UP_RATE = 0.20

# 1 ターン分の更新処理: (自分の所持金, 相手の所持金, さいころの目) → 新しい所持金
Rule = Callable[[float, float, int], float]


def fixed_income(gold: float, rival: float, dice: int) -> float:
    return gold + dice


def positive_feedback(gold: float, rival: float, dice: int) -> float:
    return gold + dice + gold * INTEREST_RATE


def rubber_band(gold: float, rival: float, dice: int) -> float:
    bonus = (rival - gold) * CATCH_UP_RATE if gold < rival else 0.0
    return positive_feedback(gold, rival, dice) + bonus


RULES: dict[str, Rule] = {
    "fixed（フィードバックなし）": fixed_income,
    "positive（正のフィードバック）": positive_feedback,
    "rubber（正＋負のフィードバック）": rubber_band,
}


def simulate_gap(rule: Rule, rng: random.Random) -> list[float]:
    """1 回のゲームを最後まで進め、各ターン終了時の所持金の差を返す。"""
    a = b = 0.0
    gaps: list[float] = []
    for _ in range(TURNS):
        dice_a, dice_b = rng.randint(1, 6), rng.randint(1, 6)
        a, b = rule(a, b, dice_a), rule(b, a, dice_b)  # 2 人を同時に更新する
        gaps.append(abs(a - b))
    return gaps


def average_gap(rule: Rule, seed: int) -> list[float]:
    """RUNS 回のゲームについて、ターンごとの差の平均を求める。"""
    rng = random.Random(seed)
    totals = [0.0] * TURNS
    for _ in range(RUNS):
        for turn, gap in enumerate(simulate_gap(rule, rng)):
            totals[turn] += gap
    return [total / RUNS for total in totals]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", help="グラフを保存するファイル名（省略時は画面に表示する）")
    parser.add_argument("--seed", type=int, default=1, help="乱数のシード")
    args = parser.parse_args()

    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(7, 4))
    turns = list(range(1, TURNS + 1))
    for label, rule in RULES.items():
        gaps = average_gap(rule, args.seed)
        ax.plot(turns, gaps, label=label, linewidth=2)
        print(f"{label}: {TURNS} ターン後の平均の差 = {gaps[-1]:.1f}")
    ax.set_xlabel("ターン")
    ax.set_ylabel("2 人の所持金の差（平均）")
    ax.set_title("フィードバックループと所持金の差")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=110)
    else:
        plt.show()


if __name__ == "__main__":
    main()
