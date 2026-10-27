"""cryptography ライブラリによる X25519 鍵共有と HKDF による鍵導出。

実行方法::

    pip install cryptography
    python x25519_demo.py
"""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def derive_key(shared_secret: bytes) -> bytes:
    """共有秘密をそのまま鍵にせず、HKDF で 32 バイトの鍵を導出する。"""
    hkdf = HKDF(algorithm=hashes.SHA256(), length=32, salt=None, info=b"x25519 demo")
    return hkdf.derive(shared_secret)


def main() -> None:
    alice_private = X25519PrivateKey.generate()
    bob_private = X25519PrivateKey.generate()
    alice_public = alice_private.public_key()
    bob_public = bob_private.public_key()

    raw = alice_public.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    print(f"Alice の公開鍵（{len(raw)} バイト）: {raw.hex()}")

    alice_key = derive_key(alice_private.exchange(bob_public))
    bob_key = derive_key(bob_private.exchange(alice_public))
    print(f"Alice の鍵: {alice_key.hex()}")
    print(f"Bob の鍵  : {bob_key.hex()}")
    print(f"一致するか: {alice_key == bob_key}")


if __name__ == "__main__":
    main()
