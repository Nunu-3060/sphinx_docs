.. _ch03:

第 3 章 ベクトル値関数と曲線
============================

この章では、1 つの変数 :math:`t` に応じてベクトルが決まる関数（ベクトル値関数）の微分と積分を扱う。ベクトル値関数を使うと、空間の曲線や物体の運動を表せる。曲線の速度と加速度、長さ（弧長）、曲がり具合（曲率）を順に説明する。ここで学ぶ曲線の扱いは、:ref:`第 11 章 <ch11>`\ の線積分の土台になる。

ベクトル値関数
--------------

実数 :math:`t` を 1 つ決めるとベクトル :math:`\bm{r}(t)` が 1 つ決まる関数を\ :term:`ベクトル値関数`\ という。成分で書くと、3 つの実数値関数の組

.. math::

   \bm{r}(t) = (x(t), \ y(t), \ z(t)) = x(t) \, \bm{e}_x + y(t) \, \bm{e}_y + z(t) \, \bm{e}_z

である。:math:`\bm{r}(t)` を位置ベクトルとみなし、:math:`t` を動かしたときの終点の軌跡を考えると、空間の曲線が得られる。:math:`t` を時刻と考えれば、:math:`\bm{r}(t)` は運動する物体の位置を表す。

微分
~~~~

ベクトル値関数の微分は、1 変数の関数と同じく

.. math::

   \frac{d\bm{r}}{dt} = \lim_{h \to 0} \frac{\bm{r}(t + h) - \bm{r}(t)}{h}

で定義する。基本単位ベクトル :math:`\bm{e}_x, \bm{e}_y, \bm{e}_z` は :math:`t` によらない定数なので、微分は成分ごとに計算すればよい。

.. math::

   \frac{d\bm{r}}{dt} = \left( \frac{dx}{dt}, \ \frac{dy}{dt}, \ \frac{dz}{dt} \right)

本書では :math:`d\bm{r}/dt` を :math:`\bm{r}'(t)` とも書く。積の微分については、1 変数の関数と同じ形の公式が成り立つ（:math:`f` はスカラー値関数）。

.. math::

   \frac{d}{dt} (f \bm{a}) &= \frac{df}{dt} \bm{a} + f \frac{d\bm{a}}{dt} \\
   \frac{d}{dt} (\bm{a} \cdot \bm{b}) &= \frac{d\bm{a}}{dt} \cdot \bm{b} + \bm{a} \cdot \frac{d\bm{b}}{dt} \\
   \frac{d}{dt} (\bm{a} \times \bm{b}) &= \frac{d\bm{a}}{dt} \times \bm{b} + \bm{a} \times \frac{d\bm{b}}{dt}

外積は順序を入れ替えると符号が変わるので、3 つ目の式では :math:`\bm{a}` と :math:`\bm{b}` の順序を保つ必要がある。

2 つ目の式から、次の有用な事実が分かる。:math:`|\bm{a}(t)|` が一定なら、:math:`\bm{a} \cdot \bm{a} = |\bm{a}|^2` を微分して

.. math::

   2 \, \bm{a} \cdot \frac{d\bm{a}}{dt} = 0

となる。つまり、長さが変わらないベクトルの導関数は、元のベクトルに垂直である。円周上を動く点の速度が半径に垂直であることや、後で説明する単位接線ベクトルの導関数が接線に垂直であることは、この事実から分かる。

積分
~~~~

積分も成分ごとに定義する。

.. math::

   \int_a^b \bm{r}(t) \, dt = \left( \int_a^b x(t) \, dt, \ \int_a^b y(t) \, dt, \ \int_a^b z(t) \, dt \right)

たとえば、加速度 :math:`\bm{a}(t)` を積分すると速度の変化が、速度を積分すると位置の変化が求められる。

曲線のパラメーター表示
----------------------

ベクトル値関数 :math:`\bm{r}(t)`\ （:math:`a \le t \le b`）で曲線を表すことを、曲線のパラメーター表示といい、:math:`t` をパラメーターという。代表的な例を挙げる。

.. list-table:: 曲線のパラメーター表示の例
   :header-rows: 1
   :widths: 25 45 30

   * - 曲線
     - パラメーター表示
     - 説明
   * - 直線
     - :math:`\bm{r}(t) = \bm{r}_0 + t \, \bm{d}`
     - 点 :math:`\bm{r}_0` を通り、方向 :math:`\bm{d}` に進む
   * - 円
     - :math:`\bm{r}(t) = (R \cos t, \ R \sin t, \ 0)`, :math:`0 \le t \le 2\pi`
     - 原点を中心とする半径 :math:`R` の円（反時計回り）
   * - らせん
     - :math:`\bm{r}(t) = (a \cos t, \ a \sin t, \ b t)`
     - 半径 :math:`a` の円柱に巻き付き、1 周で :math:`2\pi b` だけ上がる
   * - 関数のグラフ
     - :math:`\bm{r}(t) = (t, \ f(t), \ 0)`
     - 平面の曲線 :math:`y = f(x)`

パラメーター表示は 1 通りではない。たとえば :math:`(R \cos 2t, R \sin 2t, 0)`\ （:math:`0 \le t \le \pi`）も同じ円を表すが、2 倍の速さでたどる。:math:`(R \cos t, -R \sin t, 0)` は同じ円を時計回りにたどる。このように、パラメーター表示は曲線の形だけでなく、たどる向きと速さも決める。曲線のたどる向きを曲線の\ :term:`向き`\ といい、線積分（:ref:`第 11 章 <ch11>`）では向きによって結果の符号が変わる。

速度と加速度
------------

:math:`\bm{r}(t)` を時刻 :math:`t` における物体の位置とすると、

.. math::

   \bm{v}(t) = \frac{d\bm{r}}{dt}, \qquad \bm{a}(t) = \frac{d\bm{v}}{dt} = \frac{d^2\bm{r}}{dt^2}

をそれぞれ速度、加速度という。速度の大きさ :math:`|\bm{v}|` を速さという。

速度 :math:`\bm{r}'(t)` は、曲線の接線の方向を向いている。:math:`\bm{r}(t + h) - \bm{r}(t)` は曲線上の 2 点を結ぶ弦であり、:math:`h \to 0` の極限で接線の方向になるからである。そのため、:math:`\bm{r}'(t)` を\ :term:`接線ベクトル`\ ともいう。:math:`\bm{r}'(t) \ne \bm{0}` のとき、接線ベクトルを正規化した

.. math::

   \bm{T} = \frac{\bm{r}'(t)}{|\bm{r}'(t)|}

を\ :term:`単位接線ベクトル`\ という。

例：等速円運動
~~~~~~~~~~~~~~

半径 :math:`R` の円周上を、一定の角速度 :math:`\omega` で回る点の位置は

.. math::

   \bm{r}(t) = (R \cos \omega t, \ R \sin \omega t)

である。微分すると

.. math::

   \bm{v}(t) &= (-R \omega \sin \omega t, \ R \omega \cos \omega t) \\
   \bm{a}(t) &= (-R \omega^2 \cos \omega t, \ -R \omega^2 \sin \omega t) = -\omega^2 \bm{r}(t)

となる。速さは :math:`|\bm{v}| = R \omega` で一定であり、速度は半径に垂直（:math:`\bm{r} \cdot \bm{v} = 0`）である。加速度は円の中心を向き、大きさは :math:`R \omega^2 = |\bm{v}|^2 / R` である（:numref:`fig-ch03-circular-motion`）。速さが一定でも、向きが変わり続けるので加速度は 0 でない。質量 :math:`m` の物体を円運動させるには、中心向きの力（向心力）\ :math:`m |\bm{v}|^2 / R` が必要になる。

.. figure:: ../build/figures/ch03_circular_motion.svg
   :name: fig-ch03-circular-motion
   :width: 55%
   :align: center

   等速円運動の速度と加速度

サンプルの全体：:download:`ch03_circular_motion.py <../examples/ch03_circular_motion.py>`

例：投射運動
~~~~~~~~~~~~

原点から、水平に対して角度 :math:`\alpha` の向きに初速 :math:`v_0` で投げた物体の位置は、空気抵抗を無視すると（:math:`g` は重力加速度）

.. math::

   \bm{r}(t) = \left( v_0 \cos \alpha \, t, \ v_0 \sin \alpha \, t - \frac{1}{2} g t^2 \right)

である。微分すると、:math:`\bm{v}(t) = (v_0 \cos \alpha, \ v_0 \sin \alpha - g t)`、:math:`\bm{a}(t) = (0, -g)` となる。加速度は一定で真下を向き、速度の水平成分は変わらない。逆に、:math:`\bm{a} = (0, -g)` を初期条件 :math:`\bm{v}(0) = (v_0 \cos \alpha, v_0 \sin \alpha)`、:math:`\bm{r}(0) = \bm{0}` のもとで 2 回積分すると、上の :math:`\bm{r}(t)` が得られる。

弧長
----

曲線の長さを求めるには、曲線を細かく分けて、各部分を線分で近似すればよい。パラメーターが :math:`t` から :math:`t + dt` まで変わる間に点が動く距離は、およそ :math:`|\bm{r}'(t)| \, dt` である。これを足し合わせると、:math:`t = a` から :math:`t = b` までの曲線の長さ

.. math::

   L = \int_a^b |\bm{r}'(t)| \, dt = \int_a^b \sqrt{\left( \frac{dx}{dt} \right)^2 + \left( \frac{dy}{dt} \right)^2 + \left( \frac{dz}{dt} \right)^2} \, dt

が得られる。これを\ :term:`弧長`\ という。物体の運動で言えば、速さを時間で積分すると道のりになるということである。弧長の微小な部分

.. math::

   ds = |\bm{r}'(t)| \, dt = \sqrt{dx^2 + dy^2 + dz^2}

を\ :term:`線素`\ という。:math:`ds` は、:math:`x, y, z` 方向の微小な変化 :math:`dx, dy, dz` を 3 辺とする直方体の対角線の長さ（三平方の定理）である。線素は\ :ref:`第 9 章 <ch09>`\ の曲線座標系や、:ref:`第 11 章 <ch11>`\ の線積分で重要な役割を果たす。

弧長はパラメーター表示の選び方によらない。同じ曲線を 2 倍の速さでたどれば、:math:`|\bm{r}'|` は 2 倍になるが、かかる時間は半分になるからである。

弧長パラメーター
~~~~~~~~~~~~~~~~

始点からの弧長

.. math::

   s(t) = \int_a^t |\bm{r}'(u)| \, du

をパラメーターに使うと、曲線を「速さ 1」でたどる表示が得られる。これを弧長パラメーター表示という。:math:`ds/dt = |\bm{r}'(t)|` なので、連鎖律から

.. math::

   \frac{d\bm{r}}{ds} = \frac{d\bm{r}}{dt} \frac{dt}{ds} = \frac{\bm{r}'(t)}{|\bm{r}'(t)|} = \bm{T}

となる。つまり、弧長で微分すると単位接線ベクトルになる。弧長パラメーターは、曲線の形だけで決まる量（次に説明する曲率など）を定義するのに便利である。ただし、具体的な曲線で :math:`s(t)` を :math:`t` について解ける場合は少ないので、計算では元のパラメーター :math:`t` を使い、連鎖律で :math:`s` による微分に直すことが多い。

例：らせんの弧長
~~~~~~~~~~~~~~~~

らせん :math:`\bm{r}(t) = (a \cos t, \ a \sin t, \ b t)` では、:math:`\bm{r}'(t) = (-a \sin t, \ a \cos t, \ b)` なので :math:`|\bm{r}'(t)| = \sqrt{a^2 + b^2}` で一定である。したがって、1 周分（:math:`0 \le t \le 2\pi`）の弧長は :math:`2\pi \sqrt{a^2 + b^2}` である。円柱の側面を切り開くと、らせんは直角を挟む 2 辺が :math:`2\pi a` と :math:`2\pi b` の直角三角形の斜辺になることからも確かめられる。

曲率
----

曲率の定義
~~~~~~~~~~

曲線の曲がり具合は、単位接線ベクトル :math:`\bm{T}` の向きが変わる速さで測れる。ただし、同じ曲線でも速くたどれば :math:`\bm{T}` は速く変わるので、たどる速さの影響を除くため、弧長 :math:`s` で微分する。

.. math::

   \kappa = \left| \frac{d\bm{T}}{ds} \right|

を\ :term:`曲率`\ （curvature）という。:math:`1 / \kappa` を曲率半径という。直線は :math:`\bm{T}` が変わらないので曲率 0 である。半径 :math:`R` の円では、:math:`\bm{T}` は 1 周（弧長 :math:`2\pi R`）で 1 回転（角度 :math:`2\pi`）するので :math:`\kappa = 1/R` であり、曲率半径は円の半径に一致する。一般の曲線の曲率半径は、その点で曲線に最もよく接する円（接触円）の半径である。

:math:`|\bm{T}| = 1` は一定なので、:math:`d\bm{T}/ds` は :math:`\bm{T}` に垂直である。:math:`\kappa \ne 0` のとき、その向きの単位ベクトル

.. math::

   \bm{N} = \frac{1}{\kappa} \frac{d\bm{T}}{ds}

を（主）\ :term:`単位法線ベクトル`\ という。:math:`\bm{N}` は曲線が曲がっていく側（接触円の中心の方向）を向く。

曲率の計算
~~~~~~~~~~

元のパラメーター :math:`t` で計算するには、次の公式が便利である。

.. math::
   :label: eq-ch03-curvature

   \kappa = \frac{|\bm{r}'(t) \times \bm{r}''(t)|}{|\bm{r}'(t)|^3}

この式は、次に説明する加速度の分解から導ける。平面の曲線 :math:`y = f(x)` の場合は、:math:`\bm{r}(t) = (t, f(t), 0)` として :eq:`eq-ch03-curvature` に代入すると

.. math::

   \kappa = \frac{|f''(x)|}{\left( 1 + f'(x)^2 \right)^{3/2}}

となる。傾きが小さい（:math:`|f'| \ll 1`）ところでは、曲率はほぼ :math:`|f''|` に等しい。梁のたわみの計算では、この近似がよく使われる。

加速度の接線成分と法線成分
~~~~~~~~~~~~~~~~~~~~~~~~~~

速度を「速さ × 向き」として :math:`\bm{v} = |\bm{v}| \, \bm{T}` と書き、時刻で微分する。積の微分と連鎖律 :math:`d\bm{T}/dt = (d\bm{T}/ds)(ds/dt) = \kappa |\bm{v}| \bm{N}` を使うと

.. math::
   :label: eq-ch03-acceleration

   \bm{a} = \frac{d|\bm{v}|}{dt} \, \bm{T} + \kappa |\bm{v}|^2 \, \bm{N}

が得られる。加速度は、速さを変える接線方向の成分と、向きを変える法線方向の成分に分けられる。法線方向の成分 :math:`\kappa |\bm{v}|^2 = |\bm{v}|^2 / (\text{曲率半径})` は、等速円運動で求めた向心加速度と同じ形である。

:eq:`eq-ch03-acceleration` と :math:`\bm{v} = |\bm{v}| \bm{T}` の外積を取ると、:math:`\bm{T} \times \bm{T} = \bm{0}` より :math:`\bm{v} \times \bm{a} = \kappa |\bm{v}|^3 \, \bm{T} \times \bm{N}` となる。:math:`\bm{T} \times \bm{N}` は単位ベクトルなので、大きさを比べると :eq:`eq-ch03-curvature` が得られる。

たとえば、投射運動の最高点では、速度は水平で大きさ :math:`v_0 \cos \alpha`、加速度は真下向きで大きさ :math:`g` であり、加速度はすべて法線方向の成分になる。したがって、最高点での曲率は :math:`\kappa = g / (v_0 \cos \alpha)^2` である。

道路や鉄道の設計では、:eq:`eq-ch03-acceleration` の法線成分が乗り物の横方向の加速度（乗っている人には遠心力として感じられる）になる。直線から急に円に入ると曲率が不連続に変わり、横方向の加速度が急に生じる。そのため、曲率が弧長に比例して少しずつ増える緩和曲線（クロソイド曲線）を間に挟む。

フレネ・セレの公式
~~~~~~~~~~~~~~~~~~

3 次元の曲線では、:math:`\bm{T}` と :math:`\bm{N}` に加えて、両方に垂直な単位ベクトル :math:`\bm{B} = \bm{T} \times \bm{N}`\ （従法線ベクトル）を考える。:math:`\bm{T}, \bm{N}, \bm{B}` は曲線とともに動く右手系の正規直交基底になり、その変化は次の\ :term:`フレネ・セレの公式`\ で表される。

.. math::

   \frac{d\bm{T}}{ds} = \kappa \bm{N}, \qquad
   \frac{d\bm{N}}{ds} = -\kappa \bm{T} + \tau \bm{B}, \qquad
   \frac{d\bm{B}}{ds} = -\tau \bm{N}

:math:`\tau` は、曲線が平面からねじれて出ていく度合いを表す量で、ねじれ率（捩率）という。平面の曲線では :math:`\tau = 0` である。曲率とねじれ率が弧長の関数として与えられると、曲線の形は（位置と向きを除いて）一通りに決まる。本書ではこれ以上は扱わないが、CG のカメラの経路や、管・ケーブルの形状の生成などで使われる。

例：らせんの曲率
~~~~~~~~~~~~~~~~

らせん :math:`\bm{r}(t) = (a \cos t, \ a \sin t, \ b t)` について、:math:`\bm{r}'(t) = (-a \sin t, \ a \cos t, \ b)`、:math:`\bm{r}''(t) = (-a \cos t, \ -a \sin t, \ 0)` である。外積は :math:`\bm{r}' \times \bm{r}'' = (ab \sin t, \ -ab \cos t, \ a^2)` で、その大きさは :math:`a \sqrt{a^2 + b^2}` なので、:eq:`eq-ch03-curvature` から

.. math::

   \kappa = \frac{a \sqrt{a^2 + b^2}}{(a^2 + b^2)^{3/2}} = \frac{a}{a^2 + b^2}

となり、曲率は一定である。:math:`b = 0` なら半径 :math:`a` の円の曲率 :math:`1/a` に一致する。:math:`\bm{N} = (-\cos t, \ -\sin t, \ 0)` は、:math:`z` 軸に向かう水平な向きである（:numref:`fig-ch03-helix`）。ねじれ率は :math:`\tau = b / (a^2 + b^2)` になる。

.. figure:: ../build/figures/ch03_helix.svg
   :name: fig-ch03-helix
   :width: 55%
   :align: center

   らせんの単位接線ベクトルと単位法線ベクトル

サンプルの全体：:download:`ch03_helix.py <../examples/ch03_helix.py>`

SymPy と数値計算による確認
--------------------------

らせんの速さと曲率を SymPy で記号的に求め、:math:`a = 1`、:math:`b = 0.25` のときの弧長と曲率を数値計算と比べる。弧長の数値積分には SciPy の ``integrate.quad`` を使う。

.. literalinclude:: ../examples/ch03_curve_quantities.py
   :pyobject: report
   :lineno-match:
   :caption: ch03_curve_quantities.py の report()

サンプルの全体：:download:`ch03_curve_quantities.py <../examples/ch03_curve_quantities.py>`

.. literalinclude:: ../build/outputs/ch03_curve_quantities.txt
   :language: text
   :caption: ch03_curve_quantities.py の実行結果

SymPy の ``Matrix`` で位置ベクトルを表し、``diff`` で成分ごとに微分している。記号 :math:`a, b` を正（``positive=True``）と宣言しておくと、:math:`\sqrt{a^2}` が :math:`a` に簡単化される。得られた :math:`|\bm{r}'| = \sqrt{a^2 + b^2}`、:math:`\kappa = a/(a^2 + b^2)` は手計算の結果と一致し、数値計算の値も式の値と一致している。

この章のまとめ
--------------

* ベクトル値関数 :math:`\bm{r}(t)` は曲線や運動を表す。微分と積分は成分ごとに計算する。長さが一定のベクトルの導関数は、元のベクトルに垂直である。
* 速度 :math:`\bm{v} = \bm{r}'(t)` は曲線の接線の方向を向く。正規化したものが単位接線ベクトル :math:`\bm{T}` である。
* 弧長は :math:`L = \int_a^b |\bm{r}'(t)| \, dt` で求められ、パラメーター表示の選び方によらない。線素は :math:`ds = |\bm{r}'(t)| \, dt` である。
* 曲率 :math:`\kappa = |d\bm{T}/ds|` は曲がり具合を表し、:math:`\kappa = |\bm{r}' \times \bm{r}''| / |\bm{r}'|^3` で計算できる。半径 :math:`R` の円の曲率は :math:`1/R` である。
* 加速度は、速さを変える接線成分と、向きを変える法線成分 :math:`\kappa |\bm{v}|^2` に分けられる。
