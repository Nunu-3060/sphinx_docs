"""TLS で Web サーバーに接続し、ネゴシエーションの結果と証明書を表示するサンプル。

指定したホスト (既定は www.example.com) の 443 番ポートに TCP で接続し、
``ssl`` モジュールで TLS のハンドシェイクを行います。証明書の検証
(信頼できる認証局の署名か、有効期限内か、ホスト名が一致するか) を
有効にしたうえで、次の情報を表示します。

* TCP の接続と TLS のハンドシェイクにかかった時間
* 使われた TLS のバージョンと暗号スイート
* サーバー証明書の subject、issuer、有効期間、SAN (subjectAltName)

最後に、信頼する認証局を 1 つも登録していない状態で接続し直し、
証明書の検証が失敗する様子を示します。

インターネット接続が必要です。

実行方法::

    python tls_inspect.py                 # www.example.com に接続する
    python tls_inspect.py www.python.org  # 接続先を変える
"""

import socket
import ssl
import sys
import time
from typing import Any

TIMEOUT = 5.0  # 接続とハンドシェイクの最大待ち時間 (秒)
PORT = 443


def format_name(name: Any) -> str:
    """getpeercert() の subject / issuer を「CN=..., O=...」の形にする。"""
    short = {"commonName": "CN", "organizationName": "O",
             "countryName": "C", "organizationalUnitName": "OU"}
    parts: list[str] = []
    for rdn in name:
        for key, value in rdn:
            parts.append(f"{short.get(key, key)}={value}")
    return ", ".join(parts)


def inspect(host: str) -> None:
    """host に TLS で接続し、ネゴシエーションの結果と証明書を表示する。"""
    # 既定のコンテキストは、OS などの信頼する認証局の証明書を読み込み、
    # 証明書の検証とホスト名の確認を行う
    context = ssl.create_default_context()

    # 名前解決の時間を含めないよう、先に IP アドレスを求めておく
    infos = socket.getaddrinfo(host, PORT, type=socket.SOCK_STREAM)
    ip = str(infos[0][4][0])
    t0 = time.perf_counter()
    sock = socket.create_connection((ip, PORT), timeout=TIMEOUT)
    t1 = time.perf_counter()
    # server_hostname は SNI としてサーバーに送られ、ホスト名の確認にも使う
    with context.wrap_socket(sock, server_hostname=host) as tls:
        t2 = time.perf_counter()
        print(f"接続先            : {host} ({ip}) ポート {PORT}")
        print(f"TCP の接続        : {(t1 - t0) * 1000:.1f} ms")
        print(f"TLS ハンドシェイク: {(t2 - t1) * 1000:.1f} ms")
        print(f"TLS のバージョン  : {tls.version()}")
        cipher = tls.cipher()
        if cipher is not None:
            print(f"暗号スイート      : {cipher[0]} (鍵長 {cipher[2]} ビット)")
        cert = tls.getpeercert()
    if not cert:
        raise ssl.SSLError("証明書を取得できませんでした")

    print("--- サーバー証明書 ---")
    print(f"subject   : {format_name(cert['subject'])}")
    print(f"issuer    : {format_name(cert['issuer'])}")
    print(f"有効期間  : {cert['notBefore']} から {cert['notAfter']} まで")
    expires = ssl.cert_time_to_seconds(str(cert["notAfter"]))
    days = (expires - time.time()) / 86400
    print(f"残り日数  : {days:.0f} 日")
    for entry in cert.get("subjectAltName", ()):
        print(f"SAN       : {entry[0]}:{entry[1]}")


def try_without_ca(host: str) -> None:
    """信頼する認証局を登録せずに接続し、証明書の検証が失敗する様子を示す。"""
    print("--- 信頼する認証局を 1 つも登録しない場合 ---")
    # PROTOCOL_TLS_CLIENT は検証とホスト名の確認を行うが、
    # load_default_certs() を呼ばないので信頼する認証局が空になる
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    try:
        with socket.create_connection((host, PORT), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=host):
                print("検証に成功しました")
    except ssl.SSLCertVerificationError as e:
        print(f"検証に失敗しました: {e.verify_message}")


def main() -> None:
    host = sys.argv[1] if len(sys.argv) > 1 else "www.example.com"
    try:
        inspect(host)
    except ssl.SSLCertVerificationError as e:
        print(f"証明書の検証に失敗しました: {e.verify_message}")
        sys.exit(1)
    except socket.gaierror as e:
        print(f"名前解決に失敗しました: {e}")
        sys.exit(1)
    except (OSError, ssl.SSLError) as e:
        print(f"接続に失敗しました: {e}")
        print("インターネット接続とホスト名を確認してください。")
        sys.exit(1)
    print()
    try_without_ca(host)


if __name__ == "__main__":
    main()
