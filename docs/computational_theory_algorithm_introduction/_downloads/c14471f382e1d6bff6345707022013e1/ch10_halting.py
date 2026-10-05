"""第 10 章: 停止問題が決定不能であることを Python で考える。

前半: 仮に停止判定関数 halts があったとすると矛盾が生じることを示す。
後半: ステップ数に上限を設けた「判定もどき」は作れるが、停止しない場合に
「停止しない」と答えることはできず、「分からない」としか言えない。

実行例::

    python ch10_halting.py
"""

from __future__ import annotations

from collections.abc import Callable, Iterator


def halts(program: Callable[..., object], argument: object) -> bool:
    """program(argument) が停止するなら True、しないなら False を返す。

    このような関数が存在すると仮定する。下の paradox を使うと矛盾が導ける
    ため、実際には実装できない。
    """
    raise NotImplementedError("停止問題を解くプログラムは存在しない")


def paradox(program: Callable[..., object]) -> None:
    """halts の答えの逆を行うプログラム。

    paradox(paradox) を考える。
    * halts(paradox, paradox) が True なら、無限ループに入るので停止しない。
    * halts(paradox, paradox) が False なら、すぐに戻るので停止する。
    どちらの場合も halts の答えが誤りとなり、halts の存在と矛盾する。
    """
    if halts(program, program):
        while True:
            pass


# 1 ステップずつ実行できるように、プログラムをジェネレータとして表す。
Program = Callable[[int], Iterator[None]]


def collatz(n: int) -> Iterator[None]:
    """コラッツの操作を 1 になるまで繰り返す。全ての n で停止するかは未解決。"""
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        yield


def count_forever(n: int) -> Iterator[None]:
    """決して停止しない。"""
    while True:
        n += 1
        yield


def run_with_budget(program: Program, argument: int, budget: int) -> str:
    """budget ステップまで実行し、停止すれば "停止" を返す。"""
    steps = program(argument)
    for _ in range(budget):
        try:
            next(steps)
        except StopIteration:
            return "停止"
    return "分からない (上限までに停止しなかった)"


def main() -> None:
    for name, program, argument in [("collatz", collatz, 27),
                                    ("count_forever", count_forever, 0)]:
        result = run_with_budget(program, argument, 1000)
        print(f"{name}({argument}): {result}")
    try:
        paradox(paradox)
    except NotImplementedError as error:
        print("paradox(paradox):", error)


if __name__ == "__main__":
    main()
