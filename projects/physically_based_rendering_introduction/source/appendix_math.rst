付録 A 数学的準備
=================

本文で用いた数学的な道具をまとめる。

ベクトルの演算
--------------

3 次元ベクトル :math:`\mathbf{a} = (a_x, a_y, a_z)`, :math:`\mathbf{b} = (b_x, b_y, b_z)` について、次の演算を用いる。

内積
   :math:`\mathbf{a} \cdot \mathbf{b} = a_x b_x + a_y b_y + a_z b_z`。:math:`\mathbf{a}` と :math:`\mathbf{b}` がともに単位ベクトルなら、内積は 2 つのベクトルのなす角の余弦に等しい。本書では、法線と方向ベクトルの内積を角度の余弦として頻繁に用いる。

外積
   :math:`\mathbf{a} \times \mathbf{b} = (a_y b_z - a_z b_y, \; a_z b_x - a_x b_z, \; a_x b_y - a_y b_x)`。:math:`\mathbf{a}` と :math:`\mathbf{b}` の両方に垂直なベクトルになる。長方形の法線や、カメラの座標軸を求めるのに用いる。

正規化
   :math:`\mathbf{a} / \| \mathbf{a} \|`。向きを変えずに長さを 1 にする。ここで :math:`\| \mathbf{a} \| = \sqrt{\mathbf{a} \cdot \mathbf{a}}` である。

反射ベクトル
   単位ベクトル :math:`\omega` を、単位ベクトル :math:`\mathbf{m}` を軸として反射させた方向は :math:`2 (\omega \cdot \mathbf{m}) \mathbf{m} - \omega` である。ここで :math:`\omega` は反射面から外向きのベクトルとする。

球面座標と立体角
----------------

法線 :math:`\mathbf{n}` を :math:`z` 軸とする座標系で、方向を天頂角 :math:`\theta`\ （:math:`z` 軸からの角度）と方位角 :math:`\phi`\ （:math:`xy` 平面内での角度）で表す。

.. math::
   :label: spherical

   \omega = (\sin\theta \cos\phi, \; \sin\theta \sin\phi, \; \cos\theta)

単位球面上で、:math:`\theta` を :math:`d\theta`、:math:`\phi` を :math:`d\phi` だけ変化させたときにできる微小な領域を考える。:math:`\theta` 方向の辺の長さは :math:`d\theta`、:math:`\phi` 方向の辺の長さは、半径 :math:`\sin\theta` の円周上の弧なので :math:`\sin\theta \, d\phi` である。したがって、この領域の面積、すなわち微小な立体角は次のようになる。

.. math::
   :label: d-omega-derivation

   d\omega = \sin\theta \, d\theta \, d\phi

半球全体の立体角は次のように計算できる。

.. math::

   \int_{\Omega} d\omega = \int_0^{2\pi} \int_0^{\pi/2} \sin\theta \, d\theta \, d\phi = 2\pi \left[ -\cos\theta \right]_0^{\pi/2} = 2\pi

同様に、:math:`\cos\theta` で重み付けした半球の積分は次のとおりである。

.. math::

   \int_{\Omega} \cos\theta \, d\omega = \int_0^{2\pi} \int_0^{\pi/2} \cos\theta \sin\theta \, d\theta \, d\phi = 2\pi \left[ \frac{\sin^2\theta}{2} \right]_0^{\pi/2} = \pi

逆関数法による乱数の生成
------------------------

一様乱数から、指定した確率密度関数に従う乱数を作る基本的な方法が逆関数法である。確率密度関数 :math:`p(x)` の累積分布関数を :math:`P(x) = \int_{-\infty}^{x} p(t) \, dt` とする。区間 :math:`[0, 1)` の一様乱数 :math:`\xi` に対して :math:`X = P^{-1}(\xi)` とすると、:math:`X` は確率密度関数 :math:`p(x)` に従う。

コサイン重み付きサンプリングの導出
----------------------------------

逆関数法を使って、式 :eq:`cosine-sampling` を導出する。立体角に関する確率密度関数 :math:`p(\omega) = \cos\theta / \pi` を、:math:`d\omega = \sin\theta \, d\theta \, d\phi` を使って :math:`(\theta, \phi)` に関する確率密度関数に書き換えると、次のようになる。

.. math::

   p(\theta, \phi) = \frac{\cos\theta \sin\theta}{\pi}

これは :math:`\theta` の関数と :math:`\phi` の関数の積に分けられるので、:math:`\theta` と :math:`\phi` を独立に生成できる。

* :math:`\phi` について積分すると :math:`\theta` の確率密度関数 :math:`p(\theta) = 2 \cos\theta \sin\theta` が得られる。その累積分布関数は :math:`P(\theta) = \sin^2\theta` である。:math:`\sin^2\theta = \xi_1` とおくと :math:`\cos\theta = \sqrt{1 - \xi_1}` となる。
* :math:`\phi` は :math:`[0, 2\pi)` の一様分布に従うので、:math:`\phi = 2\pi \xi_2` とすればよい。

以上で式 :eq:`cosine-sampling` が得られた。:math:`1 - \xi_1` も、端点の扱いを除けば :math:`\xi_1` と同じ一様分布に従うので、:math:`\cos\theta = \sqrt{\xi_1}` としても同じ分布になる。

GGX のハーフベクトルのサンプリング
----------------------------------

パストレーサーで用いた、確率密度 :math:`D(\mathbf{h}) (\mathbf{n} \cdot \mathbf{h})` でハーフベクトルを生成する式も、同じ方法で導出できる。式 :eq:`ggx` を代入して :math:`\theta_h` の累積分布関数を求め、その逆関数をとると、次の式が得られる。

.. math::
   :label: ggx-sampling

   \cos\theta_h = \sqrt{\frac{1 - \xi_1}{1 + (\alpha^2 - 1)\xi_1}}, \qquad \phi_h = 2\pi \xi_2

このハーフベクトルで :math:`\omega_o` を反射させて :math:`\omega_i` を得る。このとき、:math:`\omega_i` の確率密度は、ハーフベクトルの確率密度に :math:`d\omega_h / d\omega_i = 1 / (4 \, \omega_o \cdot \mathbf{h})` を掛けたものになる。
