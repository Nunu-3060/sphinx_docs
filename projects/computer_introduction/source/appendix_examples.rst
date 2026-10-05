サンプルコード一覧
==================

本書のサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。どのファイルも Python 3.10 以降の標準ライブラリだけで動作し、``python turing_machine.py`` のように実行できます。

.. list-table:: サンプルコード一覧
   :header-rows: 1
   :widths: 28 22 50

   * - ファイル
     - 関連する章
     - 内容
   * - :download:`turing_machine.py <../examples/turing_machine.py>`
     - :doc:`04_theory`
     - 2 進数に 1 を足すチューリングマシンのシミュレータ
   * - :download:`base_conversion.py <../examples/base_conversion.py>`
     - :doc:`05_information`
     - 2 進数・10 進数・16 進数の相互変換
   * - :download:`twos_complement.py <../examples/twos_complement.py>`
     - :doc:`05_information`
     - 2 の補数表現、符号の反転、オーバーフローの確認
   * - :download:`float_error.py <../examples/float_error.py>`
     - :doc:`05_information`
     - 浮動小数点数の丸め誤差と IEEE 754 のビット列の表示
   * - :download:`logic_gates.py <../examples/logic_gates.py>`
     - :doc:`06_logic_circuits`
     - NAND だけで作る論理ゲートと真理値表
   * - :download:`adder.py <../examples/adder.py>`
     - :doc:`06_logic_circuits`
     - 半加算器、全加算器、リプルキャリー加算器
   * - :download:`toy_cpu.py <../examples/toy_cpu.py>`
     - :doc:`07_architecture`
     - アキュムレータ型の簡易 CPU のシミュレータ
   * - :download:`cache_sim.py <../examples/cache_sim.py>`
     - :doc:`07_architecture`
     - ダイレクトマップ方式キャッシュのヒット率の計測

各ファイルの内容は、関連する章の本文で行番号付きで閲覧できます。

コードの品質について
--------------------

すべてのサンプルコードには型ヒントを記述しています。また、次のコマンドで、PEP 8 に従っていること、および型の誤りがないことを確認しています。

.. code-block:: console
   :linenos:

   $ flake8 examples
   $ mypy --strict examples
