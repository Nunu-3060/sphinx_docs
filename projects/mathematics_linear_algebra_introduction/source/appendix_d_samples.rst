付録 D サンプルコード一覧
=========================

本書で使ったサンプルコードの一覧である。ファイル名をクリックすると、そのファイルをダウンロードできる。すべてのファイルをまとめた :download:`examples.zip <../build/extra/examples.zip>` もある。ZIP ファイルを展開すると、``examples`` フォルダーにすべてのファイルが置かれる。

実行と検査の方法
----------------

サンプルは、``examples`` フォルダーで実行する。図を描くサンプルは補助モジュール ``la_plot.py`` を import するので、個別にダウンロードした場合は、一覧の「補助モジュール」の列に示したファイルも同じフォルダーに置く。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python ch02_vector_ops.py
   $ python ch04_transforms.py

計算の結果を表示するサンプル（``report()`` を持つもの）は、結果を画面に表示する。図を描くサンプル（``create_figure()`` を持つもの）は、図をウィンドウに表示する。両方を持つサンプルは、結果を表示してから図を表示する。

サンプルは、flake8（PEP 8 などのコーディング規約の検査）と mypy（型ヒントの検査）で違反がないことを確認している。``examples`` フォルダーで次のコマンドを実行すると、同じフォルダーの ``setup.cfg`` の設定で検査できる。

.. code-block:: console
   :linenos:

   $ cd examples
   $ python -m flake8 .
   $ python -m mypy .

ファイルの一覧
--------------

第 1 章 はじめに
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch01_numpy_basics.py <../examples/ch01_numpy_basics.py>`
     - NumPy の配列の基本：ベクトルと行列を作り、形状と演算を確かめる
     - なし

第 2 章 ベクトル
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch02_projection.py <../examples/ch02_projection.py>`
     - 内積と正射影：u を v の方向の成分と、v に直交する成分に分ける
     - ``la_plot.py``
   * - :download:`ch02_vector_ops.py <../examples/ch02_vector_ops.py>`
     - ベクトルの演算：和、スカラー倍、内積、ノルム、なす角、正射影、外積
     - なし
   * - :download:`ch02_vector_sum.py <../examples/ch02_vector_sum.py>`
     - ベクトルの和と線形結合を矢印で描く
     - ``la_plot.py``

第 3 章 行列と行列の演算
~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch03_matrix_ops.py <../examples/ch03_matrix_ops.py>`
     - 行列の演算：行列とベクトルの積の 2 つの見方、行列の積、転置
     - なし

第 4 章 線形写像としての行列
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch04_composition.py <../examples/ch04_composition.py>`
     - 線形変換の合成：回転とせん断を行う順序で結果が変わることを確かめる
     - ``la_plot.py``
   * - :download:`ch04_homogeneous.py <../examples/ch04_homogeneous.py>`
     - 同次座標によるアフィン変換：回転と平行移動を 3 行 3 列の行列で表す
     - ``la_plot.py``
   * - :download:`ch04_transforms.py <../examples/ch04_transforms.py>`
     - 2 次元の基本的な線形変換で、方眼と F の字がどう変形するかを描く
     - ``la_plot.py``

第 5 章 連立一次方程式
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch05_circuit.py <../examples/ch05_circuit.py>`
     - キルヒホッフの法則で、抵抗の回路に流れる電流を求める
     - ``la_plot.py``
   * - :download:`ch05_gauss.py <../examples/ch05_gauss.py>`
     - ガウスの消去法で連立一次方程式を解く
     - なし
   * - :download:`ch05_lu.py <../examples/ch05_lu.py>`
     - LU 分解：係数行列を下三角行列 L と上三角行列 U の積に分解して解く
     - なし
   * - :download:`ch05_two_views.py <../examples/ch05_two_views.py>`
     - 連立一次方程式の 2 つの見方を描く
     - ``la_plot.py``

第 6 章 逆行列と行列式
~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch06_determinant.py <../examples/ch06_determinant.py>`
     - 行列式の計算と性質を確かめる
     - なし
   * - :download:`ch06_determinant_area.py <../examples/ch06_determinant_area.py>`
     - 行列式の幾何学的意味：単位正方形が移る平行四辺形の符号付き面積
     - ``la_plot.py``
   * - :download:`ch06_inverse.py <../examples/ch06_inverse.py>`
     - 逆行列を求め、元の行列との積が単位行列になることを確かめる
     - なし

第 7 章 ベクトル空間と基底
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch07_basis_change.py <../examples/ch07_basis_change.py>`
     - 基底の取り替え：同じベクトルを 2 つの基底で表す
     - ``la_plot.py``
   * - :download:`ch07_independence.py <../examples/ch07_independence.py>`
     - ベクトルの組が線形独立かを、ランクで判定する
     - なし
   * - :download:`ch07_span.py <../examples/ch07_span.py>`
     - 2 つのベクトルが張る空間を描く
     - ``la_plot.py``

第 8 章 ランクと 4 つの基本部分空間
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch08_rank.py <../examples/ch08_rank.py>`
     - 行列のランクと、零空間の基底を求める
     - なし
   * - :download:`ch08_solution_structure.py <../examples/ch08_solution_structure.py>`
     - 連立一次方程式の解の構造：一般解 = 特殊解 + 同次方程式の解
     - ``la_plot.py``

第 9 章 直交性と最小二乗法
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch09_gram_schmidt.py <../examples/ch09_gram_schmidt.py>`
     - グラム・シュミットの直交化で、行列を QR 分解する
     - なし
   * - :download:`ch09_least_squares.py <../examples/ch09_least_squares.py>`
     - 最小二乗法で、測定データに直線と 2 次式を当てはめる
     - ``la_plot.py``
   * - :download:`ch09_projection_matrix.py <../examples/ch09_projection_matrix.py>`
     - 部分空間への正射影と射影行列
     - なし
   * - :download:`ch09_projection_plane.py <../examples/ch09_projection_plane.py>`
     - 3 次元空間のベクトル b を、平面（列空間）へ正射影する様子を描く
     - ``la_plot.py``

第 10 章 固有値と固有ベクトル
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch10_eigen.py <../examples/ch10_eigen.py>`
     - 固有値と固有ベクトルを求め、対角化と行列のべき乗を確かめる
     - なし
   * - :download:`ch10_eigen_geometry.py <../examples/ch10_eigen_geometry.py>`
     - 固有ベクトルの幾何学的意味：変換しても向きが変わらないベクトル
     - ``la_plot.py``
   * - :download:`ch10_fibonacci.py <../examples/ch10_fibonacci.py>`
     - フィボナッチ数列を、行列のべき乗と固有値で求める
     - なし
   * - :download:`ch10_markov.py <../examples/ch10_markov.py>`
     - マルコフ連鎖：天気の移り変わりの確率と、定常分布
     - ``la_plot.py``
   * - :download:`ch10_vibration.py <../examples/ch10_vibration.py>`
     - 2 つの質点とばねの振動を、固有値と固有ベクトル（固有モード）で解く
     - ``la_plot.py``

第 11 章 対称行列と二次形式
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch11_quadratic_form.py <../examples/ch11_quadratic_form.py>`
     - 二次形式 q(x) = x^T A x の等高線と、主軸（固有ベクトル）を描く
     - ``la_plot.py``
   * - :download:`ch11_spectral.py <../examples/ch11_spectral.py>`
     - 対称行列の固有値分解（スペクトル分解）と正定値の判定
     - なし

第 12 章 特異値分解
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch12_image_compression.py <../examples/ch12_image_compression.py>`
     - 特異値分解による画像の低ランク近似
     - ``la_plot.py``
   * - :download:`ch12_svd.py <../examples/ch12_svd.py>`
     - 特異値分解の計算と、擬似逆行列による最小ノルム解
     - なし
   * - :download:`ch12_svd_geometry.py <../examples/ch12_svd_geometry.py>`
     - 特異値分解の幾何学的意味：A = U Σ V^T は「回転 → 拡大縮小 → 回転」
     - ``la_plot.py``

第 13 章 数値計算での注意
~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch13_float.py <../examples/ch13_float.py>`
     - 浮動小数点数の誤差：丸め誤差、桁落ち、計算機イプシロン
     - なし
   * - :download:`ch13_hilbert.py <../examples/ch13_hilbert.py>`
     - 悪条件の行列：ヒルベルト行列の条件数と、連立一次方程式の誤差
     - なし
   * - :download:`ch13_pivoting.py <../examples/ch13_pivoting.py>`
     - ピボット選択の効果：ピボットが非常に小さいと、消去法の結果が大きく狂う
     - ``ch05_gauss.py``

第 14 章 応用
~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 46 20

   * - ファイル
     - 内容
     - 補助モジュール
   * - :download:`ch14_pagerank.py <../examples/ch14_pagerank.py>`
     - PageRank：リンク構造から、ページの重要度を固有ベクトルとして求める
     - なし
   * - :download:`ch14_pca.py <../examples/ch14_pca.py>`
     - 主成分分析（PCA）：共分散行列の固有ベクトルで、データの主な方向を求める
     - ``la_plot.py``
   * - :download:`ch14_projection_3d.py <../examples/ch14_projection_3d.py>`
     - 3D グラフィックスの座標変換：モデル変換、ビュー変換、透視投影
     - ``la_plot.py``

共通のファイル
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 34 66

   * - ファイル
     - 内容
   * - :download:`la_plot.py <../examples/la_plot.py>`
     - 図の描画の補助関数（日本語のフォントの設定、座標平面、矢印、方眼、F の字）
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定

ソースコード
------------

すべてのファイルのソースコードを示す。

la_plot.py
~~~~~~~~~~

.. literalinclude:: ../examples/la_plot.py
   :language: python
   :linenos:

ch01_numpy_basics.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch01_numpy_basics.py
   :language: python
   :linenos:

ch02_projection.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch02_projection.py
   :language: python
   :linenos:

ch02_vector_ops.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch02_vector_ops.py
   :language: python
   :linenos:

ch02_vector_sum.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch02_vector_sum.py
   :language: python
   :linenos:

ch03_matrix_ops.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch03_matrix_ops.py
   :language: python
   :linenos:

ch04_composition.py
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch04_composition.py
   :language: python
   :linenos:

ch04_homogeneous.py
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch04_homogeneous.py
   :language: python
   :linenos:

ch04_transforms.py
~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch04_transforms.py
   :language: python
   :linenos:

ch05_circuit.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch05_circuit.py
   :language: python
   :linenos:

ch05_gauss.py
~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch05_gauss.py
   :language: python
   :linenos:

ch05_lu.py
~~~~~~~~~~

.. literalinclude:: ../examples/ch05_lu.py
   :language: python
   :linenos:

ch05_two_views.py
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch05_two_views.py
   :language: python
   :linenos:

ch06_determinant.py
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch06_determinant.py
   :language: python
   :linenos:

ch06_determinant_area.py
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch06_determinant_area.py
   :language: python
   :linenos:

ch06_inverse.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch06_inverse.py
   :language: python
   :linenos:

ch07_basis_change.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch07_basis_change.py
   :language: python
   :linenos:

ch07_independence.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch07_independence.py
   :language: python
   :linenos:

ch07_span.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/ch07_span.py
   :language: python
   :linenos:

ch08_rank.py
~~~~~~~~~~~~

.. literalinclude:: ../examples/ch08_rank.py
   :language: python
   :linenos:

ch08_solution_structure.py
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch08_solution_structure.py
   :language: python
   :linenos:

ch09_gram_schmidt.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch09_gram_schmidt.py
   :language: python
   :linenos:

ch09_least_squares.py
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch09_least_squares.py
   :language: python
   :linenos:

ch09_projection_matrix.py
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch09_projection_matrix.py
   :language: python
   :linenos:

ch09_projection_plane.py
~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch09_projection_plane.py
   :language: python
   :linenos:

ch10_eigen.py
~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch10_eigen.py
   :language: python
   :linenos:

ch10_eigen_geometry.py
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch10_eigen_geometry.py
   :language: python
   :linenos:

ch10_fibonacci.py
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch10_fibonacci.py
   :language: python
   :linenos:

ch10_markov.py
~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch10_markov.py
   :language: python
   :linenos:

ch10_vibration.py
~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch10_vibration.py
   :language: python
   :linenos:

ch11_quadratic_form.py
~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch11_quadratic_form.py
   :language: python
   :linenos:

ch11_spectral.py
~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch11_spectral.py
   :language: python
   :linenos:

ch12_image_compression.py
~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch12_image_compression.py
   :language: python
   :linenos:

ch12_svd.py
~~~~~~~~~~~

.. literalinclude:: ../examples/ch12_svd.py
   :language: python
   :linenos:

ch12_svd_geometry.py
~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch12_svd_geometry.py
   :language: python
   :linenos:

ch13_float.py
~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch13_float.py
   :language: python
   :linenos:

ch13_hilbert.py
~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch13_hilbert.py
   :language: python
   :linenos:

ch13_pivoting.py
~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch13_pivoting.py
   :language: python
   :linenos:

ch14_pagerank.py
~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch14_pagerank.py
   :language: python
   :linenos:

ch14_pca.py
~~~~~~~~~~~

.. literalinclude:: ../examples/ch14_pca.py
   :language: python
   :linenos:

ch14_projection_3d.py
~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/ch14_projection_3d.py
   :language: python
   :linenos:

setup.cfg
~~~~~~~~~

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
