.. _ch14:

第 14 章 ガウスの発散定理
==========================

:ref:`第 6 章 <ch06>`\ では、発散を「微小な直方体から出ていく正味の流出量を体積で割ったもの」として導いた。この章で扱う\ :term:`ガウスの発散定理`\ は、これを有限の大きさの立体に広げたものであり、閉曲面から出ていく流束が、内部の発散の体積積分に等しいことを主張する。この章では、定理の内容と直観的な説明、座標によらない発散の定義を説明し、両辺を数値で計算して一致を確かめる。応用として、電場のガウスの法則と連続の式を導く。

ガウスの発散定理
----------------

空間の有界な立体 :math:`V` と、その境界である閉曲面 :math:`\partial V` を考える。閉曲面の向きは、外向き（立体の内部から外部へ向かう向き）を正とし、外向きの単位法線ベクトルを :math:`\bm{n}`、ベクトル面素を :math:`d\bm{S} = \bm{n} \, dS` とする。

ベクトル場 :math:`\bm{F}` の成分が、:math:`V` とその境界を含む範囲で連続な偏導関数を持つとき、次の式が成り立つ。これをガウスの発散定理という。単に発散定理、またはガウスの定理ともいう。

.. math::
   :label: eq-ch14-gauss

   \iint_{\partial V} \bm{F} \cdot d\bm{S} = \iiint_V \nabla \cdot \bm{F} \, dV

左辺は閉曲面全体を通って外へ出ていく流束（:ref:`第 12 章 <ch12>`）、右辺は立体の内部での発散の体積積分である。言葉で書くと、次のようになる。

* 閉曲面から出ていく正味の量 ＝ 内部の湧き出しの合計

たとえば、:math:`\bm{F}` を水の流れの速度とすると、左辺は単位時間に閉曲面から流れ出る水の体積である。内部に水の湧き出し口（発散が正の場所）があれば、その分だけ水が外へ出ていく。

.. note::

   閉曲面上の面積分は、閉曲面であることを示すために ∯ という記号で書くことも多い。本書では :math:`\iint_{\partial V}` と書き、積分範囲 :math:`\partial V` が閉曲面であることで区別する。

微小な直方体による説明
----------------------

:ref:`第 6 章 <ch06>`\ では、微小な直方体 :math:`\Delta V = \Delta x \, \Delta y \, \Delta z` の 6 つの面から出ていく流束の合計が、近似的に :math:`(\nabla \cdot \bm{F}) \, \Delta V` になることを見た。これは、ガウスの発散定理を微小な直方体に適用したものに当たる。

立体 :math:`V` を微小な直方体に分割し、各直方体から出ていく流束を足し合わせる。隣り合う 2 つの直方体が共有する面では、一方の直方体にとっての外向きの法線ベクトルは、もう一方にとっては内向きである。そのため、共有する面を通る流束は、一方の直方体ではプラス、もう一方ではマイナスに数えられ、打ち消し合う。足し合わせた後に残るのは、どの直方体とも共有されない面、つまり立体の表面 :math:`\partial V` を通る流束だけである。

一方、各直方体の流束は「発散 × 体積」なので、その和は発散の体積積分になる。直方体を細かくする極限で、:eq:`eq-ch14-gauss` が得られる。この議論は、:ref:`第 13 章 <ch13>`\ で微小な長方形を足し合わせてグリーンの定理を説明したもの（:numref:`fig-ch13-small-rectangles`）を、1 つ次元を上げたものである。実際、グリーンの定理の流束形は、ガウスの発散定理の 2 次元版になっている。

.. _ch14-definition:

座標によらない発散の定義
------------------------

:ref:`第 6 章 <ch06>`\ では、発散を直交座標の成分で :math:`\nabla \cdot \bm{F} = \partial F_x / \partial x + \partial F_y / \partial y + \partial F_z / \partial z` と定義した。ガウスの発散定理を使うと、座標を使わない定義が得られる。

点 :math:`\mathrm{P}` を含む小さな立体 :math:`V` を考え、その体積を :math:`|V|` とする。:math:`V` が十分小さければ、その中で :math:`\nabla \cdot \bm{F}` はほぼ一定なので、:eq:`eq-ch14-gauss` の右辺は :math:`(\nabla \cdot \bm{F})(\mathrm{P}) \, |V|` で近似できる。:math:`V` を点 :math:`\mathrm{P}` に縮める極限を取ると

.. math::
   :label: eq-ch14-div-definition

   (\nabla \cdot \bm{F})(\mathrm{P}) = \lim_{V \to \mathrm{P}} \frac{1}{|V|} \iint_{\partial V} \bm{F} \cdot d\bm{S}

となる。右辺は「単位体積あたりの流出量」であり、立体の形（直方体か球か）にも座標系の取り方にもよらない。発散が物理的な意味を持つ量であること、つまり座標系を回転しても値が変わらないことが、この式から分かる。

この定義は、曲線座標系で発散の式を導くときにも使える。:ref:`第 9 章 <ch09>`\ の直交曲線座標系での発散の式は、座標曲面で囲まれた微小な立体に :eq:`eq-ch14-div-definition` を適用したものと考えることができる。

数値で確かめる
--------------

具体的な場で、両辺を別々に数値積分して比べる。

1 つ目の例は、:math:`\bm{F} = (x^3, y^3, z^3)` と単位球 :math:`V`\ （半径 1、中心は原点）である。発散は :math:`\nabla \cdot \bm{F} = 3(x^2 + y^2 + z^2) = 3r^2` なので、球座標の体積素 :math:`dV = r^2 \sin\theta \, dr \, d\theta \, d\phi` を使うと、右辺は

.. math::

   \iiint_V 3r^2 \, dV = \int_0^{2\pi} \int_0^{\pi} \int_0^1 3r^4 \sin\theta \, dr \, d\theta \, d\phi = \frac{3}{5} \cdot 2 \cdot 2\pi = \frac{12\pi}{5}

である。左辺は、球面上の点 :math:`(\sin\theta \cos\phi, \sin\theta \sin\phi, \cos\theta)` での外向きの単位法線ベクトルがその点の位置ベクトルに等しく、面素が :math:`dS = \sin\theta \, d\theta \, d\phi` であることを使って数値積分する。

.. literalinclude:: ../examples/ch14_gauss_check.py
   :pyobject: sphere_flux
   :lineno-match:
   :caption: ch14_gauss_check.py の sphere_flux()

2 つ目の例は、:math:`\bm{G} = (xy, yz, zx)` と立方体 :math:`[0, 1]^3` である。発散は :math:`\nabla \cdot \bm{G} = y + z + x` で、その体積積分は :math:`3/2` になる。左辺は 6 つの面の流束の和として計算する。:math:`x = 1` の面では外向きの法線ベクトルが :math:`+\bm{e}_x`、:math:`x = 0` の面では :math:`-\bm{e}_x` である。

.. literalinclude:: ../build/outputs/ch14_gauss_check.txt
   :language: text
   :caption: ch14_gauss_check.py の実行結果

どちらの例でも、閉曲面の流束と発散の体積積分が一致している。

サンプルの全体：:download:`ch14_gauss_check.py <../examples/ch14_gauss_check.py>`

.. _ch14-gauss-law:

応用 1：電場のガウスの法則
--------------------------

原点に置いた点電荷 :math:`q` がつくる電場は、真空の誘電率を :math:`\varepsilon_0` として

.. math::

   \bm{E} = \frac{q}{4 \pi \varepsilon_0} \frac{\bm{r}}{r^3}

である。以下では、係数を除いた場 :math:`\bm{F} = \bm{r} / r^3` を考える。

原点を含む球と定理の前提
~~~~~~~~~~~~~~~~~~~~~~~~~~

:ref:`第 6 章 <ch06>`\ で示したように、:math:`\bm{F}` は原点以外で :math:`\nabla \cdot \bm{F} = 0` であり、湧き出しがない。一方、:ref:`第 12 章 <ch12>`\ で求めたように、原点を中心とする半径 :math:`R` の球面を外向きに通る :math:`\bm{F} = \bm{e}_r / r^2` の流束は、:math:`R` によらず :math:`4\pi` である。

ここで注意が必要である。球の内部では原点以外で :math:`\nabla \cdot \bm{F} = 0` なので、ガウスの発散定理をそのまま当てはめると流束は 0 になるはずだが、実際は :math:`4\pi` である。矛盾ではなく、:math:`\bm{F}` が原点で定義されず、定理の前提（:math:`V` 全体で偏導関数が連続）を満たさないことが原因である。点電荷の場の湧き出しは、すべて原点という 1 点に集中している。

任意の閉曲面の流束
~~~~~~~~~~~~~~~~~~

原点を囲む任意の閉曲面 :math:`S` を考える。:math:`S` の内側に、原点を中心とする小さな球面 :math:`S_\varepsilon` を取り、:math:`S` と :math:`S_\varepsilon` に挟まれた立体を :math:`V'` とする。:math:`V'` は原点を含まないので、ガウスの発散定理が使える。:math:`V'` の境界は :math:`S`\ （外向き）と :math:`S_\varepsilon`\ （:math:`V'` から見た外向き、つまり原点に向かう向き）なので

.. math::

   \iint_S \bm{F} \cdot d\bm{S} - \iint_{S_\varepsilon} \bm{F} \cdot d\bm{S} = \iiint_{V'} \nabla \cdot \bm{F} \, dV = 0

となる。ここで :math:`S_\varepsilon` の面積分は外向き（原点から遠ざかる向き）で計算したものであり、:math:`4\pi` である。したがって、原点を囲む閉曲面ならどのような形でも流束は :math:`4\pi` になる。一方、原点を囲まない閉曲面では、内部全体で発散が 0 なので流束は 0 である。

.. figure:: ../build/figures/ch14_point_charge.svg
   :name: fig-ch14-point-charge
   :width: 65%
   :align: center

   点電荷の場と、原点を囲む閉曲面 :math:`S_1`・囲まない閉曲面 :math:`S_2`

:numref:`fig-ch14-point-charge` の :math:`S_2` では、場は一方の側から入り、反対側から同じ量だけ出ていく。いろいろな閉曲面で流束を数値積分した結果を示す。

.. literalinclude:: ../build/outputs/ch14_point_charge.txt
   :language: text
   :caption: ch14_point_charge.py の実行結果

球面の中心をずらしても、立方体の表面でも、原点を囲んでいれば流束は :math:`4\pi \approx 12.566371` になる。

サンプルの全体：:download:`ch14_point_charge.py <../examples/ch14_point_charge.py>`

ガウスの法則
~~~~~~~~~~~~

係数を戻すと、点電荷 :math:`q` を囲む閉曲面を通る電場の流束は :math:`\frac{q}{4\pi\varepsilon_0} \cdot 4\pi = q / \varepsilon_0` である。電荷が複数あるときは、電場は各電荷の電場の和（重ね合わせ）なので、流束は閉曲面の内部にある電荷の合計 :math:`Q` だけで決まる。

.. math::

   \iint_{\partial V} \bm{E} \cdot d\bm{S} = \frac{Q}{\varepsilon_0}

これを\ :term:`ガウスの法則`\ （積分形）という。電荷が電荷密度 :math:`\rho` で連続的に分布している場合は :math:`Q = \iiint_V \rho \, dV` である。左辺にガウスの発散定理を使うと

.. math::

   \iiint_V \nabla \cdot \bm{E} \, dV = \iiint_V \frac{\rho}{\varepsilon_0} \, dV

となる。これが任意の立体 :math:`V` で成り立つので、被積分関数どうしが等しい。

.. math::

   \nabla \cdot \bm{E} = \frac{\rho}{\varepsilon_0}

これがガウスの法則の微分形であり、マクスウェル方程式の 1 つである（:ref:`第 17 章 <ch17>`）。「任意の立体で積分が等しいなら、被積分関数が等しい」という論法は、積分形の法則から微分形の法則を導くときに繰り返し使う。被積分関数が連続で、ある点で両辺が異なれば、その点の周りの小さな立体で積分が異なってしまうからである。

.. tip::

   点電荷の電荷密度は原点だけに集中しているので、通常の関数では表せない。物理や工学では、ディラックのデルタ関数 :math:`\delta^3(\bm{r})` を使って :math:`\nabla \cdot (\bm{r}/r^3) = 4\pi \delta^3(\bm{r})` と書く。デルタ関数は、原点を含む立体で積分すると 1、含まない立体で積分すると 0 になる「関数」である。

.. _ch14-continuity:

応用 2：連続の式
----------------

流体の密度を :math:`\rho(\bm{r}, t)`、流れの速度を :math:`\bm{v}(\bm{r}, t)` とする。ここでの :math:`\rho` は密度であり、円柱座標の :math:`\rho` とは別のものである。空間に固定した立体 :math:`V` の中の質量の変化を考える。

* 立体の中の質量は :math:`\iiint_V \rho \, dV` である。
* 単位時間に閉曲面から流れ出る質量は、:math:`\rho \bm{v}`\ （単位時間に単位面積を通る質量を表すベクトル場）の流束 :math:`\iint_{\partial V} \rho \bm{v} \cdot d\bm{S}` である。

質量は生まれも消えもしない（質量保存）ので、立体の中の質量は、流れ出た分だけ減る。

.. math::

   \frac{d}{dt} \iiint_V \rho \, dV = -\iint_{\partial V} \rho \bm{v} \cdot d\bm{S}

左辺の時間微分は、立体が固定されているので積分の中に入れられる。右辺にガウスの発散定理を使うと

.. math::

   \iiint_V \left( \frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \bm{v}) \right) dV = 0

となる。これが任意の立体 :math:`V` で成り立つので、次の\ :term:`連続の式`\ を得る。

.. math::
   :label: eq-ch14-continuity

   \frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \bm{v}) = 0

密度が一定の流体（水のような\ :term:`非圧縮性`\ の流体）では :math:`\partial \rho / \partial t = 0` で、:math:`\rho` を微分の外に出せるので、連続の式は :math:`\nabla \cdot \bm{v} = 0` になる。非圧縮性の流れは、発散のない場である。

同じ論法は、保存される量なら何にでも使える。電荷の密度 :math:`\rho` と電流密度 :math:`\bm{J}` については、電荷保存則 :math:`\partial \rho / \partial t + \nabla \cdot \bm{J} = 0` が得られる。熱の場合は\ :ref:`第 17 章 <ch17>`\ で熱伝導方程式を導くのに使う。

グリーンの恒等式
----------------

ガウスの発散定理を :math:`\bm{F} = f \nabla g` に適用すると、便利な公式が得られる。:ref:`第 8 章 <ch08>`\ の積の公式から :math:`\nabla \cdot (f \nabla g) = \nabla f \cdot \nabla g + f \nabla^2 g` なので

.. math::

   \iiint_V (\nabla f \cdot \nabla g + f \nabla^2 g) \, dV = \iint_{\partial V} f \nabla g \cdot d\bm{S}

となる。これを\ :term:`グリーンの恒等式`\ （第 1 恒等式）という。1 変数の部分積分 :math:`\int_a^b f g'' \, dx = [f g']_a^b - \int_a^b f' g' \, dx` を 3 次元に広げたものであり、:ref:`第 16 章 <ch16>`\ でポアソン方程式の解が一意であることを示すのに使う。:math:`f` と :math:`g` を入れ替えた式を引くと、第 2 恒等式

.. math::

   \iiint_V (f \nabla^2 g - g \nabla^2 f) \, dV = \iint_{\partial V} (f \nabla g - g \nabla f) \cdot d\bm{S}

も得られる。

この章のまとめ
--------------

* ガウスの発散定理は、閉曲面から外へ出ていく流束が、内部の発散の体積積分に等しいことを表す。
* 定理は、立体を微小な直方体に分け、共有する面の流束が打ち消し合うことで理解できる。
* 発散は「単位体積あたりの流出量」として、座標によらずに定義できる。
* 点電荷の場は原点以外で発散が 0 だが、原点を囲む閉曲面の流束は :math:`4\pi` になる。湧き出しが原点に集中しているためである。ここからガウスの法則 :math:`\nabla \cdot \bm{E} = \rho / \varepsilon_0` が導かれる。
* 保存則の積分形にガウスの発散定理を使うと、連続の式 :math:`\partial \rho / \partial t + \nabla \cdot (\rho \bm{v}) = 0` のような微分形の法則が得られる。
