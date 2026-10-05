"""指数バックオフとジッターによるリトライと、冪等キーによる重複排除の例です。

このサンプルは次の 3 つを示します。

1. 一定の確率で失敗する模擬サーバーに対して、指数バックオフと
   ジッター（full jitter）を使ってリトライする様子。
2. 多数のクライアントが同時に失敗したとき、ジッターなしでは
   リトライの時刻がそろってしまい、ジッターありでは分散する様子。
3. 送金のレスポンスが失われてクライアントがリトライしたとき、
   冪等キーなしでは送金が 2 回行われ、冪等キーありでは
   重複が排除される様子。

ネットワークは使わず、1 つのプロセスの中で完結します。
待ち時間は実際に time.sleep で待ちますが、基準値を 10 ms と
小さくしているので、全体は 1 秒もかからずに終わります。
乱数のシードを固定しているので、実行結果は毎回同じです
（表示される実測の経過時間だけは多少変わります）。

実行方法:
    python retry_backoff.py
"""

import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

T = TypeVar("T")

BASE_DELAY = 0.01  # バックオフの基準値（秒）
MAX_DELAY = 0.2  # 待ち時間の上限 t_n の最大値（秒）
MAX_ATTEMPTS = 6  # 最初の試行を含めた最大の試行回数


class TransientError(Exception):
    """一時的な失敗（リトライすれば成功する可能性があるもの）です。"""


class ResponseLost(Exception):
    """サーバーは処理したが、レスポンスが届かなかったことを表します。"""


def backoff_ceiling(retry: int) -> float:
    """retry 番目（0 始まり）のリトライ前の待ち時間の上限 t_n を返します。"""
    return min(MAX_DELAY, BASE_DELAY * 2.0 ** retry)


def full_jitter(retry: int, rng: random.Random) -> float:
    """full jitter：0 から上限 t_n までの一様乱数を待ち時間とします。"""
    return rng.uniform(0.0, backoff_ceiling(retry))


@dataclass
class FlakyServer:
    """一定の確率で一時的なエラーを返す模擬サーバーです。"""

    failure_rate: float
    rng: random.Random
    calls: int = 0

    def handle(self, request: str) -> str:
        self.calls += 1
        if self.rng.random() < self.failure_rate:
            raise TransientError("503 Service Unavailable")
        return f"OK({request})"


def call_with_retry(
    func: Callable[[], T],
    rng: random.Random,
    log: Callable[[str], None],
) -> T:
    """func を呼び出し、一時的な失敗ならバックオフしてリトライします。"""
    for attempt in range(MAX_ATTEMPTS):
        try:
            return func()
        except (TransientError, ResponseLost) as exc:
            if attempt == MAX_ATTEMPTS - 1:
                log(f"  試行 {attempt + 1}: 失敗 ({exc}) -> 諦める")
                raise
            delay = full_jitter(attempt, rng)
            log(
                f"  試行 {attempt + 1}: 失敗 ({exc}) -> "
                f"{delay * 1000:5.1f} ms 待つ"
                f" (上限 {backoff_ceiling(attempt) * 1000:5.1f} ms)"
            )
            time.sleep(delay)
    raise AssertionError("ここには到達しない")


def demo_retry() -> None:
    print("=== 1. 指数バックオフ＋ジッターによるリトライ ===")
    server = FlakyServer(failure_rate=0.6, rng=random.Random(1))
    client_rng = random.Random(2)
    start = time.monotonic()
    for i in range(1, 4):
        request = f"req-{i}"
        print(f"リクエスト {request}:")
        try:
            result = call_with_retry(
                lambda: server.handle(request), client_rng, print
            )
            print(f"  -> 成功: {result}")
        except TransientError:
            print("  -> 最終的に失敗")
    elapsed = time.monotonic() - start
    print(f"サーバーへの呼び出し回数: {server.calls}")
    print(f"経過時間: 約 {elapsed:.2f} 秒")
    print()


def demo_thundering_herd() -> None:
    print("=== 2. 5 台のクライアントが同時に失敗した場合のリトライの時刻 ===")
    rng = random.Random(3)
    clients = 5
    retries = 3
    print("ジッターなし（各クライアントのリトライの時刻, ms）:")
    for c in range(clients):
        t = 0.0
        times = []
        for r in range(retries):
            t += backoff_ceiling(r)
            times.append(f"{t * 1000:6.1f}")
        print(f"  クライアント {c + 1}: " + " ".join(times))
    print("full jitter あり（各クライアントのリトライの時刻, ms）:")
    for c in range(clients):
        t = 0.0
        times = []
        for r in range(retries):
            t += full_jitter(r, rng)
            times.append(f"{t * 1000:6.1f}")
        print(f"  クライアント {c + 1}: " + " ".join(times))
    print()


@dataclass
class PaymentServer:
    """送金を処理する模擬サーバーです。

    最初の lose_responses 回は、処理を終えた後にレスポンスを失わせます。
    冪等キー付きのリクエストは、処理結果をキーと結び付けて記録し、
    同じキーで再びリクエストが来たら、処理をせずに記録した結果を返します。
    """

    balance: int
    lose_responses: int = 0
    processed: int = 0
    results: dict[str, str] = field(default_factory=dict)

    def transfer(self, amount: int, idempotency_key: str | None) -> str:
        if idempotency_key is not None and idempotency_key in self.results:
            # 同じキーのリクエストはすでに処理済み：結果だけを返す
            return self.results[idempotency_key] + " (重複を検出)"
        self.balance -= amount
        self.processed += 1
        result = f"送金完了 {amount} 円"
        if idempotency_key is not None:
            self.results[idempotency_key] = result
        if self.lose_responses > 0:
            self.lose_responses -= 1
            raise ResponseLost("レスポンスがタイムアウト")
        return result


def demo_idempotency() -> None:
    print("=== 3. レスポンスが失われたときのリトライと冪等キー ===")
    rng = random.Random(4)
    for key in [None, "7f3c9a2e-0001"]:
        label = "冪等キーなし" if key is None else f"冪等キー {key}"
        server = PaymentServer(balance=10000, lose_responses=1)
        print(f"[{label}] 残高 10000 円から 3000 円を送金")
        result = call_with_retry(
            lambda: server.transfer(3000, key), rng, print
        )
        print(f"  -> クライアントが受け取った結果: {result}")
        print(
            f"  -> サーバーの処理回数: {server.processed}, "
            f"残高: {server.balance} 円"
        )
    print()


def main() -> None:
    demo_retry()
    demo_thundering_herd()
    demo_idempotency()


if __name__ == "__main__":
    main()
