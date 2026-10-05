"""認証ログから不審なアクセスを検知するサンプル.

一定時間内にログイン失敗を繰り返している接続元と、失敗が続いた後に
ログインに成功した接続元（不正ログインの可能性がある）を検出します。

実行方法:
    python auth_log_monitor.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import re
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta

SAMPLE_LOG = """\
2026-10-05T09:00:01 LOGIN_SUCCESS user=alice ip=192.0.2.10
2026-10-05T09:01:00 LOGIN_FAILURE user=admin ip=203.0.113.7
2026-10-05T09:01:02 LOGIN_FAILURE user=admin ip=203.0.113.7
2026-10-05T09:01:04 LOGIN_FAILURE user=root ip=203.0.113.7
2026-10-05T09:01:06 LOGIN_FAILURE user=bob ip=203.0.113.7
2026-10-05T09:01:08 LOGIN_FAILURE user=bob ip=203.0.113.7
2026-10-05T09:01:10 LOGIN_SUCCESS user=bob ip=203.0.113.7
2026-10-05T09:05:00 LOGIN_FAILURE user=carol ip=198.51.100.3
2026-10-05T09:30:00 LOGIN_SUCCESS user=carol ip=198.51.100.3
"""

LINE = re.compile(
    r"(?P<time>\S+) (?P<event>LOGIN_SUCCESS|LOGIN_FAILURE) "
    r"user=(?P<user>\S+) ip=(?P<ip>\S+)"
)
WINDOW_MINUTES = 5  # 失敗回数を数える時間幅（分）
WINDOW = timedelta(minutes=WINDOW_MINUTES)
THRESHOLD = 5  # この回数以上の失敗で警告する


@dataclass(frozen=True)
class Event:
    """ログの 1 行を表す."""

    time: datetime
    success: bool
    user: str
    ip: str


def parse(log: str) -> list[Event]:
    """ログを解析する。形式に合わない行は無視する."""
    events = []
    for line in log.splitlines():
        match = LINE.fullmatch(line.strip())
        if match is None:
            continue
        events.append(Event(
            time=datetime.fromisoformat(match["time"]),
            success=match["event"] == "LOGIN_SUCCESS",
            user=match["user"],
            ip=match["ip"],
        ))
    return events


def detect(events: list[Event]) -> list[str]:
    """不審なアクセスを検知し、警告メッセージの一覧を返す."""
    alerts: list[str] = []
    failures: dict[str, deque[datetime]] = defaultdict(deque)
    for event in events:
        recent = failures[event.ip]
        # 時間幅より古い失敗の記録を捨てる
        while recent and event.time - recent[0] > WINDOW:
            recent.popleft()
        if not event.success:
            recent.append(event.time)
            if len(recent) == THRESHOLD:
                alerts.append(f"{event.time} {event.ip}: "
                              f"{WINDOW_MINUTES} 分以内に {THRESHOLD} 回の失敗")
        elif len(recent) >= THRESHOLD:
            alerts.append(f"{event.time} {event.ip}: 失敗が続いた後に "
                          f"{event.user} としてログイン成功（要調査）")
            recent.clear()
    return alerts


def main() -> None:
    for alert in detect(parse(SAMPLE_LOG)):
        print(f"[警告] {alert}")


if __name__ == "__main__":
    main()
