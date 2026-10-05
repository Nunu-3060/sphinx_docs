"""リーダーレスなキー・バリューストアのクォーラム読み書きの模擬.

N 個のレプリカを持つリーダーレスなキー・バリューストアを模擬し、
(N, W, R) の組み合わせによって、最新の値が読めるかどうかが
どう変わるかを示します。

* 各レプリカは、キーごとに (バージョン, 値) を保持します。
* 書き込みは、W 個のレプリカが受け付けた時点で成功とします。
  このサンプルでは最悪の場合を考え、残りのレプリカには
  書き込みが届かなかったものとします。
* 読み込みは、R 個のレプリカから応答を得て、そのうち
  バージョンが最大の値を返します。古い値を返したレプリカには、
  最新の値を書き戻します（読み込み修復）。
* どのレプリカが先に応答するかは乱数で決めます（シード固定）。

バージョンは単純な整数としています。実際のシステムでは、
タイムスタンプやバージョンベクトルなどが使われます。

実行方法:
    python quorum_sim.py
"""

import random
from dataclasses import dataclass, field
from math import comb

Versioned = tuple[int, str]  # (バージョン, 値)


@dataclass
class Replica:
    name: str
    up: bool = True
    data: dict[str, Versioned] = field(default_factory=dict)

    def get(self, key: str) -> Versioned:
        return self.data.get(key, (0, "(なし)"))

    def put(self, key: str, item: Versioned) -> None:
        # 手元より新しいバージョンのときだけ上書きする
        if item[0] > self.get(key)[0]:
            self.data[key] = item


class QuorumError(Exception):
    """応答したレプリカがクォーラムに満たない."""


@dataclass
class Cluster:
    n: int
    w: int
    r: int
    rng: random.Random
    replicas: list[Replica] = field(init=False)

    def __post_init__(self) -> None:
        self.replicas = [Replica(chr(ord("A") + i)) for i in range(self.n)]

    def responders(self, count: int) -> list[Replica]:
        """稼働中のレプリカから、先に応答する count 個を選ぶ."""
        alive = [rep for rep in self.replicas if rep.up]
        if len(alive) < count:
            raise QuorumError(
                f"稼働中のレプリカが {len(alive)} 個で、{count} 個に足りない"
            )
        return self.rng.sample(alive, count)

    def write(self, key: str, item: Versioned) -> list[str]:
        targets = self.responders(self.w)
        for rep in targets:
            rep.put(key, item)
        return sorted(rep.name for rep in targets)

    def read(self, key: str, verbose: bool = False) -> Versioned:
        targets = self.responders(self.r)
        answers = [(rep, rep.get(key)) for rep in targets]
        latest = max(item for _, item in answers)
        for rep, item in sorted(answers, key=lambda a: a[0].name):
            if verbose:
                print(f"    {rep.name} の応答: v{item[0]} {item[1]}")
            if item[0] < latest[0]:
                rep.put(key, latest)  # 読み込み修復
                if verbose:
                    print(f"    -> {rep.name} に v{latest[0]} を書き戻す"
                          "（読み込み修復）")
        return latest

    def show(self, key: str) -> str:
        parts = []
        for rep in self.replicas:
            ver, val = rep.get(key)
            mark = "" if rep.up else "(停止)"
            parts.append(f"{rep.name}=v{ver}:{val}{mark}")
        return "  ".join(parts)


def trace(n: int, w: int, r: int, seed: int, down: str) -> None:
    """1 回分の書き込みと読み込みの経過を表示する."""
    cond = "R+W>N" if r + w > n else "R+W<=N"
    print(f"--- N={n}, W={w}, R={r} ({cond}) ---")
    cluster = Cluster(n, w, r, random.Random(seed))
    for rep in cluster.replicas:  # 初期状態：全レプリカが v1 を持つ
        rep.put("x", (1, "old"))
    for rep in cluster.replicas:
        rep.up = rep.name not in down
    print(f"  初期状態     : {cluster.show('x')}")
    written = cluster.write("x", (2, "new"))
    print(f"  書き込み v2  : {', '.join(written)} が受け付けて成功")
    for rep in cluster.replicas:  # 停止していたレプリカが復帰する
        rep.up = True
    print(f"  書き込み後   : {cluster.show('x')}")
    print("  読み込み:")
    ver, val = cluster.read("x", verbose=True)
    result = "最新" if ver == 2 else "古い値"
    print(f"  読み込み結果 : v{ver} {val} ({result})")
    print(f"  読み込み後   : {cluster.show('x')}")
    print()


def stale_rate(n: int, w: int, r: int, trials: int, seed: int) -> float:
    """古い値を読む割合を、試行を繰り返して求める."""
    rng = random.Random(seed)
    stale = 0
    for _ in range(trials):
        cluster = Cluster(n, w, r, rng)
        for rep in cluster.replicas:
            rep.put("x", (1, "old"))
        cluster.write("x", (2, "new"))
        if cluster.read("x")[0] < 2:
            stale += 1
    return stale / trials


def summary_table() -> None:
    print("=== (N, W, R) ごとの比較（試行 10000 回）===")
    print(" N  W  R  R+W>N  古い値を読む割合(実測/理論)  "
          "停止できる数(書込/読込)")
    combos = [(3, 1, 1), (3, 2, 1), (3, 2, 2), (3, 3, 1), (3, 1, 3),
              (5, 2, 2), (5, 3, 3), (5, 4, 2)]
    for n, w, r in combos:
        measured = stale_rate(n, w, r, 10000, seed=n * 100 + w * 10 + r)
        # R 個すべてが、書き込みの届かなかった N - W 個から選ばれる確率
        theory = comb(n - w, r) / comb(n, r)
        ok = "yes" if r + w > n else "no "
        print(f" {n}  {w}  {r}   {ok}      "
              f"{measured:6.1%} / {theory:6.1%}"
              f"            {n - w} / {n - r}")


def main() -> None:
    print("=== 個別の例（最初は全レプリカが v1 を持つ）===")
    # C が停止中に書き込み、復帰後に読む
    trace(3, 2, 2, seed=3, down="C")
    # R + W <= N では古い値を読むことがある
    trace(3, 1, 1, seed=5, down="")
    # 稼働中のレプリカが W に満たないと、書き込みは失敗する
    print("--- N=3, W=3, R=1 で C が停止中 ---")
    cluster = Cluster(3, 3, 1, random.Random(0))
    cluster.replicas[2].up = False
    try:
        cluster.write("x", (1, "new"))
    except QuorumError as exc:
        print(f"  書き込み失敗: {exc}")
    print()
    summary_table()


if __name__ == "__main__":
    main()
