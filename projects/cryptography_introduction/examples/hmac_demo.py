"""HMAC によるメッセージ認証と、定数時間比較による検証。

実行方法::

    python hmac_demo.py
"""

import hashlib
import hmac
import secrets


def make_tag(key: bytes, message: bytes) -> bytes:
    """HMAC-SHA256 でタグを計算する。"""
    return hmac.new(key, message, hashlib.sha256).digest()


def verify(key: bytes, message: bytes, tag: bytes) -> bool:
    """タグを再計算し、hmac.compare_digest() で比較する。"""
    return hmac.compare_digest(make_tag(key, message), tag)


def main() -> None:
    key = secrets.token_bytes(32)
    message = b"amount=1000&to=alice"
    tag = make_tag(key, message)
    print(f"メッセージ: {message!r}")
    print(f"タグ      : {tag.hex()}")
    print(f"検証（正しいメッセージ）    : {verify(key, message, tag)}")

    tampered = b"amount=9000&to=alice"
    print(f"検証（改ざんされたメッセージ）: {verify(key, tampered, tag)}")

    wrong_key = secrets.token_bytes(32)
    print(f"検証（異なる鍵）            : {verify(wrong_key, message, tag)}")


if __name__ == "__main__":
    main()
