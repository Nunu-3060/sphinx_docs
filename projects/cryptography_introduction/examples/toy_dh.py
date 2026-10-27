"""Diffie-Hellman 鍵共有と中間者攻撃のシミュレーション（学習用）。

群には RFC 3526 の 2048 ビット MODP 群（グループ 14）を使う。

実行方法::

    python toy_dh.py
"""

import hashlib
import secrets

# RFC 3526 グループ 14 の素数 p（安全素数）と生成元 g
P = int(
    "FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1"
    "29024E088A67CC74020BBEA63B139B22514A08798E3404DD"
    "EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245"
    "E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED"
    "EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D"
    "C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F"
    "83655D23DCA3AD961C62F356208552BB9ED529077096966D"
    "670C354E4ABC9804F1746C08CA18217C32905E462E36CE3B"
    "E39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9"
    "DE2BCBF6955817183995497CEA956AE515D2261898FA0510"
    "15728E5A8AACAA68FFFFFFFFFFFFFFFF",
    16,
)
G = 2


class Party:
    """鍵共有の参加者。秘密の指数と公開値を持つ。"""

    def __init__(self, name: str) -> None:
        self.name = name
        self._secret = secrets.randbelow(P - 3) + 2  # 2 <= x <= p - 2
        self.public = pow(G, self._secret, P)

    def shared_key(self, other_public: int) -> bytes:
        """相手の公開値から共有秘密を計算し、SHA-256 で鍵に変換する。

        学習用に SHA-256 で簡略化している。実務では x25519_demo.py のように HKDF を使う。
        """
        if not 1 < other_public < P - 1:
            raise ValueError("不正な公開値")
        shared = pow(other_public, self._secret, P)
        return hashlib.sha256(shared.to_bytes(256, "big")).digest()


def main() -> None:
    alice = Party("Alice")
    bob = Party("Bob")
    k_alice = alice.shared_key(bob.public)
    k_bob = bob.shared_key(alice.public)
    print("通常の鍵共有")
    print(f"  Alice の鍵: {k_alice.hex()[:32]}...")
    print(f"  Bob の鍵  : {k_bob.hex()[:32]}...")
    print(f"  一致するか: {k_alice == k_bob}")

    # 中間者 Mallory が公開値をすり替える
    mallory_to_alice = Party("Mallory(A)")
    mallory_to_bob = Party("Mallory(B)")
    k_alice = alice.shared_key(mallory_to_alice.public)  # Alice は Bob の値だと思っている
    k_bob = bob.shared_key(mallory_to_bob.public)  # Bob は Alice の値だと思っている
    print("中間者攻撃")
    print(f"  Alice と Mallory の鍵が一致: {k_alice == mallory_to_alice.shared_key(alice.public)}")
    print(f"  Bob と Mallory の鍵が一致  : {k_bob == mallory_to_bob.shared_key(bob.public)}")
    print(f"  Alice と Bob の鍵が一致    : {k_alice == k_bob}")


if __name__ == "__main__":
    main()
