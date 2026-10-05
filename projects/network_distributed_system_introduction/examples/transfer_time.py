"""帯域幅と遅延からデータの転送時間を計算するサンプル。

データを送り終えるまでの時間は、おおよそ次の式で表せます。

    転送時間 = 遅延 + データサイズ / 帯域幅

このプログラムは、いくつかの回線とデータサイズの組み合わせについて
転送時間を計算して表にします。また、各回線の帯域幅遅延積
(帯域幅 x RTT) を計算し、回線を満たすために送信中にしておく
必要があるデータ量を示します。

ここでは簡単のため、1 KB = 1,000 バイト、1 MB = 1,000,000 バイトと
します。TCP の輻輳制御やヘッダーの大きさなどは考えていません。

実行方法:

    python transfer_time.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Link:
    """回線の性質 (帯域幅と片道の遅延)。"""

    name: str
    bandwidth_bps: float  # 帯域幅 (ビット毎秒)
    delay_s: float  # 片道の遅延 (秒)

    @property
    def rtt_s(self) -> float:
        """往復の遅延 (RTT)。ここでは片道の遅延の 2 倍とする。"""
        return 2 * self.delay_s


# 代表的な回線の例 (数値は説明用のおおよその値)
LINKS: list[Link] = [
    Link("データセンター内", 10e9, 0.0001),
    Link("家庭の光回線", 100e6, 0.010),
    Link("モバイル回線", 20e6, 0.030),
    Link("大陸間の専用線", 1e9, 0.070),
    Link("静止衛星回線", 50e6, 0.270),
]

# 転送するデータのサイズ (バイト)
SIZES: list[tuple[str, int]] = [
    ("1 KB", 1_000),
    ("100 KB", 100_000),
    ("10 MB", 10_000_000),
    ("1 GB", 1_000_000_000),
]


def transfer_time(size_bytes: int, link: Link) -> float:
    """データを送り終えて相手に届くまでの時間 (秒) を返す。"""
    transmission = size_bytes * 8 / link.bandwidth_bps  # 送り出す時間
    return link.delay_s + transmission


def bandwidth_delay_product(link: Link) -> float:
    """帯域幅遅延積 (バイト) を返す。帯域幅 x RTT をバイトに直す。"""
    return link.bandwidth_bps * link.rtt_s / 8


def format_time(seconds: float) -> str:
    """秒を読みやすい単位 (μs, ms, s) の文字列にする。"""
    if seconds < 0.001:
        return f"{seconds * 1e6:.1f} μs"
    if seconds < 1:
        return f"{seconds * 1e3:.1f} ms"
    return f"{seconds:.2f} s"


def format_bytes(size: float) -> str:
    """バイト数を読みやすい単位の文字列にする。"""
    for unit, scale in (("GB", 1e9), ("MB", 1e6), ("KB", 1e3)):
        if size >= scale:
            return f"{size / scale:.1f} {unit}"
    return f"{size:.0f} B"


def format_bandwidth(bps: float) -> str:
    """帯域幅を Gbps または Mbps の文字列にする。"""
    if bps >= 1e9:
        return f"{bps / 1e9:g} Gbps"
    return f"{bps / 1e6:g} Mbps"


def pad(text: str, width: int) -> str:
    """全角文字を幅 2 として、左寄せで width 桁にそろえる。"""
    shown = sum(1 if ord(c) < 0x2E80 else 2 for c in text)
    return text + " " * max(width - shown, 0)


def main() -> None:
    # 回線の一覧
    print("回線の一覧")
    print(pad("回線", 18) + pad("帯域幅", 12) + "片道の遅延")
    for link in LINKS:
        print(
            pad(link.name, 18)
            + pad(format_bandwidth(link.bandwidth_bps), 12)
            + format_time(link.delay_s)
        )
    print()

    # サイズと回線ごとの転送時間
    print("転送時間 = 遅延 + サイズ / 帯域幅")
    header = pad("回線", 18)
    for label, _ in SIZES:
        header += f"{label:>10}"
    print(header)
    for link in LINKS:
        row = pad(link.name, 18)
        for _, size in SIZES:
            row += f"{format_time(transfer_time(size, link)):>10}"
        print(row)
    print()

    # 帯域幅遅延積
    print("帯域幅遅延積 = 帯域幅 x RTT")
    print(pad("回線", 18) + pad("RTT", 12) + "帯域幅遅延積")
    for link in LINKS:
        print(
            pad(link.name, 18)
            + pad(format_time(link.rtt_s), 12)
            + format_bytes(bandwidth_delay_product(link))
        )


if __name__ == "__main__":
    main()
