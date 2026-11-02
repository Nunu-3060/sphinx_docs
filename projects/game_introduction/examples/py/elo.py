"""イロレーティングで強さを測る（5 章）。

実力の違う 3 人に総当たりを繰り返させ、レーティングが実力の順に分かれていく様子を表示する。

実行方法: py elo.py
"""

import random

K = 32  # 1 試合でレーティングが動く大きさの上限


def expected_score(rating_a: float, rating_b: float) -> float:
    """A が B に勝つ見込み（勝ちを 1、負けを 0 としたときの期待値）を返す。"""
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update(rating_a: float, rating_b: float, score_a: float) -> tuple[float, float]:
    """試合結果 score_a（勝ち 1、引き分け 0.5、負け 0）から、新しいレーティングを返す。"""
    delta = K * (score_a - expected_score(rating_a, rating_b))
    return rating_a + delta, rating_b - delta


def main() -> None:
    rng = random.Random(1)
    # 本当の強さ（プレイヤーには見えない）。この差から勝率を決める
    true_strength = {"A さん": 1700.0, "B さん": 1500.0, "C さん": 1300.0}
    ratings = {name: 1500.0 for name in true_strength}
    names = list(true_strength)
    for round_no in range(1, 101):
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                win = rng.random() < expected_score(true_strength[a], true_strength[b])
                ratings[a], ratings[b] = update(ratings[a], ratings[b], 1.0 if win else 0.0)
        if round_no in (1, 5, 20, 100):
            print(f"{round_no:3d} 回戦後: " + "  ".join(f"{n} {r:6.0f}" for n, r in ratings.items()))
    print(f"1700 と 1500 の対戦で強い方が勝つ見込み: {expected_score(1700, 1500):.2f}")


if __name__ == "__main__":
    main()
