サンプルコード一覧
==================

本書で使ったサンプルコードの一覧である。ファイル名をクリックするとダウンロードできる。実行環境は :doc:`ch01_introduction` の「サンプルコードの実行環境」を参照のこと。

各章のサンプル
--------------

.. list-table:: 各章のサンプル
   :header-rows: 1
   :widths: 30 10 40 20

   * - ファイル
     - 章
     - 内容
     - 使用するライブラリ
   * - :download:`state_machine.py <../examples/state_machine.py>`
     - 第 4 章
     - ゲーム画面の状態遷移を表す有限状態機械
     - 標準ライブラリ
   * - :download:`resource_flow.py <../examples/resource_flow.py>`
     - 第 4 章
     - フィードバックループによる所持金の差の変化のシミュレーション
     - matplotlib
   * - :download:`balance_simulation.py <../examples/balance_simulation.py>`
     - 第 5 章
     - モンテカルロ法によるユニットの勝率の検証
     - matplotlib
   * - :download:`difficulty_curve.py <../examples/difficulty_curve.py>`
     - 第 6 章
     - 難易度曲線の 3 つの型の比較
     - matplotlib
   * - :download:`jump_feel.py <../examples/jump_feel.py>`
     - 第 7 章
     - ジャンプの操作感を比べるデモと、ジャンプの軌跡のグラフ
     - pygame-ce、matplotlib
   * - :download:`level_graph.py <../examples/level_graph.py>`
     - 第 9 章
     - 鍵と扉の配置の検証
     - 標準ライブラリ
   * - :download:`procgen_cave.py <../examples/procgen_cave.py>`
     - 第 10 章
     - ランダムウォークとセル・オートマトンによる洞窟の生成と、到達可能性の検証
     - Pillow
   * - :download:`procgen_bsp.py <../examples/procgen_bsp.py>`
     - 第 10 章
     - BSP によるダンジョンの生成
     - Pillow
   * - :download:`playtest_heatmap.py <../examples/playtest_heatmap.py>`
     - 第 11 章、第 12 章
     - プレイログのヒートマップ
     - matplotlib
   * - :download:`setup.cfg <../examples/setup.cfg>`
     -
     - flake8 と mypy の設定
     -

どのサンプルも、``--help`` を付けて実行すると使い方が表示される。

.. code-block:: console
   :linenos:

   python procgen_cave.py --help

総合演習のサンプル
------------------

第 12 章の『宝石と見張り』は、複数のファイルからなるので、zip にまとめてある。

* :download:`final_project.zip </_generated/final_project.zip>`

zip には次のファイルが含まれている。

.. list-table:: final_project.zip の内容
   :header-rows: 1
   :widths: 40 60

   * - ファイル
     - 内容
   * - ``final_project/README.txt``
     - 遊び方とファイルの説明
   * - ``final_project/game_logic.py``
     - ルール（画面表示を含まない部分）
   * - ``final_project/solver.py``
     - 幅優先探索によるレベルの解法
   * - ``final_project/main.py``
     - pygame-ce による画面表示と操作
   * - ``final_project/levels/level1.txt`` 〜 ``level4.txt``
     - レベルのデータ
   * - ``playtest_heatmap.py``
     - プレイログのヒートマップ（第 11 章と同じもの）
   * - ``setup.cfg``
     - flake8 と mypy の設定

個別のファイルは次のリンクからもダウンロードできる。

* :download:`game_logic.py <../examples/final_project/game_logic.py>`
* :download:`solver.py <../examples/final_project/solver.py>`
* :download:`main.py <../examples/final_project/main.py>`
* :download:`level1.txt <../examples/final_project/levels/level1.txt>`
* :download:`level2.txt <../examples/final_project/levels/level2.txt>`
* :download:`level3.txt <../examples/final_project/levels/level3.txt>`
* :download:`level4.txt <../examples/final_project/levels/level4.txt>`

コードの検査
------------

サンプルコードは、PEP 8 に従って書き、すべての関数に型ヒントを付けている。``examples`` フォルダーで次のコマンドを実行すると、flake8（コードの書き方の検査、行長は 120 文字まで許容）と mypy（型の検査、``strict = True``）で検査できる。

.. code-block:: console
   :linenos:

   python -m pip install flake8 mypy
   python -m flake8
   python -m mypy .

設定は ``setup.cfg`` に書いてある。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
   :caption: setup.cfg
