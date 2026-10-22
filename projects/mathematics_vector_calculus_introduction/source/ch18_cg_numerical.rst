.. _ch18:

第 18 章 CG と数値計算への応用
==============================

実際の問題では、場は式ではなく、格子点の上の数値の並びとして与えられることが多い。この章の前半では、格子上の値から勾配・発散・回転・ラプラシアンを差分で求める方法と、ラプラス方程式を反復法で解く方法を説明する。後半では、コンピューターグラフィックス（CG）で、法線の計算、ノーマルマップ、カールノイズ、流体シミュレーションの圧力投影にベクトル解析がどのように使われているかを見る。

差分による微分
--------------

前進差分と中心差分
~~~~~~~~~~~~~~~~~~

関数 :math:`f(x)` の微分係数は、小さな刻み幅 :math:`h` を使って

.. math::

   f'(x) \approx \frac{f(x + h) - f(x)}{h} \qquad \text{（前進差分）}, \qquad f'(x) \approx \frac{f(x + h) - f(x - h)}{2h} \qquad \text{（中心差分）}

で近似できる。このように、微分を近くの点での値の差で置き換える方法を\ :term:`差分法`\ という。2 つの近似の精度は、テイラー展開

.. math::

   f(x \pm h) = f(x) \pm h f'(x) + \frac{h^2}{2} f''(x) \pm \frac{h^3}{6} f'''(x) + \cdots

から分かる。これを代入すると

.. math::

   \frac{f(x + h) - f(x)}{h} &= f'(x) + \frac{h}{2} f''(x) + \cdots \\
   \frac{f(x + h) - f(x - h)}{2h} &= f'(x) + \frac{h^2}{6} f'''(x) + \cdots

となる。前進差分の誤差は :math:`h` に比例し、中心差分の誤差は :math:`h^2` に比例する。このように、テイラー展開を途中で打ち切ったことによる誤差を\ :term:`打ち切り誤差`\ といい、誤差が :math:`h^p` に比例するとき、その近似を :math:`p` 次の精度という。中心差分は 2 次の精度を持ち、:math:`h` を 1/10 にすると誤差はおよそ 1/100 になる。

ただし、:math:`h` をいくらでも小さくすればよいわけではない。コンピューターの浮動小数点数は約 16 桁の精度しか持たないので、ほとんど等しい 2 つの数の差をとると有効数字が失われる。この\ :term:`丸め誤差`\ はおよそ :math:`\epsilon / h`\ （:math:`\epsilon \approx 10^{-16}`）の大きさで、:math:`h` が小さいほど大きくなる。:numref:`fig-ch18-finite-difference` は、:math:`f(x) = \sin x` の :math:`x = 1` での微分係数を 2 つの方法で求めたときの誤差である。:math:`h` が大きい範囲では打ち切り誤差が支配的で、傾き 1 と傾き 2 の直線に沿って誤差が減る。:math:`h` が小さい範囲では丸め誤差が支配的になり、誤差はかえって増える。誤差が最も小さくなる :math:`h` は、前進差分では :math:`10^{-8}` 程度、中心差分では :math:`10^{-5}` 程度である。

.. figure:: ../build/figures/ch18_finite_difference.svg
   :name: fig-ch18-finite-difference
   :width: 75%
   :align: center

   前進差分と中心差分の誤差

.. literalinclude:: ../build/outputs/ch18_finite_difference.txt
   :language: text
   :caption: ch18_finite_difference.py の実行結果

:math:`f''(1) = -\sin 1 \approx -0.841`、:math:`f'''(1) = -\cos 1 \approx -0.540` なので、:math:`h = 0.1` での誤差の見積もりは、前進差分が :math:`0.1 / 2 \times 0.841 \approx 4.2 \times 10^{-2}`、中心差分が :math:`0.01 / 6 \times 0.540 \approx 9.0 \times 10^{-4}` であり、実行結果とよく一致する。

サンプルの全体：:download:`ch18_finite_difference.py <../examples/ch18_finite_difference.py>`

2 階微分は、2 つのテイラー展開を足して :math:`f'` と :math:`f'''` の項を消すと得られる。

.. math::

   f''(x) \approx \frac{f(x + h) - 2 f(x) + f(x - h)}{h^2}

この近似の誤差は :math:`h^2 f''''(x) / 12` 程度で、2 次の精度を持つ。

格子上の勾配・発散・回転
~~~~~~~~~~~~~~~~~~~~~~~~

2 次元の場を、間隔 :math:`h` の格子点 :math:`(x_i, y_j)` での値 :math:`f_{i,j} = f(x_i, y_j)` で表す。偏微分は、ほかの変数を固定して差分をとればよい。中心差分を使うと

.. math::

   \frac{\partial f}{\partial x} \approx \frac{f_{i+1,j} - f_{i-1,j}}{2h}, \qquad \frac{\partial f}{\partial y} \approx \frac{f_{i,j+1} - f_{i,j-1}}{2h}

である。勾配・発散・回転は偏微分の組み合わせなので、すべてこの近似から求められる。

NumPy の ``np.gradient`` は、配列の内部の点では中心差分で、端の点では片側の差分で微分を求める。``edge_order=2`` を指定すると、端の点でも 2 次の精度の差分を使う。注意が必要なのは配列の軸の順序である。``np.meshgrid(x, y)`` で作った 2 次元配列は、行（軸 0）が :math:`y`、列（軸 1）が :math:`x` に対応する。そのため :math:`x` での偏微分は ``axis=1``、:math:`y` での偏微分は ``axis=0`` で求める。

ラプラシアンは、2 階微分の近似を :math:`x` と :math:`y` について足し合わせた 5 点差分

.. math::

   \nabla^2 f \approx \frac{f_{i+1,j} + f_{i-1,j} + f_{i,j+1} + f_{i,j-1} - 4 f_{i,j}}{h^2} = \frac{4}{h^2} \left( \frac{f_{i+1,j} + f_{i-1,j} + f_{i,j+1} + f_{i,j-1}}{4} - f_{i,j} \right)

で求める。右辺の形から、:ref:`第 8 章 <ch08>`\ で見た「ラプラシアンは、まわりの平均とその点の値との差に比例する」という性質が、格子の上でもそのまま成り立っていることが分かる。

次のサンプルは、ベクトル場 :math:`\bm{F} = (\sin x \cos y, \ \sin x \sin y)` の発散と回転の :math:`z` 成分、スカラー場 :math:`f = \sin x \cos y` のラプラシアンを差分で求め、厳密な値

.. math::

   \nabla \cdot \bm{F} = \cos x \cos y + \sin x \cos y, \qquad (\nabla \times \bm{F})_z = \cos x \sin y + \sin x \sin y, \qquad \nabla^2 f = -2 \sin x \cos y

と比べる。

.. literalinclude:: ../examples/ch18_np_gradient.py
   :pyobject: divergence
   :lineno-match:
   :caption: ch18_np_gradient.py の divergence()

.. literalinclude:: ../examples/ch18_np_gradient.py
   :pyobject: curl_z
   :lineno-match:
   :caption: ch18_np_gradient.py の curl_z()

.. literalinclude:: ../examples/ch18_np_gradient.py
   :pyobject: laplacian
   :lineno-match:
   :caption: ch18_np_gradient.py の laplacian()

.. literalinclude:: ../build/outputs/ch18_np_gradient.txt
   :language: text
   :caption: ch18_np_gradient.py の実行結果

格子点の数 :math:`n` を 2 倍にすると間隔 :math:`h` はほぼ半分になり、誤差はおよそ 1/4 になる。どの量も 2 次の精度で求められていることが分かる。

サンプルの全体：:download:`ch18_np_gradient.py <../examples/ch18_np_gradient.py>`

ラプラス方程式を反復法で解く
----------------------------

離散化とヤコビ法
~~~~~~~~~~~~~~~~

:ref:`第 17 章 <ch17>`\ で見たように、定常状態の温度分布はラプラス方程式 :math:`\nabla^2 T = 0` を満たす。正方形の板の上の辺を温度 1、ほかの 3 辺を温度 0 に保ったときの温度分布を求めてみる。

5 点差分でラプラシアンを近似し、それが 0 になるという条件を書くと

.. math::

   T_{i,j} = \frac{T_{i+1,j} + T_{i-1,j} + T_{i,j+1} + T_{i,j-1}}{4}

となる。各点の温度が上下左右の 4 点の平均に等しい、という条件である。内部の格子点の数だけ未知数と式がある連立一次方程式なので、直接解くこともできるが、ここでは最も単純な反復法である\ :term:`ヤコビ法`\ を使う。適当な初期値から始めて、すべての内部の点の値を、1 つ前の段階の 4 点の平均で同時に置き換えることを繰り返す。

.. literalinclude:: ../examples/ch18_jacobi_laplace.py
   :pyobject: solve
   :lineno-match:
   :caption: ch18_jacobi_laplace.py の solve()

配列のスライスを使うと、内部のすべての点の更新を 1 行で書ける。``t[1:-1, 2:]`` は各点の右隣、``t[1:-1, :-2]`` は左隣の値を並べた配列である。

.. figure:: ../build/figures/ch18_jacobi_laplace.svg
   :name: fig-ch18-jacobi-laplace
   :width: 70%
   :align: center

   ヤコビ法で求めた定常温度分布と熱流束

:numref:`fig-ch18-jacobi-laplace` の矢印は、:ref:`第 17 章 <ch17>`\ のフーリエの法則に従う熱流束の向き :math:`-\nabla T` であり、等温線（白い線）に直交している。熱は温度 1 の辺から入り、温度 0 の 3 辺へ流れ出る。

.. literalinclude:: ../build/outputs/ch18_jacobi_laplace.txt
   :language: text
   :caption: ch18_jacobi_laplace.py の実行結果

板の中心の温度は、ちょうど 0.25 になるはずである。理由は次のとおりである。この問題を 90° ずつ回転させた 4 つの問題（温度 1 の辺が上、右、下、左にあるもの）を考えると、それぞれの解の和は、4 辺すべてが温度 1 の問題の解になる。その解はどこでも温度 1 である。中心は 4 つの問題で同じ位置にあり、対称性から 4 つの解の中心の温度は等しいので、それぞれ 1/4 である。この議論は差分で近似した方程式についてもそのまま成り立つので、数値解の中心の温度も 0.25 になる。

サンプルの全体：:download:`ch18_jacobi_laplace.py <../examples/ch18_jacobi_laplace.py>`

反復の止め方と速さ
~~~~~~~~~~~~~~~~~~

このサンプルでは、1 回の反復での変化の最大値が :math:`10^{-9}` より小さくなったら止めている。変化が小さいことは、誤差が小さいことと同じではない点に注意する。ヤコビ法は収束が遅いため、1 回の変化が小さくても、正しい解までの距離はその数百倍あることがある。実際、止める基準を :math:`10^{-7}` にすると、中心の温度は 0.249968 となり、基準の値よりずっと大きい誤差が残る。

ヤコビ法で必要な反復の回数は、1 辺の格子点の数 :math:`N` の 2 乗にほぼ比例して増える。格子を細かくすると急に遅くなるので、実用的には、更新した値をすぐに使うガウス・ザイデル法、それを加速した SOR 法、粗い格子と細かい格子を組み合わせるマルチグリッド法、共役勾配法などを使う。SciPy の ``scipy.sparse.linalg`` には、こうした大規模な連立一次方程式の解法が用意されている。

CG での法線
-----------

陰関数曲面と SDF
~~~~~~~~~~~~~~~~

CG で物体に陰影を付けるには、表面の各点での法線ベクトルが必要である。:ref:`第 5 章 <ch05>`\ で見たように、:math:`g(x, y, z) = 0` で表される曲面（陰関数曲面）の法線ベクトルは、勾配 :math:`\nabla g` の向きである。単位法線ベクトルは :math:`\bm{n} = \nabla g / |\nabla g|` で求める。

レイマーチングと呼ばれる描画の手法では、物体を\ :term:`符号付き距離関数`\ （SDF、signed distance function）で表すことが多い。SDF :math:`d(\bm{r})` は、点 :math:`\bm{r}` から物体の表面までの距離を、物体の外側では正、内側では負の符号を付けて表した関数である。物体の表面は等値面 :math:`d = 0` である。たとえば中心 :math:`\bm{c}`、半径 :math:`R` の球の SDF は :math:`d(\bm{r}) = |\bm{r} - \bm{c}| - R` で、その勾配は :math:`\nabla d = (\bm{r} - \bm{c}) / |\bm{r} - \bm{c}|` となり、確かに球の外向きの単位法線ベクトルになる。一般に SDF は :math:`|\nabla d| = 1` を満たすので、勾配がそのまま単位法線ベクトルになる。

複雑な形の SDF では勾配の式を求めるのが面倒なので、中心差分で数値的に求めることが多い。

.. code-block:: python
   :linenos:

   import numpy as np


   def sdf_normal(sdf, p, h=1e-4):
       """SDF の勾配を中心差分で求め、単位法線ベクトルを返す."""
       ex, ey, ez = np.eye(3) * h
       grad = np.array([
           sdf(p + ex) - sdf(p - ex),
           sdf(p + ey) - sdf(p - ey),
           sdf(p + ez) - sdf(p - ez),
       ]) / (2 * h)
       return grad / np.linalg.norm(grad)

GLSL などのシェーダーでも同じ考え方で、1 点の法線を求めるために SDF を 6 回（工夫すると 4 回）評価する。

ノーマルマップ
~~~~~~~~~~~~~~

細かい凹凸を持つ表面を、ポリゴンを細かく分割せずに表現する方法として、ノーマルマップがある。表面の高さの分布（ハイトマップ）\ :math:`z = H(x, y)` を考える。この曲面は :math:`g(x, y, z) = z - H(x, y) = 0` の等値面なので、法線ベクトルは

.. math::

   \nabla g = \left( -\frac{\partial H}{\partial x}, \ -\frac{\partial H}{\partial y}, \ 1 \right)

の向きである。各画素で偏微分を差分で求め、正規化した法線ベクトルの各成分 :math:`n_x, n_y, n_z \in [-1, 1]` を :math:`(n + 1) / 2` で :math:`[0, 1]` に移して RGB の色として保存した画像が\ :term:`ノーマルマップ`\ である。平らな部分の法線は :math:`(0, 0, 1)` なので、色は :math:`(0.5, 0.5, 1.0)` の青紫色になる。ノーマルマップの多くが青紫色に見えるのはこのためである。

描画するときは、ノーマルマップから読み出した法線 :math:`\bm{n}` と、光が来る向きの単位ベクトル :math:`\bm{l}` の内積 :math:`\max(\bm{n} \cdot \bm{l}, 0)` で明るさを決める（ランバート反射）。:numref:`fig-ch18-normal-map` は、2 つの山と 1 本の溝を持つハイトマップから、ノーマルマップと陰影を求めたものである。光は左上から当てている。

.. figure:: ../build/figures/ch18_normal_map.svg
   :name: fig-ch18-normal-map
   :width: 100%
   :align: center

   ハイトマップ、ノーマルマップ、法線による陰影

.. literalinclude:: ../examples/ch18_normal_map.py
   :pyobject: normals
   :lineno-match:
   :caption: ch18_normal_map.py の normals()

サンプルの全体：:download:`ch18_normal_map.py <../examples/ch18_normal_map.py>`

実際のノーマルマップは、表面に沿った局所的な座標系（接空間）での法線を保存することが多い。また、緑（:math:`y` 成分）の向きの約束がソフトウェアによって異なり、上下が反転していることがある。

カールノイズ
------------

発散のない流れを作る
~~~~~~~~~~~~~~~~~~~~

煙や炎、パーティクルの動きを、流体らしく見せたい場合がある。手軽な方法は、滑らかなランダムな関数（ノイズ）で速度の場を作り、パーティクルをその流れに乗せて動かすことである。しかし、2 つの独立なノイズをそのまま速度の :math:`x` 成分と :math:`y` 成分にすると、発散が 0 にならない。発散が正の場所からはパーティクルが散らばり、負の場所にはパーティクルが集まってしまい、水や空気のような非圧縮の流れには見えない。

そこで、:ref:`第 8 章 <ch08>`\ の公式 :math:`\nabla \cdot (\nabla \times \bm{\Psi}) = 0` を使う。どのようなベクトル場 :math:`\bm{\Psi}` でも、その回転の発散は 0 になる。したがって、ノイズで作った :math:`\bm{\Psi}` の回転を速度にすれば、発散のない流れが得られる。これを\ :term:`カールノイズ`\ という（Bridson らが 2007 年に提案した）。2 次元では、スカラーのノイズ :math:`\psi(x, y)` を :math:`\bm{\Psi} = (0, 0, \psi)` の :math:`z` 成分とみなすと

.. math::

   \bm{v} = \nabla \times \bm{\Psi} = \left( \frac{\partial \psi}{\partial y}, \ -\frac{\partial \psi}{\partial x} \right)

となる。実際、:math:`\nabla \cdot \bm{v} = \partial^2 \psi / \partial x \partial y - \partial^2 \psi / \partial y \partial x = 0` である。また :math:`\bm{v} \cdot \nabla \psi = \psi_y \psi_x - \psi_x \psi_y = 0` なので、速度は :math:`\psi` の等高線に沿う。この :math:`\psi` は、:ref:`第 16 章 <ch16>`\ のヘルムホルツ分解で現れた流れ関数と同じものである。3 次元では、3 つの独立なノイズを成分とするベクトル場 :math:`\bm{\Psi}` の回転を使う。

.. literalinclude:: ../examples/ch18_curl_noise.py
   :pyobject: curl_noise_velocity
   :lineno-match:
   :caption: ch18_curl_noise.py の curl_noise_velocity()

:numref:`fig-ch18-curl-noise` は、ノイズをそのまま速度にした流れ（左）とカールノイズの流れ（右）を比べたものである。背景の色は発散の値を表す。左の流れでは、赤い場所（発散が正）から流れが湧き出し、青い場所（発散が負）に流れが吸い込まれている。右の流れは発散がどこでも 0 で、流線は途切れることなく渦を巻きながら続いていく。

.. figure:: ../build/figures/ch18_curl_noise.svg
   :name: fig-ch18-curl-noise
   :width: 100%
   :align: center

   ノイズをそのまま速度にした流れとカールノイズの流れ

.. literalinclude:: ../build/outputs/ch18_curl_noise.txt
   :language: text
   :caption: ch18_curl_noise.py の実行結果

カールノイズの発散は、式の上では厳密に 0 である。実行結果で 0 にならないのは、格子上の値から差分で発散を求めたときの打ち切り誤差のためである。

サンプルの全体：:download:`ch18_curl_noise.py <../examples/ch18_curl_noise.py>`

Bridson らの論文では、物体の表面の近くで :math:`\psi` を 0 に近づけるように調整し、流れが物体を貫かずに回り込むようにする方法も示されている。

流体シミュレーションの圧力投影
------------------------------

ヘルムホルツ分解の応用
~~~~~~~~~~~~~~~~~~~~~~

ゲームや映像で使われる流体シミュレーションでは、時間を小さな刻み :math:`\Delta t` に分け、1 ステップごとに速度の場を更新する。流れによる運ばれ（移流）や外力の効果を加えて速度を更新すると、その途中の速度の場 :math:`\bm{w}` は、一般に発散が 0 にならない。そこで各ステップの最後に、:math:`\bm{w}` から発散のない成分だけを取り出す。この操作を\ :term:`圧力投影`\ という。

:ref:`第 16 章 <ch16>`\ のヘルムホルツ分解によれば、ベクトル場は発散のない成分と勾配の成分の和に分けられる。

.. math::

   \bm{w} = \bm{u} + \nabla p, \qquad \nabla \cdot \bm{u} = 0

両辺の発散をとると :math:`\nabla \cdot \bm{u} = 0` なので、:math:`p` はポアソン方程式

.. math::

   \nabla^2 p = \nabla \cdot \bm{w}

を満たす。これを解いて :math:`p` を求め、:math:`\bm{u} = \bm{w} - \nabla p` とすれば、発散のない速度の場が得られる。:math:`p` は物理的には圧力に :math:`\Delta t / \rho`\ （:math:`\rho` は流体の密度で、円柱座標の :math:`\rho` とは別）を掛けたものに相当し、圧力の勾配による力が流れの圧縮や膨張を打ち消す働きをしている。これが「圧力投影」という名前の由来である。

実際のシミュレーションでは、壁などの境界条件を考えながら、格子の上でポアソン方程式を解く。その解法には、この章で見たヤコビ法や、共役勾配法などが使われる。ここでは簡単のため、周期境界（右端と左端、上端と下端がつながっている）の正方形で考え、高速フーリエ変換（FFT）を使って解く。周期的な関数を :math:`e^{i(k_x x + k_y y)}` の重ね合わせで表すと、:math:`\partial / \partial x` は :math:`i k_x` を掛けること、ラプラシアンは :math:`-(k_x^2 + k_y^2)` を掛けることになるので、ポアソン方程式は各成分の割り算で解ける。

.. literalinclude:: ../examples/ch18_projection.py
   :pyobject: project
   :lineno-match:
   :caption: ch18_projection.py の project()

サンプルでは、発散のない場 :math:`\bm{u}`\ （流れ関数 :math:`\psi = \sin x \sin y` から作ったもの）に、勾配の場 :math:`\nabla \phi`\ （:math:`\phi = 0.8 \cos x \cos 2y`）を足した場を :math:`\bm{w}` とし、そこから :math:`\bm{u}` を取り出せるかを確かめる。

.. figure:: ../build/figures/ch18_projection.svg
   :name: fig-ch18-projection
   :width: 100%
   :align: center

   圧力投影によるベクトル場の分解

.. literalinclude:: ../build/outputs/ch18_projection.txt
   :language: text
   :caption: ch18_projection.py の実行結果

投影の後の発散は丸め誤差の程度まで小さくなり、取り出した場は元の :math:`\bm{u}` と一致している。:numref:`fig-ch18-projection` の右の場では、流れは 4 つの渦に分かれて回っており、どこにも湧き出しや吸い込みがない。

サンプルの全体：:download:`ch18_projection.py <../examples/ch18_projection.py>`

この章のまとめ
--------------

* 中心差分の誤差は :math:`h^2` に比例する。:math:`h` を小さくしすぎると丸め誤差が大きくなる。
* 格子上の勾配・発散・回転は ``np.gradient`` で求められる。5 点差分のラプラシアンは、まわりの平均との差に比例する。
* ラプラス方程式は、各点を 4 点の平均で置き換えるヤコビ法で解ける。変化が小さいことと誤差が小さいことは別である。
* CG では、陰関数曲面や SDF、ハイトマップの法線を勾配で求める。
* カールノイズは :math:`\nabla \cdot (\nabla \times \bm{\Psi}) = 0` を使って発散のない流れを作る。圧力投影はヘルムホルツ分解を使って速度の場から発散を取り除く。
