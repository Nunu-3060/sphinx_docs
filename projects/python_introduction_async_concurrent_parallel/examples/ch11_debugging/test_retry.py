"""コルーチンを unittest.IsolatedAsyncioTestCase でテストするサンプル。

次のコマンドでテストを実行する。

    python -m unittest test_retry.py
"""

import asyncio
import unittest
from collections.abc import Awaitable, Callable
from typing import TypeVar

T = TypeVar("T")


async def retry(operation: Callable[[], Awaitable[T]], attempts: int, delay: float) -> T:
    """operation が ConnectionError で失敗した場合、delay 秒待って最大 attempts 回まで実行する。"""
    for attempt in range(1, attempts + 1):
        try:
            return await operation()
        except ConnectionError:
            if attempt == attempts:
                raise
            await asyncio.sleep(delay)
    raise ValueError("attempts には 1 以上を指定する")


class FlakyServer:
    """最初の failures 回だけ ConnectionError を送出するテスト用のサーバー。"""

    def __init__(self, failures: int) -> None:
        self.failures = failures
        self.calls = 0

    async def request(self) -> str:
        self.calls += 1
        await asyncio.sleep(0)
        if self.calls <= self.failures:
            raise ConnectionError("接続できない")
        return "OK"


class RetryTest(unittest.IsolatedAsyncioTestCase):
    async def test_succeeds_after_failures(self) -> None:
        server = FlakyServer(failures=2)
        result = await retry(server.request, attempts=3, delay=0.01)
        self.assertEqual(result, "OK")
        self.assertEqual(server.calls, 3)

    async def test_raises_when_attempts_run_out(self) -> None:
        server = FlakyServer(failures=5)
        with self.assertRaises(ConnectionError):
            await retry(server.request, attempts=3, delay=0.01)
        self.assertEqual(server.calls, 3)

    async def test_finishes_within_time_limit(self) -> None:
        server = FlakyServer(failures=1)
        async with asyncio.timeout(1.0):  # テストが終わらなくなることを防ぐ
            await retry(server.request, attempts=2, delay=0.01)


if __name__ == "__main__":
    unittest.main()
