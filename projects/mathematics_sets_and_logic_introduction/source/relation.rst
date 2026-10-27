関係
====

「:math:`x` は :math:`y` 以下である」「:math:`x` と :math:`y` は同じ部署に所属する」のように、2 つのものの間に成り立つかどうかが定まる性質を関係という。本章では、関係を集合として定義し、同値関係と順序関係という 2 つの重要な種類を学ぶ。

二項関係
--------

.. admonition:: 定義（二項関係）

   直積 :math:`A \times B` の部分集合 :math:`R` を、:math:`A` から :math:`B` への二項関係という。:math:`(a, b) \in R` であることを :math:`a \, R \, b` とも書く。:math:`A \times A` の部分集合を :math:`A` 上の二項関係という。

関係を「成り立つ組の集合」として定義するのがこの定義の要点である。たとえば :math:`A = \{1, 2, 3\}` 上の関係 :math:`\leq` は、次の順序対の集合として表される。

.. math::

   \{(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)\}

以下、単に関係といえば二項関係を指す。関係の例を挙げる。

* 自然数全体 :math:`\mathbb{N}` 上の :math:`\leq` と :math:`<`
* 任意の集合上の等号 :math:`=`
* 正の整数全体上の整除関係 :math:`\mid`。:math:`a \mid b` は「:math:`a` は :math:`b` を割り切る」、すなわち :math:`b` が :math:`a` の倍数であることを表す。
* 整数全体 :math:`\mathbb{Z}` 上の合同関係。:math:`a \equiv b \pmod{3}` は、:math:`a - b` が 3 で割り切れることを表す。

Python では、有限集合上の関係を ``tuple`` 型の値の集合として表せる。リレーショナルデータベースのテーブルや、SNS のフォロー関係（:math:`a` が :math:`b` をフォローしている）も、組の集合として表される関係の例である。

関係の性質
----------

集合 :math:`A` 上の関係 :math:`R` について、次の性質を考える。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 名称
     - 定義
   * - 反射律
     - :math:`\forall a \, (a \, R \, a)`
   * - 対称律
     - :math:`\forall a \, \forall b \, (a \, R \, b \to b \, R \, a)`
   * - 推移律
     - :math:`\forall a \, \forall b \, \forall c \, ((a \, R \, b \land b \, R \, c) \to a \, R \, c)`
   * - 反対称律
     - :math:`\forall a \, \forall b \, ((a \, R \, b \land b \, R \, a) \to a = b)`

前節の例がそれぞれの性質を満たすかどうかは次のとおりである（○は満たす、×は満たさない）。

.. list-table::
   :header-rows: 1

   * - 関係
     - 反射律
     - 対称律
     - 推移律
     - 反対称律
   * - :math:`\mathbb{N}` 上の :math:`\leq`
     - ○
     - ×
     - ○
     - ○
   * - :math:`\mathbb{N}` 上の :math:`<`
     - ×
     - ×
     - ○
     - ○
   * - 等号 :math:`=`
     - ○
     - ○
     - ○
     - ○
   * - 整除関係 :math:`\mid`
     - ○
     - ×
     - ○
     - ○
   * - :math:`\equiv \pmod{3}`
     - ○
     - ○
     - ○
     - ×

:math:`<` が反対称律を満たすのは、:math:`a < b` かつ :math:`b < a` となる :math:`a`、:math:`b` が存在せず、含意の前件が常に偽になるためである。

同値関係
--------

.. admonition:: 定義（同値関係）

   反射律・対称律・推移律を満たす関係を同値関係という。

同値関係は「ある観点で同じとみなせる」という関係を抽象化したものである。等号 :math:`=` や合同関係 :math:`\equiv \pmod{3}`、「同じ部署に所属する」は同値関係である。

プログラミングでよく現れる同値関係として、ある関数 ``key`` を使って「``key(x) == key(y)`` のとき :math:`x` と :math:`y` を関係付ける」と定めた関係がある。これは等号の性質から必ず同値関係になる。たとえば、文字列を ``str.lower`` の結果で比べれば、大文字と小文字を区別しない比較という同値関係が得られる。

.. admonition:: 定義（同値類・商集合）

   :math:`R` を集合 :math:`A` 上の同値関係とする。:math:`a \in A` に対し、:math:`a` と関係する要素全体の集合

   .. math::

      [a] = \{x \in A \mid x \, R \, a\}

   を :math:`a` の同値類という。同値類全体の集合 :math:`\{[a] \mid a \in A\}` を :math:`A` の :math:`R` による商集合といい、:math:`A / R` と書く。

たとえば :math:`\mathbb{Z}` 上の :math:`\equiv \pmod{3}` の同値類は、3 で割った余りが 0、1、2 の整数全体の 3 つである。

.. math::

   [0] &= \{\ldots, -3, 0, 3, 6, \ldots\} \\
   [1] &= \{\ldots, -2, 1, 4, 7, \ldots\} \\
   [2] &= \{\ldots, -1, 2, 5, 8, \ldots\}

:math:`[0] = [3] = [6]` のように、同じ同値類を異なる要素で表せることに注意する。同値類から選んだ要素を代表元という。

同値類には次の重要な性質がある。

.. admonition:: 定理

   :math:`R` を集合 :math:`A` 上の同値関係とする。任意の :math:`a, b \in A` について、:math:`[a] = [b]` と :math:`[a] \cap [b] = \emptyset` のどちらか一方が成り立つ。

**証明** :math:`[a] \cap [b] \neq \emptyset` と仮定して :math:`[a] = [b]` を示す。:math:`c \in [a] \cap [b]` とすると :math:`c \, R \, a` かつ :math:`c \, R \, b` である。対称律より :math:`a \, R \, c` なので、推移律より :math:`a \, R \, b` である。対称律よりさらに :math:`b \, R \, a` も成り立つ。ここで :math:`x \in [a]` とすると :math:`x \, R \, a` と :math:`a \, R \, b` から推移律により :math:`x \, R \, b`、すなわち :math:`x \in [b]` である。よって :math:`[a] \subseteq [b]` である。:math:`a` と :math:`b` の役割を入れ替えれば :math:`[b] \subseteq [a]` も同様に示せるので、:math:`[a] = [b]` である。□

また、反射律より :math:`a \in [a]` なので、どの要素もいずれかの同値類に属し、同値類は空でない。つまり、同値類は集合 :math:`A` を、互いに重ならない空でない部分集合に切り分ける。このような切り分けを :math:`A` の分割という。

.. admonition:: 定義（分割）

   集合 :math:`A` の空でない部分集合からなる集合族 :math:`\mathcal{F}` が次の 2 つを満たすとき、:math:`\mathcal{F}` を :math:`A` の分割という。

   #. :math:`\mathcal{F}` の要素の和集合が :math:`A` に等しい。
   #. :math:`\mathcal{F}` の異なる 2 つの要素は互いに素である。

逆に、集合 :math:`A` の分割が与えられたとき、「同じ部分集合に属する」という関係は同値関係になる。したがって、集合上の同値関係と分割は一対一に対応する。次の図は、集合 :math:`\{0, 1, \ldots, 8\}` を :math:`\equiv \pmod{3}` で分割した様子を示している。

.. graphviz::
   :alt: 0 から 8 までの整数を 3 で割った余りで 3 つの同値類に分けた図
   :caption: :math:`\{0, 1, \ldots, 8\}` の :math:`\equiv \pmod{3}` による分割

   graph partition {
       graph [rankdir=TB, nodesep=0.3];
       node [shape=circle, fontname="Helvetica", width=0.4, fixedsize=true];
       subgraph cluster_0 { label="[0]"; fontname="Helvetica"; style=rounded; 0; 3; 6; }
       subgraph cluster_1 { label="[1]"; fontname="Helvetica"; style=rounded; 1; 4; 7; }
       subgraph cluster_2 { label="[2]"; fontname="Helvetica"; style=rounded; 2; 5; 8; }
   }

同値類による分割は、データを ``key`` 関数の値ごとにグループ化する処理（``itertools.groupby`` や SQL の ``GROUP BY``）と同じ構造をしている。

順序関係
--------

.. admonition:: 定義（半順序・全順序）

   反射律・反対称律・推移律を満たす関係を半順序という。半順序 :math:`\preceq` が定められた集合を半順序集合という。半順序 :math:`\preceq` がさらに

   .. math::

      \forall a \, \forall b \, (a \preceq b \lor b \preceq a)

   を満たすとき、:math:`\preceq` を全順序という。

全順序では任意の 2 つの要素が比較できるが、半順序では比較できない要素の組があってもよい。

* 実数全体 :math:`\mathbb{R}` 上の :math:`\leq` は全順序である。
* 正の整数全体上の整除関係 :math:`\mid` は半順序だが全順序ではない。:math:`2 \mid 3` も :math:`3 \mid 2` も成り立たない。
* 集合 :math:`A` のべき集合 :math:`\mathcal{P}(A)` 上の包含関係 :math:`\subseteq` は半順序である。:math:`A` が 2 個以上の要素を持てば全順序ではない。たとえば :math:`\{a\}` と :math:`\{b\}` は比較できない。

ソフトウェアのモジュール間の依存関係や、タスクの前後関係も半順序で表されることが多い。有限の半順序集合の要素は、半順序と矛盾しないように一列に並べられる。この並べ方を求めることをトポロジカルソートといい、ビルドツールやパッケージ管理ツールで使われている。Python では標準ライブラリの ``graphlib.TopologicalSorter`` で計算できる。

ハッセ図
--------

有限の半順序集合は、ハッセ図で図示できる。ハッセ図では、要素を点で表し、:math:`a \preceq b` かつ :math:`a \neq b` で、その間に別の要素が入らないとき、:math:`a` を下、:math:`b` を上に置いて線で結ぶ。反射律と推移律から分かる線は省略する。

次の図は、12 の正の約数全体 :math:`\{1, 2, 3, 4, 6, 12\}` の整除関係と、:math:`\mathcal{P}(\{a, b, c\})` の包含関係のハッセ図である。

.. graphviz::
   :alt: 12 の約数の整除関係のハッセ図
   :caption: 12 の約数の整除関係

   graph divisors {
       graph [rankdir=BT, ranksep=0.4];
       node [shape=plaintext, fontname="Helvetica", fontsize=14];
       1 -- 2; 1 -- 3; 2 -- 4; 2 -- 6; 3 -- 6; 4 -- 12; 6 -- 12;
   }

.. graphviz::
   :alt: 3 要素の集合のべき集合の包含関係のハッセ図
   :caption: :math:`\mathcal{P}(\{a, b, c\})` の包含関係

   graph powerset {
       graph [rankdir=BT, ranksep=0.5];
       node [shape=plaintext, fontname="Helvetica", fontsize=14];
       e [label="∅"];
       a [label="{a}"]; b [label="{b}"]; c [label="{c}"];
       ab [label="{a, b}"]; ac [label="{a, c}"]; bc [label="{b, c}"];
       abc [label="{a, b, c}"];
       e -- a; e -- b; e -- c;
       a -- ab; a -- ac; b -- ab; b -- bc; c -- ac; c -- bc;
       ab -- abc; ac -- abc; bc -- abc;
   }

たとえば 1 つ目の図で :math:`1 \mid 4` は線で直接結ばれていないが、:math:`1 \mid 2` と :math:`2 \mid 4` から推移律で分かる。

関係の合成と推移閉包
--------------------

.. admonition:: 定義（関係の合成）

   :math:`R` を :math:`A` から :math:`B` への関係、:math:`S` を :math:`B` から :math:`C` への関係とする。:math:`A` から :math:`C` への関係

   .. math::

      S \circ R = \{(a, c) \in A \times C \mid \exists b \in B \, (a \, R \, b \land b \, S \, c)\}

   を :math:`R` と :math:`S` の合成という。

:math:`S \circ R` は「:math:`R` をたどってから :math:`S` をたどる」関係である。:math:`R` を先に書かないのは、第 8 章で扱う合成写像の記法に合わせるためである。

「直接依存している」という関係 :math:`R` があるとき、「直接または間接に依存している」という関係は、:math:`R`、:math:`R \circ R`、:math:`R \circ R \circ R`、… の和集合になる。これは :math:`R` を含む推移的な関係のうち最小のものであり、:math:`R` の推移閉包という。推移閉包は、ネットワークの到達可能性や、パッケージの間接的な依存関係を求める際に現れる。

サンプルコード
--------------

有限集合上の関係の性質を判定し、同値類と推移閉包を求めるサンプルコードを示す。推移閉包は、合成によって新しい組が増えなくなるまで組を追加して求めている。

:download:`relation.py <../examples/relation.py>`

.. literalinclude:: ../examples/relation.py
   :language: python
   :linenos:

実行結果は次のとおりである。

.. code-block:: text

   x ≡ y (mod 3) は同値関係か: True
     同値類: [0, 3, 6]
     同値類: [1, 4, 7]
     同値類: [2, 5, 8]
   整除関係は半順序か: True
   整除関係は同値関係か: False
     app は db に依存する
     app は http に依存する（間接）
     app は socket に依存する（間接）
     app は web に依存する
     http は socket に依存する
     web は http に依存する
     web は socket に依存する（間接）
