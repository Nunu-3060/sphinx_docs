"""数個の命令を持つ簡易 CPU のエミュレータ。

レジスタ 4 個（r0〜r3）、プログラムカウンタ、ゼロフラグを持つ CPU を
Python で表し、フェッチ・デコード・実行のサイクルを繰り返して
1 から 10 までの和を計算する。プログラムとデータは同じメモリに置く。

実行方法: python ch03_toy_cpu.py
関連する章: 第 3 章「コンピュータの構成」
"""

from dataclasses import dataclass, field

# 命令は (命令名, オペランド 1, オペランド 2) の組で表す
Instruction = tuple[str, int, int]


@dataclass
class ToyCPU:
    """レジスタ、プログラムカウンタ、ゼロフラグを持つ簡易 CPU。"""

    memory: list[Instruction | int]
    regs: list[int] = field(default_factory=lambda: [0, 0, 0, 0])
    pc: int = 0
    zero: bool = False
    halted: bool = False
    executed: int = 0

    def fetch(self) -> Instruction:
        """PC が指す番地から命令を読み出し、PC を次の番地に進める。"""
        word = self.memory[self.pc]
        if isinstance(word, int):
            raise RuntimeError(f"番地 {self.pc} は命令ではない")
        self.pc += 1
        return word

    def execute(self, inst: Instruction) -> None:
        """デコードした命令を実行する（ALU 演算、メモリ転送、分岐）。"""
        op, x, y = inst
        r = self.regs
        if op == "LOADI":  # rx <- 即値 y
            r[x] = y
        elif op == "LOAD":  # rx <- memory[y]
            value = self.memory[y]
            assert isinstance(value, int)
            r[x] = value
        elif op == "STORE":  # memory[y] <- rx
            self.memory[y] = r[x]
        elif op == "ADD":  # rx <- rx + ry
            r[x] = r[x] + r[y]
            self.zero = r[x] == 0
        elif op == "SUB":  # rx <- rx - ry
            r[x] = r[x] - r[y]
            self.zero = r[x] == 0
        elif op == "JNZ":  # ゼロフラグが偽なら y 番地へ分岐
            if not self.zero:
                self.pc = y
        elif op == "HALT":
            self.halted = True
        else:
            raise RuntimeError(f"未定義の命令 {op}")

    def run(self, trace: bool = False) -> None:
        """HALT 命令まで命令実行サイクルを繰り返す。"""
        while not self.halted:
            pc = self.pc
            inst = self.fetch()
            self.execute(inst)
            self.executed += 1
            if trace:
                print(f"{self.executed:3d} pc={pc} {inst[0]:<5} "
                      f"{inst[1]} {inst[2]:<2} regs={self.regs} "
                      f"Z={int(self.zero)}")


def main() -> None:
    """1 から 10 までの和を計算するプログラムを実行する。"""
    program: list[Instruction | int] = [
        ("LOADI", 0, 0),   # 0: r0 <- 0   （合計）
        ("LOAD", 1, 9),    # 1: r1 <- [9] （カウンタ n）
        ("LOADI", 2, 1),   # 2: r2 <- 1   （定数 1）
        ("ADD", 0, 1),     # 3: r0 <- r0 + r1
        ("SUB", 1, 2),     # 4: r1 <- r1 - 1、0 ならゼロフラグが立つ
        ("JNZ", 0, 3),     # 5: ゼロでなければ 3 番地へ
        ("STORE", 0, 10),  # 6: [10] <- r0
        ("HALT", 0, 0),    # 7: 停止
        0,                 # 8: （未使用）
        10,                # 9: データ n = 10
        0,                 # 10: 結果の格納先
    ]
    cpu = ToyCPU(program)
    cpu.run(trace=True)
    print(f"結果: memory[10] = {cpu.memory[10]}（{cpu.executed} 命令を実行）")


if __name__ == "__main__":
    main()
