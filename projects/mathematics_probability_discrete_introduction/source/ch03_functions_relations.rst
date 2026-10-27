第 3 章 写像と関係
==================

プログラムの関数は、入力を受け取って出力を 1 つ返す。数学でこれに対応する概念が写像である。また、「等しい」「以下である」「割り切る」のように 2 つのものの間に成り立つ性質は、関係として統一的に扱える。本章では写像と関係を学び、第 4 章の数え上げで使う「全単射による個数の比較」を準備する。

写像
----

写像の定義
~~~~~~~~~~

集合 :math:`A` の各要素 :math:`a` に対して、集合 :math:`B` の要素をちょうど 1 つ対応させる規則 :math:`f` を、:math:`A` から :math:`B` への\ :term:`写像`\ といい、:math:`f\colon A \to B` と書く。:math:`a` に対応する要素を :math:`f(a)` と書き、:math:`a` の\ **像**\ という。:math:`A` を\ **定義域**、:math:`B` を\ **終域**\ という。また、:math:`f(A) = \{f(a) \mid a \in A\}` を :math:`f` の\ **値域**\ という。値域は終域の部分集合であるが、一般には終域と一致しない。

本書では、終域が数の集合である写像を\ **関数**\ とも呼ぶ。

単射・全射・全単射
~~~~~~~~~~~~~~~~~~

写像 :math:`f\colon A \to B` について、次の性質を定める。

* :term:`単射`：:math:`a \ne a'` ならば :math:`f(a) \ne f(a')`。すなわち、異なる要素は異なる要素に移る。
* :term:`全射`：任意の :math:`b \in B` に対して :math:`f(a) = b` となる :math:`a \in A` が存在する。すなわち、値域が終域に一致する。
* :term:`全単射`：単射かつ全射である。

:numref:`fig-ch03-maps` に、それぞれの例を示す。

.. _fig-ch03-maps:

.. graphviz::
   :caption: 単射・全射・全単射の例（左側の集合が定義域、右側の集合が終域）
   :align: center

   digraph maps {
       rankdir=LR;
       node [shape=circle, width=0.35, fixedsize=true, fontsize=11];
       edge [arrowsize=0.6];
       subgraph cluster_inj {
           label="単射だが全射でない"; style=rounded; fontsize=11;
           subgraph cluster_inj_a { label=""; style=dashed; i_a1 [label="1"]; i_a2 [label="2"]; }
           subgraph cluster_inj_b { label=""; style=dashed; i_b1 [label="a"]; i_b2 [label="b"]; i_b3 [label="c"]; }
           i_a1 -> i_b1; i_a2 -> i_b3;
       }
       subgraph cluster_sur {
           label="全射だが単射でない"; style=rounded; fontsize=11;
           subgraph cluster_sur_a { label=""; style=dashed; s_a1 [label="1"]; s_a2 [label="2"]; s_a3 [label="3"]; }
           subgraph cluster_sur_b { label=""; style=dashed; s_b1 [label="a"]; s_b2 [label="b"]; }
           s_a1 -> s_b1; s_a2 -> s_b1; s_a3 -> s_b2;
       }
       subgraph cluster_bij {
           label="全単射"; style=rounded; fontsize=11;
           subgraph cluster_bij_a { label=""; style=dashed; b_a1 [label="1"]; b_a2 [label="2"]; b_a3 [label="3"]; }
           subgraph cluster_bij_b { label=""; style=dashed; b_b1 [label="a"]; b_b2 [label="b"]; b_b3 [label="c"]; }
           b_a1 -> b_b2; b_a2 -> b_b3; b_a3 -> b_b1;
       }
   }

有限集合 :math:`A, B` について、次が成り立つ。

* 単射 :math:`f\colon A \to B` が存在するならば :math:`|A| \le |B|`
* 全射 :math:`f\colon A \to B` が存在するならば :math:`|A| \ge |B|`
* 全単射 :math:`f\colon A \to B` が存在するならば :math:`|A| = |B|`

最後の性質は、数え上げで非常に役立つ。数えにくい集合 :math:`A` があっても、数えやすい集合 :math:`B` との全単射を作れれば :math:`|A| = |B|` として数えられる。第 2 章で見た「部分集合と :math:`n` ビットの整数の対応」は、まさにこの考え方である。また、1 つ目の性質の対偶「:math:`|A| > |B|` ならば単射は存在しない」は、第 4 章で扱う鳩の巣原理そのものである。

合成写像と逆写像
~~~~~~~~~~~~~~~~

写像 :math:`f\colon A \to B` と :math:`g\colon B \to C` に対して、:math:`(g \circ f)(a) = g(f(a))` で定まる写像 :math:`g \circ f\colon A \to C` を\ **合成写像**\ という。プログラムでいえば、関数の呼び出しを入れ子にすることに当たる。

:math:`f` が全単射のとき、各 :math:`b \in B` に対して :math:`f(a) = b` となる :math:`a` がただ 1 つ存在する。この :math:`a` を :math:`b` に対応させる写像を :math:`f` の\ **逆写像**\ といい、:math:`f^{-1}\colon B \to A` と書く。:math:`f^{-1} \circ f` は :math:`A` 上の恒等写像（各要素をそれ自身に移す写像）になる。

関係
----

関係の定義
~~~~~~~~~~

集合 :math:`A` 上の\ **関係** :math:`R` とは、直積 :math:`A \times A` の部分集合のことである。:math:`(a, b) \in R` のとき :math:`a \mathrel{R} b` と書き、「:math:`a` と :math:`b` は関係 :math:`R` にある」という。たとえば整数の大小関係 :math:`\le` は、:math:`a \le b` を満たす順序対 :math:`(a, b)` 全体の集合と考えられる。

関係 :math:`R` について、次の性質を考える。

.. list-table:: 関係の性質
   :header-rows: 1
   :widths: 20 80

   * - 性質
     - 定義
   * - 反射律
     - すべての :math:`a \in A` について :math:`a \mathrel{R} a`
   * - 対称律
     - :math:`a \mathrel{R} b` ならば :math:`b \mathrel{R} a`
   * - 反対称律
     - :math:`a \mathrel{R} b` かつ :math:`b \mathrel{R} a` ならば :math:`a = b`
   * - 推移律
     - :math:`a \mathrel{R} b` かつ :math:`b \mathrel{R} c` ならば :math:`a \mathrel{R} c`

同値関係と同値類
~~~~~~~~~~~~~~~~

反射律・対称律・推移律を満たす関係を\ :term:`同値関係`\ という。同値関係は「ある観点で同じとみなせる」ことを表す。

代表例は、正の整数 :math:`m` を法とする\ **合同関係**\ である。整数 :math:`a, b` について、:math:`a - b` が :math:`m` で割り切れるとき :math:`a \equiv b \pmod{m}` と書く。これは「:math:`m` で割った余りが等しい」ことと同じであり、同値関係になる。

同値関係 :math:`\sim` について、要素 :math:`a` と同値な要素全体の集合 :math:`[a] = \{b \in A \mid a \sim b\}` を :math:`a` の\ **同値類**\ という。同値類について、次の性質が成り立つ。

* 任意の 2 つの同値類は、一致するか互いに素であるかのどちらかである。
* すべての同値類の和集合は :math:`A` に一致する。

つまり、同値関係は集合 :math:`A` を互いに素な部分集合に分割する。このような分割を\ **類別**\ という。たとえば、:math:`\{0, 1, \ldots, 11\}` を 4 を法とする合同関係で類別すると、余りが 0, 1, 2, 3 の 4 つの同値類に分かれる。ハッシュ表が、ハッシュ値をバケット数で割った余りによってキーを振り分けるのは、この類別の一例である。

半順序
~~~~~~

反射律・反対称律・推移律を満たす関係を\ :term:`半順序`\ という。整数の大小関係 :math:`\le`、集合の包含関係 :math:`\subseteq`、正の整数の整除関係（:math:`a` が :math:`b` を割り切るとき :math:`a \mid b`）はいずれも半順序である。

大小関係 :math:`\le` では任意の 2 つの整数を比較できるが、整除関係では 2 と 3 のように比較できない組がある。任意の 2 要素が比較可能な半順序を\ **全順序**\ という。

有限集合上の半順序は、**ハッセ図**\ で表すと分かりやすい。ハッセ図では、:math:`a \mid b` かつ :math:`a \ne b` で、間に他の要素が入らない組だけを線で結び、大きい方を上に描く。:numref:`fig-ch03-hasse` は 12 の約数の整除関係のハッセ図である。

.. _fig-ch03-hasse:

.. graphviz::
   :caption: 12 の約数の整除関係のハッセ図
   :align: center

   graph hasse {
       rankdir=BT;
       node [shape=circle, width=0.4, fixedsize=true, fontsize=12];
       1 -- 2; 1 -- 3; 2 -- 4; 2 -- 6; 3 -- 6; 4 -- 12; 6 -- 12;
   }

半順序は、依存関係のあるタスクの実行順序（あるタスクは別のタスクの完了後にしか実行できない）を表す際にも現れる。半順序と矛盾しないように全要素を一列に並べることを\ **トポロジカルソート**\ という。

Python で確かめる
-----------------

サンプルコード：:download:`ch03_functions_relations.py <../examples/ch03_functions_relations.py>`

有限集合の間の写像は、Python の ``dict`` でそのまま表せる。単射であることは「値に重複がない」こと、全射であることは「値の集合が終域に一致する」ことと同じである。

.. literalinclude:: ../examples/ch03_functions_relations.py
   :language: python
   :linenos:
   :lines: 17-36

関係は順序対の集合 ``set[tuple[int, int]]`` で表せる。推移律の判定では、:math:`(a, b)` と :math:`(c, d)` の組で :math:`b = c` となるものすべてについて、:math:`(a, d)` が関係に含まれるかを調べる。

.. literalinclude:: ../examples/ch03_functions_relations.py
   :language: python
   :linenos:
   :pyobject: is_transitive

同値類は、まだどの同値類にも属していない要素 :math:`a` を選び、:math:`a` と関係にある要素を集めることを繰り返して求める。

.. literalinclude:: ../examples/ch03_functions_relations.py
   :language: python
   :linenos:
   :pyobject: equivalence_classes

実行結果は次のとおりである。

.. code-block:: text

   --- 写像の性質 ---
   f: 単射=True, 全射=True
   g: 単射=False, 全射=False
   f の逆写像: {1: 'a', 2: 'b', 3: 'c'}
   double ∘ f: {'a': 2, 'b': 4, 'c': 6}
   --- 合同関係 (mod 4) ---
   反射律=True, 対称律=True, 推移律=True
     [0] = [0, 4, 8]
     [1] = [1, 5, 9]
     [2] = [2, 6, 10]
     [3] = [3, 7, 11]
   --- 整除関係（12 の約数） ---
   反射律=True, 反対称律=True, 推移律=True
   対称律=False

写像 ``g`` は ``"a"`` と ``"b"`` を同じ 1 に移すので単射でなく、3 を値にとらないので終域 :math:`\{1, 2, 3\}` への全射でもない。4 を法とする合同関係は同値関係であり、:math:`\{0, \ldots, 11\}` が 4 つの同値類に分かれる。整除関係は対称律を満たさず、反対称律を満たすので、同値関係ではなく半順序である。

まとめ
------

* 写像は、定義域の各要素に終域の要素をちょうど 1 つ対応させる規則である。
* 単射・全射・全単射の存在は、有限集合の要素数の大小関係と対応する。全単射を作ることは、要素数が等しいことを示す強力な方法である。
* 関係は直積の部分集合であり、反射律・対称律・推移律を満たすものが同値関係、反射律・反対称律・推移律を満たすものが半順序である。
* 同値関係は集合を互いに素な同値類に分割する。

写像と関係については [Rosen2019]_ に詳しい。
