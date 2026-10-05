ワークシートとサンプルコード
============================

本書で紹介したワークシートとサンプルコードをまとめたページです。すべてのファイルは、:download:`examples.zip <_static/downloads/examples.zip>` からまとめてダウンロードできます。展開すると、``examples`` フォルダーの中に、このページで紹介する 5 つのファイルが入っています。

.. contents:: このページの目次
   :local:
   :depth: 1

ワークシート
------------

ワークシートは、Markdown という形式で書かれたテキストファイルです。メモ帳などのテキストエディターで開き、そのまま書き込んで使えます。印刷して手書きで使ってもかまいません。

学習契約書（learning_contract.md）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

自分自身と学習契約を結ぶためのひな形です。使い方は\ :doc:`10_designing_your_learning`\ で説明しています。

:download:`learning_contract.md をダウンロード <../examples/learning_contract.md>`

.. literalinclude:: ../examples/learning_contract.md
   :language: text
   :linenos:

振り返りシート（reflection_sheet.md）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コルブの経験学習モデルに沿って、一つの出来事を振り返るためのシートです。考え方は\ :doc:`06_experiential_learning`\ で説明しています。

:download:`reflection_sheet.md をダウンロード <../examples/reflection_sheet.md>`

.. literalinclude:: ../examples/reflection_sheet.md
   :language: text
   :linenos:

サンプルコード
--------------

サンプルコードは、プログラミング言語 Python で書かれたプログラムです。使わなくても本書の内容は理解できますが、関心のある方は試してみてください。

実行するには、Python（3.10 以降）をインストールしておく必要があります。Python は、`Python の公式サイト <https://www.python.org/>`__\ からダウンロードできます。追加のライブラリーは必要ありません。

ダウンロードしたファイルを置いたフォルダーで、Windows ではコマンドプロンプト、macOS ではターミナルを開き、次のように入力して実行します（macOS では ``python`` の代わりに ``python3`` と入力します）。

.. code-block:: text
   :linenos:

   python review_schedule.py 2026-10-01
   python learning_log.py learning_log_sample.csv

復習の予定を作る（review_schedule.py）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

学んだ日を入力すると、1 日後、3 日後、7 日後、14 日後、30 日後の復習の予定日を表示します。``--intervals`` の後に日数を並べると、間隔を変えられます。考え方は\ :doc:`09_learning_science`\ で説明しています。

:download:`review_schedule.py をダウンロード <../examples/review_schedule.py>`

.. literalinclude:: ../examples/review_schedule.py
   :language: python
   :linenos:

学習の記録を集計する（learning_log.py）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

学習の記録を書いた CSV ファイルを読み込み、テーマごとの合計時間と回数、週ごとの合計時間を表示します。使い方は\ :doc:`10_designing_your_learning`\ で説明しています。

:download:`learning_log.py をダウンロード <../examples/learning_log.py>`

.. literalinclude:: ../examples/learning_log.py
   :language: python
   :linenos:

学習の記録の例（learning_log_sample.csv）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``learning_log.py`` で読み込む CSV ファイルの例です。表計算ソフトで開いて、自分の記録に書き換えて使うこともできます。保存するときは、文字コードを UTF-8 にしてください。

:download:`learning_log_sample.csv をダウンロード <../examples/learning_log_sample.csv>`

.. literalinclude:: ../examples/learning_log_sample.csv
   :language: text
   :linenos:
