.. _ch17:

第 17 章 物理への応用
======================

ここまでに学んだ勾配・発散・回転と積分定理は、物理の基本法則を書き表すための言葉である。この章では、電磁気学、流体力学、熱伝導の 3 つの分野で、法則がベクトル解析でどのように表され、どのように扱われるかを見る。最後に、3 つの分野に共通する構造をまとめる。

電磁気学
--------

マクスウェル方程式
~~~~~~~~~~~~~~~~~~

電場 :math:`\bm{E}` と磁束密度 :math:`\bm{B}` のふるまいは、4 つの式からなる\ :term:`マクスウェル方程式`\ で決まる。ここでは真空中（物質の分極や磁化を考えない場合）の形を示す。電荷密度を :math:`\rho`、電流密度を :math:`\bm{J}`、真空の誘電率を :math:`\varepsilon_0`、真空の透磁率を :math:`\mu_0` とする。

.. math::

   \nabla \cdot \bm{E} &= \frac{\rho}{\varepsilon_0} \\
   \nabla \cdot \bm{B} &= 0 \\
   \nabla \times \bm{E} &= -\frac{\partial \bm{B}}{\partial t} \\
   \nabla \times \bm{B} &= \mu_0 \bm{J} + \mu_0 \varepsilon_0 \frac{\partial \bm{E}}{\partial t}

これらは微分形と呼ばれる形で、空間の各点で成り立つ関係を表す。一方、電磁気学の法則は歴史的には、閉曲面を貫く流束や閉曲線に沿った循環の関係（積分形）として見いだされた。両者は、:ref:`第 14 章 <ch14>`\ のガウスの発散定理と\ :ref:`第 15 章 <ch15>`\ のストークスの定理で互いに書き換えられる。:numref:`table-ch17-maxwell` に対応をまとめる。積分形の :math:`V` は閉曲面 :math:`\partial V` で囲まれた立体、:math:`Q` は :math:`V` の中の電荷、:math:`S` は閉曲線 :math:`\partial S` を境界とする曲面、:math:`I` は :math:`S` を貫く電流である。

.. list-table:: マクスウェル方程式の積分形と微分形
   :name: table-ch17-maxwell
   :header-rows: 1
   :widths: 18 34 26 22

   * - 法則
     - 積分形
     - 微分形
     - 書き換えに使う定理
   * - ガウスの法則
     - :math:`\displaystyle \iint_{\partial V} \bm{E} \cdot d\bm{S} = \frac{Q}{\varepsilon_0}`
     - :math:`\nabla \cdot \bm{E} = \rho / \varepsilon_0`
     - ガウスの発散定理
   * - 磁束の保存
     - :math:`\displaystyle \iint_{\partial V} \bm{B} \cdot d\bm{S} = 0`
     - :math:`\nabla \cdot \bm{B} = 0`
     - ガウスの発散定理
   * - ファラデーの電磁誘導の法則
     - :math:`\displaystyle \oint_{\partial S} \bm{E} \cdot d\bm{r} = -\frac{d}{dt} \iint_S \bm{B} \cdot d\bm{S}`
     - :math:`\nabla \times \bm{E} = -\partial \bm{B} / \partial t`
     - ストークスの定理
   * - アンペール・マクスウェルの法則
     - :math:`\displaystyle \oint_{\partial S} \bm{B} \cdot d\bm{r} = \mu_0 I + \mu_0 \varepsilon_0 \frac{d}{dt} \iint_S \bm{E} \cdot d\bm{S}`
     - :math:`\nabla \times \bm{B} = \mu_0 \bm{J} + \mu_0 \varepsilon_0 \partial \bm{E} / \partial t`
     - ストークスの定理

ガウスの法則は\ :ref:`第 14 章 <ch14>`\ で、アンペールの法則とファラデーの法則は\ :ref:`第 15 章 <ch15>`\ で、積分形から微分形に書き換えた。磁束の保存（:math:`\nabla \cdot \bm{B} = 0`）も、ガウスの法則と同じくガウスの発散定理で書き換えられる。

電荷の保存と変位電流
~~~~~~~~~~~~~~~~~~~~

アンペール・マクスウェルの法則の右辺の第 2 項 :math:`\mu_0 \varepsilon_0 \partial \bm{E} / \partial t` は\ :term:`変位電流`\ の項と呼ばれ、マクスウェルが付け加えた。この項が必要な理由は、:ref:`第 8 章 <ch08>`\ の公式 :math:`\nabla \cdot (\nabla \times \bm{B}) = 0` から分かる。アンペール・マクスウェルの法則の両辺の発散をとると、左辺は 0 になるので

.. math::

   0 = \mu_0 \nabla \cdot \bm{J} + \mu_0 \varepsilon_0 \frac{\partial}{\partial t} (\nabla \cdot \bm{E}) = \mu_0 \left( \nabla \cdot \bm{J} + \frac{\partial \rho}{\partial t} \right)

となる。最後の変形にはガウスの法則 :math:`\varepsilon_0 \nabla \cdot \bm{E} = \rho` を使った。こうして得られる :math:`\nabla \cdot \bm{J} + \partial \rho / \partial t = 0` は電荷の保存を表す連続の式であり、:ref:`第 14 章 <ch14>`\ で示した電荷の保存則に一致する。変位電流の項がなければ :math:`\nabla \cdot \bm{J} = 0` となり、コンデンサーの充電のように電荷がたまっていく現象と矛盾する。

電位とベクトルポテンシャル
~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\nabla \cdot \bm{B} = 0` なので、:ref:`第 16 章 <ch16>`\ で見たように :math:`\bm{B} = \nabla \times \bm{A}` となるベクトルポテンシャル :math:`\bm{A}` が存在する。これをファラデーの法則に代入すると :math:`\nabla \times (\bm{E} + \partial \bm{A} / \partial t) = \bm{0}` となるので、括弧の中は回転が 0 の場であり、スカラーポテンシャルの勾配で書ける。物理の慣習に従って負号を付けると

.. math::

   \bm{E} = -\nabla V - \frac{\partial \bm{A}}{\partial t}

となる。:math:`V` は電位である。時間変化のない静電場では :math:`\bm{E} = -\nabla V` であり、ガウスの法則に代入すると、:ref:`第 16 章 <ch16>`\ のポアソン方程式

.. math::

   \nabla^2 V = -\frac{\rho}{\varepsilon_0}

が得られる。電荷のない領域ではラプラス方程式 :math:`\nabla^2 V = 0` になる。

電磁波
~~~~~~

電荷も電流もない真空（:math:`\rho = 0`、:math:`\bm{J} = \bm{0}`）では、マクスウェル方程式から電場だけの式を導ける。ファラデーの法則の両辺の回転をとり、:ref:`第 8 章 <ch08>`\ の公式 :math:`\nabla \times (\nabla \times \bm{E}) = \nabla (\nabla \cdot \bm{E}) - \nabla^2 \bm{E}` を使う。:math:`\nabla \cdot \bm{E} = 0` なので左辺は :math:`-\nabla^2 \bm{E}` である。右辺は、時間と空間の微分の順序を入れ替えてアンペール・マクスウェルの法則を使うと

.. math::

   \nabla \times \left( -\frac{\partial \bm{B}}{\partial t} \right) = -\frac{\partial}{\partial t} (\nabla \times \bm{B}) = -\mu_0 \varepsilon_0 \frac{\partial^2 \bm{E}}{\partial t^2}

となる。両辺を比べると

.. math::
   :label: eq-ch17-wave

   \nabla^2 \bm{E} = \mu_0 \varepsilon_0 \frac{\partial^2 \bm{E}}{\partial t^2}

が得られる。これは、速さ :math:`c = 1 / \sqrt{\mu_0 \varepsilon_0}` で伝わる波を表す\ :term:`波動方程式`\ である。:math:`\varepsilon_0` と :math:`\mu_0` の値を代入すると :math:`c \approx 3.00 \times 10^8 \ \mathrm{m/s}` となり、光の速さに一致する。マクスウェルはこの一致から、光が電磁波であると考えた。:math:`\bm{B}` についても同じ形の式が成り立つ。

:eq:`eq-ch17-wave` の解の例として、:math:`z` 軸の正の向きに進む平面波

.. math::

   \bm{E} = E_0 \sin(kz - \omega t) \, \bm{e}_x, \qquad \bm{B} = \frac{E_0}{c} \sin(kz - \omega t) \, \bm{e}_y, \qquad \omega = ck

がある。:math:`k` は波数、:math:`\omega` は角周波数である。電場と磁場は互いに直交し、どちらも進行方向に直交している。この波がマクスウェル方程式の 4 つの式をすべて満たすことを、SymPy で確かめる。

.. literalinclude:: ../examples/ch17_em_wave.py
   :pyobject: report
   :lineno-match:
   :caption: ch17_em_wave.py の report()

.. literalinclude:: ../build/outputs/ch17_em_wave.txt
   :language: text
   :caption: ch17_em_wave.py の実行結果

どの式も「左辺 - 右辺」が 0 になり、平面波がマクスウェル方程式の解であることが分かる。発散と回転を求める関数 ``div()`` と ``curl()`` は、定義どおりに偏微分を組み合わせたものである。

サンプルの全体：:download:`ch17_em_wave.py <../examples/ch17_em_wave.py>`

流体力学
--------

流体の運動は、各点での流れの速度 :math:`\bm{v}(\bm{r}, t)` というベクトル場で表す。この節では :math:`\rho` は流体の密度を表す（電磁気学の節の電荷密度とは別のものである）。

連続の式と非圧縮性
~~~~~~~~~~~~~~~~~~

質量の保存は、:ref:`第 14 章 <ch14>`\ で導いた連続の式 :math:`\partial \rho / \partial t + \nabla \cdot (\rho \bm{v}) = 0` で表される。水のように密度がほとんど変わらない流体では、連続の式は非圧縮性の条件 :math:`\nabla \cdot \bm{v} = 0` になり、流れの中のどの点にも湧き出しや吸い込みがない。

渦度
~~~~

速度の場の回転 :math:`\bm{\omega} = \nabla \times \bm{v}` が渦度である。:ref:`第 7 章 <ch07>`\ で見たように、角速度 :math:`\bm{\Omega}` で回る剛体回転の渦度は :math:`2 \bm{\Omega}` であり、渦度は流体の微小な部分がその場で回転する角速度の 2 倍を表す。渦度が至るところで 0 の流れを渦なしの流れという。

:ref:`第 15 章 <ch15>`\ で触れたケルビンの循環定理によれば、保存力だけを受ける完全流体（粘性のない流体）では、流体とともに動く閉曲線に沿った循環は時間がたっても変わらない。そのため、静止した状態や一様な流れから始まった完全流体の流れは、渦なしのまま保たれる。

ポテンシャル流
~~~~~~~~~~~~~~

渦なしの流れは、領域が単連結であれば、:ref:`第 16 章 <ch16>`\ で見たようにスカラーポテンシャル :math:`\phi` の勾配で書ける。

.. math::

   \bm{v} = \nabla \phi

この :math:`\phi` を\ :term:`速度ポテンシャル`\ という（流体力学では負号を付けない）。さらに流れが非圧縮であれば :math:`\nabla \cdot \bm{v} = \nabla \cdot \nabla \phi = 0` なので、速度ポテンシャルはラプラス方程式

.. math::

   \nabla^2 \phi = 0

を満たす。このように渦なしで非圧縮の流れを\ :term:`ポテンシャル流`\ という。ラプラス方程式は線形なので、2 つの解を足したものも解になる。この性質を使うと、単純な流れを重ね合わせて複雑な流れを作れる。

例として、半径 :math:`a` の円柱を過ぎる 2 次元の流れを考える。遠くで :math:`x` 軸の正の向きに速さ :math:`v_\infty` で流れる一様流 :math:`\phi = v_\infty x` に、原点に置いた二重湧き出し（湧き出しと吸い込みを近づけた極限）を重ねると、2 次元の極座標 :math:`(r, \theta)` で

.. math::

   \phi = v_\infty \left( r + \frac{a^2}{r} \right) \cos\theta

となる。この :math:`\phi` は :math:`r > 0` でラプラス方程式を満たす。:ref:`第 9 章 <ch09>`\ の円柱座標の勾配の式で :math:`\rho` を :math:`r`、方位角 :math:`\phi` を :math:`\theta` に置き換えたもの（この :math:`\phi` は速度ポテンシャルとは別）を使うと、速度の成分は

.. math::

   v_r = \frac{\partial \phi}{\partial r} = v_\infty \left( 1 - \frac{a^2}{r^2} \right) \cos\theta, \qquad v_\theta = \frac{1}{r} \frac{\partial \phi}{\partial \theta} = -v_\infty \left( 1 + \frac{a^2}{r^2} \right) \sin\theta

である。円柱の表面 :math:`r = a` では :math:`v_r = 0` となり、流れは円柱の表面を貫かずに沿って進む。また :math:`r \to \infty` では :math:`\phi \to v_\infty x` となり、遠くでは一様流に戻る。表面での速さ :math:`|v_\theta| = 2 v_\infty |\sin\theta|` は、円柱の上下（:math:`\theta = \pm \pi / 2`）で最大値 :math:`2 v_\infty` をとる。:numref:`fig-ch17-potential-flow` は、この流れを直交座標の成分に直して流線で描いたものである。

.. figure:: ../build/figures/ch17_potential_flow.svg
   :name: fig-ch17-potential-flow
   :width: 85%
   :align: center

   円柱を過ぎるポテンシャル流

.. literalinclude:: ../examples/ch17_potential_flow.py
   :pyobject: velocity
   :lineno-match:
   :caption: ch17_potential_flow.py の velocity()

サンプルの全体：:download:`ch17_potential_flow.py <../examples/ch17_potential_flow.py>`

この流れは上下だけでなく前後（左右）にも対称なので、円柱の前面と背面の圧力がつり合い、円柱は流れから力を受けない。これは実際の流れとは異なる（ダランベールのパラドックス）。実際の流体には粘性があり、円柱の表面の近くの薄い層（境界層）で渦が生まれ、背後に渦の列ができる。ポテンシャル流は、境界層の外側の流れや翼のまわりの流れの近似として役立つ。

運動方程式の概要
~~~~~~~~~~~~~~~~

流体の運動方程式についても、概要だけを示しておく。完全流体の運動方程式（オイラー方程式）は、圧力を :math:`p`、単位質量あたりの外力を :math:`\bm{g}` として

.. math::

   \rho \left( \frac{\partial \bm{v}}{\partial t} + (\bm{v} \cdot \nabla) \bm{v} \right) = -\nabla p + \rho \bm{g}

と書ける。左辺の括弧の中は、流体とともに動く微小な部分の加速度である。:math:`(\bm{v} \cdot \nabla) \bm{v}` は、各成分に演算子 :math:`v_x \partial / \partial x + v_y \partial / \partial y + v_z \partial / \partial z` を作用させたもので、流れに乗って場所が変わることによる速度の変化を表す。右辺の :math:`-\nabla p` は、圧力の高い側から低い側へ押す力である。粘性を考えると、非圧縮の流れでは右辺に :math:`\mu \nabla^2 \bm{v}`\ （:math:`\mu` は粘性係数で、透磁率 :math:`\mu_0` とは別）が加わり、ナビエ・ストークス方程式になる。

:ref:`第 8 章 <ch08>`\ の公式から得られる恒等式 :math:`(\bm{v} \cdot \nabla) \bm{v} = \nabla (|\bm{v}|^2 / 2) - \bm{v} \times (\nabla \times \bm{v})` を使うと、オイラー方程式からベルヌーイの定理を導ける。時間変化のない、渦なしの、非圧縮の流れで、外力がない場合は、渦度が 0 なので

.. math::

   \nabla \left( p + \frac{1}{2} \rho |\bm{v}|^2 \right) = \bm{0}

となり、:math:`p + \rho |\bm{v}|^2 / 2` は流れの中のどこでも等しい。速く流れる場所ほど圧力が低い。

熱伝導
------

フーリエの法則
~~~~~~~~~~~~~~

物体の中の温度を :math:`T(\bm{r}, t)` とする。熱は温度の高いところから低いところへ流れる。単位時間に単位面積を通る熱の量を表すベクトル場を熱流束 :math:`\bm{q}` とすると、多くの物質で\ :term:`フーリエの法則`

.. math::

   \bm{q} = -\lambda \nabla T

が成り立つ。:math:`\lambda` は熱伝導率である（:math:`k` と書く本も多い）。:ref:`第 5 章 <ch05>`\ で見たように、勾配は温度が最も急に上がる向きを指すので、負号を付けた :math:`-\nabla T` は温度が最も急に下がる向きであり、熱はその向きに流れる。

熱伝導方程式の導出
~~~~~~~~~~~~~~~~~~

物体の中に、動かない任意の領域 :math:`V` をとる。この節では :math:`\rho` は物体の密度、:math:`c` は比熱（単位質量の温度を 1 K 上げるのに必要な熱量）、:math:`Q` は単位体積・単位時間あたりの発熱量とする（電磁気学の節の電荷密度 :math:`\rho`、光の速さ :math:`c`、電荷 :math:`Q` とは別である）。:math:`V` の中の熱エネルギーの増え方は、表面 :math:`\partial V` から流れ込む熱と、内部での発熱の和に等しい。

.. math::

   \frac{d}{dt} \iiint_V c \rho T \, dV = -\iint_{\partial V} \bm{q} \cdot d\bm{S} + \iiint_V Q \, dV

右辺の第 1 項は、外向きの流束に負号を付けたものなので、流れ込む熱を表す。この項をガウスの発散定理で体積積分に直すと、すべての項が :math:`V` での体積積分になる。

.. math::

   \iiint_V \left( c \rho \frac{\partial T}{\partial t} + \nabla \cdot \bm{q} - Q \right) dV = 0

これがどのような :math:`V` でも成り立つので、被積分関数が各点で 0 になる。フーリエの法則を代入し、:math:`\lambda` が場所によらない定数であれば :math:`\nabla \cdot (-\lambda \nabla T) = -\lambda \nabla^2 T` なので

.. math::
   :label: eq-ch17-heat

   \frac{\partial T}{\partial t} = \alpha \nabla^2 T + \frac{Q}{c \rho}, \qquad \alpha = \frac{\lambda}{c \rho}

が得られる。これを\ :term:`熱伝導方程式`\ という。:math:`\alpha` は温度拡散率と呼ばれる。「積分形の保存則をガウスの発散定理で微分形に直す」という手順は、:ref:`第 14 章 <ch14>`\ で連続の式を導いたときと同じである。

ラプラシアンの意味
~~~~~~~~~~~~~~~~~~

:ref:`第 8 章 <ch08>`\ で見たように、:math:`\nabla^2 T` は、ある点の温度がまわりの平均よりどれだけ低いかに比例する。:eq:`eq-ch17-heat` は、発熱がなければ、まわりより冷たい点は温まり、まわりより熱い点は冷めることを表している。こうして温度の山や谷はならされていく。

1 次元の棒（長さ :math:`L`、両端の温度を 0 に保つ）では、:eq:`eq-ch17-heat` は :math:`\partial T / \partial t = \alpha \, \partial^2 T / \partial x^2` となり、

.. math::

   T(x, t) = \sin \frac{n \pi x}{L} \exp \left( -\alpha \left( \frac{n \pi}{L} \right)^2 t \right) \qquad (n = 1, 2, 3, \ldots)

がその解になる。実際に代入すると、両辺とも :math:`-\alpha (n\pi / L)^2 T` に等しい。方程式は線形なので、これらの和も解である。:numref:`fig-ch17-heat-decay` は、:math:`n = 1` と :math:`n = 3` の 2 つの解を重ねた温度分布が、時間とともに変わる様子を描いたものである。:math:`n = 3` の成分は :math:`n = 1` の成分の 9 倍の速さで減衰するので、細かい凸凹が先に消え、なだらかな山だけが残る。

.. figure:: ../build/figures/ch17_heat_decay.svg
   :name: fig-ch17-heat-decay
   :width: 75%
   :align: center

   熱伝導による温度分布の変化

.. literalinclude:: ../examples/ch17_heat_decay.py
   :pyobject: temperature
   :lineno-match:
   :caption: ch17_heat_decay.py の temperature()

サンプルの全体：:download:`ch17_heat_decay.py <../examples/ch17_heat_decay.py>`

定常状態
~~~~~~~~

十分に時間がたち、温度が変わらなくなった状態を定常状態という。:eq:`eq-ch17-heat` で :math:`\partial T / \partial t = 0` とおくと、発熱がない場合はラプラス方程式 :math:`\nabla^2 T = 0`、発熱がある場合はポアソン方程式 :math:`\nabla^2 T = -Q / \lambda` になる。境界の温度を与えて定常状態の温度分布を数値的に求める方法は、:ref:`第 18 章 <ch18>`\ で扱う。

3 つの分野に共通する構造
------------------------

ここまでの 3 つの分野には、共通する構造がある。

1. 閉曲面を通る流束と、内部にある量（電荷、質量、熱エネルギー）やその増減との関係を表す（積分形）。
2. ガウスの発散定理で、各点で成り立つ式（微分形）に直す。
3. 流束をポテンシャルの勾配で表す関係（:math:`\bm{E} = -\nabla V`、:math:`\bm{v} = \nabla \phi`、:math:`\bm{q} = -\lambda \nabla T`）と組み合わせると、ポアソン方程式やラプラス方程式が得られる。

.. graphviz::
   :name: fig-ch17-structure
   :caption: 積分形の法則からポアソン方程式・ラプラス方程式が得られる流れ
   :align: center

   digraph structure {
       graph [rankdir=LR, fontname="Yu Gothic", fontsize=11, nodesep=0.4];
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb", fontname="Yu Gothic", fontsize=11];
       edge [fontname="Yu Gothic", fontsize=10];
       integral [label="積分形の法則\n（閉曲面を通る流束）"];
       local [label="微分形\n∇·（流束）= 湧き出し"];
       law [label="流束とポテンシャル u の関係\n（流束 ∝ ∇u）", fillcolor="#fdf1e3"];
       poisson [label="ポアソン方程式\n∇²u = （湧き出しに比例する項）", fillcolor="#e8f5e9"];
       laplace [label="ラプラス方程式\n∇²u = 0", fillcolor="#e8f5e9"];
       integral -> local [label="ガウスの\n発散定理"];
       local -> poisson;
       law -> poisson;
       poisson -> laplace [label="湧き出しが\nない領域"];
   }

:numref:`table-ch17-common` に、各分野の量の対応をまとめる。式の形が同じなので、ある分野で得た解や解法を、別の分野の問題にそのまま使える。たとえば、一様な熱の流れの中に熱を通さない円柱を置いたときの定常な温度分布は、円柱を過ぎるポテンシャル流の速度ポテンシャルと同じ形の関数で表される。どちらもラプラス方程式を満たし、円柱の表面で法線方向の流束が 0 という同じ境界条件を持つからである。

.. list-table:: 各分野の対応
   :name: table-ch17-common
   :header-rows: 1
   :widths: 16 20 28 36

   * - 分野
     - ポテンシャル
     - 流束（ベクトル場）
     - 定常状態の方程式
   * - 静電場
     - 電位 :math:`V`
     - 電場 :math:`\bm{E} = -\nabla V`
     - :math:`\nabla^2 V = -\rho / \varepsilon_0`
   * - ポテンシャル流
     - 速度ポテンシャル :math:`\phi`
     - 速度 :math:`\bm{v} = \nabla \phi`
     - :math:`\nabla^2 \phi = 0`
   * - 熱伝導
     - 温度 :math:`T`
     - 熱流束 :math:`\bm{q} = -\lambda \nabla T`
     - :math:`\nabla^2 T = -Q / \lambda`
   * - 重力
     - 単位質量あたりの位置エネルギー（重力ポテンシャル）\ :math:`U`
     - 重力加速度 :math:`\bm{g} = -\nabla U`
     - :math:`\nabla^2 U = 4 \pi G \rho`

この章のまとめ
--------------

* マクスウェル方程式の積分形と微分形は、ガウスの発散定理とストークスの定理で互いに書き換えられる。
* :math:`\nabla \cdot (\nabla \times \bm{B}) = 0` から電荷の保存が、:math:`\nabla \times (\nabla \times \bm{E})` の公式から電磁波の波動方程式が導かれる。
* 流体の渦度は速度の回転である。渦なしで非圧縮の流れ（ポテンシャル流）の速度ポテンシャルはラプラス方程式を満たす。
* 熱伝導方程式は、エネルギーの収支にガウスの発散定理とフーリエの法則を組み合わせて導かれる。ラプラシアンは温度をならす働きを表す。
* 静電場、ポテンシャル流、熱伝導、重力は、いずれもポアソン方程式やラプラス方程式で表される共通の構造を持つ。
