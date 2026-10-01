"""選考結果の公平性を属性別に確認するサンプルです。

AI モデルや選考ルールが、特定の属性の人を不利に扱っていないかを
数値で確認します。ここでは次の 2 つの指標を計算します。

* 選考通過率の差（人口統計学的パリティの差）
* 格差影響比（最も低い通過率 / 最も高い通過率）

格差影響比が 0.8 を下回る場合は、米国の雇用選考の指針で使われる
「4/5 ルール」に照らして、不利益な影響の疑いがあると判断します。
指標はあくまで調査のきっかけであり、基準を満たせば公平である、
という意味ではない点に注意してください。

実行方法::

    python fairness_check.py
"""

from dataclasses import dataclass

FOUR_FIFTHS_THRESHOLD = 0.8


@dataclass(frozen=True)
class Applicant:
    """応募者 1 人分の選考結果です。"""

    group: str
    passed: bool


def pass_rates(applicants: list[Applicant]) -> dict[str, float]:
    """属性ごとの選考通過率を計算します。"""
    totals: dict[str, int] = {}
    passes: dict[str, int] = {}
    for applicant in applicants:
        totals[applicant.group] = totals.get(applicant.group, 0) + 1
        if applicant.passed:
            passes[applicant.group] = passes.get(applicant.group, 0) + 1
    return {group: passes.get(group, 0) / total
            for group, total in totals.items()}


def parity_difference(rates: dict[str, float]) -> float:
    """最も高い通過率と最も低い通過率の差を返します。"""
    return max(rates.values()) - min(rates.values())


def disparate_impact(rates: dict[str, float]) -> float:
    """最も低い通過率を最も高い通過率で割った比を返します。"""
    highest = max(rates.values())
    if highest == 0:
        raise ValueError("全員が不合格のため、比を計算できません。")
    return min(rates.values()) / highest


def make_sample() -> list[Applicant]:
    """属性 A は 100 人中 60 人、属性 B は 100 人中 42 人が通過したデータです。"""
    group_a = [Applicant("A", i < 60) for i in range(100)]
    group_b = [Applicant("B", i < 42) for i in range(100)]
    return group_a + group_b


def main() -> None:
    """サンプルデータで公平性の指標を計算し、結果を表示します。"""
    rates = pass_rates(make_sample())
    for group, rate in sorted(rates.items()):
        print(f"属性 {group} の通過率: {rate:.2f}")

    difference = parity_difference(rates)
    ratio = disparate_impact(rates)
    print(f"通過率の差: {difference:.2f}")
    print(f"格差影響比: {ratio:.2f}")

    if ratio < FOUR_FIFTHS_THRESHOLD:
        print("4/5 ルールを下回っています。原因を調査してください。")
    else:
        print("4/5 ルールは満たしています。他の観点からも確認してください。")


if __name__ == "__main__":
    main()
