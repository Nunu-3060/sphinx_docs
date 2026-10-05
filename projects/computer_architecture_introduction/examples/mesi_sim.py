"""MESI プロトコルのシミュレーター。

複数のコア（2〜4 個）がそれぞれ私有キャッシュを持ち、共有バスでつながった
構成を考えます。読み書きの列を与えると、各コアのキャッシュラインの状態
（M/E/S/I）の遷移と、バスに出るトランザクションを表示します。
さらに、2 つのコアが同じキャッシュラインの別の変数に交互に書き込む
false sharing の場合と、別のラインに置いた場合とで無効化の回数を比べます。

実行方法: python mesi_sim.py
"""

LINE_SIZE = 64  # キャッシュラインの大きさ（バイト）

Access = tuple[int, str, int]  # （コア番号、"R" または "W"、アドレス）


class MesiSystem:
    """共有バスでつながったコアとキャッシュの集まり。"""

    def __init__(self, num_cores: int) -> None:
        self.num_cores = num_cores
        # caches[c][line] はコア c が持つライン line の状態。
        # 辞書にないラインは I（無効）とみなす。
        self.caches: list[dict[int, str]] = [{} for _ in range(num_cores)]
        self.invalidations = 0  # 他コアのラインを無効化した回数
        self.bus_count = 0  # バストランザクションの回数

    def state(self, core: int, line: int) -> str:
        return self.caches[core].get(line, "I")

    def access(self, core: int, op: str, addr: int) -> str:
        """1 回の読み書きを処理し、バスの動作を文字列で返す。"""
        line = addr // LINE_SIZE
        mine = self.state(core, line)
        others = [c for c in range(self.num_cores) if c != core]
        if op == "R":
            if mine != "I":
                return "hit"  # M、E、S ならバスを使わずに読める
            bus = "BusRd"
            holders = [c for c in others if self.state(c, line) != "I"]
            for c in holders:
                if self.state(c, line) == "M":
                    bus += f" + Flush(C{c})"  # 最新の値を書き戻して渡す
                self.caches[c][line] = "S"
            # ほかに持っているコアがなければ E、あれば S
            self.caches[core][line] = "S" if holders else "E"
        else:
            if mine in ("M", "E"):
                self.caches[core][line] = "M"  # E→M はバス不要
                return "hit"
            # S なら無効化だけを求める BusUpgr、I ならデータも読む BusRdX
            bus = "BusUpgr" if mine == "S" else "BusRdX"
            for c in others:
                other = self.state(c, line)
                if other == "M":
                    bus += f" + Flush(C{c})"
                if other != "I":
                    self.caches[c][line] = "I"
                    self.invalidations += 1
            self.caches[core][line] = "M"
        self.bus_count += 1
        return bus


def trace(num_cores: int, accesses: list[Access]) -> None:
    """読み書きの列を実行し、ライン 0 の状態の遷移を表として表示する。"""
    system = MesiSystem(num_cores)
    cores = " ".join(f"C{c}" for c in range(num_cores))
    print(f"手順 操作       バスの動作            {cores}")
    for step, (core, op, addr) in enumerate(accesses, start=1):
        bus = system.access(core, op, addr)
        states = "  ".join(
            system.state(c, addr // LINE_SIZE) for c in range(num_cores)
        )
        print(f"{step:>3}  C{core} {op} {addr:>4}  {bus:<20}  {states}")
    print(f"バストランザクション {system.bus_count} 回、"
          f"無効化 {system.invalidations} 回")


def ping_pong(addr0: int, addr1: int, rounds: int) -> MesiSystem:
    """コア 0 と 1 が交互に自分の変数を x += 1 する（読んでから書く）。"""
    system = MesiSystem(2)
    for _ in range(rounds):
        for core, addr in ((0, addr0), (1, addr1)):
            system.access(core, "R", addr)
            system.access(core, "W", addr)
    return system


def main() -> None:
    print("=== 3 コアでの状態遷移（アドレス 0〜63 はライン 0）===")
    accesses: list[Access] = [
        (0, "R", 0),   # C0 だけが持つので E
        (0, "W", 0),   # E→M（バス不要）
        (1, "R", 8),   # C0 が書き戻し、両方 S
        (2, "R", 16),  # 3 つとも S
        (2, "W", 16),  # C2 が BusUpgr で他を無効化
        (0, "R", 0),   # C2 が書き戻し
        (1, "W", 8),   # BusRdX で C0、C2 を無効化
        (1, "R", 8),   # M のままヒット
    ]
    trace(3, accesses)

    rounds = 1000
    print()
    print(f"=== false sharing の比較（各コアが {rounds} 回ずつ x += 1）===")
    for label, addr1 in (("同じライン（0 と 8）", 8),
                         ("別のライン（0 と 64）", 64)):
        s = ping_pong(0, addr1, rounds)
        print(f"{label}: バストランザクション {s.bus_count:>5} 回、"
              f"無効化 {s.invalidations:>5} 回")


if __name__ == "__main__":
    main()
