"""性能の式、アムダールの法則、ルーフラインモデルを数値で確かめるサンプル。

CPU 性能の式で 2 つのプロセッサの実行時間を比較し、アムダールの法則に
よる全体の速度向上率の表と、ルーフラインモデルによる到達可能な性能を
計算して表示します。

実行方法: python performance_calc.py
"""

from dataclasses import dataclass


@dataclass
class Processor:
    """CPU 性能の式に必要なパラメータを持つプロセッサ。"""

    name: str
    instructions: float  # プログラムの実行命令数
    cpi: float  # 1 命令あたりの平均クロックサイクル数
    clock_ghz: float  # クロック周波数（GHz）

    def execution_time(self) -> float:
        """実行時間（秒）= 命令数 × CPI × クロック周期 を返す。"""
        cycle_time = 1.0 / (self.clock_ghz * 1e9)  # クロック周期（秒）
        return self.instructions * self.cpi * cycle_time

    def mips(self) -> float:
        """MIPS 値（1 秒あたりの実行命令数 ÷ 10^6）を返す。"""
        return self.instructions / self.execution_time() / 1e6


def amdahl_speedup(fraction: float, speedup: float) -> float:
    """割合 fraction の部分を speedup 倍にしたときの全体の速度向上率。"""
    return 1.0 / ((1.0 - fraction) + fraction / speedup)


def roofline(peak_gflops: float, bandwidth_gbs: float,
             intensity: float) -> float:
    """演算強度 intensity（FLOP/バイト）での到達可能な性能（GFLOP/s）。"""
    return min(peak_gflops, bandwidth_gbs * intensity)


def compare_processors() -> None:
    """同じプログラムを 2 つのプロセッサで実行した場合を比較する。"""
    print("=== CPU 性能の式による比較 ===")
    # B は命令数が少ない（高機能な命令を持つ）が、CPI が大きく
    # クロック周波数も低いと仮定する
    procs = [
        Processor("A", instructions=10e9, cpi=1.2, clock_ghz=3.0),
        Processor("B", instructions=8e9, cpi=1.8, clock_ghz=2.5),
    ]
    for p in procs:
        print(f"{p.name}: 命令数 {p.instructions:.1e}, CPI {p.cpi}, "
              f"{p.clock_ghz} GHz -> 実行時間 {p.execution_time():.3f} 秒,"
              f" {p.mips():,.0f} MIPS")
    ratio = procs[1].execution_time() / procs[0].execution_time()
    print(f"A は B より {ratio:.2f} 倍速い")
    print()


def amdahl_table() -> None:
    """並列化できる割合とコア数ごとの速度向上率の表を表示する。"""
    print("=== アムダールの法則（並列化できる割合 × コア数）===")
    cores = [2, 4, 8, 16, 64, 1024]
    print("割合  " + "".join(f"{n:>8}" for n in cores) + "   上限")
    for fraction in [0.5, 0.9, 0.95, 0.99]:
        row = "".join(f"{amdahl_speedup(fraction, n):8.2f}" for n in cores)
        limit = 1.0 / (1.0 - fraction)  # コア数を無限大にしたときの上限
        print(f"{fraction:4.2f}  {row}{limit:7.0f}")
    print()


def roofline_table() -> None:
    """演算強度ごとの到達可能な性能を表示する。"""
    peak = 1000.0  # 演算のピーク性能（GFLOP/s）
    bandwidth = 100.0  # メモリ帯域幅（GB/s）
    print("=== ルーフラインモデル ===")
    print(f"ピーク性能 {peak:.0f} GFLOP/s, メモリ帯域幅 {bandwidth:.0f} GB/s,"
          f" リッジポイント {peak / bandwidth:.0f} FLOP/バイト")
    # 例: 単精度の a[i] = b[i] + c[i] は 1 FLOP で 12 バイトを読み書きする
    kernels = [("単精度のベクトル加算", 1 / 12), ("", 1.0), ("", 4.0),
               ("リッジポイント", 10.0), ("", 50.0)]
    for name, intensity in kernels:
        perf = roofline(peak, bandwidth, intensity)
        bound = "メモリ律速" if perf < peak else "演算律速"
        print(f"I={intensity:6.3f} -> {perf:7.1f} GFLOP/s"
              f"（{bound}）{name}")


def main() -> None:
    """各計算を順に実行する。"""
    compare_processors()
    amdahl_table()
    roofline_table()


if __name__ == "__main__":
    main()
