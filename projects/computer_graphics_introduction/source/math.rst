ベクトルと行列
==============

3 次元の CG では、点の位置、面の向き、光の向きをベクトルで表し、物体の移動や回転、カメラから見た画面への投影を行列で表す。本章では、以降の章で使うベクトルと行列の計算をまとめる。

本章のコードは NumPy の関数を直接使う例と、``cg_utils.py`` にある。

ベクトル
--------

3 次元のベクトル :math:`\mathbf{v} = (v_x, v_y, v_z)` は、CG では主に次の 2 つの意味で使われる。

* 位置: 原点から見た点の位置。頂点の座標、カメラの位置など。
* 向き: 大きさと向きだけを持ち、位置を持たない量。面の法線、光の向き、視線の向きなど。

2 つの点 :math:`\mathbf{p}`、:math:`\mathbf{q}` の差 :math:`\mathbf{q} - \mathbf{p}` は、:math:`\mathbf{p}` から :math:`\mathbf{q}` に向かう向きのベクトルである。

ベクトルの長さ（ノルム）は :math:`|\mathbf{v}| = \sqrt{v_x^2 + v_y^2 + v_z^2}` である。長さが 1 のベクトルを単位ベクトルといい、ベクトルを長さで割って単位ベクトルにすることを正規化という。向きだけが意味を持つベクトル（法線、光の向きなど）は、正規化して使うことが多い。

.. literalinclude:: ../examples/cg_utils.py
   :language: python
   :pyobject: normalize
   :lineno-match:

この関数は、配列の末尾の軸をベクトルとみなすので、形状が（点の数, 3）や（高さ, 幅, 3）の配列に含まれる多数のベクトルを、まとめて正規化できる。

内積
----

2 つのベクトルの内積は、次の式で定義される。

.. math::

   \mathbf{a} \cdot \mathbf{b} = a_x b_x + a_y b_y + a_z b_z = |\mathbf{a}| |\mathbf{b}| \cos \theta

:math:`\theta` は 2 つのベクトルのなす角である。2 つのベクトルが単位ベクトルであれば、内積は :math:`\cos \theta` に等しい。内積は、CG で最もよく使う計算の 1 つである。

* 2 つの向きがどれだけそろっているかを表す。同じ向きなら 1、直交していれば 0、逆向きなら -1 である。:doc:`shading`\ では、面の法線と光の向きの内積で、面の明るさを求める。
* 内積の符号で、2 つの向きが同じ側を向いているかを判定できる。
* 単位ベクトル :math:`\mathbf{n}` との内積 :math:`\mathbf{v} \cdot \mathbf{n}` は、ベクトル :math:`\mathbf{v}` の :math:`\mathbf{n}` の方向の成分の長さである。

.. code-block:: python
   :linenos:

   import numpy as np

   a = np.array([1.0, 0.0, 0.0])
   b = np.array([1.0, 1.0, 0.0]) / np.sqrt(2.0)
   print(np.dot(a, b))  # 0.7071... (= cos 45°)

外積
----

2 つのベクトルの外積は、次の式で定義されるベクトルである。

.. math::

   \mathbf{a} \times \mathbf{b} = (a_y b_z - a_z b_y,\ a_z b_x - a_x b_z,\ a_x b_y - a_y b_x)

外積には次の性質がある。

* :math:`\mathbf{a}` と :math:`\mathbf{b}` の両方に直交する。そのため、三角形の 2 辺の外積から、三角形の面の法線を求められる。
* 向きは右手の法則にしたがう。右手の親指を :math:`\mathbf{a}`、人差し指を :math:`\mathbf{b}` に合わせたとき、中指の向きが :math:`\mathbf{a} \times \mathbf{b}` である。
* 長さは、:math:`\mathbf{a}` と :math:`\mathbf{b}` が作る平行四辺形の面積 :math:`|\mathbf{a}| |\mathbf{b}| \sin \theta` に等しい。
* 順序を入れ替えると向きが逆になる（:math:`\mathbf{b} \times \mathbf{a} = -\mathbf{a} \times \mathbf{b}`）。

三角形の頂点 :math:`\mathbf{v}_0`、:math:`\mathbf{v}_1`、:math:`\mathbf{v}_2` が、ある側から見て反時計回りに並んでいるとき、:math:`(\mathbf{v}_1 - \mathbf{v}_0) \times (\mathbf{v}_2 - \mathbf{v}_0)` はその側を向く。本資料では、三角形の頂点を、物体の外側から見て反時計回りに並べる約束にしている。

.. code-block:: python
   :linenos:

   import numpy as np

   v0 = np.array([0.0, 0.0, 0.0])
   v1 = np.array([1.0, 0.0, 0.0])
   v2 = np.array([0.0, 1.0, 0.0])
   print(np.cross(v1 - v0, v2 - v0))  # [0. 0. 1.]

:doc:`raster2d`\ のエッジ関数は、z 成分を 0 とした 2 次元のベクトルの外積の z 成分である。

行列と線形変換
--------------

3 × 3 の行列 :math:`M` をベクトル :math:`\mathbf{v}` に掛けると、新しいベクトル :math:`M \mathbf{v}` が得られる。拡大縮小や回転は、このような行列の掛け算で表せる。たとえば、z 軸のまわりに角度 :math:`\theta` だけ回転する行列は次のとおりである。

.. math::

   R_z(\theta) =
   \begin{pmatrix}
   \cos \theta & -\sin \theta & 0 \\
   \sin \theta & \cos \theta & 0 \\
   0 & 0 & 1
   \end{pmatrix}

行列を使う利点は、複数の変換を 1 つの行列にまとめられることである。ベクトル :math:`\mathbf{v}` に変換 :math:`A` を行ってから変換 :math:`B` を行った結果は :math:`B (A \mathbf{v}) = (B A) \mathbf{v}` なので、あらかじめ :math:`BA` を計算しておけば、何万もの頂点に対して 1 回の掛け算で済む。

ただし、行列の積は一般に交換できない（:math:`BA \ne AB`）。「回転してから移動する」と「移動してから回転する」は異なる結果になる。この違いは\ :doc:`transform`\ で図を使って確かめる。本資料のように列ベクトルを使う場合、先に行う変換が右側にくることに注意する。

NumPy では、行列の積を ``@`` 演算子で書く。次の例は、x 軸の向きの単位ベクトルを z 軸のまわりに 90 度回転させている。結果は y 軸の向きの単位ベクトル (0, 1, 0) になる。x 成分が 0 ではなくわずかな値になっているのは、浮動小数点数の丸め誤差のためである。

.. code-block:: python
   :linenos:

   import numpy as np

   theta = np.radians(90.0)
   rz = np.array([
       [np.cos(theta), -np.sin(theta), 0.0],
       [np.sin(theta), np.cos(theta), 0.0],
       [0.0, 0.0, 1.0],
   ])
   print(rz @ np.array([1.0, 0.0, 0.0]))  # [6.123234e-17 1.000000e+00 0.000000e+00]

同次座標
--------

平行移動 :math:`\mathbf{v} + \mathbf{t}` は、3 × 3 の行列の掛け算では表せない。原点 :math:`\mathbf{0}` にどんな 3 × 3 の行列を掛けても、結果は原点のままだからである。

そこで、3 次元の点 :math:`(x, y, z)` に 4 つ目の成分 :math:`w = 1` を加えた :math:`(x, y, z, 1)` で点を表し、4 × 4 の行列で変換する。この表し方を同次座標という。平行移動は次の行列で表せる。

.. math::

   \begin{pmatrix}
   1 & 0 & 0 & t_x \\
   0 & 1 & 0 & t_y \\
   0 & 0 & 1 & t_z \\
   0 & 0 & 0 & 1
   \end{pmatrix}
   \begin{pmatrix} x \\ y \\ z \\ 1 \end{pmatrix}
   =
   \begin{pmatrix} x + t_x \\ y + t_y \\ z + t_z \\ 1 \end{pmatrix}

同次座標を使うと、拡大縮小、回転、平行移動、そして\ :doc:`transform`\ で説明する透視投影を、全て 4 × 4 の行列の掛け算で統一的に扱える。GPU やグラフィックス API が 4 × 4 の行列を基本としているのは、このためである。

同次座標には、次の約束がある。

* 向きを表すベクトルは :math:`w = 0` とする。すると、平行移動の行列を掛けても値が変わらない。向きは位置を持たないので、平行移動の影響を受けないのが正しい。
* :math:`(x, y, z, w)` と、それを定数倍した :math:`(kx, ky, kz, kw)` は、同じ点 :math:`(x/w, y/w, z/w)` を表す。:math:`w` で割って 3 次元の点に戻すことを、透視除算という。
