第 3 章 行列と行列の演算
========================

この章では、数を長方形に並べた行列と、その演算を扱う。特に、行列とベクトルの積を「列ベクトルの線形結合」として見る考え方は、これ以降のすべての章で使う。

行列
----

数を縦と横の長方形に並べたものを\ :term:`行列`\ という。横の並びを\ :term:`行`、縦の並びを\ :term:`列`\ と呼ぶ。:math:`m` 個の行と :math:`n` 個の列からなる行列を :math:`m` 行 :math:`n` 列の行列、または :math:`m \times n` 行列という。

.. math::

   A = \begin{pmatrix}
   a_{11} & a_{12} & \cdots & a_{1n} \\
   a_{21} & a_{22} & \cdots & a_{2n} \\
   \vdots & \vdots & \ddots & \vdots \\
   a_{m1} & a_{m2} & \cdots & a_{mn}
   \end{pmatrix}

:math:`a_{ij}` は :math:`i` 行 :math:`j` 列の\ :term:`成分`\ である。行と列の数が等しい :math:`n \times n` 行列を :math:`n` 次の\ :term:`正方行列`\ という。:math:`n` 次元の列ベクトルは :math:`n \times 1` 行列、行ベクトルは :math:`1 \times n` 行列とみなせる。

行列 :math:`A` の :math:`j` 番目の列を取り出したベクトルを :math:`\bm{a}_j` と書くと、行列は列ベクトルを横に並べたもの

.. math::

   A = \begin{pmatrix} \bm{a}_1 & \bm{a}_2 & \cdots & \bm{a}_n \end{pmatrix}

とみなせる。この見方は、行列とベクトルの積で重要になる。

和、スカラー倍、転置
--------------------

同じ大きさの行列の和とスカラー倍は、ベクトルと同じく成分ごとに計算する。

.. math::

   (A + B)_{ij} = a_{ij} + b_{ij}, \qquad (cA)_{ij} = c\,a_{ij}

行列 :math:`A` の行と列を入れ替えた行列を\ :term:`転置行列`\ といい、:math:`A^\top` と書く。:math:`m \times n` 行列の転置は :math:`n \times m` 行列になり、:math:`(A^\top)_{ij} = a_{ji}` である。

.. math::

   A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{pmatrix}, \qquad
   A^\top = \begin{pmatrix} 1 & 4 \\ 2 & 5 \\ 3 & 6 \end{pmatrix}

行列とベクトルの積
------------------

:math:`m \times n` 行列 :math:`A` と :math:`n` 次元のベクトル :math:`\bm{x}` の積 :math:`A\bm{x}` は、:math:`m` 次元のベクトルである。この積には、2 つの見方がある。:math:`A` と :math:`\bm{x}` を次のようにして、両方の見方で計算してみる。

.. math::

   A = \begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}, \qquad
   \bm{x} = \begin{pmatrix} 5 \\ 6 \end{pmatrix}

**見方 1：行との内積。**\ :math:`A\bm{x}` の :math:`i` 番目の成分は、:math:`A` の :math:`i` 行目と :math:`\bm{x}` の内積である。

.. math::

   A\bm{x} = \begin{pmatrix} 1 \cdot 5 + 2 \cdot 6 \\ 3 \cdot 5 + 4 \cdot 6 \end{pmatrix}
   = \begin{pmatrix} 17 \\ 39 \end{pmatrix}

**見方 2：列の線形結合。**\ :math:`A\bm{x}` は、:math:`A` の列ベクトルを、:math:`\bm{x}` の成分を係数として線形結合したものである。

.. math::

   A\bm{x} = x_1 \bm{a}_1 + x_2 \bm{a}_2
   = 5 \begin{pmatrix} 1 \\ 3 \end{pmatrix} + 6 \begin{pmatrix} 2 \\ 4 \end{pmatrix}
   = \begin{pmatrix} 17 \\ 39 \end{pmatrix}

手で計算するときは見方 1 が便利だが、意味を考えるときは見方 2 が役に立つ。例えば、「:math:`A\bm{x} = \bm{b}` を満たす :math:`\bm{x}` があるか」という問題は、見方 2 では「:math:`\bm{b}` を :math:`A` の列ベクトルの線形結合で表せるか」という問題になる（第 5 章、第 8 章）。また、:math:`A\bm{e}_1 = \bm{a}_1` のように、基本ベクトル :math:`\bm{e}_j`\ （:math:`j` 番目の成分だけが 1 で、他が 0 のベクトル）を掛けると :math:`j` 番目の列が取り出せる。これは第 4 章で、行列を線形写像として理解するときの鍵になる。

行列の積
--------

:math:`l \times m` 行列 :math:`A` と :math:`m \times n` 行列 :math:`B` の積 :math:`AB` は :math:`l \times n` 行列であり、その成分は

.. math::

   (AB)_{ij} = \sum_{k=1}^{m} a_{ik} b_{kj}

である。つまり、:math:`AB` の :math:`i` 行 :math:`j` 列の成分は、:math:`A` の :math:`i` 行目と :math:`B` の :math:`j` 列目の内積である。積が定義されるのは、:math:`A` の列の数と :math:`B` の行の数が等しいときだけである。

列で見ると、:math:`AB` の :math:`j` 列目は :math:`A` と :math:`B` の :math:`j` 列目の積 :math:`A\bm{b}_j` である。

.. math::

   AB = A \begin{pmatrix} \bm{b}_1 & \cdots & \bm{b}_n \end{pmatrix}
   = \begin{pmatrix} A\bm{b}_1 & \cdots & A\bm{b}_n \end{pmatrix}

行列の積には、次の性質がある。

* **結合法則が成り立つ。**\ :math:`(AB)C = A(BC)` なので、括弧を省略して :math:`ABC` と書ける。
* **分配法則が成り立つ。**\ :math:`A(B + C) = AB + AC`、:math:`(A + B)C = AC + BC`
* **交換法則は一般には成り立たない。**\ :math:`AB \ne BA` となるのが普通である。:math:`AB` が定義されても :math:`BA` が定義されないこともある。
* **転置の順序が逆になる。**\ :math:`(AB)^\top = B^\top A^\top`

交換法則が成り立たないことは、数の掛け算との大きな違いである。その理由は、第 4 章で行列の積を「変換の合成」として見るとよく分かる。

特殊な行列
----------

よく使う行列に、次のものがある。

.. list-table:: 特殊な行列
   :header-rows: 1
   :widths: 20 45 35

   * - 名前
     - 定義
     - 例（2 次または 3 次）
   * - :term:`単位行列`
     - 対角成分（:math:`a_{11}, a_{22}, \ldots`）がすべて 1 で、他が 0 の正方行列。:math:`I` または :math:`I_n` と書く。任意の行列 :math:`A` について :math:`AI = IA = A`
     - :math:`\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}`
   * - 零行列
     - すべての成分が 0 の行列。:math:`O` と書く
     - :math:`\begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}`
   * - :term:`対角行列`
     - 対角成分以外がすべて 0 の正方行列
     - :math:`\begin{pmatrix} 2 & 0 \\ 0 & 3 \end{pmatrix}`
   * - 上三角行列
     - 対角成分より下の成分がすべて 0 の正方行列（下三角行列も同様）
     - :math:`\begin{pmatrix} 1 & 2 & 3 \\ 0 & 4 & 5 \\ 0 & 0 & 6 \end{pmatrix}`
   * - :term:`対称行列`
     - :math:`A^\top = A` を満たす正方行列
     - :math:`\begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}`

対角行列を左から掛けると各行が、右から掛けると各列が、対角成分の倍数になる。三角行列は、第 5 章の連立一次方程式の解法で中心的な役割を果たす。対称行列は第 11 章で詳しく扱う。

NumPy で計算する
----------------

:numref:`list-ch03-matrix-ops` で、行列とベクトルの積を 2 つの見方で計算し、行列の積の性質を確かめる。

.. literalinclude:: ../examples/ch03_matrix_ops.py
   :pyobject: report
   :lineno-match:
   :caption: ch03_matrix_ops.py の report()
   :name: list-ch03-matrix-ops

.. literalinclude:: ../build/outputs/ch03_matrix_ops.txt
   :language: text
   :caption: ch03_matrix_ops.py の実行結果

行列 :math:`B = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}` を右から掛けると :math:`A` の列が入れ替わり、左から掛けると行が入れ替わる。そのため :math:`AB \ne BA` である。このように、単位行列の行（または列）を並べ替えた行列を\ :term:`置換行列`\ という。

``np.array_equal()`` は、2 つの配列の成分がすべて等しいかを調べる関数である。浮動小数点数の計算では丸め誤差があるので、一般には、誤差の範囲で等しいかを調べる ``np.allclose()`` を使う（第 13 章）。この例は整数の値だけを扱うので、誤差が生じない。

サンプルの全体：:download:`ch03_matrix_ops.py <../examples/ch03_matrix_ops.py>`

行列の積の計算量
----------------

:math:`n` 次の正方行列どうしの積は、:math:`n^2` 個の成分のそれぞれについて :math:`n` 回の掛け算と足し算を行うので、およそ :math:`n^3` 回の演算が必要になる。これを計算量 :math:`O(n^3)` と書く。:math:`n` が 10 倍になると、計算時間はおよそ 1000 倍になる。

NumPy の ``@`` は、BLAS と呼ばれる高度に最適化されたライブラリ（第 13 章）を呼び出すため、Python で 3 重のループを書くよりはるかに速い。行列の計算は、ループを書かず、できるだけ配列全体の演算として書くのがよい。

計算量の観点から、結合法則の使い方にも注意が要る。:math:`n \times n` 行列 :math:`A, B` と :math:`n` 次元のベクトル :math:`\bm{x}` について、:math:`(AB)\bm{x}` は行列どうしの積に :math:`O(n^3)` かかるが、:math:`A(B\bm{x})` は行列とベクトルの積を 2 回行うだけなので :math:`O(n^2)` で済む。結果は同じでも、計算の順序で計算量は大きく変わる。

この章のまとめ
--------------

* :math:`m \times n` 行列は、:math:`n` 本の :math:`m` 次元の列ベクトルを横に並べたものとみなせる。
* 行列とベクトルの積 :math:`A\bm{x}` は、:math:`A` の列ベクトルを :math:`\bm{x}` の成分で線形結合したものである。
* 行列の積は結合法則を満たすが、交換法則は一般に成り立たない。また、:math:`(AB)^\top = B^\top A^\top` である。
* 単位行列、対角行列、三角行列、対称行列などの特殊な行列がある。
* :math:`n` 次の正方行列の積の計算量は :math:`O(n^3)` である。
