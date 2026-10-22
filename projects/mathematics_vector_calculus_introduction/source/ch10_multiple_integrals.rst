.. _ch10:

第 10 章 重積分と変数変換
==========================

この章から、場を積分する方法を扱う。最初に、平面の領域や立体の上で関数を積分する重積分を説明する。重積分は、1 変数の積分を繰り返す累次積分で計算できる。また、極座標や球座標に変数を変換すると、円や球の上の積分が簡単になる。最後に、質量・重心・慣性モーメントへの応用と、SciPy による数値計算を示す。

2 重積分の定義
--------------

1 変数の定積分 :math:`\int_a^b f(x) \, dx` は、区間を細かく分け、各区間の幅と関数の値の積を足し合わせた和の極限であった。2 重積分は、これを平面の領域に広げたものである。

平面の領域 :math:`D` を、小さな長方形 :math:`\Delta D_1, \Delta D_2, \ldots, \Delta D_n` に分ける。各長方形の面積を :math:`\Delta A_k`、その中の 1 点を :math:`(x_k, y_k)` として、和

.. math::

   \sum_{k=1}^{n} f(x_k, y_k) \, \Delta A_k

をつくる。分割を細かくしていったときにこの和が一定の値に近づくなら、その値を :math:`f` の :math:`D` 上の\ :term:`重積分`\ （2 重積分）といい、次のように書く。

.. math::

   \iint_D f(x, y) \, dA = \iint_D f(x, y) \, dx \, dy

:math:`dA` は面積の微小な要素（面積要素）である。:math:`f \ge 0` なら、重積分は曲面 :math:`z = f(x, y)` と領域 :math:`D` の間にある立体の体積を表す。:math:`f = 1` なら、重積分は :math:`D` の面積そのものである。:math:`f` が板の面密度なら板の質量、熱の発生量の分布なら総発熱量になる。工学では「分布している量の合計」を求めるときに重積分を使う。

累次積分
--------

長方形の領域
~~~~~~~~~~~~

重積分を定義どおりに和の極限として計算するのは大変である。実際には、1 変数の積分を 2 回繰り返す\ :term:`累次積分`\ で計算する。

長方形の領域 :math:`D = \{(x, y) \mid a \le x \le b, \ c \le y \le d\}` で :math:`f` が連続なら、次の式が成り立つ（フビニの定理）。

.. math::

   \iint_D f(x, y) \, dx \, dy
   = \int_a^b \left( \int_c^d f(x, y) \, dy \right) dx
   = \int_c^d \left( \int_a^b f(x, y) \, dx \right) dy

内側の積分では、もう一方の変数を定数とみなす。たとえば、:math:`D = [0, 1] \times [0, 2]` での :math:`f = x y^2` の積分は次のようになる。

.. math::

   \int_0^1 \left( \int_0^2 x y^2 \, dy \right) dx = \int_0^1 \frac{8}{3} x \, dx = \frac{4}{3}

一般の領域
~~~~~~~~~~

長方形でない領域では、内側の積分の範囲が外側の変数に依存する。例として、曲線 :math:`y = x^2` と直線 :math:`y = x` で囲まれた領域

.. math::

   D = \{(x, y) \mid 0 \le x \le 1, \ x^2 \le y \le x\}

で :math:`f = xy` を積分する。:numref:`fig-ch10-region-order` の左のように、:math:`x` を固定すると :math:`y` は :math:`x^2` から :math:`x` まで動く。そこで、先に :math:`y` で積分する。

.. math::

   \iint_D xy \, dx \, dy
   = \int_0^1 \left( \int_{x^2}^{x} xy \, dy \right) dx
   = \int_0^1 \frac{x (x^2 - x^4)}{2} \, dx
   = \frac{1}{2} \left( \frac{1}{4} - \frac{1}{6} \right) = \frac{1}{24}

.. figure:: ../build/figures/ch10_region_order.svg
   :name: fig-ch10-region-order
   :width: 95%
   :align: center

   同じ領域を縦の帯と横の帯に分ける

積分の順序の交換
~~~~~~~~~~~~~~~~

同じ領域を、:numref:`fig-ch10-region-order` の右のように横の帯に分けることもできる。:math:`y` を固定すると、:math:`x` は直線 :math:`x = y` から曲線 :math:`x = \sqrt{y}` まで動く。

.. math::

   \iint_D xy \, dx \, dy
   = \int_0^1 \left( \int_{y}^{\sqrt{y}} xy \, dx \right) dy
   = \int_0^1 \frac{y (y - y^2)}{2} \, dy
   = \frac{1}{2} \left( \frac{1}{3} - \frac{1}{4} \right) = \frac{1}{24}

どちらの順序でも同じ値になる。順序を交換するときは、領域の図を描いて、積分の範囲を正しく書き直すことが大切である。

順序の交換は、計算できない積分を計算できる形に変えるのに役立つ。たとえば

.. math::

   \int_0^1 \left( \int_x^1 e^{y^2} \, dy \right) dx

は、:math:`e^{y^2}` の原始関数が初等関数で表せないため、このままでは内側の積分を計算できない。積分の領域は :math:`0 \le x \le y \le 1` という三角形なので、順序を交換すると

.. math::

   \int_0^1 \left( \int_0^y e^{y^2} \, dx \right) dy = \int_0^1 y \, e^{y^2} \, dy = \left[ \frac{e^{y^2}}{2} \right]_0^1 = \frac{e - 1}{2}

と計算できる。

3 重積分
--------

立体 :math:`V` の上の\ :term:`体積積分`\ （3 重積分）も、2 重積分と同じく小さな直方体に分けた和の極限として定義し、累次積分で計算する。

.. math::

   \iiint_V f(x, y, z) \, dV = \iiint_V f(x, y, z) \, dx \, dy \, dz

例として、:math:`x \ge 0`, :math:`y \ge 0`, :math:`z \ge 0`, :math:`x + y + z \le 1` で表される四面体の体積を求める。外側から順に :math:`x` は 0 から 1、:math:`y` は 0 から :math:`1 - x`、:math:`z` は 0 から :math:`1 - x - y` まで動く。

.. math::

   \int_0^1 \int_0^{1-x} \int_0^{1-x-y} dz \, dy \, dx
   = \int_0^1 \int_0^{1-x} (1 - x - y) \, dy \, dx
   = \int_0^1 \frac{(1 - x)^2}{2} \, dx = \frac{1}{6}

変数変換とヤコビアン
--------------------

1 変数の置換積分
~~~~~~~~~~~~~~~~

1 変数の積分で :math:`x = g(u)` と置き換えると、:math:`dx = g'(u) \, du` となる。:math:`g'(u)` は、:math:`u` の微小な区間の長さが :math:`x` に移ったときに何倍になるかを表す。多変数でも同じように、変数を変えたときに面積や体積が何倍になるかを考えればよい。

2 変数の変数変換
~~~~~~~~~~~~~~~~

:math:`x = x(u, v)`, :math:`y = y(u, v)` と変数を変換する。:math:`uv` 平面の小さな長方形（辺 :math:`du`, :math:`dv`）は、:math:`xy` 平面では、2 つのベクトル

.. math::

   \frac{\partial \bm{r}}{\partial u} du = \left( \frac{\partial x}{\partial u}, \frac{\partial y}{\partial u} \right) du, \qquad
   \frac{\partial \bm{r}}{\partial v} dv = \left( \frac{\partial x}{\partial v}, \frac{\partial y}{\partial v} \right) dv

で張られる小さな平行四辺形に移る。平行四辺形の面積は、2 つのベクトルを並べた行列式の絶対値に等しい。2 つのベクトルを :math:`z` 成分が 0 の 3 次元のベクトルとみなすと、この行列式は外積の :math:`z` 成分であり、その絶対値は外積の大きさ、つまり平行四辺形の面積である（:ref:`第 2 章 <ch02>`）。この行列式を\ :term:`ヤコビアン`\ （ヤコビ行列式）という。

.. math::

   \frac{\partial(x, y)}{\partial(u, v)} =
   \begin{vmatrix}
   \dfrac{\partial x}{\partial u} & \dfrac{\partial x}{\partial v} \\
   \dfrac{\partial y}{\partial u} & \dfrac{\partial y}{\partial v}
   \end{vmatrix}

したがって :math:`dx \, dy = \left| \dfrac{\partial(x, y)}{\partial(u, v)} \right| du \, dv` であり、次の変数変換の公式が成り立つ。

.. math::

   \iint_D f(x, y) \, dx \, dy = \iint_{D'} f(x(u, v), y(u, v)) \left| \frac{\partial(x, y)}{\partial(u, v)} \right| du \, dv

:math:`D'` は、:math:`D` に対応する :math:`uv` 平面の領域である。変換は、:math:`D'` と :math:`D` の点が 1 対 1 に対応するものとする（境界の点のように面積が 0 の部分では、1 対 1 でなくてもよい）。

極座標
~~~~~~

極座標 :math:`x = r\cos\theta`, :math:`y = r\sin\theta` のヤコビアンは

.. math::

   \frac{\partial(x, y)}{\partial(r, \theta)} =
   \begin{vmatrix}
   \cos\theta & -r\sin\theta \\
   \sin\theta & r\cos\theta
   \end{vmatrix} = r

なので、:math:`dx \, dy = r \, dr \, d\theta` である。:numref:`fig-ch10-polar-cell` のように、極座標の微小な領域は、半径方向の幅 :math:`\Delta r`、円周方向の幅 :math:`r \Delta\theta` のほぼ長方形とみなせる。原点から遠いほど同じ :math:`\Delta\theta` でも面積が大きくなることが、因子 :math:`r` に表れている。これは\ :ref:`第 9 章 <ch09>`\ のスケール因子の積 :math:`h_r h_\theta = r` と同じものである。

.. figure:: ../build/figures/ch10_polar_cell.svg
   :name: fig-ch10-polar-cell
   :width: 65%
   :align: center

   極座標の微小な領域の面積

例として、平面全体で :math:`e^{-(x^2 + y^2)}` を積分する。直交座標のままでは計算できないが、極座標に変換すると

.. math::

   \iint_{\mathbb{R}^2} e^{-(x^2 + y^2)} \, dx \, dy
   = \int_0^{2\pi} \int_0^\infty e^{-r^2} \, r \, dr \, d\theta
   = 2\pi \left[ -\frac{e^{-r^2}}{2} \right]_0^\infty = \pi

となる。左辺は :math:`\left( \int_{-\infty}^\infty e^{-x^2} dx \right)^2` に等しいので、ガウス積分 :math:`\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}` が得られる。この値は、正規分布や熱伝導の解など、工学のさまざまな場面で現れる。

線形な変換
~~~~~~~~~~

:math:`x = au`, :math:`y = bv`\ （:math:`a, b > 0`）と変換すると、ヤコビアンは :math:`ab` である。楕円 :math:`x^2/a^2 + y^2/b^2 \le 1` は単位円板 :math:`u^2 + v^2 \le 1` に対応するので、楕円の面積は

.. math::

   \iint_{\text{楕円}} dx \, dy = \iint_{u^2 + v^2 \le 1} ab \, du \, dv = \pi ab

となる。一般に、行列 :math:`M` による線形な変換では、面積は :math:`|\det M|` 倍になる。

3 変数の変数変換
~~~~~~~~~~~~~~~~

3 変数でも同じく、:math:`dx \, dy \, dz = \left| \dfrac{\partial(x, y, z)}{\partial(u, v, w)} \right| du \, dv \, dw` である。ヤコビアンは 3 行 3 列の行列式で、微小な平行六面体の体積の倍率を表す。円柱座標と球座標のヤコビアンは、:ref:`第 9 章 <ch09>`\ の体積素と一致する。

.. list-table:: 主な座標変換のヤコビアン
   :name: table-ch10-jacobian
   :header-rows: 1
   :widths: 25 45 30

   * - 座標
     - 変換
     - 面積素・体積素
   * - 極座標
     - :math:`x = r\cos\theta, \ y = r\sin\theta`
     - :math:`dx \, dy = r \, dr \, d\theta`
   * - 円柱座標
     - :math:`x = \rho\cos\phi, \ y = \rho\sin\phi, \ z = z`
     - :math:`dV = \rho \, d\rho \, d\phi \, dz`
   * - 球座標
     - :math:`x = r\sin\theta\cos\phi, \ y = r\sin\theta\sin\phi, \ z = r\cos\theta`
     - :math:`dV = r^2 \sin\theta \, dr \, d\theta \, d\phi`

球座標を使うと、半径 :math:`R` の球の体積は

.. math::

   \int_0^{2\pi} \int_0^{\pi} \int_0^{R} r^2 \sin\theta \, dr \, d\theta \, d\phi
   = 2\pi \cdot 2 \cdot \frac{R^3}{3} = \frac{4}{3} \pi R^3

と簡単に求まる。

応用：質量・重心・慣性モーメント
--------------------------------

物体の密度を :math:`\mu(x, y, z)` とする。この章では、円柱座標の :math:`\rho` と区別するため、密度を :math:`\mu` で表す。物体の質量 :math:`M`、重心 :math:`(\bar{x}, \bar{y}, \bar{z})`、:math:`z` 軸まわりの慣性モーメント :math:`I_z` は、次の体積積分で求まる。

.. math::

   M = \iiint_V \mu \, dV, \qquad
   \bar{x} = \frac{1}{M} \iiint_V x \, \mu \, dV, \qquad
   I_z = \iiint_V (x^2 + y^2) \, \mu \, dV

:math:`\bar{y}`, :math:`\bar{z}` も同様である。慣性モーメントの :math:`x^2 + y^2` は、回転軸からの距離の 2 乗である。平面の板なら、面密度を使って 2 重積分で同じように計算する。

半円板の重心
~~~~~~~~~~~~

半径 :math:`R` の一様な半円板 :math:`x^2 + y^2 \le R^2`, :math:`y \ge 0` の重心を求める。対称性から :math:`\bar{x} = 0` である。極座標で計算すると、面積は :math:`\pi R^2 / 2` で、

.. math::

   \iint_D y \, dA = \int_0^{\pi} \int_0^{R} r \sin\theta \cdot r \, dr \, d\theta = \frac{R^3}{3} \cdot 2 = \frac{2R^3}{3}

なので、:math:`\bar{y} = \dfrac{2R^3 / 3}{\pi R^2 / 2} = \dfrac{4R}{3\pi} \approx 0.424 R` となる。

球と円柱の慣性モーメント
~~~~~~~~~~~~~~~~~~~~~~~~

半径 :math:`R`、質量 :math:`M` の一様な球（密度 :math:`\mu = M / (\frac{4}{3}\pi R^3)`）の、中心を通る軸まわりの慣性モーメントを球座標で求める。軸からの距離は :math:`r\sin\theta` なので

.. math::

   I_z = \mu \int_0^{2\pi} \int_0^{\pi} \int_0^{R} (r \sin\theta)^2 \, r^2 \sin\theta \, dr \, d\theta \, d\phi
   = \mu \cdot 2\pi \cdot \frac{4}{3} \cdot \frac{R^5}{5} = \frac{2}{5} M R^2

となる。:math:`\int_0^\pi \sin^3\theta \, d\theta = 4/3` を使った。同じように、半径 :math:`R`、高さ :math:`H` の一様な円柱の中心軸まわりの慣性モーメントは、円柱座標で

.. math::

   I_z = \mu \int_0^{H} \int_0^{2\pi} \int_0^{R} \rho^2 \cdot \rho \, d\rho \, d\phi \, dz = \mu \cdot \frac{\pi R^4 H}{2} = \frac{1}{2} M R^2

となる。質量が軸の近くに集まっている球のほうが、慣性モーメントが小さい。

SciPy による数値計算
--------------------

形が複雑な領域や、原始関数が求まらない関数は、数値積分で計算する。SciPy の ``scipy.integrate.dblquad`` と ``scipy.integrate.tplquad`` は、2 重積分と 3 重積分を累次積分として数値計算する。

.. literalinclude:: ../examples/ch10_scipy_integrals.py
   :pyobject: region_xy
   :lineno-match:
   :caption: ch10_scipy_integrals.py の region_xy()

``dblquad(f, a, b, g, h)`` は :math:`\int_a^b \int_{g(x)}^{h(x)} f(y, x) \, dy \, dx` を計算する。内側の積分の範囲は、外側の変数の関数 ``g``, ``h`` で与える。被積分関数の引数は ``(y, x)`` の順で、内側の積分変数が先に来ることに注意する。間違えやすいので、慣れないうちは答えの分かっている簡単な例で確かめるとよい。

次は、球座標で球の慣性モーメントを計算する例である。被積分関数に体積素 :math:`r^2 \sin\theta` を掛け忘れないようにする。

.. literalinclude:: ../examples/ch10_scipy_integrals.py
   :pyobject: sphere_inertia_ratio
   :lineno-match:
   :caption: ch10_scipy_integrals.py の sphere_inertia_ratio()

この章で手計算した値と、数値計算の結果を比べる。

.. literalinclude:: ../build/outputs/ch10_scipy_integrals.txt
   :language: text
   :caption: ch10_scipy_integrals.py の実行結果

すべての例で、数値計算の結果が厳密な値と一致している。積分の範囲に無限大を含む例（平面全体でのガウス関数の積分）も、``math.inf`` を範囲に指定して計算できる。

サンプルの全体：:download:`ch10_scipy_integrals.py <../examples/ch10_scipy_integrals.py>`

.. tip::

   4 次元以上の積分や、領域が複雑な積分では、累次積分による数値計算は計算量が急に増える。そのような場合は、領域の中に点を乱数でばらまいて平均を取るモンテカルロ積分がよく使われる。

この章のまとめ
--------------

* 重積分は、領域を細かく分けた和の極限であり、分布している量の合計を表す。
* 重積分は累次積分で計算する。一般の領域では、内側の積分の範囲が外側の変数に依存する。
* 積分の順序を交換すると、計算できなかった積分が計算できることがある。順序を変えるときは領域の図を描く。
* 変数変換では、ヤコビアンの絶対値を掛ける。極座標では :math:`r`、円柱座標では :math:`\rho`、球座標では :math:`r^2 \sin\theta` である。
* 質量・重心・慣性モーメントは体積積分で求まる。SciPy の ``dblquad`` と ``tplquad`` で数値計算できる。
