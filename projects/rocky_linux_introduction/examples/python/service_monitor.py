#!/usr/bin/env python3
"""systemd サービスの稼働状態を確認するスクリプト.

指定したサービスが active (稼働中) かどうかを systemctl で確認し、
結果を一覧表示します。1 つでも停止しているサービスがあれば
終了コード 1 で終了するため、systemd タイマーや cron から定期実行し、
監視の仕組みと組み合わせて利用できます。

使い方:
    python3 service_monitor.py sshd chronyd nginx
    python3 service_monitor.py --restart nginx   # 停止していたら再起動を試みる

注意:
    --restart を指定する場合は root 権限 (sudo) が必要です。
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import sys
from dataclasses import dataclass

logger = logging.getLogger("service_monitor")


@dataclass
class ServiceStatus:
    """サービスの確認結果."""

    name: str
    state: str

    @property
    def is_active(self) -> bool:
        """サービスが稼働中かどうか."""
        return self.state == "active"


def get_state(service: str) -> str:
    """systemctl is-active でサービスの状態を取得する.

    戻り値は active, inactive, failed, activating などの文字列です。
    サービスが存在しない場合は inactive が返ります。
    """
    try:
        completed = subprocess.run(
            ["systemctl", "is-active", service],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        sys.exit("systemctl が見つかりません。systemd 環境で実行してください。")
    # is-active は停止中のとき終了コードが 0 以外になるため、
    # 終了コードではなく標準出力の文字列で判定する
    return completed.stdout.strip() or "unknown"


def restart(service: str) -> bool:
    """サービスを再起動し、成功したかどうかを返す."""
    completed = subprocess.run(
        ["systemctl", "restart", service],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        logger.error(
            "%s の再起動に失敗しました: %s", service, completed.stderr.strip()
        )
        return False
    logger.info("%s を再起動しました", service)
    return True


def check_services(
    services: list[str], do_restart: bool
) -> list[ServiceStatus]:
    """サービスの状態を確認し、必要に応じて再起動する."""
    results: list[ServiceStatus] = []
    for service in services:
        status = ServiceStatus(name=service, state=get_state(service))
        if not status.is_active and do_restart and restart(service):
            status = ServiceStatus(name=service, state=get_state(service))
        results.append(status)
    return results


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する."""
    parser = argparse.ArgumentParser(
        description="systemd サービスの稼働状態を確認します。"
    )
    parser.add_argument(
        "services",
        nargs="+",
        metavar="SERVICE",
        help="確認するサービス名 (例: sshd nginx)",
    )
    parser.add_argument(
        "--restart",
        action="store_true",
        help="停止しているサービスの再起動を試みる",
    )
    return parser.parse_args()


def main() -> int:
    """エントリーポイント. 全サービスが稼働中なら 0、それ以外は 1 を返す."""
    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s: %(message)s"
    )
    args = parse_args()
    results = check_services(args.services, args.restart)

    for status in results:
        mark = "OK  " if status.is_active else "NG  "
        print(f"{mark}{status.name:<24}{status.state}")

    stopped = [status.name for status in results if not status.is_active]
    if stopped:
        logger.warning("停止しているサービス: %s", ", ".join(stopped))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
