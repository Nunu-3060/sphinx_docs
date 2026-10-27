付録 A 記号一覧
===============

本書で用いた記号を、初出の章の順にまとめる。「Python」の列は、対応する Python の書き方がある場合に記載した。

論理
----

.. list-table::
   :header-rows: 1
   :widths: 15 25 20 20 20

   * - 記号
     - 意味・読み方
     - LaTeX
     - Python
     - 初出
   * - :math:`\neg P`
     - 否定（:math:`P` でない）
     - ``\neg``
     - ``not p``
     - :doc:`proposition`
   * - :math:`P \land Q`
     - 論理積（:math:`P` かつ :math:`Q`）
     - ``\land``
     - ``p and q``
     - :doc:`proposition`
   * - :math:`P \lor Q`
     - 論理和（:math:`P` または :math:`Q`）
     - ``\lor``
     - ``p or q``
     - :doc:`proposition`
   * - :math:`P \to Q`
     - 含意（:math:`P` ならば :math:`Q`）
     - ``\to``
     - ``not p or q``
     - :doc:`proposition`
   * - :math:`P \leftrightarrow Q`
     - 同値
     - ``\leftrightarrow``
     - ``p == q``
     - :doc:`proposition`
   * - :math:`P \oplus Q`
     - 排他的論理和
     - ``\oplus``
     - ``p != q``
     - :doc:`proposition`
   * - :math:`\top`、:math:`\bot`
     - 恒真、恒偽
     - ``\top``、``\bot``
     - ``True``、``False``
     - :doc:`equivalence`
   * - :math:`A \equiv B`
     - 論理的同値
     - ``\equiv``
     -
     - :doc:`equivalence`
   * - :math:`P \uparrow Q`
     - NAND
     - ``\uparrow``
     - ``not (p and q)``
     - :doc:`equivalence`
   * - :math:`\forall x \, P(x)`
     - 全称量化子（すべての :math:`x` について）
     - ``\forall``
     - ``all(...)``
     - :doc:`predicate`
   * - :math:`\exists x \, P(x)`
     - 存在量化子（ある :math:`x` について）
     - ``\exists``
     - ``any(...)``
     - :doc:`predicate`
   * - :math:`\exists! \, x \, P(x)`
     - :math:`P(x)` を満たす :math:`x` がただ 1 つ存在する
     - ``\exists!``
     -
     - :doc:`mapping`

集合
----

.. list-table::
   :header-rows: 1
   :widths: 15 25 20 20 20

   * - 記号
     - 意味・読み方
     - LaTeX
     - Python
     - 初出
   * - :math:`\mathbb{N}`、:math:`\mathbb{Z}`、:math:`\mathbb{Q}`、:math:`\mathbb{R}`
     - 自然数（0 を含む）、整数、有理数、実数の全体
     - ``\mathbb{N}`` など
     -
     - :doc:`introduction`
   * - :math:`a \in A`
     - :math:`a` は :math:`A` の要素である
     - ``\in``
     - ``a in s``
     - :doc:`set`
   * - :math:`a \notin A`
     - :math:`a` は :math:`A` の要素でない
     - ``\notin``
     - ``a not in s``
     - :doc:`set`
   * - :math:`\{x \in A \mid P(x)\}`
     - 内包的記法
     - ``\{x \in A \mid P(x)\}``
     - ``{x for x in a if p(x)}``
     - :doc:`set`
   * - :math:`A \subseteq B`
     - :math:`A` は :math:`B` の部分集合である
     - ``\subseteq``
     - ``a <= b``
     - :doc:`set`
   * - :math:`A \subsetneq B`
     - :math:`A` は :math:`B` の真部分集合である
     - ``\subsetneq``
     - ``a < b``
     - :doc:`set`
   * - :math:`\emptyset`
     - 空集合
     - ``\emptyset``
     - ``set()``
     - :doc:`set`
   * - :math:`A \cup B`
     - 和集合
     - ``\cup``
     - ``a | b``
     - :doc:`set`
   * - :math:`A \cap B`
     - 共通部分
     - ``\cap``
     - ``a & b``
     - :doc:`set`
   * - :math:`A \setminus B`
     - 差集合
     - ``\setminus``
     - ``a - b``
     - :doc:`set`
   * - :math:`A^{c}`
     - 補集合
     - ``A^{c}``
     - ``u - a``
     - :doc:`set`
   * - :math:`A \triangle B`
     - 対称差
     - ``\triangle``
     - ``a ^ b``
     - :doc:`set`
   * - :math:`\mathcal{P}(A)`
     - べき集合
     - ``\mathcal{P}(A)``
     -
     - :doc:`set`
   * - :math:`(a, b)`
     - 順序対
     - ``(a, b)``
     - ``(a, b)``
     - :doc:`set`
   * - :math:`A \times B`
     - 直積
     - ``\times``
     - ``itertools.product(a, b)``
     - :doc:`set`
   * - :math:`a \, R \, b`
     - :math:`a` と :math:`b` は関係 :math:`R` にある
     - ``a \, R \, b``
     - ``(a, b) in r``
     - :doc:`relation`
   * - :math:`[a]`
     - :math:`a` の同値類
     - ``[a]``
     -
     - :doc:`relation`
   * - :math:`A / R`
     - 商集合
     - ``A / R``
     -
     - :doc:`relation`
   * - :math:`S \circ R`
     - 関係の合成
     - ``\circ``
     -
     - :doc:`relation`
   * - :math:`f \colon A \to B`
     - :math:`A` から :math:`B` への写像
     - ``f \colon A \to B``
     -
     - :doc:`mapping`
   * - :math:`a \mapsto f(a)`
     - :math:`a` を :math:`f(a)` に対応させる
     - ``\mapsto``
     - ``lambda a: f(a)``
     - :doc:`mapping`
   * - :math:`f(X)`、:math:`f^{-1}(Y)`
     - 像、逆像
     - ``f^{-1}(Y)``
     -
     - :doc:`mapping`
   * - :math:`g \circ f`
     - 合成写像
     - ``\circ``
     - ``lambda a: g(f(a))``
     - :doc:`mapping`
   * - :math:`\mathrm{id}_A`
     - 恒等写像
     - ``\mathrm{id}_A``
     -
     - :doc:`mapping`
   * - :math:`f^{-1}`
     - 逆写像
     - ``f^{-1}``
     -
     - :doc:`mapping`
   * - :math:`|A|`
     - 要素数、濃度
     - ``|A|``
     - ``len(a)``
     - :doc:`cardinality`
