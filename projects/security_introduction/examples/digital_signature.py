"""Ed25519 によるデジタル署名と検証のサンプル.

秘密鍵で署名し、公開鍵で検証します。公開鍵は誰に渡しても
問題ありませんが、署名を作れるのは秘密鍵の持ち主だけです。

実行方法:
    python digital_signature.py

必要なライブラリ:
    cryptography（python -m pip install cryptography）
"""

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


def verify(public_key: Ed25519PublicKey, signature: bytes,
           message: bytes) -> bool:
    """署名を検証し、正しければ True を返す."""
    try:
        public_key.verify(signature, message)
    except InvalidSignature:
        return False
    return True


def main() -> None:
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    message = "リリース 1.0 のファイル一式".encode("utf-8")
    signature = private_key.sign(message)
    print(f"署名（16 進数）: {signature.hex()}")

    print(f"元のメッセージの検証: {verify(public_key, signature, message)}")
    tampered = "リリース 1.0 のファイル一式（改変）".encode("utf-8")
    print(f"改変後の検証        : {verify(public_key, signature, tampered)}")


if __name__ == "__main__":
    main()
