"""ソルトとストレッチングを用いたパスワードの保存と検証。

標準ライブラリの hashlib.scrypt() を使う。保存形式は「ソルト$ハッシュ値」（いずれも 16 進）とする。

実行方法::

    python password_hash.py
"""

import hashlib
import hmac
import secrets

# scrypt のパラメータ（n: CPU / メモリコスト、r: ブロックサイズ、p: 並列度）。
# OWASP の推奨する最低値（N = 2^17, r = 8, p = 1）に合わせている。必要なメモリは 128 * r * N = 128 MiB である。
SCRYPT_N = 2**17
SCRYPT_R = 8
SCRYPT_P = 1
KEY_LENGTH = 32
MAX_MEMORY = 256 * 1024 * 1024  # OpenSSL の既定の上限（32 MiB）では足りないため引き上げる


def _derive(password: str, salt: bytes) -> bytes:
    """パスワードとソルトから scrypt でハッシュ値を導出する。"""
    return hashlib.scrypt(password.encode(), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, maxmem=MAX_MEMORY,
                          dklen=KEY_LENGTH)


def hash_password(password: str) -> str:
    """利用者ごとに異なるソルトを生成し、保存用の文字列を返す。"""
    salt = secrets.token_bytes(16)
    return f"{salt.hex()}${_derive(password, salt).hex()}"


def verify_password(password: str, stored: str) -> bool:
    """保存されたソルトでハッシュ値を再計算し、定数時間で比較する。"""
    salt_hex, hash_hex = stored.split("$")
    return hmac.compare_digest(_derive(password, bytes.fromhex(salt_hex)), bytes.fromhex(hash_hex))


def main() -> None:
    stored1 = hash_password("correct horse battery staple")
    stored2 = hash_password("correct horse battery staple")
    print(f"保存値 1: {stored1}")
    print(f"保存値 2: {stored2}")
    print("  -> 同じパスワードでもソルトが異なるため保存値は異なる")
    print(f"正しいパスワードの検証  : {verify_password('correct horse battery staple', stored1)}")
    print(f"誤ったパスワードの検証  : {verify_password('password123', stored1)}")


if __name__ == "__main__":
    main()
