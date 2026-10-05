"""エンコード・暗号化・ハッシュの違いを確認するサンプル.

Base64 によるエンコードは鍵を使わないため、誰でも元に戻せます。
一方、ハッシュ関数の出力から元のデータを計算で求めることはできません。

実行方法:
    python encoding_is_not_encryption.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import base64
import hashlib


def encode(text: str) -> str:
    """文字列を Base64 でエンコードする."""
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def decode(encoded: str) -> str:
    """Base64 の文字列を元に戻す（鍵は不要）."""
    return base64.b64decode(encoded).decode("utf-8")


def sha256_hex(text: str) -> str:
    """文字列の SHA-256 ハッシュ値を 16 進数で返す."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    secret = "P@ssw0rd"

    encoded = encode(secret)
    print(f"Base64 エンコード: {encoded}")
    print(f"誰でもデコードできる: {decode(encoded)}")

    print(f"SHA-256 ハッシュ値: {sha256_hex(secret)}")
    print("ハッシュ値から元の文字列を計算で求めることはできません。")


if __name__ == "__main__":
    main()
