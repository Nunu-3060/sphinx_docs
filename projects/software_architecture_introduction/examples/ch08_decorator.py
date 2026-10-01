"""Decorator パターンと、Python のデコレーターの例.

Decorator パターンは、同じインターフェースを持つオブジェクトで元の
オブジェクトを包み、機能を追加します（ch06_composition.py の
LoggingSender も Decorator パターンです）。

関数に機能を追加したいだけなら、Python のデコレーター構文を使うと
簡潔に書けます。ここでは、処理時間を計測する機能と、結果をキャッシュ
する機能を、元の関数を変更せずに追加します。

実行方法::

    python ch08_decorator.py
"""

import functools
import time
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def timed(func: Callable[P, R]) -> Callable[P, R]:
    """関数の処理時間を表示するデコレーターです."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"[timed] {func.__name__}: {elapsed * 1000:.2f} ms")
    return wrapper


@timed
def slow_square(value: int) -> int:
    """時間のかかる計算の代わりに、少し待ってから 2 乗を返します."""
    time.sleep(0.05)
    return value * value


@functools.cache
def fibonacci(n: int) -> int:
    """n 番目のフィボナッチ数を返します. 標準のデコレーターでキャッシュします."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main() -> None:
    """デコレーターで機能を追加した関数を実行します."""
    print(slow_square(12))
    print(fibonacci(80))


if __name__ == "__main__":
    main()
