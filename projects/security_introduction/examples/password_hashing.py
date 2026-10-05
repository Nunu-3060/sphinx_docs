"""パスワードの安全な保存方法を確認するサンプル.

高速なハッシュ関数（SHA-256 など）をそのまま使うと、総当たりや
辞書攻撃で短時間に元のパスワードを特定されます。パスワードの保存には
Argon2id のような、意図的に計算を重くした専用の関数を使います。

実行方法:
    python password_hashing.py

必要なライブラリ:
    argon2-cffi（python -m pip install argon2-cffi）
"""

import hashlib
import time
from collections.abc import Callable

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# 引数を省略すると、RFC 9106 が推奨するパラメーターが使われる
password_hasher = PasswordHasher()


def naive_hash(password: str) -> str:
    """ソルトなしの SHA-256（悪い例）."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    """Argon2id でパスワードをハッシュ化する.

    戻り値にはアルゴリズム名、パラメーター、ソルトも含まれるため、
    この文字列だけをデータベースに保存すればよい。
    """
    return password_hasher.hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    """入力されたパスワードが保存済みのハッシュと一致するか確認する."""
    try:
        password_hasher.verify(stored_hash, password)
    except VerifyMismatchError:
        return False
    return True


def measure(label: str, count: int, func: Callable[[], object]) -> None:
    """関数を count 回実行し、1 回あたりの所要時間を表示する."""
    start = time.perf_counter()
    for _ in range(count):
        func()
    elapsed = (time.perf_counter() - start) / count
    print(f"  {label}: 1 回あたり {elapsed * 1000:.3f} ミリ秒")


def main() -> None:
    password = "correct horse battery staple"

    print("[ソルトなしの SHA-256（悪い例）]")
    print(f"  1 回目: {naive_hash(password)}")
    print(f"  2 回目: {naive_hash(password)}")
    print("  -> 同じパスワードは常に同じ値になります。")

    print("[Argon2id]")
    first = hash_password(password)
    second = hash_password(password)
    print(f"  1 回目: {first}")
    print(f"  2 回目: {second}")
    print("  -> ソルトが毎回異なるため、同じパスワードでも値が変わります。")
    print(f"  正しいパスワードの検証: {verify_password(first, password)}")
    print(f"  誤ったパスワードの検証: {verify_password(first, 'password')}")
    print(f"  再ハッシュが必要か: {password_hasher.check_needs_rehash(first)}")

    print("[計算時間の比較]")
    measure("SHA-256 ", 10000, lambda: naive_hash(password))
    measure("Argon2id", 10, lambda: hash_password(password))


if __name__ == "__main__":
    main()
