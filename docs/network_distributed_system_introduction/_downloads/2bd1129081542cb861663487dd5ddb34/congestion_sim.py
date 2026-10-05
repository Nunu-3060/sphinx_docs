"""TCP の輻輳制御（スロースタートと輻輳回避）を模擬するサンプル。

輻輳ウィンドウ（cwnd）の大きさを、RTT ごとに計算して表示します。
単位は MSS（1 セグメントの大きさ）です。TCP Reno の考え方に沿った、
次の単純なモデルを使います。

* スロースタート: cwnd < ssthresh の間、RTT ごとに cwnd を 2 倍にする
* 輻輳回避: cwnd >= ssthresh になったら、RTT ごとに cwnd を 1 増やす
* 重複 ACK による損失の検出: ssthresh = cwnd / 2、cwnd = ssthresh
  （高速再送・高速リカバリー）
* 再送タイムアウト: ssthresh = cwnd / 2、cwnd = 1（スロースタートから）

損失が起きる RTT はあらかじめ決めてあるので、実行結果は毎回同じです。

実行方法:
    python congestion_sim.py
"""

import unicodedata
from enum import Enum


class Event(Enum):
    """その RTT で起きる損失の種類。"""

    DUP_ACK = "重複 ACK"
    TIMEOUT = "タイムアウト"


# 損失が起きる RTT の番号と、その種類
LOSSES = {11: Event.DUP_ACK, 19: Event.TIMEOUT}
ROUNDS = 26  # 模擬する RTT の数
INITIAL_SSTHRESH = 16


def simulate() -> list[tuple[int, int, int, str]]:
    """RTT ごとの (番号, cwnd, ssthresh, 説明) のリストを返す。"""
    cwnd = 1
    ssthresh = INITIAL_SSTHRESH
    history: list[tuple[int, int, int, str]] = []
    for rtt in range(1, ROUNDS + 1):
        phase = "スロースタート" if cwnd < ssthresh else "輻輳回避"
        event = LOSSES.get(rtt)
        if event is not None:
            # この RTT で送ったセグメントの一部が失われた
            history.append((rtt, cwnd, ssthresh, f"損失（{event.value}）"))
            ssthresh = max(cwnd // 2, 2)
            cwnd = ssthresh if event is Event.DUP_ACK else 1
            continue
        history.append((rtt, cwnd, ssthresh, phase))
        if cwnd < ssthresh:
            cwnd = min(cwnd * 2, ssthresh)  # 指数的に増やす
        else:
            cwnd += 1  # 線形に増やす（加算的増加）
    return history


def pad(text: str, width: int) -> str:
    """全角文字を幅 2 として数え、表示幅が width になるよう空白を足す。"""
    used = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1
               for c in text)
    return text + " " * max(width - used, 0)


def main() -> None:
    print("RTT  cwnd  ssthresh  " + pad("状態", 22) + "cwnd のグラフ")
    for rtt, cwnd, ssthresh, note in simulate():
        bar = "#" * cwnd  # cwnd の大きさを # の数で表す
        print(f"{rtt:>3}  {cwnd:>4}  {ssthresh:>8}  {pad(note, 22)}{bar}")


if __name__ == "__main__":
    main()
