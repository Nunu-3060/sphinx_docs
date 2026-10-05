付録：RISC-V RV32I 命令一覧
============================

この付録では、本書で使う RISC-V の命令を中心に、RV32I のすべての命令、乗除算の M 拡張の命令、主な擬似命令、レジスタの ABI 名をまとめます。命令形式とアドレッシングモードについては「:doc:`06_isa`」、擬似命令と呼び出し規約については「:doc:`07_machine_language`」を参照してください。

表の記法は次のとおりです。

* rd は書き込み先のレジスタ、rs1、rs2 は読み出し元のレジスタ、imm は即値です。
* M[a] はアドレス a から始まるメモリの内容を表します。
* 「符号拡張」は上位ビットを符号ビットで埋めること、「ゼロ拡張」は 0 で埋めることを表します。
* 分岐とジャンプの offset は PC からの相対的なバイト数で、アセンブリではラベルで書くのが普通です。

算術論理命令
------------

.. list-table:: RV32I の算術論理命令
   :header-rows: 1
   :widths: 14 8 42 36

   * - 命令
     - 形式
     - 意味
     - 例
   * - add
     - R
     - rd = rs1 + rs2
     - ``add a0, a1, a2``
   * - sub
     - R
     - rd = rs1 - rs2
     - ``sub a0, a1, a2``
   * - and
     - R
     - rd = rs1 & rs2（ビットごとの AND）
     - ``and a0, a1, a2``
   * - or
     - R
     - rd = rs1 | rs2（ビットごとの OR）
     - ``or a0, a1, a2``
   * - xor
     - R
     - rd = rs1 ^ rs2（ビットごとの XOR）
     - ``xor a0, a1, a2``
   * - sll
     - R
     - rd = rs1 << rs2[4:0]（論理左シフト）
     - ``sll a0, a1, a2``
   * - srl
     - R
     - rd = rs1 >> rs2[4:0]（論理右シフト、上位を 0 で埋める）
     - ``srl a0, a1, a2``
   * - sra
     - R
     - rd = rs1 >> rs2[4:0]（算術右シフト、上位を符号ビットで埋める）
     - ``sra a0, a1, a2``
   * - slt
     - R
     - rd = (rs1 < rs2) ? 1 : 0（符号付きの比較）
     - ``slt a0, a1, a2``
   * - sltu
     - R
     - rd = (rs1 < rs2) ? 1 : 0（符号なしの比較）
     - ``sltu a0, a1, a2``
   * - addi
     - I
     - rd = rs1 + imm
     - ``addi a0, a1, -5``
   * - andi
     - I
     - rd = rs1 & imm
     - ``andi a0, a1, 0xff``
   * - ori
     - I
     - rd = rs1 | imm
     - ``ori a0, a1, 1``
   * - xori
     - I
     - rd = rs1 ^ imm
     - ``xori a0, a1, -1``
   * - slli
     - I
     - rd = rs1 << imm（imm は 0〜31）
     - ``slli a0, a1, 2``
   * - srli
     - I
     - rd = rs1 >> imm（論理右シフト）
     - ``srli a0, a1, 4``
   * - srai
     - I
     - rd = rs1 >> imm（算術右シフト）
     - ``srai a0, a1, 4``
   * - slti
     - I
     - rd = (rs1 < imm) ? 1 : 0（符号付きの比較）
     - ``slti a0, a1, 10``
   * - sltiu
     - I
     - rd = (rs1 < imm) ? 1 : 0（符号なしの比較）
     - ``sltiu a0, a1, 1``
   * - lui
     - U
     - rd = imm << 12（上位 20 ビットを設定）
     - ``lui a0, 0x12345``
   * - auipc
     - U
     - rd = PC + (imm << 12)
     - ``auipc a0, 0x1``

I 形式の即値は 12 ビットの符号付き整数で、演算の前に 32 ビットに符号拡張されます。sltiu も即値を符号拡張してから符号なしとして比較します。

ロード命令とストア命令
----------------------

.. list-table:: RV32I のロード命令とストア命令
   :header-rows: 1
   :widths: 14 8 42 36

   * - 命令
     - 形式
     - 意味
     - 例
   * - lw
     - I
     - rd = M[rs1 + imm]（4 バイト）
     - ``lw a0, 8(sp)``
   * - lh
     - I
     - rd = M[rs1 + imm]（2 バイト、符号拡張）
     - ``lh a0, 2(a1)``
   * - lhu
     - I
     - rd = M[rs1 + imm]（2 バイト、ゼロ拡張）
     - ``lhu a0, 2(a1)``
   * - lb
     - I
     - rd = M[rs1 + imm]（1 バイト、符号拡張）
     - ``lb a0, 0(a1)``
   * - lbu
     - I
     - rd = M[rs1 + imm]（1 バイト、ゼロ拡張）
     - ``lbu a0, 0(a1)``
   * - sw
     - S
     - M[rs1 + imm] = rs2（4 バイト）
     - ``sw a0, 8(sp)``
   * - sh
     - S
     - M[rs1 + imm] = rs2 の下位 2 バイト
     - ``sh a0, 2(a1)``
   * - sb
     - S
     - M[rs1 + imm] = rs2 の下位 1 バイト
     - ``sb a0, 0(a1)``

分岐命令とジャンプ命令
----------------------

.. list-table:: RV32I の分岐命令とジャンプ命令
   :header-rows: 1
   :widths: 14 8 42 36

   * - 命令
     - 形式
     - 意味
     - 例
   * - beq
     - B
     - rs1 == rs2 なら PC = PC + offset
     - ``beq a0, a1, loop``
   * - bne
     - B
     - rs1 != rs2 なら PC = PC + offset
     - ``bne a0, zero, loop``
   * - blt
     - B
     - rs1 < rs2（符号付き）なら PC = PC + offset
     - ``blt t0, t1, loop``
   * - bge
     - B
     - rs1 >= rs2（符号付き）なら PC = PC + offset
     - ``bge t0, t1, done``
   * - bltu
     - B
     - rs1 < rs2（符号なし）なら PC = PC + offset
     - ``bltu a0, a1, loop``
   * - bgeu
     - B
     - rs1 >= rs2（符号なし）なら PC = PC + offset
     - ``bgeu a0, a1, done``
   * - jal
     - J
     - rd = PC + 4、PC = PC + offset
     - ``jal ra, func``
   * - jalr
     - I
     - rd = PC + 4、PC = (rs1 + imm) の最下位ビットを 0 にした値
     - ``jalr zero, 0(ra)``

条件分岐の範囲は PC から約 :math:`\pm 4` KiB、jal の範囲は約 :math:`\pm 1` MiB です。より遠くへのジャンプは auipc と jalr を組み合わせて行います。

その他の命令
------------

.. list-table:: RV32I のその他の命令
   :header-rows: 1
   :widths: 14 8 42 36

   * - 命令
     - 形式
     - 意味
     - 例
   * - ecall
     - I
     - 実行環境（OS など）を呼び出します（システムコール）。
     - ``ecall``
   * - ebreak
     - I
     - デバッガに制御を移します（ブレークポイント）。
     - ``ebreak``
   * - fence
     - I
     - メモリ操作の順序を保証します。
     - ``fence rw, rw``

RV32I の命令は、上の表の 40 種類ですべてです。CSR を読み書きする csrrw、csrrs などの命令は Zicsr 拡張に、mret はマシンモードの特権命令として定められています。

M 拡張の命令
------------

.. list-table:: M 拡張（乗算と除算）の命令
   :header-rows: 1
   :widths: 14 8 42 36

   * - 命令
     - 形式
     - 意味
     - 例
   * - mul
     - R
     - rd = (rs1 × rs2) の下位 32 ビット
     - ``mul a0, a1, a2``
   * - mulh
     - R
     - rd = (rs1 × rs2) の上位 32 ビット（符号付き × 符号付き）
     - ``mulh a0, a1, a2``
   * - mulhu
     - R
     - rd = (rs1 × rs2) の上位 32 ビット（符号なし × 符号なし）
     - ``mulhu a0, a1, a2``
   * - mulhsu
     - R
     - rd = (rs1 × rs2) の上位 32 ビット（符号付き × 符号なし）
     - ``mulhsu a0, a1, a2``
   * - div
     - R
     - rd = rs1 ÷ rs2（符号付き、0 方向に切り捨て）
     - ``div a0, a1, a2``
   * - divu
     - R
     - rd = rs1 ÷ rs2（符号なし）
     - ``divu a0, a1, a2``
   * - rem
     - R
     - rd = rs1 を rs2 で割った余り（符号付き）
     - ``rem a0, a1, a2``
   * - remu
     - R
     - rd = rs1 を rs2 で割った余り（符号なし）
     - ``remu a0, a1, a2``

RISC-V では、0 による除算は例外を起こさず、決められた値（div では :math:`-1`\ 、rem では被除数）を返します。

主な擬似命令
------------

.. list-table:: RISC-V の主な擬似命令
   :header-rows: 1
   :widths: 24 40 36

   * - 擬似命令
     - 展開後の命令
     - 意味
   * - ``nop``
     - ``addi zero, zero, 0``
     - 何もしません。
   * - ``li rd, imm``
     - ``addi rd, zero, imm`` または ``lui`` + ``addi``
     - 定数を読み込みます。
   * - ``la rd, symbol``
     - ``auipc rd, ...`` + ``addi rd, rd, ...``
     - アドレスを読み込みます。
   * - ``mv rd, rs``
     - ``addi rd, rs, 0``
     - レジスタのコピー
   * - ``not rd, rs``
     - ``xori rd, rs, -1``
     - ビット反転
   * - ``neg rd, rs``
     - ``sub rd, zero, rs``
     - 符号反転
   * - ``seqz rd, rs``
     - ``sltiu rd, rs, 1``
     - rs == 0 なら 1
   * - ``snez rd, rs``
     - ``sltu rd, zero, rs``
     - rs != 0 なら 1
   * - ``beqz rs, label``
     - ``beq rs, zero, label``
     - rs == 0 なら分岐
   * - ``bnez rs, label``
     - ``bne rs, zero, label``
     - rs != 0 なら分岐
   * - ``blez rs, label``
     - ``bge zero, rs, label``
     - rs <= 0 なら分岐
   * - ``bgt rs, rt, label``
     - ``blt rt, rs, label``
     - rs > rt なら分岐
   * - ``ble rs, rt, label``
     - ``bge rt, rs, label``
     - rs <= rt なら分岐
   * - ``j label``
     - ``jal zero, label``
     - 無条件ジャンプ
   * - ``jr rs``
     - ``jalr zero, 0(rs)``
     - レジスタの値のアドレスへジャンプ
   * - ``call label``
     - ``auipc ra, ...`` + ``jalr ra, ...(ra)``
     - 関数呼び出し
   * - ``ret``
     - ``jalr zero, 0(ra)``
     - 関数からの戻り

レジスタの ABI 名
-----------------

.. list-table:: 整数レジスタの ABI 名
   :header-rows: 1
   :widths: 16 16 40 28

   * - レジスタ
     - ABI 名
     - 用途
     - 呼び出しをまたいで保存されるか
   * - x0
     - zero
     - 常に 0
     - —
   * - x1
     - ra
     - 戻りアドレス
     - されません。
   * - x2
     - sp
     - スタックポインタ
     - されます。
   * - x3
     - gp
     - グローバルポインタ
     - —
   * - x4
     - tp
     - スレッドポインタ
     - —
   * - x5〜x7
     - t0〜t2
     - 一時レジスタ
     - されません。
   * - x8
     - s0（fp）
     - 保存レジスタ、フレームポインタ
     - されます。
   * - x9
     - s1
     - 保存レジスタ
     - されます。
   * - x10〜x11
     - a0〜a1
     - 引数、戻り値
     - されません。
   * - x12〜x17
     - a2〜a7
     - 引数
     - されません。
   * - x18〜x27
     - s2〜s11
     - 保存レジスタ
     - されます。
   * - x28〜x31
     - t3〜t6
     - 一時レジスタ
     - されません。

「されます」のレジスタ（callee-saved）は、呼び出された関数が使う場合に元の値を保存して復元する義務があります。「されません」のレジスタ（caller-saved）は、呼び出し後も値が必要なら呼び出し側が保存します。

.. list-table:: 浮動小数点レジスタの ABI 名（F／D 拡張）
   :header-rows: 1
   :widths: 16 16 40 28

   * - レジスタ
     - ABI 名
     - 用途
     - 呼び出しをまたいで保存されるか
   * - f0〜f7
     - ft0〜ft7
     - 一時レジスタ
     - されません。
   * - f8〜f9
     - fs0〜fs1
     - 保存レジスタ
     - されます。
   * - f10〜f11
     - fa0〜fa1
     - 引数、戻り値
     - されません。
   * - f12〜f17
     - fa2〜fa7
     - 引数
     - されません。
   * - f18〜f27
     - fs2〜fs11
     - 保存レジスタ
     - されます。
   * - f28〜f31
     - ft8〜ft11
     - 一時レジスタ
     - されません。
