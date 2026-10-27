"""先頭から 1 文字ずつ比較する素朴な比較関数に対するタイミング攻撃のシミュレーション。

実際の文字列比較の時間差はナノ秒単位で、観測には多数の試行が必要になる。ここでは差を観測しやすくするため、
1 文字の比較ごとに一定時間の待ちを入れて誇張している。

実行方法::

    python timing_attack.py
"""

import hmac
import secrets
import statistics
import time

CHARSET = "0123456789abcdef"
SECRET_LENGTH = 6
DELAY_NS = 100_000  # 1 文字の比較にかかる時間（誇張した値）
TRIALS = 5


def busy_wait(ns: int) -> None:
    """指定したナノ秒だけ処理を止めずに待つ。"""
    end = time.perf_counter_ns() + ns
    while time.perf_counter_ns() < end:
        pass


def naive_equal(a: str, b: str) -> bool:
    """先頭から比較し、一致しない文字が見つかった時点で False を返す（脆弱）。"""
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        busy_wait(DELAY_NS)
        if x != y:
            return False
    return True


def measure(secret: str, guess: str) -> int:
    """naive_equal() の処理時間の中央値 [ns] を測る。"""
    samples = []
    for _ in range(TRIALS):
        start = time.perf_counter_ns()
        naive_equal(secret, guess)
        samples.append(time.perf_counter_ns() - start)
    return int(statistics.median(samples))


def attack(secret: str) -> str:
    """1 文字ずつ、処理時間が最も長くなる文字を選んで秘密の文字列を推定する。"""
    known = ""
    for position in range(SECRET_LENGTH - 1):
        padding = "0" * (SECRET_LENGTH - position - 1)
        timings = {ch: measure(secret, known + ch + padding) for ch in CHARSET}
        best = max(timings, key=lambda ch: timings[ch])
        known += best
        print(f"  {position + 1} 文字目: {best!r}（{timings[best] / 1000:.0f} μs）")
    # 最後の 1 文字は処理時間に差が出ないので、比較結果（ログインの成否など）を見て決める
    for ch in CHARSET:
        if naive_equal(secret, known + ch):
            known += ch
            print(f"  {SECRET_LENGTH} 文字目: {ch!r}（比較結果が True になった）")
            break
    return known


def main() -> None:
    secret = "".join(secrets.choice(CHARSET) for _ in range(SECRET_LENGTH))
    print(f"秘密の文字列: {secret}")
    guessed = attack(secret)
    print(f"推定結果    : {guessed}（一致: {guessed == secret}）")
    # 対策: hmac.compare_digest() は内容によらず比較時間が変わらないように実装されている
    print(f"compare_digest による比較: {hmac.compare_digest(secret.encode(), guessed.encode())}")


if __name__ == "__main__":
    main()
