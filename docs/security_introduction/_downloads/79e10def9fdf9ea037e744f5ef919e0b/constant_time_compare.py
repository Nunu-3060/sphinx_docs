"""タイミング攻撃と定数時間比較のサンプル.

先頭から 1 文字ずつ比較し、異なる文字が見つかった時点で終了する比較では、
一致している文字数によって処理時間が変わります。攻撃者はこの差を測定して、
秘密の値を 1 文字ずつ推測できます。

実際の時間差は小さく測定の誤差に埋もれやすいため、このサンプルでは
比較した文字数を数えることで処理量の違いを示します。

実行方法:
    python constant_time_compare.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import hmac


def naive_compare(secret: str, guess: str) -> tuple[bool, int]:
    """早期終了する比較。結果と比較した文字数を返す（悪い例）."""
    steps = 0
    if len(secret) != len(guess):
        return False, steps
    for a, b in zip(secret, guess):
        steps += 1
        if a != b:
            return False, steps
    return True, steps


def main() -> None:
    secret = "s3cr3t-t0ken"
    guesses = ["xxxxxxxxxxxx", "sxxxxxxxxxxx", "s3cxxxxxxxxx", "s3cr3t-t0kex"]

    print("[早期終了する比較（悪い例）]")
    for guess in guesses:
        matched, steps = naive_compare(secret, guess)
        print(f"  {guess}: 結果={matched!s:5s} 比較した文字数={steps:2d}")
    print("  -> 先頭の一致が長いほど処理量が増え、推測の手がかりになります。")

    print("[hmac.compare_digest()（良い例）]")
    for guess in guesses:
        print(f"  {guess}: 結果={hmac.compare_digest(secret, guess)}")
    print("  -> 一致している位置に関係なく、処理時間がほぼ一定になります。")


if __name__ == "__main__":
    main()
