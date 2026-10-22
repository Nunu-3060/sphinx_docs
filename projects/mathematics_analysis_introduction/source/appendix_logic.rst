付録 B 論理と証明の基本
=======================

解析学の定義や定理は、「任意の」「存在する」「ならば」といった言葉を組み合わせて書かれる。本付録では、それらを正確に読み書きするための最低限の論理と、本書で使う証明の方法をまとめる。特に、ε-N 論法や ε-δ 論法の\ **否定**\ を正しく作れることは、反例を示したり背理法を使ったりするために欠かせない。

命題と論理記号
--------------

真か偽かが定まる主張を\ **命題**\ という。たとえば「:math:`2 < 3`」は真の命題、「:math:`\sqrt{2}` は有理数である」は偽の命題である。命題 :math:`P, Q` から、次のような新しい命題を作ることができる。

.. list-table:: 論理記号
   :name: appB-tab-connectives
   :header-rows: 1
   :widths: 20 30 50

   * - 記号
     - 読み方
     - 真となる条件
   * - :math:`\neg P`
     - :math:`P` でない
     - :math:`P` が偽のとき
   * - :math:`P \land Q`
     - :math:`P` かつ :math:`Q`
     - :math:`P` と :math:`Q` がともに真のとき
   * - :math:`P \lor Q`
     - :math:`P` または :math:`Q`
     - :math:`P` と :math:`Q` の少なくとも一方が真のとき
   * - :math:`P \Rightarrow Q`
     - :math:`P` ならば :math:`Q`
     - :math:`P` が偽であるか、:math:`Q` が真であるとき
   * - :math:`P \Leftrightarrow Q`
     - :math:`P` と :math:`Q` は同値
     - :math:`P` と :math:`Q` の真偽が一致するとき

数学の「または」は、両方が成り立つ場合を含む。また、:math:`P \Rightarrow Q` は :math:`P` が偽ならば :math:`Q` の真偽によらず真とみなす。「:math:`x > 2` ならば :math:`x^2 > 4`」という命題は、:math:`x = 1` のように仮定を満たさない場合には何も主張していない、と考えればよい。

:math:`P \Rightarrow Q` が真であるとき、:math:`P` は :math:`Q` であるための\ **十分条件**、:math:`Q` は :math:`P` であるための\ **必要条件**\ であるという。:math:`P \Leftrightarrow Q` のときは\ **必要十分条件**\ であるという。

否定については、次の\ **ド・モルガンの法則**\ が基本である。

.. math::

   \neg (P \land Q) \Leftrightarrow (\neg P) \lor (\neg Q), \qquad \neg (P \lor Q) \Leftrightarrow (\neg P) \land (\neg Q)

また、:math:`P \Rightarrow Q` の否定は「:math:`P` であるのに :math:`Q` でない」、すなわち :math:`P \land \neg Q` である。

逆・裏・対偶
------------

命題 :math:`P \Rightarrow Q` に対して、:math:`Q \Rightarrow P` を\ **逆**、:math:`\neg P \Rightarrow \neg Q` を\ **裏**、:math:`\neg Q \Rightarrow \neg P` を\ **対偶**\ という。もとの命題と対偶は常に真偽が一致するが、逆や裏は一致するとは限らない。

.. admonition:: 例 B.1
   :class: example

   「数列が収束するならば、その数列は有界である」（:ref:`定理 2.2 <ch02-thm-bounded>`）は真である。その対偶「数列が有界でないならば、その数列は収束しない」も真である。一方、逆「有界な数列は収束する」は偽であり、:math:`(-1)^n` が反例となる。

量化子
------

「任意の :math:`x` について :math:`P(x)`」を :math:`\forall x,\ P(x)` と書き、「ある :math:`x` が存在して :math:`P(x)`」を :math:`\exists x,\ P(x)` と書く。:math:`\forall` を\ **全称量化子**、:math:`\exists` を\ **存在量化子**\ という。

量化子の順序
^^^^^^^^^^^^

量化子が複数あるときは、その\ **順序**\ が意味を大きく変える。次の 2 つの命題を比べる。

.. math::

   \text{(a)}\ \ \forall x \in \mathbb{R},\ \exists y \in \mathbb{R},\ y > x \qquad \text{(b)}\ \ \exists y \in \mathbb{R},\ \forall x \in \mathbb{R},\ y > x

(a) は「どの実数 :math:`x` に対しても、それより大きい :math:`y` がある」という意味であり、真である（:math:`y = x + 1` とすればよい）。(b) は「すべての実数より大きい :math:`y` がある」という意味であり、偽である。(a) では :math:`y` を :math:`x` に応じて選んでよいが、(b) では :math:`y` を先に 1 つ決めなければならない。

数列の収束の定義（:ref:`定義 2.1 <ch02-def-convergence>`）は :math:`\forall \varepsilon > 0,\ \exists N,\ \forall n \geq N,\ |a_n - \alpha| < \varepsilon` である。ここで :math:`N` は :math:`\varepsilon` に応じて選んでよい。

量化子を含む命題の否定
^^^^^^^^^^^^^^^^^^^^^^

量化子を含む命題の否定は、次の規則で作る。

.. math::

   \neg (\forall x,\ P(x)) \Leftrightarrow \exists x,\ \neg P(x), \qquad \neg (\exists x,\ P(x)) \Leftrightarrow \forall x,\ \neg P(x)

「すべての :math:`x` で :math:`P(x)` が成り立つ」の否定は「:math:`P(x)` が成り立たない :math:`x` がある」であり、「:math:`P(x)` を満たす :math:`x` がある」の否定は「どの :math:`x` も :math:`P(x)` を満たさない」である。量化子が複数ある場合は、この規則を外側から順に適用する。結果として、**すべての** :math:`\forall` **と** :math:`\exists` **を入れ替え、最後の条件を否定する**\ ことになる。

ε-N 論法の否定
--------------

以上の規則を使って、「数列 :math:`(a_n)` は :math:`\alpha` に収束しない」を書き下す。収束の定義は次のとおりである。

.. math::

   \forall \varepsilon > 0,\ \exists N \in \mathbb{N},\ \forall n \geq N,\ |a_n - \alpha| < \varepsilon

量化子を入れ替え、最後の不等式を否定すると、次を得る。

.. math::
   :label: appB-eq-not-converge

   \exists \varepsilon > 0,\ \forall N \in \mathbb{N},\ \exists n \geq N,\ |a_n - \alpha| \geq \varepsilon

言葉で言えば、「ある正の数 :math:`\varepsilon` があって、どんなに大きい :math:`N` をとっても、:math:`N` 以降に :math:`\alpha` から :math:`\varepsilon` 以上離れた項が現れる」ということである。:math:`|a_n - \alpha| < \varepsilon` の否定が :math:`|a_n - \alpha| \geq \varepsilon`\ （:math:`>` ではない）であることにも注意する。

.. admonition:: 例 B.2
   :class: example

   :math:`a_n = (-1)^n` がどの実数 :math:`\alpha` にも収束しないことを、式 :eq:`appB-eq-not-converge` に沿って示す。:math:`\varepsilon = 1` とし、任意の :math:`N` をとる。:math:`a_N` と :math:`a_{N+1}` の一方は :math:`1`、他方は :math:`-1` である。もし両方とも :math:`|a_n - \alpha| < 1` を満たすなら、:math:`2 = |a_N - a_{N+1}| \leq |a_N - \alpha| + |\alpha - a_{N+1}| < 2` となって矛盾する。したがって :math:`n = N` または :math:`n = N + 1` のどちらかで :math:`|a_n - \alpha| \geq 1` となる。

同じ方法で、ほかの定義の否定も作れる。たとえば、関数 :math:`f` が点 :math:`a` で連続であること（ε-δ 論法、第 4 章）は

.. math::

   \forall \varepsilon > 0,\ \exists \delta > 0,\ \forall x,\ \bigl( |x - a| < \delta \Rightarrow |f(x) - f(a)| < \varepsilon \bigr)

であり、その否定「:math:`f` は :math:`a` で連続でない」は、:math:`P \Rightarrow Q` の否定が :math:`P \land \neg Q` であることに注意すると、次のようになる。

.. math::

   \exists \varepsilon > 0,\ \forall \delta > 0,\ \exists x,\ \bigl( |x - a| < \delta \land |f(x) - f(a)| \geq \varepsilon \bigr)

証明の方法
----------

本書で使う主な証明の方法をまとめる。

直接証明
^^^^^^^^

仮定 :math:`P` から出発し、既知の事実を組み合わせて結論 :math:`Q` を導く方法である。ε-N 論法による収束の証明は、多くの場合「:math:`\varepsilon > 0` を任意にとる」から始め、条件を満たす :math:`N` を具体的に作って示す直接証明である。

対偶による証明
^^^^^^^^^^^^^^

:math:`P \Rightarrow Q` の代わりに、同値な対偶 :math:`\neg Q \Rightarrow \neg P` を示す方法である。

.. admonition:: 例 B.3
   :class: example

   整数 :math:`n` について「:math:`n^2` が偶数ならば :math:`n` は偶数」を示す。対偶「:math:`n` が奇数ならば :math:`n^2` は奇数」を示せばよい。:math:`n = 2k + 1` とすると :math:`n^2 = 2(2k^2 + 2k) + 1` であり、奇数である。

背理法
^^^^^^

結論 :math:`Q` を否定した :math:`\neg Q` を仮定し、矛盾を導くことで :math:`Q` を示す方法である。:ref:`定理 1.1 <ch01-thm-sqrt2-irrational>`\ （:math:`\sqrt{2}` の無理性）や\ :ref:`定理 2.1 <ch02-thm-unique>`\ （極限の一意性）は背理法による証明である。背理法では、結論の否定を正確に作ることが出発点になる。

数学的帰納法
^^^^^^^^^^^^

自然数 :math:`n` に関する命題 :math:`P(n)` がすべての :math:`n \in \mathbb{N}` で成り立つことを示すには、次の 2 つを示せばよい。

1. :math:`P(1)` が成り立つ。
2. 任意の :math:`n` について、:math:`P(n)` が成り立つならば :math:`P(n + 1)` も成り立つ。

.. admonition:: 例 B.4
   :class: example

   :math:`1 + 2 + \cdots + n = n(n + 1)/2` を示す。:math:`n = 1` では両辺とも :math:`1` である。:math:`n` で成り立つと仮定すると、:math:`1 + \cdots + n + (n + 1) = n(n + 1)/2 + (n + 1) = (n + 1)(n + 2)/2` となり、:math:`n + 1` でも成り立つ。

漸化式で定まる数列の性質（:ref:`例 2.6 <ch02-ex-newton>` など）や、ベルヌーイの不等式（:ref:`補題 2.6 <ch02-lem-bernoulli>`）は、数学的帰納法で示される。

反例
^^^^

「すべての :math:`x` について :math:`P(x)`」が偽であることを示すには、:math:`P(x)` が成り立たない :math:`x` を 1 つ挙げればよい。これを\ **反例**\ という。本書では、定理の仮定を外すと結論が成り立たなくなることを、反例によって繰り返し示す。
