"""認証付き暗号（AES-GCM / ChaCha20-Poly1305）による暗号化と改ざん検知。

実行方法::

    pip install cryptography
    python aead_demo.py
"""

import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

NONCE_SIZE = 12  # 96 ビットのナンス


def seal(aead: AESGCM | ChaCha20Poly1305, plaintext: bytes, associated_data: bytes) -> bytes:
    """ナンスを生成して暗号化し、ナンス || 暗号文 || タグ を返す。"""
    nonce = os.urandom(NONCE_SIZE)
    return nonce + aead.encrypt(nonce, plaintext, associated_data)


def open_sealed(aead: AESGCM | ChaCha20Poly1305, data: bytes, associated_data: bytes) -> bytes:
    """seal() の出力を復号する。改ざんされていれば InvalidTag が送出される。"""
    nonce, ciphertext = data[:NONCE_SIZE], data[NONCE_SIZE:]
    return aead.decrypt(nonce, ciphertext, associated_data)


def main() -> None:
    header = b"user-id=42"  # 暗号化はしないが改ざんは検知したいデータ（関連データ）
    plaintext = b"secret message"

    ciphers: list[tuple[str, AESGCM | ChaCha20Poly1305]] = [
        ("AES-256-GCM", AESGCM(AESGCM.generate_key(bit_length=256))),
        ("ChaCha20-Poly1305", ChaCha20Poly1305(ChaCha20Poly1305.generate_key())),
    ]
    for name, aead in ciphers:
        sealed = seal(aead, plaintext, header)
        print(f"{name}: {len(plaintext)} バイトの平文 -> {len(sealed)} バイト（ナンス 12 + 暗号文 14 + タグ 16）")
        print(f"  復号: {open_sealed(aead, sealed, header)!r}")

        tampered = bytearray(sealed)
        tampered[NONCE_SIZE] ^= 0x01  # 暗号文の 1 ビットを反転
        try:
            open_sealed(aead, bytes(tampered), header)
        except InvalidTag:
            print("  暗号文の改ざんを検知した")

        try:
            open_sealed(aead, sealed, b"user-id=43")
        except InvalidTag:
            print("  関連データの改ざんを検知した")


if __name__ == "__main__":
    main()
