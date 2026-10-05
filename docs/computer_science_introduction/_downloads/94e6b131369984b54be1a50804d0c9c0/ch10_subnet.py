"""ipaddress モジュールで CIDR 表記のネットワークを計算するサンプル。

ネットワークアドレス、サブネットマスク、ブロードキャストアドレス、
ホストに割り当てられるアドレス数、所属判定、サブネット分割を示す。

実行方法: python ch10_subnet.py
関連する章: 第 10 章「コンピュータネットワーク」
"""

import ipaddress


def describe(cidr: str) -> None:
    """IPv4 ネットワークの各種アドレスを表示する。"""
    net = ipaddress.IPv4Network(cidr)
    print(f"ネットワーク      : {net}")
    print(f"サブネットマスク  : {net.netmask}")
    print(f"マスク（2 進数）  : {int(net.netmask):032b}")
    print(f"ブロードキャスト  : {net.broadcast_address}")
    # 全アドレスからネットワークアドレスとブロードキャストアドレスを除く
    print(f"ホスト用アドレス数: {net.num_addresses - 2}")
    hosts = list(net.hosts())
    print(f"ホストの範囲      : {hosts[0]} - {hosts[-1]}")


def main() -> None:
    """CIDR の計算例を表示する。"""
    describe("192.168.10.0/24")

    print()
    net = ipaddress.IPv4Network("192.168.10.0/24")
    for addr in ["192.168.10.77", "192.168.11.5"]:
        inside = ipaddress.IPv4Address(addr) in net
        print(f"{addr} は {net} に含まれるか: {inside}")

    print()
    print(f"{net} を /26 に分割:")
    for sub in net.subnets(new_prefix=26):
        print(f"  {sub} (ブロードキャスト {sub.broadcast_address})")

    print()
    for addr in ["10.1.2.3", "172.16.0.1", "8.8.8.8", "2001:db8::1"]:
        ip = ipaddress.ip_address(addr)
        print(f"{addr}: IPv{ip.version}, プライベート={ip.is_private}")


if __name__ == "__main__":
    main()
