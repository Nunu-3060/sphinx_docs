.. _ch04:

第 4 章 スカラー場とベクトル場
==============================

この章では、本書の主題である「場」を導入し、図で表す方法を説明する。続いて、場の変化を調べる基本の道具である偏微分、全微分、連鎖律を学ぶ。最後に、ベクトル場に沿って進む曲線である流線を扱う。第 II 部の勾配・発散・回転は、すべてこの章の偏微分の組み合わせとして定義される。

場とは何か
----------

空間の各点 :math:`(x, y, z)` に 1 つの実数 :math:`f(x, y, z)` が決まっているとき、:math:`f` をスカラー場という。温度の分布、地形の標高、圧力の分布、電位などがその例である。位置ベクトル :math:`\bm{r} = (x, y, z)` を使って :math:`f(\bm{r})` とも書く。数学的には、3 変数（平面なら 2 変数）の実数値関数のことである。

空間の各点に 1 つのベクトル :math:`\bm{F}(x, y, z)` が決まっているとき、:math:`\bm{F}` をベクトル場という。風や水の流れの速度、電場、磁場、重力などがその例である。成分で書くと

.. math::

   \bm{F}(x, y, z) = (F_x(x, y, z), \ F_y(x, y, z), \ F_z(x, y, z))

であり、ベクトル場は 3 つのスカラー場の組とみなせる。

場は時刻 :math:`t` によって変わることもある。たとえば、朝と昼では部屋の温度の分布が違う。このときは :math:`f(x, y, z, t)` のように時刻も変数に含める。時刻によらない場を\ :term:`定常`\ な場という。本書では、特に断らない限り定常な場を扱う。

場の例をいくつか挙げる。

.. list-table:: 場の例
   :header-rows: 1
   :widths: 30 40 30

   * - 場
     - 式の例
     - 種類
   * - 原点からの距離
     - :math:`f(\bm{r}) = r = \sqrt{x^2 + y^2 + z^2}`
     - スカラー場
   * - 点電荷の電位
     - :math:`V(\bm{r}) = \dfrac{q}{4 \pi \varepsilon_0 r}`
     - スカラー場
   * - 原点から放射状に広がる場
     - :math:`\bm{F}(\bm{r}) = \bm{r} = (x, y, z)`
     - ベクトル場
   * - :math:`z` 軸のまわりの回転
     - :math:`\bm{F}(\bm{r}) = (-y, \ x, \ 0)`
     - ベクトル場
   * - 一様な重力
     - :math:`\bm{F}(\bm{r}) = (0, \ 0, \ -mg)`
     - ベクトル場

スカラー場を図で表す
--------------------

2 変数のスカラー場 :math:`f(x, y)` は、2 通りの方法で図にできる。1 つは、高さ :math:`z = f(x, y)` の曲面（関数のグラフ）として 3 次元で描く方法である。もう 1 つは、:math:`f` の値が等しい点を結んだ曲線 :math:`f(x, y) = c` を、いくつかの :math:`c` について平面に描く方法である。この曲線を\ :term:`等高線`\ という。地図の等高線や天気図の等圧線と同じものである。

:numref:`fig-ch04-scalar-field` は、スカラー場 :math:`f(x, y) = x e^{-(x^2 + y^2)}` を 2 つの方法で描いたものである。右の曲面では山と谷の形がつかみやすく、左の等高線図では値を正確に読み取りやすい。

.. figure:: ../build/figures/ch04_scalar_field.svg
   :name: fig-ch04-scalar-field
   :width: 100%
   :align: center

   スカラー場 :math:`f(x, y) = x e^{-(x^2 + y^2)}` の等高線図と曲面

.. literalinclude:: ../examples/ch04_scalar_field.py
   :pyobject: create_figure
   :lineno-match:
   :caption: ch04_scalar_field.py の create_figure()

サンプルの全体：:download:`ch04_scalar_field.py <../examples/ch04_scalar_field.py>`

matplotlib では、``contourf`` で等高線の間を塗り分け、``contour`` で等高線を描く。等高線の値は一定の間隔で選んでいるので、等高線が密なところほど :math:`f` が急に変化している。地図で等高線が混んでいるところが急斜面であるのと同じである。この「急さ」と「向き」を表すのが\ :ref:`第 5 章 <ch05>`\ の勾配である。

3 変数のスカラー場 :math:`f(x, y, z)` では、:math:`f(x, y, z) = c` を満たす点は曲面になる。これを\ :term:`等値面`\ という。たとえば、:math:`f = r` の等値面は原点を中心とする球面であり、点電荷の電位の等値面（等電位面）も球面である。

ベクトル場を図で表す
--------------------

矢印図
~~~~~~

ベクトル場を図にする最も直接的な方法は、格子状に並べた点ごとに、その点のベクトルを矢印で描くことである。これを矢印図といい、matplotlib では ``quiver`` で描ける。ただし、ベクトルの大きさをそのまま矢印の長さにすると、矢印どうしが重なって見にくくなる。``quiver`` は既定で矢印の長さをまとめて縮小する。矢印の色で大きさを表すこともある。

流線
~~~~

矢印図では、点と点の間の様子が分かりにくい。そこで、各点でベクトル場に接する曲線を描くことがある。この曲線を\ :term:`流線`\ という。流れの速度場 :math:`\bm{v}` の流線は、小さな粒子（煙や染料）が流れに乗って動くときの道筋を表す。matplotlib では ``streamplot`` で描ける。

:numref:`fig-ch04-vector-field` は、ベクトル場 :math:`\bm{F}(x, y) = (x - y, \ x + y)` を 2 つの方法で描いたものである。原点から渦を巻きながら外に広がっていく様子が分かる。このベクトル場は「放射状に広がる場 :math:`(x, y)`」と「原点のまわりを回る場 :math:`(-y, x)`」の和であり、:ref:`第 6 章 <ch06>`\ の発散と\ :ref:`第 7 章 <ch07>`\ の回転の両方を持つ。

.. figure:: ../build/figures/ch04_vector_field.svg
   :name: fig-ch04-vector-field
   :width: 100%
   :align: center

   ベクトル場 :math:`\bm{F}(x, y) = (x - y, \ x + y)` の矢印図と流線

.. literalinclude:: ../examples/ch04_vector_field.py
   :pyobject: create_figure
   :lineno-match:
   :caption: ch04_vector_field.py の create_figure()

サンプルの全体：:download:`ch04_vector_field.py <../examples/ch04_vector_field.py>`

流線を求める
~~~~~~~~~~~~

流線は、各点での接線の方向がベクトル場の向きに一致する曲線である。流線を :math:`\bm{r}(s)` とパラメーター表示すると、接線ベクトルが :math:`\bm{F}` に平行であることから

.. math::

   \frac{d\bm{r}}{ds} = \bm{F}(\bm{r}(s))

という常微分方程式を満たすように選べる（:math:`s` は流線に沿ったパラメーターで、弧長とは限らない）。成分で書いてパラメーター :math:`s` を消去すると、

.. math::

   \frac{dx}{F_x} = \frac{dy}{F_y} = \frac{dz}{F_z}

という形にもなる。

例として、:math:`\bm{F}(x, y) = (-y, \ x)` の流線を求める。:math:`dx/(-y) = dy/x` から :math:`x \, dx + y \, dy = 0` となり、積分すると :math:`x^2 + y^2 = c`\ （定数）が得られる。流線は原点を中心とする円である。

流線の方程式は、一般には手で解けない。その場合は、数値的に解けばよい。次のサンプルは、SciPy の ``integrate.solve_ivp``\ （常微分方程式の初期値問題を解く関数）で、点 :math:`(1, 0)` を通る流線を求める。

.. literalinclude:: ../examples/ch04_streamline.py
   :pyobject: report
   :lineno-match:
   :caption: ch04_streamline.py の report()

サンプルの全体：:download:`ch04_streamline.py <../examples/ch04_streamline.py>`

.. literalinclude:: ../build/outputs/ch04_streamline.txt
   :language: text
   :caption: ch04_streamline.py の実行結果

原点からの距離が常に 1 であり、流線が半径 1 の円であることが確かめられる。

流線には次の性質がある。

* :math:`\bm{F} \ne \bm{0}` の点では、その点を通る流線は 1 本だけであり、流線どうしは交わらない（常微分方程式の解の一意性による）。
* 流線は場の向きを表すが、大きさは表さない。流れの速さは、流線の間隔（流管の太さ）や色で表すことが多い。
* 時刻によって変わる流れでは、ある瞬間の流線と、1 つの粒子が実際にたどる道筋（流跡線）は一般に一致しない。定常な流れでは両者は一致する。

偏微分
------

偏微分の定義
~~~~~~~~~~~~

場の変化を調べるには、多変数関数の微分が必要になる。最も基本的なのは、1 つの変数だけを動かし、ほかの変数を定数とみなして微分する方法である。2 変数関数 :math:`f(x, y)` について

.. math::

   \frac{\partial f}{\partial x}(x, y) &= \lim_{h \to 0} \frac{f(x + h, y) - f(x, y)}{h} \\
   \frac{\partial f}{\partial y}(x, y) &= \lim_{h \to 0} \frac{f(x, y + h) - f(x, y)}{h}

を、それぞれ :math:`f` の :math:`x` および :math:`y` についての\ :term:`偏微分`\ （partial derivative）という。:math:`\partial` は「ラウンド」や「パーシャル」と読む。偏微分を関数とみなしたものを\ :term:`偏導関数`\ という。:math:`\partial f / \partial x` は :math:`f_x` とも書く。3 変数以上でも同様に定義する。

図形的には、:math:`\partial f / \partial x` は、曲面 :math:`z = f(x, y)` を平面 :math:`y = \text{一定}` で切った断面の曲線の傾きである。地形で言えば、真東に進んだときの坂の傾きである。同様に、:math:`\partial f / \partial y` は真北に進んだときの坂の傾きである。

計算は、1 変数の微分の規則をそのまま使えばよい。たとえば、\ :ref:`第 1 章 <ch01>`\ で SymPy を使って偏微分した :math:`f(x, y) = x^2 y + \sin(xy)` を手で計算すると

.. math::

   \frac{\partial f}{\partial x} = 2xy + y \cos(xy), \qquad
   \frac{\partial f}{\partial y} = x^2 + x \cos(xy)

となり、第 1 章の SymPy の結果と一致する。:math:`x` で偏微分するときは :math:`y` を定数とみなし、:math:`\sin(xy)` には合成関数の微分を使う。

偏微分の値は、座標軸の方向の変化しか表さない。斜めの方向の変化は、次に説明する全微分を使って、偏微分の組み合わせで表せる（:ref:`第 5 章 <ch05>`\ の方向微分）。

高階の偏微分
~~~~~~~~~~~~

偏導関数をさらに偏微分したものを 2 階の偏導関数という。2 変数の場合は次の 4 つがある。

.. math::

   f_{xx} = \frac{\partial^2 f}{\partial x^2}, \quad
   f_{xy} = \frac{\partial^2 f}{\partial y \partial x}, \quad
   f_{yx} = \frac{\partial^2 f}{\partial x \partial y}, \quad
   f_{yy} = \frac{\partial^2 f}{\partial y^2}

:math:`f_{xy}` は「:math:`x` で偏微分してから :math:`y` で偏微分する」ことを表す。:math:`\partial` を使う書き方では、右側の変数から先に微分する。2 つの書き方で順序の表し方が逆になることに注意する。

偏微分の順序は、ふつうは結果に影響しない。

.. admonition:: シュワルツの定理

   :math:`f_{xy}` と :math:`f_{yx}` が存在して連続なら、:math:`f_{xy} = f_{yx}` である。

この定理を\ :term:`シュワルツの定理`\ という。連続でない場合には成り立たない例もあるが、工学で扱う滑らかな場ではまず問題にならない。本書では、場は十分に滑らかであるとし、偏微分の順序を自由に入れ替える。:ref:`第 8 章 <ch08>`\ で示す :math:`\nabla \times (\nabla f) = \bm{0}` や :math:`\nabla \cdot (\nabla \times \bm{F}) = 0` は、この定理から導かれる。

全微分と 1 次近似
-----------------

全微分
~~~~~~

:math:`x` と :math:`y` を同時に少しずつ動かしたとき、:math:`f` はどれだけ変わるだろうか。点 :math:`(x, y)` から :math:`(x + dx, y + dy)` に動くとき、まず :math:`x` 方向に :math:`dx` 動くと :math:`f` はおよそ :math:`f_x \, dx` 変わり、続いて :math:`y` 方向に :math:`dy` 動くとおよそ :math:`f_y \, dy` 変わる。合わせると

.. math::

   df = \frac{\partial f}{\partial x} \, dx + \frac{\partial f}{\partial y} \, dy

となる。これを :math:`f` の\ :term:`全微分`\ という。3 変数なら :math:`df = f_x \, dx + f_y \, dy + f_z \, dz` である。

全微分は、:math:`f` の変化を 1 次式で近似する。

.. math::

   f(a + dx, \ b + dy) \approx f(a, b) + f_x(a, b) \, dx + f_y(a, b) \, dy

右辺は、点 :math:`(a, b)` で曲面 :math:`z = f(x, y)` に接する平面（接平面）の式である。この近似の誤差は、:math:`dx` や :math:`dy` の 2 次の大きさ（:math:`dx` と :math:`dy` を半分にすると、誤差はおよそ 4 分の 1）になる。このように 1 次式で近似できるとき、:math:`f` は全微分可能（または単に微分可能）であるという。偏導関数が存在して連続なら、関数は全微分可能である。

.. note::

   偏導関数が存在するだけでは、全微分可能とは限らない。偏微分は座標軸の方向しか見ていないので、斜めの方向に不連続な関数でも偏導関数が存在することがある。本書で扱う場は偏導関数が連続であり、この問題は起きない。

工学の例：誤差の伝播
~~~~~~~~~~~~~~~~~~~~

全微分は、測定誤差が計算結果にどう伝わるかを見積もるのに使える。たとえば、円柱の体積 :math:`V = \pi r^2 h` について、全微分は

.. math::

   dV = 2 \pi r h \, dr + \pi r^2 \, dh

である。両辺を :math:`V` で割ると :math:`dV/V = 2 \, dr/r + dh/h` となる。半径と高さの相対誤差がともに 1 % なら、体積の相対誤差は最大でおよそ 3 % になる。半径の誤差は 2 倍に効くので、半径をより正確に測る必要があることが分かる。

連鎖律
------

曲線に沿った変化
~~~~~~~~~~~~~~~~

点が曲線 :math:`\bm{r}(t) = (x(t), y(t), z(t))` に沿って動くとき、その点でのスカラー場の値 :math:`f(x(t), y(t), z(t))` は :math:`t` の関数になる。全微分の式の両辺を :math:`dt` で割ると、その変化率が得られる。

.. math::
   :label: eq-ch04-chain-curve

   \frac{d}{dt} f(\bm{r}(t)) = \frac{\partial f}{\partial x} \frac{dx}{dt} + \frac{\partial f}{\partial y} \frac{dy}{dt} + \frac{\partial f}{\partial z} \frac{dz}{dt}

これを多変数関数の\ :term:`連鎖律`\ （chain rule）という。右辺は、偏導関数を並べたベクトル :math:`(f_x, f_y, f_z)` と、曲線の速度 :math:`\bm{r}'(t) = (x', y', z')` の内積になっている。このベクトルこそが\ :ref:`第 5 章 <ch05>`\ で学ぶ勾配 :math:`\nabla f` であり、:eq:`eq-ch04-chain-curve` は :math:`df/dt = \nabla f \cdot \bm{r}'(t)` と書ける。

たとえば、温度分布 :math:`f` の中を速度 :math:`\bm{v}` で移動する温度計が感じる温度の変化率は、:eq:`eq-ch04-chain-curve` で求められる。

変数変換
~~~~~~~~

:math:`x, y` がさらに別の 2 つの変数 :math:`u, v` の関数 :math:`x(u, v), \ y(u, v)` であるとき、:math:`f(x(u, v), y(u, v))` を :math:`u` で偏微分すると

.. math::

   \frac{\partial f}{\partial u} = \frac{\partial f}{\partial x} \frac{\partial x}{\partial u} + \frac{\partial f}{\partial y} \frac{\partial y}{\partial u}, \qquad
   \frac{\partial f}{\partial v} = \frac{\partial f}{\partial x} \frac{\partial x}{\partial v} + \frac{\partial f}{\partial y} \frac{\partial y}{\partial v}

となる。:math:`v` を定数とみなして :math:`u` だけを動かせば、点 :math:`(x, y)` は 1 本の曲線を描くので、:eq:`eq-ch04-chain-curve` がそのまま使える。

例として、極座標 :math:`x = r \cos \theta`、:math:`y = r \sin \theta` を考える。:math:`\partial x / \partial r = \cos \theta`、:math:`\partial y / \partial r = \sin \theta`、:math:`\partial x / \partial \theta = -r \sin \theta`、:math:`\partial y / \partial \theta = r \cos \theta` なので

.. math::

   \frac{\partial f}{\partial r} = f_x \cos \theta + f_y \sin \theta, \qquad
   \frac{\partial f}{\partial \theta} = -f_x \, r \sin \theta + f_y \, r \cos \theta

となる。:math:`\partial f / \partial r` は、原点から外向きに進んだときの :math:`f` の変化率である。この種の計算は、:ref:`第 9 章 <ch09>`\ で曲線座標系の勾配などを求めるときに使う。

SymPy と数値計算による確認
--------------------------

ここまでの内容を、同じ :math:`f(x, y) = x^2 y + \sin(xy)` で確かめる。次のサンプルは、偏導関数、偏微分の順序交換、中心差分による数値微分、1 次近似の誤差、連鎖律を順に計算する。

.. literalinclude:: ../examples/ch04_partial.py
   :pyobject: report
   :lineno-match:
   :caption: ch04_partial.py の report()

サンプルの全体：:download:`ch04_partial.py <../examples/ch04_partial.py>`

.. literalinclude:: ../build/outputs/ch04_partial.txt
   :language: text
   :caption: ch04_partial.py の実行結果

実行結果から次のことが分かる。

* :math:`f_{xy}` と :math:`f_{yx}` の差は 0 であり、シュワルツの定理のとおり偏微分の順序によらない。
* 偏微分は、:math:`(f(x + h, y) - f(x - h, y)) / (2h)` のような差分で数値的に近似できる（中心差分）。:math:`h` を 10 分の 1 にすると、誤差はおよそ 100 分の 1 になる。差分による数値微分は\ :ref:`第 18 章 <ch18>`\ で詳しく扱う。
* 1 次近似の誤差は、:math:`dx = dy = 0.1` で約 :math:`4.5 \times 10^{-3}`、:math:`0.01` で約 :math:`5.1 \times 10^{-5}` であり、ずれを 10 分の 1 にすると誤差はおよそ 100 分の 1 になる。誤差がずれの 2 次の大きさであることが分かる。
* 単位円 :math:`(\cos t, \sin t)` に沿った :math:`df/dt` は、式に代入してから直接微分しても、連鎖律で計算しても同じになる。

この章のまとめ
--------------

* 空間の各点に数が決まっているものをスカラー場、ベクトルが決まっているものをベクトル場という。ベクトル場は 3 つのスカラー場の組である。
* スカラー場は等高線（3 次元では等値面）で、ベクトル場は矢印図や流線で図にできる。流線は :math:`d\bm{r}/ds = \bm{F}(\bm{r})` を満たす曲線である。
* 偏微分は、1 つの変数だけを動かしたときの変化率である。偏導関数が連続なら、偏微分の順序は交換できる（シュワルツの定理）。
* 全微分 :math:`df = f_x \, dx + f_y \, dy + f_z \, dz` は、場の変化を 1 次式で近似する。誤差の見積もりにも使える。
* 連鎖律により、曲線に沿った変化率は :math:`(f_x, f_y, f_z)` と速度の内積で表される。このベクトルが次の章の勾配である。
