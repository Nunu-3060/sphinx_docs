"""random モジュールと secrets モジュールの違い。

random モジュールの擬似乱数生成器（メルセンヌ・ツイスタ）は、シードが同じなら同じ列を出力し、
出力を十分な量観測すると内部状態を復元できる。鍵やトークンの生成には secrets モジュールを使う。

実行方法::

    python secure_random.py
"""

import random
import secrets


def main() -> None:
    # シードが同じなら random の出力は毎回同じになる
    gen1 = random.Random(2026)
    gen2 = random.Random(2026)
    print("random（シード 2026）1 回目:", [gen1.randrange(100) for _ in range(5)])
    print("random（シード 2026）2 回目:", [gen2.randrange(100) for _ in range(5)])

    # secrets は OS の暗号論的擬似乱数生成器を使う
    print()
    print(f"secrets.token_bytes(16) : {secrets.token_bytes(16).hex()}")
    print(f"secrets.token_hex(16)   : {secrets.token_hex(16)}")
    print(f"secrets.token_urlsafe(16): {secrets.token_urlsafe(16)}")
    print(f"secrets.randbelow(100)  : {secrets.randbelow(100)}")
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # 紛らわしい文字を除いた文字集合
    password = "".join(secrets.choice(alphabet) for _ in range(12))
    print(f"ランダムなパスワード    : {password}")


if __name__ == "__main__":
    main()
