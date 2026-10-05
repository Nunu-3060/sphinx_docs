"""デッドロックを再現し、ロックの取得順序をそろえて回避するサンプル。

2 つのスレッドが 2 つのロック A と B を使います。

* 順序がばらばらの場合: スレッド 1 は A → B、スレッド 2 は B → A の
  順に取得しようとするので、互いに相手のロックを待ち続けます。
* 順序をそろえた場合: どちらのスレッドも A → B の順に取得するので、
  デッドロックは起きません。

プログラムが止まったままにならないよう、2 つ目のロックの取得には
タイムアウトを設定し、タイムアウトしたらデッドロックと判定します。

実行方法::

    python deadlock.py
"""

import threading
import time

TIMEOUT = 1.0  # 2 つ目のロックを待つ最大時間 (秒)


def worker(
    name: str,
    first: threading.Lock,
    second: threading.Lock,
    results: dict[str, bool],
) -> None:
    """first → second の順にロックを取得して作業する。"""
    with first:
        # 相手のスレッドが 1 つ目のロックを取るまで少し待ち、
        # デッドロックが起きやすい状況を作る
        time.sleep(0.1)
        acquired = second.acquire(timeout=TIMEOUT)
        if acquired:
            time.sleep(0.01)  # 2 つのロックを使った作業の代わり
            second.release()
        results[name] = acquired


def run(same_order: bool) -> dict[str, bool]:
    """2 つのスレッドを実行し、各スレッドが作業を完了できたかを返す。"""
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    if same_order:
        orders = [(lock_a, lock_b), (lock_a, lock_b)]
    else:
        orders = [(lock_a, lock_b), (lock_b, lock_a)]
    results: dict[str, bool] = {}
    threads = [
        threading.Thread(
            target=worker,
            args=(f"スレッド {i + 1}", first, second, results),
        )
        for i, (first, second) in enumerate(orders)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


def main() -> None:
    for same_order in (False, True):
        label = "順序をそろえた場合" if same_order else "順序がばらばらの場合"
        print(f"{label}:")
        for name, ok in sorted(run(same_order).items()):
            status = "完了" if ok else "タイムアウト (デッドロック)"
            print(f"  {name}: {status}")


if __name__ == "__main__":
    main()
