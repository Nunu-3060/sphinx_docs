図の作成に使ったコード
======================

本書の図は、Graphviz と Python（matplotlib）を使って作成しています。このページでは、図の作成に使ったコードを紹介します。本書の内容を理解するために、このページを読む必要はありません。図を修正したい方や、同じような図を作りたい方は参考にしてください。

すべてのファイルは、:download:`examples.zip <_static/downloads/examples.zip>` からまとめてダウンロードできます。展開すると、``examples`` フォルダーの中に、このページで紹介する 5 つのファイルが入っています。

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
   * - 退職の流れ
     - :doc:`02_overview`
     - retirement_flow.dot
   * - 退職後の主な手続きの期限
     - :doc:`02_overview`
     - deadlines.dot
   * - 退職日と、3 月分の保険料を納める保険
     - :doc:`03_before_decision`
     - make_figures.py
   * - 退職日から逆算した日程の例
     - :doc:`05_handover`
     - make_figures.py
   * - 退職後の医療保険の選び方
     - :doc:`07_health_insurance`
     - health_insurance_choice.dot
   * - 退職による国民年金の種別の変化
     - :doc:`08_pension`
     - pension_types.dot
   * - 基本手当の支給の対象になるまでの期間
     - :doc:`09_employment_insurance`
     - make_figures.py
   * - 勤続年数と退職所得控除額
     - :doc:`10_tax`
     - make_figures.py
   * - 住民税の対象となる所得と、納める期間
     - :doc:`10_tax`
     - make_figures.py

実行の方法
----------

実行するには、次のものが必要です。

* Python（3.10 以降）と matplotlib
* Graphviz（``dot`` コマンドを実行できるようにしておきます）
* 日本語のフォント（BIZ UDGothic、Yu Gothic、Meiryo などのいずれか）

ダウンロードしたファイルを置いたフォルダーで、次のように入力して実行します。``--out`` の後に、画像を保存するフォルダーを指定します。

.. code-block:: text
   :linenos:

   pip install matplotlib
   python make_figures.py --out figures

``figures`` フォルダーに、9 つの PNG 画像が作成されます。本書をビルドするときは、Sphinx の設定ファイル（conf.py）からこのスクリプトを呼び出し、自動的に図を作成しています。

図を作成するスクリプト（make_figures.py）
------------------------------------------

Graphviz の dot ファイルを PNG 画像に変換し、matplotlib で 5 つのグラフを描きます。図の色は、本文の表や注記と調和する、落ち着いた青とオレンジを中心にしています。

:download:`make_figures.py をダウンロード <../examples/make_figures.py>`

.. literalinclude:: ../examples/make_figures.py
   :language: python
   :linenos:

退職の流れ（retirement_flow.dot）
---------------------------------

4 つの時期を箱で表し、左から右に矢印でつないでいます。箱の中の文字は、HTML に似た書き方で、見出しを太字にしています。

:download:`retirement_flow.dot をダウンロード <../examples/retirement_flow.dot>`

.. literalinclude:: ../examples/retirement_flow.dot
   :language: text
   :linenos:

手続きの期限（deadlines.dot）
-----------------------------

期限を早い順に左から右に並べています。期限が短く、特に注意が必要なもの（14 日以内、20 日以内）はオレンジ色の箱にしています。箱の間隔は、実際の日数に比例していません。

:download:`deadlines.dot をダウンロード <../examples/deadlines.dot>`

.. literalinclude:: ../examples/deadlines.dot
   :language: text
   :linenos:

医療保険の選び方（health_insurance_choice.dot）
-----------------------------------------------

質問を灰色の箱、選択肢を青色の箱で表し、「はい」「いいえ」などの答えを矢印に書いています。

:download:`health_insurance_choice.dot をダウンロード <../examples/health_insurance_choice.dot>`

.. literalinclude:: ../examples/health_insurance_choice.dot
   :language: text
   :linenos:

国民年金の種別の変化（pension_types.dot）
-----------------------------------------

在職中と退職後を枠（cluster）で囲み、本人と配偶者の種別が変わることを矢印で示しています。本人と配偶者を結ぶ点線は扶養の関係を表します。

:download:`pension_types.dot をダウンロード <../examples/pension_types.dot>`

.. literalinclude:: ../examples/pension_types.dot
   :language: text
   :linenos:
