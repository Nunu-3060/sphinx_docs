#!/usr/bin/env python3
"""サーバーの基本情報を収集して表示するスクリプト.

OS のバージョン、カーネル、CPU、メモリ、ディスク使用量を 1 画面にまとめて
表示します。標準ライブラリのみを使用しているため、Rocky Linux 10 に
標準で導入されている python3 でそのまま実行できます。

使い方:
    python3 system_info.py           # 人間向けの表形式で表示
    python3 system_info.py --json    # JSON 形式で表示 (他のツールとの連携用)
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
from dataclasses import asdict, dataclass, field
from pathlib import Path

OS_RELEASE_PATH = Path("/etc/os-release")
MEMINFO_PATH = Path("/proc/meminfo")
UPTIME_PATH = Path("/proc/uptime")

# 使用量を調べるマウントポイント
DEFAULT_MOUNT_POINTS = ["/", "/boot", "/home", "/var"]


@dataclass
class DiskUsage:
    """1 つのマウントポイントのディスク使用量."""

    mount_point: str
    total_gib: float
    used_gib: float
    free_gib: float
    used_percent: float


@dataclass
class SystemInfo:
    """収集したサーバー情報."""

    hostname: str
    os_name: str
    kernel: str
    architecture: str
    cpu_count: int
    memory_total_gib: float
    memory_available_gib: float
    uptime_hours: float
    disks: list[DiskUsage] = field(default_factory=list)


def bytes_to_gib(value: int) -> float:
    """バイト数を GiB 単位に変換し、小数点以下 1 桁に丸める."""
    return round(value / 1024**3, 1)


def read_os_name(path: Path = OS_RELEASE_PATH) -> str:
    """/etc/os-release から PRETTY_NAME を読み取る."""
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("PRETTY_NAME="):
                return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    return "unknown"


def read_meminfo(path: Path = MEMINFO_PATH) -> dict[str, int]:
    """/proc/meminfo を読み取り、項目名と値 (バイト) の辞書を返す."""
    result: dict[str, int] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return result
    for line in text.splitlines():
        # 例: "MemTotal:        3836604 kB"
        name, _, rest = line.partition(":")
        parts = rest.split()
        if parts and parts[0].isdigit():
            result[name] = int(parts[0]) * 1024
    return result


def read_uptime_hours(path: Path = UPTIME_PATH) -> float:
    """/proc/uptime から稼働時間 (時間) を読み取る."""
    try:
        seconds = float(path.read_text(encoding="utf-8").split()[0])
    except (OSError, IndexError, ValueError):
        return 0.0
    return round(seconds / 3600, 1)


def collect_disks(mount_points: list[str]) -> list[DiskUsage]:
    """指定したマウントポイントのディスク使用量を収集する.

    存在しないマウントポイントは読み飛ばします。同じファイルシステム上の
    ディレクトリ (例: /home が / と同じ) も、そのまま表示します。
    """
    disks: list[DiskUsage] = []
    for mount_point in mount_points:
        if not os.path.isdir(mount_point):
            continue
        usage = shutil.disk_usage(mount_point)
        disks.append(
            DiskUsage(
                mount_point=mount_point,
                total_gib=bytes_to_gib(usage.total),
                used_gib=bytes_to_gib(usage.used),
                free_gib=bytes_to_gib(usage.free),
                used_percent=round(usage.used / usage.total * 100, 1),
            )
        )
    return disks


def collect(mount_points: list[str]) -> SystemInfo:
    """サーバー情報を収集する."""
    meminfo = read_meminfo()
    uname = platform.uname()
    return SystemInfo(
        hostname=socket.gethostname(),
        os_name=read_os_name(),
        kernel=uname.release,
        architecture=uname.machine,
        cpu_count=os.cpu_count() or 0,
        memory_total_gib=bytes_to_gib(meminfo.get("MemTotal", 0)),
        memory_available_gib=bytes_to_gib(meminfo.get("MemAvailable", 0)),
        uptime_hours=read_uptime_hours(),
        disks=collect_disks(mount_points),
    )


def format_text(info: SystemInfo) -> str:
    """人間向けの表形式の文字列を作成する."""
    lines = [
        f"ホスト名      : {info.hostname}",
        f"OS            : {info.os_name}",
        f"カーネル      : {info.kernel} ({info.architecture})",
        f"CPU 数        : {info.cpu_count}",
        f"メモリ        : {info.memory_available_gib} GiB 利用可能"
        f" / {info.memory_total_gib} GiB",
        f"稼働時間      : {info.uptime_hours} 時間",
        "ディスク      :",
    ]
    for disk in info.disks:
        lines.append(
            f"  {disk.mount_point:<10} {disk.used_gib:>7} GiB 使用"
            f" / {disk.total_gib:>7} GiB ({disk.used_percent}%)"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(description="サーバーの基本情報を表示します。")
    parser.add_argument(
        "--json",
        action="store_true",
        help="JSON 形式で出力する",
    )
    parser.add_argument(
        "--mount",
        action="append",
        metavar="PATH",
        help="使用量を調べるマウントポイント (複数指定可)",
    )
    return parser.parse_args()


def main() -> None:
    """エントリーポイント."""
    args = parse_args()
    mount_points: list[str] = args.mount or DEFAULT_MOUNT_POINTS
    info = collect(mount_points)
    if args.json:
        print(json.dumps(asdict(info), ensure_ascii=False, indent=2))
    else:
        print(format_text(info))


if __name__ == "__main__":
    main()
