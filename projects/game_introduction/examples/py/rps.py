"""勝ったときの得点が手ごとに違うじゃんけんの最適な混合戦略を求める（5 章、8 章）。

例として、グーで勝つと 3 歩、チョキとパーで勝つと 6 歩進む遊び（グリコ）を扱う。
得点は相手との差（ゼロ和）とし、相手がどの手を出しても期待値が同じになる手の割合を求める。

実行方法:
    py rps.py            グリコの得点で計算する
    py rps.py 1 1 1      グー、パー、チョキで勝ったときの得点を指定する
"""

import random
import sys

import numpy as np
import numpy.typing as npt

HANDS = ["グー", "パー", "チョキ"]


def payoff_matrix(points: tuple[float, float, float]) -> npt.NDArray[np.float64]:
    """行の手を出した側が得る点（相手との差）の表を返す。

    points はグー、パー、チョキで勝ったときの得点。
    """
    rock, paper, scissors = points
    return np.array([
        [0.0, -paper, rock],        # グー: パーに負け、チョキに勝つ
        [paper, 0.0, -scissors],    # パー: グーに勝ち、チョキに負ける
        [-rock, scissors, 0.0],     # チョキ: グーに負け、パーに勝つ
    ])


def equilibrium(points: tuple[float, float, float]) -> npt.NDArray[np.float64]:
    """どの手の期待値も 0 になる混合戦略（ナッシュ均衡）を求める。

    A p = 0 と p の和 = 1 を連立して最小二乗法で解く。
    """
    a = payoff_matrix(points)
    system = np.vstack([a, np.ones(3)])
    rhs = np.array([0.0, 0.0, 0.0, 1.0])
    solution, *_ = np.linalg.lstsq(system, rhs, rcond=None)
    return np.asarray(solution, dtype=np.float64)


def simulate(points: tuple[float, float, float], mine: list[float], theirs: list[float], rounds: int,
             seed: int = 1) -> float:
    """2 つの混合戦略を対戦させ、1 回あたりの平均得点を返す。"""
    rng = random.Random(seed)
    a = payoff_matrix(points)
    total = 0.0
    for _ in range(rounds):
        i = rng.choices(range(3), weights=mine)[0]
        j = rng.choices(range(3), weights=theirs)[0]
        total += float(a[i, j])
    return total / rounds


def main() -> None:
    values = [float(v) for v in sys.argv[1:4]] or [3.0, 6.0, 6.0]
    points = (values[0], values[1], values[2])
    p = equilibrium(points)
    print("勝ったときの得点: " + "、".join(f"{h} {v:g}" for h, v in zip(HANDS, points)))
    print("最適な割合:       " + "、".join(f"{h} {x:.3f}" for h, x in zip(HANDS, p)))
    a = payoff_matrix(points)
    uniform = np.full(3, 1 / 3)
    print("最適な割合の相手に対する各手の期待値: " + "、".join(f"{h} {round(v, 9) + 0.0:+.3f}" for h, v in zip(HANDS, a @ p)))
    print("均等に出す相手に対する各手の期待値:   " + "、".join(f"{h} {round(v, 9) + 0.0:+.3f}" for h, v in zip(HANDS, a @ uniform)))
    best = int(np.argmax(a @ uniform))
    mine = [1.0 if i == best else 0.0 for i in range(3)]
    result = simulate(points, mine, list(uniform), 100_000)
    print(f"均等に出す相手に毎回{HANDS[best]}を出したときの平均得点（シミュレーション）: {result:+.3f}")


if __name__ == "__main__":
    main()
