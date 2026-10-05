"""RV32I のサブセットを実行する命令セットシミュレーター。

アセンブリをラベル解決して読み込み、1 命令ずつ実行して、レジスタの変化と
実行命令数を表示します。実行方法: python riscv_sim.py
"""

from collections import Counter

# ABI 名からレジスタ番号への対応（x0〜x31 の名前でも書ける）
ABI = ("zero ra sp gp tp t0 t1 t2 s0 s1 a0 a1 a2 a3 a4 a5 a6 a7 "
       "s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 t3 t4 t5 t6").split()
REGS = {name: i for i, name in enumerate(ABI)}
REGS.update({f"x{i}": i for i in range(32)})

# 擬似命令を実際の命令に置き換える規則
PSEUDO = {"li": "addi {0}, zero, {1}", "mv": "addi {0}, {1}, 0",
          "j": "jal zero, {0}", "ret": "jalr zero, 0(ra)"}

Instr = tuple[str, list[str]]


def assemble(source: str) -> tuple[list[Instr], dict[str, int]]:
    """アセンブリを命令のリストとラベル表（ラベル→アドレス）に変換する。"""
    program: list[Instr] = []
    labels: dict[str, int] = {}
    for line in source.splitlines():
        text = line.split("#")[0].strip()  # コメントを除く
        if text.endswith(":"):
            labels[text[:-1]] = 4 * len(program)  # 命令は 4 バイトずつ並ぶ
            continue
        if not text:
            continue
        op, _, rest = text.partition(" ")
        args = [a.strip() for a in rest.split(",") if a.strip()]
        if op in PSEUDO:
            op, _, rest = PSEUDO[op].format(*args).partition(" ")
            args = [a.strip() for a in rest.split(",")]
        program.append((op, args))
    return program, labels


def to_signed(value: int) -> int:
    """値を 32 ビットの 2 の補数として解釈し直す。"""
    value &= 0xFFFFFFFF
    return value - (1 << 32) if value & 0x80000000 else value


class CPU:
    """32 本のレジスタ、PC、ワード単位のメモリを持つ簡単な CPU。"""

    def __init__(self, program: list[Instr], labels: dict[str, int]) -> None:
        self.program = program
        self.labels = labels
        self.x, self.pc = [0] * 32, 0  # 汎用レジスタとプログラムカウンタ
        self.mem: dict[int, int] = {}
        self.count: Counter[str] = Counter()

    def mem_addr(self, operand: str) -> int:
        """「imm(rs1)」形式のオペランドから実効アドレスを求める。"""
        imm, base = operand.rstrip(")").split("(")
        addr = self.x[REGS[base]] + int(imm, 0)
        assert addr % 4 == 0, "ワード境界にそろっていないアクセス"
        return addr

    def step(self) -> str:
        """PC が指す命令を 1 つ実行し、変化の説明を返す。"""
        op, a = self.program[self.pc // 4]
        self.count[op] += 1
        x, next_pc = self.x, self.pc + 4
        rd = REGS[a[0]]
        value: int | None = None  # rd に書き込む値
        if op in ("add", "sub", "and", "or"):
            r1, r2 = x[REGS[a[1]]], x[REGS[a[2]]]
            value = {"add": r1 + r2, "sub": r1 - r2,
                     "and": r1 & r2, "or": r1 | r2}[op]
        elif op in ("addi", "slli"):
            r1, imm = x[REGS[a[1]]], int(a[2], 0)
            value = r1 + imm if op == "addi" else r1 << imm
        elif op == "lw":
            value = self.mem.get(self.mem_addr(a[1]), 0)
        elif op == "sw":
            self.mem[self.mem_addr(a[1])] = x[rd]
        elif op in ("beq", "bne", "blt"):
            r1, r2 = x[rd], x[REGS[a[1]]]
            if {"beq": r1 == r2, "bne": r1 != r2, "blt": r1 < r2}[op]:
                next_pc = self.labels[a[2]]
        elif op == "jal":
            value, next_pc = self.pc + 4, self.labels[a[1]]
        elif op == "jalr":
            value, next_pc = self.pc + 4, self.mem_addr(a[1])
        else:
            raise ValueError(f"未対応の命令: {op}")
        text = f"{self.pc:04x}: {op:<5}{', '.join(a):<18}"
        if value is not None and rd != 0:  # x0 への書き込みは捨てる
            x[rd] = to_signed(value)
            text += f"{a[0]} = {x[rd]}"
        self.pc = next_pc
        return text

    def run(self, trace: int = 0) -> None:
        """PC がプログラムの外に出るまで実行する（最初の trace 命令を表示）。"""
        while 0 <= self.pc < 4 * len(self.program):
            text = self.step()
            if self.count.total() <= trace:
                print("  " + text.rstrip())
        print(f"  実行命令数: {self.count.total()}"
              f"（静的な命令数: {len(self.program)}）")
        print("  命令ごとの内訳:", dict(self.count))
        print(f"  結果: a0 = {self.x[REGS['a0']]}")


SUM_1_TO_10 = """
    li   a0, 0          # a0 = 合計
    li   t0, 1          # t0 = i
    li   t1, 11         # t1 = 上限
loop:
    add  a0, a0, t0     # 合計 += i
    addi t0, t0, 1      # i += 1
    blt  t0, t1, loop   # i < 11 なら繰り返す
"""

ARRAY_SUM = """
main:
    li   a0, 256        # 第 1 引数: 配列の先頭アドレス
    li   a1, 5          # 第 2 引数: 要素数
    jal  ra, sum        # sum(a0, a1) を呼ぶ
    sw   a0, 276(zero)  # 戻り値を配列の直後に格納する
    j    end
sum:
    li   t0, 0          # t0 = 合計
    slli t2, a1, 2      # t2 = 要素数 * 4
    add  t2, a0, t2     # t2 = 配列の末尾の次のアドレス
loop:
    beq  a0, t2, done   # 末尾に達したら終了
    lw   t1, 0(a0)      # t1 = 配列の要素
    add  t0, t0, t1
    addi a0, a0, 4      # 次の要素へ
    j    loop
done:
    mv   a0, t0         # 戻り値は a0 に入れる
    ret
end:
"""


def main() -> None:
    """2 つの例題プログラムを実行する。"""
    print("例題 1: 1 から 10 までの和（最初の 8 命令をトレース）")
    cpu = CPU(*assemble(SUM_1_TO_10))
    cpu.run(trace=8)
    print("例題 2: 配列の合計を関数で求める")
    cpu = CPU(*assemble(ARRAY_SUM))
    for i, v in enumerate([3, -1, 4, 1, 5]):  # 配列をメモリに置く
        cpu.mem[256 + 4 * i] = v
    cpu.run()
    print(f"  メモリ[276] = {cpu.mem[276]}")


if __name__ == "__main__":
    main()
