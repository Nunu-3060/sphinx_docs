.. _appendix-b:

付録 B 添字記法とレヴィ＝チヴィタ記号
=====================================

:ref:`第 8 章 <ch08>`\ のナブラを含む公式は、成分を書き下せば確かめられるが、式が長くなる。この付録では、成分を添字で表す記法と、外積を表すレヴィ＝チヴィタ記号を導入し、公式を短く証明する方法を示す。

添字記法と総和規約
------------------

座標を :math:`(x_1, x_2, x_3) = (x, y, z)` と番号で表し、ベクトル :math:`\bm{a}` の成分を :math:`a_i`\ （:math:`i = 1, 2, 3`）と書く。また、偏微分を :math:`\partial_i = \partial / \partial x_i` と略記する。

1 つの項の中に同じ添字が 2 回現れたら、その添字について 1 から 3 まで和をとると約束する。これを\ **アインシュタインの総和規約**\ という。たとえば内積と発散は次のように書ける。

.. math::

   \bm{a} \cdot \bm{b} = a_i b_i = \sum_{i=1}^{3} a_i b_i, \qquad \nabla \cdot \bm{F} = \partial_i F_i

和をとる添字（ダミー添字）は、別の文字に置き換えても意味が変わらない（:math:`a_i b_i = a_j b_j`）。一方、1 回だけ現れる添字（自由添字）は「ベクトルの第 :math:`i` 成分」を表し、等式の両辺で一致していなければならない。たとえば勾配の第 :math:`i` 成分は :math:`(\nabla f)_i = \partial_i f` である。

クロネッカーのデルタ
--------------------

次の記号をクロネッカーのデルタという。

.. math::

   \delta_{ij} = \begin{cases} 1 & (i = j) \\ 0 & (i \ne j) \end{cases}

:math:`\delta_{ij}` は単位行列の成分であり、:math:`\delta_{ij} a_j = a_i`\ （添字の付け替え）、:math:`\delta_{ii} = 3`、:math:`\partial_i x_j = \delta_{ij}` が成り立つ。

レヴィ＝チヴィタ記号
--------------------

次の記号をレヴィ＝チヴィタ記号（完全反対称記号）という。

.. math::

   \varepsilon_{ijk} = \begin{cases} 1 & ((i, j, k) = (1, 2, 3), (2, 3, 1), (3, 1, 2)) \\ -1 & ((i, j, k) = (3, 2, 1), (2, 1, 3), (1, 3, 2)) \\ 0 & (\text{添字に同じ数がある}) \end{cases}

添字を 2 つ入れ替えると符号が変わる（:math:`\varepsilon_{ijk} = -\varepsilon_{jik}`）。添字を巡回させても値は変わらない（:math:`\varepsilon_{ijk} = \varepsilon_{jki} = \varepsilon_{kij}`）。この記号を使うと、外積と回転は次のように書ける。

.. math::

   (\bm{a} \times \bm{b})_i = \varepsilon_{ijk} a_j b_k, \qquad (\nabla \times \bm{F})_i = \varepsilon_{ijk} \partial_j F_k

たとえば :math:`i = 1` のとき、0 でない項は :math:`(j, k) = (2, 3), (3, 2)` だけなので、:math:`(\bm{a} \times \bm{b})_1 = a_2 b_3 - a_3 b_2` となり、外積の定義と一致する。スカラー三重積は :math:`\bm{a} \cdot (\bm{b} \times \bm{c}) = \varepsilon_{ijk} a_i b_j c_k` であり、行列式と同じものである。

証明で中心となるのは、次の縮約の公式である。

.. math::
   :label: eq-appb-epsilon-delta

   \varepsilon_{ijk} \varepsilon_{imn} = \delta_{jm} \delta_{kn} - \delta_{jn} \delta_{km}

左辺は :math:`i` について和をとる。:math:`j \ne k` かつ :math:`m \ne n` でなければ両辺とも 0 である。:math:`j \ne k` のとき、和の中で 0 でない項は、:math:`i` が :math:`j` とも :math:`k` とも異なる 1 つの項だけである。その :math:`i` に対して :math:`\{m, n\}` も :math:`i` 以外の 2 つの数でなければならないので、左辺は :math:`(m, n) = (j, k)` なら 1、:math:`(m, n) = (k, j)` なら :math:`-1`、それ以外なら 0 となり、右辺と一致する。

対称と反対称の積は 0
--------------------

:math:`S_{jk} = S_{kj}`\ （対称）なら :math:`\varepsilon_{ijk} S_{jk} = 0` である。ダミー添字 :math:`j, k` の名前を入れ替えてから、:math:`\varepsilon` の反対称性と :math:`S` の対称性を使うと、次のように自分自身の符号を反転したものに等しくなるからである。

.. math::

   \varepsilon_{ijk} S_{jk} = \varepsilon_{ikj} S_{kj} = -\varepsilon_{ijk} S_{jk}

偏微分の順序は交換できる（:ref:`第 4 章 <ch04>`\ のシュワルツの定理）ので、:math:`\partial_j \partial_k` は :math:`j, k` について対称である。この事実が次の 2 つの公式の証明になる。

.. math::

   (\nabla \times \nabla f)_i &= \varepsilon_{ijk} \partial_j \partial_k f = 0 \\
   \nabla \cdot (\nabla \times \bm{F}) &= \partial_i (\varepsilon_{ijk} \partial_j F_k) = \varepsilon_{ijk} \partial_i \partial_j F_k = 0

公式の証明の例
--------------

ベクトル三重積
~~~~~~~~~~~~~~

:eq:`eq-appb-epsilon-delta` を使う。:math:`\varepsilon_{ijk} = \varepsilon_{kij}` と並べ替えてから縮約する。

.. math::

   [\bm{a} \times (\bm{b} \times \bm{c})]_i &= \varepsilon_{ijk} a_j (\varepsilon_{kmn} b_m c_n) = \varepsilon_{kij} \varepsilon_{kmn} a_j b_m c_n \\
   &= (\delta_{im} \delta_{jn} - \delta_{in} \delta_{jm}) a_j b_m c_n = b_i (a_j c_j) - c_i (a_j b_j)

したがって :math:`\bm{a} \times (\bm{b} \times \bm{c}) = \bm{b} (\bm{a} \cdot \bm{c}) - \bm{c} (\bm{a} \cdot \bm{b})` である。

回転の回転
~~~~~~~~~~

同じ手順で、:math:`\nabla \times (\nabla \times \bm{F})` の公式が得られる。

.. math::

   [\nabla \times (\nabla \times \bm{F})]_i &= \varepsilon_{ijk} \partial_j (\varepsilon_{kmn} \partial_m F_n) = \varepsilon_{kij} \varepsilon_{kmn} \partial_j \partial_m F_n \\
   &= (\delta_{im} \delta_{jn} - \delta_{in} \delta_{jm}) \partial_j \partial_m F_n = \partial_i (\partial_j F_j) - \partial_j \partial_j F_i

第 1 項は :math:`\nabla (\nabla \cdot \bm{F})` の第 :math:`i` 成分、第 2 項は :math:`\nabla^2 F_i` である。したがって :math:`\nabla \times (\nabla \times \bm{F}) = \nabla (\nabla \cdot \bm{F}) - \nabla^2 \bm{F}` となる。ベクトル三重積の公式で :math:`\bm{a} = \bm{b} = \nabla` と置いた形になっているが、微分の順序を気にせず形式的に置き換えてよいのは、この例のように :math:`\nabla` どうしの順序が交換できる場合に限る。

外積の発散
~~~~~~~~~~

積の微分（ライプニッツ則）を使う。

.. math::

   \nabla \cdot (\bm{F} \times \bm{G}) &= \partial_i (\varepsilon_{ijk} F_j G_k) = \varepsilon_{ijk} (\partial_i F_j) G_k + \varepsilon_{ijk} F_j (\partial_i G_k) \\
   &= G_k (\varepsilon_{kij} \partial_i F_j) - F_j (\varepsilon_{jik} \partial_i G_k) = \bm{G} \cdot (\nabla \times \bm{F}) - \bm{F} \cdot (\nabla \times \bm{G})

2 行目では、:math:`\varepsilon_{ijk} = \varepsilon_{kij}` と :math:`\varepsilon_{ijk} = -\varepsilon_{jik}` を使った。

数値による確認
--------------

:eq:`eq-appb-epsilon-delta` は、NumPy で :math:`\varepsilon_{ijk}` を 3×3×3 の配列として作り、``np.einsum`` で添字の和をとると確かめられる。``np.einsum`` の添字の文字列は、総和規約をそのまま書いたものになっている（NumPy の添字は 0 から始まる）。

.. code-block:: python
   :linenos:

   import numpy as np

   eps = np.zeros((3, 3, 3))
   for i, j, k in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
       eps[i, j, k] = 1.0   # 偶置換
       eps[i, k, j] = -1.0  # 奇置換
   delta = np.eye(3)

   left = np.einsum("ijk,imn->jkmn", eps, eps)
   right = np.einsum("jm,kn->jkmn", delta, delta) - np.einsum("jn,km->jkmn", delta, delta)
   print(np.array_equal(left, right))  # True

   a, b = np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0])
   print(np.einsum("ijk,j,k->i", eps, a, b), np.cross(a, b))  # 同じ値になる
