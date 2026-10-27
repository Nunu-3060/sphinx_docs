写像
====

写像は、集合の要素に別の集合の要素を対応させる規則である。プログラミングの関数とよく似ているが、異なる点もある。本章では、写像を関係の特別な場合として定義し、その基本的な性質を学ぶ。

写像の定義
----------

.. admonition:: 定義（写像）

   集合 :math:`A` から集合 :math:`B` への関係 :math:`f \subseteq A \times B` が

   .. math::

      \forall a \in A \, \exists! \, b \in B \, ((a, b) \in f)

   を満たすとき、:math:`f` を :math:`A` から :math:`B` への写像といい、:math:`f \colon A \to B` と書く。:math:`(a, b) \in f` であることを :math:`f(a) = b` と書き、:math:`b` を :math:`f` による :math:`a` の像という。:math:`A` を :math:`f` の定義域、:math:`B` を :math:`f` の終域という。

ここで :math:`\exists! \, b` は「条件を満たす :math:`b` がただ 1 つ存在する」ことを表す。つまり写像の条件は、次の 2 つからなる。

* 定義域のどの要素にも、対応する終域の要素がある。
* 対応する終域の要素は 1 つに限られる。

たとえば、:math:`f(x) = x^2` で定まる :math:`f \colon \mathbb{R} \to \mathbb{R}` は写像である。一方、:math:`\{(x, y) \in \mathbb{R} \times \mathbb{R} \mid x = y^2\}` は :math:`\mathbb{R}` から :math:`\mathbb{R}` への写像ではない。:math:`x = 1` には :math:`y = 1` と :math:`y = -1` の 2 つが対応し、:math:`x = -1` には対応する :math:`y` が無いからである。

写像 :math:`f` が要素 :math:`a` を :math:`f(a)` に対応させることを :math:`a \mapsto f(a)` とも書く。また、2 つの写像 :math:`f, g \colon A \to B` が等しいとは、すべての :math:`a \in A` について :math:`f(a) = g(a)` であることをいう。写像は対応の結果だけで決まり、計算の手順は問わない。

Python の関数との違い
---------------------

写像と Python の関数はよく似ているが、次の点で異なる。

* Python の関数は、例外を送出したり、終了しなかったりすることがある。そのような引数では値が定まらないので、写像の条件の 1 つ目を満たさない。
* Python の関数は、乱数や現在時刻、外部の状態によって、同じ引数に対して異なる値を返すことがある。これは写像の条件の 2 つ目を満たさない。
* Python の関数は、画面への出力やファイルの書き込みのような副作用を持つことがある。写像には対応以外の働きは無い。

したがって、写像に近いのは、どの引数に対しても必ず終了して値を返し、同じ引数に同じ値を返し、副作用を持たない関数である。このような関数は純粋関数とも呼ばれる。

有限集合の間の写像は、定義域の要素をキーとする辞書（``dict`` 型）で表すのが分かりやすい。辞書のキーは重複しないので、キーの集合が定義域に一致していれば写像の条件を満たす。

像と逆像
--------

.. admonition:: 定義（像・逆像）

   写像 :math:`f \colon A \to B` について、:math:`X \subseteq A` と :math:`Y \subseteq B` に対し

   .. math::

      f(X) &= \{f(x) \mid x \in X\} \\
      f^{-1}(Y) &= \{a \in A \mid f(a) \in Y\}

   と定め、:math:`f(X)` を :math:`X` の像、:math:`f^{-1}(Y)` を :math:`Y` の逆像という。

:math:`f(A)` を :math:`f` の像という。:math:`f(A)` を値域と呼ぶ文献もあるが、値域という語は終域の意味で使われることもあるため、本書では使わない。

たとえば :math:`f \colon \mathbb{Z} \to \mathbb{Z}`、:math:`f(x) = x^2` について、

* :math:`f(\{-1, 0, 1\}) = \{0, 1\}`
* :math:`f^{-1}(\{4\}) = \{-2, 2\}`
* :math:`f^{-1}(\{3\}) = \emptyset`

である。逆像は、後述の逆写像が存在しない写像に対しても定義される。たとえばデータベースの検索は「属性の値がある範囲に入るレコード全体」を求める操作なので、逆像を求める操作とみなせる。

像と逆像は、集合演算と次の関係にある。

.. math::

   f(X_1 \cup X_2) &= f(X_1) \cup f(X_2) \\
   f(X_1 \cap X_2) &\subseteq f(X_1) \cap f(X_2) \\
   f^{-1}(Y_1 \cup Y_2) &= f^{-1}(Y_1) \cup f^{-1}(Y_2) \\
   f^{-1}(Y_1 \cap Y_2) &= f^{-1}(Y_1) \cap f^{-1}(Y_2)

2 行目だけは等号が成り立つとは限らない。上の :math:`f(x) = x^2` で :math:`X_1 = \{-1\}`、:math:`X_2 = \{1\}` とすると、:math:`f(X_1 \cap X_2) = f(\emptyset) = \emptyset` だが、:math:`f(X_1) \cap f(X_2) = \{1\}` である。

単射・全射・全単射
------------------

.. admonition:: 定義（単射・全射・全単射）

   写像 :math:`f \colon A \to B` について、

   * :math:`\forall a \in A \, \forall a' \in A \, (f(a) = f(a') \to a = a')` が成り立つとき、:math:`f` を単射という。
   * :math:`\forall b \in B \, \exists a \in A \, (f(a) = b)` が成り立つとき、:math:`f` を全射という。
   * 単射かつ全射であるとき、:math:`f` を全単射という。

単射の条件は、対偶をとると「:math:`a \neq a'` ならば :math:`f(a) \neq f(a')`」となる。つまり単射とは、異なる要素が異なる要素に移る写像である。全射の条件は :math:`f(A) = B`、すなわち終域のどの要素も何かの像になっていることである。全単射は、定義域と終域の要素を過不足なく一対一に対応させる写像である。

次の図は、有限集合の間の写像の例である。各写像について、上の段が定義域、下の段が終域の要素を表す。

.. graphviz::
   :alt: 単射でも全射でもない写像、単射だが全射でない写像、全射だが単射でない写像、全単射の矢印図
   :caption: f1 は単射でも全射でもない写像、f2 は単射だが全射でない写像、f3 は全射だが単射でない写像、f4 は全単射

   digraph mappings {
       graph [rankdir=TB, nodesep=0.3, ranksep=0.7, newrank=true];
       node [shape=circle, fontname="Helvetica", width=0.35, fixedsize=true, fontsize=11];
       edge [arrowsize=0.6];
       subgraph cluster_n { label="f1"; fontname="Helvetica"; style=rounded;
           n_a1 [label="1"]; n_a2 [label="2"]; n_a3 [label="3"];
           n_b1 [label="a"]; n_b2 [label="b"]; n_b3 [label="c"];
           n_a1 -> n_b1; n_a2 -> n_b1; n_a3 -> n_b2; }
       subgraph cluster_i { label="f2"; fontname="Helvetica"; style=rounded;
           i_a1 [label="1"]; i_a2 [label="2"];
           i_b1 [label="a"]; i_b2 [label="b"]; i_b3 [label="c"];
           i_a1 -> i_b1; i_a2 -> i_b3; }
       subgraph cluster_s { label="f3"; fontname="Helvetica"; style=rounded;
           s_a1 [label="1"]; s_a2 [label="2"]; s_a3 [label="3"];
           s_b1 [label="a"]; s_b2 [label="b"];
           s_a1 -> s_b1; s_a2 -> s_b2; s_a3 -> s_b2; }
       subgraph cluster_b { label="f4"; fontname="Helvetica"; style=rounded;
           b_a1 [label="1"]; b_a2 [label="2"]; b_a3 [label="3"];
           b_b1 [label="a"]; b_b2 [label="b"]; b_b3 [label="c"];
           b_a1 -> b_b2; b_a2 -> b_b3; b_a3 -> b_b1; }
       { rank=same; n_a1; n_a2; n_a3; i_a1; i_a2; s_a1; s_a2; s_a3; b_a1; b_a2; b_a3; }
       { rank=same; n_b1; n_b2; n_b3; i_b1; i_b2; i_b3; s_b1; s_b2; b_b1; b_b2; b_b3; }
       n_a3 -> i_a1 -> s_a1 [style=invis];
       s_a3 -> b_a1 [style=invis];
       n_a1 -> n_a2 -> n_a3 [style=invis];
       n_b1 -> n_b2 -> n_b3 [style=invis];
       i_a1 -> i_a2 [style=invis];
       i_b1 -> i_b2 -> i_b3 [style=invis];
       s_a1 -> s_a2 -> s_a3 [style=invis];
       s_b1 -> s_b2 [style=invis];
       b_a1 -> b_a2 -> b_a3 [style=invis];
       b_b1 -> b_b2 -> b_b3 [style=invis];
   }

数の集合の間の写像の例を挙げる。

.. list-table::
   :header-rows: 1
   :widths: 64 12 12 12

   * - 写像
     - 単射
     - 全射
     - 全単射
   * - :math:`f \colon \mathbb{Z} \to \mathbb{Z}`、:math:`f(x) = 2x`
     - ○
     - ×
     - ×
   * - :math:`f \colon \mathbb{Z} \to \mathbb{Z}`、:math:`f(x) = x^2`
     - ×
     - ×
     - ×
   * - :math:`f \colon \mathbb{Z} \to \{0, 1, 2\}`、:math:`f(x) = (x \text{ を 3 で割った余り})`
     - ×
     - ○
     - ×
   * - :math:`f \colon \mathbb{R} \to \mathbb{R}`、:math:`f(x) = 2x + 1`
     - ○
     - ○
     - ○

同じ式で定まる写像でも、定義域と終域によって性質が変わる。たとえば :math:`f(x) = x^2` は、:math:`f \colon \mathbb{Z} \to \mathbb{Z}` としては単射でも全射でもないが、:math:`f \colon \mathbb{N} \to \mathbb{N}` としては単射になる。写像を考えるときは、常に定義域と終域を明示する必要がある。

これらの概念はプログラミングにも現れる。データの符号化（エンコード）は、元のデータを復元（デコード）できるように単射でなければならない。一方、ハッシュ関数は、入力となりうる値の数が出力の値の数より多いので、単射にはなりえない。これは第 9 章の鳩の巣原理から分かる。

合成写像
--------

.. admonition:: 定義（合成写像）

   写像 :math:`f \colon A \to B` と :math:`g \colon B \to C` に対し、:math:`a \mapsto g(f(a))` で定まる写像 :math:`A \to C` を :math:`f` と :math:`g` の合成写像といい、:math:`g \circ f` と書く。

:math:`g \circ f` は「:math:`f` を先に、:math:`g` を後に適用する」写像である。記号の並び順と適用の順が逆になるのは、:math:`(g \circ f)(a) = g(f(a))` と書いたときに :math:`g` と :math:`f` の並び順がそろうようにするためである。

写像の合成は結合法則 :math:`h \circ (g \circ f) = (h \circ g) \circ f` を満たす。一方、交換法則は一般に成り立たない。:math:`f(x) = x + 1` と :math:`g(x) = 2x` について、:math:`(g \circ f)(x) = 2x + 2` だが :math:`(f \circ g)(x) = 2x + 1` である。

また、単射どうしの合成は単射、全射どうしの合成は全射、したがって全単射どうしの合成は全単射である。

逆写像
------

集合 :math:`A` の各要素をそれ自身に対応させる写像を :math:`A` 上の恒等写像といい、:math:`\mathrm{id}_A` と書く。

.. admonition:: 定義（逆写像）

   写像 :math:`f \colon A \to B` に対し、写像 :math:`g \colon B \to A` が :math:`g \circ f = \mathrm{id}_A` と :math:`f \circ g = \mathrm{id}_B` を満たすとき、:math:`g` を :math:`f` の逆写像といい、:math:`f^{-1}` と書く。

.. admonition:: 定理

   写像 :math:`f \colon A \to B` が逆写像を持つための必要十分条件は、:math:`f` が全単射であることである。

**証明** :math:`f` が逆写像 :math:`g` を持つとする。:math:`f(a) = f(a')` ならば :math:`a = g(f(a)) = g(f(a')) = a'` なので :math:`f` は単射である。また、任意の :math:`b \in B` について :math:`f(g(b)) = b` なので :math:`f` は全射である。

逆に :math:`f` が全単射であるとする。全射なので、任意の :math:`b \in B` に対して :math:`f(a) = b` となる :math:`a \in A` があり、単射なのでそのような :math:`a` はただ 1 つである。この :math:`a` を :math:`g(b)` と定めると、:math:`g \colon B \to A` は写像であり、作り方から :math:`g \circ f = \mathrm{id}_A` と :math:`f \circ g = \mathrm{id}_B` を満たす。□

たとえば :math:`f \colon \mathbb{R} \to \mathbb{R}`、:math:`f(x) = 2x + 1` の逆写像は :math:`f^{-1}(y) = (y - 1) / 2` である。

逆像の記号 :math:`f^{-1}(Y)` と逆写像の記号 :math:`f^{-1}` は同じ記号を使うが、別のものである。逆像はどの写像についても定義されるが、逆写像は全単射の場合だけ存在する。:math:`f` が全単射のときは、:math:`\{b\}` の逆像は逆写像による :math:`b` の像を唯一の要素とする集合 :math:`\{f^{-1}(b)\}` になるので、混乱は生じない。

サンプルコード
--------------

有限集合の間の写像を辞書で表し、像・逆像・単射・全射・逆写像・合成写像を扱うサンプルコードを示す。

:download:`mapping.py <../examples/mapping.py>`

.. literalinclude:: ../examples/mapping.py
   :language: python
   :linenos:

実行結果は次のとおりである。

.. code-block:: text

   f(x) = x²（{-2, ..., 2} → {0, 1, 4}）: 単射=False, 全射=True, 全単射=False
     f({-1, 0, 1}) = [0, 1]
     f⁻¹({4}) = [-2, 2]
   g(x) = x + 1（{-2, ..., 2} → {-1, ..., 3}）: 単射=True, 全射=True, 全単射=True
     g⁻¹(3) = 2
   (f ∘ (x ↦ -x))(2) = 4
