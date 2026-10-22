.. _ch08:

第 8 章 ナブラを含む公式とラプラシアン
======================================

勾配・発散・回転を組み合わせたり、場の積に作用させたりすると、多くの公式が得られる。この章では、積の微分公式と 2 階の微分の公式をまとめ、特に重要な「勾配の回転は 0」「回転の発散は 0」の意味を説明する。後半では、勾配の発散であるラプラシアンを導入し、その意味を「周囲の平均との差」として理解する。

積の微分公式
------------

1 変数の微分には積の微分公式 :math:`(fg)' = f'g + fg'` がある。ナブラは偏微分を並べたものなので、場の積に作用させたときにも同様の公式が成り立つ。:math:`f, g` をスカラー場、:math:`\bm{F}, \bm{G}` をベクトル場とする。

.. list-table:: ナブラを含む積の微分公式
   :header-rows: 1
   :widths: 8 92

   * - 番号
     - 公式
   * - (1)
     - :math:`\nabla (fg) = f \nabla g + g \nabla f`
   * - (2)
     - :math:`\nabla \cdot (f\bm{F}) = \nabla f \cdot \bm{F} + f \, \nabla \cdot \bm{F}`
   * - (3)
     - :math:`\nabla \times (f\bm{F}) = \nabla f \times \bm{F} + f \, \nabla \times \bm{F}`
   * - (4)
     - :math:`\nabla \cdot (\bm{F} \times \bm{G}) = \bm{G} \cdot (\nabla \times \bm{F}) - \bm{F} \cdot (\nabla \times \bm{G})`
   * - (5)
     - :math:`\nabla \times (\bm{F} \times \bm{G}) = \bm{F} (\nabla \cdot \bm{G}) - \bm{G} (\nabla \cdot \bm{F}) + (\bm{G} \cdot \nabla) \bm{F} - (\bm{F} \cdot \nabla) \bm{G}`
   * - (6)
     - :math:`\nabla (\bm{F} \cdot \bm{G}) = (\bm{F} \cdot \nabla) \bm{G} + (\bm{G} \cdot \nabla) \bm{F} + \bm{F} \times (\nabla \times \bm{G}) + \bm{G} \times (\nabla \times \bm{F})`

(1) は\ :ref:`第 5 章 <ch05>`\ で示した。(2) は成分で書けばすぐに確かめられる。

.. math::

   \nabla \cdot (f\bm{F}) &= \frac{\partial (f F_x)}{\partial x} + \frac{\partial (f F_y)}{\partial y} + \frac{\partial (f F_z)}{\partial z} \\
   &= \left( \frac{\partial f}{\partial x} F_x + \frac{\partial f}{\partial y} F_y + \frac{\partial f}{\partial z} F_z \right) + f \left( \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z} \right) \\
   &= \nabla f \cdot \bm{F} + f \, \nabla \cdot \bm{F}

(3) も同様に成分で確かめられる。(4) から (6) も成分で確かめられるが、式が長くなる。添字を使った短い証明は\ :ref:`付録 B <appendix-b>` で示し、この章では後で SymPy を使って確かめる。

(5) と (6) に現れる :math:`(\bm{F} \cdot \nabla) \bm{G}` は、演算子

.. math::

   \bm{F} \cdot \nabla = F_x \frac{\partial}{\partial x} + F_y \frac{\partial}{\partial y} + F_z \frac{\partial}{\partial z}

を :math:`\bm{G}` の各成分に作用させたベクトルである。:math:`\bm{F}` が単位ベクトルなら、:math:`(\bm{F} \cdot \nabla) \bm{G}` は :math:`\bm{G}` の :math:`\bm{F}` の向きの方向微分（:ref:`第 5 章 <ch05>`）を成分ごとに並べたものになる。流体の速度 :math:`\bm{v}` を使った :math:`(\bm{v} \cdot \nabla) \bm{v}` は、流れに乗って動いたときの速度の変化を表し、流体の運動方程式に現れる（:ref:`第 17 章 <ch17>`）。

公式の覚え方
~~~~~~~~~~~~

これらの公式は、次の 2 つの規則を組み合わせると覚えやすい。

* 積の微分：ナブラは積の各因子に順に作用する。たとえば (2) では、:math:`f` に作用した項と :math:`\bm{F}` に作用した項の和になる。
* ベクトルの公式：作用する相手を決めたら、ナブラを普通のベクトルとみなしてベクトルの公式を当てはめる。(4) はスカラー三重積の性質、(5) はベクトル三重積の公式 :math:`\bm{a} \times (\bm{b} \times \bm{c}) = \bm{b}(\bm{a} \cdot \bm{c}) - \bm{c}(\bm{a} \cdot \bm{b})`\ （:ref:`第 2 章 <ch02>`）に対応する。

ただし、ベクトルの公式を当てはめるときは、ナブラが作用する場をナブラの右側に置かなければならない。(5) の :math:`(\bm{G} \cdot \nabla) \bm{F}` は、ベクトル三重積の公式の :math:`\bm{b}(\bm{a} \cdot \bm{c})` で :math:`\bm{a} = \nabla` が :math:`\bm{b} = \bm{F}` に作用する項を、作用する相手が右に来るように並べ替えたものである。覚え方はあくまで目安であり、符号や順序に迷ったら成分で確かめるのが確実である。

2 階の微分
----------

勾配・発散・回転を 2 回続けて使う組み合わせのうち、作用させる場の種類（スカラー場かベクトル場か）が合うものは次の 5 通りである。

.. list-table:: 2 階の微分の組み合わせ
   :header-rows: 1
   :widths: 30 20 50

   * - 組み合わせ
     - 結果
     - 内容
   * - 勾配の発散 :math:`\nabla \cdot (\nabla f)`
     - スカラー場
     - ラプラシアン :math:`\nabla^2 f`
   * - 勾配の回転 :math:`\nabla \times (\nabla f)`
     - ベクトル場
     - 常に :math:`\bm{0}`
   * - 発散の勾配 :math:`\nabla (\nabla \cdot \bm{F})`
     - ベクトル場
     - 特別な名前はない
   * - 回転の発散 :math:`\nabla \cdot (\nabla \times \bm{F})`
     - スカラー場
     - 常に 0
   * - 回転の回転 :math:`\nabla \times (\nabla \times \bm{F})`
     - ベクトル場
     - :math:`\nabla (\nabla \cdot \bm{F}) - \nabla^2 \bm{F}`

以下、この表の公式を説明する。場は 2 回連続して偏微分でき、2 階の偏導関数が連続であるとする。

勾配の回転は 0
~~~~~~~~~~~~~~

:math:`\nabla f` の回転の :math:`x` 成分は

.. math::

   \frac{\partial}{\partial y} \left( \frac{\partial f}{\partial z} \right) - \frac{\partial}{\partial z} \left( \frac{\partial f}{\partial y} \right) = 0

である。偏微分の順序を交換できる（シュワルツの定理。:ref:`第 4 章 <ch04>`）ので、2 つの項は等しい。:math:`y, z` 成分も同様なので

.. math::
   :label: eq-ch08-curl-grad

   \nabla \times (\nabla f) = \bm{0}

が成り立つ。勾配で表されるベクトル場は渦なしの場である（:ref:`第 7 章 <ch07>`）。たとえば、位置エネルギーの勾配で表される力 :math:`\bm{F} = -\nabla U` は、回転が :math:`\bm{0}` である。形式的には、同じベクトルどうしの外積 :math:`\bm{a} \times \bm{a} = \bm{0}` に対応する。

回転の発散は 0
~~~~~~~~~~~~~~

:math:`\nabla \times \bm{F}` の発散を成分で書くと

.. math::

   \frac{\partial}{\partial x} \left( \frac{\partial F_z}{\partial y} - \frac{\partial F_y}{\partial z} \right) + \frac{\partial}{\partial y} \left( \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \right) + \frac{\partial}{\partial z} \left( \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right)

となる。偏微分の順序を交換できるので、たとえば :math:`\partial^2 F_z / \partial x \partial y` の項と :math:`-\partial^2 F_z / \partial y \partial x` の項が打ち消し合い、全体は 0 になる。

.. math::
   :label: eq-ch08-div-curl

   \nabla \cdot (\nabla \times \bm{F}) = 0

回転で表されるベクトル場は、発散のない場である（:ref:`第 6 章 <ch06>`）。形式的には、同じベクトルを 2 つ含むスカラー三重積 :math:`\bm{a} \cdot (\bm{a} \times \bm{b}) = 0` に対応する。磁束密度 :math:`\bm{B}` を別のベクトル場の回転として :math:`\bm{B} = \nabla \times \bm{A}` と表す（ベクトルポテンシャル）と、:math:`\nabla \cdot \bm{B} = 0` が自動的に満たされる。

:eq:`eq-ch08-curl-grad` と :eq:`eq-ch08-div-curl` の逆、つまり「渦なしの場は勾配で表せるか」「発散のない場は回転で表せるか」は、場が定義されている領域の形に依存する。これは\ :ref:`第 16 章 <ch16>`\ で扱う。

回転の回転
~~~~~~~~~~

回転の回転には次の公式がある。

.. math::
   :label: eq-ch08-curl-curl

   \nabla \times (\nabla \times \bm{F}) = \nabla (\nabla \cdot \bm{F}) - \nabla^2 \bm{F}

右辺の :math:`\nabla^2 \bm{F}` はベクトル場のラプラシアンであり、次節で定義する。この公式はベクトル三重積の公式で :math:`\bm{a} = \bm{b} = \nabla`、:math:`\bm{c} = \bm{F}` とした形をしている。:math:`x` 成分を書き下すと

.. math::

   (\nabla \times (\nabla \times \bm{F}))_x &= \frac{\partial}{\partial y} \left( \frac{\partial F_y}{\partial x} - \frac{\partial F_x}{\partial y} \right) - \frac{\partial}{\partial z} \left( \frac{\partial F_x}{\partial z} - \frac{\partial F_z}{\partial x} \right) \\
   &= \frac{\partial}{\partial x} \left( \frac{\partial F_y}{\partial y} + \frac{\partial F_z}{\partial z} \right) - \left( \frac{\partial^2 F_x}{\partial y^2} + \frac{\partial^2 F_x}{\partial z^2} \right) \\
   &= \frac{\partial}{\partial x} (\nabla \cdot \bm{F}) - \nabla^2 F_x

となる（最後の行では :math:`\partial^2 F_x / \partial x^2` を足して引いた）。この公式は、マクスウェル方程式から電磁波の波動方程式を導くときに使う（:ref:`第 17 章 <ch17>`）。

ラプラシアン
------------

勾配の発散を\ :term:`ラプラシアン`\ （Laplacian）という。

.. math::
   :label: eq-ch08-laplacian

   \nabla^2 f = \nabla \cdot (\nabla f) = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}

演算子 :math:`\nabla^2 = \partial^2 / \partial x^2 + \partial^2 / \partial y^2 + \partial^2 / \partial z^2` は、ナブラと自分自身の内積の形をしている。数学の本では :math:`\Delta f` と書くことも多い。本書では :math:`\nabla^2 f` と書く。

計算例を示す。

* :math:`f = r^2 = x^2 + y^2 + z^2` では、:math:`\nabla^2 f = 2 + 2 + 2 = 6` である。
* :math:`f = x^2 - y^2` では、:math:`\nabla^2 f = 2 - 2 = 0` である。
* :math:`f = 1/r` では、:ref:`第 5 章 <ch05>`\ の :math:`\nabla (1/r) = -\bm{r}/r^3` と、:ref:`第 6 章 <ch06>`\ の :math:`\nabla \cdot (\bm{r}/r^3) = 0` から、:math:`\nabla^2 (1/r) = 0`\ （:math:`r \neq 0`）である。

ベクトル場 :math:`\bm{F}` のラプラシアン :math:`\nabla^2 \bm{F}` は、直交座標では成分ごとのラプラシアンを並べたベクトル場である。

.. math::

   \nabla^2 \bm{F} = (\nabla^2 F_x, \ \nabla^2 F_y, \ \nabla^2 F_z)

曲線座標系では基底ベクトルが場所によって変わるため、成分ごとのラプラシアンにはならない。そのときは :eq:`eq-ch08-curl-curl` を逆に使い、:math:`\nabla^2 \bm{F} = \nabla (\nabla \cdot \bm{F}) - \nabla \times (\nabla \times \bm{F})` で計算する（:ref:`第 9 章 <ch09>`）。

ラプラシアンは、熱伝導方程式、波動方程式、\ :term:`ラプラス方程式`、ポアソン方程式など、工学の主要な偏微分方程式に現れる（:ref:`第 16 章 <ch16>`、:ref:`第 17 章 <ch17>`）。

ラプラシアンの意味
------------------

ラプラシアンは、「ある点の値が、周囲の平均からどれだけずれているか」を表す。1 変数で考えると分かりやすい。2 階微分は

.. math::

   f''(x) \approx \frac{f(x + h) + f(x - h) - 2f(x)}{h^2} = \frac{2}{h^2} \left( \frac{f(x + h) + f(x - h)}{2} - f(x) \right)

と近似でき、両隣の平均と中心の値の差に比例する。:math:`f'' > 0`\ （下に凸）なら中心は両隣の平均より低く、:math:`f'' < 0`\ （上に凸）なら高い。

2 次元でも同じことが成り立つ。点 :math:`\bm{p}` を中心とする半径 :math:`h` の円周上での :math:`f` の平均を :math:`\bar{f}(h)` とする。円周上の点を :math:`\bm{p} + (h\cos t, h\sin t)` と表し、:math:`f` を 2 次の項までテイラー展開すると、1 次の項と :math:`\cos t \sin t` の項は円周を一周すると平均が 0 になる。残るのは :math:`\cos^2 t` と :math:`\sin^2 t` の項で、その平均はどちらも :math:`1/2` なので

.. math::

   \bar{f}(h) \approx f(\bm{p}) + \frac{1}{2} \left( \frac{\partial^2 f}{\partial x^2} \cdot \frac{h^2}{2} + \frac{\partial^2 f}{\partial y^2} \cdot \frac{h^2}{2} \right) = f(\bm{p}) + \frac{h^2}{4} \nabla^2 f(\bm{p})

となる。つまり

.. math::

   \nabla^2 f(\bm{p}) = \lim_{h \to 0} \frac{4}{h^2} \bigl( \bar{f}(h) - f(\bm{p}) \bigr)

である。3 次元で半径 :math:`h` の球面上の平均を考えると、同様に :math:`\bar{f}(h) \approx f(\bm{p}) + (h^2/6) \nabla^2 f(\bm{p})` となる。

* :math:`\nabla^2 f > 0` の点では、:math:`f` は周囲の平均より小さい（谷の底のような形）。
* :math:`\nabla^2 f < 0` の点では、:math:`f` は周囲の平均より大きい（山の頂上のような形）。

この関係を数値で確かめる。円周上の平均を SciPy で数値積分し、:math:`4(\bar{f} - f) / h^2` を計算する。

.. literalinclude:: ../examples/ch08_laplacian_mean.py
   :pyobject: circle_mean
   :lineno-match:
   :caption: ch08_laplacian_mean.py の circle_mean()

.. literalinclude:: ../build/outputs/ch08_laplacian_mean.txt
   :language: text
   :caption: ch08_laplacian_mean.py の実行結果

1 つ目の関数では、:math:`h` を小さくすると :math:`4(\bar{f} - f) / h^2` がラプラシアンの値 7.520574 に近づく。2 つ目の関数 :math:`x^2 - y^2` はラプラシアンが 0 であり、円周上の平均は :math:`h` によらず中心の値に等しい。

サンプルの全体：:download:`ch08_laplacian_mean.py <../examples/ch08_laplacian_mean.py>`

:numref:`fig-ch08-laplacian-bump` は、山の形をしたスカラー場 :math:`f = e^{-(x^2 + y^2)}` と、そのラプラシアン :math:`\nabla^2 f = 4(r^2 - 1) e^{-r^2}`\ （:math:`r^2 = x^2 + y^2`）を色で表したものである。山頂の付近（:math:`r < 1`）では周囲より高いのでラプラシアンは負、山のすそ（:math:`r > 1`）では下に凸の形になるので正である。

.. figure:: ../build/figures/ch08_laplacian_bump.svg
   :name: fig-ch08-laplacian-bump
   :width: 95%
   :align: center

   山の形をしたスカラー場とそのラプラシアン

サンプルの全体：:download:`ch08_laplacian_bump.py <../examples/ch08_laplacian_bump.py>`

この「周囲の平均との差」という見方は、ラプラシアンを数値計算するときにそのまま使える。2 次元の格子の間隔を :math:`h` とすると、上下左右の 4 点の平均と中心の値の差から

.. math::

   \nabla^2 f(x, y) \approx \frac{f(x + h, y) + f(x - h, y) + f(x, y + h) + f(x, y - h) - 4 f(x, y)}{h^2}

と近似できる。この差分による近似は\ :ref:`第 18 章 <ch18>`\ で使う。

調和関数
~~~~~~~~

:math:`\nabla^2 f = 0` を満たす関数を\ :term:`調和関数`\ という。方程式 :math:`\nabla^2 f = 0` はラプラス方程式と呼ばれる。上の :math:`x^2 - y^2` や、原点以外での :math:`1/r` は調和関数である。

調和関数は、どの点でも値が周囲の平均に等しい。実際、調和関数では円周（3 次元では球面）上の平均が、半径によらず中心の値に厳密に一致する（平均値の性質）。この性質から、定数でない調和関数は領域の内部で最大値も最小値もとらず、最大値と最小値は領域の境界でとる（最大値原理）。理由は次のとおりである。内部の点 P で最大値をとったとすると、P を中心とする小さな円周上の値はどれも P の値以下であり、しかもその平均は P の値に等しい。したがって、円周上の値はすべて P の値に等しい。半径を変えても同じことがいえるので、P の周りで関数は一定になる。これを領域全体に広げていくと、関数は定数になってしまう。最小値も同じである。たとえば、時間がたって変化しなくなった温度分布は調和関数になる（:ref:`第 17 章 <ch17>`）。そのため、内部に熱源がなければ、最も熱い点と最も冷たい点は必ず境界にある。

SymPy で公式を確かめる
----------------------

この章の公式が任意のスカラー場とベクトル場で成り立つことを、SymPy で確かめる。``sp.Function("f")(x, y, z)`` は、具体的な形を決めない :math:`x, y, z` の関数を表す。勾配・発散・回転を偏微分で定義し、各公式の「左辺 − 右辺」を展開して 0 になるかを調べる。

.. literalinclude:: ../examples/ch08_identities.py
   :start-at: def grad
   :end-before: def dot
   :lineno-match:
   :caption: ch08_identities.py の勾配・発散・回転・ラプラシアンの定義

.. literalinclude:: ../build/outputs/ch08_identities.txt
   :language: text
   :caption: ch08_identities.py の実行結果

すべての公式が成り立つことが確かめられた。SymPy は偏微分の順序を区別しない（:math:`\partial^2 f / \partial x \partial y` と :math:`\partial^2 f / \partial y \partial x` を同じ式として扱う）ので、この確認はシュワルツの定理が成り立つ場を前提にしている。

サンプルの全体：:download:`ch08_identities.py <../examples/ch08_identities.py>`

この章のまとめ
--------------

* ナブラを場の積に作用させると、積の微分とベクトルの公式を組み合わせた形の公式が得られる。迷ったら成分で確かめる。
* 勾配の回転は常に :math:`\bm{0}`、回転の発散は常に 0 である。勾配の場は渦なし、回転の場は発散がない。
* 回転の回転は :math:`\nabla (\nabla \cdot \bm{F}) - \nabla^2 \bm{F}` である。
* ラプラシアン :math:`\nabla^2 f` は勾配の発散であり、ある点の値と周囲の平均との差を表す。
* ラプラシアンが 0 の調和関数は、平均値の性質を持ち、定数でなければ領域の内部で最大値・最小値をとらない（最大値原理）。
