.. _ch13:

第 13 章 グリーンの定理
========================

1 変数の微分積分学の基本定理 :math:`\int_a^b f'(x) \, dx = f(b) - f(a)` は、区間の内部での微分の積分が、区間の端（境界）での値だけで決まることを表している。この章で扱う\ :term:`グリーンの定理`\ は、これを平面の領域に広げたものであり、領域の内部での回転（または発散）の重積分が、境界に沿った線積分に等しいことを主張する。この章では、定理の内容と直観的な説明、循環形と流束形の 2 つの見方、面積の計算への応用を説明し、両辺を数値で計算して一致を確かめる。

.. _ch13-orientation:

平面の領域と境界の向き
----------------------

グリーンの定理では、平面の有界な領域 :math:`D` と、その\ :term:`境界` :math:`\partial D` を考える。境界は、いくつかの滑らかな曲線をつないだ閉曲線であるとする。

線積分の値は曲線をたどる向きで符号が変わる（:ref:`第 11 章 <ch11>`）。そこで、境界の向きを次のように決める。

* 境界の\ :term:`正の向き`\ とは、その向きに進むとき、領域 :math:`D` が常に左手側にある向きである。

穴のない領域では、正の向きは反時計回りである。穴のある領域（たとえば円環）では、外側の境界は反時計回り、内側の境界（穴の縁）は時計回りが正の向きになる。どちらの場合も「領域を左に見て進む」という 1 つの規則で決まる。

.. figure:: ../build/figures/ch13_shoelace.svg
   :name: fig-ch13-shoelace
   :width: 65%
   :align: center

   多角形の領域と、正の向き（反時計回り）にたどる境界

:numref:`fig-ch13-shoelace` は多角形の領域とその境界を描いたものである。頂点を :math:`P_1, P_2, \ldots, P_5` の順にたどると、領域は常に左手側にある。

グリーンの定理
--------------

平面のベクトル場 :math:`\bm{F} = (P(x, y), Q(x, y))` の成分が、領域 :math:`D` とその境界を含む範囲で連続な偏導関数を持つとする。このとき、次の式が成り立つ。これをグリーンの定理という。

.. math::
   :label: eq-ch13-green

   \oint_{\partial D} (P \, dx + Q \, dy) = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dx \, dy

左辺は境界を正の向きに 1 周する線積分、右辺は領域全体での重積分である。右辺の被積分関数 :math:`\partial Q / \partial x - \partial P / \partial y` は、:ref:`第 7 章 <ch07>`\ で導いた回転の :math:`z` 成分そのものである。平面のベクトル場を :math:`\bm{F} = (P, Q, 0)` とみなすと、:eq:`eq-ch13-green` は次のように書ける。

.. math::

   \oint_{\partial D} \bm{F} \cdot d\bm{r} = \iint_D (\nabla \times \bm{F}) \cdot \bm{e}_z \, dx \, dy

つまり、グリーンの定理は「境界に沿った循環は、内部の回転を足し合わせたものに等しい」ことを表している。

.. note::

   成分の偏導関数が連続という条件は重要である。領域の中に場が定義されない点（特異点）があると、定理は成り立つとは限らない。この例は\ :ref:`第 16 章 <ch16>`\ の自由渦で扱う。

微小な長方形による説明
----------------------

:ref:`第 7 章 <ch07>`\ では、微小な長方形 :math:`[x, x + \Delta x] \times [y, y + \Delta y]` の周を反時計回りに 1 周する循環が、近似的に

.. math::

   \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) \Delta x \, \Delta y

になることを見た。これは、グリーンの定理を微小な長方形に適用したものに当たる。

領域 :math:`D` を微小な長方形に分割し、各長方形の循環を足し合わせることを考える（:numref:`fig-ch13-small-rectangles`）。隣り合う 2 つの長方形が共有する辺は、2 つの長方形で互いに逆向きにたどられる（横の辺なら右向きと左向き、縦の辺なら上向きと下向き）。線積分の値は向きを逆にすると符号が変わるので、共有する辺の寄与は打ち消し合う。その結果、足し合わせた後に残るのは、どの長方形とも共有されない辺、つまり領域の境界に沿った線積分だけである。

.. figure:: ../build/figures/ch13_small_rectangles.svg
   :name: fig-ch13-small-rectangles
   :width: 95%
   :align: center

   微小な長方形の循環を足し合わせると、境界の循環だけが残る

一方、各長方形の循環は「回転の :math:`z` 成分 × 面積」なので、その和は回転の重積分になる。長方形を細かくする極限で、:eq:`eq-ch13-green` が得られる。曲がった境界は長方形では正確に表せないが、細かくする極限では誤差が 0 に近づく。

長方形の領域では、直接計算しても確かめられる。:math:`D = [a, b] \times [c, d]` として、右辺の :math:`-\partial P / \partial y` の項を :math:`y` について先に積分すると

.. math::

   -\int_a^b \int_c^d \frac{\partial P}{\partial y} \, dy \, dx = \int_a^b P(x, c) \, dx - \int_a^b P(x, d) \, dx

となる。右辺の第 1 項は下の辺を右向きに、第 2 項は上の辺を左向きにたどる :math:`\int P \, dx` である。左右の辺では :math:`dx = 0` なので :math:`P \, dx` の寄与はない。同じように、:math:`\partial Q / \partial x` の項は左右の辺に沿った :math:`\int Q \, dy` になる。これらを合わせると、境界を反時計回りに 1 周する線積分になる。

循環形と流束形
--------------

グリーンの定理には、もう 1 つの見方がある。:eq:`eq-ch13-green` の :math:`P` を :math:`-Q`、:math:`Q` を :math:`P` に置き換えると

.. math::
   :label: eq-ch13-green-flux

   \oint_{\partial D} (P \, dy - Q \, dx) = \iint_D \left( \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} \right) dx \, dy

を得る。右辺の被積分関数は :math:`\bm{F}` の発散 :math:`\nabla \cdot \bm{F}` である。

左辺の意味を考える。境界を正の向きにたどるとき、接線ベクトルの向きの線素は :math:`d\bm{r} = (dx, dy)` である。これを時計回りに 90° 回したベクトル :math:`(dy, -dx)` は、領域の外向きを向き、大きさは線素の長さ :math:`ds` に等しい。外向きの単位法線ベクトルを :math:`\bm{n}` とすると :math:`\bm{n} \, ds = (dy, -dx)` なので

.. math::

   \oint_{\partial D} \bm{F} \cdot \bm{n} \, ds = \iint_D \nabla \cdot \bm{F} \, dx \, dy

となる。左辺は境界を通って外へ出ていく量（2 次元の流束）である。つまり、「境界から出ていく正味の量は、内部の湧き出しを足し合わせたものに等しい」。これは\ :ref:`第 6 章 <ch06>`\ で微小な直方体について考えた流出量を、2 次元の微小な長方形について足し合わせた結果であり、:ref:`第 14 章 <ch14>`\ のガウスの発散定理の 2 次元版である。

.. list-table:: グリーンの定理の 2 つの形
   :header-rows: 1
   :widths: 16 42 42

   * - 形
     - 式
     - 意味
   * - 循環形
     - :math:`\displaystyle \oint_{\partial D} \bm{F} \cdot d\bm{r} = \iint_D (\nabla \times \bm{F}) \cdot \bm{e}_z \, dx \, dy`
     - 境界に沿った循環 ＝ 内部の回転の和
   * - 流束形
     - :math:`\displaystyle \oint_{\partial D} \bm{F} \cdot \bm{n} \, ds = \iint_D \nabla \cdot \bm{F} \, dx \, dy`
     - 境界から出る流束 ＝ 内部の発散の和

数値で確かめる
--------------

具体的な場で、両辺を別々に数値積分して比べる。場は :math:`\bm{F} = (x - y^3, x^3 + y)` とする。

.. math::

   \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = 3x^2 + 3y^2, \qquad
   \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y} = 2

単位円板では、極座標で重積分すると、循環形の右辺は :math:`\int_0^{2\pi} \int_0^1 3r^2 \cdot r \, dr \, d\theta = 3\pi/2`、流束形の右辺は :math:`2 \times (\text{面積 } \pi) = 2\pi` である。長方形 :math:`[0, 2] \times [0, 1]` では、それぞれ :math:`10` と :math:`4` になる。

境界の線積分は、境界を :math:`t` でパラメーター表示して、:math:`P \, dx + Q \, dy = (P \, x'(t) + Q \, y'(t)) \, dt` を ``scipy.integrate.quad`` で積分する。流束形では :math:`P \, dy - Q \, dx` を積分する。

.. literalinclude:: ../examples/ch13_green_check.py
   :pyobject: boundary_integrals
   :lineno-match:
   :caption: ch13_green_check.py の boundary_integrals()

重積分は ``scipy.integrate.dblquad`` で計算する。``dblquad`` は被積分関数を ``f(y, x)`` の順で受け取り、内側の変数 :math:`y` の範囲を :math:`x` の関数で与えられる。単位円板では :math:`-\sqrt{1 - x^2} \le y \le \sqrt{1 - x^2}` とする。

.. literalinclude:: ../build/outputs/ch13_green_check.txt
   :language: text
   :caption: ch13_green_check.py の実行結果

どちらの領域でも、境界の線積分と領域の重積分が一致している。

サンプルの全体：:download:`ch13_green_check.py <../examples/ch13_green_check.py>`

面積の計算への応用
------------------

グリーンの定理は、重積分を線積分に置き換える道具として使える。特に、:math:`\partial Q / \partial x - \partial P / \partial y = 1` となる :math:`P, Q` を選ぶと、右辺は領域の面積 :math:`A` になる。たとえば :math:`(P, Q) = (0, x)`、:math:`(-y, 0)`、:math:`(-y/2, x/2)` を選ぶと、次の 3 つの式が得られる。

.. math::

   A = \oint_{\partial D} x \, dy = -\oint_{\partial D} y \, dx = \frac{1}{2} \oint_{\partial D} (x \, dy - y \, dx)

境界の形さえ分かれば、内部を調べなくても面積が求まる。たとえば楕円 :math:`x = a \cos t`, :math:`y = b \sin t`\ （:math:`0 \le t \le 2\pi`）では

.. math::

   A = \frac{1}{2} \int_0^{2\pi} (a \cos t \cdot b \cos t + b \sin t \cdot a \sin t) \, dt = \frac{1}{2} \int_0^{2\pi} ab \, dt = \pi a b

となる。

靴ひも公式
~~~~~~~~~~

多角形の面積は、頂点の座標だけから求められる。頂点 :math:`(x_1, y_1), \ldots, (x_n, y_n)` を反時計回りに並べ、:math:`(x_{n+1}, y_{n+1}) = (x_1, y_1)` とする。:math:`(x_i, y_i)` から :math:`(x_{i+1}, y_{i+1})` への辺を直線でたどると、その辺での :math:`\frac{1}{2} \int (x \, dy - y \, dx)` は :math:`\frac{1}{2} (x_i y_{i+1} - x_{i+1} y_i)` になる。これは原点と辺の両端が作る三角形の符号付き面積であり、:ref:`第 2 章 <ch02>`\ で見た 2 次元の外積の半分に当たる。すべての辺について足し合わせると、次の\ :term:`靴ひも公式`\ を得る。

.. math::

   A = \frac{1}{2} \sum_{i=1}^{n} (x_i y_{i+1} - x_{i+1} y_i)

名前は、:math:`x_i y_{i+1}` と :math:`x_{i+1} y_i` を組み合わせる計算の形が、靴ひもを交差させて通す様子に似ていることに由来する。頂点を時計回りに並べると、境界を負の向きにたどることになり、値の符号が逆になる。この性質は、CG や GIS（地理情報システム）で多角形の頂点の並びが反時計回りか時計回りかを判定するのにも使われる。

.. literalinclude:: ../examples/ch13_shoelace.py
   :pyobject: shoelace_area
   :lineno-match:
   :caption: ch13_shoelace.py の shoelace_area()

``np.roll(x, -1)`` は配列を 1 つ前にずらし、:math:`x_{i+1}` の並びを作る。最後の要素の次は最初の要素になるので、:math:`x_{n+1} = x_1` の約束が自然に実現される。:numref:`fig-ch13-shoelace` の多角形で、靴ひも公式と線積分の数値積分を比べた結果を示す。

.. literalinclude:: ../build/outputs/ch13_shoelace.txt
   :language: text
   :caption: ch13_shoelace.py の実行結果

サンプルの全体：:download:`ch13_shoelace.py <../examples/ch13_shoelace.py>`

プラニメーター
~~~~~~~~~~~~~~

:term:`プラニメーター`\ は、図面や地図の上で図形の輪郭をなぞるだけで面積を測る機械式の器具である。代表的な極式プラニメーターは、図面に固定する極、2 本の腕、腕に取り付けた測定車輪からなる。輪郭をなぞる腕（長さ :math:`L`）の先端を境界に沿って 1 周させると、測定車輪は腕に垂直な方向の動きだけを拾って転がる。車輪の転がり方は腕の位置と向きで決まるので、1 周の間に車輪が転がった距離 :math:`w` は、境界に沿ったある線積分で表せる。その線積分にグリーンの定理を適用すると、極が図形の外側にある場合、面積は :math:`A = L w` になる。

つまり、プラニメーターは「境界を 1 周する線積分で面積が求まる」というグリーンの定理を、機械で実現したものである。

穴のある領域
------------

円環のように穴のある領域でも、境界の向きを正しく取ればグリーンの定理が成り立つ。外側の境界を :math:`C_1`\ （反時計回り）、内側の境界を :math:`C_2`\ （時計回り）とすると

.. math::

   \oint_{C_1} \bm{F} \cdot d\bm{r} + \oint_{C_2} \bm{F} \cdot d\bm{r} = \iint_D (\nabla \times \bm{F}) \cdot \bm{e}_z \, dx \, dy

である。これは、穴のある領域に切れ目を入れて穴のない領域とみなし、切れ目を往復する線積分が打ち消し合うことから導ける。

特に、領域 :math:`D` で回転が 0 なら右辺は 0 になる。内側の境界を反時計回りにたどる向きに直すと

.. math::

   \oint_{C_1} \bm{F} \cdot d\bm{r} = \oint_{C_2'} \bm{F} \cdot d\bm{r} \qquad (C_2' \text{ は } C_2 \text{ を逆向きにたどった曲線})

となる。回転が 0 の場では、穴を囲む閉曲線を穴の外側でどのように変形しても循環は変わらない。この性質は、:ref:`第 16 章 <ch16>`\ の自由渦で重要になる。

この章のまとめ
--------------

* 境界の正の向きは、領域を左手側に見て進む向きである。穴のない領域では反時計回りになる。
* グリーンの定理（循環形）は、境界に沿った循環が、内部の回転の :math:`z` 成分の重積分に等しいことを表す。
* 定理は、領域を微小な長方形に分け、共有する辺の線積分が打ち消し合うことで理解できる。
* 流束形では、境界から外へ出る流束が、内部の発散の重積分に等しい。これはガウスの発散定理の 2 次元版である。
* :math:`\partial Q / \partial x - \partial P / \partial y = 1` となる場を選ぶと、線積分で面積が求まる。靴ひも公式とプラニメーターはこの応用である。
