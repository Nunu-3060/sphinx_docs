"""SSRF を防ぐための URL 検証のサンプル.

利用者が指定した URL にサーバーがアクセスする機能では、内部ネットワークや
クラウドのメタデータサービス（169.254.169.254）へのアクセスを防ぐ必要が
あります。ここでは、ホスト名を名前解決した結果の IP アドレスを検証します。

実行方法:
    python ssrf_url_check.py

注意:
    URL の検証のために DNS の名前解決を行いますが、URL へのアクセスは
    行いません。

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

import ipaddress
import socket
from urllib.parse import urlsplit

ALLOWED_SCHEMES = {"https"}


def resolve_addresses(hostname: str) -> list[str]:
    """ホスト名を名前解決し、IP アドレスの一覧を返す."""
    infos = socket.getaddrinfo(hostname, None)
    return sorted({str(info[4][0]) for info in infos})


def is_public_address(address: str) -> bool:
    """グローバルな（インターネット上の）IP アドレスか判定する."""
    return ipaddress.ip_address(address).is_global


def check_url(url: str) -> str:
    """アクセスしてよい URL なら "許可"、そうでなければ理由を返す."""
    parts = urlsplit(url)
    if parts.scheme not in ALLOWED_SCHEMES:
        return f"拒否（スキーム {parts.scheme!r} は許可されていません）"
    if not parts.hostname:
        return "拒否（ホスト名がありません）"
    try:
        addresses = resolve_addresses(parts.hostname)
    except socket.gaierror:
        return "拒否（名前解決できません）"
    for address in addresses:
        if not is_public_address(address):
            return f"拒否（内部アドレス {address} に解決されました）"
    return "許可"


def main() -> None:
    urls = [
        "https://www.python.org/",
        "http://www.python.org/",
        "https://127.0.0.1/admin",
        "https://169.254.169.254/latest/meta-data/",
        "https://10.0.0.5/",
        "https://localhost/",
        "file:///etc/passwd",
    ]
    for url in urls:
        print(f"{url:45s} -> {check_url(url)}")


if __name__ == "__main__":
    main()
