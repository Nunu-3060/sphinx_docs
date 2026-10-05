"""HS256 の JWT を作成・検証し、改ざんを検出するサンプル（学習用）。

標準ライブラリの hmac・base64・json だけで JWT（JSON Web Token）の
構造を確かめる。ヘッダ・ペイロードは署名で改ざんを検出できるが、
暗号化されてはおらず、鍵が無くても誰でも読めることも示す。
実際のシステムでは、検証済みの JWT ライブラリを使うこと。

結果を再現できるよう、鍵と時刻は固定値にしている。実際の鍵は
secrets.token_bytes(32) などで生成し、ソースコードに書かない。

実行方法: python ch14_jwt.py
関連する章: 第 14 章「認証とアプリケーションのセキュリティ」
"""

import base64
import hashlib
import hmac
import json
from typing import Any

KEY = b"demo-key-for-learning-only-32byt"  # 学習用の固定鍵
NOW = 1_700_000_000  # 現在時刻とみなす Unix 時間（秒）


def b64url_encode(data: bytes) -> str:
    """Base64URL で符号化し、末尾の = を取り除く。"""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(text: str) -> bytes:
    """取り除かれた = を補ってから Base64URL を復号する。"""
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def encode_part(obj: dict[str, Any]) -> str:
    """辞書を JSON にして Base64URL で符号化する。"""
    raw = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    return b64url_encode(raw)


def sign(signing_input: str, key: bytes) -> str:
    """「ヘッダ.ペイロード」に対する HMAC-SHA256 の署名を返す。"""
    mac = hmac.new(key, signing_input.encode("ascii"), hashlib.sha256)
    return b64url_encode(mac.digest())


def create_token(payload: dict[str, Any], key: bytes) -> str:
    """HS256 の JWT を作成する。"""
    signing_input = encode_part({"alg": "HS256", "typ": "JWT"}) + "." \
        + encode_part(payload)
    return signing_input + "." + sign(signing_input, key)


def verify_token(token: str, key: bytes, now: int) -> dict[str, Any]:
    """JWT を検証してペイロードを返す。不正なら ValueError を送出する。"""
    header_b64, payload_b64, sig_b64 = token.split(".")
    header = json.loads(b64url_decode(header_b64))
    if header.get("alg") != "HS256":  # alg=none などを受け付けない
        raise ValueError(f"許可しないアルゴリズム: {header.get('alg')}")
    expected = sign(header_b64 + "." + payload_b64, key)
    if not hmac.compare_digest(expected, sig_b64):
        raise ValueError("署名が一致しない")
    payload: dict[str, Any] = json.loads(b64url_decode(payload_b64))
    if payload["exp"] <= now:
        raise ValueError("有効期限切れ")
    return payload


def check(label: str, token: str, now: int = NOW) -> None:
    """検証結果を 1 行で表示する。"""
    try:
        payload = verify_token(token, KEY, now)
        print(f"{label}: 成功 {payload}")
    except ValueError as e:
        print(f"{label}: 拒否（{e}）")


def main() -> None:
    """作成、デコード、検証、改ざん検出を順に示す。"""
    token = create_token(
        {"sub": "alice", "role": "user", "exp": NOW + 900}, KEY)
    header_b64, payload_b64, sig_b64 = token.split(".")
    print("[作成した JWT]")
    print("ヘッダ    :", header_b64)
    print("ペイロード:", payload_b64)
    print("署名      :", sig_b64)
    print("[鍵が無くても読める]")
    print(b64url_decode(payload_b64).decode("utf-8"))
    print("[検証]")
    check("正しいトークン", token)
    forged = encode_part({"sub": "alice", "role": "admin",
                          "exp": NOW + 900})
    check("role を書き換え", f"{header_b64}.{forged}.{sig_b64}")
    none_header = encode_part({"alg": "none", "typ": "JWT"})
    check("alg=none", f"{none_header}.{forged}.")
    check("16 分後", token, now=NOW + 960)


if __name__ == "__main__":
    main()
