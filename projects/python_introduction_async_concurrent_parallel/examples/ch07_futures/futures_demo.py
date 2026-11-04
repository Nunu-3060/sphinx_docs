"""concurrent.futures の submit()、as_completed()、例外の扱いを確かめるサンプル。

引数に process を指定するとプロセスプールで、指定しないとスレッドプールで実行する。
Executor の種類を変えても、それ以外のコードは変更しなくてよい。

実行例:
    python futures_demo.py
    python futures_demo.py process
"""

import sys
import time
from concurrent.futures import Executor, Future, ProcessPoolExecutor, ThreadPoolExecutor, as_completed


def download(name: str, seconds: float) -> str:
    """ファイルのダウンロードを模擬する。name が broken のときは失敗する。"""
    time.sleep(seconds)
    if name == "broken":
        raise ValueError(f"{name} のダウンロードに失敗した")
    return f"{name} ({seconds} 秒)"


def create_executor(kind: str) -> Executor:
    if kind == "process":
        return ProcessPoolExecutor(max_workers=3)
    return ThreadPoolExecutor(max_workers=3)


def main() -> None:
    kind = sys.argv[1] if len(sys.argv) > 1 else "thread"
    jobs = {"a.txt": 1.5, "b.txt": 0.5, "broken": 1.0, "c.txt": 0.8}

    start = time.perf_counter()
    with create_executor(kind) as executor:
        futures: dict[Future[str], str] = {
            executor.submit(download, name, seconds): name for name, seconds in jobs.items()
        }
        # 投入した順ではなく、完了した順に結果を受け取る
        for future in as_completed(futures):
            name = futures[future]
            elapsed = time.perf_counter() - start
            try:
                result = future.result()
            except ValueError as error:
                print(f"{elapsed:4.1f} 秒: 失敗 {name}: {error}")
            else:
                print(f"{elapsed:4.1f} 秒: 完了 {result}")
    print(f"{kind} で実行した。合計 {time.perf_counter() - start:.1f} 秒")


if __name__ == "__main__":
    main()
