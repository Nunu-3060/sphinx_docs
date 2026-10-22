第 9 章 直交性と最小二乗法
==========================

互いに直交するベクトルの組は、計算が簡単で、数値的にも安定している。この章では、正規直交基底と直交行列を導入し、部分空間への正射影を一般化する。さらに、正射影を使って、解が存在しない連立一次方程式の「最もよい近似解」を求める最小二乗法を説明する。

正規直交基底
------------

どの 2 つも互いに直交し、それぞれのノルムが 1 であるベクトルの組を、\ :term:`正規直交系`\ という。正規直交系である基底を\ :term:`正規直交基底`\ という。:math:`\bm{q}_1, \ldots, \bm{q}_n` が正規直交系であることは、内積で次のように書ける。

.. math::

   \bm{q}_i \cdot \bm{q}_j = \begin{cases} 1 & (i = j) \\ 0 & (i \ne j) \end{cases}

標準基底は正規直交基底である。また、標準基底を回転したものも正規直交基底である。

正規直交基底の最大の利点は、座標が内積だけで求められることである。第 7 章では、基底 :math:`\bm{b}_1, \ldots, \bm{b}_n` に関する座標を、連立一次方程式を解いて求めた。正規直交基底 :math:`\bm{q}_1, \ldots, \bm{q}_n` なら、:math:`\bm{x} = c_1 \bm{q}_1 + \cdots + c_n \bm{q}_n` の両辺と :math:`\bm{q}_i` の内積を取ると、直交性から :math:`c_i` の項だけが残り

.. math::

   c_i = \bm{q}_i \cdot \bm{x}

となる。これは、第 2 章で述べた「単位ベクトルとの内積は、その方向の成分の大きさ」ということである。フーリエ級数（関数を三角関数の和で表す方法）の係数が積分（関数の内積）で求められるのも、三角関数が直交系をなすからである。

直交行列
--------

正規直交基底を列に並べた正方行列 :math:`Q = (\bm{q}_1 \ \cdots \ \bm{q}_n)` を\ :term:`直交行列`\ という。:math:`Q^\top Q` の :math:`(i, j)` 成分は :math:`\bm{q}_i \cdot \bm{q}_j` なので、直交行列は

.. math::

   Q^\top Q = I, \qquad \text{つまり} \qquad Q^{-1} = Q^\top

を満たす。逆行列が転置で求められるので、計算が非常に簡単である。

直交行列による変換は、ベクトルの長さと内積（したがって角度）を変えない。

.. math::

   \|Q\bm{x}\|^2 = (Q\bm{x})^\top (Q\bm{x}) = \bm{x}^\top Q^\top Q \bm{x} = \bm{x}^\top \bm{x} = \|\bm{x}\|^2

図形の形を変えない変換なので、直交行列は回転か、回転と反射の組み合わせを表す。:math:`\det Q = 1` なら回転、:math:`\det Q = -1` なら反射を含む。数値計算で直交行列が好まれるのは、長さを変えないので、丸め誤差を拡大しないからである。

部分空間への正射影
------------------

第 2 章では、ベクトル :math:`\bm{b}` を 1 本のベクトル :math:`\bm{a}` の方向に正射影した。これを、:math:`m \times n` 行列 :math:`A` の列空間（:math:`\bm{a}_1, \ldots, \bm{a}_n` が張る部分空間）への正射影に一般化する。

列空間の上の点 :math:`\bm{p} = A\hat{\bm{x}}` のうち、:math:`\bm{b}` に最も近いものを求めたい。:numref:`fig-ch09-projection-plane` のように、最も近い点は、誤差 :math:`\bm{e} = \bm{b} - \bm{p}` が列空間に垂直になる点である。

.. _fig-ch09-projection-plane:

.. figure:: ../build/figures/ch09_projection_plane.svg
   :alt: 3 次元空間のベクトル b を、a1 と a2 が張る平面に正射影した p と、平面に垂直な誤差 e
   :width: 60%

   平面への正射影。:math:`\bm{a}_1 = (1, 0, 1)`、:math:`\bm{a}_2 = (0, 1, 1)`、:math:`\bm{b} = (1, 2, 5)`

:math:`\bm{e}` が列空間に垂直であることは、:math:`\bm{e}` が :math:`A` のすべての列ベクトルと直交すること、つまり :math:`A^\top \bm{e} = \bm{0}` である（第 8 章の言葉では、:math:`\bm{e}` は左零空間にある）。:math:`\bm{e} = \bm{b} - A\hat{\bm{x}}` を代入すると、次の式が得られる。

.. math::

   A^\top A \hat{\bm{x}} = A^\top \bm{b}

これを\ :term:`正規方程式`\ という。:math:`A` の列ベクトルが線形独立なら :math:`A^\top A` は正則なので、:math:`\hat{\bm{x}} = (A^\top A)^{-1} A^\top \bm{b}` であり、正射影は

.. math::

   \bm{p} = A (A^\top A)^{-1} A^\top \bm{b} = P\bm{b}

である。:math:`P = A (A^\top A)^{-1} A^\top` を\ :term:`射影行列`\ という。射影行列には、:math:`P^2 = P`\ （射影したものをもう一度射影しても変わらない）、:math:`P^\top = P` という性質がある。:math:`A` が 1 列 :math:`\bm{a}` だけなら :math:`A^\top A = \bm{a} \cdot \bm{a}` は数になり、第 2 章の式 :math:`\bm{p} = (\bm{a} \cdot \bm{b} / \bm{a} \cdot \bm{a})\,\bm{a}` に一致する。

.. literalinclude:: ../examples/ch09_projection_matrix.py
   :pyobject: report
   :lineno-match:
   :caption: ch09_projection_matrix.py の report()

.. literalinclude:: ../build/outputs/ch09_projection_matrix.txt
   :language: text
   :caption: ch09_projection_matrix.py の実行結果

誤差 :math:`\bm{e} = (-2/3, -2/3, 2/3)` は、:math:`\bm{a}_1` とも :math:`\bm{a}_2` とも直交している。ここでは射影行列を示すために ``np.linalg.inv()`` を使ったが、:math:`\hat{\bm{x}}` だけが必要なら、:numref:`fig-ch09-projection-plane` を描くコードのように、正規方程式を ``np.linalg.solve()`` で解けばよい。

サンプルの全体：:download:`ch09_projection_matrix.py <../examples/ch09_projection_matrix.py>`、:download:`ch09_projection_plane.py <../examples/ch09_projection_plane.py>`

最小二乗法
----------

測定データ :math:`(x_1, y_1), \ldots, (x_m, y_m)` に、直線 :math:`y = c_0 + c_1 x` を当てはめたい。すべての点が直線の上にあれば

.. math::

   \underbrace{\begin{pmatrix} 1 & x_1 \\ 1 & x_2 \\ \vdots & \vdots \\ 1 & x_m \end{pmatrix}}_{A}
   \underbrace{\begin{pmatrix} c_0 \\ c_1 \end{pmatrix}}_{\bm{c}}
   = \underbrace{\begin{pmatrix} y_1 \\ y_2 \\ \vdots \\ y_m \end{pmatrix}}_{\bm{y}}

が成り立つ。しかし、測定には誤差があるので、点の数 :math:`m` が 2 より多いと、この方程式には一般に解がない（:math:`\bm{y}` が :math:`A` の列空間に入らない）。そこで、残差 :math:`\bm{y} - A\bm{c}` のノルムの 2 乗、つまり

.. math::

   \|\bm{y} - A\bm{c}\|^2 = \sum_{i=1}^{m} \bigl(y_i - (c_0 + c_1 x_i)\bigr)^2

を最小にする :math:`\bm{c}` を求める。これを\ :term:`最小二乗法`\ という。残差のノルムが最小になるのは、:math:`A\bm{c}` が :math:`\bm{y}` の列空間への正射影になるときなので、:math:`\bm{c}` は正規方程式 :math:`A^\top A \bm{c} = A^\top \bm{y}` の解である。

直線以外の関数も、係数について線形なら同じ方法で当てはめられる。例えば 2 次式 :math:`y = c_0 + c_1 x + c_2 x^2` なら、:math:`A` の列を :math:`1, x_i, x_i^2` にすればよい。:math:`x^2` が入っていても、未知数 :math:`c_0, c_1, c_2` については線形だからである。

:numref:`fig-ch09-least-squares` は、架空の測定データに直線と 2 次式を当てはめた結果である。左の図の赤い縦線が残差であり、その 2 乗の和が最小になっている。

.. _fig-ch09-least-squares:

.. figure:: ../build/figures/ch09_least_squares.svg
   :alt: 測定データに当てはめた直線と残差、別のデータに当てはめた 2 次式

   最小二乗法による直線（左）と 2 次式（右）の当てはめ

.. literalinclude:: ../examples/ch09_least_squares.py
   :pyobject: fit_polynomial
   :lineno-match:
   :caption: ch09_least_squares.py の fit_polynomial()

``np.vander()`` は、列が :math:`1, x, x^2, \ldots` の行列（ヴァンデルモンド行列）を作る関数である。

.. literalinclude:: ../build/outputs/ch09_least_squares.txt
   :language: text
   :caption: ch09_least_squares.py の実行結果

データは :math:`y = 1.5 + 0.8x` と :math:`y = 3 - 2x + 0.5x^2` に誤差を加えて作ったもので、求めた係数はそれに近い値になっている。

サンプルの全体：:download:`ch09_least_squares.py <../examples/ch09_least_squares.py>`

正規方程式は分かりやすいが、:math:`A^\top A` を作ると、第 13 章で扱う条件数が 2 乗になり、誤差が大きくなりやすい。実用では、次に述べる QR 分解か、第 12 章の特異値分解を使う ``np.linalg.lstsq()`` を使うのがよい。この例では、どちらの方法でも同じ係数が得られている。

グラム・シュミットの直交化と QR 分解
------------------------------------

線形独立なベクトルの組から、同じ空間を張る正規直交系を作る方法を、\ :term:`グラム・シュミットの直交化`\ という。手順は次のとおりである。

1. :math:`\bm{a}_1` を正規化して :math:`\bm{q}_1 = \bm{a}_1 / \|\bm{a}_1\|` とする。
2. :math:`\bm{a}_2` から :math:`\bm{q}_1` 方向の成分（正射影）を引いて :math:`\bm{v}_2 = \bm{a}_2 - (\bm{q}_1 \cdot \bm{a}_2)\,\bm{q}_1` とし、正規化して :math:`\bm{q}_2` とする。
3. :math:`\bm{a}_3` から :math:`\bm{q}_1` 方向と :math:`\bm{q}_2` 方向の成分を引いて正規化し、:math:`\bm{q}_3` とする。
4. 以下同様に、それまでに作った :math:`\bm{q}` の方向の成分を引いて正規化する。

.. literalinclude:: ../examples/ch09_gram_schmidt.py
   :pyobject: gram_schmidt
   :lineno-match:
   :caption: ch09_gram_schmidt.py の gram_schmidt()

この手順を行列で表すと、:math:`\bm{a}_j` は :math:`\bm{q}_1, \ldots, \bm{q}_j` の線形結合で書けるので

.. math::

   A = QR

となる。:math:`Q` は :math:`\bm{q}` を列に並べた行列（列が正規直交）、:math:`R = Q^\top A` は上三角行列である。これを\ :term:`QR 分解`\ という。

.. literalinclude:: ../build/outputs/ch09_gram_schmidt.txt
   :language: text
   :caption: ch09_gram_schmidt.py の実行結果

:math:`Q^\top Q` が単位行列になり、:math:`R` が上三角行列になっている。NumPy の ``np.linalg.qr()`` は、グラム・シュミットの直交化ではなく、より数値的に安定なハウスホルダー変換という方法で QR 分解を行う。:math:`Q` の列と :math:`R` の行の符号が反対になることがあるが（この例では 1 行目）、:math:`QR` は同じである。

サンプルの全体：:download:`ch09_gram_schmidt.py <../examples/ch09_gram_schmidt.py>`

QR 分解を使うと、最小二乗法の正規方程式 :math:`A^\top A \bm{c} = A^\top \bm{y}` は、:math:`A = QR` を代入して :math:`R^\top Q^\top Q R \bm{c} = R^\top Q^\top \bm{y}`、つまり :math:`R\bm{c} = Q^\top \bm{y}` になる。:math:`R` は上三角行列なので、後退代入で解ける。:math:`A^\top A` を作らないので、誤差が大きくなりにくい。

この章のまとめ
--------------

* 正規直交基底では、座標が内積 :math:`c_i = \bm{q}_i \cdot \bm{x}` で求められる。
* 直交行列は :math:`Q^{-1} = Q^\top` を満たし、長さと角度を変えない（回転と反射）。
* 列空間への正射影 :math:`\bm{p} = A\hat{\bm{x}}` は、正規方程式 :math:`A^\top A \hat{\bm{x}} = A^\top \bm{b}` で求められる。
* 最小二乗法は、残差の 2 乗の和を最小にする方法であり、データを列空間に正射影することにあたる。
* グラム・シュミットの直交化で、行列を :math:`A = QR` と分解できる。実用では ``np.linalg.lstsq()`` や QR 分解を使う。
