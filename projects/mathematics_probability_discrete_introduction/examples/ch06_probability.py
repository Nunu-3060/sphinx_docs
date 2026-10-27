"""第 6 章 確率の基礎のサンプルコード。

標本空間を全列挙して厳密な確率を求め、モンテカルロ・シミュレーションの結果と比較する。
"""

import random
from fractions import Fraction
from itertools import product


def two_dice_probabilities() -> None:
    """2 個のサイコロの標本空間を全列挙し、事象の確率と条件付き確率を求める。"""
    omega = list(product(range(1, 7), repeat=2))
    sum_is_7 = [w for w in omega if sum(w) == 7]
    first_is_3 = [w for w in omega if w[0] == 3]
    sum_is_8 = [w for w in omega if sum(w) == 8]
    both = [w for w in first_is_3 if sum(w) == 8]

    print(f"|Ω| = {len(omega)}")
    print(f"P(和が 7) = {Fraction(len(sum_is_7), len(omega))}")
    print(f"P(和が 8) = {Fraction(len(sum_is_8), len(omega))}")
    print(f"P(和が 8 | 1 個目が 3) = {Fraction(len(both), len(first_is_3))}")


def birthday_exact(n: int, days: int = 365) -> float:
    """n 人の中に誕生日が一致する組が少なくとも 1 組ある確率を返す。"""
    p_all_distinct = 1.0
    for i in range(n):
        p_all_distinct *= (days - i) / days
    return 1.0 - p_all_distinct


def birthday_simulation(n: int, trials: int, rng: random.Random, days: int = 365) -> float:
    """誕生日問題をシミュレーションで推定する。"""
    hits = 0
    for _ in range(trials):
        birthdays = [rng.randrange(days) for _ in range(n)]
        if len(set(birthdays)) < n:
            hits += 1
    return hits / trials


def monty_hall(trials: int, switch: bool, rng: random.Random) -> float:
    """モンティ・ホール問題で当たりを引く割合をシミュレーションで求める。"""
    wins = 0
    for _ in range(trials):
        car = rng.randrange(3)
        choice = rng.randrange(3)
        # 司会者は、挑戦者が選んでおらず車もない扉を 1 つ開ける
        opened = rng.choice([d for d in range(3) if d != choice and d != car])
        if switch:
            choice = next(d for d in range(3) if d != choice and d != opened)
        wins += choice == car
    return wins / trials


def bayes_posterior(prior: float, sensitivity: float, specificity: float) -> float:
    """検査で陽性と判定されたときに実際に罹患している確率をベイズの定理で求める。"""
    p_positive = sensitivity * prior + (1 - specificity) * (1 - prior)
    return sensitivity * prior / p_positive


def main() -> None:
    rng = random.Random(2026)

    print("--- 2 個のサイコロ ---")
    two_dice_probabilities()

    print("--- 誕生日問題 ---")
    for n in [10, 23, 30, 50]:
        print(f"n={n}: 厳密値={birthday_exact(n):.4f}  シミュレーション={birthday_simulation(n, 10000, rng):.4f}")

    print("--- モンティ・ホール問題 ---")
    print(f"選択を変えない: {monty_hall(100000, False, rng):.4f}")
    print(f"選択を変える  : {monty_hall(100000, True, rng):.4f}")

    print("--- ベイズの定理 ---")
    posterior = bayes_posterior(prior=0.01, sensitivity=0.99, specificity=0.95)
    print(f"P(罹患 | 陽性) = {posterior:.4f}")


if __name__ == "__main__":
    main()
