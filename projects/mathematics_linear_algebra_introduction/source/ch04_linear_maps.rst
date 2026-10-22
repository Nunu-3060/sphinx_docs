第 4 章 線形写像としての行列
============================

第 3 章では、行列を数の表として扱った。この章では、行列を「ベクトルを別のベクトルに移す変換」として見る。この見方をすると、行列の積の意味や、交換法則が成り立たない理由が図で理解できる。本書のこれ以降の章は、すべてこの見方に基づいている。

線形写像
--------

ベクトルを入力として、ベクトルを出力する関数 :math:`f: \mathbb{R}^n \to \mathbb{R}^m` を\ :term:`写像`\ という。写像 :math:`f` が、任意のベクトル :math:`\bm{x}, \bm{y}` と数 :math:`c` について

.. math::

   f(\bm{x} + \bm{y}) = f(\bm{x}) + f(\bm{y}), \qquad f(c\,\bm{x}) = c\,f(\bm{x})

を満たすとき、:math:`f` を\ :term:`線形写像`\ という。第 1 章で述べた重ね合わせの原理が成り立つ写像である。入力と出力の空間が同じ（:math:`m = n`）線形写像を、線形変換とも呼ぶ。

:math:`m \times n` 行列 :math:`A` を掛ける写像 :math:`f(\bm{x}) = A\bm{x}` は線形写像である。:math:`A(\bm{x} + \bm{y}) = A\bm{x} + A\bm{y}`、:math:`A(c\,\bm{x}) = c\,A\bm{x}` が成り立つからである。

逆に、どんな線形写像も行列で表せる。2 次元で確かめてみる。任意のベクトルは、基本ベクトル :math:`\bm{e}_1 = (1, 0)`、:math:`\bm{e}_2 = (0, 1)` の線形結合で :math:`\bm{x} = x_1 \bm{e}_1 + x_2 \bm{e}_2` と書ける。:math:`f` が線形なら

.. math::

   f(\bm{x}) = x_1 f(\bm{e}_1) + x_2 f(\bm{e}_2)
   = \begin{pmatrix} f(\bm{e}_1) & f(\bm{e}_2) \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \end{pmatrix}

となる。つまり、:math:`f(\bm{e}_1)` と :math:`f(\bm{e}_2)` を列に並べた行列を掛ければ、:math:`f` が計算できる。次の事実は、本書で最も重要なものの 1 つである。

.. important::

   行列の :math:`j` 列目は、基本ベクトル :math:`\bm{e}_j` の行き先である。線形写像は、基本ベクトルの行き先だけで完全に決まる。

線形写像では、原点は原点に移り（:math:`A\bm{0} = \bm{0}`）、直線は直線（または 1 点）に移り、平行な直線は平行なまま移る。そのため、方眼は「平行四辺形の方眼」に変形する。

2 次元の基本的な変換
--------------------

:numref:`fig-ch04-transforms` は、2 次元の基本的な線形変換で、方眼と F の字がどう変形するかを示したものである。赤の矢印は :math:`\bm{e}_1` の行き先（行列の 1 列目）、青の矢印は :math:`\bm{e}_2` の行き先（2 列目）である。F の字は、左右や上下が反転すると形が変わるので、変換の向きを確かめるのに使っている。

.. _fig-ch04-transforms:

.. figure:: ../build/figures/ch04_transforms.svg
   :alt: 恒等変換、拡大縮小、回転、反射、せん断、射影で、方眼と F の字が変形する様子

   平面の基本的な線形変換

各変換の行列は次のとおりである。

.. list-table:: 平面の基本的な線形変換の行列
   :header-rows: 1
   :widths: 20 30 50

   * - 変換
     - 行列
     - 説明
   * - 拡大縮小
     - :math:`\begin{pmatrix} s_x & 0 \\ 0 & s_y \end{pmatrix}`
     - x 方向に :math:`s_x` 倍、y 方向に :math:`s_y` 倍する。図は :math:`s_x = 1.5`、:math:`s_y = 0.5`
   * - 回転
     - :math:`\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}`
     - 原点を中心に角 :math:`\theta` だけ反時計回りに回す。:math:`\bm{e}_1` は :math:`(\cos\theta, \sin\theta)` に、:math:`\bm{e}_2` は :math:`(-\sin\theta, \cos\theta)` に移る。図は :math:`\theta = 30^\circ`
   * - 反射
     - :math:`\begin{pmatrix} -1 & 0 \\ 0 & 1 \end{pmatrix}`
     - y 軸に関して折り返す。F の字が裏返しになる
   * - せん断
     - :math:`\begin{pmatrix} 1 & k \\ 0 & 1 \end{pmatrix}`
     - 高さ y に比例して、x 方向にずらす（トランプの束を横から押したような変形）。図は :math:`k = 1`
   * - 射影
     - :math:`\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}`
     - x 軸に垂直に落とす。平面全体が x 軸（直線）に潰れ、F の字は線分になる

射影の例のように、線形写像は空間を潰してしまうことがある。潰れた次元の情報は失われるので、元に戻すことはできない。どのような場合に空間が潰れるか、潰れないなら元に戻せるかは、第 6 章（逆行列と行列式）と第 8 章（ランク）の主題である。

図を描くコードを :numref:`list-ch04-transforms` に示す。変換の行列を辞書 ``TRANSFORMS`` にまとめ、行列ごとに、方眼、F の字の頂点、基本ベクトルの行き先を描いている。

.. literalinclude:: ../examples/ch04_transforms.py
   :pyobject: create_figure
   :lineno-match:
   :caption: ch04_transforms.py の create_figure()
   :name: list-ch04-transforms

F の字の頂点は、2 行 :math:`N` 列の配列 ``shape`` にまとめてある（各列が 1 つの頂点）。``a @ shape`` の 1 回の積で、すべての頂点を変換できる。行列の積の列による見方（第 3 章）のとおり、各列（頂点）に ``a`` を掛けた結果が並ぶからである。

サンプルの全体：:download:`ch04_transforms.py <../examples/ch04_transforms.py>`、:download:`la_plot.py <../examples/la_plot.py>`\ （補助モジュール）

変換の合成と行列の積
--------------------

ベクトル :math:`\bm{x}` を、まず行列 :math:`B` で変換し、次に行列 :math:`A` で変換すると、結果は :math:`A(B\bm{x})` である。結合法則から、これは :math:`(AB)\bm{x}` に等しい。つまり、行列の積 :math:`AB` は「:math:`B` の後に :math:`A`」という変換の合成を表す。右側の行列から先に作用することに注意する。

変換の順序を入れ替えると、結果は一般に異なる。:numref:`fig-ch04-composition` は、90 度の回転 :math:`R` とせん断 :math:`S` を、2 通りの順序で合成した結果である。

.. math::

   R = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}, \qquad
   S = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}

.. _fig-ch04-composition:

.. figure:: ../build/figures/ch04_composition.svg
   :alt: 回転の後にせん断を行った場合と、せん断の後に回転を行った場合で、F の字の形が異なる様子

   回転とせん断の合成。順序によって結果が異なる

.. literalinclude:: ../build/outputs/ch04_composition.txt
   :language: text
   :caption: ch04_composition.py の実行結果（合成した変換の行列）

2 つの行列は異なり、F の字の最終的な形も異なる。服を着てから上着を着るのと、上着を着てから服を着るのとで結果が違うのと同じで、変換の合成は順序に依存する。これが、行列の積で交換法則が成り立たない理由である。

サンプルの全体：:download:`ch04_composition.py <../examples/ch04_composition.py>`

平行移動と同次座標
------------------

3D グラフィックスやロボットの制御では、回転や拡大縮小に加えて、平行移動 :math:`\bm{x} \mapsto \bm{x} + \bm{t}` も使う。しかし、平行移動は原点を動かすので、線形写像ではない（:math:`\bm{0}` が :math:`\bm{t}` に移る）。線形写像と平行移動を組み合わせた :math:`\bm{x} \mapsto A\bm{x} + \bm{t}` を\ :term:`アフィン変換`\ という。

アフィン変換を行列の積だけで扱うために、\ :term:`同次座標`\ を使う。2 次元の点 :math:`(x, y)` に 1 を付け加えて 3 次元のベクトル :math:`(x, y, 1)` で表すと、平行移動は 3 × 3 行列の積で書ける。

.. math::

   \begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix}
   \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}
   = \begin{pmatrix} x + t_x \\ y + t_y \\ 1 \end{pmatrix}

回転などの線形変換 :math:`A` は、左上の 2 × 2 の部分に :math:`A` を置き、右の列を :math:`(0, 0, 1)` にした行列で表す。こうすると、回転と平行移動の組み合わせも、行列の積 1 つにまとめられる。

:numref:`fig-ch04-homogeneous` は、家の形をした図形を、90 度の回転 :math:`R` と平行移動 :math:`T`\ （x 方向に 3、y 方向に 1）で変換したものである。

.. _fig-ch04-homogeneous:

.. figure:: ../build/figures/ch04_homogeneous.svg
   :alt: 家の形の図形を、回転の後に平行移動した結果と、平行移動の後に回転した結果

   同次座標による回転と平行移動。点は家の右下の角 (1, 0) の行き先

.. literalinclude:: ../examples/ch04_homogeneous.py
   :pyobject: translation
   :lineno-match:
   :caption: ch04_homogeneous.py の translation()

.. literalinclude:: ../build/outputs/ch04_homogeneous.txt
   :language: text
   :caption: ch04_homogeneous.py の実行結果

「回転の後に平行移動」（:math:`TR`）では、家は原点のまわりで回ってから :math:`(3, 1)` だけ動く。「平行移動の後に回転」（:math:`RT`）では、:math:`(3, 1)` だけ動いた家が、原点のまわりで回るので、大きく離れた位置に移る。3D グラフィックスでは、3 次元の点を :math:`(x, y, z, 1)` と表し、4 × 4 行列で同じことを行う（第 14 章）。

サンプルの全体：:download:`ch04_homogeneous.py <../examples/ch04_homogeneous.py>`

この章のまとめ
--------------

* 重ね合わせの原理を満たす写像を線形写像といい、線形写像は行列の積で表せる。
* 行列の :math:`j` 列目は、基本ベクトル :math:`\bm{e}_j` の行き先である。
* 拡大縮小、回転、反射、せん断、射影は、2 × 2 行列で表せる。
* 行列の積 :math:`AB` は「:math:`B` の後に :math:`A`」という変換の合成である。変換の合成は順序に依存するので、:math:`AB \ne BA` となる。
* 平行移動は線形写像ではないが、同次座標を使うと行列の積で表せる。
