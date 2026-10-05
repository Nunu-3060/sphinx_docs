"""ワンタイムパスワード（TOTP、RFC 6238）の実装サンプル.

認証アプリが表示する 6 桁のコードは、共有の秘密鍵と現在時刻から
HMAC を使って計算されています。

実行方法:
    python totp.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import base64
import hashlib
import hmac
import secrets
import struct
import time

TIME_STEP = 30  # コードが切り替わる間隔（秒）


def hotp(key: bytes, counter: int, digits: int = 6) -> str:
    """カウンター値からワンタイムパスワードを計算する（RFC 4226）."""
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    # 動的切り出し: 最後のバイトの下位 4 ビットを開始位置にする
    offset = digest[-1] & 0x0F
    code = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(code % 10 ** digits).zfill(digits)


def totp(key: bytes, unix_time: float, digits: int = 6) -> str:
    """時刻からワンタイムパスワードを計算する（RFC 6238）."""
    return hotp(key, int(unix_time // TIME_STEP), digits)


def verify_totp(key: bytes, code: str, unix_time: float,
                window: int = 1) -> bool:
    """前後 window ステップの時刻のずれを許して検証する."""
    for step in range(-window, window + 1):
        candidate = totp(key, unix_time + step * TIME_STEP, len(code))
        if hmac.compare_digest(candidate, code):
            return True
    return False


def main() -> None:
    # RFC 6238 付録 B のテストベクターで実装を確認する
    rfc_key = b"12345678901234567890"
    result = totp(rfc_key, 59, digits=8)
    print(f"RFC 6238 のテストベクター: {result}（期待値 94287082）")

    # 新しい秘密鍵を作り、認証アプリに登録する形式（Base32）で表示する
    key = secrets.token_bytes(20)
    print(f"秘密鍵（Base32）: {base64.b32encode(key).decode('ascii')}")

    now = time.time()
    code = totp(key, now)
    print(f"現在のコード: {code}")
    print(f"現在の検証結果: {verify_totp(key, code, now)}")
    print(f"5 分後に同じコードで検証: {verify_totp(key, code, now + 300)}")


if __name__ == "__main__":
    main()
