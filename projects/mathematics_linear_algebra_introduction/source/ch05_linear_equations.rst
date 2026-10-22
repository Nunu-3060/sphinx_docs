第 5 章 連立一次方程式
======================

工学の問題を数式にすると、多くの場合、連立一次方程式になる。この章では、連立一次方程式を行列で表し、図による 2 つの見方を示した後、コンピューターでも使われる解法であるガウスの消去法と LU 分解を説明する。最後に、電気回路の電流を求める例を示す。

行列による表示
--------------

次の連立一次方程式を考える。

.. math::

   \begin{aligned}
   2x - y &= 1 \\
   x + y &= 5
   \end{aligned}

係数を並べた行列 :math:`A`、未知数のベクトル :math:`\bm{x}`、右辺のベクトル :math:`\bm{b}` を使うと、この方程式は :math:`A\bm{x} = \bm{b}` と書ける。

.. math::

   \underbrace{\begin{pmatrix} 2 & -1 \\ 1 & 1 \end{pmatrix}}_{A}
   \underbrace{\begin{pmatrix} x \\ y \end{pmatrix}}_{\bm{x}}
   = \underbrace{\begin{pmatrix} 1 \\ 5 \end{pmatrix}}_{\bm{b}}

:math:`A` を\ :term:`係数行列`\ という。未知数が 1000 個あっても、方程式は同じ :math:`A\bm{x} = \bm{b}` の形で書ける。

2 つの見方
----------

第 3 章で、行列とベクトルの積に 2 つの見方があることを示した。連立一次方程式にも、それに対応する 2 つの見方がある（:numref:`fig-ch05-two-views`）。

.. _fig-ch05-two-views:

.. figure:: ../build/figures/ch05_two_views.svg
   :alt: 2 本の直線の交点として解を表した図と、列ベクトルの線形結合として右辺を表した図

   連立一次方程式の行の見方（左）と列の見方（右）

**行の見方。**\ 各方程式（行列の各行）は、平面上の直線を表す。解は、すべての直線が通る点、つまり交点である。この例では、2 本の直線 :math:`2x - y = 1` と :math:`x + y = 5` の交点 :math:`(2, 3)` が解になる。3 元の方程式なら、各方程式は 3 次元空間の平面を表し、解は 3 枚の平面の交点である。

**列の見方。**\ 方程式は、右辺 :math:`\bm{b}` を、係数行列の列ベクトルの線形結合で表す問題である。

.. math::

   x \begin{pmatrix} 2 \\ 1 \end{pmatrix} + y \begin{pmatrix} -1 \\ 1 \end{pmatrix} = \begin{pmatrix} 1 \\ 5 \end{pmatrix}

右の図のように、:math:`\bm{a}_1` を 2 倍し、:math:`\bm{a}_2` を 3 倍してつなぐと :math:`\bm{b}` に着く。解 :math:`x = 2`、:math:`y = 3` は、その係数である。

行の見方は図が描きやすいが、未知数が増えると扱いにくい。列の見方は、解が存在するかどうかを考えるときに威力を発揮する（第 8 章）。

解の個数
--------

2 元の連立一次方程式を行の見方で考えると、解の個数には 3 つの場合がある。

.. list-table:: 未知数が 2 個の連立一次方程式の解の個数
   :header-rows: 1
   :widths: 25 35 40

   * - 直線の位置関係
     - 解
     - 例
   * - 1 点で交わる
     - ただ 1 つ
     - :math:`2x - y = 1,\ x + y = 5`
   * - 平行で、一致しない
     - 存在しない
     - :math:`x + y = 1,\ x + y = 2`
   * - 一致する
     - 無数にある（直線上のすべての点）
     - :math:`x + y = 1,\ 2x + 2y = 2`

「解が 2 つだけある」ということは起こらない。2 つの解 :math:`\bm{x}_1, \bm{x}_2` があれば、:math:`A(t\bm{x}_1 + (1 - t)\bm{x}_2) = t\bm{b} + (1 - t)\bm{b} = \bm{b}` なので、2 点を結ぶ直線上のすべての点が解になるからである。未知数がいくつあっても、連立一次方程式の解は「ただ 1 つ」「存在しない」「無数にある」のいずれかである。どの場合になるかは、第 6 章の行列式と第 8 章のランクで判定できる。

ガウスの消去法
--------------

連立一次方程式を解く基本的な方法は、中学校で学ぶ加減法を系統的に行う\ :term:`ガウスの消去法`\ である。次の 3 元連立一次方程式を例に説明する。

.. math::

   \begin{aligned}
   2x + y - z &= 8 \\
   -3x - y + 2z &= -11 \\
   -2x + y + 2z &= -3
   \end{aligned}

係数行列と右辺を並べた行列 :math:`(A \mid \bm{b})` を\ :term:`拡大係数行列`\ という。

.. math::

   \left(\begin{array}{ccc|c}
   2 & 1 & -1 & 8 \\
   -3 & -1 & 2 & -11 \\
   -2 & 1 & 2 & -3
   \end{array}\right)

消去法では、次の 3 つの操作を使う。これらを\ :term:`行基本変形`\ という。どの操作も、方程式の解を変えない。

1. ある行に、別の行の定数倍を加える。
2. 2 つの行を入れ替える。
3. ある行に、0 でない数を掛ける。

**前進消去。**\ まず、1 行目を使って、2 行目と 3 行目の 1 列目を 0 にする。2 行目に 1 行目の 3/2 倍を加え、3 行目に 1 行目を加える。

.. math::

   \left(\begin{array}{ccc|c}
   2 & 1 & -1 & 8 \\
   0 & 0.5 & 0.5 & 1 \\
   0 & 2 & 1 & 5
   \end{array}\right)

次に、2 行目を使って、3 行目の 2 列目を 0 にする。3 行目から 2 行目の 4 倍を引く。

.. math::

   \left(\begin{array}{ccc|c}
   2 & 1 & -1 & 8 \\
   0 & 0.5 & 0.5 & 1 \\
   0 & 0 & -1 & 1
   \end{array}\right)

係数行列の部分が上三角行列になった。消去に使った対角成分（2、0.5、-1）を\ :term:`ピボット`\ という。

**後退代入。**\ 下の行から順に未知数を求める。3 行目から :math:`-z = 1` なので :math:`z = -1`。2 行目 :math:`0.5y + 0.5z = 1` に代入して :math:`y = 3`。1 行目 :math:`2x + y - z = 8` に代入して :math:`x = 2` である。

この手順を :numref:`list-ch05-gauss` に示す。

.. literalinclude:: ../examples/ch05_gauss.py
   :pyobject: gaussian_elimination
   :lineno-match:
   :caption: ch05_gauss.py の gaussian_elimination()
   :name: list-ch05-gauss

``m[i] -= factor * m[k]`` が「行 :math:`i` から行 :math:`k` の定数倍を引く」操作である。NumPy では行全体を 1 つのベクトルとして扱えるので、列についてのループを書かずに済む。引数 ``pivoting`` は、第 13 章で説明するピボット選択を行うかどうかの指定であり、ここでは使わない。実行結果は次のとおりで、手計算と一致する。

.. literalinclude:: ../build/outputs/ch05_gauss.txt
   :language: text
   :caption: ch05_gauss.py の実行結果

サンプルの全体：:download:`ch05_gauss.py <../examples/ch05_gauss.py>`

途中でピボットが 0 になった場合は、下の行と入れ替えてから消去を続ける。どの行と入れ替えても 0 にしかならない場合は、解がただ 1 つには定まらない（解が存在しないか、無数にある）。

消去法の計算量は、前進消去がおよそ :math:`\tfrac{2}{3}n^3` 回の演算、後退代入がおよそ :math:`n^2` 回の演算である。未知数が 1000 個なら約 7 億回であり、現在のコンピューターでは 1 秒もかからない。

LU 分解
-------

同じ係数行列 :math:`A` で、右辺 :math:`\bm{b}` だけが異なる方程式を何度も解くことがある。例えば、構造物の解析で荷重の条件を変える場合や、回路の解析で電源の電圧を変える場合である。毎回消去法をやり直すと、:math:`O(n^3)` の前進消去を繰り返すことになり、無駄が大きい。

前進消去の計算は、右辺に依存しない。そこで、消去に使った倍率を記録しておく。上の例では、2 行目の消去に -1.5（1 行目の -1.5 倍を引いた）、3 行目に -1 と 4 を使った。この倍率を対角成分 1 の下三角行列 :math:`L` に並べ、前進消去の結果の上三角行列を :math:`U` とすると、:math:`A = LU` が成り立つ。

.. math::

   \underbrace{\begin{pmatrix} 2 & 1 & -1 \\ -3 & -1 & 2 \\ -2 & 1 & 2 \end{pmatrix}}_{A}
   = \underbrace{\begin{pmatrix} 1 & 0 & 0 \\ -1.5 & 1 & 0 \\ -1 & 4 & 1 \end{pmatrix}}_{L}
   \underbrace{\begin{pmatrix} 2 & 1 & -1 \\ 0 & 0.5 & 0.5 \\ 0 & 0 & -1 \end{pmatrix}}_{U}

これを\ :term:`LU 分解`\ という。:math:`A = LU` なら、:math:`A\bm{x} = \bm{b}` は :math:`L(U\bm{x}) = \bm{b}` なので、:math:`\bm{y} = U\bm{x}` とおいて、次の 2 段階で解ける。

1. :math:`L\bm{y} = \bm{b}` を上から順に解く（前進代入）。
2. :math:`U\bm{x} = \bm{y}` を下から順に解く（後退代入）。

三角行列の方程式は :math:`O(n^2)` で解けるので、分解を一度行えば、右辺ごとの計算は :math:`O(n^2)` で済む。

.. literalinclude:: ../examples/ch05_lu.py
   :pyobject: lu_decompose
   :lineno-match:
   :caption: ch05_lu.py の lu_decompose()

.. literalinclude:: ../build/outputs/ch05_lu.txt
   :language: text
   :caption: ch05_lu.py の実行結果

1 つ目の右辺の解は、消去法の結果と一致している。2 つ目の右辺 :math:`\bm{b} = (1, 0, 0)` の解は、第 6 章で扱う逆行列 :math:`A^{-1}` の 1 列目になる。

サンプルの全体：:download:`ch05_lu.py <../examples/ch05_lu.py>`

このサンプルは説明のため、ピボット選択を行っていない。実用のライブラリ（SciPy の ``scipy.linalg.lu_factor()`` など）は、行の入れ替えを記録する置換行列 :math:`P` を含めた :math:`PA = LU` の形で分解する。

例：電気回路の電流
------------------

:numref:`fig-ch05-circuit` の回路に流れる電流を求める。電源の電圧は :math:`E = 10` V、抵抗は :math:`R_1 = 2` Ω、:math:`R_2 = R_3 = 4` Ω である。

.. _fig-ch05-circuit:

.. figure:: ../build/figures/ch05_circuit.svg
   :alt: 電源と抵抗 R1 を直列につなぎ、その先に抵抗 R2 と R3 を並列につないだ回路
   :width: 70%

   抵抗の回路と電流の向き

キルヒホッフの法則から、電流 :math:`I_1, I_2, I_3` について次の式が成り立つ。

* 電流の法則（上の節点に流れ込む電流と流れ出す電流は等しい）：:math:`I_1 = I_2 + I_3`
* 電圧の法則（電源、:math:`R_1`、:math:`R_2` を通る閉路）：:math:`R_1 I_1 + R_2 I_2 = E`
* 電圧の法則（:math:`R_2` と :math:`R_3` を通る閉路）：:math:`R_2 I_2 - R_3 I_3 = 0`

行列で表すと次のようになる。

.. math::

   \begin{pmatrix} 1 & -1 & -1 \\ R_1 & R_2 & 0 \\ 0 & R_2 & -R_3 \end{pmatrix}
   \begin{pmatrix} I_1 \\ I_2 \\ I_3 \end{pmatrix}
   = \begin{pmatrix} 0 \\ E \\ 0 \end{pmatrix}

実用の計算では、消去法を自分で書かず、NumPy の ``np.linalg.solve()`` を使う。内部では、ピボット選択付きの LU 分解（LAPACK というライブラリ）が使われる。

.. literalinclude:: ../examples/ch05_circuit.py
   :pyobject: report
   :lineno-match:
   :caption: ch05_circuit.py の report()

.. literalinclude:: ../build/outputs/ch05_circuit.txt
   :language: text
   :caption: ch05_circuit.py の実行結果

:math:`R_2` と :math:`R_3` の並列の合成抵抗は 2 Ω なので、回路全体の抵抗は 4 Ω であり、:math:`I_1 = 10/4 = 2.5` A になる。これは計算結果と一致する。この程度の回路なら合成抵抗で解けるが、回路が複雑になると、連立一次方程式として解くほうが確実である。回路シミュレーター（SPICE など）は、節点の電圧を未知数とする大規模な連立一次方程式を解いている。

サンプルの全体：:download:`ch05_circuit.py <../examples/ch05_circuit.py>`

この章のまとめ
--------------

* 連立一次方程式は :math:`A\bm{x} = \bm{b}` と書ける。
* 行の見方では解は直線（平面）の交点であり、列の見方では解は :math:`\bm{b}` を列ベクトルの線形結合で表す係数である。
* 解は「ただ 1 つ」「存在しない」「無数にある」のいずれかである。
* ガウスの消去法は、前進消去で上三角行列を作り、後退代入で解を求める。計算量は :math:`O(n^3)` である。
* LU 分解 :math:`A = LU` をしておけば、右辺を変えて何度も解くときの計算が :math:`O(n^2)` で済む。
* 実用の計算では ``np.linalg.solve()`` を使う。
