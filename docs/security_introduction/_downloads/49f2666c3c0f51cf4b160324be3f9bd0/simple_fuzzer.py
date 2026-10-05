"""ファジングの考え方を確認する簡単なファザーのサンプル.

ランダムに生成した入力を関数に大量に与え、想定外の例外が発生する入力を
探します。開発者が思いつかない入力によるバグを見つけるのに役立ちます。

実行方法:
    python simple_fuzzer.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import random
from collections.abc import Callable

ALPHABET = "ab=&%2 "  # 対象の関数が特別に扱う文字を多めに含める
ITERATIONS = 10000


def parse_query_buggy(query: str) -> dict[str, str]:
    """「key=value&key=value」形式を解析する（バグあり）."""
    result: dict[str, str] = {}
    for pair in query.split("&"):
        key, value = pair.split("=")  # 「=」がない、または複数あると失敗する
        result[key] = value
    return result


def parse_query_fixed(query: str) -> dict[str, str]:
    """「key=value&key=value」形式を解析する（修正版）."""
    result: dict[str, str] = {}
    for pair in query.split("&"):
        if not pair:
            continue
        key, _, value = pair.partition("=")
        result[key] = value
    return result


def fuzz(target: Callable[[str], object], seed: int) -> str | None:
    """target に例外を発生させる入力を探し、見つかればその入力を返す."""
    rng = random.Random(seed)  # シードを固定し、結果を再現できるようにする
    for _ in range(ITERATIONS):
        length = rng.randint(0, 12)
        text = "".join(rng.choice(ALPHABET) for _ in range(length))
        try:
            target(text)
        except Exception as error:  # 想定外の例外をすべて捕捉する
            print(f"  例外を発生させる入力: {text!r}")
            print(f"  例外: {type(error).__name__}: {error}")
            return text
    print(f"  {ITERATIONS} 回の試行で例外は発生しませんでした。")
    return None


def main() -> None:
    print("[バグのある関数]")
    fuzz(parse_query_buggy, seed=1)
    print("[修正版の関数]")
    fuzz(parse_query_fixed, seed=1)


if __name__ == "__main__":
    main()
