"""第 9 章: 重み付き評価マトリクスで設計案を比較する。

工場内の温度センサー 50 台からデータを集める通信方式を、
3 つの案から選ぶ、という想定です。

* 評価項目ごとに重みを決め、各案を 1〜5 点で採点して総合点を求める
* 重みを少し変えても 1 位が入れ替わらないか (感度) を確かめる

実行例::

    python ch09_decision_matrix.py
"""

from __future__ import annotations

import itertools

# 評価項目と重み (合計 1.0)
WEIGHTS: dict[str, float] = {
    "導入コスト": 0.25,
    "消費電力": 0.20,
    "通信の信頼性": 0.30,
    "設置の容易さ": 0.15,
    "開発工数": 0.10,
}

# 各案の採点 (5 が最も良い)
SCORES: dict[str, dict[str, int]] = {
    "有線 (RS-485)": {
        "導入コスト": 2, "消費電力": 4, "通信の信頼性": 5,
        "設置の容易さ": 1, "開発工数": 4,
    },
    "Wi-Fi": {
        "導入コスト": 4, "消費電力": 2, "通信の信頼性": 3,
        "設置の容易さ": 4, "開発工数": 4,
    },
    "BLE メッシュ": {
        "導入コスト": 4, "消費電力": 5, "通信の信頼性": 3,
        "設置の容易さ": 4, "開発工数": 2,
    },
}


def total_scores(weights: dict[str, float]) -> dict[str, float]:
    """重みに従って各案の総合点を計算する。"""
    total = sum(weights.values())
    return {
        option: sum(weights[c] * s for c, s in scores.items()) / total
        for option, scores in SCORES.items()
    }


def best_option(weights: dict[str, float]) -> str:
    """総合点が最も高い案を返す。"""
    totals = total_scores(weights)
    return max(totals, key=lambda option: totals[option])


def sensitivity(delta: float) -> dict[str, int]:
    """各重みを ±delta だけ変えた組み合わせで、1 位になった回数を数える。"""
    counts = {option: 0 for option in SCORES}
    criteria = list(WEIGHTS)
    for signs in itertools.product((-1, 0, 1), repeat=len(criteria)):
        weights = {
            c: max(0.0, WEIGHTS[c] + sign * delta)
            for c, sign in zip(criteria, signs)
        }
        counts[best_option(weights)] += 1
    return counts


def main() -> None:
    print("総合点 (5 点満点)")
    totals = total_scores(WEIGHTS)
    for option, score in sorted(totals.items(), key=lambda item: -item[1]):
        print(f"  {option:14s}: {score:.2f}")

    delta = 0.05
    counts = sensitivity(delta)
    trials = sum(counts.values())
    print(f"\n各重みを ±{delta} 変えた {trials} 通りで 1 位になった回数")
    for option, count in counts.items():
        print(f"  {option:14s}: {count:4d} 回 ({count / trials:.0%})")


if __name__ == "__main__":
    main()
