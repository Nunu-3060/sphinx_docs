"""ハッシュ関数とメッセージ認証コード（HMAC）の違いを確認するサンプル.

ハッシュ値だけでは改ざんを検知できない場合があることと、
共有鍵を使う HMAC なら改ざんを検知できることを示します。

実行方法:
    python hash_and_hmac.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import hashlib
import hmac
import secrets


def sha256_hex(message: bytes) -> str:
    """メッセージの SHA-256 ハッシュ値を返す."""
    return hashlib.sha256(message).hexdigest()


def hmac_sha256_hex(key: bytes, message: bytes) -> str:
    """メッセージの HMAC-SHA256 を返す."""
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def verify_hmac(key: bytes, message: bytes, tag: str) -> bool:
    """HMAC を定数時間で比較して検証する."""
    expected = hmac_sha256_hex(key, message)
    return hmac.compare_digest(expected, tag)


def main() -> None:
    message = b"amount=1000&to=alice"
    tampered = b"amount=9999&to=mallory"

    # ハッシュ値は誰でも計算できるため、攻撃者はメッセージを
    # 書き換えたうえでハッシュ値も計算し直せる
    print("[ハッシュ値のみの場合]")
    print(f"  元のメッセージ    : {sha256_hex(message)}")
    print(f"  改ざん後に再計算  : {sha256_hex(tampered)}")
    print("  -> 受信者には改ざんを見分ける手段がありません。")

    # HMAC は鍵を知らないと正しい値を計算できない
    key = secrets.token_bytes(32)
    tag = hmac_sha256_hex(key, message)
    print("[HMAC の場合]")
    print(f"  元のメッセージの検証: {verify_hmac(key, message, tag)}")
    print(f"  改ざん後の検証      : {verify_hmac(key, tampered, tag)}")


if __name__ == "__main__":
    main()
