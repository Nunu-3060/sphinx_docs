.. _ch16:

第 16 章 ポテンシャルとヘルムホルツ分解
========================================

回転が 0 の場は、あるスカラー場の勾配として書けるか。発散が 0 の場は、あるベクトル場の回転として書けるか。この章では、積分定理を使ってこれらの問いに答え、答えが場の定義される領域の形に左右されることを、自由渦の例で示す。さらに、一般のベクトル場が渦なしの成分と発散のない成分に分けられること（ヘルムホルツ分解）を紹介し、ポテンシャルが満たすポアソン方程式とラプラス方程式を説明する。

スカラーポテンシャル
--------------------

:ref:`第 11 章 <ch11>`\ で見たように、ベクトル場 :math:`\bm{F}` がスカラー場 :math:`\phi` の勾配として :math:`\bm{F} = \nabla \phi` と書けるとき、:math:`\phi` を :math:`\bm{F}` の\ :term:`スカラーポテンシャル`\ という。連続なベクトル場 :math:`\bm{F}` について、:ref:`第 11 章 <ch11>`\ で見た次の 3 条件は互いに同値である（領域は連結であるとする。番号は第 11 章と同じ）。

#. 線積分 :math:`\int_C \bm{F} \cdot d\bm{r}` は、曲線 :math:`C` の始点と終点だけで決まり、経路によらない。
#. 任意の閉曲線 :math:`C` について :math:`\oint_C \bm{F} \cdot d\bm{r} = 0` である。
#. :math:`\bm{F} = \nabla \phi` となるスカラー場 :math:`\phi` がある（:math:`\bm{F}` は保存場である）。

物理では、力 :math:`\bm{F} = -\nabla U` や電場 :math:`\bm{E} = -\nabla V` のように負号を付けたものをポテンシャル（位置エネルギー、電位）と呼ぶ習慣がある（:ref:`第 11 章 <ch11>`）。負号の違いは本質的ではないので、この章では数学の習慣に従い :math:`\bm{F} = \nabla \phi` と書く。

回転が 0 であることは必要条件
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:math:`\bm{F} = \nabla \phi` なら、:ref:`第 8 章 <ch08>`\ の公式 :math:`\nabla \times (\nabla \phi) = \bm{0}` から :math:`\nabla \times \bm{F} = \bm{0}` である。したがって、回転が 0 でない場はスカラーポテンシャルを持たない。:math:`\nabla \times \bm{F} = \bm{0}` は、保存場であるための必要条件であり、手軽に確かめられる判定法になる。

逆に、:math:`\nabla \times \bm{F} = \bm{0}` なら、必ずスカラーポテンシャルがあるのだろうか。ストークスの定理（:ref:`第 15 章 <ch15>`）を使って考える。領域内の任意の閉曲線 :math:`C` について、:math:`C` を境界とする曲面 :math:`S` が領域内に取れれば

.. math::

   \oint_C \bm{F} \cdot d\bm{r} = \iint_S (\nabla \times \bm{F}) \cdot d\bm{S} = 0

となり、上の条件 2 が満たされる。問題は「:math:`C` を境界とする曲面が、領域からはみ出さずに取れるか」である。

単連結な領域
~~~~~~~~~~~~

:ref:`第 11 章 <ch11>`\ で定義した単連結な領域（任意の閉曲線を、領域からはみ出さずに連続的に縮めて 1 点にできる領域）の例を挙げる。

* 空間全体、球の内部、直方体の内部は単連結である。
* 空間から 1 点（たとえば原点）を除いた領域も単連結である。原点の周りを回る閉曲線は、原点を避けて縮められる。
* 空間から直線（たとえば :math:`z` 軸）を除いた領域は単連結でない。:math:`z` 軸の周りを 1 周する閉曲線は、:math:`z` 軸に引っかかって縮められない。
* 平面から 1 点を除いた領域も単連結でない。

単連結な領域では、閉曲線を縮めていく軌跡がその閉曲線を境界とする曲面になるので、上の議論が成り立つ。まとめると次のようになる。

* 単連結な領域で :math:`\nabla \times \bm{F} = \bm{0}` なら、:math:`\bm{F}` はスカラーポテンシャルを持つ。

ポテンシャルの求め方
~~~~~~~~~~~~~~~~~~~~

スカラーポテンシャルは、基準点 :math:`\bm{r}_0` から点 :math:`\bm{r}` までの線積分 :math:`\phi(\bm{r}) = \int_{\bm{r}_0}^{\bm{r}} \bm{F} \cdot d\bm{r}` で求められる。経路によらないので、計算しやすい経路を選べばよい。

領域が原点を含み、原点と領域内の各点を結ぶ線分が領域からはみ出さない場合（空間全体や球の内部など）は、原点から :math:`\bm{r}` までの線分 :math:`t \bm{r}`\ （:math:`0 \le t \le 1`）に沿って積分するのが簡単である。:math:`d(t\bm{r}) = \bm{r} \, dt` なので

.. math::
   :label: eq-ch16-scalar-potential

   \phi(\bm{r}) = \int_0^1 \bm{F}(t \bm{r}) \cdot \bm{r} \, dt

となる。ポテンシャルには定数を足す自由度があり、この式は :math:`\phi(\bm{0}) = 0` となるものを選んでいる。

たとえば :math:`\bm{F} = (2xy + z, \ x^2 + 3z, \ x + 3y)` は、回転を計算すると :math:`\bm{0}` になり、空間全体で定義されているので、スカラーポテンシャルを持つ。:eq:`eq-ch16-scalar-potential` を SymPy で計算する。

.. literalinclude:: ../examples/ch16_potential_sympy.py
   :pyobject: scalar_potential
   :lineno-match:
   :caption: ch16_potential_sympy.py の scalar_potential()

``at_tr()`` は、場の式の :math:`x, y, z` を :math:`tx, ty, tz` に置き換えて :math:`\bm{F}(t\bm{r})` を作る関数である。実行結果は後でベクトルポテンシャルの例とあわせて示す（:numref:`ch16-potential-output`）。:math:`\phi = x^2 y + xz + 3yz` が得られ、その勾配が :math:`\bm{F}` に一致する。

.. _ch16-vortex:

単連結でない領域の反例：自由渦
------------------------------

:ref:`第 7 章 <ch07>`\ で見たように、自由渦

.. math::

   \bm{F} = \frac{(-y, \ x)}{x^2 + y^2}

は原点以外で回転が 0 なのに、原点を囲む循環は :math:`2\pi` である（3 次元で考えるときは :math:`z` 成分を 0 とする）。この場は原点（3 次元では :math:`z` 軸）で定義されない。原点を中心とする半径 :math:`R` の円 :math:`(R\cos t, R\sin t)` に沿って反時計回りに 1 周すると、:math:`\oint_C \bm{F} \cdot d\bm{r} = \int_0^{2\pi} (R^2 \sin^2 t + R^2 \cos^2 t) / R^2 \, dt = 2\pi` となり、循環は半径 :math:`R` によらない。

回転が 0 なのに循環が 0 でないので、自由渦はスカラーポテンシャルを持たない。原因は、場の定義される領域（平面から原点を除いたもの）が単連結でないことにある。原点を囲む円を境界とする曲面（円板）は、必ず原点を含んでしまうので、ストークスの定理（グリーンの定理）が使えない。

.. figure:: ../build/figures/ch16_vortex.svg
   :name: fig-ch16-vortex
   :width: 60%
   :align: center

   自由渦の流線と、原点を囲む閉曲線 :math:`C_1`・囲まない閉曲線 :math:`C_2`

いろいろな閉曲線で循環を数値積分した結果を示す。

.. literalinclude:: ../build/outputs/ch16_vortex.txt
   :language: text
   :caption: ch16_vortex.py の実行結果

原点を囲む閉曲線では、大きさや形によらず循環は :math:`2\pi` になり、原点を囲まない閉曲線では 0 になる。:ref:`第 13 章 <ch13>`\ の「穴のある領域」で見たように、回転が 0 の場では、穴（原点）を囲む閉曲線をどのように変形しても循環は変わらない。:ref:`第 14 章 <ch14>`\ の点電荷の場で、原点を囲む閉曲面の流束が形によらず :math:`4\pi` だったことと同じ構造である。

サンプルの全体：:download:`ch16_vortex.py <../examples/ch16_vortex.py>`

局所的なポテンシャル
~~~~~~~~~~~~~~~~~~~~

自由渦は、極座標の角度 :math:`\theta` を使うと :math:`\bm{F} = \nabla \theta` と書ける。実際、:ref:`第 9 章 <ch09>`\ の円柱座標の勾配の式で :math:`\rho` を :math:`r`、:math:`\phi` を :math:`\theta` に置き換えたものから :math:`\nabla \theta = \frac{1}{r} \bm{e}_\theta = \frac{(-y, x)}{x^2 + y^2}` である。

それでもスカラーポテンシャルを持たないのは、:math:`\theta` が平面全体で 1 つの値に決まらないからである。原点の周りを 1 周すると :math:`\theta` は :math:`2\pi` 増え、元の点に戻っても元の値に戻らない。:math:`\theta` を 1 つの値に決めるには、たとえば :math:`x` 軸の負の部分で切れ目を入れて :math:`-\pi < \theta < \pi` とする必要がある。切れ目を入れた領域は単連結なので、その中では :math:`\theta` が正しいポテンシャルになる。

この場は、:ref:`第 15 章 <ch15>`\ の直線電流がつくる磁場 :math:`\bm{B} = \frac{\mu_0 I}{2\pi\rho} \bm{e}_\phi` と同じ形をしている。電流の外側では :math:`\nabla \times \bm{B} = \bm{0}` だが、電流を囲む閉曲線の循環は :math:`\mu_0 I` であり、0 にならない。流体力学では、竜巻や渦糸の外側の流れのモデルになる。

.. _ch16-vector-potential:

ベクトルポテンシャル
--------------------

ベクトル場 :math:`\bm{B}` が、あるベクトル場 :math:`\bm{A}` の回転として :math:`\bm{B} = \nabla \times \bm{A}` と書けるとき、:math:`\bm{A}` を :math:`\bm{B}` の\ :term:`ベクトルポテンシャル`\ という。:ref:`第 8 章 <ch08>`\ の公式 :math:`\nabla \cdot (\nabla \times \bm{A}) = 0` から、ベクトルポテンシャルを持つ場は発散が 0 である。

* :math:`\bm{B} = \nabla \times \bm{A}` なら :math:`\nabla \cdot \bm{B} = 0`

逆に、空間全体や球の内部のような領域（原点と各点を結ぶ線分が領域からはみ出さない領域）では、:math:`\nabla \cdot \bm{B} = 0` なら、次の式でベクトルポテンシャルが得られる。

.. math::
   :label: eq-ch16-vector-potential

   \bm{A}(\bm{r}) = \int_0^1 t \, \bm{B}(t \bm{r}) \times \bm{r} \, dt

一様な場 :math:`\bm{B}`\ （定ベクトル）では :math:`\bm{A} = \frac{1}{2} \bm{B} \times \bm{r}` となる。たとえば :math:`\bm{B} = (0, 0, B_0)` なら :math:`\bm{A} = \frac{B_0}{2} (-y, x, 0)` で、回転を計算すると確かに :math:`(0, 0, B_0)` になる。

.. literalinclude:: ../examples/ch16_potential_sympy.py
   :pyobject: vector_potential
   :lineno-match:
   :caption: ch16_potential_sympy.py の vector_potential()

:math:`\bm{B} = (y, z, x)` は発散が 0 なので、ベクトルポテンシャルを持つ。スカラーポテンシャルの例とあわせて、SymPy で求めた結果を示す。

.. literalinclude:: ../build/outputs/ch16_potential_sympy.txt
   :language: text
   :caption: ch16_potential_sympy.py の実行結果
   :name: ch16-potential-output

どちらのポテンシャルも、微分すると元の場に戻る（差が :math:`\bm{0}` になる）。

サンプルの全体：:download:`ch16_potential_sympy.py <../examples/ch16_potential_sympy.py>`

ゲージの自由度
~~~~~~~~~~~~~~

スカラーポテンシャルに定数を足しても勾配は変わらないように、ベクトルポテンシャルには任意のスカラー場 :math:`\chi` の勾配を足しても回転は変わらない。

.. math::

   \nabla \times (\bm{A} + \nabla \chi) = \nabla \times \bm{A} + \nabla \times (\nabla \chi) = \nabla \times \bm{A}

実行結果の最後の行は、:math:`\chi = xyz` の勾配を足しても回転が変わらないことを確かめたものである。この自由度を\ :term:`ゲージの自由度`\ という。電磁気学では、:math:`\chi` をうまく選んで :math:`\nabla \cdot \bm{A} = 0` となるようにすること（クーロンゲージ）が多い。

発散が 0 でもベクトルポテンシャルを持たない例
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スカラーポテンシャルと同じように、ベクトルポテンシャルの存在も領域の形に左右される。:ref:`第 14 章 <ch14>`\ の点電荷の場 :math:`\bm{F} = \bm{r} / r^3` は、原点以外で発散が 0 である。もし :math:`\bm{F} = \nabla \times \bm{A}` と書けたとすると、原点を中心とする球面 :math:`S` について、:math:`S` を赤道で上下 2 つの半球面に分けてストークスの定理を使うと

.. math::

   \iint_S \bm{F} \cdot d\bm{S} = \oint_{C} \bm{A} \cdot d\bm{r} + \oint_{C'} \bm{A} \cdot d\bm{r} = 0

となるはずである。ここで :math:`C` と :math:`C'` は同じ赤道を互いに逆向きにたどる閉曲線なので、和は 0 になる。ところが実際の流束は :math:`4\pi` なので、矛盾する。空間から原点を除いた領域は単連結だが、原点を囲む閉曲面を、領域からはみ出さずに縮めて 1 点にすることはできない。ベクトルポテンシャルの存在には、閉曲線ではなく閉曲面が縮められるかどうかが関係する。

.. _ch16-helmholtz:

ヘルムホルツ分解
----------------

ここまでで、2 種類の特別な場が分かった。

* 渦なしの場（:math:`\nabla \times \bm{F} = \bm{0}`）：スカラーポテンシャルの勾配 :math:`\nabla \phi` で書ける。
* 発散のない場（:math:`\nabla \cdot \bm{F} = 0`、ソレノイダルな場ともいう）：ベクトルポテンシャルの回転 :math:`\nabla \times \bm{A}` で書ける。

一般のベクトル場は、この 2 種類の和に分けられる。

.. math::
   :label: eq-ch16-helmholtz

   \bm{F} = \nabla \phi + \nabla \times \bm{A}

これを\ :term:`ヘルムホルツ分解`\ という。第 1 項は回転が 0、第 2 項は発散が 0 なので、両辺の発散と回転をとると

.. math::

   \nabla \cdot \bm{F} = \nabla^2 \phi, \qquad \nabla \times \bm{F} = \nabla \times (\nabla \times \bm{A})

となる。つまり、:math:`\bm{F}` の発散（湧き出し）が渦なしの成分を決め、:math:`\bm{F}` の回転（渦）が発散のない成分を決める。:numref:`fig-ch16-helmholtz` は、湧き出しのある渦なしの成分と、渦のある発散のない成分を足し合わせて、1 つの場を組み立てたものである。

.. figure:: ../build/figures/ch16_helmholtz.svg
   :name: fig-ch16-helmholtz
   :width: 100%
   :align: center

   渦なしの成分と発散のない成分を足し合わせた場

2 次元の場では、発散のない成分を :math:`\nabla \times (\psi \bm{e}_z) = (\partial \psi / \partial y, \ -\partial \psi / \partial x)` と書ける。:math:`\psi` は流体力学で\ :term:`流れ関数`\ と呼ばれる。図では :math:`\phi = -e^{-((x-1)^2 + y^2)}`、:math:`\psi = e^{-((x+1)^2 + y^2)}` とした。各成分の発散と回転を SymPy で確かめた結果を示す。

.. literalinclude:: ../build/outputs/ch16_helmholtz.txt
   :language: text
   :caption: ch16_helmholtz.py の実行結果

渦なしの成分は回転が 0、発散のない成分は発散が 0 であり、和の発散は :math:`\nabla^2 \phi`、和の回転は :math:`-\nabla^2 \psi` だけで決まっている。

サンプルの全体：:download:`ch16_helmholtz.py <../examples/ch16_helmholtz.py>`

分解の求め方と一意性
~~~~~~~~~~~~~~~~~~~~

空間全体で定義され、無限遠で十分速く 0 に近づく場 :math:`\bm{F}` では、:math:`\phi` と :math:`\bm{A}` を次の式で求められる。

.. math::

   \phi(\bm{r}) = -\frac{1}{4\pi} \iiint \frac{\nabla' \cdot \bm{F}(\bm{r}')}{|\bm{r} - \bm{r}'|} \, dV', \qquad
   \bm{A}(\bm{r}) = \frac{1}{4\pi} \iiint \frac{\nabla' \times \bm{F}(\bm{r}')}{|\bm{r} - \bm{r}'|} \, dV'

:math:`\nabla'` は :math:`\bm{r}'` についての微分を表す。これらの式は、次節のポアソン方程式の解の公式から導かれる。この場合、分解は一意である。発散も回転も 0 で、無限遠で 0 に近づく場は、恒等的に 0 の場しかないからである。

有界な領域では、発散と回転だけでは場は決まらず、境界での条件（境界を通る流束など）が必要になる。:ref:`第 18 章 <ch18>`\ で扱う流体シミュレーションの圧力投影は、速度場から渦なしの成分を取り除き、発散のない成分だけを残す操作であり、ヘルムホルツ分解の代表的な応用である。

.. _ch16-poisson:

ポアソン方程式とラプラス方程式
------------------------------

渦なしの場 :math:`\bm{F} = \nabla \phi` の発散（湧き出しの分布）\ :math:`s` が分かっているとき、:math:`\nabla \cdot \bm{F} = \nabla \cdot (\nabla \phi) = s` から、ポテンシャルは次の方程式を満たす。

.. math::

   \nabla^2 \phi = s

これを\ :term:`ポアソン方程式`\ という。特に湧き出しがない場合（:math:`s = 0`）の

.. math::

   \nabla^2 \phi = 0

をラプラス方程式という（その解が\ :ref:`第 8 章 <ch08>`\ で見た調和関数である）。工学では、たとえば次のような場面で現れる。表の :math:`\rho` は電荷密度または質量密度であり、円柱座標の :math:`\rho` とは別である。

.. list-table:: ポアソン方程式とラプラス方程式が現れる例
   :header-rows: 1
   :widths: 22 38 40

   * - 分野
     - 方程式
     - 意味
   * - 静電場
     - :math:`\nabla^2 V = -\rho / \varepsilon_0`
     - :math:`\bm{E} = -\nabla V` とガウスの法則 :math:`\nabla \cdot \bm{E} = \rho / \varepsilon_0` から
   * - 重力場
     - :math:`\nabla^2 U = 4\pi G \rho`
     - 質量密度 :math:`\rho` が、単位質量あたりの位置エネルギー（重力ポテンシャル）\ :math:`U` の源
   * - 定常な熱伝導
     - :math:`\nabla^2 T = 0`
     - 熱源のない物体の中の、時間変化しない温度分布（:ref:`第 17 章 <ch17>`）
   * - ポテンシャル流
     - :math:`\nabla^2 \phi = 0`
     - 渦なしで非圧縮性の流れの速度ポテンシャル（:ref:`第 17 章 <ch17>`）

基本解
~~~~~~

:ref:`第 9 章 <ch09>`\ で見たように、:math:`\nabla^2 (1/r) = 0`\ （:math:`r \neq 0`）である。:math:`\phi = -\frac{1}{4\pi r}` とすると :math:`\nabla \phi = \frac{\bm{r}}{4\pi r^3}` であり、:ref:`第 14 章 <ch14>`\ の結果から、原点を囲む閉曲面を通る流束は :math:`\frac{1}{4\pi} \cdot 4\pi = 1` になる。つまり :math:`-\frac{1}{4\pi r}` は、原点に強さ 1 の湧き出しが集中している場合のポアソン方程式の解である。これを\ :term:`基本解`\ という。

湧き出しが :math:`s(\bm{r}')` で分布している場合は、各点の湧き出しがつくるポテンシャルを重ね合わせて

.. math::

   \phi(\bm{r}) = -\frac{1}{4\pi} \iiint \frac{s(\bm{r}')}{|\bm{r} - \bm{r}'|} \, dV'

が解になる。静電場では :math:`s = -\rho / \varepsilon_0` なので :math:`V(\bm{r}) = \frac{1}{4\pi\varepsilon_0} \iiint \frac{\rho(\bm{r}')}{|\bm{r} - \bm{r}'|} \, dV'` となり、点電荷の電位 :math:`\frac{q}{4\pi\varepsilon_0 r}` を重ね合わせたものに一致する。

解の一意性
~~~~~~~~~~

有界な領域 :math:`V` で、境界 :math:`\partial V` 上の :math:`\phi` の値を与えてポアソン方程式を解く問題を考える。解が 2 つあったとして、その差を :math:`u` とすると、:math:`\nabla^2 u = 0` で、境界上で :math:`u = 0` である。:ref:`第 14 章 <ch14>`\ のグリーンの恒等式で :math:`f = g = u` とすると

.. math::

   \iiint_V |\nabla u|^2 \, dV = \iint_{\partial V} u \nabla u \cdot d\bm{S} - \iiint_V u \nabla^2 u \, dV = 0

となる。被積分関数 :math:`|\nabla u|^2` は 0 以上なので、:math:`\nabla u = \bm{0}`、つまり :math:`u` は定数である。境界で :math:`u = 0` なので :math:`u = 0` となり、2 つの解は一致する。境界の値が決まれば、内部の解はただ 1 つに決まる。

調和関数の性質
~~~~~~~~~~~~~~

:ref:`第 8 章 <ch08>`\ で見たように、調和関数は平均値の性質を持ち（各点の値が周囲の平均に等しい）、定数でなければ最大値・最小値を境界でとる（最大値原理）。この「周囲の平均をとる」という性質は、:ref:`第 18 章 <ch18>`\ でラプラス方程式を数値的に解くヤコビ法の考え方の基礎になる。

この章のまとめ
--------------

* 回転が 0 であることは、スカラーポテンシャルを持つための必要条件である。単連結な領域では十分条件にもなる。
* 自由渦は原点以外で回転が 0 だが、原点を囲む閉曲線の循環は :math:`2\pi` であり、スカラーポテンシャルを持たない。領域が単連結でないためである。
* 発散が 0 の場はベクトルポテンシャルを持つ（空間全体などの領域で）。ベクトルポテンシャルには勾配を足す自由度（ゲージの自由度）がある。
* ヘルムホルツ分解により、一般のベクトル場は渦なしの成分と発散のない成分の和に分けられる。発散が前者を、回転が後者を決める。
* 渦なしの場のポテンシャルはポアソン方程式 :math:`\nabla^2 \phi = s` を満たす。湧き出しがなければラプラス方程式になり、その解（調和関数）は境界の値で一意に決まる。
