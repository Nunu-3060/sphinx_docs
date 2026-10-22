図の作成に使ったコード
======================

本書の図は、Graphviz と Python（matplotlib）を使って作成している。このページでは、図の作成に使ったコードを紹介する。本書の内容を理解するために、このページを読む必要はない。図を修正したい人や、同じような図を作りたい人は参考にしてほしい。

すべてのファイルは、:download:`examples.zip <_static/downloads/examples.zip>` からまとめてダウンロードできる。展開すると、``examples`` フォルダーの中に、このページで紹介する 4 つのファイルが入っている。

.. contents:: このページの目次
   :local:
   :depth: 1

図とファイルの対応
------------------

.. list-table:: 図とファイルの対応
   :header-rows: 1
   :widths: 35 30 35

   * - 図
     - 掲載している章
     - ファイル
   * - 転職の流れと各段階の期間の例
     - :doc:`02_overview`
     - make_figures.py
   * - 選考の流れの例
     - :doc:`06_selection`
     - selection_flow.dot
   * - 内定の承諾から入社日までの日程の例
     - :doc:`08_resignation`
     - make_figures.py
   * - 空白期間の有無による公的手続きの違い
     - :doc:`10_procedures`
     - procedures.dot

実行の方法
----------

実行するには、次のものが必要である。

* Python（3.10 以降）と matplotlib
* Graphviz（``dot`` コマンドを実行できるようにしておく）
* 日本語のフォント（BIZ UDGothic、Yu Gothic、Meiryo などのいずれか）

ダウンロードしたファイルを置いたフォルダーで、次のように入力して実行する。``--out`` の後に、画像を保存するフォルダーを指定する。

.. code-block:: text
   :linenos:

   pip install matplotlib
   python make_figures.py --out figures

``figures`` フォルダーに、4 つの PNG 画像が作成される。本書をビルドするときは、Sphinx の設定ファイル（conf.py）からこのスクリプトを呼び出し、自動的に図を作成している。

図を作成するスクリプト（make_figures.py）
------------------------------------------

Graphviz の dot ファイルを PNG 画像に変換し、matplotlib で 2 つの日程の図を描く。日程の図では、転職活動を青、退職に関する活動をオレンジ、入社後の活動を緑で示している。帯の情報（見出し、開始、終了、色）をリストにまとめ、共通の関数 ``draw_bands`` で描いているため、帯の追加や期間の変更は、リストを書き換えるだけでできる。

:download:`make_figures.py をダウンロード <../examples/make_figures.py>`

.. literalinclude:: ../examples/make_figures.py
   :language: python
   :linenos:

選考の流れ（selection_flow.dot）
--------------------------------

選考の段階を箱で表し、矢印でつないでいる。会社によって行う場合と行わない場合がある段階は、点線の箱にしている。``rank=same`` で 3 つずつを同じ段に並べ、図が横に長くなりすぎないようにしている。

:download:`selection_flow.dot をダウンロード <../examples/selection_flow.dot>`

.. literalinclude:: ../examples/selection_flow.dot
   :language: text
   :linenos:

公的手続きの分岐（procedures.dot）
----------------------------------

質問と共通の手続きを灰色の箱、転職先が行う手続きを青色の箱、自分で行う手続きをオレンジ色の箱で表している。箱の中の文字は、HTML に似た書き方で、見出しを太字にしている。

:download:`procedures.dot をダウンロード <../examples/procedures.dot>`

.. literalinclude:: ../examples/procedures.dot
   :language: text
   :linenos:

検査の設定（setup.cfg）
-----------------------

make_figures.py は、flake8（コードの書き方の検査）と mypy（型の検査）で問題がないことを確認している。setup.cfg は、その設定ファイルである。flake8 では 1 行の長さを 120 文字まで認め、mypy では最も厳しい検査（``strict = True``）を行う。

:download:`setup.cfg をダウンロード <../examples/setup.cfg>`

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:

検査は、``examples`` フォルダーで次のように入力して実行する。

.. code-block:: text
   :linenos:

   pip install flake8 mypy
   flake8 make_figures.py
   mypy make_figures.py
