"""ソルトとストレッチングを用いたパスワードの保存と照合を示すサンプル。

hashlib.pbkdf2_hmac（PBKDF2-HMAC-SHA256）と hashlib.scrypt で
パスワードから導出した値を保存し、ログイン時に照合する。
ソルトは os.urandom で毎回ランダムに生成するため、表示される
ソルトと導出値は実行ごとに異なる。

実行方法: python ch14_password.py
関連する章: 第 14 章「認証とアプリケーションのセキュリティ」
"""

import hashlib
import hmac
import os

PBKDF2_ITERATIONS = 600_000  # 反復回数（ストレッチングの強さ）
SALT_BYTES = 16


def hash_pbkdf2(password: str) -> str:
    """PBKDF2 で導出した値を「方式$反復回数$ソルト$導出値」で返す。"""
    salt = os.urandom(SALT_BYTES)  # ユーザごとに異なるソルト
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${dk.hex()}"


def verify_pbkdf2(password: str, stored: str) -> bool:
    """入力されたパスワードが保存値と一致するかを調べる。"""
    _, iterations, salt_hex, dk_hex = stored.split("$")
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"),
        bytes.fromhex(salt_hex), int(iterations))
    # 比較にかかる時間から情報が漏れないよう定数時間で比較する
    return hmac.compare_digest(dk, bytes.fromhex(dk_hex))


def hash_scrypt(password: str, salt: bytes) -> bytes:
    """scrypt で導出した 32 バイトの値を返す。"""
    # n: CPU・メモリコスト、r: ブロックサイズ、p: 並列度
    return hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=32)


def main() -> None:
    """保存形式の表示と、照合の結果を表示する。"""
    print("[PBKDF2-HMAC-SHA256]")
    stored1 = hash_pbkdf2("correct horse")
    stored2 = hash_pbkdf2("correct horse")  # 同じパスワードを再度保存
    print("保存値:", stored1[:56] + "...")
    print("同じパスワードの保存値が一致するか:", stored1 == stored2)
    print("正しいパスワード:", verify_pbkdf2("correct horse", stored1))
    print("誤ったパスワード:", verify_pbkdf2("correct horsf", stored1))

    print("[scrypt]")
    salt = os.urandom(SALT_BYTES)
    dk = hash_scrypt("correct horse", salt)
    print("導出値の長さ:", len(dk), "バイト")
    same = hmac.compare_digest(dk, hash_scrypt("correct horse", salt))
    print("同じソルトで再計算すると一致するか:", same)


if __name__ == "__main__":
    main()
