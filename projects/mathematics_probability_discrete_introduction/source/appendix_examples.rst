付録 B サンプルコードの実行方法
===============================

サンプルコードの一覧
--------------------

本書のサンプルコードは次のとおりである。ファイル名をクリックするとダウンロードできる。

.. list-table::
   :header-rows: 1
   :widths: 45 15 40

   * - ファイル
     - 章
     - 内容
   * - :download:`ch02_sets_logic.py <../examples/ch02_sets_logic.py>`
     - 第 2 章
     - 集合演算、べき集合、真理値表
   * - :download:`ch03_functions_relations.py <../examples/ch03_functions_relations.py>`
     - 第 3 章
     - 単射・全射の判定、同値類、半順序
   * - :download:`ch04_counting.py <../examples/ch04_counting.py>`
     - 第 4 章
     - 順列・組合せ、攪乱順列、漸化式
   * - :download:`ch05_graphs.py <../examples/ch05_graphs.py>`
     - 第 5 章
     - 隣接リスト、幅優先探索、二部グラフ、オイラー路
   * - :download:`ch06_probability.py <../examples/ch06_probability.py>`
     - 第 6 章
     - 古典的確率、誕生日問題、モンティ・ホール問題、ベイズの定理
   * - :download:`ch07_random_variables.py <../examples/ch07_random_variables.py>`
     - 第 7 章
     - 分布の表現、期待値と分散、指示確率変数
   * - :download:`ch08_distributions.py <../examples/ch08_distributions.py>`
     - 第 8 章
     - 代表的な離散分布、scipy.stats との照合、ポアソン近似
   * - :download:`ch09_joint_distributions.py <../examples/ch09_joint_distributions.py>`
     - 第 9 章
     - 同時分布、共分散と相関係数、畳み込み
   * - :download:`ch10_limit_theorems.py <../examples/ch10_limit_theorems.py>`
     - 第 10 章
     - 確率の不等式、大数の法則、中心極限定理
   * - :download:`ch11_markov_chains.py <../examples/ch11_markov_chains.py>`
     - 第 11 章
     - 遷移行列、定常分布、ギャンブラーの破産問題
   * - :download:`ch12_randomized_algorithms.py <../examples/ch12_randomized_algorithms.py>`
     - 第 12 章
     - ハッシュ衝突、クーポンコレクター問題、乱択クイックソート、ブルームフィルタ、モンテカルロ法
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - －
     - flake8 と mypy の設定ファイル

環境の準備
----------

Python 3.11 以上をインストールし、必要なライブラリをインストールする。仮想環境を使う場合の手順（Windows のコマンドプロンプト）は次のとおりである。

.. code-block:: bat
   :linenos:

   python -m venv .venv
   .venv\Scripts\activate
   python -m pip install numpy scipy
   python -m pip install flake8 mypy scipy-stubs

macOS や Linux では、2 行目を ``source .venv/bin/activate`` に置き換える。4 行目は型検査を行う場合にのみ必要である。``scipy-stubs`` は SciPy の型情報を提供するパッケージで、mypy で SciPy を使うコードを検査する際に必要となる。

実行
----

サンプルコードは、いずれも単独で実行できる。ダウンロードしたファイルのあるディレクトリで、次のように実行する。

.. code-block:: bat
   :linenos:

   python ch06_probability.py

乱数を使うサンプルコードでは乱数の種を固定しているので、同じ環境で実行すれば本文と同じ結果が得られる。ただし、Python や NumPy のバージョンによっては、乱数列や計算結果が本文と異なることがある。

Windows のコマンドプロンプトで出力の日本語が文字化けする場合は、環境変数 ``PYTHONIOENCODING`` に ``utf-8`` を設定するか、``python -X utf8 ch06_probability.py`` のように UTF-8 モードで実行する。

コードの検査
------------

サンプルコードは、コーディング規約 PEP 8 に従い、すべての関数に型ヒントを付けている。flake8（コーディング規約の検査）と mypy（型検査）による検査に合格することを確認している。設定ファイル ``setup.cfg`` の内容は次のとおりである。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:

flake8 では 1 行の長さを 120 文字まで許容し、mypy では ``strict = True`` で最も厳しい検査を行う。``setup.cfg`` とサンプルコードを同じディレクトリに置き、そのディレクトリで次のように実行する。

.. code-block:: bat
   :linenos:

   python -m flake8 .
   python -m mypy .

問題がなければ、flake8 は何も出力せず、mypy は ``Success: no issues found in 11 source files`` のように出力する。
