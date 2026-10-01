"""マーカーでテストの扱いを変える."""

import sys
import time

import pytest


@pytest.mark.skip(reason="仕様が確定するまで実行しない")
def test_not_ready() -> None:
    assert False


@pytest.mark.skipif(sys.platform != "win32", reason="Windows 専用の機能")
def test_windows_only() -> None:
    assert sys.platform == "win32"


@pytest.mark.xfail(reason="既知の欠陥: 四捨五入になっていない", strict=True)
def test_known_bug() -> None:
    # round は偶数への丸めを行うため、四捨五入を期待すると失敗する
    assert round(2.5) == 3


@pytest.mark.slow
def test_slow_operation() -> None:
    time.sleep(0.5)
    assert sum(range(10)) == 45
