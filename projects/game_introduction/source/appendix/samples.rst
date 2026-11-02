付録 B　サンプルコード一覧
==========================

本書のサンプルは、次のリンクからダウンロードできる。ファイル名のリンクを開くとダウンロードでき、「全文」のリンクを開くとこのページの下の方でコード全体を読める。

ダウンロード
------------

.. list-table:: Python のサンプル
   :header-rows: 1
   :widths: 25 10 55 10

   * - ファイル
     - 章
     - 内容
     - 全文
   * - :download:`game_loop.py <../../examples/py/game_loop.py>`
     - 4
     - ゲームループの最小の例。落ちてくる果物をかごで受け止める
     - :ref:`表示 <src-game_loop>`
   * - :download:`tictactoe.py <../../examples/py/tictactoe.py>`
     - 5、8
     - 三目並べの局面数を数える。ミニマックス法の AI と対戦する
     - :ref:`表示 <src-tictactoe>`
   * - :download:`nim.py <../../examples/py/nim.py>`
     - 5、8
     - ニムの必勝法を使う AI と対戦する
     - :ref:`表示 <src-nim>`
   * - :download:`rps.py <../../examples/py/rps.py>`
     - 5、8
     - 勝ったときの点が手ごとに違うじゃんけんの最適な混合戦略を求める（numpy を使う）
     - :ref:`表示 <src-rps>`
   * - :download:`dice.py <../../examples/py/dice.py>`
     - 5
     - サイコロの和の分布を計算し、実際に振った結果と比べる
     - :ref:`表示 <src-dice>`
   * - :download:`gacha.py <../../examples/py/gacha.py>`
     - 5
     - 全種類をそろえるまでの回数を計算・シミュレーションする
     - :ref:`表示 <src-gacha>`
   * - :download:`shuffle.py <../../examples/py/shuffle.py>`
     - 5
     - 正しいシャッフルと誤ったシャッフルの偏りを比べる
     - :ref:`表示 <src-shuffle>`
   * - :download:`elo.py <../../examples/py/elo.py>`
     - 5
     - イロレーティングで強さを測る
     - :ref:`表示 <src-elo>`
   * - :download:`sugoroku.py <../../examples/py/sugoroku.py>`
     - 2、8
     - すごろくのルールを変えて勝敗の決まり方を測る
     - :ref:`表示 <src-sugoroku>`
   * - :download:`difficulty_plot.py <../../examples/py/difficulty_plot.py>`
     - 8
     - dodge_lab の記録（CSV）から難易度曲線を描く（matplotlib を使う）
     - :ref:`表示 <src-difficulty_plot>`
   * - :download:`difficulty_sample.csv <../../examples/py/difficulty_sample.csv>`
     - 8
     - 演習 7 の記入例のデータ。\ ``difficulty_plot.py`` と同じフォルダーに置く
     - ―
   * - :download:`setup.cfg <../../examples/setup.cfg>`
     - ―
     - flake8 と mypy の設定。\ ``py`` フォルダーの 1 つ上に置く
     - ―

.. list-table:: Godot のサンプルとワークシート
   :header-rows: 1
   :widths: 25 10 55 10

   * - ファイル
     - 章
     - 内容
     - 全文
   * - :download:`dodge_lab.zip <../_generated/dodge_lab.zip>`
     - 4、8
     - 落ちてくるブロックを避ける Godot 4.7.2 のプロジェクト。展開して ``project.godot`` をインポートする
     - :ref:`表示 <src-main_gd>`
   * - :download:`01_play_log.txt <../../examples/worksheets/01_play_log.txt>`
     - 7
     - ワークシート 1　遊びの記録
     - :doc:`表示 <worksheets>`
   * - :download:`02_mda_analysis.txt <../../examples/worksheets/02_mda_analysis.txt>`
     - 8
     - ワークシート 2　MDA とコアループによる分析
     - :doc:`表示 <worksheets>`
   * - :download:`03_rule_change.txt <../../examples/worksheets/03_rule_change.txt>`
     - 8
     - ワークシート 3　ルール変更の記録
     - :doc:`表示 <worksheets>`

実行方法
--------

Python のサンプルは、Python 3.12 以降で動作する。\ ``rps.py`` は numpy を、\ ``difficulty_plot.py`` は matplotlib を使うので、必要に応じて次のようにインストールする。

.. code-block:: text
   :linenos:

   py -m pip install numpy matplotlib

各ファイルの先頭のコメントに、実行方法と引数の説明がある。コードの検査には flake8 と mypy を使い、\ ``setup.cfg`` のある場所で次のように実行すると、違反が検出されないことを確認している。

.. code-block:: text
   :linenos:

   py -m flake8
   py -m mypy py

``dodge_lab`` は、Godot 4.7.2 で開いたときに警告とエラーが出ないことを確認している。GDScript の変数と関数には、すべて型を書いている。

全文
----

.. _src-game_loop:

game_loop.py
~~~~~~~~~~~~

.. literalinclude:: ../../examples/py/game_loop.py
   :language: python
   :linenos:

.. _src-tictactoe:

tictactoe.py
~~~~~~~~~~~~

.. literalinclude:: ../../examples/py/tictactoe.py
   :language: python
   :linenos:

.. _src-nim:

nim.py
~~~~~~

.. literalinclude:: ../../examples/py/nim.py
   :language: python
   :linenos:

.. _src-rps:

rps.py
~~~~~~

.. literalinclude:: ../../examples/py/rps.py
   :language: python
   :linenos:

.. _src-dice:

dice.py
~~~~~~~

.. literalinclude:: ../../examples/py/dice.py
   :language: python
   :linenos:

.. _src-gacha:

gacha.py
~~~~~~~~

.. literalinclude:: ../../examples/py/gacha.py
   :language: python
   :linenos:

.. _src-shuffle:

shuffle.py
~~~~~~~~~~

.. literalinclude:: ../../examples/py/shuffle.py
   :language: python
   :linenos:

.. _src-elo:

elo.py
~~~~~~

.. literalinclude:: ../../examples/py/elo.py
   :language: python
   :linenos:

.. _src-sugoroku:

sugoroku.py
~~~~~~~~~~~

.. literalinclude:: ../../examples/py/sugoroku.py
   :language: python
   :linenos:

.. _src-difficulty_plot:

difficulty_plot.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../examples/py/difficulty_plot.py
   :language: python
   :linenos:

.. _src-main_gd:

dodge_lab/main.gd
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../../examples/godot/dodge_lab/main.gd
   :language: gdscript
   :linenos:
