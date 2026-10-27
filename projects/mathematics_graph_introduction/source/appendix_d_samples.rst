付録 D サンプルコード一覧
=========================

サンプルコードの一覧
--------------------

本書のサンプルコードは次のとおりである。ファイル名をクリックするとダウンロードできる。各ファイルは単独で実行でき、自作した実装の結果を表示した後、NetworkX の結果と照合する。

.. list-table::
   :header-rows: 1
   :widths: 35 15 50

   * - ファイル
     - 章
     - 内容
   * - :download:`graph_repr.py <../examples/graph_repr.py>`
     - 第 3 章
     - 隣接行列・接続行列・隣接リストへの変換、握手補題の確認
   * - :download:`connectivity.py <../examples/connectivity.py>`
     - 第 4 章、第 5 章
     - 幅優先探索による距離と連結成分、二部グラフの判定、切断点と橋
   * - :download:`spanning_tree.py <../examples/spanning_tree.py>`
     - 第 6 章
     - Union-Find、クラスカル法、プリム法、プリューファー符号とケイリーの公式
   * - :download:`euler_path.py <../examples/euler_path.py>`
     - 第 7 章
     - ヒールホルツァーのアルゴリズム、バックトラックによるハミルトン閉路の探索
   * - :download:`planarity.py <../examples/planarity.py>`
     - 第 8 章
     - 平面性の判定、オイラーの公式の確認
   * - :download:`coloring.py <../examples/coloring.py>`
     - 第 9 章
     - 貪欲彩色、彩色数の計算、彩色多項式
   * - :download:`matching.py <../examples/matching.py>`
     - 第 10 章
     - 増加路による最大マッチング、最小頂点被覆、ゲール・シャプレー法
   * - :download:`traversal.py <../examples/traversal.py>`
     - 第 11 章
     - 幅優先探索、深さ優先探索、トポロジカルソート、強連結成分分解
   * - :download:`shortest_path.py <../examples/shortest_path.py>`
     - 第 12 章
     - ダイクストラ法、ベルマン・フォード法、ワーシャル・フロイド法、A* 探索
   * - :download:`max_flow.py <../examples/max_flow.py>`
     - 第 13 章
     - エドモンズ・カープ法、最小カット
   * - :download:`spectral.py <../examples/spectral.py>`
     - 第 14 章
     - 歩道の数え上げ、ラプラシアン行列の固有値、行列木定理、スペクトル分割、PageRank
   * - :download:`network_analysis.py <../examples/network_analysis.py>`
     - 第 15 章
     - クラスタ係数、中心性、ER・WS・BA モデルの比較
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - －
     - flake8 と mypy の設定ファイル

実行方法
--------

Python 3.10 以降と、NetworkX（3.3 以降）・NumPy・SciPy が必要である。動作は Python 3.14、NetworkX 3.6 で確認している。ダウンロードしたファイルのあるディレクトリで、次のように実行する。

.. code-block:: text
   :linenos:

   pip install networkx numpy scipy
   python graph_repr.py

Windows のコマンドプロンプトで日本語が文字化けする場合は、環境変数 ``PYTHONIOENCODING`` に ``utf-8`` を設定するか、Windows Terminal などの UTF-8 に対応した端末を使う。

コードの検査
------------

サンプルコードは、PEP 8 に準拠し、すべての関数に型ヒントを付けている。flake8（行長は 120 文字まで許容）と mypy（``strict = True``）の検査で違反が検出されないことを確認している。設定は ``setup.cfg`` に記述してある。NetworkX の型情報を mypy で検査するには、型スタブ ``types-networkx`` が必要である。

.. code-block:: text
   :linenos:

   pip install flake8 mypy types-networkx
   python -m flake8 .
   python -m mypy .

ソースコード
------------

各サンプルコードの全文を示す。

graph_repr.py
~~~~~~~~~~~~~

.. literalinclude:: ../examples/graph_repr.py
   :language: python
   :linenos:

connectivity.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/connectivity.py
   :language: python
   :linenos:

spanning_tree.py
~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/spanning_tree.py
   :language: python
   :linenos:

euler_path.py
~~~~~~~~~~~~~

.. literalinclude:: ../examples/euler_path.py
   :language: python
   :linenos:

planarity.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/planarity.py
   :language: python
   :linenos:

coloring.py
~~~~~~~~~~~

.. literalinclude:: ../examples/coloring.py
   :language: python
   :linenos:

matching.py
~~~~~~~~~~~

.. literalinclude:: ../examples/matching.py
   :language: python
   :linenos:

traversal.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/traversal.py
   :language: python
   :linenos:

shortest_path.py
~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/shortest_path.py
   :language: python
   :linenos:

max_flow.py
~~~~~~~~~~~

.. literalinclude:: ../examples/max_flow.py
   :language: python
   :linenos:

spectral.py
~~~~~~~~~~~

.. literalinclude:: ../examples/spectral.py
   :language: python
   :linenos:

network_analysis.py
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/network_analysis.py
   :language: python
   :linenos:
