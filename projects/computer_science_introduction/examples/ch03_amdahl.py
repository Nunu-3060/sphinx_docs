"""アムダールの法則で、並列化による速度向上率の上限を計算するサンプル。

プログラムのうち並列化できる部分の割合 p と、コア数 n から、
速度向上率 S(n) = 1 / ((1 - p) + p / n) を計算して表にする。
n を無限に大きくしたときの上限 1 / (1 - p) と、
コア 1 個あたりの効率 S(n) / n も表示する。

実行方法: python ch03_amdahl.py
関連する章: 第 3 章「コンピュータの構成」（並列化の限界とアムダールの法則）
"""

import math

CORES = [1, 2, 4, 8, 16, 64, 1024]
FRACTIONS = [0.5, 0.9, 0.95, 0.99]


def speedup(p: float, n: int) -> float:
    """並列化率 p、コア数 n のときの速度向上率を返す。"""
    return 1.0 / ((1.0 - p) + p / n)


def limit(p: float) -> float:
    """コア数を無限に増やしたときの速度向上率の上限を返す。"""
    return math.inf if p == 1.0 else 1.0 / (1.0 - p)


def print_table(title: str, value: str) -> None:
    """並列化率ごと・コア数ごとの値を表にして表示する。

    value が "speedup" なら速度向上率、"efficiency" なら効率を表示する。
    """
    print(f"== {title} ==")
    header = "".join(f"{n:>8}" for n in CORES)
    print(f"{'p':>5}{header}{'上限':>7}" if value == "speedup"
          else f"{'p':>5}{header}")
    for p in FRACTIONS:
        cells = []
        for n in CORES:
            s = speedup(p, n)
            cells.append(f"{s:8.2f}" if value == "speedup"
                         else f"{s / n:8.1%}")
        line = f"{p:>5.2f}" + "".join(cells)
        if value == "speedup":
            line += f"{limit(p):9.1f}"
        print(line)


def cores_needed(p: float, target: float) -> int | None:
    """速度向上率 target を達成するのに必要な最小のコア数を返す。

    上限以上の目標は有限のコア数では達成できないので None を返す。
    """
    if target >= limit(p) - 1e-9:  # 浮動小数点数の誤差を考慮する
        return None
    # target = 1 / ((1 - p) + p / n) を n について解く
    n = p / (1.0 / target - (1.0 - p))
    return math.ceil(n - 1e-9)


def main() -> None:
    """速度向上率と効率の表、必要なコア数を表示する。"""
    print_table("速度向上率 S(n)（列はコア数 n）", "speedup")
    print_table("効率 S(n) / n", "efficiency")
    print("== 10 倍速にするのに必要なコア数 ==")
    for p in FRACTIONS:
        n = cores_needed(p, 10.0)
        print(f"  p = {p:.2f}: {'不可能' if n is None else f'{n} コア'}")


if __name__ == "__main__":
    main()
