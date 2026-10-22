.. _ch09:

第 9 章 曲線座標系
==================

円や球、円筒のような対称性を持つ問題は、直交座標 :math:`(x, y, z)` よりも、極座標、円柱座標、球座標を使うと式が簡単になる。この章では、これらの座標系の定義と基底ベクトルの性質を説明し、スケール因子を使って勾配・発散・回転・ラプラシアンを直交曲線座標系で表す方法を導く。

曲線座標系が必要な理由
----------------------

点電荷がつくる電場の強さは、電荷からの距離 :math:`r` だけで決まる。直交座標で書くと

.. math::

   \bm{E} = \frac{q}{4 \pi \varepsilon_0} \frac{(x, y, z)}{(x^2 + y^2 + z^2)^{3/2}}

となり、発散を計算するには 3 つの成分をそれぞれ偏微分しなければならない。一方、後で説明する球座標を使うと :math:`\bm{E} = \dfrac{q}{4 \pi \varepsilon_0 r^2} \bm{e}_r` と 1 つの成分だけで書ける。問題の対称性に合った座標系を選ぶと、場の式も計算も簡単になる。

ただし、曲線座標系では基底ベクトルの向きが場所によって変わる。そのため、勾配・発散・回転を直交座標の式の :math:`x, y, z` を単純に置き換えて求めることはできない。この章の目標は、その違いを正しく扱う方法を身に付けることである。

極座標
------

平面上の点の位置を、原点からの距離 :math:`r` と、:math:`x` 軸から反時計回りに測った角度 :math:`\theta` で表すのが\ :term:`極座標`\ である。直交座標との関係は次のとおりである。

.. math::

   x = r \cos\theta, \qquad y = r \sin\theta \qquad (r \ge 0, \ 0 \le \theta < 2\pi)

:math:`r` だけを少し増やしたときに点が動く向きの単位ベクトルを :math:`\bm{e}_r`、:math:`\theta` だけを少し増やしたときに点が動く向きの単位ベクトルを :math:`\bm{e}_\theta` とする。位置ベクトル :math:`\bm{r} = (r\cos\theta, r\sin\theta)` を偏微分すると

.. math::

   \frac{\partial \bm{r}}{\partial r} = (\cos\theta, \sin\theta), \qquad
   \frac{\partial \bm{r}}{\partial \theta} = (-r\sin\theta, r\cos\theta)

となる。それぞれの大きさは :math:`1` と :math:`r` なので、大きさで割って単位ベクトルにすると

.. math::

   \bm{e}_r = (\cos\theta, \sin\theta), \qquad \bm{e}_\theta = (-\sin\theta, \cos\theta)

を得る。:math:`\bm{e}_r \cdot \bm{e}_\theta = 0` なので、2 つは直交している。

:numref:`fig-ch09-polar-basis` は、いくつかの点で :math:`\bm{e}_r` と :math:`\bm{e}_\theta` を描いたものである。直交座標の :math:`\bm{e}_x`, :math:`\bm{e}_y` はどこでも同じ向きだが、極座標の基底ベクトルは点の位置（角度 :math:`\theta`）によって向きが変わる。

.. figure:: ../build/figures/ch09_polar_basis.svg
   :name: fig-ch09-polar-basis
   :width: 70%
   :align: center

   極座標の座標曲線と基底ベクトル

基底ベクトルを :math:`\theta` で微分すると、次のようになる。

.. math::

   \frac{\partial \bm{e}_r}{\partial \theta} = \bm{e}_\theta, \qquad
   \frac{\partial \bm{e}_\theta}{\partial \theta} = -\bm{e}_r

ベクトル場 :math:`\bm{F} = F_r \bm{e}_r + F_\theta \bm{e}_\theta` を微分するときは、成分 :math:`F_r`, :math:`F_\theta` だけでなく、基底ベクトル自体の変化も考えなければならない。これが、曲線座標系で発散や回転の式が複雑になる原因である。

.. literalinclude:: ../examples/ch09_polar_basis.py
   :pyobject: polar_basis
   :lineno-match:
   :caption: ch09_polar_basis.py の polar_basis()

サンプルの全体：:download:`ch09_polar_basis.py <../examples/ch09_polar_basis.py>`

円柱座標
--------

3 次元の点を、:math:`xy` 平面への射影を極座標で表し、高さ :math:`z` を加えて表すのが\ :term:`円柱座標`\ である。本書では、:math:`z` 軸からの距離を :math:`\rho`、方位角を :math:`\phi` と書く。

.. math::

   x = \rho \cos\phi, \qquad y = \rho \sin\phi, \qquad z = z \qquad (\rho \ge 0, \ 0 \le \phi < 2\pi)

基底ベクトルは次の 3 つである。

.. math::

   \bm{e}_\rho = (\cos\phi, \sin\phi, 0), \qquad
   \bm{e}_\phi = (-\sin\phi, \cos\phi, 0), \qquad
   \bm{e}_z = (0, 0, 1)

:math:`\rho` が一定の面は :math:`z` 軸を中心とする円筒面、:math:`\phi` が一定の面は :math:`z` 軸を含む半平面、:math:`z` が一定の面は水平な平面である。円管の中の流れ、電線のまわりの磁場、回転軸のある機械など、軸のまわりの対称性を持つ問題に向いている。

球座標
------

3 次元の点を、原点からの距離 :math:`r`、:math:`z` 軸から測った角度 :math:`\theta`\ （天頂角）、:math:`x` 軸から :math:`xy` 平面内で測った角度 :math:`\phi`\ （方位角）で表すのが\ :term:`球座標`\ である（:numref:`fig-ch09-spherical-basis`）。

.. math::

   x = r \sin\theta \cos\phi, \qquad y = r \sin\theta \sin\phi, \qquad z = r \cos\theta
   \qquad (r \ge 0, \ 0 \le \theta \le \pi, \ 0 \le \phi < 2\pi)

基底ベクトルは次のとおりである。

.. math::

   \bm{e}_r &= (\sin\theta\cos\phi, \ \sin\theta\sin\phi, \ \cos\theta) \\
   \bm{e}_\theta &= (\cos\theta\cos\phi, \ \cos\theta\sin\phi, \ -\sin\theta) \\
   \bm{e}_\phi &= (-\sin\phi, \ \cos\phi, \ 0)

:math:`\bm{e}_r` は原点から外向き、:math:`\bm{e}_\theta` は経線に沿って南向き（:math:`\theta` が増える向き）、:math:`\bm{e}_\phi` は緯線に沿って東向きである。:math:`(\bm{e}_r, \bm{e}_\theta, \bm{e}_\phi)` はこの順に右手系をなし、:math:`\bm{e}_r \times \bm{e}_\theta = \bm{e}_\phi` が成り立つ。

.. figure:: ../build/figures/ch09_spherical_basis.svg
   :name: fig-ch09-spherical-basis
   :width: 65%
   :align: center

   球座標の意味と点 P での基底ベクトル

.. note::

   2 次元の極座標の :math:`\theta` は :math:`x` 軸からの角度だが、球座標の :math:`\theta` は :math:`z` 軸からの角度である。また、物理と数学の教科書で :math:`\theta` と :math:`\phi` の役割が逆の場合がある。本書は物理で一般的な記法（:math:`\theta` が天頂角、:math:`\phi` が方位角）に従う。他の資料を読むときは、どちらの記法かを最初に確認するとよい。

球座標は、点電荷や惑星の重力のように、1 点を中心とする対称性（球対称性）を持つ問題に向いている。

.. literalinclude:: ../examples/ch09_spherical_basis.py
   :pyobject: spherical_basis
   :lineno-match:
   :caption: ch09_spherical_basis.py の spherical_basis()

サンプルの全体：:download:`ch09_spherical_basis.py <../examples/ch09_spherical_basis.py>`

スケール因子と線素・面素・体積素
--------------------------------

直交曲線座標系
~~~~~~~~~~~~~~

一般に、3 つの数 :math:`(u_1, u_2, u_3)` で点の位置 :math:`\bm{r}(u_1, u_2, u_3)` を表す方法を曲線座標系という。各点で 3 つの基底ベクトルが互いに直交するものを\ :term:`直交曲線座標系`\ という。円柱座標と球座標は直交曲線座標系である。本書では直交曲線座標系だけを扱う。

スケール因子
~~~~~~~~~~~~

座標 :math:`u_i` を :math:`du_i` だけ増やしたとき、点が実際に動く距離は :math:`du_i` そのものではない。たとえば極座標で :math:`\theta` を :math:`d\theta` だけ増やすと、点は半径 :math:`r` の円周に沿って :math:`r \, d\theta` だけ動く。この倍率を\ :term:`スケール因子`\ といい、次の式で定義する。

.. math::

   h_i = \left| \frac{\partial \bm{r}}{\partial u_i} \right|

基底ベクトルは :math:`\bm{e}_i = \dfrac{1}{h_i} \dfrac{\partial \bm{r}}{\partial u_i}` であり、位置の微小な変化は

.. math::

   d\bm{r} = h_1 \, du_1 \, \bm{e}_1 + h_2 \, du_2 \, \bm{e}_2 + h_3 \, du_3 \, \bm{e}_3

と書ける。主な座標系のスケール因子を\ :numref:`table-ch09-scale-factors` に示す。

.. list-table:: 主な座標系のスケール因子
   :name: table-ch09-scale-factors
   :header-rows: 1
   :widths: 30 30 40

   * - 座標系
     - 座標
     - スケール因子
   * - 直交座標
     - :math:`(x, y, z)`
     - :math:`h_x = 1, \ h_y = 1, \ h_z = 1`
   * - 円柱座標
     - :math:`(\rho, \phi, z)`
     - :math:`h_\rho = 1, \ h_\phi = \rho, \ h_z = 1`
   * - 球座標
     - :math:`(r, \theta, \phi)`
     - :math:`h_r = 1, \ h_\theta = r, \ h_\phi = r \sin\theta`

球座標の :math:`h_\phi = r \sin\theta` は、:math:`\phi` を変えたとき点が動く円（緯線）の半径が :math:`r \sin\theta` であることを表している。

線素・面素・体積素
~~~~~~~~~~~~~~~~~~

基底ベクトルが直交しているので、微小な移動の長さ（線素）は三平方の定理から求まる。

.. math::

   ds^2 = |d\bm{r}|^2 = h_1^2 \, du_1^2 + h_2^2 \, du_2^2 + h_3^2 \, du_3^2

座標を :math:`du_1, du_2, du_3` だけ変えてできる微小な領域は、辺の長さが :math:`h_1 du_1`, :math:`h_2 du_2`, :math:`h_3 du_3` の直方体とみなせる。したがって、:math:`u_3` が一定の面上の\ :term:`面素`\ と\ :term:`体積素`\ は次のようになる。

.. math::

   dS = h_1 h_2 \, du_1 \, du_2, \qquad dV = h_1 h_2 h_3 \, du_1 \, du_2 \, du_3

円柱座標と球座標の体積素は次のとおりである。

.. math::

   dV = \rho \, d\rho \, d\phi \, dz \quad \text{（円柱座標）}, \qquad
   dV = r^2 \sin\theta \, dr \, d\theta \, d\phi \quad \text{（球座標）}

半径 :math:`R` の球面上の面素は :math:`dS = h_\theta h_\phi \, d\theta \, d\phi = R^2 \sin\theta \, d\theta \, d\phi` である。これらは重積分の変数変換で現れるヤコビアンと一致する。積分での使い方は\ :ref:`第 10 章 <ch10>`\ と\ :ref:`第 12 章 <ch12>`\ で説明する。

直交曲線座標系での勾配
----------------------

勾配は、全微分 :math:`df = \nabla f \cdot d\bm{r}` を満たすベクトルとして特徴付けられる（:ref:`第 5 章 <ch05>`）。曲線座標でも :math:`f` の全微分は

.. math::

   df = \frac{\partial f}{\partial u_1} du_1 + \frac{\partial f}{\partial u_2} du_2 + \frac{\partial f}{\partial u_3} du_3

である。:math:`\nabla f = G_1 \bm{e}_1 + G_2 \bm{e}_2 + G_3 \bm{e}_3` とおき、:math:`d\bm{r} = \sum_i h_i \, du_i \, \bm{e}_i` との内積が :math:`df` に等しいとすると :math:`G_i h_i = \partial f / \partial u_i` を得る。したがって

.. math::

   \nabla f = \frac{1}{h_1} \frac{\partial f}{\partial u_1} \bm{e}_1
            + \frac{1}{h_2} \frac{\partial f}{\partial u_2} \bm{e}_2
            + \frac{1}{h_3} \frac{\partial f}{\partial u_3} \bm{e}_3

となる。:math:`1/h_i` は、座標の変化を実際の距離に直すための係数である。円柱座標と球座標では次のようになる。

.. math::

   \nabla f &= \frac{\partial f}{\partial \rho} \bm{e}_\rho + \frac{1}{\rho} \frac{\partial f}{\partial \phi} \bm{e}_\phi + \frac{\partial f}{\partial z} \bm{e}_z \quad \text{（円柱座標）} \\
   \nabla f &= \frac{\partial f}{\partial r} \bm{e}_r + \frac{1}{r} \frac{\partial f}{\partial \theta} \bm{e}_\theta + \frac{1}{r \sin\theta} \frac{\partial f}{\partial \phi} \bm{e}_\phi \quad \text{（球座標）}

例として :math:`f = 1/r` の勾配を求める。:math:`f` は :math:`r` だけの関数なので、:math:`\nabla (1/r) = -\dfrac{1}{r^2} \bm{e}_r` となる。直交座標で 3 つの偏微分を計算するよりずっと簡単である。

直交曲線座標系での発散
----------------------

円柱座標での導出
~~~~~~~~~~~~~~~~

発散は、微小な領域から出ていく正味の流束を、領域の体積で割ったものであった（:ref:`第 6 章 <ch06>`）。円柱座標で、:math:`\rho` から :math:`\rho + \Delta\rho`、:math:`\phi` から :math:`\phi + \Delta\phi`、:math:`z` から :math:`z + \Delta z` までの微小な領域を考える。体積は :math:`\rho \, \Delta\rho \, \Delta\phi \, \Delta z` である。ベクトル場を :math:`\bm{F} = F_\rho \bm{e}_\rho + F_\phi \bm{e}_\phi + F_z \bm{e}_z` とする。

* :math:`\rho` が一定の 2 つの面：面積は :math:`\rho \, \Delta\phi \, \Delta z` で、:math:`\rho` によって変わる。外側の面から出る量と内側の面から入る量の差は、:math:`F_\rho \rho` の変化として

  .. math::

     \left[ F_\rho \rho \right]_{\rho + \Delta\rho} \Delta\phi \, \Delta z - \left[ F_\rho \rho \right]_{\rho} \Delta\phi \, \Delta z
     \approx \frac{\partial (\rho F_\rho)}{\partial \rho} \Delta\rho \, \Delta\phi \, \Delta z

* :math:`\phi` が一定の 2 つの面：面積はどちらも :math:`\Delta\rho \, \Delta z` なので、差は :math:`\dfrac{\partial F_\phi}{\partial \phi} \Delta\phi \, \Delta\rho \, \Delta z` である。
* :math:`z` が一定の 2 つの面：面積はどちらも :math:`\rho \, \Delta\rho \, \Delta\phi` なので、差は :math:`\dfrac{\partial F_z}{\partial z} \Delta z \, \rho \, \Delta\rho \, \Delta\phi` である。

3 つを足して体積 :math:`\rho \, \Delta\rho \, \Delta\phi \, \Delta z` で割ると、円柱座標での発散を得る。

.. math::

   \nabla \cdot \bm{F} = \frac{1}{\rho} \frac{\partial (\rho F_\rho)}{\partial \rho} + \frac{1}{\rho} \frac{\partial F_\phi}{\partial \phi} + \frac{\partial F_z}{\partial z}

第 1 項に :math:`\rho` が入るのは、外側の面ほど面積が大きいからである。:math:`\nabla \cdot \bm{F}` を :math:`\partial F_\rho / \partial \rho + \partial F_\phi / \partial \phi + \partial F_z / \partial z` としてはいけない。

一般の公式
~~~~~~~~~~

同じ考え方を一般の直交曲線座標系に当てはめると、:math:`u_1` が一定の面の面積は :math:`h_2 h_3 \, du_2 \, du_3`、体積は :math:`h_1 h_2 h_3 \, du_1 \, du_2 \, du_3` なので、次の公式を得る。

.. math::

   \nabla \cdot \bm{F} = \frac{1}{h_1 h_2 h_3} \left[
      \frac{\partial (h_2 h_3 F_1)}{\partial u_1}
    + \frac{\partial (h_3 h_1 F_2)}{\partial u_2}
    + \frac{\partial (h_1 h_2 F_3)}{\partial u_3} \right]

球座標では次のようになる。

.. math::

   \nabla \cdot \bm{F} = \frac{1}{r^2} \frac{\partial (r^2 F_r)}{\partial r}
   + \frac{1}{r \sin\theta} \frac{\partial (\sin\theta \, F_\theta)}{\partial \theta}
   + \frac{1}{r \sin\theta} \frac{\partial F_\phi}{\partial \phi}

例として、点電荷の電場 :math:`\bm{E} = \dfrac{q}{4 \pi \varepsilon_0 r^2} \bm{e}_r` の発散を求める。:math:`r^2 E_r = q / (4 \pi \varepsilon_0)` は定数なので、:math:`r > 0` では

.. math::

   \nabla \cdot \bm{E} = \frac{1}{r^2} \frac{\partial}{\partial r} \left( \frac{q}{4 \pi \varepsilon_0} \right) = 0

となる。電荷のない場所では電場の湧き出しがないことが、1 行の計算で確かめられる。原点（電荷のある点）での扱いは\ :ref:`第 14 章 <ch14>`\ で説明する。

直交曲線座標系での回転
----------------------

円柱座標での導出
~~~~~~~~~~~~~~~~

回転の成分は、その成分の向きを法線とする微小な面を一周したときの循環を、面積で割ったものであった（:ref:`第 7 章 <ch07>`）。円柱座標の :math:`z` 成分を求めるため、:math:`z` が一定の平面上で、:math:`\rho` から :math:`\rho + \Delta\rho`、:math:`\phi` から :math:`\phi + \Delta\phi` で囲まれた扇形の一部を反時計回りに一周する。

* 外側の円弧（長さ :math:`(\rho + \Delta\rho) \Delta\phi`、:math:`\bm{e}_\phi` の向きに進む）と内側の円弧（長さ :math:`\rho \, \Delta\phi`、逆向きに進む）の寄与の和は

  .. math::

     \left[ \rho F_\phi \right]_{\rho + \Delta\rho} \Delta\phi - \left[ \rho F_\phi \right]_{\rho} \Delta\phi
     \approx \frac{\partial (\rho F_\phi)}{\partial \rho} \Delta\rho \, \Delta\phi

* 2 本の半径方向の辺（長さ :math:`\Delta\rho`）の寄与の和は :math:`-\dfrac{\partial F_\rho}{\partial \phi} \Delta\phi \, \Delta\rho` である。

面積 :math:`\rho \, \Delta\rho \, \Delta\phi` で割ると、:math:`z` 成分は次のようになる。

.. math::

   (\nabla \times \bm{F})_z = \frac{1}{\rho} \left[ \frac{\partial (\rho F_\phi)}{\partial \rho} - \frac{\partial F_\rho}{\partial \phi} \right]

他の成分も同様に求められ、円柱座標での回転は次のようになる。

.. math::

   \nabla \times \bm{F} =
     \left( \frac{1}{\rho} \frac{\partial F_z}{\partial \phi} - \frac{\partial F_\phi}{\partial z} \right) \bm{e}_\rho
   + \left( \frac{\partial F_\rho}{\partial z} - \frac{\partial F_z}{\partial \rho} \right) \bm{e}_\phi
   + \frac{1}{\rho} \left( \frac{\partial (\rho F_\phi)}{\partial \rho} - \frac{\partial F_\rho}{\partial \phi} \right) \bm{e}_z

一般の公式
~~~~~~~~~~

一般の直交曲線座標系では、行列式の形で次のように書ける。:math:`\bm{e}_1, \bm{e}_2, \bm{e}_3` はこの順に右手系をなすものとする。

.. math::

   \nabla \times \bm{F} = \frac{1}{h_1 h_2 h_3}
   \begin{vmatrix}
   h_1 \bm{e}_1 & h_2 \bm{e}_2 & h_3 \bm{e}_3 \\
   \dfrac{\partial}{\partial u_1} & \dfrac{\partial}{\partial u_2} & \dfrac{\partial}{\partial u_3} \\
   h_1 F_1 & h_2 F_2 & h_3 F_3
   \end{vmatrix}

球座標では次のようになる。

.. math::

   \nabla \times \bm{F} =
     \frac{1}{r \sin\theta} \left( \frac{\partial (\sin\theta \, F_\phi)}{\partial \theta} - \frac{\partial F_\theta}{\partial \phi} \right) \bm{e}_r
   + \frac{1}{r} \left( \frac{1}{\sin\theta} \frac{\partial F_r}{\partial \phi} - \frac{\partial (r F_\phi)}{\partial r} \right) \bm{e}_\theta
   + \frac{1}{r} \left( \frac{\partial (r F_\theta)}{\partial r} - \frac{\partial F_r}{\partial \theta} \right) \bm{e}_\phi

例として、:ref:`第 7 章 <ch07>`\ の 2 つの流れを円柱座標で調べる。

* 角速度 :math:`\omega` の剛体回転 :math:`\bm{v} = \omega \rho \, \bm{e}_\phi`：:math:`(\nabla \times \bm{v})_z = \dfrac{1}{\rho} \dfrac{\partial (\omega \rho^2)}{\partial \rho} = 2\omega` となり、回転は角速度の 2 倍である。
* 自由渦 :math:`\bm{v} = \dfrac{\Gamma}{2 \pi \rho} \bm{e}_\phi`：:math:`\rho v_\phi = \Gamma / (2\pi)` は定数なので、:math:`\rho > 0` では回転は 0 である。

直交座標で計算すると分数の偏微分が必要になるが、円柱座標では 1 行で済む。

直交曲線座標系でのラプラシアン
------------------------------

ラプラシアンは勾配の発散 :math:`\nabla^2 f = \nabla \cdot (\nabla f)` なので、勾配の公式を発散の公式に代入すれば求まる。

.. math::

   \nabla^2 f = \frac{1}{h_1 h_2 h_3} \left[
      \frac{\partial}{\partial u_1} \left( \frac{h_2 h_3}{h_1} \frac{\partial f}{\partial u_1} \right)
    + \frac{\partial}{\partial u_2} \left( \frac{h_3 h_1}{h_2} \frac{\partial f}{\partial u_2} \right)
    + \frac{\partial}{\partial u_3} \left( \frac{h_1 h_2}{h_3} \frac{\partial f}{\partial u_3} \right) \right]

円柱座標と球座標では次のようになる。

.. math::

   \nabla^2 f &= \frac{1}{\rho} \frac{\partial}{\partial \rho} \left( \rho \frac{\partial f}{\partial \rho} \right)
   + \frac{1}{\rho^2} \frac{\partial^2 f}{\partial \phi^2} + \frac{\partial^2 f}{\partial z^2} \quad \text{（円柱座標）} \\
   \nabla^2 f &= \frac{1}{r^2} \frac{\partial}{\partial r} \left( r^2 \frac{\partial f}{\partial r} \right)
   + \frac{1}{r^2 \sin\theta} \frac{\partial}{\partial \theta} \left( \sin\theta \frac{\partial f}{\partial \theta} \right)
   + \frac{1}{r^2 \sin^2\theta} \frac{\partial^2 f}{\partial \phi^2} \quad \text{（球座標）}

たとえば :math:`f = 1/r` は、:math:`r^2 \, \partial f / \partial r = -1` が定数なので、:math:`r > 0` で :math:`\nabla^2 (1/r) = 0` を満たす。この関数は\ :ref:`第 16 章 <ch16>`\ でポアソン方程式の解として再び現れる。

ベクトル場のラプラシアン :math:`\nabla^2 \bm{F}` は、:ref:`第 8 章 <ch08>`\ で述べたように、曲線座標では成分ごとのラプラシアンにならないので、:math:`\nabla^2 \bm{F} = \nabla (\nabla \cdot \bm{F}) - \nabla \times (\nabla \times \bm{F})` で計算する。

例：円管の中の流れ
------------------

半径 :math:`R` の円管の中を流れる粘性流体の、ゆっくりとした定常な流れ（ハーゲン・ポアズイユ流れ）の速度は

.. math::

   \bm{v} = v_{\max} \left( 1 - \frac{\rho^2}{R^2} \right) \bm{e}_z

で与えられる。中心で最も速く、管の壁（:math:`\rho = R`）で 0 になる。円柱座標の公式を使うと、次のことが分かる。

* 発散：:math:`v_z` は :math:`z` によらないので :math:`\nabla \cdot \bm{v} = 0` である。流体が途中で増えたり減ったりしない。
* 回転：:math:`\nabla \times \bm{v} = -\dfrac{\partial v_z}{\partial \rho} \bm{e}_\phi = \dfrac{2 v_{\max} \rho}{R^2} \bm{e}_\phi` である。流れはまっすぐだが、速さが場所によって違うため、流れの中に置いた小さな羽根車は回る。回転は壁の近くほど大きい。
* ラプラシアン：:math:`\nabla^2 v_z = \dfrac{1}{\rho} \dfrac{d}{d\rho} \left( \rho \dfrac{d v_z}{d \rho} \right) = -\dfrac{4 v_{\max}}{R^2}` は一定である。粘性流体の運動方程式では、この値に粘性係数を掛けたものが、管の長さ方向の圧力の勾配とつり合う。

SymPy で確かめる
----------------

スケール因子さえ分かれば、勾配・発散・回転・ラプラシアンは機械的に計算できる。次のサンプルは、位置ベクトルからスケール因子を求め、一般の公式で各演算を計算する。最後に、球座標の公式で求めた :math:`f = x^2 y + z^2` のラプラシアンが、直交座標で求めた :math:`2y + 2` と一致することを確かめている。

.. literalinclude:: ../examples/ch09_orthogonal_ops.py
   :pyobject: divergence
   :lineno-match:
   :caption: ch09_orthogonal_ops.py の divergence()

.. literalinclude:: ../examples/ch09_orthogonal_ops.py
   :pyobject: rotation
   :lineno-match:
   :caption: ch09_orthogonal_ops.py の rotation()

.. literalinclude:: ../build/outputs/ch09_orthogonal_ops.txt
   :language: text
   :caption: ch09_orthogonal_ops.py の実行結果

剛体回転の回転が :math:`2\omega`、自由渦の回転が 0、点電荷の電場の発散が 0 になり、本文の計算と一致している。円管の流れの回転は :math:`(0, 2 \rho v_{\max} / R^2, 0)` と表示されているが、これは :math:`(\bm{e}_\rho, \bm{e}_\phi, \bm{e}_z)` 成分の順である。

サンプルの全体：:download:`ch09_orthogonal_ops.py <../examples/ch09_orthogonal_ops.py>`

この章のまとめ
--------------

* 円柱座標 :math:`(\rho, \phi, z)` は軸対称な問題に、球座標 :math:`(r, \theta, \phi)` は球対称な問題に向いている。
* 曲線座標系の基底ベクトルは場所によって向きが変わる。そのため、微分演算の式は直交座標の式の置き換えでは得られない。
* スケール因子 :math:`h_i = |\partial \bm{r} / \partial u_i|` は、座標の変化を実際の距離に直す係数である。体積素は :math:`h_1 h_2 h_3 \, du_1 \, du_2 \, du_3` になる。
* 勾配・発散・回転・ラプラシアンは、スケール因子を使った一般の公式で表せる。発散と回転の公式は、微小な領域の流束と循環から導ける。
* 対称性に合った座標系を使うと、点電荷の電場や渦の計算が 1 行で済む。
