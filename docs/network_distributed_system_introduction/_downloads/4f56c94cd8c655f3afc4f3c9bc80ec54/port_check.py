"""タイムアウト付きの connect() で、host:port に接続できるかを調べる。

結果を次の 4 種類に分けて表示します。

* 成功：TCP の 3 ウェイハンドシェイクが完了した
* 接続拒否：相手のホストには届いたが、そのポートで待ち受けている
  プログラムがない（RST が返ってきた）
* タイムアウト：決めた時間内に応答がない（ファイアウォールでの破棄、
  経路の問題、相手のホストの停止など）
* 名前解決失敗：ホスト名から IP アドレスを得られない

使い方::

    # デモ：localhost に一時的なサーバーを立て、開いているポートと
    # 閉じているポート、存在しないホスト名を調べる
    python port_check.py

    # 指定したホストとポートを調べる（ポートは複数指定できる）
    python port_check.py example.com 80 443
    python port_check.py 192.0.2.1 80 --timeout 2

デモは localhost だけで完結します。引数で外部のホストを指定した場合は、
そのホストに届くネットワークが必要です。
"""

import argparse
import socket
import time

DEFAULT_TIMEOUT = 3.0


def check(host: str, port: int, timeout: float) -> str:
    """host:port への TCP 接続を試み、結果を表す文字列を返します。"""
    # 1. 名前解決。失敗した場合は、接続を試みる以前の問題と分かる
    try:
        infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    except socket.gaierror as e:
        return f"名前解決失敗（{e.strerror}）"

    # 2. 得られたアドレスに順に接続を試みる（IPv6 と IPv4 の両方など）
    result = "失敗"
    for family, socktype, proto, _, addr in infos:
        with socket.socket(family, socktype, proto) as sock:
            sock.settimeout(timeout)
            try:
                sock.connect(addr)
            except ConnectionRefusedError:
                result = f"接続拒否（{addr[0]}）"
            except TimeoutError:
                result = f"タイムアウト（{addr[0]}、{timeout} 秒）"
            except OSError as e:
                # 経路がない、ネットワークに到達できない、など
                result = f"エラー（{addr[0]}：{e.strerror}）"
            else:
                return f"成功（{addr[0]}）"
    return result


def check_and_print(host: str, port: int, timeout: float) -> None:
    start = time.monotonic()
    result = check(host, port, timeout)
    elapsed = time.monotonic() - start
    print(f"{host}:{port} -> {result}  [{elapsed:.1f} 秒]")


def demo(timeout: float) -> None:
    """localhost に一時的なサーバーを立てて、各種の結果を確かめます。"""
    # 開いているポート：ポート番号 0 で空いている番号を OS に選ばせる
    with socket.create_server(("127.0.0.1", 0)) as server:
        open_port = server.getsockname()[1]
        # 閉じているポート：一度 bind して番号を得てから閉じる
        with socket.socket() as tmp:
            tmp.bind(("127.0.0.1", 0))
            closed_port = tmp.getsockname()[1]
        print(f"一時サーバーを 127.0.0.1:{open_port} で起動しました")
        check_and_print("127.0.0.1", open_port, timeout)
        check_and_print("127.0.0.1", closed_port, timeout)
    # .invalid は、存在しないことが保証されたトップレベルドメイン
    check_and_print("no-such-host.invalid", 80, timeout)


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP ポートの疎通確認")
    parser.add_argument("host", nargs="?", help="調べるホスト")
    parser.add_argument("ports", nargs="*", type=int, help="ポート番号")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                        help="接続を待つ秒数")
    args = parser.parse_args()
    if args.host is None:
        demo(args.timeout)
        return
    for port in args.ports or [80]:
        check_and_print(args.host, port, args.timeout)


if __name__ == "__main__":
    main()
