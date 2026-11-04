"""多数の URL からデータを取得するケーススタディ（asyncio）。

ローカルに簡単な HTTP サーバーを起動し、asyncio のストリームで書いた HTTP クライアントから多数のリクエストを送る。
次の 3 点を組み合わせている。

* asyncio.Semaphore で同時に送るリクエストの数を制限する
* asyncio.timeout() で 1 件ごとの待ち時間に上限を設ける
* 失敗したリクエストは例外として記録し、他のリクエストは続行する
"""

import asyncio
import json
import time
from dataclasses import dataclass

HOST = "127.0.0.1"
REQUESTS = 40
CONCURRENCY = 10
TIMEOUT_SECONDS = 1.0


# ---- サーバー側（取得先の Web API の代わり） ----

def response_delay(item_id: int) -> float:
    """id ごとに応答までの時間を変える。10 件に 1 件は TIMEOUT_SECONDS より遅い。"""
    if item_id % 10 == 9:
        return 2.0
    return (item_id % 5) * 0.1


async def handle_http(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    try:
        request_line = (await reader.readline()).decode()
        while (await reader.readline()) not in (b"\r\n", b""):
            pass  # ヘッダーは読み飛ばす
        path = request_line.split()[1]  # 例: "GET /items/3 HTTP/1.1"
        item_id = int(path.rsplit("/", 1)[1])
        await asyncio.sleep(response_delay(item_id))
        body = json.dumps({"id": item_id, "value": item_id * item_id}).encode()
        header = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n"
        writer.write(header.encode() + body)
        await writer.drain()
    except ConnectionError:
        pass  # クライアントがタイムアウトで切断した場合など
    finally:
        writer.close()


# ---- クライアント側 ----

@dataclass
class Result:
    item_id: int
    value: int | None = None
    error: str | None = None


async def http_get_json(port: int, path: str) -> dict[str, int]:
    """HTTP/1.1 の GET リクエストを送り、JSON の本文を辞書として返す。"""
    reader, writer = await asyncio.open_connection(HOST, port)
    try:
        writer.write(f"GET {path} HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n".encode())
        await writer.drain()
        response = await reader.read()  # Connection: close なので、サーバーが閉じるまで読む
    finally:
        writer.close()
        await writer.wait_closed()
    _, body = response.split(b"\r\n\r\n", 1)
    data: dict[str, int] = json.loads(body)
    return data


async def fetch(item_id: int, port: int, semaphore: asyncio.Semaphore) -> Result:
    async with semaphore:
        try:
            async with asyncio.timeout(TIMEOUT_SECONDS):
                data = await http_get_json(port, f"/items/{item_id}")
        except TimeoutError:
            return Result(item_id, error="タイムアウト")
        except (ConnectionError, ValueError) as error:
            return Result(item_id, error=repr(error))
    return Result(item_id, value=data["value"])


async def main() -> None:
    server = await asyncio.start_server(handle_http, HOST, 0)
    port = server.sockets[0].getsockname()[1]
    async with server:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        start = time.perf_counter()
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(fetch(i, port, semaphore)) for i in range(REQUESTS)]
        elapsed = time.perf_counter() - start

    results = [task.result() for task in tasks]
    succeeded = [r for r in results if r.error is None]
    failed = [r for r in results if r.error is not None]
    sequential = sum(min(response_delay(i), TIMEOUT_SECONDS) for i in range(REQUESTS))

    print(f"成功: {len(succeeded)} 件, 失敗: {len(failed)} 件")
    for result in failed:
        print(f"  id={result.item_id}: {result.error}")
    print(f"経過時間: {elapsed:.1f} 秒（1 件ずつ取得した場合の待ち時間の合計: {sequential:.1f} 秒）")


if __name__ == "__main__":
    asyncio.run(main())
