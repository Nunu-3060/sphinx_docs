"""冪等キーの有無で再試行の結果がどう変わるかを比べるサンプル。

要求または応答が一定の確率で失われる不安定な通信を、乱数の
シードを固定して模擬する。クライアントは応答が返らなければ
指数バックオフとジッタで待ってから再試行する（待ち時間は
実際には待たず、合計だけを計算する）。決済サーバが冪等キーを
使わない場合と使う場合で、同じ注文が何回課金されるかを比べる。

実行方法: python ch12_idempotent_retry.py
関連する章: 第 12 章「分散システム」
"""

import random

LOSS_RATE = 0.3     # 要求・応答のそれぞれが失われる確率
MAX_ATTEMPTS = 4    # 1 つの注文に対する最大の試行回数
BASE_MS = 100.0     # バックオフの基準の待ち時間（ミリ秒）
SEED = 8
ORDERS = ["A", "B", "C", "D", "E", "F"]


class PaymentServer:
    """課金を行うサーバ。use_key が真なら冪等キーで重複を防ぐ。"""

    def __init__(self, use_key: bool) -> None:
        self.use_key = use_key
        self.charges: list[str] = []      # 実際に行った課金（注文名）
        self.done: dict[str, int] = {}    # 冪等キー -> 課金番号

    def handle(self, key: str, order: str) -> int:
        """課金要求を処理し、課金番号を返す。"""
        if self.use_key and key in self.done:
            return self.done[key]  # 処理済み: 前回の結果を返すだけ
        self.charges.append(order)
        charge_id = len(self.charges)
        if self.use_key:
            self.done[key] = charge_id
        return charge_id


def call_with_retry(server: PaymentServer, rng: random.Random,
                    order: str) -> tuple[int, bool, float]:
    """1 つの注文を再試行付きで送る。

    戻り値は (試行回数, 応答を受け取れたか, 待ち時間の合計)。
    冪等キーは注文ごとに 1 つ作り、再試行でも同じものを使う。
    """
    key = f"order-{order}"
    waited = 0.0
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if attempt > 1:
            # 指数バックオフ + フルジッタ: n 回目の前に [0, BASE * 2^(n-2)) 待つ
            waited += rng.uniform(0.0, BASE_MS * 2 ** (attempt - 2))
        if rng.random() < LOSS_RATE:
            continue  # 要求が失われた: サーバは何もしていない
        server.handle(key, order)
        if rng.random() < LOSS_RATE:
            continue  # 応答が失われた: 処理は済んだがクライアントは知らない
        return attempt, True, waited
    return MAX_ATTEMPTS, False, waited


def simulate(use_key: bool) -> None:
    """すべての注文を送り、注文ごとの課金回数を表示する。"""
    rng = random.Random(SEED)  # 両方の実験で同じ通信の失敗を再現する
    server = PaymentServer(use_key)
    print(f"== 冪等キー: {'あり' if use_key else 'なし'} ==")
    for order in ORDERS:
        attempts, ok, waited = call_with_retry(server, rng, order)
        result = "成功" if ok else "失敗（結果不明）"
        count = server.charges.count(order)
        print(f"注文 {order}: 試行 {attempts} 回, {result}, "
              f"課金 {count} 回, 待ち {waited:.0f} ms")
    doubled = sum(1 for o in ORDERS if server.charges.count(o) > 1)
    print(f"課金の合計 {len(server.charges)} 回"
          f"（注文 {len(ORDERS)} 件, 二重課金 {doubled} 件）")


def main() -> None:
    """冪等キーなし・ありの 2 通りを実行する。"""
    simulate(use_key=False)
    simulate(use_key=True)


if __name__ == "__main__":
    main()
