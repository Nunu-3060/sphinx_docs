#!/usr/bin/env python3
"""journalctl のログを集計して、エラーの多い発生元を一覧表示するスクリプト.

journalctl の JSON 出力 (1 行 1 エントリー) を読み込み、
発生元 (SYSLOG_IDENTIFIER) ごとの件数を優先度別に集計します。

使い方:
    # 直近 24 時間の warning 以上のログを集計する (journalctl を内部で実行)
    python3 journal_summary.py --since "24 hours ago"

    # 保存済みの JSON ファイルを集計する
    journalctl -o json --since today > today.json
    python3 journal_summary.py --file today.json

注意:
    他のユーザーやシステムのログを読むには、root 権限か
    systemd-journal グループ (または wheel グループ) への所属が必要です。
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from collections.abc import Iterable, Iterator
from pathlib import Path

# journald の優先度 (数値が小さいほど重大)
PRIORITY_NAMES: dict[int, str] = {
    0: "emerg",
    1: "alert",
    2: "crit",
    3: "err",
    4: "warning",
    5: "notice",
    6: "info",
    7: "debug",
}


def run_journalctl(since: str, max_priority: int) -> Iterator[str]:
    """journalctl を実行し、JSON 形式の出力を 1 行ずつ返す."""
    command = [
        "journalctl",
        "--output=json",
        "--no-pager",
        f"--since={since}",
        f"--priority={max_priority}",
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        sys.exit("journalctl が見つかりません。Linux 上で実行してください。")
    except subprocess.CalledProcessError as error:
        sys.exit(f"journalctl の実行に失敗しました: {error.stderr.strip()}")
    yield from completed.stdout.splitlines()


def read_file(path: Path) -> Iterator[str]:
    """保存済みの JSON ファイルを 1 行ずつ返す."""
    with path.open(encoding="utf-8") as file:
        for line in file:
            yield line


def summarize(
    lines: Iterable[str], max_priority: int
) -> Counter[tuple[str, str]]:
    """(発生元, 優先度名) ごとの件数を数える.

    JSON として解釈できない行や、max_priority より重要度の低い行は
    読み飛ばします。
    """
    counter: Counter[tuple[str, str]] = Counter()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        try:
            priority = int(entry.get("PRIORITY", 6))
        except (TypeError, ValueError):
            continue
        if priority > max_priority:
            continue
        source = str(
            entry.get("SYSLOG_IDENTIFIER") or entry.get("_COMM") or "unknown"
        )
        counter[(source, PRIORITY_NAMES.get(priority, str(priority)))] += 1
    return counter


def print_report(counter: Counter[tuple[str, str]], top: int) -> None:
    """集計結果を件数の多い順に表示する."""
    if not counter:
        print("該当するログはありません。")
        return
    print(f"{'COUNT':>8}  {'PRIORITY':<10}  SOURCE")
    for (source, priority), count in counter.most_common(top):
        print(f"{count:>8}  {priority:<10}  {source}")


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(
        description="journald のログを発生元と優先度ごとに集計します。"
    )
    parser.add_argument(
        "--since",
        default="24 hours ago",
        help='集計を開始する日時 (journalctl の --since 形式、既定値: "24 hours ago")',
    )
    parser.add_argument(
        "--priority",
        type=int,
        default=4,
        choices=range(0, 8),
        help="集計対象とする最も低い優先度 (0-7、既定値: 4 = warning)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=20,
        help="表示する件数の上限 (既定値: 20)",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="journalctl -o json の出力を保存したファイル",
    )
    return parser.parse_args()


def main() -> None:
    """エントリーポイント."""
    args = parse_args()
    if args.file is not None:
        lines = read_file(args.file)
    else:
        lines = run_journalctl(args.since, args.priority)
    print_report(summarize(lines, args.priority), args.top)


if __name__ == "__main__":
    main()
