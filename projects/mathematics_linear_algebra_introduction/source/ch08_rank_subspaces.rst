第 8 章 ランクと 4 つの基本部分空間
====================================

この章では、行列の「実質的な大きさ」を表すランクを導入し、行列に付随する 4 つの部分空間を調べる。これにより、連立一次方程式 :math:`A\bm{x} = \bm{b}` がいつ解を持ち、解がどのような形をしているかが、正方行列に限らず完全に分かる。

ランク
------

:math:`m \times n` 行列 :math:`A` の列ベクトルのうち、線形独立なものの最大の本数を、:math:`A` の\ :term:`ランク`\ （階数）といい、:math:`\mathrm{rank}\,A` と書く。ランクは、列ベクトルが張る空間の次元でもある。

ランクは、行基本変形で求められる。行基本変形を繰り返して、次の形の行列にする。

* 各行の、最初の 0 でない成分（ピボット）は 1 である。
* ピボットは、下の行ほど右にある。
* ピボットのある列の、ピボット以外の成分はすべて 0 である。
* すべての成分が 0 の行は、一番下にまとめる。

この形の行列を\ :term:`被約階段行列`\ （reduced row echelon form、RREF）という。ピボットの個数がランクに等しい。例として、次の行列を考える。

.. math::

   A = \begin{pmatrix} 1 & 2 & 1 & 3 \\ 2 & 4 & 0 & 2 \\ 3 & 6 & 1 & 5 \end{pmatrix}

被約階段行列を求めるコードを :numref:`list-ch08-rref` に示す。

.. literalinclude:: ../examples/ch08_rank.py
   :pyobject: rref
   :lineno-match:
   :caption: ch08_rank.py の rref()
   :name: list-ch08-rref

浮動小数点数の計算では、0 になるはずの値が丸め誤差でわずかに 0 からずれる。そのため、絶対値が ``tol`` より小さい値を 0 とみなしている。ピボットには、その列で絶対値が最大の成分を選んでいる（第 13 章のピボット選択）。

.. literalinclude:: ../build/outputs/ch08_rank.txt
   :language: text
   :caption: ch08_rank.py の実行結果

被約階段行列は次のようになる。

.. math::

   R = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 0 & 1 & 2 \\ 0 & 0 & 0 & 0 \end{pmatrix}

ピボットは 1 列目と 3 列目にあり、ランクは 2 である。:math:`A` の 3 行目は 1 行目と 2 行目の和なので、実質的には 2 本の方程式しかない。

ランクについて、次の重要な事実がある。

* 行ベクトルのうち線形独立なものの最大の本数も、ランクに等しい（:math:`\mathrm{rank}\,A = \mathrm{rank}\,A^\top`）。
* したがって、:math:`m \times n` 行列のランクは :math:`m` 以下かつ :math:`n` 以下である。
* :math:`n` 次の正方行列について、:math:`\mathrm{rank}\,A = n` と :math:`\det A \ne 0` は同値である。

4 つの基本部分空間
------------------

:math:`m \times n` 行列 :math:`A` には、次の 4 つの部分空間が付随する。

.. list-table:: 行列の 4 つの基本部分空間
   :header-rows: 1
   :widths: 22 38 18 22

   * - 名前
     - 定義
     - どこにあるか
     - 次元
   * - :term:`列空間`
     - :math:`A` の列ベクトルが張る空間。:math:`A\bm{x}` の形で表せるベクトル全体
     - :math:`\mathbb{R}^m`
     - :math:`r`
   * - :term:`零空間`
     - :math:`A\bm{x} = \bm{0}` を満たす :math:`\bm{x}` 全体（核とも呼ぶ）
     - :math:`\mathbb{R}^n`
     - :math:`n - r`
   * - 行空間
     - :math:`A` の行ベクトルが張る空間（:math:`A^\top` の列空間）
     - :math:`\mathbb{R}^n`
     - :math:`r`
   * - 左零空間
     - :math:`\bm{y}^\top A = \bm{0}^\top` を満たす :math:`\bm{y}` 全体（:math:`A^\top` の零空間）
     - :math:`\mathbb{R}^m`
     - :math:`m - r`

ここで :math:`r = \mathrm{rank}\,A` である。列空間は、線形写像 :math:`\bm{x} \mapsto A\bm{x}` の行き先全体であり、\ :term:`像`\ とも呼ばれる。零空間は、:math:`A` で原点に潰れてしまうベクトル全体である。

4 つの部分空間の関係を :numref:`fig-ch08-subspaces` に示す。4 つの基本部分空間で行列を理解する見方は、Strang の教科書 [Strang2016]_ で詳しく解説されている。

.. _fig-ch08-subspaces:

.. graphviz::
   :caption: 行列の 4 つの基本部分空間の関係
   :alt: 定義域の行空間と零空間、値域の列空間と左零空間、行列 A による対応

   digraph subspaces {
       rankdir=LR;
       graph [fontname="Yu Gothic", nodesep=0.6, ranksep=1.6];
       node [fontname="Yu Gothic", shape=box, style="rounded,filled", fontsize=11, width=1.4];
       edge [fontname="Yu Gothic", fontsize=10];
       subgraph cluster_domain {
           label=<定義域 R<SUP>n</SUP>>;
           style=rounded;
           row [label="行空間\n次元 r", fillcolor="#cfe2f3"];
           null [label="零空間\n次元 n - r", fillcolor="#f4cccc"];
           {rank=same; row -> null [dir=none, style=dashed, label="直交"];}
       }
       subgraph cluster_codomain {
           label=<値域 R<SUP>m</SUP>>;
           style=rounded;
           col [label="列空間\n次元 r", fillcolor="#cfe2f3"];
           leftnull [label="左零空間\n次元 m - r", fillcolor="#f4cccc"];
           {rank=same; col -> leftnull [dir=none, style=dashed, label="直交"];}
       }
       zero [label="原点 0", shape=box, width=0.8, fillcolor="#eeeeee"];
       row -> col [label="A（1 対 1 に対応）"];
       null -> zero [label="A"];
   }

この図の要点は次のとおりである。

* **次元定理。**\ 定義域 :math:`\mathbb{R}^n` の次元 :math:`n` は、行空間の次元 :math:`r` と零空間の次元 :math:`n - r` に分かれる。つまり

  .. math::

     \mathrm{rank}\,A + \dim(\text{零空間}) = n

  が成り立つ。これを\ :term:`次元定理`\ （ランク・退化次数の定理）という。「:math:`n` 次元の入力のうち、:math:`n - r` 次元分が潰れて、:math:`r` 次元分が出力に残る」と読める。

* **直交性。**\ 零空間のベクトルは、行空間のどのベクトルとも直交する。:math:`A\bm{x} = \bm{0}` は「:math:`\bm{x}` と :math:`A` の各行の内積が 0」という意味だからである。同様に、左零空間は列空間と直交する。この直交性は、第 9 章の最小二乗法で重要になる。

上の例の行列 :math:`A`\ （:math:`m = 3`、:math:`n = 4`、:math:`r = 2`）では、零空間の次元は :math:`4 - 2 = 2`、左零空間の次元は :math:`3 - 2 = 1` である。実行結果の零空間の基底ベクトル :math:`(-2, 1, 0, 0)` と :math:`(-1, 0, -2, 1)` は、被約階段行列から次のように求めたものである。ピボットのない列（2 列目と 4 列目）に対応する変数 :math:`x_2, x_4` は自由に選べる（\ :term:`自由変数`\ ）。:math:`R\bm{x} = \bm{0}` は :math:`x_1 = -2x_2 - x_4`、:math:`x_3 = -2x_4` なので、:math:`(x_2, x_4) = (1, 0)` と :math:`(0, 1)` を代入すると 2 本の基底ベクトルが得られる。

.. literalinclude:: ../examples/ch08_rank.py
   :pyobject: null_space_basis
   :lineno-match:
   :caption: ch08_rank.py の null_space_basis()

実行結果の ``a @ x`` に表示される ``-0.`` は、丸め誤差による非常に小さな負の数である。左零空間の基底ベクトル :math:`\bm{y} = (1, 1, -1)` は「1 行目 + 2 行目 - 3 行目 = 0」という行の間の関係を表している。

サンプルの全体：:download:`ch08_rank.py <../examples/ch08_rank.py>`

解の存在と解の構造
------------------

4 つの部分空間を使うと、連立一次方程式 :math:`A\bm{x} = \bm{b}` について、次のことが分かる。

**解が存在する条件。**\ :math:`A\bm{x}` は列ベクトルの線形結合なので、解が存在するのは :math:`\bm{b}` が :math:`A` の列空間に含まれるときであり、そのときに限る。ランクで言えば、:math:`A` に :math:`\bm{b}` を加えた拡大係数行列 :math:`(A \mid \bm{b})` のランクが、:math:`A` のランクと等しいときである（:math:`\bm{b}` を加えても、線形独立な列が増えない）。

**解の構造。**\ 解が存在するとき、解の 1 つを :math:`\bm{x}_p` とする（\ :term:`特殊解`\ ）。:math:`\bm{x}_n` を零空間の任意のベクトルとすると、:math:`A(\bm{x}_p + \bm{x}_n) = \bm{b} + \bm{0} = \bm{b}` なので、:math:`\bm{x}_p + \bm{x}_n` も解である。逆に、任意の解 :math:`\bm{x}` について :math:`A(\bm{x} - \bm{x}_p) = \bm{0}` なので、:math:`\bm{x} - \bm{x}_p` は零空間に含まれる。したがって、解全体は

.. math::

   \bm{x} = \bm{x}_p + \bm{x}_n \qquad (\bm{x}_n \text{ は零空間の任意のベクトル})

と表される。これを\ :term:`一般解`\ という。一般解は「特殊解 + 同次方程式 :math:`A\bm{x} = \bm{0}` の解」である。この構造は、線形の微分方程式の一般解（特殊解 + 同次方程式の一般解）とまったく同じである。

:numref:`fig-ch08-solution-structure` は、1 本の方程式 :math:`x + 2y = 4`\ （:math:`A = (1 \ \ 2)`）の解の構造である。零空間は原点を通る直線 :math:`x + 2y = 0` で、基底ベクトルは :math:`\bm{n} = (-2, 1)` である。解の集合は、零空間を特殊解 :math:`\bm{x}_p = (4, 0)` だけ平行移動した直線になる。:math:`\bm{x}_p` に :math:`2\bm{n}` を加えた :math:`(0, 2)` も解である。

.. _fig-ch08-solution-structure:

.. figure:: ../build/figures/ch08_solution_structure.svg
   :alt: 零空間の直線と、それを特殊解だけ平行移動した解の集合の直線
   :width: 80%

   一般解 = 特殊解 + 同次方程式の解。点線の矢印は xp に 2n を加える操作

解の集合のうち、原点に最も近い点（ノルムが最小の解）:math:`(0.8, 1.6)` は、零空間と直交する方向、つまり行空間の中にある。ノルム最小の解は、第 12 章で扱う擬似逆行列で求められる。

サンプルの全体：:download:`ch08_solution_structure.py <../examples/ch08_solution_structure.py>`

まとめると、:math:`m \times n` 行列 :math:`A`\ （ランク :math:`r`）の連立一次方程式 :math:`A\bm{x} = \bm{b}` は、次のように分類できる。

.. list-table:: ランクによる連立一次方程式の分類
   :header-rows: 1
   :widths: 30 35 35

   * - ランク
     - 解の存在
     - 解の個数
   * - :math:`r = m = n`
     - 任意の :math:`\bm{b}` で存在する
     - ただ 1 つ
   * - :math:`r = m < n`
     - 任意の :math:`\bm{b}` で存在する
     - 無数（:math:`n - r` 次元分の自由度）
   * - :math:`r = n < m`
     - :math:`\bm{b}` が列空間にあるときだけ存在する
     - 存在すればただ 1 つ
   * - :math:`r < m` かつ :math:`r < n`
     - :math:`\bm{b}` が列空間にあるときだけ存在する
     - 存在すれば無数

3 番目の場合（方程式が未知数より多い）は、測定データの当てはめでよく現れる。測定には誤差があるので、:math:`\bm{b}` は通常、列空間に入らず、厳密な解は存在しない。そこで、誤差が最小になる :math:`\bm{x}` を求めるのが、第 9 章の最小二乗法である。

この章のまとめ
--------------

* ランクは、線形独立な列ベクトル（行ベクトル）の最大の本数であり、被約階段行列のピボットの個数として求められる。
* 行列には、列空間、零空間、行空間、左零空間の 4 つの基本部分空間が付随する。
* 次元定理：ランク + 零空間の次元 = 列の数。
* :math:`A\bm{x} = \bm{b}` の解は、:math:`\bm{b}` が列空間にあるときに存在し、一般解は「特殊解 + 零空間のベクトル」である。
