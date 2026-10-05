"""セキュリティ用途の乱数生成を確認するサンプル.

random モジュールは再現可能な擬似乱数であり、トークンや鍵の生成には
使えません。セキュリティ用途には secrets モジュールを使います。

実行方法:
    python secure_random.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import random
import secrets
import string


def predictable_token(seed: int, length: int = 16) -> str:
    """random モジュールでトークンを作る（悪い例）."""
    rng = random.Random(seed)
    alphabet = string.ascii_letters + string.digits
    return "".join(rng.choice(alphabet) for _ in range(length))


def secure_password(length: int = 16) -> str:
    """secrets モジュールでランダムなパスワードを作る."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main() -> None:
    # 同じシードからは同じ値が生成される。シードが推測されると
    # 生成されたトークンもすべて推測されてしまう
    print("[random モジュール（悪い例）]")
    print(f"  1 回目: {predictable_token(seed=2026)}")
    print(f"  2 回目: {predictable_token(seed=2026)}")

    print("[secrets モジュール（良い例）]")
    print(f"  URL に使えるトークン: {secrets.token_urlsafe(32)}")
    print(f"  16 進数のトークン   : {secrets.token_hex(16)}")
    print(f"  パスワード          : {secure_password()}")


if __name__ == "__main__":
    main()
