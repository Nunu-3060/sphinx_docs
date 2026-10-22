.. _ch02:

第 2 章 ベクトルの基礎
======================

この章では、本書全体で使うベクトルの演算を復習する。成分表示、和とスカラー倍、ノルムから始め、内積、外積、スカラー三重積とベクトル三重積を扱う。どれも、後の章で勾配・発散・回転や線積分・面積分を理解するための道具になる。

ベクトルと成分表示
------------------

:term:`ベクトル`\ は、大きさと向きを持つ量である。図では矢印で表し、矢印の長さが大きさ、矢印の向きがベクトルの向きを表す。始点の位置は問わないので、平行移動して重なる 2 本の矢印は同じベクトルを表す。これに対して、温度や質量のように大きさだけを持つ量をスカラーという。

3 次元の空間に直交座標系を取り、:math:`x, y, z` 軸の正の向きを向いた長さ 1 のベクトルを :math:`\bm{e}_x, \bm{e}_y, \bm{e}_z` とする。これらを基本単位ベクトルという。任意のベクトル :math:`\bm{a}` は、これらの組み合わせで

.. math::

   \bm{a} = a_x \bm{e}_x + a_y \bm{e}_y + a_z \bm{e}_z = (a_x, a_y, a_z)

と一通りに表せる。:math:`a_x, a_y, a_z` を :math:`\bm{a}` の成分といい、右辺の書き方を成分表示という。

原点 O を始点とし、点 P :math:`(x, y, z)` を終点とするベクトルを、点 P の\ :term:`位置ベクトル`\ といい、本書では :math:`\bm{r} = (x, y, z)` と書く。位置ベクトルを使うと、空間の点とベクトルを同じように扱える。

座標系は右手系に取る。:term:`右手系`\ とは、右手の親指、人差し指、中指を互いに直角に開いたとき、それぞれが :math:`x, y, z` 軸の正の向きになる座標系である。:math:`x` 軸から :math:`y` 軸へ右ねじを回すと、ねじが :math:`z` 軸の正の向きに進む、と言ってもよい。右手系か左手系かは、後で説明する外積の向きに影響する。

和、スカラー倍、ノルム
----------------------

ベクトルの和とスカラー倍は、成分ごとに計算する。

.. math::

   \bm{a} + \bm{b} &= (a_x + b_x, \ a_y + b_y, \ a_z + b_z) \\
   k \bm{a} &= (k a_x, \ k a_y, \ k a_z)

和 :math:`\bm{a} + \bm{b}` は、:math:`\bm{a}` の終点に :math:`\bm{b}` の始点をつないだときの、:math:`\bm{a}` の始点から :math:`\bm{b}` の終点へ向かう矢印である。スカラー倍 :math:`k \bm{a}` は、:math:`\bm{a}` の長さを :math:`|k|` 倍し、:math:`k < 0` なら向きを反対にしたものである。

ベクトルの大きさ（長さ）を\ :term:`ノルム`\ といい、:math:`|\bm{a}|` と書く。三平方の定理から

.. math::

   |\bm{a}| = \sqrt{a_x^2 + a_y^2 + a_z^2}

である。ノルムが 1 のベクトルを\ :term:`単位ベクトル`\ という。0 でないベクトル :math:`\bm{a}` を自分のノルムで割った :math:`\bm{a} / |\bm{a}|` は、:math:`\bm{a}` と同じ向きの単位ベクトルになる。この操作を正規化という。向きだけが必要な場面（法線の向き、進む方向など）で頻繁に使う。

内積
----

定義と成分による計算
~~~~~~~~~~~~~~~~~~~~

2 つのベクトル :math:`\bm{a}, \bm{b}` のなす角を :math:`\theta`\ （:math:`0 \le \theta \le \pi`）とするとき、

.. math::

   \bm{a} \cdot \bm{b} = |\bm{a}| \, |\bm{b}| \cos \theta

を :math:`\bm{a}` と :math:`\bm{b}` の\ :term:`内積`\ （inner product、dot product）という。内積の値はスカラーである。成分で書くと

.. math::

   \bm{a} \cdot \bm{b} = a_x b_x + a_y b_y + a_z b_z

となる。2 つの式が等しいことは、余弦定理 :math:`|\bm{a} - \bm{b}|^2 = |\bm{a}|^2 + |\bm{b}|^2 - 2 |\bm{a}| |\bm{b}| \cos \theta` の左辺を成分で展開すると確かめられる。

内積には次の性質がある。

* :math:`\bm{a} \cdot \bm{b} = \bm{b} \cdot \bm{a}`\ （交換法則）
* :math:`\bm{a} \cdot (\bm{b} + \bm{c}) = \bm{a} \cdot \bm{b} + \bm{a} \cdot \bm{c}`\ （分配法則）
* :math:`\bm{a} \cdot \bm{a} = |\bm{a}|^2`
* 0 でない :math:`\bm{a}, \bm{b}` について、:math:`\bm{a} \cdot \bm{b} = 0` と :math:`\bm{a} \perp \bm{b}`\ （直交する）は同じことである。

内積の符号は、2 つのベクトルの向きの関係を表す。なす角が鋭角なら正、直角なら 0、鈍角なら負になる。基本単位ベクトルどうしの内積は :math:`\bm{e}_x \cdot \bm{e}_x = 1`、:math:`\bm{e}_x \cdot \bm{e}_y = 0` などであり、:math:`\bm{a} \cdot \bm{e}_x = a_x` のように、内積で成分を取り出せる。

内積の式から、なす角は

.. math::

   \cos \theta = \frac{\bm{a} \cdot \bm{b}}{|\bm{a}| \, |\bm{b}|}

で求められる。右辺の絶対値が 1 を超えないことは、:term:`コーシー・シュワルツの不等式` :math:`|\bm{a} \cdot \bm{b}| \le |\bm{a}| \, |\bm{b}|` で保証される。等号は 2 つのベクトルが平行なときに成り立つ。

正射影
~~~~~~

内積の最も重要な使い方は、あるベクトルの「ある方向の成分」を取り出すことである。単位ベクトル :math:`\bm{u}` に対して、:math:`\bm{a} \cdot \bm{u} = |\bm{a}| \cos \theta` は、:math:`\bm{a}` と :math:`\bm{u}` の始点をそろえ、:math:`\bm{a}` の終点から :math:`\bm{u}` の方向の直線に垂線を下ろしたときにできる影の長さ（符号付き）である。ここで :math:`\theta` は :math:`\bm{a}` と :math:`\bm{u}` のなす角である。影をベクトルとして表した

.. math::

   (\bm{a} \cdot \bm{u}) \, \bm{u} = \frac{\bm{a} \cdot \bm{b}}{\bm{b} \cdot \bm{b}} \, \bm{b} \qquad \left( \bm{u} = \frac{\bm{b}}{|\bm{b}|} \right)

を、:math:`\bm{a}` の :math:`\bm{b}` 方向への\ :term:`正射影`\ という。:math:`\bm{a}` から正射影を引いた残りは :math:`\bm{b}` に直交する。つまり、任意のベクトルは「ある方向の成分」と「それに垂直な成分」に分けられる。

この考え方は本書の随所に現れる。たとえば、:ref:`第 5 章 <ch05>`\ の方向微分は勾配の正射影であり、:ref:`第 12 章 <ch12>`\ の流束は流れの速度の法線方向の成分を集めたものである。

力学の例として、物体が一定の力 :math:`\bm{F}` を受けながら、まっすぐ :math:`\bm{d}` だけ移動したとする。力がする仕事は、力の移動方向の成分と移動距離の積

.. math::

   W = |\bm{F}| \cos \theta \cdot |\bm{d}| = \bm{F} \cdot \bm{d}

である。移動方向に垂直な力（たとえば、円運動の向心力）は仕事をしない。:ref:`第 11 章 <ch11>`\ では、この式を曲がった経路に広げて線積分を定義する。

外積
----

定義
~~~~

3 次元のベクトル :math:`\bm{a}, \bm{b}` に対して、次の性質を持つベクトルを :math:`\bm{a}` と :math:`\bm{b}` の\ :term:`外積`\ （cross product、ベクトル積）といい、:math:`\bm{a} \times \bm{b}` と書く。

* 向き：:math:`\bm{a}` と :math:`\bm{b}` の両方に垂直で、:math:`\bm{a}` から :math:`\bm{b}` へ右ねじを回したときにねじが進む向き
* 大きさ：:math:`|\bm{a} \times \bm{b}| = |\bm{a}| \, |\bm{b}| \sin \theta`\ （:math:`\bm{a}` と :math:`\bm{b}` が作る平行四辺形の面積）

内積がスカラーを返すのに対し、外積はベクトルを返す。:numref:`fig-ch02-cross-product` は、:math:`xy` 平面上の 2 つのベクトルの外積が :math:`z` 軸の正の向きを向く様子を示したものである。

.. figure:: ../build/figures/ch02_cross_product.svg
   :name: fig-ch02-cross-product
   :width: 60%
   :align: center

   外積の向きと、平行四辺形の面積

.. literalinclude:: ../examples/ch02_cross_product.py
   :pyobject: create_figure
   :lineno-match:
   :caption: ch02_cross_product.py の create_figure()

サンプルの全体：:download:`ch02_cross_product.py <../examples/ch02_cross_product.py>`

成分による計算
~~~~~~~~~~~~~~

外積を成分で書くと次のようになる。

.. math::

   \bm{a} \times \bm{b} = (a_y b_z - a_z b_y, \ a_z b_x - a_x b_z, \ a_x b_y - a_y b_x)

覚えにくい式だが、形式的な行列式

.. math::

   \bm{a} \times \bm{b} =
   \begin{vmatrix}
   \bm{e}_x & \bm{e}_y & \bm{e}_z \\
   a_x & a_y & a_z \\
   b_x & b_y & b_z
   \end{vmatrix}

を 1 行目について展開すると得られる。また、:math:`x` 成分は添字 :math:`y, z` から、:math:`y` 成分は :math:`z, x` から、:math:`z` 成分は :math:`x, y` から作られている（:math:`x \to y \to z \to x` と循環させる）ことに注目すると覚えやすい。この覚え方は\ :ref:`第 7 章 <ch07>`\ の回転の成分表示でも役に立つ。

基本単位ベクトルどうしの外積は

.. math::

   \bm{e}_x \times \bm{e}_y = \bm{e}_z, \quad \bm{e}_y \times \bm{e}_z = \bm{e}_x, \quad \bm{e}_z \times \bm{e}_x = \bm{e}_y

であり、同じベクトルどうしの外積は :math:`\bm{0}` である。

外積の性質
~~~~~~~~~~

外積には次の性質がある。

* :math:`\bm{b} \times \bm{a} = -\bm{a} \times \bm{b}`\ （順序を入れ替えると符号が変わる。交換法則は成り立たない）
* :math:`\bm{a} \times \bm{a} = \bm{0}`。より一般に、平行な 2 つのベクトルの外積は :math:`\bm{0}` である。
* :math:`\bm{a} \times (\bm{b} + \bm{c}) = \bm{a} \times \bm{b} + \bm{a} \times \bm{c}`\ （分配法則）
* :math:`(\bm{a} \times \bm{b}) \cdot \bm{a} = (\bm{a} \times \bm{b}) \cdot \bm{b} = 0`\ （外積は元の 2 つのベクトルに垂直）
* 結合法則は成り立たない。一般に :math:`\bm{a} \times (\bm{b} \times \bm{c}) \ne (\bm{a} \times \bm{b}) \times \bm{c}` である。

外積の工学での使い方
~~~~~~~~~~~~~~~~~~~~

外積は、「2 つの方向に垂直な方向」と「平行四辺形の面積」を同時に与える。代表的な使い方を挙げる。

* 法線ベクトル：平面上の 2 つの方向 :math:`\bm{a}, \bm{b}` の外積は、その平面に垂直である。CG では、三角形ポリゴンの 2 辺の外積で面の法線を求める。:ref:`第 12 章 <ch12>`\ では、曲面の法線と面積を同じ方法で求める。
* トルク（力のモーメント）：原点から見た位置 :math:`\bm{r}` の点に力 :math:`\bm{F}` を加えたときの、原点のまわりのトルクは :math:`\bm{\tau} = \bm{r} \times \bm{F}` である。向きが回転軸、大きさが回そうとする強さを表す。
* 回転する物体の速度：角速度ベクトル :math:`\bm{\Omega}`\ （向きが回転軸、大きさが角速度）で回転する剛体の、位置 :math:`\bm{r}` の点の速度は :math:`\bm{v} = \bm{\Omega} \times \bm{r}` である。この式は\ :ref:`第 7 章 <ch07>`\ で回転の意味を調べるときに使う。
* ローレンツ力：磁束密度 :math:`\bm{B}` の中を速度 :math:`\bm{v}` で動く電荷 :math:`q` が受ける力は :math:`q \bm{v} \times \bm{B}` である。モーターの原理である。

外積は 3 次元に特有の演算である。2 次元のベクトル :math:`(a_x, a_y)`、:math:`(b_x, b_y)` については、:math:`z` 成分を 0 とした 3 次元のベクトルとみなすと、外積の :math:`z` 成分 :math:`a_x b_y - a_y b_x` だけが残る。この値は、2 つのベクトルが作る平行四辺形の符号付き面積であり、:math:`\bm{a}` から :math:`\bm{b}` へ反時計回りなら正になる。:ref:`第 13 章 <ch13>`\ の面積公式で使う。

三重積
------

スカラー三重積
~~~~~~~~~~~~~~

3 つのベクトルについて、:math:`\bm{a} \cdot (\bm{b} \times \bm{c})` を\ :term:`スカラー三重積`\ という。:math:`\bm{b} \times \bm{c}` の大きさは :math:`\bm{b}` と :math:`\bm{c}` が作る平行四辺形の面積で、向きはその面に垂直である。そこに :math:`\bm{a}` との内積を取ると、:math:`\bm{a}` の面に垂直な成分（高さ）が掛かる。したがって、スカラー三重積の絶対値は、3 つのベクトルが作る平行六面体の体積である。符号は、:math:`\bm{a}, \bm{b}, \bm{c}` がこの順に右手系をなすときに正になる。

成分で書くと、スカラー三重積は 3 つのベクトルを並べた行列式に等しい。

.. math::

   \bm{a} \cdot (\bm{b} \times \bm{c}) =
   \begin{vmatrix}
   a_x & a_y & a_z \\
   b_x & b_y & b_z \\
   c_x & c_y & c_z
   \end{vmatrix}

行列式の性質から、3 つのベクトルを巡回的に入れ替えても値は変わらない。

.. math::

   \bm{a} \cdot (\bm{b} \times \bm{c}) = \bm{b} \cdot (\bm{c} \times \bm{a}) = \bm{c} \cdot (\bm{a} \times \bm{b})

スカラー三重積が 0 になるのは、3 つのベクトルが同じ平面に乗っている（平行六面体がつぶれている）ときである。:ref:`第 10 章 <ch10>`\ では、変数変換で体積がどう変わるかを、この「行列式は体積」という見方で説明する。

ベクトル三重積
~~~~~~~~~~~~~~

:math:`\bm{a} \times (\bm{b} \times \bm{c})` をベクトル三重積という。次の公式が成り立つ。

.. math::
   :label: eq-ch02-bac-cab

   \bm{a} \times (\bm{b} \times \bm{c}) = (\bm{a} \cdot \bm{c}) \, \bm{b} - (\bm{a} \cdot \bm{b}) \, \bm{c}

右辺の並びから「バック・キャブ（BAC − CAB）の公式」と呼ばれることがある。:math:`\bm{b} \times \bm{c}` は :math:`\bm{b}` と :math:`\bm{c}` が張る平面に垂直なので、それとさらに外積を取った左辺は、:math:`\bm{b}` と :math:`\bm{c}` が張る平面の中にある。右辺が :math:`\bm{b}` と :math:`\bm{c}` の組み合わせになっているのはそのためである。この公式は、:ref:`第 8 章 <ch08>`\ で回転の回転 :math:`\nabla \times (\nabla \times \bm{F})` の公式を導くときの手がかりになる。成分による証明は\ :ref:`付録 B <appendix-b>` で示す。

NumPy による計算
----------------

これまでの演算を NumPy で計算してみる。NumPy では、ベクトルを 1 次元の配列で表す。内積は ``@`` 演算子（または ``np.dot``）、外積は ``np.cross``、ノルムは ``np.linalg.norm`` で計算できる。

.. literalinclude:: ../examples/ch02_vector_ops.py
   :pyobject: report
   :lineno-match:
   :caption: ch02_vector_ops.py の report()

サンプルの全体：:download:`ch02_vector_ops.py <../examples/ch02_vector_ops.py>`

.. literalinclude:: ../build/outputs/ch02_vector_ops.txt
   :language: text
   :caption: ch02_vector_ops.py の実行結果

:math:`\bm{a} = (1, 2, 2)`、:math:`\bm{b} = (3, 0, 4)` の内積は :math:`3 + 0 + 8 = 11` であり、:math:`|\bm{a}| = 3`、:math:`|\bm{b}| = 5` なので :math:`\cos \theta = 11/15`、なす角は約 42.8 度である。外積 :math:`\bm{a} \times \bm{b} = (8, 2, -6)` は、:math:`\bm{a}` とも :math:`\bm{b}` とも内積が 0 であり、両方に垂直であることが確かめられる。順序を入れ替えた :math:`\bm{b} \times \bm{a}` は符号が反転している。:math:`\bm{c} = (0, 1, 1)` を加えたスカラー三重積は行列式と一致し、ベクトル三重積は :eq:`eq-ch02-bac-cab` の右辺と一致している。

この章のまとめ
--------------

* ベクトルは大きさと向きを持つ量であり、基本単位ベクトル :math:`\bm{e}_x, \bm{e}_y, \bm{e}_z` を使って成分表示できる。座標系は右手系に取る。
* 内積 :math:`\bm{a} \cdot \bm{b} = |\bm{a}| |\bm{b}| \cos \theta` はスカラーであり、なす角、直交の判定、ある方向の成分（正射影）、仕事の計算に使う。
* 外積 :math:`\bm{a} \times \bm{b}` は 2 つのベクトルに垂直なベクトルで、大きさは平行四辺形の面積である。法線、トルク、回転の速度に使う。順序を入れ替えると符号が変わる。
* スカラー三重積は平行六面体の符号付き体積で、行列式に等しい。
* ベクトル三重積には :math:`\bm{a} \times (\bm{b} \times \bm{c}) = (\bm{a} \cdot \bm{c}) \bm{b} - (\bm{a} \cdot \bm{b}) \bm{c}` が成り立つ。
