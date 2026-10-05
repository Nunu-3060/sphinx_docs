"""アキュムレータ型の簡易 CPU のシミュレータ。

プログラムとデータを同じメモリに置き (プログラム内蔵方式)、
フェッチ・デコード・実行の命令サイクルを 1 命令ずつ表示します。

命令は 10 進数 3 桁で表し、百の位が命令の種類 (オペコード)、
下 2 桁がメモリのアドレス (オペランド) です。

    0xx  HALT     停止する
    1aa  LOAD aa  ACC <- M[aa]
    2aa  STORE aa M[aa] <- ACC
    3aa  ADD aa   ACC <- ACC + M[aa]
    4aa  SUB aa   ACC <- ACC - M[aa]
    5aa  JUMP aa  PC <- aa
    6aa  JZ aa    ACC が 0 なら PC <- aa
    7xx  OUT      ACC の値を出力する

ACC はアキュムレータ、PC はプログラムカウンタ、M[aa] はアドレス aa の
メモリの内容を表します。xx は使用しません。

実行方法::

    python toy_cpu.py
"""

MEMORY_SIZE = 32

MNEMONICS = {
    0: "HALT",
    1: "LOAD",
    2: "STORE",
    3: "ADD",
    4: "SUB",
    5: "JUMP",
    6: "JZ",
    7: "OUT",
}

# 1 + 2 + 3 + 4 + 5 を計算するプログラム
# M[20] = n (残りの回数), M[21] = sum (合計), M[22] = 定数 1
SUM_PROGRAM: dict[int, int] = {
    0: 121,  # LOAD 21   ACC <- sum
    1: 320,  # ADD 20    ACC <- sum + n
    2: 221,  # STORE 21  sum <- ACC
    3: 120,  # LOAD 20   ACC <- n
    4: 422,  # SUB 22    ACC <- n - 1
    5: 220,  # STORE 20  n <- ACC
    6: 608,  # JZ 08     n が 0 ならループを抜ける
    7: 500,  # JUMP 00   ループの先頭へ戻る
    8: 121,  # LOAD 21   ACC <- sum
    9: 700,  # OUT       合計を出力する
    10: 0,   # HALT
    20: 5,   # n
    21: 0,   # sum
    22: 1,   # 定数 1
}


class ToyCPU:
    """アキュムレータ 1 個とプログラムカウンタだけを持つ CPU。"""

    def __init__(self, program: dict[int, int]) -> None:
        self.memory = [0] * MEMORY_SIZE
        for address, word in program.items():
            self.memory[address] = word
        self.pc = 0  # プログラムカウンタ: 次に実行する命令のアドレス
        self.acc = 0  # アキュムレータ: 計算結果を保持するレジスタ
        self.halted = False

    def step(self) -> None:
        """命令を 1 つ実行する (命令サイクル 1 回分)。"""
        # 1. フェッチ: PC が指すアドレスから命令を読み、PC を進める
        address_of_instruction = self.pc
        instruction = self.memory[self.pc]
        self.pc += 1

        # 2. デコード: 命令をオペコードとアドレスに分解する
        opcode, address = divmod(instruction, 100)

        # 3. 実行: オペコードに応じた処理を行う
        output = None
        if opcode == 0:
            self.halted = True
        elif opcode == 1:
            self.acc = self.memory[address]
        elif opcode == 2:
            self.memory[address] = self.acc
        elif opcode == 3:
            self.acc += self.memory[address]
        elif opcode == 4:
            self.acc -= self.memory[address]
        elif opcode == 5:
            self.pc = address
        elif opcode == 6:
            if self.acc == 0:
                self.pc = address
        elif opcode == 7:
            output = self.acc
        else:
            raise ValueError(f"未定義の命令です: {instruction}")

        mnemonic = MNEMONICS[opcode]
        print(
            f"{address_of_instruction:02d}: {instruction:03d} "
            f"{mnemonic:<5} {address:02d} | ACC={self.acc:>2} PC={self.pc:02d}"
        )
        if output is not None:
            print(f"    出力: {output}")

    def run(self, max_steps: int = 1000) -> None:
        """HALT 命令を実行するまで命令サイクルを繰り返す。"""
        for _ in range(max_steps):
            if self.halted:
                return
            self.step()
        raise RuntimeError(f"{max_steps} 命令以内に停止しませんでした")


def main() -> None:
    """合計を求めるプログラムを実行する。"""
    cpu = ToyCPU(SUM_PROGRAM)
    cpu.run()


if __name__ == "__main__":
    main()
