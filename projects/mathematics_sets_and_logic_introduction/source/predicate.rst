述語と量化子
============

「:math:`x > 3`」のように変数を含む主張は、変数の値が決まるまで真偽が定まらない。本章では、このような主張を扱う述語と、「すべての」「ある」を表す量化子を導入する。

述語
----

.. admonition:: 定義（述語）

   変数を含み、変数に値を代入すると命題になる主張を述語という。

たとえば :math:`P(x)` を「:math:`x > 3`」とすると、:math:`P(5)` は真の命題、:math:`P(1)` は偽の命題である。変数が動く範囲をあらかじめ定めておき、これを議論領域という。議論領域は、自然数全体や整数全体、あるプログラムが扱うユーザー全体などである。議論領域は値の集まりであり、第 6 章で扱う集合の言葉で表される。

述語は複数の変数を含んでもよい。たとえば :math:`Q(x, y)` を「:math:`x + y = 4`」とすると、:math:`Q(1, 3)` は真、:math:`Q(2, 3)` は偽である。

述語は「議論領域の値を受け取って真理値を返すもの」なので、Python では ``bool`` 型の値を返す関数として表せる。

.. code-block:: python
   :linenos:

   def p(x: int) -> bool:
       return x > 3

量化子
------

述語に値を代入する以外にも、述語から命題を作る方法がある。

.. admonition:: 定義（全称量化子・存在量化子）

   :math:`\forall x \, P(x)` は「議論領域のすべての :math:`x` について :math:`P(x)` が成り立つ」という命題を表す。:math:`\exists x \, P(x)` は「議論領域のある :math:`x` について :math:`P(x)` が成り立つ」、すなわち「:math:`P(x)` を満たす :math:`x` が少なくとも 1 つ存在する」という命題を表す。記号 :math:`\forall` を全称量化子、:math:`\exists` を存在量化子という。

:math:`\forall x \, P(x)` の形の命題を全称命題、:math:`\exists x \, P(x)` の形の命題を存在命題という。議論領域を明示したいときは、議論領域を :math:`D` として :math:`\forall x \in D \, P(x)`、:math:`\exists x \in D \, P(x)` と書く。

議論領域を自然数全体とすると、:math:`\forall x \, (x \geq 0)` は真、:math:`\forall x \, (x > 3)` は偽、:math:`\exists x \, (x > 3)` は真である。

議論領域が有限集合 :math:`\{a_1, a_2, \ldots, a_n\}` のときは、全称命題は論理積、存在命題は論理和で書き直せる。

.. math::

   \forall x \, P(x) &\equiv P(a_1) \land P(a_2) \land \cdots \land P(a_n) \\
   \exists x \, P(x) &\equiv P(a_1) \lor P(a_2) \lor \cdots \lor P(a_n)

これは Python の組み込み関数 ``all`` と ``any`` にそのまま対応する。

.. code-block:: python
   :linenos:

   domain = range(10)
   print(all(x >= 0 for x in domain))  # ∀x (x ≥ 0) → True
   print(any(x > 3 for x in domain))   # ∃x (x > 3) → True

ただし、プログラムで確かめられるのは議論領域が有限の場合だけである。議論領域が自然数全体のように無限の場合、全称命題をすべての値について確かめることはできない。そのため、無限の議論領域についての全称命題は、第 4 章で扱った証明によって示す必要がある。

量化子の否定
------------

「すべてのテストが成功した」の否定は「成功しなかったテストが存在する」である。「すべてのテストが失敗した」ではない点に注意する。一般に、次の法則が成り立つ。

.. admonition:: 量化子の否定

   .. math::

      \neg \forall x \, P(x) &\equiv \exists x \, \neg P(x) \\
      \neg \exists x \, P(x) &\equiv \forall x \, \neg P(x)

議論領域が有限の場合、全称命題は論理積、存在命題は論理和なので、これはド・モルガンの法則そのものである。この法則は、反例を 1 つ挙げれば全称命題を否定できるという、第 4 章で述べた事実の根拠でもある。

Python では ``not all(p(x) for x in domain)`` と ``any(not p(x) for x in domain)`` が常に同じ値になる。

多重の量化子と順序
------------------

量化子は重ねて使える。議論領域を自然数全体とすると、

* :math:`\forall x \, \exists y \, (y > x)` は「どの :math:`x` に対しても、:math:`x` より大きい :math:`y` がある」という意味であり、真である（:math:`y = x + 1` とすればよい）。
* :math:`\exists y \, \forall x \, (y > x)` は「どの :math:`x` よりも大きい :math:`y` がある」という意味であり、偽である（そのような :math:`y` は :math:`y > y` を満たさなければならない）。

このように、異なる種類の量化子の順序を入れ替えると意味が変わる。:math:`\forall x \, \exists y` では :math:`y` を :math:`x` ごとに選んでよいが、:math:`\exists y \, \forall x` では 1 つの :math:`y` がすべての :math:`x` に対して通用しなければならない。

一方、同じ種類の量化子どうしは入れ替えてもよい。

.. math::

   \forall x \, \forall y \, P(x, y) &\equiv \forall y \, \forall x \, P(x, y) \\
   \exists x \, \exists y \, P(x, y) &\equiv \exists y \, \exists x \, P(x, y)

また、:math:`\exists y \, \forall x \, P(x, y)` が真ならば :math:`\forall x \, \exists y \, P(x, y)` も真である。逆は上の例のとおり成り立つとは限らない。

多重の量化子を含む命題の否定は、量化子の否定を外側から順に適用して求める。たとえば、数列 :math:`a_0, a_1, a_2, \ldots` が上に有界であるとは

.. math::

   \exists M \, \forall n \, (a_n \leq M)

が成り立つことをいう。その否定は

.. math::

   \neg \exists M \, \forall n \, (a_n \leq M)
   \equiv \forall M \, \neg \forall n \, (a_n \leq M)
   \equiv \forall M \, \exists n \, (a_n > M)

であり、「どのような :math:`M` に対しても、:math:`M` を超える項がある」という意味になる。

自由変数と束縛変数
------------------

:math:`\forall x \, P(x, y)` において、変数 :math:`x` は量化子 :math:`\forall x` によって束縛されているといい、束縛変数と呼ぶ。束縛されていない変数 :math:`y` を自由変数と呼ぶ。自由変数を含む式は、その変数の値が決まるまで真偽が定まらない述語である。

束縛変数の名前は自由に付け替えられる。:math:`\forall x \, P(x)` と :math:`\forall z \, P(z)` は同じ命題である。ただし、付け替えた名前が既に自由変数として使われている場合は意味が変わってしまうので、そのような名前は使えない。

この区別は、Python のジェネレータ式の変数と外側の変数の区別によく似ている。

.. code-block:: python
   :linenos:

   y = 5
   result = all(x < y for x in range(3))

ここで ``x`` はジェネレータ式の中だけで意味を持つ束縛変数にあたり、``z`` に名前を変えても結果は変わらない。一方 ``y`` は式の外で値が決まる自由変数にあたる。

議論領域の制限と空の議論領域
----------------------------

議論領域全体ではなく、条件 :math:`D(x)` を満たす :math:`x` だけについて述べたいことがある。:math:`D(x)` を満たす :math:`x` の全体を :math:`D` と書くと、次のように書き換えられる。

.. math::

   \forall x \in D \, P(x) &\equiv \forall x \, (D(x) \to P(x)) \\
   \exists x \in D \, P(x) &\equiv \exists x \, (D(x) \land P(x))

全称量化子では含意 :math:`\to`、存在量化子では論理積 :math:`\land` になることに注意する。存在量化子のほうを :math:`\exists x \, (D(x) \to P(x))` と書くと、:math:`D(x)` を満たさない :math:`x` が 1 つでもあれば真になってしまい、意図と異なる命題になる。

この書き換えから、:math:`D(x)` を満たす :math:`x` が 1 つも無い場合、すなわち議論領域が空の場合の真理値が分かる。

* :math:`\forall x \in D \, P(x)` は、含意の前件 :math:`D(x)` が常に偽なので、:math:`P(x)` の内容にかかわらず真である。
* :math:`\exists x \in D \, P(x)` は、論理積の一方 :math:`D(x)` が常に偽なので偽である。

空の議論領域についての全称命題が真になることを、空虚な真という。Python でも ``all([])`` は ``True``、``any([])`` は ``False`` である。「チェック対象が 0 件のとき、すべてのチェックに合格した」とみなされる、という形でプログラムにも現れるので注意する。

サンプルコード
--------------

有限の議論領域上で全称命題・存在命題を評価し、量化子の順序による違いと空の議論領域の扱いを確かめるサンプルコードを示す。

:download:`quantifier.py <../examples/quantifier.py>`

.. literalinclude:: ../examples/quantifier.py
   :language: python
   :linenos:

実行結果は次のとおりである。

.. code-block:: text

   ∀x ∃y (x + y = 4): True
   ∃y ∀x (x + y = 4): False
   ¬∀x (x は偶数): True
   ∃x ¬(x は偶数): True
   ∀x ∈ ∅ (x は偶数): True
   ∃x ∈ ∅ (x は偶数): False
