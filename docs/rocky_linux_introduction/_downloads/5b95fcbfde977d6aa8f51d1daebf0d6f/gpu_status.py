#!/usr/bin/env python3
"""NVIDIA GPU の状態を一覧表示するスクリプト.

nvidia-smi の問い合わせ機能 (--query-gpu) で GPU ごとの情報を CSV 形式で
取得し、温度、使用率、メモリの使用量を見やすく表示します。
温度またはメモリの使用率がしきい値を超えた GPU があれば警告を表示し、
終了コード 1 で終了するため、systemd タイマーなどから定期実行して
簡易的な監視に利用できます。

使い方:
    python3 gpu_status.py
    python3 gpu_status.py --temp-limit 80 --memory-limit 90

前提:
    NVIDIA のドライバーが導入され、nvidia-smi コマンドが使えること。
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from dataclasses import dataclass

# nvidia-smi に問い合わせる項目 (順番は GpuStatus.from_row と対応させる)
QUERY_FIELDS = [
    "index",
    "name",
    "driver_version",
    "temperature.gpu",
    "utilization.gpu",
    "memory.used",
    "memory.total",
]


@dataclass
class GpuStatus:
    """1 枚の GPU の状態."""

    index: int
    name: str
    driver_version: str
    temperature_c: int
    utilization_percent: int
    memory_used_mib: int
    memory_total_mib: int

    @property
    def memory_percent(self) -> float:
        """メモリの使用率 (%)."""
        if self.memory_total_mib == 0:
            return 0.0
        return round(self.memory_used_mib / self.memory_total_mib * 100, 1)

    @classmethod
    def from_row(cls, row: list[str]) -> GpuStatus:
        """nvidia-smi の CSV の 1 行から GpuStatus を作成する."""
        values = [value.strip() for value in row]
        return cls(
            index=int(values[0]),
            name=values[1],
            driver_version=values[2],
            temperature_c=to_int(values[3]),
            utilization_percent=to_int(values[4]),
            memory_used_mib=to_int(values[5]),
            memory_total_mib=to_int(values[6]),
        )


def to_int(value: str) -> int:
    """数値に変換する. 取得できない項目 ("[N/A]" など) は 0 とする."""
    try:
        return int(float(value))
    except ValueError:
        return 0


def query_gpus() -> list[GpuStatus]:
    """nvidia-smi を実行して、すべての GPU の状態を取得する."""
    command = [
        "nvidia-smi",
        f"--query-gpu={','.join(QUERY_FIELDS)}",
        "--format=csv,noheader,nounits",
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        sys.exit(
            "nvidia-smi が見つかりません。NVIDIA のドライバーを導入してください。"
        )
    except subprocess.CalledProcessError as error:
        # ドライバーが読み込まれていない場合などに発生する
        sys.exit(f"nvidia-smi の実行に失敗しました: {error.stdout.strip()}")
    return parse_csv(completed.stdout)


def parse_csv(text: str) -> list[GpuStatus]:
    """nvidia-smi の CSV 出力を解析する."""
    rows = csv.reader(line for line in text.splitlines() if line.strip())
    return [GpuStatus.from_row(row) for row in rows]


def print_report(gpus: list[GpuStatus]) -> None:
    """GPU の状態を表形式で表示する."""
    print(f"{'GPU':<4}{'NAME':<24}{'DRIVER':<10}{'TEMP':>6}"
          f"{'UTIL':>6}{'MEMORY (MiB)':>20}")
    for gpu in gpus:
        memory = (f"{gpu.memory_used_mib}/{gpu.memory_total_mib}"
                  f" ({gpu.memory_percent}%)")
        print(f"{gpu.index:<4}{gpu.name[:23]:<24}{gpu.driver_version:<10}"
              f"{gpu.temperature_c:>4} C{gpu.utilization_percent:>5}%"
              f"{memory:>20}")


def find_problems(
    gpus: list[GpuStatus], temp_limit: int, memory_limit: float
) -> list[str]:
    """しきい値を超えた GPU についての警告メッセージを作成する."""
    problems: list[str] = []
    for gpu in gpus:
        if gpu.temperature_c >= temp_limit:
            problems.append(
                f"GPU {gpu.index}: 温度が {gpu.temperature_c} C です"
                f" (しきい値 {temp_limit} C)"
            )
        if gpu.memory_percent >= memory_limit:
            problems.append(
                f"GPU {gpu.index}: メモリの使用率が {gpu.memory_percent}% です"
                f" (しきい値 {memory_limit}%)"
            )
    return problems


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(
        description="NVIDIA GPU の状態を表示します。"
    )
    parser.add_argument(
        "--temp-limit",
        type=int,
        default=85,
        help="警告する GPU の温度 (C、既定値: 85)",
    )
    parser.add_argument(
        "--memory-limit",
        type=float,
        default=95.0,
        help="警告するメモリの使用率 (%%、既定値: 95)",
    )
    return parser.parse_args()


def main() -> int:
    """エントリーポイント. 問題がなければ 0、あれば 1 を返す."""
    args = parse_args()
    gpus = query_gpus()
    if not gpus:
        print("GPU が見つかりません。")
        return 1
    print_report(gpus)
    problems = find_problems(gpus, args.temp_limit, args.memory_limit)
    for problem in problems:
        print(f"WARNING: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
