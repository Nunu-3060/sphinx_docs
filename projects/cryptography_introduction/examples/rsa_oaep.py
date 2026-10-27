"""cryptography ライブラリによる RSA-OAEP 暗号化と、RSA を使ったハイブリッド暗号。

実行方法::

    pip install cryptography
    python rsa_oaep.py
"""

import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

OAEP = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)


def hybrid_encrypt(public_key: rsa.RSAPublicKey, plaintext: bytes) -> tuple[bytes, bytes, bytes]:
    """使い捨ての AES 鍵でデータを暗号化し、その鍵を RSA-OAEP で暗号化する。"""
    session_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    ciphertext = AESGCM(session_key).encrypt(nonce, plaintext, None)
    wrapped_key = public_key.encrypt(session_key, OAEP)
    return wrapped_key, nonce, ciphertext


def hybrid_decrypt(private_key: rsa.RSAPrivateKey, wrapped_key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
    """RSA-OAEP で AES 鍵を取り出し、データを復号する。"""
    session_key = private_key.decrypt(wrapped_key, OAEP)
    return AESGCM(session_key).decrypt(nonce, ciphertext, None)


def main() -> None:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=3072)
    public_key = private_key.public_key()

    message = b"hello OAEP"
    c1 = public_key.encrypt(message, OAEP)
    c2 = public_key.encrypt(message, OAEP)
    print(f"暗号文の長さ: {len(c1)} バイト")
    print(f"同じ平文の暗号文が一致するか: {c1 == c2}（OAEP は乱数を含むため一致しない）")
    print(f"復号: {private_key.decrypt(c1, OAEP)!r}")

    # 長いデータは RSA で直接暗号化せず、ハイブリッド暗号を使う。
    long_message = b"A" * 10_000
    wrapped_key, nonce, ciphertext = hybrid_encrypt(public_key, long_message)
    recovered = hybrid_decrypt(private_key, wrapped_key, nonce, ciphertext)
    print(f"ハイブリッド暗号: {len(long_message)} バイトを暗号化・復号できたか: {recovered == long_message}")


if __name__ == "__main__":
    main()
