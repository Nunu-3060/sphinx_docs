"""パスワードを安全に保存し、照合するサンプルです。

パスワードを平文のまま保存したり、ソルトなしの高速なハッシュ関数
（MD5 や SHA-256 を 1 回だけ適用するなど）で保存したりすると、
データベースが漏えいしたときに多くのパスワードが復元されてしまいます。
このサンプルでは、標準ライブラリの hashlib.scrypt を使い、
利用者ごとに異なるソルトを付けて計算コストの高いハッシュ値を保存します。

パラメーターは OWASP Password Storage Cheat Sheet の推奨値
（N=2**17, r=8, p=1）に合わせています。

実行方法::

    python password_hashing.py
"""

import hashlib
import hmac
import secrets

SCRYPT_N = 2**17  # CPU とメモリーのコスト
SCRYPT_R = 8  # ブロックサイズ
SCRYPT_P = 1  # 並列度
SALT_BYTES = 16
KEY_BYTES = 32

# scrypt が使うメモリー量はおよそ 128 * N * r バイト（この設定で 128 MiB）です。
MAX_MEMORY = 256 * 1024 * 1024


def _derive_key(password: str, salt: bytes, n: int, r: int, p: int) -> bytes:
    """パスワードとソルトから scrypt で鍵を導出します。"""
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=n,
        r=r,
        p=p,
        maxmem=MAX_MEMORY,
        dklen=KEY_BYTES,
    )


def hash_password(password: str) -> str:
    """パスワードを保存用の文字列に変換します。

    戻り値は「方式$N$r$p$ソルト$ハッシュ値」の形式です。
    パラメーターも一緒に保存しておくと、将来コストを引き上げたときにも
    古いハッシュ値を照合できます。
    """
    salt = secrets.token_bytes(SALT_BYTES)
    key = _derive_key(password, salt, SCRYPT_N, SCRYPT_R, SCRYPT_P)
    return "$".join(
        ["scrypt", str(SCRYPT_N), str(SCRYPT_R), str(SCRYPT_P),
         salt.hex(), key.hex()]
    )


def verify_password(password: str, stored: str) -> bool:
    """入力されたパスワードが保存済みのハッシュ値と一致するか調べます。"""
    scheme, n, r, p, salt_hex, key_hex = stored.split("$")
    if scheme != "scrypt":
        raise ValueError(f"未対応の方式です: {scheme}")
    key = _derive_key(password, bytes.fromhex(salt_hex), int(n), int(r),
                      int(p))
    # 比較にかかる時間から情報が漏れないよう、定数時間で比較します。
    return hmac.compare_digest(key, bytes.fromhex(key_hex))


def main() -> None:
    """ハッシュ化と照合の流れを示します。"""
    stored = hash_password("correct horse battery staple")
    print("保存する値:", stored)

    # 同じパスワードでもソルトが異なるため、保存される値は毎回変わります。
    print("2 回目の値:", hash_password("correct horse battery staple"))

    print("正しいパスワード:",
          verify_password("correct horse battery staple", stored))
    print("誤ったパスワード:", verify_password("password123", stored))


if __name__ == "__main__":
    main()
