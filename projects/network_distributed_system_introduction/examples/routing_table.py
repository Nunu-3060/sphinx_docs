"""ルーティングテーブルを最長一致（longest prefix match）で検索するサンプル。

ルーターは、宛先 IP アドレスに一致する経路が複数あるとき、
プレフィックス長が最も長い（最も具体的な）経路を選びます。
このサンプルでは、簡単なルーティングテーブルを作り、
いくつかの宛先について、一致した経路と選ばれた経路を表示します。

実行方法:
    python routing_table.py
"""

import ipaddress
import unicodedata
from dataclasses import dataclass


def pad(text: str, width: int) -> str:
    """全角文字を幅 2 として数え、表示幅が width になるよう空白を足す。"""
    used = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
               for c in text)
    return text + " " * max(width - used, 0)


@dataclass(frozen=True)
class Route:
    """ルーティングテーブルの 1 行（経路）。"""

    network: ipaddress.IPv4Network  # 宛先ネットワーク
    next_hop: str  # 次に転送するルーター（直結なら "直結"）
    interface: str  # 送出するインターフェース


def make_route(cidr: str, next_hop: str, interface: str) -> Route:
    """文字列から経路を作る。"""
    return Route(ipaddress.IPv4Network(cidr), next_hop, interface)


class RoutingTable:
    """経路を保持し、最長一致で検索するルーティングテーブル。"""

    def __init__(self, routes: list[Route]) -> None:
        self.routes = routes

    def matches(self, dest: ipaddress.IPv4Address) -> list[Route]:
        """宛先を含むすべての経路を返す。"""
        return [r for r in self.routes if dest in r.network]

    def lookup(self, dest: ipaddress.IPv4Address) -> Route | None:
        """最長一致で経路を 1 つ選ぶ。一致する経路がなければ None。"""
        candidates = self.matches(dest)
        if not candidates:
            return None
        # プレフィックス長が最も長い経路を選ぶ
        return max(candidates, key=lambda r: r.network.prefixlen)

    def show(self) -> None:
        """テーブルの内容を表示する。"""
        print(pad("宛先ネットワーク", 18) + pad("ネクストホップ", 16)
              + "インターフェース")
        for r in self.routes:
            print(pad(str(r.network), 18) + pad(r.next_hop, 16)
                  + r.interface)


def main() -> None:
    table = RoutingTable([
        make_route("192.168.1.0/24", "直結", "eth0"),
        make_route("10.0.0.0/8", "192.168.1.254", "eth0"),
        make_route("10.20.0.0/16", "192.168.1.253", "eth0"),
        make_route("10.20.30.0/24", "172.16.0.2", "eth1"),
        make_route("172.16.0.0/30", "直結", "eth1"),
        # デフォルトルート（すべての宛先に一致する /0 の経路）
        make_route("0.0.0.0/0", "192.168.1.1", "eth0"),
    ])
    print("=== ルーティングテーブル ===")
    table.show()
    print()
    print("=== 宛先ごとの検索結果 ===")
    destinations = ["10.20.30.40", "10.20.99.1", "10.99.0.1",
                    "192.168.1.50", "172.16.0.2", "203.0.113.5"]
    for text in destinations:
        dest = ipaddress.IPv4Address(text)
        found = [str(r.network) for r in table.matches(dest)]
        best = table.lookup(dest)
        print(f"宛先 {text}")
        print(f"  一致した経路: {', '.join(found)}")
        if best is None:
            print("  選ばれた経路: なし（破棄）")
        else:
            print(f"  選ばれた経路: {best.network} -> {best.next_hop}"
                  f" ({best.interface})")


if __name__ == "__main__":
    main()
