"""Tomasulo のアルゴリズムを簡略化したシミュレーター。

浮動小数点数の命令列を、リザベーションステーションと共通データバス
（CDB）を持つプロセッサで実行したときに、各命令が発行・実行開始・
実行完了・結果の書き込みをするサイクルを表にして表示します。

簡略化の前提:

* 1 サイクルに 1 命令をプログラム順に発行する。発行には同じ種類の
  リザベーションステーションの空きが必要。
* オペランドがそろった次のサイクルから実行を始める。
* 実行完了の次のサイクルに CDB へ結果を書き込む。CDB は 1 サイクルに
  1 つだけで、競合したら古い命令を優先する。
* リザベーションステーションは書き込みのサイクルに解放され、次の
  サイクルから再利用できる。リオーダーバッファは持たない。

実行方法: python tomasulo_sim.py
"""

from dataclasses import dataclass

LATENCY = {"load": 2, "add": 2, "mul": 10, "div": 40}  # 実行サイクル数
STATIONS = {"load": 2, "add": 3, "mul": 2}  # リザベーションステーション数
UNIT = {"load": "load", "add": "add", "mul": "mul", "div": "mul"}


@dataclass
class Instr:
    """命令と、各段のサイクル（未実行なら 0）。"""

    text: str
    op: str  # "load", "add", "mul", "div" のいずれか
    dest: str
    srcs: tuple[str, ...]
    issue: int = 0
    start: int = 0
    end: int = 0
    write: int = 0
    waits: tuple[int, ...] = ()  # 待っている命令の番号（タグ）


def simulate(prog: list[Instr]) -> None:
    """命令列 prog を実行し、各命令のサイクルを記録する。"""
    reg_tag: dict[str, int] = {}  # レジスタ -> 値を生産する命令の番号
    next_issue = 0
    cycle = 0
    while any(ins.write == 0 for ins in prog):
        cycle += 1
        # (1) 書き込み: 実行を終えた命令のうち最も古いものが CDB を使う
        done = [i for i, ins in enumerate(prog)
                if ins.end and ins.end < cycle and not ins.write]
        if done:
            i = done[0]
            prog[i].write = cycle
            if reg_tag.get(prog[i].dest) == i:
                del reg_tag[prog[i].dest]  # レジスタに最新の値が入った
        # (2) 実行開始: 待っている値がすべて前のサイクルまでに CDB に
        #     流れた命令は、実行を始める
        for ins in prog:
            if ins.issue and not ins.start and ins.issue < cycle and all(
                    0 < prog[t].write < cycle for t in ins.waits):
                ins.start = cycle
                ins.end = cycle + LATENCY[ins.op] - 1
        # (3) 発行: 同じ種類のステーションに空きがあれば次の命令を発行する
        if next_issue < len(prog):
            ins = prog[next_issue]
            unit = UNIT[ins.op]
            busy = sum(1 for p in prog if p.issue and UNIT[p.op] == unit
                       and not 0 < p.write < cycle)
            if busy < STATIONS[unit]:
                ins.issue = cycle
                # ソースが未完了の命令の結果なら、値の代わりにタグを覚える
                ins.waits = tuple(reg_tag[s] for s in ins.srcs
                                  if s in reg_tag)
                reg_tag[ins.dest] = next_issue  # 宛先をリネームする
                next_issue += 1


def main() -> None:
    """浮動小数点数の命令列を実行し、各命令のサイクルを表示する。"""
    prog = [
        Instr("fld    f6, 32(x2)", "load", "f6", ()),
        Instr("fld    f2, 48(x3)", "load", "f2", ()),
        Instr("fmul.d f0, f2, f4", "mul", "f0", ("f2", "f4")),
        Instr("fsub.d f8, f6, f2", "add", "f8", ("f6", "f2")),
        Instr("fdiv.d f10, f0, f6", "div", "f10", ("f0", "f6")),
        Instr("fadd.d f6, f8, f2", "add", "f6", ("f8", "f2")),
    ]
    simulate(prog)
    print("命令                  発行  実行開始  実行完了  書き込み  待つ命令")
    for ins in prog:
        waits = ", ".join(str(t + 1) for t in ins.waits) or "-"
        print(f"{ins.text:<20}{ins.issue:>6}{ins.start:>10}{ins.end:>10}"
              f"{ins.write:>10}  {waits}")


if __name__ == "__main__":
    main()
