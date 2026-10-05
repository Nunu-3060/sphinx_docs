"""第 11 章: 信頼区間と並べ替え検定を計算する。

1. ハードウェアの例: 抵抗器 10 個の抵抗値を測定し、母平均の
   95 % 信頼区間を t 分布で求める
2. ソフトウェアの例: 改修前と改修後の応答時間を 20 回ずつ測定し、
   平均の差が偶然で説明できるかを並べ替え検定 (permutation test) で
   確かめる

外部の統計ライブラリーを使わずに計算できるように、t 分布の値は
表として持たせています。

実行例::

    python ch11_statistics.py
"""

from __future__ import annotations

import math
import random
import statistics

# 両側 95 % (片側 2.5 %) の t 分布の値。キーは自由度
T_975 = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    15: 2.131, 20: 2.086, 30: 2.042,
}

# 抵抗器 10 個の測定値 [Ω] (公称値 100 Ω)
RESISTANCES = [100.3, 99.8, 100.6, 100.1, 99.9,
               100.4, 100.2, 99.7, 100.5, 100.0]

# 応答時間の測定値 [ms]
BEFORE = [52.1, 49.8, 55.3, 51.0, 50.7, 53.9, 48.6, 52.8, 54.1, 50.2,
          51.7, 49.5, 53.0, 52.4, 50.9, 55.8, 51.3, 49.9, 52.6, 53.5]
AFTER = [49.2, 50.1, 47.8, 51.5, 48.9, 50.6, 47.5, 49.8, 52.0, 48.3,
         50.4, 49.0, 51.1, 47.9, 49.6, 50.8, 48.7, 49.3, 51.8, 48.1]


def confidence_interval(data: list[float]) -> tuple[float, float]:
    """母平均の両側 95 % 信頼区間を返す。"""
    n = len(data)
    mean = statistics.mean(data)
    standard_error = statistics.stdev(data) / math.sqrt(n)
    t = T_975.get(n - 1, 1.96)  # 表にない自由度では正規分布で近似する
    return mean - t * standard_error, mean + t * standard_error


def permutation_test(a: list[float], b: list[float], trials: int,
                     seed: int) -> float:
    """平均の差の両側並べ替え検定を行い、p 値を返す。

    「2 つのグループに差はない」と仮定すると、測定値のラベル
    (改修前・改修後) を入れ替えても差の分布は変わらないはずです。
    ラベルをランダムに入れ替えたときに、実際の差以上の差が
    出る割合を p 値とします。
    """
    observed = abs(statistics.mean(a) - statistics.mean(b))
    pooled = a + b
    rng = random.Random(seed)
    count = 0
    for _ in range(trials):
        rng.shuffle(pooled)
        diff = abs(statistics.mean(pooled[:len(a)])
                   - statistics.mean(pooled[len(a):]))
        if diff >= observed:
            count += 1
    return (count + 1) / (trials + 1)


def main() -> None:
    low, high = confidence_interval(RESISTANCES)
    print("1. 抵抗値の測定")
    print(f"   平均 {statistics.mean(RESISTANCES):.3f} Ω, "
          f"標準偏差 {statistics.stdev(RESISTANCES):.3f} Ω")
    print(f"   母平均の 95 % 信頼区間: {low:.3f}〜{high:.3f} Ω")

    print("2. 応答時間の比較")
    print(f"   改修前の平均 {statistics.mean(BEFORE):.2f} ms, "
          f"改修後の平均 {statistics.mean(AFTER):.2f} ms")
    p_value = permutation_test(BEFORE, AFTER, trials=20_000, seed=0)
    print(f"   並べ替え検定の p 値: {p_value:.4f}")
    if p_value < 0.05:
        print("   有意水準 5 % で「差がない」という仮説を棄却します。")
    else:
        print("   有意水準 5 % では、差があるとは言えません。")


if __name__ == "__main__":
    main()
