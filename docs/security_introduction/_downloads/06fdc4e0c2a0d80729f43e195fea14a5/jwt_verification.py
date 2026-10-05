"""JWT の発行と安全な検証のサンプル.

JWT を検証するときは、許可するアルゴリズムを明示し、
有効期限などのクレームも必ず検証します。

実行方法:
    python jwt_verification.py

必要なライブラリ:
    PyJWT（python -m pip install PyJWT）
"""

import base64
import json
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

SECRET_KEY = secrets.token_bytes(32)
ISSUER = "https://auth.example.com"


def issue_token(user_id: str, lifetime: timedelta) -> str:
    """ユーザー ID を含むトークンを発行する."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "iss": ISSUER,
        "iat": now,
        "exp": now + lifetime,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> dict[str, Any]:
    """トークンを検証し、問題がなければペイロードを返す."""
    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=["HS256"],  # 許可するアルゴリズムを固定する
        issuer=ISSUER,
        options={"require": ["exp", "iss", "sub"]},
    )


def unsafe_decode(token: str) -> dict[str, Any]:
    """署名を検証せずにデコードする（悪い例）."""
    return jwt.decode(token, options={"verify_signature": False})


def b64url(data: dict[str, Any]) -> str:
    """辞書を JSON にして Base64URL でエンコードする."""
    raw = json.dumps(data).encode("utf-8")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def forge_none_token(user_id: str) -> str:
    """alg=none を指定した、署名のない偽造トークンを作る."""
    header = {"alg": "none", "typ": "JWT"}
    payload = {"sub": user_id, "iss": ISSUER, "exp": 4102444800}
    return f"{b64url(header)}.{b64url(payload)}."


def try_verify(label: str, token: str) -> None:
    """検証を試み、結果を表示する."""
    try:
        payload = verify_token(token)
        print(f"{label}: 成功（sub={payload['sub']}）")
    except jwt.InvalidTokenError as error:
        print(f"{label}: 拒否（{type(error).__name__}）")


def main() -> None:
    try_verify("正規のトークン", issue_token("alice", timedelta(minutes=15)))
    try_verify("期限切れのトークン", issue_token("alice", timedelta(seconds=-1)))

    forged = forge_none_token("admin")
    try_verify("alg=none の偽造トークン", forged)
    print(f"署名を検証しない場合（悪い例）: {unsafe_decode(forged)}")


if __name__ == "__main__":
    main()
