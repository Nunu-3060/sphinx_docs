"""発展課題 11-A の解答例: モンテカルロ法によるスケジュールの見積もり（第 11 章）.

各作業の所要日数を 1 つの値ではなく、楽観値・最頻値・悲観値の 3 点で見積もる。
所要日数を三角分布に従う乱数として多数回シミュレーションし、
プロジェクト全体の所要日数の分布を求める。作業の構成は演習問題 11-1 と同じである。
"""

import random
import statistics

# 作業名: (楽観値, 最頻値, 悲観値)（日）
ESTIMATES: dict[str, tuple[float, float, float]] = {
    "A": (2, 3, 5),
    "B": (3, 4, 8),
    "C": (5, 7, 12),
    "D": (1, 2, 4),
    "E": (2, 3, 6),
    "F": (1, 2, 3),
}

# 作業名: 先行作業の一覧（先行作業が先に現れる順に並べる）
PREDECESSORS: dict[str, list[str]] = {
    "A": [],
    "B": ["A"],
    "C": ["A"],
    "D": ["B"],
    "E": ["C", "D"],
    "F": ["E"],
}


def project_duration(durations: dict[str, float]) -> float:
    """各作業の所要日数から、プロジェクト全体の所要日数を求める."""
    finish: dict[str, float] = {}
    for task, predecessors in PREDECESSORS.items():
        start = max((finish[p] for p in predecessors), default=0.0)
        finish[task] = start + durations[task]
    return max(finish.values())


def simulate(trials: int, seed: int) -> list[float]:
    """シミュレーションを ``trials`` 回行い、全体の所要日数の一覧を返す."""
    rng = random.Random(seed)
    results = []
    for _ in range(trials):
        durations = {
            task: rng.triangular(low, high, mode)
            for task, (low, mode, high) in ESTIMATES.items()
        }
        results.append(project_duration(durations))
    return results


def percentile(values: list[float], ratio: float) -> float:
    """``values`` のうち、小さいほうから ``ratio`` の位置にある値を返す."""
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(len(ordered) * ratio))
    return ordered[index]


if __name__ == "__main__":
    most_likely = project_duration(
        {task: mode for task, (_, mode, _) in ESTIMATES.items()}
    )
    results = simulate(trials=10_000, seed=1)
    print(f"最頻値だけで計算した所要日数: {most_likely:.1f} 日")
    print(f"シミュレーションの平均: {statistics.mean(results):.1f} 日")
    print(f"50 % の確率で終わる日数: {percentile(results, 0.5):.1f} 日")
    print(f"90 % の確率で終わる日数: {percentile(results, 0.9):.1f} 日")
    on_time = sum(1 for value in results if value <= most_likely)
    print(f"最頻値の日数以内に終わる確率: {on_time / len(results):.1%}")
