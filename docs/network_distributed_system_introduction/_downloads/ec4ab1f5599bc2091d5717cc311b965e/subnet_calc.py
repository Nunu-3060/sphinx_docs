"""IPv4 のサブネットと CIDR の計算を示すサンプル。

標準ライブラリの ipaddress モジュールを使って、次の内容を表示します。

* CIDR 表記のネットワークの、ネットワークアドレス・ブロードキャスト
  アドレス・サブネットマスク・ホスト数
* 1 つのネットワークを、より小さなサブネットに分割した結果
* IP アドレスが、どのネットワークに属するかの判定
* プライベートアドレスかどうかの判定

実行方法:
    python subnet_calc.py
"""

import ipaddress
import unicodedata


def pad(text: str, width: int) -> str:
    """全角文字を幅 2 として数え、表示幅が width になるよう空白を足す。"""
    used = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
               for c in text)
    return text + " " * max(width - used, 0)


def show_network(cidr: str) -> None:
    """CIDR 表記のネットワークの基本情報を表示する。"""
    net = ipaddress.IPv4Network(cidr)
    # 先頭（ネットワークアドレス）と末尾（ブロードキャスト）は
    # ホストに割り当てられないので、ホスト数は全体から 2 を引いた数
    hosts = list(net.hosts())
    rows = [
        ("ネットワーク", str(net)),
        ("サブネットマスク", str(net.netmask)),
        ("ネットワークアドレス", str(net.network_address)),
        ("ブロードキャストアドレス", str(net.broadcast_address)),
        ("アドレスの総数", str(net.num_addresses)),
        ("ホスト数", str(len(hosts))),
        ("ホストの範囲", f"{hosts[0]} - {hosts[-1]}"),
        ("プライベート", str(net.is_private)),
    ]
    for label, value in rows:
        print(f"{pad(label, 24)}: {value}")


def show_subnets(cidr: str, new_prefix: int) -> None:
    """ネットワークを、プレフィックス長 new_prefix のサブネットに分割する。"""
    net = ipaddress.IPv4Network(cidr)
    print(f"{net} を /{new_prefix} に分割:")
    for sub in net.subnets(new_prefix=new_prefix):
        print(f"  {str(sub):<18} ブロードキャスト "
              f"{str(sub.broadcast_address):<15}"
              f"  ホスト数 {sub.num_addresses - 2}")


def show_membership(address: str, cidrs: list[str]) -> None:
    """IP アドレスが、各ネットワークに属するかどうかを表示する。"""
    addr = ipaddress.IPv4Address(address)
    for cidr in cidrs:
        net = ipaddress.IPv4Network(cidr)
        result = "属する" if addr in net else "属さない"
        print(f"  {address} は {cidr:<17} に{result}")


def main() -> None:
    print("=== ネットワークの基本情報 ===")
    show_network("192.168.10.0/24")
    print()
    # ホストのアドレスとプレフィックス長から、所属するネットワークを求める
    iface = ipaddress.IPv4Interface("172.16.5.130/26")
    print(f"インターフェース {iface} の所属ネットワーク: {iface.network}")
    print()
    print("=== サブネット分割 ===")
    show_subnets("192.168.10.0/24", 26)
    print()
    print("=== 所属判定 ===")
    show_membership("192.168.10.77",
                    ["192.168.10.0/24", "192.168.10.64/26",
                     "192.168.10.128/26", "10.0.0.0/8"])
    print()
    print("=== プライベートアドレスかどうか ===")
    for text in ["10.1.2.3", "172.20.0.1", "192.168.0.1", "8.8.8.8"]:
        addr = ipaddress.IPv4Address(text)
        print(f"  {text:<12} プライベート: {addr.is_private}")


if __name__ == "__main__":
    main()
