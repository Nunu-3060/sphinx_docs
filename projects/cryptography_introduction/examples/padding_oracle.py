"""AES-CBC に対するパディングオラクル攻撃のシミュレーション（学習用）。

サーバーは「パディングが正しいかどうか」だけを返す（これをオラクルと呼ぶ）。
攻撃者は鍵を知らなくても、この情報だけで暗号文を 1 バイトずつ復号できる。

実行方法::

    pip install cryptography
    python padding_oracle.py
"""

import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK = 16


class Server:
    """秘密鍵を持ち、復号時のパディング検査の結果を漏らしてしまうサーバー。"""

    def __init__(self) -> None:
        self._key = os.urandom(16)

    def encrypt(self, plaintext: bytes) -> bytes:
        """IV || 暗号文 を返す。"""
        iv = os.urandom(BLOCK)
        padder = padding.PKCS7(BLOCK * 8).padder()
        padded = padder.update(plaintext) + padder.finalize()
        encryptor = Cipher(algorithms.AES(self._key), modes.CBC(iv)).encryptor()
        return iv + encryptor.update(padded) + encryptor.finalize()

    def padding_ok(self, data: bytes) -> bool:
        """復号してパディングが正しいかどうかだけを返す（これがオラクルになる）。"""
        iv, ciphertext = data[:BLOCK], data[BLOCK:]
        decryptor = Cipher(algorithms.AES(self._key), modes.CBC(iv)).decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(BLOCK * 8).unpadder()
        try:
            unpadder.update(padded)
            unpadder.finalize()
        except ValueError:
            return False
        return True


def decrypt_block(server: Server, previous: bytes, block: bytes) -> bytes:
    """オラクルを使って 1 ブロックを復号する。previous は直前の暗号文ブロック（または IV）。"""
    intermediate = bytearray(BLOCK)  # D_K(block) の値
    for pad in range(1, BLOCK + 1):
        index = BLOCK - pad
        for guess in range(256):
            forged = bytearray(BLOCK)
            # 既に分かっている末尾のバイトは、復号結果が pad になるように設定する
            for j in range(index + 1, BLOCK):
                forged[j] = intermediate[j] ^ pad
            forged[index] = guess
            if not server.padding_ok(bytes(forged) + block):
                continue
            if pad == 1:
                # 末尾が偶然 0x02 0x02 などになった場合を除外するため、1 つ前のバイトを変えて再確認する
                forged[index - 1] ^= 0xFF
                if not server.padding_ok(bytes(forged) + block):
                    continue
            intermediate[index] = guess ^ pad
            break
    return bytes(i ^ p for i, p in zip(intermediate, previous))


def attack(server: Server, data: bytes) -> bytes:
    """全ブロックを復号し、パディングを取り除いた平文を返す。"""
    blocks = [data[i:i + BLOCK] for i in range(0, len(data), BLOCK)]
    plaintext = b"".join(decrypt_block(server, blocks[i - 1], blocks[i]) for i in range(1, len(blocks)))
    return plaintext[:-plaintext[-1]]


def main() -> None:
    server = Server()
    data = server.encrypt(b"Transfer 1000 yen to account 12345")
    print(f"暗号文（IV を含む）: {data.hex()}")
    recovered = attack(server, data)
    print(f"鍵を使わずに復号した平文: {recovered!r}")


if __name__ == "__main__":
    main()
