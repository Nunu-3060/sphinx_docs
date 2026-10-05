"""擬似乱数の再現性と予測可能性、secrets モジュールの使い方を示すサンプル。

random モジュールはメルセンヌ・ツイスタ（MT19937）であり、同じシードから
は同じ列が得られる。さらに、出力を 624 個観測すると内部状態を復元でき、
以後の出力をすべて予測できる。そのため、トークンやパスワードの生成には
暗号学的に安全な乱数を返す secrets モジュールを使う。

実行方法: python ch13_random.py
関連する章: 第 13 章「情報セキュリティと暗号」
"""

import random
import secrets

MASK32 = 0xFFFFFFFF


def undo_right(y: int, shift: int) -> int:
    """y ^= y >> shift の逆変換。"""
    x = y
    for _ in range(32 // shift + 1):
        x = y ^ (x >> shift)
    return x & MASK32


def undo_left(y: int, shift: int, mask: int) -> int:
    """y ^= (y << shift) & mask の逆変換。"""
    x = y
    for _ in range(32 // shift + 1):
        x = y ^ ((x << shift) & mask)
    return x & MASK32


def untemper(y: int) -> int:
    """MT19937 の出力変換（tempering）を逆にたどり、内部状態の値に戻す。"""
    y = undo_right(y, 18)
    y = undo_left(y, 15, 0xEFC60000)
    y = undo_left(y, 7, 0x9D2C5680)
    return undo_right(y, 11)


def clone(outputs: list[int]) -> random.Random:
    """連続する 624 個の 32 ビット出力から、同じ状態の生成器を作る。"""
    state = tuple(untemper(y) for y in outputs) + (624,)
    rng = random.Random()
    rng.setstate((3, state, None))
    return rng


def main() -> None:
    """再現性、状態の復元による予測、secrets の使用例を順に示す。"""
    print("[シードによる再現性]")
    for _ in range(2):
        rng = random.Random(2024)
        print([rng.randrange(100) for _ in range(5)])

    print("[出力からの予測]")
    victim = random.Random()  # シードは OS の乱数源から設定される
    observed = [victim.getrandbits(32) for _ in range(624)]
    attacker = clone(observed)
    predicted = [attacker.getrandbits(32) for _ in range(5)]
    actual = [victim.getrandbits(32) for _ in range(5)]
    print("予測と実際が一致:", predicted == actual)
    print("予測したトークン:", attacker.getrandbits(128).to_bytes(16).hex())
    print("実際のトークン  :", victim.getrandbits(128).to_bytes(16).hex())

    print("[secrets モジュール]")
    print("token_hex(16)    :", secrets.token_hex(16))
    print("token_urlsafe(16):", secrets.token_urlsafe(16))
    print("randbelow(100)   :", secrets.randbelow(100))


if __name__ == "__main__":
    main()
