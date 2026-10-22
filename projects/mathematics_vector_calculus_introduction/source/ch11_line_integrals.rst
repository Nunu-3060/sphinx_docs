.. _ch11:

第 11 章 線積分と保存場
========================

曲線に沿って場を積分するのが線積分である。この章では、スカラー場の線積分（曲線に沿った量の合計）と、ベクトル場の線積分（力がする仕事や流れの循環）を説明する。さらに、線積分の値が経路によらない場（保存場）と、その場を表すポテンシャルを扱う。

スカラー場の線積分
------------------

定義
~~~~

針金の線密度 :math:`\mu` が場所によって違うとき、針金全体の質量を求めるには、針金を短く分けて「線密度 × 長さ」を足し合わせればよい。これを極限にしたものが、スカラー場の\ :term:`線積分`\ である。

曲線 :math:`C` を :math:`\bm{r}(t)`\ （:math:`a \le t \le b`）とパラメーター表示する。パラメーターが :math:`dt` だけ変わると、点は曲線に沿って :math:`ds = |\bm{r}'(t)| \, dt` だけ進む（:ref:`第 3 章 <ch03>`\ の弧長）。したがって、スカラー場 :math:`f` の線積分は次のように計算できる。

.. math::

   \int_C f \, ds = \int_a^b f(\bm{r}(t)) \, |\bm{r}'(t)| \, dt

:math:`f = 1` なら、線積分は曲線の長さである。

この値は、曲線のパラメーター表示の選び方にも、曲線をたどる向きにもよらない。:math:`ds` は長さなので、常に正だからである。

例：らせん状の針金の質量
~~~~~~~~~~~~~~~~~~~~~~~~

らせん :math:`\bm{r}(t) = (\cos t, \sin t, t)`\ （:math:`0 \le t \le 2\pi`）の形をした針金があり、線密度が高さに比例して :math:`\mu = z` であるとする。:math:`\bm{r}'(t) = (-\sin t, \cos t, 1)` なので :math:`|\bm{r}'(t)| = \sqrt{2}` であり、質量は

.. math::

   \int_C z \, ds = \int_0^{2\pi} t \sqrt{2} \, dt = 2\sqrt{2} \, \pi^2 \approx 27.92

となる。

ベクトル場の線積分
------------------

仕事
~~~~

一定の力 :math:`\bm{F}` を受けながら物体が変位 :math:`\Delta\bm{r}` だけ動くと、力がする仕事は :math:`\bm{F} \cdot \Delta\bm{r}` である（:ref:`第 2 章 <ch02>`）。力が場所によって変わる場合や、物体が曲線に沿って動く場合は、経路を短く分けて仕事を足し合わせる。これを極限にしたものが、ベクトル場の線積分である。

.. math::

   \int_C \bm{F} \cdot d\bm{r} = \int_a^b \bm{F}(\bm{r}(t)) \cdot \bm{r}'(t) \, dt

成分で書くと :math:`d\bm{r} = (dx, dy, dz)` なので、次の形でも書かれる。

.. math::

   \int_C \bm{F} \cdot d\bm{r} = \int_C (F_x \, dx + F_y \, dy + F_z \, dz)

単位接線ベクトル :math:`\bm{T}` を使うと :math:`d\bm{r} = \bm{T} \, ds` なので、:math:`\int_C \bm{F} \cdot d\bm{r} = \int_C (\bm{F} \cdot \bm{T}) \, ds` である。つまり、ベクトル場の線積分は、場の接線方向の成分 :math:`\bm{F} \cdot \bm{T}` をスカラー場として線積分したものである。曲線に垂直な成分は寄与しない。

向きによる符号の変化
~~~~~~~~~~~~~~~~~~~~

ベクトル場の線積分は、曲線をたどる向きを逆にすると符号が変わる。逆向きでは :math:`\bm{T}` が :math:`-\bm{T}` になるからである。曲線 :math:`C` を逆向きにたどる曲線を :math:`-C` と書くと

.. math::

   \int_{-C} \bm{F} \cdot d\bm{r} = -\int_C \bm{F} \cdot d\bm{r}

が成り立つ。スカラー場の線積分と違い、ベクトル場の線積分では曲線の向きを指定しなければならない。一方、同じ向きにたどるなら、パラメーター表示の選び方にはよらない。

循環
~~~~

始点と終点が一致する曲線を\ :term:`閉曲線`\ という。閉曲線に沿ったベクトル場の線積分を循環といい、:math:`\oint_C` と書く。

.. math::

   \Gamma = \oint_C \bm{F} \cdot d\bm{r}

流れの速度場 :math:`\bm{v}` の循環は、流れが閉曲線に沿ってどれだけ回っているかを表す。:ref:`第 7 章 <ch07>`\ の回転（の成分）は、微小な長方形を一周する循環を面積で割ったものであった。平面の閉曲線は、特に断らない限り反時計回りを正の向きとする。

経路による違い
--------------

線積分の値は、一般には始点と終点だけでなく、途中の経路によって変わる。:numref:`fig-ch11-two-paths` の 2 つのベクトル場

.. math::

   \bm{F}_1 = (y, x), \qquad \bm{F}_2 = (-y, x)

を、原点 A から点 B :math:`(1, 1)` までの 3 つの経路に沿って線積分してみる。

* :math:`C_1`：線分 :math:`\bm{r}(t) = (t, t)`\ （:math:`0 \le t \le 1`）
* :math:`C_2`：:math:`(1, 0)` を経由する折れ線
* :math:`C_3`：放物線 :math:`\bm{r}(t) = (t, t^2)`\ （:math:`0 \le t \le 1`）

.. figure:: ../build/figures/ch11_two_paths.svg
   :name: fig-ch11-two-paths
   :width: 95%
   :align: center

   2 つのベクトル場と、A から B への 3 つの経路

たとえば :math:`C_3` では :math:`\bm{r}'(t) = (1, 2t)` なので、次のようになる。

.. math::

   \int_{C_3} \bm{F}_1 \cdot d\bm{r} &= \int_0^1 (t^2, t) \cdot (1, 2t) \, dt = \int_0^1 3t^2 \, dt = 1 \\
   \int_{C_3} \bm{F}_2 \cdot d\bm{r} &= \int_0^1 (-t^2, t) \cdot (1, 2t) \, dt = \int_0^1 t^2 \, dt = \frac{1}{3}

すべての経路の結果を\ :numref:`table-ch11-paths` に示す。

.. list-table:: 3 つの経路に沿った線積分
   :name: table-ch11-paths
   :header-rows: 1
   :widths: 40 30 30

   * - 経路
     - :math:`\bm{F}_1 = (y, x)`
     - :math:`\bm{F}_2 = (-y, x)`
   * - :math:`C_1`\ （線分）
     - 1
     - 0
   * - :math:`C_2`\ （折れ線）
     - 1
     - 1
   * - :math:`C_3`\ （放物線）
     - 1
     - 1/3

:math:`\bm{F}_1` ではどの経路でも 1 になるが、:math:`\bm{F}_2` では経路によって値が違う。:math:`\bm{F}_2` は原点のまわりを回る場なので、経路が原点からどう離れていくかで、場に沿って進む量が変わるのである。次のサンプルは、これらの線積分を SciPy で数値計算する。

.. literalinclude:: ../examples/ch11_two_paths.py
   :pyobject: line_integral
   :lineno-match:
   :caption: ch11_two_paths.py の line_integral()

.. literalinclude:: ../build/outputs/ch11_two_paths.txt
   :language: text
   :caption: ch11_two_paths.py の実行結果

単位円を反時計回りに 1 周する循環は、:math:`\bm{F}_1` では 0、:math:`\bm{F}_2` では :math:`2\pi` になる。2 つの経路の線積分が違うことと、閉曲線の循環が 0 でないことは同じことを表している。経路 :math:`C` と :math:`C'` が同じ始点と終点を持つなら、:math:`C` をたどってから :math:`C'` を逆にたどると閉曲線になり、その循環は 2 つの線積分の差に等しいからである。

サンプルの全体：:download:`ch11_two_paths.py <../examples/ch11_two_paths.py>`

保存場とポテンシャル
--------------------

勾配の線積分
~~~~~~~~~~~~

:math:`\bm{F}_1 = (y, x)` は、スカラー場 :math:`\phi = xy` の勾配 :math:`\nabla \phi = (y, x)` である。勾配の線積分は、次の式で計算できる。

.. math::
   :label: eq-ch11-gradient-theorem

   \int_C \nabla \phi \cdot d\bm{r} = \phi(\mathrm{B}) - \phi(\mathrm{A})

A と B は曲線 :math:`C` の始点と終点である。これは、連鎖律（:ref:`第 4 章 <ch04>`）から

.. math::

   \frac{d}{dt} \phi(\bm{r}(t)) = \nabla \phi(\bm{r}(t)) \cdot \bm{r}'(t)

となるので、両辺を :math:`t` について :math:`a` から :math:`b` まで積分すると、右辺は線積分 :math:`\int_C \nabla \phi \cdot d\bm{r}`、左辺は :math:`\phi(\bm{r}(b)) - \phi(\bm{r}(a))` になることから分かる。式 :eq:`eq-ch11-gradient-theorem` は 1 変数の微分積分学の基本定理 :math:`\int_a^b f'(x) \, dx = f(b) - f(a)` を曲線に拡張したもので、勾配定理（線積分の基本定理）と呼ばれる。右辺は始点と終点だけで決まるので、勾配の線積分は経路によらない。:math:`\bm{F}_1` の線積分がどの経路でも :math:`\phi(1, 1) - \phi(0, 0) = 1` になったのはこのためである。

保存場の定義
~~~~~~~~~~~~

ある領域で、任意の 2 点を結ぶ線積分が経路によらないベクトル場を\ :term:`保存場`\ という。このとき、次の 3 つは同値である。

1. :math:`\bm{F}` の線積分が経路によらない。
2. 領域内の任意の閉曲線で :math:`\oint_C \bm{F} \cdot d\bm{r} = 0` である。
3. :math:`\bm{F} = \nabla \phi` となるスカラー場 :math:`\phi` が存在する。

:math:`\phi` を :math:`\bm{F}` の\ :term:`ポテンシャル`\ （スカラーポテンシャル）という。3 から 1 は勾配定理そのものであり、1 と 2 が同値であることは前の節で説明した。1 から 3 は、基準点 :math:`\bm{r}_0` を決めて

.. math::

   \phi(\bm{r}) = \int_{\bm{r}_0}^{\bm{r}} \bm{F} \cdot d\bm{r}

と定義すればよい。線積分が経路によらないので、:math:`\phi` は終点 :math:`\bm{r}` だけで決まる。終点を :math:`x` 方向に少し動かして差を取ると :math:`\partial \phi / \partial x = F_x` となり、他の成分も同様なので :math:`\nabla \phi = \bm{F}` が成り立つ。ポテンシャルには定数を加える自由がある。

物理での符号の慣習
~~~~~~~~~~~~~~~~~~

物理では、保存力 :math:`\bm{F}` に対して :math:`\bm{F} = -\nabla U` となる :math:`U` を\ **位置エネルギー**\ （ポテンシャルエネルギー）と呼ぶ。負号が付くのは、力が位置エネルギーの低い方へ向かうように定義するためである。このとき、A から B まで動く間に力がする仕事は

.. math::

   W = \int_C \bm{F} \cdot d\bm{r} = U(\mathrm{A}) - U(\mathrm{B})

で、位置エネルギーの減少量に等しい。電場でも同様に :math:`\bm{E} = -\nabla V`\ （:math:`V` は電位）と書く。本書では、数学的な議論では :math:`\bm{F} = \nabla \phi`、物理の議論では :math:`\bm{F} = -\nabla U` を使う。ポテンシャルという言葉が出てきたら、どちらの符号の約束かを確かめるとよい。

例：重力の仕事
~~~~~~~~~~~~~~

地表付近の重力 :math:`\bm{F} = (0, 0, -mg)` は、:math:`U = mgz` とすると :math:`\bm{F} = -\nabla U` を満たす保存場である。物体がらせん :math:`\bm{r}(t) = (\cos t, \sin t, t)` に沿って :math:`t = 2\pi` から :math:`t = 0` まで下る間に重力がする仕事と、同じ 2 点をまっすぐ結ぶ経路で下る間の仕事を比べる。

.. literalinclude:: ../examples/ch11_helix.py
   :pyobject: gravity_work_helix
   :lineno-match:
   :caption: ch11_helix.py の gravity_work_helix()

.. literalinclude:: ../build/outputs/ch11_helix.txt
   :language: text
   :caption: ch11_helix.py の実行結果

サンプルでは :math:`m = 1 \, \mathrm{kg}`、:math:`g = 9.8 \, \mathrm{m/s^2}` とした。どちらの経路でも、仕事は位置エネルギーの減少 :math:`mgh = mg \cdot 2\pi` に等しい。1 行目は、前の節で求めた針金の質量の数値計算である。

サンプルの全体：:download:`ch11_helix.py <../examples/ch11_helix.py>`

例：摩擦力
~~~~~~~~~~

床の上で物体を引きずるときの動摩擦力は、大きさが一定（:math:`\mu_k N`、:math:`\mu_k` は動摩擦係数、:math:`N` は垂直抗力）で、向きが常に運動の向きと逆である。したがって、摩擦力がする仕事は :math:`-\mu_k N \times \text{（経路の長さ）}` となり、遠回りするほど大きな負の仕事をする。摩擦力は経路によって仕事が変わる力の代表例であり、位置エネルギーで表すことはできない。そもそも摩擦力は位置だけでなく運動の向きで決まるので、位置の関数としてのベクトル場ではない。

ポテンシャルの求め方
--------------------

保存場であるための必要条件
~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\bm{F} = \nabla \phi` なら、:ref:`第 8 章 <ch08>`\ の公式 :math:`\nabla \times (\nabla \phi) = \bm{0}` から

.. math::

   \nabla \times \bm{F} = \bm{0}

が成り立つ。つまり、渦なしの場であることは、保存場であるための必要条件である。:math:`\bm{F}_2 = (-y, x)` は\ :ref:`第 7 章 <ch07>`\ の角速度 :math:`\omega = 1` の剛体回転と同じ場であり、:math:`\nabla \times \bm{F}_2 = (0, 0, 2) \ne \bm{0}` なので、保存場ではない。

逆に、:math:`\nabla \times \bm{F} = \bm{0}` なら保存場かというと、領域の形によっては成り立たない。領域が\ :term:`単連結`\ である場合、つまり、領域内の任意の閉曲線を、領域から出ることなく連続的に縮めて 1 点にできる場合には、:math:`\nabla \times \bm{F} = \bm{0}` なら保存場である。このことは、:ref:`第 15 章 <ch15>`\ のストークスの定理を使って\ :ref:`第 16 章 <ch16>`\ で示す。空間全体や球の内部は単連結だが、穴の開いた平面や、:math:`z` 軸を除いた空間は単連結ではない。単連結でない領域で、渦なしなのに保存場でない例（自由渦）は\ :ref:`第 16 章 <ch16>`\ で扱う。

成分を順に積分する
~~~~~~~~~~~~~~~~~~

渦なしの場のポテンシャルは、成分を順に積分して求められる。例として、次の場のポテンシャルを求める。

.. math::

   \bm{F} = (2xy + z, \ x^2 + 2yz, \ x + y^2 + 3z^2)

回転を計算すると :math:`\bm{0}` になるので、空間全体（単連結）で保存場である。

1. :math:`\partial \phi / \partial x = F_x` を :math:`x` で積分する。積分定数は :math:`y` と :math:`z` の関数 :math:`g(y, z)` になる。

   .. math::

      \phi = x^2 y + xz + g(y, z)

2. :math:`\partial \phi / \partial y = x^2 + \partial g / \partial y` が :math:`F_y = x^2 + 2yz` に等しいので、:math:`\partial g / \partial y = 2yz` である。:math:`y` で積分して :math:`g = y^2 z + h(z)` を得る。
3. :math:`\partial \phi / \partial z = x + y^2 + h'(z)` が :math:`F_z = x + y^2 + 3z^2` に等しいので、:math:`h'(z) = 3z^2`、:math:`h = z^3 + \text{定数}` である。

以上から :math:`\phi = x^2 y + xz + y^2 z + z^3 + \text{定数}` を得る。手順 2 と 3 で、:math:`\partial g / \partial y` が :math:`x` を含まず、:math:`h'(z)` が :math:`x, y` を含まないことは、回転が :math:`\bm{0}` であることから保証される。回転が :math:`\bm{0}` でない場で同じことをすると、どこかの手順で矛盾が生じる。

次のサンプルは、同じ手順を SymPy で実行する。

.. literalinclude:: ../examples/ch11_potential.py
   :pyobject: report
   :lineno-match:
   :caption: ch11_potential.py の report()

.. literalinclude:: ../build/outputs/ch11_potential.txt
   :language: text
   :caption: ch11_potential.py の実行結果

ポテンシャルが求まれば、どんな経路の線積分も、端点でのポテンシャルの差として計算できる。

サンプルの全体：:download:`ch11_potential.py <../examples/ch11_potential.py>`

この章のまとめ
--------------

* スカラー場の線積分 :math:`\int_C f \, ds` は曲線に沿った量の合計で、向きによらない。
* ベクトル場の線積分 :math:`\int_C \bm{F} \cdot d\bm{r}` は、場の接線方向の成分の積分で、仕事を表す。向きを逆にすると符号が変わる。閉曲線に沿った線積分を循環という。
* 線積分の値は一般に経路によって変わる。経路によらない場を保存場といい、保存場はポテンシャルの勾配として表せる。
* 勾配の線積分は、端点でのポテンシャルの差に等しい（勾配定理）。物理では :math:`\bm{F} = -\nabla U` と負号を付ける。
* 保存場なら回転は :math:`\bm{0}` である。逆は、領域が単連結なら成り立つ。
