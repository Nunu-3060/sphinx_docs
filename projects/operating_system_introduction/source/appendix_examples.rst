サンプルコード一覧
==================

本書のサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。どのファイルも Python 3.10 以降の標準ライブラリだけで動作し、Linux、macOS、Windows のいずれでも ``python process_info.py`` のように実行できます。

.. list-table:: サンプルコード一覧
   :header-rows: 1
   :widths: 30 25 45

   * - ファイル
     - 関連する章
     - 内容
   * - :download:`syscall_cost.py <../examples/syscall_cost.py>`
     - :doc:`04_hardware_and_kernel`
     - バッファリングの有無による書き込みの速さの比較
   * - :download:`process_info.py <../examples/process_info.py>`
     - :doc:`05_process`
     - 自分自身のプロセスの情報の表示
   * - :download:`subprocess_pipe.py <../examples/subprocess_pipe.py>`
     - :doc:`05_process`
     - 子プロセスの起動とパイプによる通信
   * - :download:`race_condition.py <../examples/race_condition.py>`
     - :doc:`06_thread`
     - 競合状態の再現とロックによる解消
   * - :download:`producer_consumer.py <../examples/producer_consumer.py>`
     - :doc:`06_thread`
     - 条件変数を使った生産者・消費者問題
   * - :download:`deadlock.py <../examples/deadlock.py>`
     - :doc:`06_thread`
     - デッドロックの再現とロックの取得順序による回避
   * - :download:`scheduler_sim.py <../examples/scheduler_sim.py>`
     - :doc:`07_scheduling`
     - FCFS、SJF、ラウンドロビンのシミュレーター
   * - :download:`address_translation.py <../examples/address_translation.py>`
     - :doc:`08_memory`
     - ページテーブルによるアドレス変換
   * - :download:`page_replacement_sim.py <../examples/page_replacement_sim.py>`
     - :doc:`08_memory`
     - FIFO、LRU、クロック、OPT のページフォールトの回数の比較
   * - :download:`mmap_example.py <../examples/mmap_example.py>`
     - :doc:`08_memory`
     - メモリマップトファイルの読み書き
   * - :download:`file_descriptor.py <../examples/file_descriptor.py>`
     - :doc:`09_storage_and_filesystem`
     - ファイルディスクリプタの複製とファイルのメタデータ
   * - :download:`nonblocking_io.py <../examples/nonblocking_io.py>`
     - :doc:`10_io_and_device`
     - I/O 多重化を使ったエコーサーバー

各ファイルの内容は、関連する章の本文で行番号付きで閲覧できます。

コードの品質について
--------------------

すべてのサンプルコードには型ヒントを記述しています。また、次のコマンドで、PEP 8 に従っていること、および型の誤りがないことを確認しています。

.. code-block:: console
   :linenos:

   $ flake8 examples
   $ mypy --strict examples

実行時の注意
------------

* Windows のコマンドプロンプトや PowerShell で日本語が文字化けする場合は、``python -X utf8 process_info.py`` のように ``-X utf8`` を付けて実行してください。
* 実行結果のうち、プロセス ID、処理時間、ポート番号、スレッドの実行順序に依存する出力は、実行のたびに変わります。
