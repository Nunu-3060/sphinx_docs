"""5 段パイプラインのストール数とサイクル数を計算するサンプル。

命令列（宛先レジスタ、ソースレジスタ、ロード命令かどうか）を入力に、
フォワーディングなし／ありの 2 通りでデータハザードによるストール数、
総サイクル数、CPI を計算し、パイプライン図をテキストで表示します。
分岐命令（制御ハザード）は扱いません。

実行方法: python pipeline_sim.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Instr:
    """パイプラインに流す命令。"""

    text: str  # 表示用のアセンブリ
    dest: int  # 宛先レジスタ番号（書き込まない命令は 0）
    srcs: tuple[int, ...]  # ソースレジスタ番号
    is_load: bool = False  # ロード命令なら True


def ex_cycles(prog: list[Instr], forwarding: bool) -> list[int]:
    """各命令が EX 段を実行するサイクルを返す（1 番目の命令の IF が 1）。"""
    ex: list[int] = []
    for i, ins in enumerate(prog):
        # ハザードがなければ、前の命令の次のサイクルに EX を実行する
        t = 3 if i == 0 else ex[i - 1] + 1
        for j in range(i - 1, -1, -1):  # 直前の命令から順にさかのぼる
            p = prog[j]
            if p.dest == 0 or p.dest not in ins.srcs:
                continue
            if not forwarding:
                # 前半で WB、後半で ID の読み出しをするので、
                # 生産者の WB（EX + 2）と同じサイクルに ID ができる
                t = max(t, ex[j] + 3)
            elif p.is_load:
                # ロードの値は MEM の終わりにできる
                t = max(t, ex[j] + 2)
            else:
                # ALU の結果は EX の終わりにでき、次の EX へ送れる
                t = max(t, ex[j] + 1)
            break  # 最も近い生産者だけを見ればよい
        ex.append(t)
    return ex


def diagram(prog: list[Instr], ex: list[int]) -> list[list[str]]:
    """各命令の、サイクルごとの段の名前の表を作る。"""
    total = ex[-1] + 2  # 最後の命令が WB を終えるサイクル
    rows: list[list[str]] = []
    # ID に入るサイクル（前の命令が EX に進むサイクル）
    id_start = [2] + ex[:-1]
    for i in range(len(prog)):
        row = [""] * (total + 1)
        # 前の命令が ID を出るまでは IF にとどまる
        if_start = 1 if i == 0 else id_start[i - 1]
        for c in range(if_start, id_start[i]):
            row[c] = "IF"
        for c in range(id_start[i], ex[i]):
            row[c] = "ID"  # ストール中は ID にとどまる
        row[ex[i]] = "EX"
        row[ex[i] + 1] = "MEM"
        row[ex[i] + 2] = "WB"
        rows.append(row[1:])
    return rows


def report(title: str, prog: list[Instr], forwarding: bool) -> None:
    """パイプライン図とサイクル数、CPI を表示する。"""
    ex = ex_cycles(prog, forwarding)
    n = len(prog)
    total = ex[-1] + 2
    stalls = total - (n + 4)  # 理想は n + 4 サイクル
    fw = "あり" if forwarding else "なし"
    print(f"--- {title}（フォワーディング{fw}）---")
    header = "".join(f"{c:>4}" for c in range(1, total + 1))
    print(f"{'命令':<18}{header}")
    for ins, row in zip(prog, diagram(prog, ex)):
        cells = "".join(f"{s:>4}" for s in row)
        # 命令は ASCII 文字だけなので、文字数で桁がそろう
        print(f"{ins.text:<20}{cells}".rstrip())
    cpi = (n + stalls) / n
    print(f"命令数 {n}, ストール {stalls}, 総サイクル {total}, "
          f"CPI {cpi:.2f}（パイプラインを満たす 4 サイクルを除く）")
    print()


def main() -> None:
    """ロード使用ハザードを含む命令列と、並べ替えた命令列を比べる。"""
    original = [
        Instr("lw   x1, 0(x10)", 1, (10,), is_load=True),
        Instr("add  x2, x1, x3", 2, (1, 3)),
        Instr("sub  x4, x2, x5", 4, (2, 5)),
        Instr("sw   x4, 4(x10)", 0, (4, 10)),
        Instr("lw   x6, 8(x10)", 6, (10,), is_load=True),
        Instr("add  x7, x6, x8", 7, (6, 8)),
    ]
    # 2 つ目のロードを前に移し、ロードの直後に使わないようにする
    reordered = [original[0], original[4], original[1],
                 original[2], original[3], original[5]]
    for forwarding in (False, True):
        report("元の命令列", original, forwarding)
    report("並べ替えた命令列", reordered, True)


if __name__ == "__main__":
    main()
