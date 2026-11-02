"""忘却曲線と復習の効果を簡易モデルで計算し、グラフにする。

使い方:
    py forgetting_curve.py                      # 1, 3, 7, 14 日目に復習する例
    py forgetting_curve.py --reviews 2 5 12     # 復習日を指定する
    py forgetting_curve.py --reviews            # 復習しない場合

結果は表として画面に表示し、グラフを output/forgetting_curve.png に保存する。

モデル:
    保持率 R(t) = 1 / (1 + t / (9 * S))
        t: 最後の学習からの経過日数
        S: 安定性（保持率が 0.9 まで下がるのにかかる日数）
    復習すると安定性 S は BASE_GAIN + GAIN * (1 - R) 倍になる。
    R は復習した時点の保持率で、思い出しにくくなってから復習するほど安定性が大きく伸びる。

これは仕組みを理解するための簡易モデルであり、実際の記憶を正確に予測するものではない。
"""

from __future__ import annotations

import argparse
import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402

INITIAL_STABILITY = 1.0  # 初回学習後の安定性（日）
BASE_GAIN = 1.3  # 復習による安定性の伸び（最小値）
GAIN = 8.0  # 思い出しにくさに応じた安定性の伸び
OUTPUT_DIR = pathlib.Path(__file__).resolve().parent / "output"


def retention(elapsed: float, stability: float) -> float:
    """最後の学習から elapsed 日後の保持率を返す。"""
    return 1.0 / (1.0 + elapsed / (9.0 * stability))


def simulate(review_days: list[float], end_day: float, step: float = 0.05) -> tuple[list[float], list[float]]:
    """0 日目に初めて学習し、review_days に復習したときの保持率の推移を返す。

    戻り値は (経過日数のリスト, 保持率のリスト) である。
    """
    days: list[float] = []
    values: list[float] = []
    reviews = sorted(review_days)
    stability = INITIAL_STABILITY
    last_study = 0.0
    next_index = 0
    n_steps = int(end_day / step)
    for i in range(n_steps + 1):
        day = i * step
        # この時点までに予定されている復習をすべて反映する。
        while next_index < len(reviews) and reviews[next_index] <= day:
            review_day = reviews[next_index]
            recall = retention(review_day - last_study, stability)
            stability *= BASE_GAIN + GAIN * (1.0 - recall)
            last_study = review_day
            next_index += 1
        days.append(day)
        values.append(retention(day - last_study, stability))
    return days, values


def retention_before(review_days: list[float], target: float) -> float:
    """target 日目の保持率を返す。

    target 日目に復習する場合は、その復習をする直前の値を返す。
    """
    stability = INITIAL_STABILITY
    last_study = 0.0
    for review_day in sorted(review_days):
        if review_day >= target:
            break
        recall = retention(review_day - last_study, stability)
        stability *= BASE_GAIN + GAIN * (1.0 - recall)
        last_study = review_day
    return retention(target - last_study, stability)


def main() -> None:
    parser = argparse.ArgumentParser(description="忘却曲線と復習の効果を簡易モデルで計算する。")
    parser.add_argument("--reviews", type=float, nargs="*", default=[1.0, 3.0, 7.0, 14.0], help="復習する日（初回学習からの経過日数）")
    parser.add_argument("--days", type=float, default=30.0, help="計算する日数")
    args = parser.parse_args()

    reviews: list[float] = args.reviews
    end_day: float = args.days

    base_days, base_values = simulate([], end_day)
    days, values = simulate(reviews, end_day)

    print(f"復習日: {reviews if reviews else 'なし'}")
    # 全角文字は半角 2 文字分の幅で表示されるため、見出しは空白で位置を合わせる。
    print("経過日数 復習しない   復習する（復習日は復習直前の値）")
    for check_day in [2, 5, 10, 20, 30]:
        if check_day > end_day:
            break
        no_review = retention_before([], check_day)
        with_review = retention_before(reviews, check_day)
        print(f"{check_day:>8} {no_review:>10.2f} {with_review:>10.2f}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.plot(base_days, base_values, linestyle="--", label="no review")
    ax.plot(days, values, label=f"review on days {reviews}")
    ax.set_xlabel("days since first study")
    ax.set_ylabel("retention (model)")
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower left")
    fig.tight_layout()
    path = OUTPUT_DIR / "forgetting_curve.png"
    fig.savefig(path, dpi=100)
    plt.close(fig)
    print(f"グラフを保存した: {path}")


if __name__ == "__main__":
    main()
