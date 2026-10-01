"""HMAC を使って識別子を仮名化するサンプルです。

分析のためにデータを渡すとき、氏名や電話番号などの識別子を
別の値に置き換えることを仮名化といいます。

電話番号のように取り得る値の種類が少ない識別子は、単純なハッシュ値
（SHA-256 など）に置き換えても、すべての候補のハッシュ値を計算すれば
元の値を突き止められます。秘密鍵を使う HMAC で置き換えれば、
鍵を知らない人には元の値を推測できません。

仮名化したデータも、鍵や他の情報と照合すれば個人を識別できるため、
個人情報として適切に管理する必要があります。

実行方法::

    python pseudonymize.py
"""

import hashlib
import hmac
import os
import secrets

KEY_ENV_NAME = "PSEUDONYM_KEY"
TOKEN_LENGTH = 16


def load_key() -> bytes:
    """環境変数から秘密鍵を読み込みます。未設定ならデモ用の鍵を生成します。

    実際の運用では、鍵をデータと別の場所で管理し、
    データの受け渡し先には渡さないようにします。
    """
    key_hex = os.environ.get(KEY_ENV_NAME)
    if key_hex:
        return bytes.fromhex(key_hex)
    print(f"{KEY_ENV_NAME} が未設定のため、デモ用の鍵を生成します。")
    return secrets.token_bytes(32)


def pseudonymize(identifier: str, key: bytes) -> str:
    """識別子を HMAC-SHA256 で仮名に置き換えます。

    同じ鍵と同じ識別子からは常に同じ仮名が得られるため、
    仮名化した後もデータどうしを突き合わせて分析できます。
    """
    digest = hmac.new(key, identifier.encode("utf-8"), hashlib.sha256)
    return digest.hexdigest()[:TOKEN_LENGTH]


def plain_hash(identifier: str) -> str:
    """【悪い例】鍵を使わない単純なハッシュ値に置き換えます。"""
    digest = hashlib.sha256(identifier.encode("utf-8"))
    return digest.hexdigest()[:TOKEN_LENGTH]


def main() -> None:
    """単純なハッシュ値と HMAC による仮名を比較します。"""
    key = load_key()
    records = [
        ("090-1234-5678", "購入金額 12,000 円"),
        ("080-9876-5432", "購入金額 3,500 円"),
        ("090-1234-5678", "購入金額 8,000 円"),
    ]

    for phone, detail in records:
        print(f"{pseudonymize(phone, key)}  {detail}")

    # 単純なハッシュ値は誰でも同じ計算ができるため、候補を総当たりすれば
    # 元の値を突き止められます（ここでは候補を 100 件に絞っています）。
    leaked = plain_hash("090-1234-5678")
    candidates = [f"090-1234-56{i:02d}" for i in range(100)]
    found = [c for c in candidates if plain_hash(c) == leaked]
    print("単純なハッシュ値:", leaked)
    print("総当たりで判明した元の値:", found)


if __name__ == "__main__":
    main()
