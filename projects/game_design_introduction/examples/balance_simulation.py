"""Monte Carlo 法によるユニットの勝率の検証。

「戦士」（体力が高く、攻撃が安定している）と「盗賊」（体力は低いが、会心の一撃が出る）を
何度も戦わせ、盗賊の会心率を変えたときに勝率がどう変わるかを調べる。

実行例:
    python balance_simulation.py                     # 結果を表示し、グラフを画面に出す
    python balance_simulation.py --output win.png    # グラフを画像として保存する
    python balance_simulation.py --battles 20000     # 試行回数を増やす
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

import matplotlib.pyplot as plt


@dataclass(frozen=True)
class Unit:
    """戦闘ユニットの能力値。"""

    name: str
    hp: int
    damage: int
    hit_rate: float  # 攻撃が当たる確率
    crit_rate: float = 0.0  # 当たったときに会心になる確率
    crit_multiplier: float = 1.0  # 会心のときのダメージ倍率

    def expected_damage(self) -> float:
        """1 回の攻撃で与えるダメージの期待値。"""
        crit_bonus = self.crit_rate * (self.crit_multiplier - 1.0)
        return self.hit_rate * self.damage * (1.0 + crit_bonus)

    def attack(self, rng: random.Random) -> int:
        """1 回攻撃し、与えたダメージを返す。"""
        if rng.random() >= self.hit_rate:
            return 0
        if rng.random() < self.crit_rate:
            return round(self.damage * self.crit_multiplier)
        return self.damage


WARRIOR = Unit("戦士", hp=100, damage=10, hit_rate=0.9)


def make_rogue(crit_rate: float) -> Unit:
    return Unit("盗賊", hp=75, damage=8, hit_rate=0.95, crit_rate=crit_rate, crit_multiplier=2.5)


def battle(first: Unit, second: Unit, rng: random.Random) -> Unit:
    """2 体を交互に攻撃させ、勝ったほうを返す。"""
    hp = {first.name: first.hp, second.name: second.hp}
    attacker, defender = first, second
    while True:
        hp[defender.name] -= attacker.attack(rng)
        if hp[defender.name] <= 0:
            return attacker
        attacker, defender = defender, attacker


def win_rate(unit: Unit, opponent: Unit, battles: int, rng: random.Random) -> float:
    """unit が opponent に勝つ割合。先攻と後攻は半分ずつにする。"""
    wins = 0
    for i in range(battles):
        first, second = (unit, opponent) if i % 2 == 0 else (opponent, unit)
        if battle(first, second, rng) is unit:
            wins += 1
    return wins / battles


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", help="グラフを保存するファイル名（省略時は画面に表示する）")
    parser.add_argument("--battles", type=int, default=5000, help="会心率 1 通りあたりの試行回数")
    parser.add_argument("--seed", type=int, default=1, help="乱数のシード")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    crit_rates = [i / 100 for i in range(0, 51, 5)]
    rates: list[float] = []
    print(f"戦士の期待ダメージ: {WARRIOR.expected_damage():.2f}")
    for crit in crit_rates:
        rogue = make_rogue(crit)
        rate = win_rate(rogue, WARRIOR, args.battles, rng)
        rates.append(rate)
        print(f"会心率 {crit:4.0%}: 盗賊の期待ダメージ {rogue.expected_damage():5.2f}, 盗賊の勝率 {rate:6.1%}")

    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot([c * 100 for c in crit_rates], [r * 100 for r in rates], marker="o", linewidth=2, label="盗賊の勝率")
    ax.axhline(50, color="gray", linestyle="--", label="勝率 50 %")
    ax.set_xlabel("盗賊の会心率 [%]")
    ax.set_ylabel("盗賊の勝率 [%]")
    ax.set_ylim(0, 100)
    ax.set_title(f"会心率と勝率（各 {args.battles} 戦）")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()

    if args.output:
        fig.savefig(args.output, dpi=110)
    else:
        plt.show()


if __name__ == "__main__":
    main()
