サンプルコード一覧
==================

本書のサンプルコードの一覧である。各ファイルは、ファイル名のリンクからダウンロードできる。

動作環境
--------

* Python 3.10 以降
* NumPy、matplotlib

必要なライブラリは次のコマンドでインストールできる。

.. code-block:: console
   :linenos:

   pip install numpy matplotlib

各サンプルは、``python ファイル名 --help`` で使い方（指定できる引数の一覧）を表示できる。

すべてのサンプルは、PEP 8 に従い、型ヒントを付けて書かれている。flake8 と mypy（strict モード）による検査に通ることを確認している。検査に使った設定ファイルは次のとおりである（\ :download:`setup.cfg <../examples/setup.cfg>`\ ）。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:

一覧
----

.. list-table:: サンプルコードの一覧
   :header-rows: 1
   :widths: 30 50 20

   * - ファイル
     - 内容
     - 関連する章
   * - :download:`elementary_ca.py <../examples/elementary_ca.py>`
     - 基本セル・オートマトンの時空図を描く
     - :doc:`one_dimensional`
   * - :download:`game_of_life.py <../examples/game_of_life.py>`
     - ライフゲーム（B/S 表記の Life-like CA）をアニメーション表示する
     - :doc:`two_dimensional`
   * - :download:`langtons_ant.py <../examples/langtons_ant.py>`
     - ラングトンのアリを動かす
     - :doc:`two_dimensional`
   * - :download:`traffic_nasch.py <../examples/traffic_nasch.py>`
     - ナーゲル・シュレッケンベルク・モデルで交通流をシミュレーションする
     - :doc:`applications`
   * - :download:`lattice_gas_hpp.py <../examples/lattice_gas_hpp.py>`
     - HPP モデル（格子ガス・オートマトン）で密度の波が広がる様子を表示する
     - :doc:`applications`

elementary_ca.py
----------------

ルール番号を指定して、基本セル・オートマトンの時空図を表示する。既定では中央の 1 セルだけが 1 の初期配置を使い、``--random`` を指定するとランダムな初期配置を使う。

.. code-block:: console
   :linenos:

   python elementary_ca.py 30
   python elementary_ca.py 110 --width 301 --steps 150 --random
   python elementary_ca.py 90 --output rule90.png

.. literalinclude:: ../examples/elementary_ca.py
   :language: python
   :linenos:

game_of_life.py
---------------

ライフゲームをアニメーション表示する。``--pattern`` で初期パターン（block、beehive、blinker、toad、glider、lwss、r_pentomino、gosper_gun）を、``--rule`` で B/S 表記の規則を指定できる。

.. code-block:: console
   :linenos:

   python game_of_life.py --pattern glider
   python game_of_life.py --pattern gosper_gun --size 60 80
   python game_of_life.py --random 0.3 --rule B36/S23

.. literalinclude:: ../examples/game_of_life.py
   :language: python
   :linenos:

langtons_ant.py
---------------

ラングトンのアリを指定したステップ数だけ動かし、結果を表示する。既定の 11000 ステップでは、ハイウェイが伸び始めた様子が見られる。

.. code-block:: console
   :linenos:

   python langtons_ant.py
   python langtons_ant.py --steps 500 --size 40

.. literalinclude:: ../examples/langtons_ant.py
   :language: python
   :linenos:

traffic_nasch.py
----------------

ナーゲル・シュレッケンベルク・モデルの時空図を表示する。``--diagram`` を指定すると、密度を変えながら流量を求めて基本図を描く。

.. code-block:: console
   :linenos:

   python traffic_nasch.py
   python traffic_nasch.py --density 0.1 --p 0.3
   python traffic_nasch.py --diagram

.. literalinclude:: ../examples/traffic_nasch.py
   :language: python
   :linenos:

lattice_gas_hpp.py
------------------

HPP モデル（格子ガス・オートマトン）で、中央の密度の高い領域から波が広がる様子を表示する。

.. code-block:: console
   :linenos:

   python lattice_gas_hpp.py
   python lattice_gas_hpp.py --size 256 --steps 60

.. literalinclude:: ../examples/lattice_gas_hpp.py
   :language: python
   :linenos:
