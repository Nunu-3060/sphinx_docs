"""暗号学的ハッシュ関数と HMAC の性質を示すサンプル。

hashlib で SHA-256 のハッシュ値を計算し、入力が 1 文字違うだけで
出力のおよそ半分のビットが変わること（雪崩効果）を確認する。
さらに hmac で HMAC-SHA256 によるメッセージ認証コードを計算し、
hmac.compare_digest で検証する。

実行方法: python ch13_hash.py
関連する章: 第 13 章「情報セキュリティと暗号」
"""

import hashlib
import hmac


def sha256_hex(data: bytes) -> str:
    """data の SHA-256 ハッシュ値を 16 進文字列で返す。"""
    return hashlib.sha256(data).hexdigest()


def bit_difference(a: bytes, b: bytes) -> int:
    """同じ長さのバイト列 a と b で値が異なるビットの数を返す。"""
    return sum(bin(x ^ y).count("1") for x, y in zip(a, b, strict=True))


def make_tag(key: bytes, message: bytes) -> bytes:
    """鍵 key を使って message の HMAC-SHA256 を計算する。"""
    return hmac.new(key, message, hashlib.sha256).digest()


def verify_tag(key: bytes, message: bytes, tag: bytes) -> bool:
    """タグが正しいかを定数時間の比較で検証する。"""
    return hmac.compare_digest(make_tag(key, message), tag)


def main() -> None:
    """ハッシュ値、雪崩効果、HMAC の計算と検証を表示する。"""
    print("[SHA-256]")
    for text in [b"hello", b"hellp", b"hello" * 1000]:
        digest = sha256_hex(text)
        print(f"入力 {len(text):>4} バイト -> {digest[:32]}...")

    d1 = hashlib.sha256(b"hello").digest()
    d2 = hashlib.sha256(b"hellp").digest()
    diff = bit_difference(d1, d2)
    print(f"異なるビット数: {diff} / {len(d1) * 8}")

    print("[HMAC-SHA256]")
    key = b"shared-secret-key"
    message = b"amount=100&to=alice"
    tag = make_tag(key, message)
    print("タグ        :", tag.hex()[:32] + "...")
    print("正しい検証  :", verify_tag(key, message, tag))
    tampered = b"amount=900&to=alice"
    print("改ざん後    :", verify_tag(key, tampered, tag))
    print("鍵が異なる  :", verify_tag(b"wrong-key", message, tag))


if __name__ == "__main__":
    main()
