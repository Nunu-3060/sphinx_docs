"""可用性の計算（第 10 章）.

可用性 A は MTBF（平均故障間隔）と MTTR（平均修復時間）から
A = MTBF / (MTBF + MTTR) で求める。
直列構成では各要素の可用性の積、並列構成では
1 - (各要素の不可用率の積) がシステム全体の可用性となる。
"""

import math


def availability(mtbf_hours: float, mttr_hours: float) -> float:
    """MTBF と MTTR から可用性を返す."""
    if mtbf_hours <= 0 or mttr_hours < 0:
        raise ValueError("MTBF は正、MTTR は 0 以上を指定すること")
    return mtbf_hours / (mtbf_hours + mttr_hours)


def series(values: list[float]) -> float:
    """直列構成（すべてが動作して初めて動作する）の可用性を返す."""
    return math.prod(values)


def parallel(values: list[float]) -> float:
    """並列構成（どれか 1 つが動作すれば動作する）の可用性を返す."""
    return 1 - math.prod(1 - a for a in values)


def downtime_hours_per_year(value: float) -> float:
    """可用性から 1 年あたりの停止時間（時間）を返す."""
    return (1 - value) * 365 * 24


if __name__ == "__main__":
    server = availability(mtbf_hours=1000, mttr_hours=10)
    print(f"サーバー 1 台: {server:.4f}")
    print(f"2 台を直列: {series([server, server]):.4f}")
    print(f"2 台を並列: {parallel([server, server]):.4f}")
    print(f"1 台の年間停止時間: {downtime_hours_per_year(server):.1f} 時間")
