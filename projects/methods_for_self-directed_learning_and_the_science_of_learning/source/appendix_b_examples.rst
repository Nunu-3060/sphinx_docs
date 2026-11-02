.. _appendix-b:

付録 B サンプルコード一覧
========================================================

本書のサンプルコードを示す。いずれも Python 3.10 以降で動作し、標準ライブラリと matplotlib だけを使う。生成 AI などの外部サービスは呼び出さない。

サンプルコードは学習の仕組みを理解するための簡易なモデルや道具であり、実際の記憶を正確に予測するものではない。

すべてのファイルは :download:`examples.zip <_static/downloads/examples.zip>` からまとめてダウンロードできる。個別のファイルは各節のリンクからダウンロードできる。

.. list-table:: サンプルコードの一覧
   :name: tbl-appb-list
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 内容
     - 関連する章
   * - ``forgetting_curve.py``
     - 忘却曲線と復習による保持率の変化を簡易モデルで計算し、グラフにする。
     - :ref:`ch03`、:ref:`ch16`
   * - ``leitner_box.py``
     - ライトナー方式によるカード管理をシミュレーションする。
     - :ref:`ch16`
   * - ``sm2_scheduler.py``
     - SM-2 アルゴリズムで次回の復習日を計算する。
     - :ref:`ch16`
   * - ``quiz.py``
     - CSV の問題集から出題する、検索練習用の小テスト。
     - :ref:`ch04`、:ref:`ch16`
   * - ``interleave_plan.py``
     - 複数の学習項目から、交互学習の計画表を作成する。
     - :ref:`ch04`、:ref:`ch15`
   * - ``study_log.py``
     - CSV 形式の学習ログを集計し、週ごとの学習時間をグラフにする。
     - :ref:`ch15`

実行の準備
----------

matplotlib を使うサンプル（``forgetting_curve.py`` と ``study_log.py``）を実行するには、matplotlib をインストールしておく。

.. code-block:: text
   :linenos:

   py -m pip install matplotlib

コマンド例は Windows の ``py`` コマンドで示す。macOS や Linux では ``python3`` に読み替える。Windows のコマンドプロンプトで日本語の出力が文字化けする場合は、環境変数 ``PYTHONIOENCODING`` に ``utf-8`` を設定する。

グラフを出力するサンプルは、サンプルと同じフォルダに output フォルダを作成し、その中に PNG ファイルを保存する。

コードの検査
^^^^^^^^^^^^

サンプルコードには型ヒントを付け、flake8 と mypy（strict モード）で検査している。設定は examples フォルダの ``setup.cfg`` に記述した（:download:`setup.cfg <../examples/setup.cfg>`）。examples フォルダで次のコマンドを実行すると検査できる。

.. code-block:: text
   :linenos:

   py -m pip install flake8 mypy
   py -m flake8 .
   py -m mypy .

forgetting_curve.py
-------------------------

忘却曲線と、間隔を空けて復習したときの保持率の変化を、簡易モデルで計算する。モデルの考え方は :ref:`ch16` で説明する。

:download:`forgetting_curve.py <../examples/forgetting_curve.py>`

.. literalinclude:: ../examples/forgetting_curve.py
   :language: python
   :linenos:
   :caption: forgetting_curve.py

実行例を示す。``--reviews`` で復習する日（初回学習からの経過日数）を指定する。

.. code-block:: text
   :linenos:

   > py forgetting_curve.py --reviews 1 3 7 14
   復習日: [1.0, 3.0, 7.0, 14.0]
   経過日数 復習しない   復習する（復習日は復習直前の値）
          2       0.82       0.95
          5       0.64       0.95
         10       0.47       0.96
         20       0.31       0.96
         30       0.23       0.91
   グラフを保存した: ...\examples\output\forgetting_curve.png

leitner_box.py
--------------------

ライトナー方式によるカード管理をシミュレーションする。正解する確率は、箱が上がるほど高くなると仮定している。

:download:`leitner_box.py <../examples/leitner_box.py>`

.. literalinclude:: ../examples/leitner_box.py
   :language: python
   :linenos:
   :caption: leitner_box.py

sm2_scheduler.py
----------------------

SM-2 アルゴリズムで、復習ごとの自己評価（0 から 5）から次回の復習日を計算する。

:download:`sm2_scheduler.py <../examples/sm2_scheduler.py>`

.. literalinclude:: ../examples/sm2_scheduler.py
   :language: python
   :linenos:
   :caption: sm2_scheduler.py

quiz.py
-------------

CSV の問題集から出題する、検索練習用の小テストである。問題が表示されたら、答えを見る前に自分で思い出す。思い出せなかった問題は、全問を解き終えた後にもう一度出題する。

:download:`quiz.py <../examples/quiz.py>`、:download:`quiz_sample.csv <../examples/quiz_sample.csv>`

.. literalinclude:: ../examples/quiz.py
   :language: python
   :linenos:
   :caption: quiz.py

問題集は、1 行目を見出し（question,answer）とした CSV ファイルで作る。文字コードは UTF-8 とする。

.. literalinclude:: ../examples/quiz_sample.csv
   :language: text
   :linenos:
   :caption: quiz_sample.csv

問題を作ること自体も、学んだ内容を思い出して整理する作業になる。教材を読み終えたら、教材を閉じてから問題を作るとよい（:ref:`ch04`）。

interleave_plan.py
------------------------

複数の学習項目と項目ごとの問題数から、同じ項目ができるだけ連続しないように並べた交互学習の計画表を作成する。比較のため、項目ごとにまとめて解くブロック学習の順序も表示する。

:download:`interleave_plan.py <../examples/interleave_plan.py>`

.. literalinclude:: ../examples/interleave_plan.py
   :language: python
   :linenos:
   :caption: interleave_plan.py

実行例を示す。

.. code-block:: text
   :linenos:

   > py interleave_plan.py Python=6 SQL=4 正規表現=4
   ## ブロック学習（同じ項目の連続: 11 回）
     1 日目: Python → Python → Python → Python
     2 日目: Python → Python → SQL → SQL
     3 日目: SQL → SQL → 正規表現 → 正規表現
     4 日目: 正規表現 → 正規表現

   ## 交互学習（同じ項目の連続: 0 回）
     1 日目: Python → SQL → Python → 正規表現
     2 日目: Python → SQL → Python → 正規表現
     3 日目: Python → SQL → 正規表現 → Python
     4 日目: SQL → 正規表現

交互学習が効果を発揮するのは、混ぜた項目どうしが紛らわしく、問題ごとに「どの方法を使うべきか」を見分ける必要がある場合である（:ref:`ch04`）。

study_log.py
------------------

CSV 形式の学習ログを集計し、項目別・方法別の合計時間と、週ごとの学習時間を表示する。週ごとの学習時間は棒グラフとして保存する。

:download:`study_log.py <../examples/study_log.py>`、:download:`study_log_sample.csv <../examples/study_log_sample.csv>`

.. literalinclude:: ../examples/study_log.py
   :language: python
   :linenos:
   :caption: study_log.py

学習ログは、1 行目を見出し（date,topic,minutes,method）とした CSV ファイルで記録する。method には「読書」「検索練習」「実装」「執筆」のように学習の方法を書く。方法別の時間を集計すると、効果の低い学び方（読むだけの学習など）に時間が偏っていないかを確認できる（:ref:`ch15`）。

.. literalinclude:: ../examples/study_log_sample.csv
   :language: text
   :linenos:
   :caption: study_log_sample.csv（先頭部分）
   :lines: 1-8

実行例を示す。

.. code-block:: text
   :linenos:

   > py study_log.py
   期間: 2026-10-05 から 2026-11-01
   合計: 785 分（13.1 時間）、学習した日数: 22 日

   ## 項目別
     Rust         650 分 (82.8%)
     SQL          135 分 (17.2%)

   ## 方法別
     実装         365 分 (46.5%)
     検索練習     190 分 (24.2%)
     執筆         130 分 (16.6%)
     読書         100 分 (12.7%)

   ## 週別
     2026-10-05 の週:  205 分
     2026-10-12 の週:  240 分
     2026-10-19 の週:  180 分
     2026-10-26 の週:  160 分

   グラフを保存した: ...\examples\output\study_log.png
