"""認証付き暗号 AES-GCM による暗号化と復号のサンプル.

AES-GCM は暗号化と同時に改ざん検知用のタグを付けます。
暗号文が 1 ビットでも書き換えられると復号に失敗します。

実行方法:
    python aes_gcm.py

必要なライブラリ:
    cryptography（python -m pip install cryptography）
"""

import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_SIZE = 12  # GCM で推奨されるナンスの長さ（バイト）


def encrypt(key: bytes, plaintext: bytes, associated: bytes) -> bytes:
    """平文を暗号化し、ナンスと暗号文を連結して返す.

    ナンスは同じ鍵で絶対に再利用してはいけないため、毎回生成します。
    """
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = AESGCM(key).encrypt(nonce, plaintext, associated)
    return nonce + ciphertext


def decrypt(key: bytes, data: bytes, associated: bytes) -> bytes:
    """encrypt() の出力を復号する。改ざんされていれば InvalidTag."""
    nonce, ciphertext = data[:NONCE_SIZE], data[NONCE_SIZE:]
    return AESGCM(key).decrypt(nonce, ciphertext, associated)


def main() -> None:
    key = AESGCM.generate_key(bit_length=256)
    # 暗号化はしないが改ざんは検知したい付随データ（例: レコードの ID）
    associated = b"user_id=42"

    data = encrypt(key, "口座番号: 1234-5678".encode("utf-8"), associated)
    print(f"暗号文（16 進数）: {data.hex()}")
    print(f"復号結果: {decrypt(key, data, associated).decode('utf-8')}")

    # 暗号文の最後の 1 バイトを書き換える
    tampered = data[:-1] + bytes([data[-1] ^ 0x01])
    try:
        decrypt(key, tampered, associated)
    except InvalidTag:
        print("改ざんを検知したため、復号に失敗しました。")


if __name__ == "__main__":
    main()
