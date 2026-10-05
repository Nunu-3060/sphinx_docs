"""DNS の問い合わせメッセージを自分で組み立てて送り、応答を解析するサンプル。

DNS のメッセージ (RFC 1035) をバイト列として組み立て、UDP の 53 番ポートで
フルリゾルバー (既定は 8.8.8.8) に送ります。返ってきた応答のバイト列を
解析し、ヘッダーの各フィールドと、回答セクションのレコード (A、AAAA、
CNAME、MX、NS、TXT、SOA) を表示します。応答に含まれる名前の圧縮
(圧縮ポインタ) にも対応しています。最後に、比較として OS のスタブ
リゾルバーを使う ``socket.getaddrinfo`` の結果も表示します。

インターネット接続が必要です (UDP の 53 番ポートで外部の DNS サーバーに
到達できる必要があります)。

実行方法::

    python dns_query.py                          # www.python.org の A と AAAA
    python dns_query.py example.com -t MX -t NS  # 種類を指定する
    python dns_query.py www.python.org -s 1.1.1.1  # 問い合わせ先を変える
"""

import argparse
import random
import socket
import struct
import sys
from dataclasses import dataclass

TIMEOUT = 3.0  # 応答を待つ最大時間 (秒)

# レコードの種類 (TYPE) の名前と番号
TYPES: dict[str, int] = {
    "A": 1, "NS": 2, "CNAME": 5, "SOA": 6, "MX": 15, "TXT": 16, "AAAA": 28,
}
TYPE_NAMES: dict[int, str] = {v: k for k, v in TYPES.items()}
CLASS_IN = 1  # インターネットのクラス

# RCODE (応答コード) の意味
RCODES: dict[int, str] = {
    0: "NOERROR (成功)",
    1: "FORMERR (問い合わせの形式が不正)",
    2: "SERVFAIL (サーバー側の失敗)",
    3: "NXDOMAIN (その名前は存在しない)",
    4: "NOTIMP (未実装)",
    5: "REFUSED (拒否)",
}

# 問い合わせ ID。実際のリゾルバーは推測できない乱数を使う必要があるが
# (キャッシュポイズニング対策)、ここでは出力を再現できるようシードを固定する
rng = random.Random(1035)


class DNSError(Exception):
    """応答が解析できない場合などに送出する例外。"""


@dataclass
class Record:
    """リソースレコード 1 件。"""

    name: str
    rtype: int
    ttl: int
    data: str


def build_query(qid: int, name: str, qtype: int) -> bytes:
    """問い合わせメッセージのバイト列を組み立てる。"""
    # ヘッダー (12 バイト): ID、フラグ、各セクションのレコード数
    # フラグ 0x0100 は RD (Recursion Desired: 再帰的な解決を依頼) だけが 1
    header = struct.pack("!HHHHHH", qid, 0x0100, 1, 0, 0, 0)
    # 質問セクション: 名前をラベルに分け、「長さ + 文字列」を並べて 0 で終える
    qname = b""
    for label in name.rstrip(".").split("."):
        encoded = label.encode("ascii")
        if not 0 < len(encoded) <= 63:
            raise DNSError(f"ラベルの長さが不正です: {label!r}")
        qname += bytes([len(encoded)]) + encoded
    qname += b"\x00"
    return header + qname + struct.pack("!HH", qtype, CLASS_IN)


def read_name(msg: bytes, offset: int) -> tuple[str, int]:
    """offset から名前を読み、(名前, 名前の直後の位置) を返す。

    長さバイトの上位 2 ビットが 11 なら圧縮ポインタで、残りの 14 ビットが
    メッセージの先頭からの位置を表す。その位置に書かれた名前の続きを読む。
    """
    labels: list[str] = []
    end = -1  # 最初のポインタの直後の位置 (ポインタを含まない場合は -1)
    jumps = 0
    while True:
        if offset >= len(msg):
            raise DNSError("名前の途中でメッセージが終わっています")
        length = msg[offset]
        if length & 0xC0 == 0xC0:  # 圧縮ポインタ (2 バイト)
            if offset + 1 >= len(msg):
                raise DNSError("圧縮ポインタが途中で切れています")
            if end < 0:
                end = offset + 2
            offset = ((length & 0x3F) << 8) | msg[offset + 1]
            jumps += 1
            if jumps > 20:  # 不正な応答でループし続けないための防御
                raise DNSError("圧縮ポインタがループしています")
        elif length == 0:  # 名前の終わり
            offset += 1
            break
        else:  # 通常のラベル
            label = msg[offset + 1:offset + 1 + length]
            labels.append(label.decode("ascii", errors="replace"))
            offset += 1 + length
    name = ".".join(labels) + "."
    return name, (end if end >= 0 else offset)


def parse_rdata(msg: bytes, rtype: int, start: int, length: int) -> str:
    """レコードのデータ部分 (RDATA) を、種類に応じて文字列にする。"""
    rdata = msg[start:start + length]
    if rtype == TYPES["A"] and length == 4:
        return socket.inet_ntop(socket.AF_INET, rdata)
    if rtype == TYPES["AAAA"] and length == 16:
        return socket.inet_ntop(socket.AF_INET6, rdata)
    if rtype in (TYPES["CNAME"], TYPES["NS"]):
        return read_name(msg, start)[0]  # 名前は圧縮されていることがある
    if rtype == TYPES["MX"]:
        preference = struct.unpack("!H", rdata[:2])[0]
        return f"{preference} {read_name(msg, start + 2)[0]}"
    if rtype == TYPES["TXT"]:
        # 「長さ 1 バイト + 文字列」が 1 つ以上並ぶ
        texts: list[str] = []
        pos = 0
        while pos < len(rdata):
            n = rdata[pos]
            texts.append(rdata[pos + 1:pos + 1 + n].decode(errors="replace"))
            pos += 1 + n
        return " ".join(f'"{t}"' for t in texts)
    if rtype == TYPES["SOA"]:
        mname, pos = read_name(msg, start)
        rname, pos = read_name(msg, pos)
        serial, refresh, retry, expire, minimum = struct.unpack(
            "!IIIII", msg[pos:pos + 20]
        )
        return (f"{mname} {rname} serial={serial} refresh={refresh} "
                f"retry={retry} expire={expire} minimum={minimum}")
    return rdata.hex()  # 対応していない種類は 16 進数で表示する


def parse_response(msg: bytes, qid: int) -> tuple[int, list[Record]]:
    """応答を解析し、(フラグ, 回答セクションのレコード) を返す。"""
    if len(msg) < 12:
        raise DNSError("応答が短すぎます")
    rid, flags, qdcount, ancount, nscount, arcount = struct.unpack(
        "!HHHHHH", msg[:12]
    )
    if rid != qid:
        raise DNSError(f"ID が一致しません (送信 {qid}, 受信 {rid})")
    print(f"  ヘッダー: ID={rid} QR={flags >> 15} AA={(flags >> 10) & 1} "
          f"TC={(flags >> 9) & 1} RD={(flags >> 8) & 1} "
          f"RA={(flags >> 7) & 1}")
    print(f"  RCODE={flags & 0xF} {RCODES.get(flags & 0xF, '')}")
    print(f"  レコード数: 質問 {qdcount}, 回答 {ancount}, "
          f"権威 {nscount}, 追加 {arcount}")
    offset = 12
    for _ in range(qdcount):  # 質問セクションは読み飛ばす
        _, offset = read_name(msg, offset)
        offset += 4  # QTYPE と QCLASS
    records: list[Record] = []
    for _ in range(ancount):
        name, offset = read_name(msg, offset)
        rtype, _rclass, ttl, rdlength = struct.unpack(
            "!HHIH", msg[offset:offset + 10]
        )
        offset += 10
        data = parse_rdata(msg, rtype, offset, rdlength)
        records.append(Record(name, rtype, ttl, data))
        offset += rdlength
    return flags, records


def query(server: str, name: str, qtype: int) -> list[Record]:
    """server に UDP で問い合わせ、回答セクションのレコードを返す。"""
    qid = rng.randrange(0x10000)
    packet = build_query(qid, name, qtype)
    print(f"  問い合わせ ({len(packet)} バイト): {packet.hex(' ')}")
    family = socket.AF_INET6 if ":" in server else socket.AF_INET
    with socket.socket(family, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)
        sock.connect((server, 53))  # 他のアドレスからのデータグラムを無視する
        sock.send(packet)
        msg = sock.recv(4096)
    print(f"  応答 {len(msg)} バイトを受信しました")
    flags, records = parse_response(msg, qid)
    if (flags >> 9) & 1:
        print("  注意: 応答が切り詰められています (TC=1)。"
              "本来は TCP で問い合わせ直します。")
    return records


def show_getaddrinfo(name: str) -> None:
    """比較として、OS のリゾルバー (getaddrinfo) の結果を表示する。"""
    print(f"--- 比較: socket.getaddrinfo({name!r}) ---")
    try:
        infos = socket.getaddrinfo(name, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as e:
        print(f"  名前解決に失敗しました: {e}")
        return
    for family, _, _, _, sockaddr in infos:
        print(f"  {family.name:9s} {sockaddr[0]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="DNS に問い合わせる")
    parser.add_argument("name", nargs="?", default="www.python.org")
    parser.add_argument("-s", "--server", default="8.8.8.8",
                        help="問い合わせ先のフルリゾルバー")
    parser.add_argument("-t", "--type", action="append",
                        choices=sorted(TYPES), dest="types",
                        help="レコードの種類 (複数指定可。既定は A と AAAA)")
    args = parser.parse_args()
    types: list[str] = args.types or ["A", "AAAA"]

    for tname in types:
        print(f"=== {args.name} の {tname} レコードを "
              f"{args.server} に問い合わせ ===")
        try:
            records = query(args.server, args.name, TYPES[tname])
        except TimeoutError:
            print(f"  {TIMEOUT} 秒待っても応答がありませんでした。"
                  "インターネット接続や、UDP の 53 番ポートが"
                  "ファイアウォールで遮断されていないかを確認してください。")
            sys.exit(1)
        except (OSError, DNSError) as e:
            print(f"  問い合わせに失敗しました: {e}")
            sys.exit(1)
        if not records:
            print("  回答はありません")
        for r in records:
            rtype = TYPE_NAMES.get(r.rtype, str(r.rtype))
            print(f"  {r.name} TTL={r.ttl} {rtype} {r.data}")
        print()
    show_getaddrinfo(args.name)


if __name__ == "__main__":
    main()
