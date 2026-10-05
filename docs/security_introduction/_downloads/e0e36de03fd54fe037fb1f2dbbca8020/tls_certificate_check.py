"""TLS 接続を確立し、サーバー証明書の情報を表示するサンプル.

ssl.create_default_context() が作るコンテキストは、証明書の検証と
ホスト名の検証を自動で行います。検証に失敗すると接続は中断されます。

実行方法:
    python tls_certificate_check.py [ホスト名]
    （ホスト名を省略すると www.python.org に接続します）

注意:
    指定したホストの 443 番ポートに接続します（インターネット接続が必要です）。

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import socket
import ssl
import sys
from typing import Any

PORT = 443
TIMEOUT = 10.0


def name_to_text(name: Any) -> str:
    """getpeercert() が返す識別名を「CN=...」形式の文字列にする."""
    parts = [f"{key}={value}" for rdn in name for key, value in rdn]
    return ", ".join(parts)


def check(hostname: str) -> None:
    """hostname に TLS で接続し、証明書の情報を表示する."""
    context = ssl.create_default_context()
    print("[コンテキストの設定]")
    print(f"  証明書の検証    : {context.verify_mode.name}")
    print(f"  ホスト名の検証  : {context.check_hostname}")
    print(f"  最小 TLS バージョン: {context.minimum_version.name}")

    with socket.create_connection((hostname, PORT), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as tls:
            cert = tls.getpeercert()
            if not cert:
                raise ssl.SSLError("サーバー証明書を取得できませんでした")
            print("[接続結果]")
            print(f"  TLS バージョン  : {tls.version()}")
            cipher = tls.cipher()
            print(f"  暗号スイート    : {cipher[0] if cipher else '不明'}")
            print(f"  サブジェクト    : {name_to_text(cert['subject'])}")
            print(f"  発行者          : {name_to_text(cert['issuer'])}")
            print(f"  有効期限        : {cert['notAfter']}")
            san = cert.get("subjectAltName", ())
            names = [str(entry[1]) for entry in san
                     if isinstance(entry, tuple)]
            print(f"  SAN（先頭 5 件）: {', '.join(names[:5])}")


def main() -> None:
    hostname = sys.argv[1] if len(sys.argv) > 1 else "www.python.org"
    try:
        check(hostname)
    except ssl.SSLCertVerificationError as error:
        print(f"証明書の検証に失敗したため接続を中断しました: {error}")
    except OSError as error:
        print(f"接続できませんでした: {error}")


if __name__ == "__main__":
    main()
