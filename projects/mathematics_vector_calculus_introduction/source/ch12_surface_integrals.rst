.. _ch12:

第 12 章 面積分と流束
======================

曲面の上で場を積分するのが面積分である。この章では、曲面をパラメーター表示し、法線ベクトルと面素を求める方法を説明する。それを使って、曲面の面積、スカラー場の面積分、そしてベクトル場が曲面を通り抜ける量である流束を計算する。流束は、:ref:`第 14 章 <ch14>`\ のガウスの発散定理と\ :ref:`第 15 章 <ch15>`\ のストークスの定理の主役になる。

曲面のパラメーター表示
----------------------

曲線を 1 つのパラメーター :math:`t` で表したように、曲面は 2 つのパラメーター :math:`(u, v)` で表せる。

.. math::

   \bm{r}(u, v) = (x(u, v), \ y(u, v), \ z(u, v))

:math:`(u, v)` が平面の領域 :math:`D` を動くと、点 :math:`\bm{r}(u, v)` は空間の曲面 :math:`S` を描く。代表的な曲面のパラメーター表示を示す。

.. list-table:: 曲面のパラメーター表示の例
   :name: table-ch12-surfaces
   :header-rows: 1
   :widths: 25 45 30

   * - 曲面
     - パラメーター表示
     - パラメーターの範囲
   * - 平面
     - :math:`\bm{r}(u, v) = \bm{r}_0 + u \bm{a} + v \bm{b}`
     - :math:`D` は平面の領域
   * - 円柱面（半径 :math:`R`）
     - :math:`\bm{r}(\phi, z) = (R\cos\phi, \ R\sin\phi, \ z)`
     - :math:`0 \le \phi < 2\pi`
   * - 球面（半径 :math:`R`）
     - :math:`\bm{r}(\theta, \phi) = (R\sin\theta\cos\phi, \ R\sin\theta\sin\phi, \ R\cos\theta)`
     - :math:`0 \le \theta \le \pi, \ 0 \le \phi < 2\pi`
   * - グラフ :math:`z = g(x, y)`
     - :math:`\bm{r}(x, y) = (x, \ y, \ g(x, y))`
     - :math:`(x, y) \in D`

平面のパラメーター表示の :math:`\bm{a}`, :math:`\bm{b}` は、平面に平行で互いに平行でない 2 つのベクトルである。円柱面と球面は、:ref:`第 9 章 <ch09>`\ の円柱座標と球座標で :math:`\rho = R`、:math:`r = R` と固定したものである。

:math:`v` を固定して :math:`u` だけを動かすと、曲面上に 1 本の曲線ができる。:math:`u` を固定した場合も同様である。これらの曲線を座標曲線という。球面では、:math:`\theta` が一定の曲線が緯線、:math:`\phi` が一定の曲線が経線である。

法線ベクトルと面素
------------------

接ベクトルと法線ベクトル
~~~~~~~~~~~~~~~~~~~~~~~~

座標曲線の接ベクトルは、偏微分

.. math::

   \bm{r}_u = \frac{\partial \bm{r}}{\partial u}, \qquad \bm{r}_v = \frac{\partial \bm{r}}{\partial v}

で与えられる。2 つの接ベクトルはどちらも曲面に接しているので、その外積 :math:`\bm{r}_u \times \bm{r}_v` は曲面に垂直な法線ベクトルになる（:ref:`第 2 章 <ch02>`）。大きさで割ったものが単位法線ベクトルである。

.. math::

   \bm{n} = \frac{\bm{r}_u \times \bm{r}_v}{|\bm{r}_u \times \bm{r}_v|}

ここでは、:math:`\bm{r}_u \times \bm{r}_v \ne \bm{0}`\ （2 つの接ベクトルが平行にならない）と仮定する。このような点では、曲面に滑らかな接平面がある。

面素
~~~~

パラメーターの小さな長方形（辺 :math:`du`, :math:`dv`）は、曲面上では 2 つのベクトル :math:`\bm{r}_u \, du` と :math:`\bm{r}_v \, dv` が張る小さな平行四辺形になる。平行四辺形の面積は外積の大きさなので、曲面の面素は

.. math::

   dS = |\bm{r}_u \times \bm{r}_v| \, du \, dv

である。:ref:`第 10 章 <ch10>`\ の変数変換で現れたヤコビアンの絶対値は、平面から平面への変換での同じ量であった。面素に単位法線ベクトルを掛けた

.. math::

   d\bm{S} = \bm{n} \, dS = (\bm{r}_u \times \bm{r}_v) \, du \, dv

をベクトル面素という。大きさが面積、向きが曲面に垂直なベクトルである。

代表的な曲面の面素
~~~~~~~~~~~~~~~~~~

* 球面：:math:`\bm{r}_\theta = R(\cos\theta\cos\phi, \cos\theta\sin\phi, -\sin\theta)`、:math:`\bm{r}_\phi = R(-\sin\theta\sin\phi, \sin\theta\cos\phi, 0)` から

  .. math::

     \bm{r}_\theta \times \bm{r}_\phi = R^2 \sin\theta \, \bm{e}_r, \qquad dS = R^2 \sin\theta \, d\theta \, d\phi

  となる。法線ベクトルは外向き（:math:`\bm{e}_r` の向き）である（:numref:`fig-ch12-sphere-normals`）。面素は\ :ref:`第 9 章 <ch09>`\ で求めたものと一致する。

* 円柱面：:math:`\bm{r}_\phi = (-R\sin\phi, R\cos\phi, 0)`、:math:`\bm{r}_z = (0, 0, 1)` から :math:`\bm{r}_\phi \times \bm{r}_z = R \, \bm{e}_\rho`、:math:`dS = R \, d\phi \, dz` となる。法線ベクトルは外向きである。

* グラフ :math:`z = g(x, y)`：:math:`\bm{r}_x = (1, 0, g_x)`、:math:`\bm{r}_y = (0, 1, g_y)` から

  .. math::

     \bm{r}_x \times \bm{r}_y = (-g_x, \ -g_y, \ 1), \qquad dS = \sqrt{1 + g_x^2 + g_y^2} \, dx \, dy

  となる。:math:`g_x = \partial g / \partial x` などである。法線ベクトルは上向き（:math:`z` 成分が正）である。:math:`\sqrt{1 + g_x^2 + g_y^2}` は、傾いた曲面の面積が、:math:`xy` 平面に射影した面積の何倍かを表している。

.. figure:: ../build/figures/ch12_sphere_normals.svg
   :name: fig-ch12-sphere-normals
   :width: 65%
   :align: center

   球面の接ベクトル :math:`\bm{r}_\theta`, :math:`\bm{r}_\phi` と外向きの法線ベクトル

.. literalinclude:: ../examples/ch12_sphere_normals.py
   :pyobject: tangents
   :lineno-match:
   :caption: ch12_sphere_normals.py の tangents()

サンプルの全体：:download:`ch12_sphere_normals.py <../examples/ch12_sphere_normals.py>`

曲面の向き
----------

1 つの曲面には、法線ベクトルの向きが 2 通りある。たとえば球面には外向きと内向きがある。曲面の各点で、連続的に変わるように法線ベクトルの向きを 1 つ選ぶことを、曲面の向きを決めるという。向きを決めた曲面を、向きの付いた曲面という。

* パラメーター表示した曲面では、:math:`\bm{r}_u \times \bm{r}_v` の向きが 1 つの向きを与える。:math:`u` と :math:`v` を入れ替えると、向きは逆になる。
* 球面や立方体の表面のように、空間のある領域を囲む曲面を\ :term:`閉曲面`\ という。閉曲面では、特に断らない限り、外向きの法線ベクトルを正の向きとする。

ほとんどの曲面は向きを決められるが、例外もある。細長い帯を 1 回ひねって両端を貼り合わせたメビウスの帯は、法線ベクトルを連続的に動かして 1 周すると、元と逆の向きに戻ってしまう。このような曲面では向きを決められず、流束を定義できない。本書では向きを決められる曲面だけを扱う。

曲面積とスカラー場の面積分
--------------------------

定義
~~~~

スカラー場 :math:`f` の曲面 :math:`S` 上の\ :term:`面積分`\ は、曲面を小さく分けて「:math:`f` の値 × 面積」を足し合わせた和の極限であり、パラメーター表示を使って次のように計算できる。

.. math::

   \iint_S f \, dS = \iint_D f(\bm{r}(u, v)) \, |\bm{r}_u \times \bm{r}_v| \, du \, dv

:math:`f = 1` なら曲面の面積になる。:math:`f` が曲面の面密度なら、曲面の形をした薄い殻の質量になる。スカラー場の面積分は、曲面の向きにもパラメーター表示の選び方にもよらない。

例：球面と放物面の面積
~~~~~~~~~~~~~~~~~~~~~~

半径 :math:`R` の球面の面積は

.. math::

   \int_0^{2\pi} \int_0^{\pi} R^2 \sin\theta \, d\theta \, d\phi = 2\pi R^2 \left[ -\cos\theta \right]_0^{\pi} = 4\pi R^2

である。

放物面 :math:`z = x^2 + y^2` の :math:`z \le 1` の部分の面積を求める。グラフの公式から :math:`dS = \sqrt{1 + 4x^2 + 4y^2} \, dx \, dy` で、:math:`xy` 平面上の領域は単位円板である。極座標に変換すると

.. math::

   \int_0^{2\pi} \int_0^{1} \sqrt{1 + 4r^2} \, r \, dr \, d\theta
   = 2\pi \left[ \frac{(1 + 4r^2)^{3/2}}{12} \right]_0^1
   = \frac{\pi (5\sqrt{5} - 1)}{6} \approx 5.330

となる。底面の円板の面積 :math:`\pi \approx 3.14` より大きいのは、曲面が傾いているからである。

例：半球面の殻の質量
~~~~~~~~~~~~~~~~~~~~

半径 :math:`R` の半球面 :math:`z \ge 0` の面密度が高さに比例して :math:`z` であるとき、質量は

.. math::

   \iint_S z \, dS = \int_0^{2\pi} \int_0^{\pi/2} R\cos\theta \cdot R^2 \sin\theta \, d\theta \, d\phi = 2\pi R^3 \cdot \frac{1}{2} = \pi R^3

となる。

流束
----

流れが曲面を通り抜ける量
~~~~~~~~~~~~~~~~~~~~~~~~

速度 :math:`\bm{v}` の流れの中に、面積 :math:`\Delta S`、単位法線ベクトル :math:`\bm{n}` の小さな面を置く。:ref:`第 6 章 <ch06>`\ で見たように、時間 :math:`\Delta t` の間にこの面を通り抜ける流体は、底面が :math:`\Delta S`、側面が :math:`\bm{v} \Delta t` に平行な斜めの柱をなす。柱の高さは :math:`\bm{v} \Delta t` の :math:`\bm{n}` 方向の成分 :math:`(\bm{v} \cdot \bm{n}) \Delta t` なので、通り抜ける体積は :math:`(\bm{v} \cdot \bm{n}) \Delta S \, \Delta t` である。単位時間あたりでは :math:`(\bm{v} \cdot \bm{n}) \Delta S` となる。

* 流れが面に垂直なら :math:`\bm{v} \cdot \bm{n} = |\bm{v}|` で、通り抜ける量は最大である。
* 流れが面に平行なら :math:`\bm{v} \cdot \bm{n} = 0` で、何も通り抜けない。
* 流れが :math:`\bm{n}` と逆向きなら負になり、逆向きに通り抜けることを表す。

曲面全体で足し合わせたものを、ベクトル場 :math:`\bm{F}` の曲面 :math:`S` を通る流束という。

.. math::

   \Phi = \iint_S \bm{F} \cdot d\bm{S} = \iint_S \bm{F} \cdot \bm{n} \, dS
   = \iint_D \bm{F}(\bm{r}(u, v)) \cdot (\bm{r}_u \times \bm{r}_v) \, du \, dv

流束は、法線方向の成分 :math:`\bm{F} \cdot \bm{n}` をスカラー場として面積分したものである。曲面の向きを逆にすると符号が変わる。この点は、ベクトル場の線積分が曲線の向きで符号を変えたこと（:ref:`第 11 章 <ch11>`）と同じである。

流束という言葉は、流れ以外のベクトル場にも使う。電場 :math:`\bm{E}` の流束は電束、磁束密度 :math:`\bm{B}` の流束は磁束、熱流束ベクトルの流束は単位時間に曲面を通る熱量である。

例：位置ベクトル場の流束
~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\bm{F} = \bm{r} = (x, y, z)` の、半径 :math:`R` の球面を外向きに通る流束を求める。球面上では :math:`\bm{n} = \bm{e}_r`、:math:`\bm{r} = R \bm{e}_r` なので :math:`\bm{F} \cdot \bm{n} = R` は一定であり、

.. math::

   \iint_S \bm{F} \cdot \bm{n} \, dS = R \times 4\pi R^2 = 4\pi R^3

となる。同じ場の、半径 :math:`R`、高さ :math:`h` の円柱の側面を外向きに通る流束は、側面で :math:`\bm{F} \cdot \bm{n} = R` なので :math:`R \times 2\pi R h = 2\pi R^2 h` である。このように、:math:`\bm{F} \cdot \bm{n}` が曲面上で一定になる場合は、積分せずに面積を掛けるだけで流束が求まる。

例：逆 2 乗の場の流束
~~~~~~~~~~~~~~~~~~~~~

点電荷の電場や万有引力と同じ形の場 :math:`\bm{F} = \bm{e}_r / r^2` の、半径 :math:`R` の球面を通る流束は

.. math::

   \iint_S \bm{F} \cdot \bm{n} \, dS = \frac{1}{R^2} \times 4\pi R^2 = 4\pi

であり、球面の半径によらない。場の強さが :math:`1/R^2` で弱くなる効果と、球面の面積が :math:`R^2` に比例して増える効果が打ち消し合うからである。この性質は、:ref:`第 14 章 <ch14>`\ で電場のガウスの法則として再び現れる。

数値計算
--------

曲面のパラメーター表示 :math:`\bm{r}(u, v)` を関数として与えれば、面積分と流束は機械的に計算できる。次のサンプルでは、接ベクトル :math:`\bm{r}_u`, :math:`\bm{r}_v` を中心差分で近似し、その外積で法線ベクトルを求めている。

.. literalinclude:: ../examples/ch12_surface_integrals.py
   :pyobject: normal
   :lineno-match:
   :caption: ch12_surface_integrals.py の normal()

.. literalinclude:: ../examples/ch12_surface_integrals.py
   :pyobject: flux
   :lineno-match:
   :caption: ch12_surface_integrals.py の flux()

この章の例を数値計算した結果を示す。

.. literalinclude:: ../build/outputs/ch12_surface_integrals.txt
   :language: text
   :caption: ch12_surface_integrals.py の実行結果

すべての例で、手計算の値と一致している。曲面の向きは、パラメーター :math:`(u, v)` の順序で決まる。球面を :math:`(\phi, \theta)` の順にパラメーター表示すると、法線ベクトルが内向きになり、流束の符号が逆になるので注意する。

サンプルの全体：:download:`ch12_surface_integrals.py <../examples/ch12_surface_integrals.py>`

この章のまとめ
--------------

* 曲面は 2 つのパラメーターで :math:`\bm{r}(u, v)` と表せる。接ベクトル :math:`\bm{r}_u`, :math:`\bm{r}_v` の外積が法線ベクトルになる。
* 面素は :math:`dS = |\bm{r}_u \times \bm{r}_v| \, du \, dv`、ベクトル面素は :math:`d\bm{S} = (\bm{r}_u \times \bm{r}_v) \, du \, dv` である。
* 曲面の向きは法線ベクトルの向きで決める。閉曲面では外向きを正とする。
* スカラー場の面積分 :math:`\iint_S f \, dS` は、曲面積や殻の質量を表し、向きによらない。
* 流束 :math:`\iint_S \bm{F} \cdot \bm{n} \, dS` は、ベクトル場が曲面を通り抜ける量を表し、向きを逆にすると符号が変わる。
