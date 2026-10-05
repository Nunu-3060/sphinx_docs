サンプルコード一覧
==================

本書のサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。どのファイルも Python 3.10 以降の標準ライブラリだけで動作し、``python riscv_sim.py`` のように引数なしで実行できます。

.. list-table:: サンプルコード一覧
   :header-rows: 1
   :widths: 28 24 48

   * - ファイル
     - 関連する章
     - 内容
   * - :download:`performance_calc.py <../examples/performance_calc.py>`
     - :doc:`04_performance`
     - CPU 性能の式によるプロセッサの比較、アムダールの法則、ルーフラインモデルの計算
   * - :download:`float_representation.py <../examples/float_representation.py>`
     - :doc:`05_data_representation`
     - 2 の補数と IEEE 754 のビット表現、FP16 への丸め、バイトオーダーの確認
   * - :download:`alu.py <../examples/alu.py>`
     - :doc:`08_digital_logic`
     - 論理ゲートから組み立てる全加算器・リプルキャリー加算器・8 ビット ALU
   * - :download:`riscv_sim.py <../examples/riscv_sim.py>`
     - :doc:`09_datapath`
     - RV32I のサブセットを実行する命令セットシミュレーター（ラベルを解決する簡易アセンブラ付き）
   * - :download:`pipeline_sim.py <../examples/pipeline_sim.py>`
     - :doc:`10_pipeline`
     - 5 段パイプラインのストール数・サイクル数・CPI の計算（フォワーディングの有無の比較）
   * - :download:`branch_predictor.py <../examples/branch_predictor.py>`
     - :doc:`11_ilp`
     - 常に成立・1 ビット・2 ビット・gshare の分岐予測器の的中率の比較
   * - :download:`tomasulo_sim.py <../examples/tomasulo_sim.py>`
     - :doc:`11_ilp`
     - Tomasulo のアルゴリズムを簡略化したアウトオブオーダー実行のシミュレーター
   * - :download:`cache_sim.py <../examples/cache_sim.py>`
     - :doc:`12_memory_hierarchy`
     - セットアソシアティブキャッシュのシミュレーター（ミスの 3C 分類付き）
   * - :download:`cache_effect.py <../examples/cache_effect.py>`
     - :doc:`12_memory_hierarchy`
     - 連続アクセスとストライドアクセスの実行時間の比較
   * - :download:`tlb_sim.py <../examples/tlb_sim.py>`
     - :doc:`13_virtual_memory`
     - 2 段ページテーブルと TLB によるアドレス変換のシミュレーター
   * - :download:`mesi_sim.py <../examples/mesi_sim.py>`
     - :doc:`15_parallel`
     - MESI プロトコルの状態遷移と false sharing のシミュレーター
   * - :download:`gpu_simt_sim.py <../examples/gpu_simt_sim.py>`
     - :doc:`16_gpu`
     - SIMT の分岐ダイバージェンスによる実行サイクル数の比較
   * - :download:`gpu_coalescing.py <../examples/gpu_coalescing.py>`
     - :doc:`16_gpu`
     - GPU のメモリアクセスの合体と共有メモリのバンクコンフリクトの計数
   * - :download:`hamming_code.py <../examples/hamming_code.py>`
     - :doc:`18_security_reliability`
     - ハミング (7,4) 符号による 1 ビット誤りの訂正と SECDED

各ファイルの内容は、関連する章の本文で行番号付きで閲覧できます。

コードの品質について
--------------------

すべてのサンプルコードには型ヒントを記述しています。また、プロジェクトのルートで次のコマンドを実行し、PEP 8 に従っていること、および型の誤りがないことを確認しています。

.. code-block:: console
   :linenos:

   python -m flake8 examples
   python -m mypy --strict examples
