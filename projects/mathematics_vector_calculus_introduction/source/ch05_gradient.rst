.. _ch05:

第 5 章 勾配
============

この章から第 9 章までは、場を微分する方法を扱う。最初に扱う勾配は、スカラー場が最も急に増える向きと、その増え方を表すベクトルである。この章では、勾配の定義と意味、方向微分、等値面との関係、ナブラ演算子を説明し、勾配降下法とポテンシャルへの応用を示す。

坂の向きとしての勾配
--------------------

山の地図を思い浮かべる。地点 :math:`(x, y)` の高さを :math:`f(x, y)` とすると、:math:`f` は平面上のスカラー場であり、地図の等高線は :math:`f` の値が等しい点を結んだ曲線である（:ref:`第 4 章 <ch04>`）。

ある地点に立って周りを見回すと、登り坂がいちばん急な向きが 1 つ決まる。その向きを持ち、長さが坂の急さ（水平に単位長さ進んだときの高さの増え方）に等しい矢印を、地図上の各点に描いたものが\ :numref:`fig-ch05-gradient-contour` である（見やすくするため、矢印の長さは一定の割合で縮めている）。この矢印が、この章で扱う\ :term:`勾配`\ （gradient）である。

.. figure:: ../build/figures/ch05_gradient_contour.svg
   :name: fig-ch05-gradient-contour
   :width: 80%
   :align: center

   2 つの山がある地形の等高線と勾配ベクトル

サンプルの全体：:download:`ch05_gradient_contour.py <../examples/ch05_gradient_contour.py>`

図から次のことが読み取れる。

* 矢印は、どこでも等高線に垂直である。
* 矢印は、山頂に向かう登りの向きを指す。
* 等高線が密な（坂が急な）場所ほど矢印が長い。
* 山頂と、2 つの山の間の鞍部（峠）では、矢印の長さが 0 になる。

これらの性質が成り立つ理由を、以下で順に説明する。

勾配の定義
----------

3 次元のスカラー場 :math:`f(x, y, z)` の勾配を、3 つの偏導関数を成分とするベクトル場として定義する。

.. math::
   :label: eq-ch05-gradient

   \nabla f = \frac{\partial f}{\partial x} \bm{e}_x + \frac{\partial f}{\partial y} \bm{e}_y + \frac{\partial f}{\partial z} \bm{e}_z = \left( \frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}, \frac{\partial f}{\partial z} \right)

勾配は :math:`\operatorname{grad} f` とも書く。2 次元のスカラー場 :math:`f(x, y)` では、:math:`\nabla f = (\partial f / \partial x, \partial f / \partial y)` である。スカラー場からベクトル場が作られる点に注意する。

たとえば :math:`f(x, y, z) = x^2 y + y z^3` の勾配は

.. math::

   \nabla f = (2xy, \ x^2 + z^3, \ 3yz^2)

であり、点 :math:`(1, 2, 1)` では :math:`\nabla f = (4, 2, 6)` となる。

工学でよく使う例として、原点からの距離 :math:`r = \sqrt{x^2 + y^2 + z^2}` の勾配を求める。:math:`\partial r / \partial x = x / r` などから

.. math::

   \nabla r = \left( \frac{x}{r}, \frac{y}{r}, \frac{z}{r} \right) = \frac{\bm{r}}{r} \qquad (r \neq 0)

となる。これは原点から外へ向かう単位ベクトルである。距離が最も速く増えるのは原点から真っすぐ遠ざかる向きであり、その増え方は 1 であるから、直観にも合う。

.. _ch05-directional:

方向微分
--------

勾配が「最も急に増える向き」を表す理由を説明するため、任意の向きへの変化率を考える。点 :math:`\bm{p}` から単位ベクトル :math:`\bm{u}` の向きに距離 :math:`t` だけ進んだ点での値を :math:`f(\bm{p} + t\bm{u})` とする。この関数を :math:`t` で微分した

.. math::

   D_{\bm{u}} f(\bm{p}) = \lim_{t \to 0} \frac{f(\bm{p} + t\bm{u}) - f(\bm{p})}{t}

を、:math:`\bm{u}` の向きの\ :term:`方向微分`\ という。:math:`\bm{u} = \bm{e}_x` なら、方向微分は偏微分 :math:`\partial f / \partial x` そのものである。方向微分は、偏微分を任意の向きに一般化したものといえる。

:math:`\bm{u} = (u_x, u_y, u_z)` とすると、:math:`f(\bm{p} + t\bm{u})` は :math:`x = p_x + t u_x` などを :math:`f` に代入した 1 変数関数なので、連鎖律（:ref:`第 4 章 <ch04>`）から

.. math::
   :label: eq-ch05-directional

   D_{\bm{u}} f = \frac{\partial f}{\partial x} u_x + \frac{\partial f}{\partial y} u_y + \frac{\partial f}{\partial z} u_z = \nabla f \cdot \bm{u}

が得られる。どの向きの変化率も、勾配との内積で計算できる。

:math:`\nabla f` と :math:`\bm{u}` のなす角を :math:`\theta` とすると、:math:`|\bm{u}| = 1` なので

.. math::

   D_{\bm{u}} f = |\nabla f| \cos\theta

である。この式から、勾配の意味がすべて分かる。

* :math:`\theta = 0`、つまり :math:`\bm{u}` が勾配と同じ向きのとき、方向微分は最大値 :math:`|\nabla f|` をとる。勾配の向きは :math:`f` が最も急に増える向きであり、勾配の大きさはその向きの変化率である。
* :math:`\theta = \pi` のとき、方向微分は最小値 :math:`-|\nabla f|` をとる。:math:`-\nabla f` の向きは :math:`f` が最も急に減る向きである。
* :math:`\theta = \pi / 2` のとき、方向微分は 0 である。勾配に垂直な向きには、:math:`f` は（1 次の近似では）変化しない。

なお、:eq:`eq-ch05-directional` の :math:`\bm{u}` は単位ベクトルでなければならない。長さ :math:`|\bm{a}|` のベクトル :math:`\bm{a}` を使って :math:`\nabla f \cdot \bm{a}` を計算すると、変化率の :math:`|\bm{a}|` 倍になる。

:math:`f(x, y) = x^2 y` の点 :math:`(1, 2)` での方向微分を、いくつかの向きで計算して確かめる。勾配は :math:`\nabla f = (2xy, x^2) = (4, 1)`、大きさは :math:`\sqrt{17} \approx 4.123` である。:math:`\bm{u} = (\cos\alpha, \sin\alpha)` として、:math:`\nabla f \cdot \bm{u}` と、中心差分 :math:`(f(\bm{p} + h\bm{u}) - f(\bm{p} - h\bm{u})) / (2h)` による近似値を比べる。

.. literalinclude:: ../examples/ch05_directional.py
   :pyobject: report
   :lineno-match:
   :caption: ch05_directional.py の report()

.. literalinclude:: ../build/outputs/ch05_directional.txt
   :language: text
   :caption: ch05_directional.py の実行結果

2 つの値はよく一致する。勾配の向き（約 14.036 度）で方向微分は最大値 :math:`\sqrt{17}` をとり、そこから 90 度回った向き（約 104.036 度）では 0 になる。180 度の向き（:math:`x` 軸の負の向き）では、勾配と鈍角をなすので負の値になる。

サンプルの全体：:download:`ch05_directional.py <../examples/ch05_directional.py>`

勾配と等値面
------------

:numref:`fig-ch05-gradient-contour` で勾配が等高線に垂直だったことを示す。3 次元では、:math:`f` の値が一定 :math:`c` となる点の集まり :math:`f(x, y, z) = c` は曲面になり、これを等値面という（:ref:`第 4 章 <ch04>`）。2 次元の等高線は、等値面の 2 次元版である。

等値面の上を通る任意の曲線 :math:`\bm{r}(t)` を考える。曲線の上では常に :math:`f(\bm{r}(t)) = c` なので、:math:`t` で微分すると連鎖律から

.. math::

   \frac{d}{dt} f(\bm{r}(t)) = \nabla f \cdot \frac{d\bm{r}}{dt} = 0

となる。:math:`d\bm{r}/dt` は曲線の接線ベクトル（:ref:`第 3 章 <ch03>`）なので、勾配は等値面上のあらゆる曲線の接線ベクトルと直交する。つまり、:math:`\nabla f \neq \bm{0}` である点では、:math:`\nabla f` は等値面の\ :term:`法線ベクトル`\ である。

この性質から、曲面 :math:`f(x, y, z) = c` の点 :math:`\bm{p}` での\ :term:`接平面`\ の方程式が

.. math::

   \nabla f(\bm{p}) \cdot (\bm{r} - \bm{p}) = 0

と求まる。:math:`\bm{r} = (x, y, z)` は接平面上の点である。

例として、楕円体 :math:`x^2/4 + y^2 + z^2/9 = 3` の点 :math:`(2, 1, 3)` での接平面を求める。:math:`f = x^2/4 + y^2 + z^2/9` とすると :math:`\nabla f = (x/2, \ 2y, \ 2z/9)` であり、点 :math:`(2, 1, 3)` では :math:`(1, 2, 2/3)` である。接平面は

.. math::

   1 \cdot (x - 2) + 2 (y - 1) + \frac{2}{3} (z - 3) = 0 \quad \Longleftrightarrow \quad 3x + 6y + 2z = 18

となる。球面 :math:`x^2 + y^2 + z^2 = R^2` では :math:`\nabla f = 2\bm{r}` となり、法線が中心から外へ向かうという、よく知られた結果が得られる。

曲面を :math:`f(x, y, z) = c` の形（陰関数）で表しておけば、勾配を計算するだけで法線ベクトルが求まる。この性質は CG で曲面に陰影を付けるときに使われる（:ref:`第 18 章 <ch18>`）。

全微分と 1 次近似
-----------------

:ref:`第 4 章 <ch04>`\ の全微分は、勾配を使うと内積で書ける。

.. math::

   df = \frac{\partial f}{\partial x} dx + \frac{\partial f}{\partial y} dy + \frac{\partial f}{\partial z} dz = \nabla f \cdot d\bm{r}

ここで :math:`d\bm{r} = (dx, dy, dz)` は位置の微小な変化である。これを近似式として書くと

.. math::

   f(\bm{p} + \Delta\bm{r}) \approx f(\bm{p}) + \nabla f(\bm{p}) \cdot \Delta\bm{r}

となる。1 変数の 1 次近似 :math:`f(x + \Delta x) \approx f(x) + f'(x) \Delta x` で、導関数 :math:`f'` の役割を勾配 :math:`\nabla f` が果たしている。勾配は、多変数関数の「導関数」にあたるベクトルである。逆に、すべての微小な変化 :math:`d\bm{r}` に対して :math:`df = \bm{g} \cdot d\bm{r}` を満たすベクトル :math:`\bm{g}` は勾配に限られる。この見方は、直交座標以外の座標系で勾配を求めるときに使う（:ref:`第 9 章 <ch09>`）。

.. _ch05-nabla:

ナブラ演算子
------------

勾配の定義 :eq:`eq-ch05-gradient` は、次の演算子を :math:`f` に掛けた形をしている。

.. math::

   \nabla = \bm{e}_x \frac{\partial}{\partial x} + \bm{e}_y \frac{\partial}{\partial y} + \bm{e}_z \frac{\partial}{\partial z}

この記号 :math:`\nabla` を\ :term:`ナブラ`\ （nabla）という。ナブラは、成分が偏微分の操作であるベクトルのようなものであり、ベクトル微分演算子と呼ばれる。ナブラ自体は値を持たず、右側にある場に作用して初めて意味を持つ。

ナブラをベクトルのように扱うと、ベクトルの 3 つの積に対応して 3 つの微分ができる。

.. list-table:: ナブラを使う 3 つの微分
   :header-rows: 1
   :widths: 15 20 20 25 20

   * - 演算
     - 式
     - 作用する場と結果
     - 対応するベクトルの積
     - 扱う章
   * - 勾配
     - :math:`\nabla f`
     - スカラー場からベクトル場
     - スカラー倍
     - この章
   * - 発散
     - :math:`\nabla \cdot \bm{F}`
     - ベクトル場からスカラー場
     - 内積
     - :ref:`第 6 章 <ch06>`
   * - 回転
     - :math:`\nabla \times \bm{F}`
     - ベクトル場からベクトル場
     - 外積
     - :ref:`第 7 章 <ch07>`

ただし、ナブラは普通のベクトルとは違い、順序を入れ替えられない。:math:`\nabla f` はベクトル場だが、:math:`f \nabla` は場に作用する前の演算子のままである。ナブラを含む式を変形するときは、「どの場に微分が作用しているか」を常に意識する必要がある（:ref:`第 8 章 <ch08>`）。

勾配の計算規則
--------------

勾配は偏微分を並べたものなので、1 変数の微分の規則がそのまま成り立つ。:math:`f, g` をスカラー場、:math:`a, b` を定数、:math:`h` を 1 変数関数とする。

.. math::

   \nabla (af + bg) &= a \nabla f + b \nabla g \\
   \nabla (fg) &= f \nabla g + g \nabla f \\
   \nabla h(f) &= h'(f) \nabla f

3 番目の式は連鎖律である。たとえば :math:`r^n` の勾配は、:math:`h(r) = r^n` と :math:`\nabla r = \bm{r}/r` から

.. math::

   \nabla r^n = n r^{n-1} \nabla r = n r^{n-2} \bm{r} \qquad (r \neq 0)

となる。:math:`n = -1` とすると :math:`\nabla (1/r) = -\bm{r}/r^3` であり、これは点電荷の電位や万有引力のポテンシャルの勾配として何度も登場する。

応用：勾配降下法
----------------

関数の最小値を数値的に求める方法の 1 つに\ :term:`勾配降下法`\ がある。:math:`-\nabla f` が :math:`f` の最も急に減る向きであることを使い、現在の点から少しずつ坂を下る。

.. math::

   \bm{p}_{k+1} = \bm{p}_k - \eta \nabla f(\bm{p}_k)

:math:`\eta > 0` はステップ幅（機械学習では学習率）と呼ばれる定数である。機械学習では、:math:`f` を誤差（損失関数）、:math:`\bm{p}` をモデルのパラメーターとして、この反復でパラメーターを調整する。

:math:`f(x, y) = x^2/2 + 5y^2` の最小点（原点）を、点 :math:`(-4, 1.2)` から探した結果を\ :numref:`fig-ch05-gradient-descent` に示す。

.. literalinclude:: ../examples/ch05_gradient_descent.py
   :pyobject: gradient_descent
   :lineno-match:
   :caption: ch05_gradient_descent.py の gradient_descent()

.. figure:: ../build/figures/ch05_gradient_descent.svg
   :name: fig-ch05-gradient-descent
   :width: 85%
   :align: center

   ステップ幅による勾配降下法の進み方の違い

:math:`\nabla f = (x, 10y)` なので、1 回の反復で :math:`x` は :math:`(1 - \eta)` 倍、:math:`y` は :math:`(1 - 10\eta)` 倍になる。

* :math:`\eta = 0.05` では :math:`y` は速く 0 に近づくが、:math:`x` は 1 回に 0.95 倍にしかならず、20 回では最小点に届かない。
* :math:`\eta = 0.18` では :math:`y` が 1 回ごとに :math:`-0.8` 倍になり、谷を横切るようにジグザグに進む。
* :math:`\eta \ge 0.2` では :math:`|1 - 10\eta| \ge 1` となり、:math:`y` は 0 に近づかない（:math:`\eta > 0.2` では発散する）。

ジグザグが生じるのは、勾配が等高線に垂直であり、細長い等高線では最小点の方を向かないためである。勾配降下法は、勾配の「その場で最も急な向き」という性質が局所的なものであることをよく示している。

サンプルの全体：:download:`ch05_gradient_descent.py <../examples/ch05_gradient_descent.py>`

応用：ポテンシャルと力
----------------------

物理では、力を位置エネルギー（ポテンシャルエネルギー）\ :math:`U` の勾配で表すことが多い。

.. math::

   \bm{F} = -\nabla U

負号は、力が位置エネルギーの減る向き（坂を下る向き）に働くことを表す。

* 地表近くの重力：:math:`U = mgz` から :math:`\bm{F} = (0, 0, -mg)` となる。
* ばねの力：原点に固定したばね定数 :math:`k` のばねでは :math:`U = kr^2/2` であり、:math:`\nabla U = k r \nabla r = k\bm{r}` から :math:`\bm{F} = -k\bm{r}` となる。

スカラー 1 つで表される :math:`U` から、3 つの成分を持つ力が勾配によって得られる。どのようなベクトル場がこの形に書けるか、また数学と物理で負号の付け方が異なる点は\ :ref:`第 11 章 <ch11>`\ で扱う。

この章のまとめ
--------------

* スカラー場 :math:`f` の勾配 :math:`\nabla f = (\partial f / \partial x, \partial f / \partial y, \partial f / \partial z)` はベクトル場である。
* 単位ベクトル :math:`\bm{u}` の向きの方向微分は :math:`\nabla f \cdot \bm{u}` である。勾配の向きは :math:`f` が最も急に増える向きで、大きさはその変化率である。
* 勾配は等値面（等高線）に垂直であり、陰関数で表した曲面の法線ベクトルになる。
* 全微分は :math:`df = \nabla f \cdot d\bm{r}` と書け、勾配は多変数関数の導関数の役割を果たす。
* ナブラ :math:`\nabla` はベクトルのように扱える微分の演算子であり、勾配・発散・回転を統一的に表す。
* 勾配は、勾配降下法による最適化や、ポテンシャルから力を求める計算に使われる。
