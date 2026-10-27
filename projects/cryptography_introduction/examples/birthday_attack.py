"""出力を短く切り詰めた SHA-256 に対する誕生日攻撃（衝突探索）。

出力を n ビットに切り詰めると、およそ 2^(n/2) 回の計算で衝突が見つかることを確かめる。

実行方法::

    python birthday_attack.py
"""

import hashlib
import math
import secrets


def truncated_hash(data: bytes, bits: int) -> int:
    """SHA-256 の出力の上位 bits ビットを整数として返す。"""
    digest = int.from_bytes(hashlib.sha256(data).digest(), "big")
    return digest >> (256 - bits)


def find_collision(bits: int) -> tuple[bytes, bytes, int]:
    """ハッシュ値が一致する異なる 2 つの入力と、それまでに計算したハッシュ値の個数を返す。"""
    seen: dict[int, bytes] = {}
    trials = 0
    while True:
        message = secrets.token_bytes(16)
        trials += 1
        h = truncated_hash(message, bits)
        if h in seen and seen[h] != message:
            return seen[h], message, trials
        seen[h] = message


def main() -> None:
    for bits in [16, 24, 32]:
        m1, m2, trials = find_collision(bits)
        expected = math.sqrt(math.pi / 2 * 2**bits)  # 衝突までの試行回数の期待値
        print(f"{bits} ビット: {trials:7d} 回で衝突（期待値 約 {expected:7.0f} 回）")
        print(f"  {m1.hex()} と {m2.hex()} -> {truncated_hash(m1, bits):x}")


if __name__ == "__main__":
    main()
