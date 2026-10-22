第 11 章 対称行列と二次形式
===========================

工学で現れる行列には、対称行列が非常に多い。剛性行列、共分散行列、慣性テンソル、ヘッセ行列などである。対称行列の固有値は必ず実数で、固有ベクトルは互いに直交する。この章では、この性質（スペクトル定理）と、対称行列に対応する二次形式を説明し、正定値性による極値の判定に応用する。

スペクトル定理
--------------

:math:`A^\top = A` を満たす正方行列を対称行列という（第 3 章）。対称行列には、次の重要な性質がある。

.. important::

   **スペクトル定理。**\ :math:`n` 次の実対称行列 :math:`A` について、次が成り立つ。

   * 固有値はすべて実数である。
   * 異なる固有値に対する固有ベクトルは直交する。
   * 正規直交な固有ベクトルを :math:`n` 本選べる。したがって、直交行列 :math:`Q` と対角行列 :math:`\Lambda` で

     .. math::

        A = Q \Lambda Q^\top

     と対角化できる。

2 番目の性質は、次のように示せる。:math:`A\bm{v}_1 = \lambda_1 \bm{v}_1`、:math:`A\bm{v}_2 = \lambda_2 \bm{v}_2`\ （:math:`\lambda_1 \ne \lambda_2`）とすると、:math:`A^\top = A` から

.. math::

   \lambda_1 (\bm{v}_1 \cdot \bm{v}_2) = (A\bm{v}_1)^\top \bm{v}_2 = \bm{v}_1^\top A \bm{v}_2 = \lambda_2 (\bm{v}_1 \cdot \bm{v}_2)

なので、:math:`(\lambda_1 - \lambda_2)(\bm{v}_1 \cdot \bm{v}_2) = 0`、つまり :math:`\bm{v}_1 \cdot \bm{v}_2 = 0` である。

一般の行列の対角化 :math:`A = PDP^{-1}` では、逆行列 :math:`P^{-1}` が必要だった。対称行列では :math:`P` を直交行列 :math:`Q` に選べるので、:math:`Q^{-1} = Q^\top` となり、計算が簡単で数値的にも安定である。:math:`A = Q \Lambda Q^\top` を列ごとに書くと

.. math::

   A = \lambda_1 \bm{q}_1 \bm{q}_1^\top + \lambda_2 \bm{q}_2 \bm{q}_2^\top + \cdots + \lambda_n \bm{q}_n \bm{q}_n^\top

となる。:math:`\bm{q}_i \bm{q}_i^\top` は :math:`\bm{q}_i` 方向への射影行列（第 9 章）なので、対称行列は「直交する方向への射影を、固有値の重みで足し合わせたもの」である。これを\ :term:`スペクトル分解`\ という。

NumPy では、対称行列の固有値と固有ベクトルを ``np.linalg.eigh()`` で求める。``np.linalg.eig()`` より速く、固有値は実数の配列として小さい順に返り、固有ベクトルは正規直交になる。次の行列は、弦の振動や熱伝導の方程式を差分法で離散化したときに現れる行列である。

.. math::

   A = \begin{pmatrix} 2 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 2 \end{pmatrix}

.. literalinclude:: ../examples/ch11_spectral.py
   :pyobject: report
   :lineno-match:
   :caption: ch11_spectral.py の report()
   :name: list-ch11-spectral

.. literalinclude:: ../build/outputs/ch11_spectral.txt
   :language: text
   :caption: ch11_spectral.py の実行結果

固有値は :math:`2 - \sqrt{2}, 2, 2 + \sqrt{2}` であり、:math:`Q^\top Q = I`、:math:`Q \Lambda Q^\top = A` が確かめられる。コレスキー分解については後で説明する。

サンプルの全体：:download:`ch11_spectral.py <../examples/ch11_spectral.py>`

二次形式
--------

対称行列 :math:`A` とベクトル :math:`\bm{x}` から作られる数

.. math::

   q(\bm{x}) = \bm{x}^\top A \bm{x} = \sum_{i=1}^{n} \sum_{j=1}^{n} a_{ij} x_i x_j

を\ :term:`二次形式`\ という。2 次元では、:math:`A = \begin{pmatrix} a & b \\ b & c \end{pmatrix}` に対して :math:`q(x, y) = ax^2 + 2bxy + cy^2` であり、すべての項が 2 次の多項式である。逆に、どのような 2 次の同次多項式も、対称行列を使って二次形式で表せる。

二次形式は、エネルギーとしてよく現れる。ばねの弾性エネルギー :math:`\tfrac{1}{2}\bm{x}^\top K \bm{x}`\ （:math:`K` は剛性行列）、運動エネルギー :math:`\tfrac{1}{2}\dot{\bm{x}}^\top M \dot{\bm{x}}`\ （:math:`M` は質量行列）、回転体の運動エネルギー :math:`\tfrac{1}{2}\bm{\omega}^\top I \bm{\omega}`\ （:math:`I` は慣性テンソル）などである。

二次形式の主軸
~~~~~~~~~~~~~~

:math:`xy` の項があると、:math:`q(x, y) = 1` などの等高線がどのような図形か分かりにくい。スペクトル定理を使って :math:`A = Q \Lambda Q^\top` とし、新しい座標 :math:`\bm{y} = Q^\top \bm{x}`\ （固有ベクトルを基底とする座標）を使うと

.. math::

   q = \bm{x}^\top Q \Lambda Q^\top \bm{x} = \bm{y}^\top \Lambda \bm{y} = \lambda_1 y_1^2 + \lambda_2 y_2^2 + \cdots + \lambda_n y_n^2

となり、交差項が消える。:math:`Q` は回転（と反射）なので、これは「座標軸を固有ベクトルの方向に回すと、二次形式は 2 乗の和になる」ということである。固有ベクトルの方向を二次形式の\ :term:`主軸`\ という。

:numref:`fig-ch11-quadratic-form` は、3 つの対称行列について、二次形式の等高線と主軸（黒の矢印）を描いたものである。

.. _fig-ch11-quadratic-form:

.. figure:: ../build/figures/ch11_quadratic_form.svg
   :alt: 正定値、不定値、半正定値の対称行列の二次形式の等高線と、固有ベクトルの方向の主軸

   二次形式の等高線と主軸。左から正定値、不定値、半正定値

* 左（固有値 3, 1）：等高線は楕円で、主軸は楕円の長軸と短軸の方向である。:math:`q = 1` の楕円の半径は、各主軸の方向に :math:`1/\sqrt{\lambda_i}` なので、固有値の小さい方向に長く伸びる。
* 中（固有値 3, -1）：等高線は双曲線である。固有値が正の方向には値が増え、負の方向には減る。
* 右（固有値 2, 0）：固有値 0 の方向 :math:`(-1, 1)` には値が変わらないので、等高線は平行な直線になる。

サンプルの全体：:download:`ch11_quadratic_form.py <../examples/ch11_quadratic_form.py>`

正定値行列
----------

0 でないすべての :math:`\bm{x}` について :math:`\bm{x}^\top A \bm{x} > 0` となる対称行列 :math:`A` を\ :term:`正定値`\ 行列という。主軸の座標では :math:`q = \sum \lambda_i y_i^2` なので、次のように分類できる。

.. list-table:: 対称行列の分類
   :header-rows: 1
   :widths: 20 40 40

   * - 分類
     - 条件
     - 二次形式の形
   * - 正定値
     - 固有値がすべて正
     - 原点で最小になる「お椀」の形
   * - 半正定値
     - 固有値がすべて 0 以上
     - 原点で最小だが、値が変わらない方向がある
   * - 負定値
     - 固有値がすべて負
     - 原点で最大になる「山」の形
   * - 不定値
     - 正と負の固有値がある
     - 原点は鞍点（馬の鞍の形）

:math:`A^\top A` の形の行列（第 9 章の正規方程式や、第 14 章の共分散行列）は、:math:`\bm{x}^\top A^\top A \bm{x} = \|A\bm{x}\|^2 \ge 0` なので、必ず半正定値であり、:math:`A` の列が線形独立なら正定値である。また、構造物の剛性行列が正定値であることは、どのように変形させても弾性エネルギーが正になる、つまり構造物が安定であることを意味する。

コレスキー分解
~~~~~~~~~~~~~~

正定値行列 :math:`A` は、下三角行列 :math:`L`\ （対角成分が正）を使って

.. math::

   A = LL^\top

と分解できる。これを\ :term:`コレスキー分解`\ という。LU 分解の特別な場合で、計算量は LU 分解の約半分である。正定値行列を係数とする連立一次方程式（有限要素法の剛性方程式など）を解くのに使われる。また、コレスキー分解ができるかどうかで、行列が正定値かを判定できる。:numref:`list-ch11-spectral` の実行結果では、正定値の行列ではコレスキー分解ができ、不定値の行列では ``LinAlgError`` が送出されている。

多変数関数の極値
----------------

二次形式は、多変数関数の極値の判定に使われる。2 変数関数 :math:`f(x, y)` が点 :math:`\bm{a}` で勾配 0（:math:`\partial f / \partial x = \partial f / \partial y = 0`）になるとき、:math:`\bm{a}` の近くでのテイラー展開は

.. math::

   f(\bm{a} + \bm{h}) \approx f(\bm{a}) + \frac{1}{2}\bm{h}^\top H \bm{h}, \qquad
   H = \begin{pmatrix} f_{xx} & f_{xy} \\ f_{xy} & f_{yy} \end{pmatrix}

となる。:math:`H` は 2 階の偏導関数を並べた対称行列で、\ :term:`ヘッセ行列`\ という。:math:`f` の点 :math:`\bm{a}` の近くでの形は、二次形式 :math:`\bm{h}^\top H \bm{h}` で決まるので、次のように判定できる。

* :math:`H` が正定値なら、:math:`\bm{a}` は極小点である。
* :math:`H` が負定値なら、:math:`\bm{a}` は極大点である。
* :math:`H` が不定値なら、:math:`\bm{a}` は鞍点である。

例えば :math:`f(x, y) = x^2 + xy + y^2` は、原点で勾配 0 であり、:math:`H = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}` の固有値は 3 と 1（:numref:`fig-ch11-quadratic-form` の左の行列）なので、原点は極小点である。:math:`n` 変数でも同じであり、機械学習の損失関数の最小化などの最適化の理論の基礎になっている。

この章のまとめ
--------------

* 実対称行列の固有値は実数で、固有ベクトルは直交し、:math:`A = Q\Lambda Q^\top` と直交行列で対角化できる（スペクトル定理）。
* 対称行列の固有値と固有ベクトルは ``np.linalg.eigh()`` で求める。
* 二次形式 :math:`\bm{x}^\top A \bm{x}` は、固有ベクトルの方向（主軸）の座標では 2 乗の和 :math:`\sum \lambda_i y_i^2` になる。
* 固有値がすべて正の対称行列は正定値であり、コレスキー分解 :math:`A = LL^\top` ができる。
* ヘッセ行列が正定値なら極小、負定値なら極大、不定値なら鞍点である。
