第 2 章 ベクトル
================

この章では、線形代数の最も基本的な対象であるベクトルを扱う。ベクトルの和とスカラー倍、線形結合、内積、ノルム、正射影、外積を、図と NumPy の計算で確かめる。

矢印としてのベクトル、数の組としてのベクトル
--------------------------------------------

物理では、:term:`ベクトル`\ を「大きさと向きを持つ量」として導入する。速度、力、変位などがその例であり、図では矢印で表す。矢印は、始点の位置を変えても（平行移動しても）同じベクトルを表す。

平面上の矢印は、始点を原点に置くと、終点の座標 :math:`(x, y)` で決まる。そこで、ベクトルを数の組として

.. math::

   \bm{v} = \begin{pmatrix} v_1 \\ v_2 \end{pmatrix}

と表す。:math:`v_1, v_2` をベクトルの\ :term:`成分`\ という。成分が :math:`n` 個のベクトルを :math:`n` 次元のベクトルと呼び、:math:`n` 次元のベクトル全体の集合を :math:`\mathbb{R}^n` と書く。

3 次元までは矢印として図に描けるが、4 次元以上は描けない。しかし、数の組としては何次元でも同じように扱える。例えば、ある製品の重さ、長さ、価格、在庫数を並べた 4 次元のベクトルや、128 × 128 画素の画像の画素値を並べた 16384 次元のベクトルを考えることができる。線形代数の強みは、2 次元や 3 次元の図で得た直観を、そのまま高い次元に持ち込めることである。

和とスカラー倍
--------------

ベクトルの和とスカラー倍は、成分ごとに計算する。

.. math::

   \bm{u} + \bm{v} = \begin{pmatrix} u_1 + v_1 \\ u_2 + v_2 \end{pmatrix}, \qquad
   c\,\bm{v} = \begin{pmatrix} c\,v_1 \\ c\,v_2 \end{pmatrix}

ここで :math:`c` は数であり、ベクトルと区別して\ :term:`スカラー`\ と呼ぶ。

矢印で考えると、和 :math:`\bm{u} + \bm{v}` は、:math:`\bm{u}` の終点に :math:`\bm{v}` の始点をつないだときの、全体の矢印である（:numref:`fig-ch02-vector-sum` の左）。:math:`\bm{u}` と :math:`\bm{v}` を 2 辺とする平行四辺形の対角線と言ってもよい。スカラー倍 :math:`c\,\bm{v}` は、:math:`\bm{v}` と同じ直線の上で、長さを :math:`|c|` 倍した矢印である。:math:`c` が負なら向きが逆になる。

.. _fig-ch02-vector-sum:

.. figure:: ../build/figures/ch02_vector_sum.svg
   :alt: ベクトルの和を平行四辺形で表した図と、線形結合 2u - v を矢印をつないで表した図

   ベクトルの和（左）と線形結合 :math:`2\bm{u} - \bm{v}`\ （右）。:math:`\bm{u} = (3, 1)`、:math:`\bm{v} = (1, 2)`

線形結合
--------

スカラー倍と和を組み合わせた

.. math::

   c_1 \bm{v}_1 + c_2 \bm{v}_2 + \cdots + c_k \bm{v}_k

を、ベクトル :math:`\bm{v}_1, \ldots, \bm{v}_k` の\ :term:`線形結合`\ （一次結合）という。:numref:`fig-ch02-vector-sum` の右は、線形結合 :math:`2\bm{u} - \bm{v}` を、:math:`2\bm{u}` の矢印の先に :math:`-\bm{v}` をつないで作った図である。

線形結合は、線形代数の中心となる操作である。第 3 章で示すように、行列とベクトルの積は列ベクトルの線形結合であり、第 5 章の連立一次方程式は「あるベクトルを、与えられたベクトルの線形結合で表す係数を求める問題」と言い換えられる。

内積
----

2 つのベクトル :math:`\bm{u}, \bm{v} \in \mathbb{R}^n` の\ :term:`内積`\ を、成分の積の和で定義する。

.. math::

   \bm{u} \cdot \bm{v} = u_1 v_1 + u_2 v_2 + \cdots + u_n v_n

内積の結果はベクトルではなく数（スカラー）である。列ベクトルの記法では、内積を :math:`\bm{u}^\top \bm{v}` とも書く（行ベクトルと列ベクトルの積。第 3 章を参照）。

内積から、ベクトルの長さが定まる。ベクトル :math:`\bm{v}` の長さを\ :term:`ノルム`\ と呼び、:math:`\|\bm{v}\|` と書く。

.. math::

   \|\bm{v}\| = \sqrt{\bm{v} \cdot \bm{v}} = \sqrt{v_1^2 + v_2^2 + \cdots + v_n^2}

これは三平方の定理を :math:`n` 次元に広げたものである。ノルムが 1 のベクトルを\ :term:`単位ベクトル`\ という。0 でないベクトル :math:`\bm{v}` を :math:`\|\bm{v}\|` で割ると、同じ向きの単位ベクトルが得られる。この操作を\ :term:`正規化`\ という。

内積の幾何学的な意味は、次の式で表される。:math:`\theta` は 2 つのベクトルのなす角である。

.. math::

   \bm{u} \cdot \bm{v} = \|\bm{u}\|\,\|\bm{v}\| \cos\theta

この式は、2 次元では余弦定理から導ける。:math:`\bm{u}, \bm{v}, \bm{u} - \bm{v}` を 3 辺とする三角形に余弦定理を使うと :math:`\|\bm{u} - \bm{v}\|^2 = \|\bm{u}\|^2 + \|\bm{v}\|^2 - 2\|\bm{u}\|\|\bm{v}\|\cos\theta` であり、左辺を成分で展開すると :math:`\|\bm{u}\|^2 + \|\bm{v}\|^2 - 2\,\bm{u} \cdot \bm{v}` になるからである。

この式から、次のことが分かる。

* :math:`\bm{u} \cdot \bm{v} > 0` なら、なす角は鋭角（同じような向き）である。
* :math:`\bm{u} \cdot \bm{v} = 0` なら、なす角は直角である。このとき、2 つのベクトルは\ :term:`直交`\ するという。
* :math:`\bm{u} \cdot \bm{v} < 0` なら、なす角は鈍角（反対に近い向き）である。

:math:`|\cos\theta| \le 1` なので、:math:`|\bm{u} \cdot \bm{v}| \le \|\bm{u}\|\,\|\bm{v}\|` が成り立つ。これを\ :term:`コーシー・シュワルツの不等式`\ という。4 次元以上では「なす角」を図で考えられないが、この不等式が成り立つので、逆に :math:`\cos\theta = \bm{u} \cdot \bm{v} / (\|\bm{u}\|\,\|\bm{v}\|)` でなす角を定義できる。機械学習で文書や画像の類似度として使われる\ :term:`コサイン類似度`\ は、この :math:`\cos\theta` のことである。

正射影
------

内積を使うと、あるベクトルの、ある方向の成分を取り出せる。ベクトル :math:`\bm{u}` から、:math:`\bm{v}` を含む直線に垂線を下ろしたときの足を :math:`\bm{p}` とする（:numref:`fig-ch02-projection`）。:math:`\bm{p}` を、:math:`\bm{u}` の :math:`\bm{v}` 方向への\ :term:`正射影`\ という。

.. _fig-ch02-projection:

.. figure:: ../build/figures/ch02_projection.svg
   :alt: ベクトル u を、v の方向の成分 p と、v に垂直な成分 u - p に分けた図

   :math:`\bm{u} = (2, 3)` の :math:`\bm{v} = (4, 1)` 方向への正射影 :math:`\bm{p}`

:math:`\bm{p}` は :math:`\bm{v}` のスカラー倍なので :math:`\bm{p} = c\,\bm{v}` と書ける。残りの成分 :math:`\bm{u} - \bm{p}` が :math:`\bm{v}` と直交するという条件 :math:`(\bm{u} - c\,\bm{v}) \cdot \bm{v} = 0` から :math:`c` を求めると、次の式が得られる。

.. math::

   \bm{p} = \frac{\bm{u} \cdot \bm{v}}{\bm{v} \cdot \bm{v}}\,\bm{v}

:math:`\bm{v}` が単位ベクトルなら分母は 1 になり、:math:`\bm{p} = (\bm{u} \cdot \bm{v})\,\bm{v}` と簡単になる。つまり、単位ベクトルとの内積は「その方向の成分の大きさ」である。正射影は、第 9 章の最小二乗法とグラム・シュミットの直交化の基礎になる。

外積
----

3 次元のベクトルには、もう 1 つの積がある。:math:`\bm{a}, \bm{b} \in \mathbb{R}^3` の\ :term:`外積`\ （ベクトル積）を次の式で定義する。

.. math::

   \bm{a} \times \bm{b} = \begin{pmatrix} a_2 b_3 - a_3 b_2 \\ a_3 b_1 - a_1 b_3 \\ a_1 b_2 - a_2 b_1 \end{pmatrix}

内積と異なり、外積の結果はベクトルである。外積 :math:`\bm{a} \times \bm{b}` には、次の性質がある。

* :math:`\bm{a}` とも :math:`\bm{b}` とも直交する。
* 向きは、右手の親指を :math:`\bm{a}`、人差し指を :math:`\bm{b}` の向きにしたときの中指の向き（右手系）である。
* 長さは、:math:`\bm{a}` と :math:`\bm{b}` を 2 辺とする平行四辺形の面積 :math:`\|\bm{a}\|\,\|\bm{b}\| \sin\theta` に等しい。
* 順序を入れ替えると符号が変わる（:math:`\bm{b} \times \bm{a} = -\bm{a} \times \bm{b}`）。

外積は、3D グラフィックスで面の法線ベクトル（面に垂直なベクトル）を求めるときや、力学でトルク（力のモーメント）:math:`\bm{\tau} = \bm{r} \times \bm{F}` を計算するときに使う。外積は 3 次元に特有の演算であり、本書のこれ以降の内容では使わない。

NumPy で計算する
----------------

:numref:`list-ch02-vector-ops` で、ここまでの演算を NumPy で計算する。

.. literalinclude:: ../examples/ch02_vector_ops.py
   :pyobject: report
   :lineno-match:
   :caption: ch02_vector_ops.py の report()
   :name: list-ch02-vector-ops

関数 ``angle_between()`` と ``project()`` は、なす角と正射影の式をそのままコードにしたものである。

.. literalinclude:: ../examples/ch02_vector_ops.py
   :pyobject: project
   :lineno-match:
   :caption: ch02_vector_ops.py の project()

実行結果は次のとおりである。

.. literalinclude:: ../build/outputs/ch02_vector_ops.txt
   :language: text
   :caption: ch02_vector_ops.py の実行結果

:math:`\bm{u} = (3, 1)`、:math:`\bm{v} = (1, 2)` の内積は :math:`3 \cdot 1 + 1 \cdot 2 = 5` であり、:math:`\cos\theta = 5 / (\sqrt{10}\sqrt{5}) = 1/\sqrt{2}` なので、なす角は 45 度である。正射影 :math:`\bm{p}` は :math:`(5/5)\,\bm{v} = (1, 2)` で、残りの成分 :math:`\bm{u} - \bm{p}` と :math:`\bm{v}` の内積は 0 になっている。外積 :math:`\bm{a} \times \bm{b}` は :math:`\bm{a}` とも :math:`\bm{b}` とも内積が 0 であり、順序を入れ替えると符号が反転している。

サンプルの全体：:download:`ch02_vector_ops.py <../examples/ch02_vector_ops.py>`、:download:`ch02_vector_sum.py <../examples/ch02_vector_sum.py>`、:download:`ch02_projection.py <../examples/ch02_projection.py>`

この章のまとめ
--------------

* ベクトルは矢印であり、数の組でもある。数の組として扱えば、何次元でも同じように計算できる。
* ベクトルの和とスカラー倍を組み合わせたものを線形結合という。
* 内積は :math:`\|\bm{u}\|\,\|\bm{v}\|\cos\theta` に等しく、内積が 0 の 2 つのベクトルは直交する。
* 正射影 :math:`\bm{p} = (\bm{u} \cdot \bm{v} / \bm{v} \cdot \bm{v})\,\bm{v}` で、ベクトルのある方向の成分を取り出せる。
* 3 次元のベクトルの外積は、2 つのベクトルに直交し、長さが平行四辺形の面積に等しいベクトルである。
