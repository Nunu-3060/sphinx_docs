.. _ch06:

第 6 章 双曲三角法と面積
========================

この章では、双曲平面の三角形の辺と角の関係（双曲三角法）と、三角形の面積を扱う。ユークリッド幾何学の余弦定理、正弦定理、三平方の定理に対応する公式があり、どれも小さな三角形ではユークリッドの公式に近づく。一方、面積が内角だけで決まるという、ユークリッド幾何学にない性質が現れる。

記号の約束
----------

双曲平面の 3 点 :math:`A`、:math:`B`、:math:`C` を測地線分で結んだ図形を三角形という。本章では、頂点 :math:`A`、:math:`B`、:math:`C` の内角を :math:`\alpha`、:math:`\beta`、:math:`\gamma`、それぞれの対辺の長さを :math:`a`、:math:`b`、:math:`c` とする。長さはすべて双曲距離である。

双曲余弦定理
------------

双曲平面の三角形では、次の\ :term:`双曲余弦定理`\ が成り立つ。

.. math::
   :label: eq-ch06-cosine

   \cosh c = \cosh a \cosh b - \sinh a \sinh b \cos \gamma

双曲面モデルを使うと、この式は簡単に導ける。等長変換で頂点 :math:`C` を双曲面の頂点 :math:`(1, 0, 0)` に移し、さらに :math:`x_0` 軸のまわりに回転して、辺 :math:`CA` を :math:`x_0 x_1` 平面の中に置く。頂点 :math:`C` から出る測地線は、:math:`C` を通る双曲線 :math:`(\cosh t, \ \sinh t \cos\theta, \ \sinh t \sin\theta)` であり、:math:`t` が :math:`C` からの距離、:math:`\theta` が向きを表す。したがって

.. math::

   A = (\cosh b, \ \sinh b, \ 0), \qquad B = (\cosh a, \ \sinh a \cos \gamma, \ \sinh a \sin \gamma)

と書ける。双曲面モデルの距離の公式 :math:`\cosh c = B(A, B)` に代入すると

.. math::

   \cosh c = \cosh a \cosh b - \sinh a \sinh b \cos \gamma

が得られる。

球面の余弦定理 :math:`\cos c = \cos a \cos b + \sin a \sin b \cos \gamma` も、単位球面上で同じ手順（内積 :math:`\cos c = A \cdot B`）で導ける。2 つの公式が :math:`\cos` と :math:`\cosh` の入れ替えで対応するのは、\ :ref:`第 3 章 <ch03>`\ で述べた双曲面モデルと球面の類似による。

三角形が小さいとき、:math:`\cosh x \approx 1 + x^2/2`、:math:`\sinh x \approx x` を代入して 2 次の項まで残すと

.. math::

   1 + \frac{c^2}{2} \approx 1 + \frac{a^2}{2} + \frac{b^2}{2} - ab \cos \gamma

すなわち :math:`c^2 \approx a^2 + b^2 - 2ab \cos \gamma` となり、ユークリッドの余弦定理に一致する。

直角三角形
----------

:math:`\gamma = \pi/2` とすると、:math:`\cos \gamma = 0` なので、式 :eq:`eq-ch06-cosine` は

.. math::

   \cosh c = \cosh a \cosh b

となる。これが双曲平面の\ **三平方の定理**\ である。小さな三角形では :math:`c^2 \approx a^2 + b^2` となる。一方、大きな三角形では、:math:`\cosh x \approx e^x / 2` より :math:`c \approx a + b - \ln 2` となり、斜辺の長さが 2 辺の長さの和に近づく。双曲平面の大きな三角形は「やせて」いて、辺の上の点はどれも、ほかの 2 辺のどちらかに近い。

正弦定理と第 2 余弦定理
-----------------------

ユークリッドの正弦定理に対応して、\ :term:`双曲正弦定理`

.. math::

   \frac{\sin \alpha}{\sinh a} = \frac{\sin \beta}{\sinh b} = \frac{\sin \gamma}{\sinh c}

が成り立つ。

さらに、双曲平面には、3 つの角から辺を求める公式（第 2 余弦定理）がある。

.. math::
   :label: eq-ch06-cosine2

   \cos \gamma = -\cos \alpha \cos \beta + \sin \alpha \sin \beta \cosh c

この式は、3 つの角が決まれば、辺の長さ :math:`c` が（同様に :math:`a`、:math:`b` も）決まることを示している。つまり、双曲平面では 3 つの角が等しい 2 つの三角形は合同である。ユークリッド平面では、3 つの角が等しくても大きさの違う三角形（相似な三角形）がいくらでもあるのと対照的である。\ :ref:`第 1 章 <ch01>`\ で、相似な三角形の存在が平行線公準と同値であると述べたのは、このことに対応する。

三角形の面積
------------

面積も、計量から決まる。上半平面モデルでは、ユークリッドの面積要素 :math:`dx \, dy` を :math:`y^2` で割った

.. math::

   dA = \frac{dx \, dy}{y^2}

が面積要素である（長さが :math:`1/y` 倍になるので、面積は :math:`1/y^2` 倍になる）。同様に、円板モデルでは :math:`dA = 4 \, dx \, dy / (1 - |z|^2)^2`、クラインモデルでは :math:`dA = dx \, dy / (1 - |k|^2)^{3/2}` である。

三角形の面積については、次の\ :term:`ガウス・ボネの定理`\ （三角形の場合）が成り立つ。

.. math::
   :label: eq-ch06-area

   A = \pi - (\alpha + \beta + \gamma)

面積は正なので、内角の和は必ず :math:`\pi` （180 度）より小さい。:math:`\pi` からの不足分 :math:`\pi - (\alpha + \beta + \gamma)` を\ :term:`角欠損`\ という。面積は角欠損に等しく、内角だけで決まる。曲率が :math:`K = -1/R^2` のときは :math:`A = R^2 (\pi - (\alpha + \beta + \gamma))` となる。

式 :eq:`eq-ch06-area` の意味を、極端な場合で確かめる。3 つの頂点がすべて無限遠点にある三角形を\ :term:`理想三角形`\ という。理想三角形の内角はすべて 0 であり（隣り合う 2 辺が無限遠点で接するため）、式 :eq:`eq-ch06-area` によれば面積は :math:`\pi` である。上半平面モデルで、頂点が :math:`-1`、:math:`1`、:math:`\infty` の理想三角形は、2 本の垂直な半直線 :math:`x = \pm 1` と単位半円で囲まれた領域であり、その面積は

.. math::

   A = \int_{-1}^{1} \int_{\sqrt{1 - x^2}}^{\infty} \frac{dy}{y^2} \, dx = \int_{-1}^{1} \frac{dx}{\sqrt{1 - x^2}} = \pi

となって、確かに :math:`\pi` に一致する。理想三角形はすべて合同であり、どんな三角形も理想三角形の中に収まるので、双曲平面の三角形の面積は :math:`\pi` を超えない。辺の長さはいくらでも長くできるのに、面積には上限がある。

一般の三角形については、三角形を理想三角形から切り取った形として表し、面積の足し引きで式 :eq:`eq-ch06-area` を導ける。詳しくは参考文献（\ :ref:`付録 D <appendix-d>`\ ）を参照してほしい。

:math:`n` 角形の内角の和は、:math:`n - 2` 個の三角形に分けて考えると、:math:`(n - 2)\pi` から面積を引いたものになる。特に、四角形の内角の和は 360 度より小さく、4 つの角がすべて直角の四角形（長方形）は存在しない。

大きさと内角の和
----------------

円板モデルで、中心から頂点までの距離 :math:`R` を変えて正三角形を描いたものが\ :numref:`fig-ch06-triangles`\ である。

.. figure:: ../build/figures/ch06_triangles.svg
   :name: fig-ch06-triangles
   :width: 60%
   :align: center

   大きさの異なる正三角形と、その内角の和

サンプルの全体：:download:`ch06_triangles.py <../examples/ch06_triangles.py>`

小さな三角形（:math:`R = 0.4`）はユークリッドの三角形に近く、内角の和は 180 度に近い。三角形が大きくなるにつれて辺が内側にへこみ、内角の和が減っていく。頂点を境界まで遠ざけた極限が理想三角形であり、内角の和は 0 になる。

数値で確かめる
--------------

円板モデルの三角形の辺と角を ``hg.py`` の関数で測り、双曲余弦定理、正弦定理、ガウス・ボネの定理の両辺を比べる。面積は、クラインモデル（辺が線分になる）で三角形を細かな三角形に分割し、面積要素を数値積分して求める。

.. literalinclude:: ../examples/ch06_trig.py
   :pyobject: klein_area
   :lineno-match:
   :caption: ch06_trig.py の klein_area()

.. literalinclude:: ../build/outputs/ch06_trig.txt
   :language: text
   :caption: ch06_trig.py の実行結果

サンプルの全体：:download:`ch06_trig.py <../examples/ch06_trig.py>`

余弦定理と正弦定理は、丸め誤差の範囲で成り立っている。数値積分で求めた面積は、角欠損 :math:`\pi - (\alpha + \beta + \gamma)` に有効数字 5 桁ほどで一致する（差は数値積分の誤差である）。最後の表は、頂点の配置を保ったまま、中心からの距離を縮めた三角形の内角の和である。三角形が小さくなるほど、内角の和は 180 度に近づく。

この章のまとめ
--------------

* 双曲余弦定理 :math:`\cosh c = \cosh a \cosh b - \sinh a \sinh b \cos \gamma` は、双曲面モデルで内積の代わりに :math:`B` を使えば導ける。
* 小さな三角形では、双曲三角法の公式はユークリッドの公式に近づく。
* 3 つの角が決まれば三角形は合同になり、相似で大きさの異なる三角形は存在しない。
* 三角形の面積は角欠損 :math:`\pi - (\alpha + \beta + \gamma)` に等しく、:math:`\pi` を超えない。
