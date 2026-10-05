################################################################
付録 A サンプルコード
################################################################

本書のサンプルコードの一覧と使い方をまとめます。

ダウンロード
================================================================

すべてのサンプルコードをまとめた ZIP ファイルを用意しています。

* :download:`tiny_examples.zip <_generated/tiny_examples.zip>`

ZIP ファイルを展開し、展開したディレクトリで次の節のコマンドを実行してください。各ファイルは、下の表のリンク先で閲覧・個別にダウンロードすることもできます。

ファイルの一覧
================================================================

.. list-table::
   :header-rows: 1
   :widths: 30 15 55

   * - ファイル
     - 章
     - 内容
   * - :doc:`tiny_lexer.py <code/tiny_lexer>`
     - 第 3 章
     - 字句解析器
   * - :doc:`calc_rd.py <code/calc_rd>`
     - 第 4 章
     - 再帰下降構文解析による電卓
   * - :doc:`calc_pratt.py <code/calc_pratt>`
     - 第 4 章
     - Pratt 構文解析による算術式の解析
   * - :doc:`tiny_ast.py <code/tiny_ast>`
     - 第 5 章
     - 型と抽象構文木
   * - :doc:`tiny_parser.py <code/tiny_parser>`
     - 第 5 章
     - 構文解析器
   * - :doc:`tiny_checker.py <code/tiny_checker>`
     - 第 6 章
     - 意味解析器
   * - :doc:`tiny_runtime.py <code/tiny_runtime>`
     - 第 7 章
     - 実行時ライブラリ
   * - :doc:`tiny_interp.py <code/tiny_interp>`
     - 第 7 章
     - 木構造インタプリタ
   * - :doc:`tiny_ir.py <code/tiny_ir>`
     - 第 8 章
     - 中間表現と IR インタプリタ
   * - :doc:`tiny_ssa.py <code/tiny_ssa>`
     - 第 8 章
     - 支配関係と SSA 形式
   * - :doc:`tiny_opt.py <code/tiny_opt>`
     - 第 9 章
     - 最適化と生存変数解析
   * - :doc:`tiny_bytecode.py <code/tiny_bytecode>`
     - 第 10 章
     - バイトコード生成器
   * - :doc:`tiny_vm.py <code/tiny_vm>`
     - 第 10 章
     - 仮想マシン
   * - :doc:`tiny_regalloc.py <code/tiny_regalloc>`
     - 第 11 章
     - レジスタ割り当て
   * - :doc:`gc_sim.py <code/gc_sim>`
     - 第 11 章
     - ガベージコレクションのシミュレーション
   * - :doc:`tiny.py <code/tiny>`
     - 付録 A
     - コマンドラインツール
   * - :doc:`test_tiny.py <code/test_tiny>`
     - 付録 A
     - テスト
   * - :doc:`programs/*.tiny <code/programs>`
     -
     - Tiny のサンプルプログラム

.. toctree::
   :hidden:

   code/tiny_lexer
   code/calc_rd
   code/calc_pratt
   code/tiny_ast
   code/tiny_parser
   code/tiny_checker
   code/tiny_runtime
   code/tiny_interp
   code/tiny_ir
   code/tiny_ssa
   code/tiny_opt
   code/tiny_bytecode
   code/tiny_vm
   code/tiny_regalloc
   code/gc_sim
   code/tiny
   code/test_tiny
   code/programs

動作環境
================================================================

* Python 3.10 以降（本書の実行例は Python 3.14 で確認しています）
* 標準ライブラリだけを使っており、追加のパッケージは不要です。
* 制御フローグラフの図を描くには、別途 Graphviz が必要です。

コマンドラインツール
================================================================

``tiny.py`` は、Tiny 処理系の各段階の結果を表示したり、プログラムを実行したりするコマンドラインツールです。

.. code-block:: text
   :linenos:

   python tiny.py <サブコマンド> [オプション] <ファイル>

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - サブコマンド
     - 内容
   * - ``tokens``
     - トークン列を表示する（第 3 章）
   * - ``ast``
     - 抽象構文木を表示する（第 5 章）
   * - ``check``
     - 意味解析だけを行う（第 6 章）
   * - ``run``
     - 木構造インタプリタで実行する（第 7 章）
   * - ``ir``
     - 中間表現を表示する（第 8 章）。オプションは ``--ssa`` で SSA 形式に、``--opt`` で最適化した IR に、``--dot 関数名`` で制御フローグラフの DOT 言語の出力に、``--exec`` で IR インタプリタによる実行になる
   * - ``bytecode``
     - バイトコードを逆アセンブルして表示する（第 10 章）
   * - ``vm``
     - 仮想マシンで実行する（第 10 章）
   * - ``regalloc``
     - レジスタ割り当ての結果を表示する（第 11 章）。``-k 個数`` でレジスタの数を指定する（既定値は 4）

使用例を示します。

.. code-block:: console
   :linenos:

   $ python tiny.py run programs/fib.tiny
   $ python tiny.py ir --opt programs/sort.tiny
   $ python tiny.py ir --dot sum programs/sum.tiny > sum.dot
   $ python tiny.py vm programs/primes.tiny
   $ python tiny.py regalloc -k 6 programs/sum.tiny

``tiny_ast.py`` と ``tiny_runtime.py`` 以外のモジュールは単独でも実行でき、引数なしで実行すると組み込みの例を処理します。また、``tiny_lexer.py``、``tiny_parser.py``、``tiny_checker.py``、``tiny_interp.py``、``tiny_ir.py``、``tiny_ssa.py``、``tiny_opt.py``、``tiny_bytecode.py``、``tiny_vm.py``、``tiny_regalloc.py`` は、Tiny のファイル名を引数に与えると、そのファイルを処理します。

テスト
================================================================

``test_tiny.py`` は、サンプルプログラムと小さなテストケースを、6 とおりの方法（木構造インタプリタ、IR、SSA 形式の IR、最適化した IR、SSA 形式から戻した IR、仮想マシン）で実行し、すべての出力が一致することを確かめます。エラーの検出のテストも含みます。

.. code-block:: console
   :linenos:

   $ python -m unittest test_tiny.py
   ..........
   ----------------------------------------------------------------------
   Ran 10 tests in 0.140s

   OK

静的検査
================================================================

すべての Python ファイルは、次のコマンドで違反が検出されないことを確認しています。

.. code-block:: console
   :linenos:

   $ python -m flake8 .
   $ python -m mypy --strict .
   Success: no issues found in 17 source files
