"""サーキットブレーカーの状態遷移を示すサンプル。

Closed（通常）、Open（遮断）、Half-Open（試行）の 3 つの状態を持つ
サーキットブレーカーを実装し、一定の期間だけ障害を起こすサービスを
2 秒ごとに呼び出したときに、状態がどう変わるかを表示します。

* Closed：呼び出しをそのまま通す。連続 3 回失敗したら Open にする
* Open：呼び出しをサービスに送らず、すぐにエラーを返す（即時失敗）。
  10 秒たったら Half-Open にする
* Half-Open：試しに呼び出しを通す。成功したら Closed に戻し、
  失敗したら再び Open にする

時刻は模擬時計の値（秒）で、実際の時間は経過しません。

実行方法:
    python circuit_breaker.py
"""

from enum import Enum


class Clock:
    """模擬時計。"""

    def __init__(self) -> None:
        self.now = 0.0

    def advance(self, seconds: float) -> None:
        self.now += seconds


class ServiceError(Exception):
    """呼び出し先のサービスのエラー（タイムアウトなど）。"""


class CircuitOpenError(Exception):
    """サーキットブレーカーが Open のため、呼び出さなかったことを表す。"""


class FlakyService:
    """指定した期間だけ障害を起こす、呼び出し先のサービス。"""

    def __init__(self, clock: Clock, down_from: float,
                 down_until: float) -> None:
        self.clock = clock
        self.down_from = down_from
        self.down_until = down_until
        self.received = 0  # 実際に受け付けたリクエストの数

    def call(self) -> str:
        self.received += 1
        if self.down_from <= self.clock.now < self.down_until:
            raise ServiceError("タイムアウト")
        return "OK"


class State(Enum):
    CLOSED = "Closed"
    OPEN = "Open"
    HALF_OPEN = "Half-Open"


class CircuitBreaker:
    """サーキットブレーカー。"""

    def __init__(self, clock: Clock, failure_threshold: int = 3,
                 open_timeout: float = 10.0) -> None:
        self.clock = clock
        self.failure_threshold = failure_threshold
        self.open_timeout = open_timeout
        self.state = State.CLOSED
        self.failures = 0  # 連続した失敗の回数
        self.opened_at = 0.0

    def _log(self, message: str) -> None:
        print(f"  {self.clock.now:4.0f} 秒  [{self.state.value:<9}] "
              f"{message}")

    def _change(self, new_state: State, reason: str) -> None:
        self._log(f"*** {self.state.value} → {new_state.value}"
                  f"（{reason}）")
        self.state = new_state

    def call(self, service: FlakyService) -> str:
        # Open のまま一定時間がたったら、試しに通す Half-Open へ
        if self.state == State.OPEN:
            if self.clock.now - self.opened_at >= self.open_timeout:
                self._change(State.HALF_OPEN,
                             f"{self.open_timeout:.0f} 秒経過")
            else:
                self._log("即時失敗（サービスは呼ばない）")
                raise CircuitOpenError("即時失敗")

        try:
            result = service.call()
        except ServiceError as e:
            self._log(f"呼び出し失敗（{e}）")
            self._on_failure()
            raise
        self._log("呼び出し成功")
        self._on_success()
        return result

    def _on_success(self) -> None:
        if self.state == State.HALF_OPEN:
            self._change(State.CLOSED, "試行が成功")
        self.failures = 0

    def _on_failure(self) -> None:
        self.failures += 1
        if self.state == State.HALF_OPEN:
            self._open("試行が失敗")
        elif self.failures >= self.failure_threshold:
            self._open(f"{self.failures} 回連続で失敗")

    def _open(self, reason: str) -> None:
        self._change(State.OPEN, reason)
        self.opened_at = self.clock.now


def main() -> None:
    clock = Clock()
    # 10 秒から 35 秒まで障害が起きているサービス
    service = FlakyService(clock, down_from=10.0, down_until=35.0)
    breaker = CircuitBreaker(clock)
    calls = 26
    print("サービスの障害期間: 10 秒〜35 秒、2 秒ごとに呼び出す")
    print("   時刻    [状態]     出来事")

    for _ in range(calls):
        try:
            breaker.call(service)
        except (ServiceError, CircuitOpenError):
            pass  # 実際のアプリケーションでは代替の処理をする
        clock.advance(2.0)

    print()
    print(f"呼び出し {calls} 回のうち、サービスに届いたのは "
          f"{service.received} 回")


if __name__ == "__main__":
    main()
