論理式の同値変形
================

見た目の異なる論理式が、常に同じ真理値をとることがある。本章では、そのような論理式どうしの関係を調べ、論理式を変形する規則を整理する。

恒真式と矛盾式
--------------

.. admonition:: 定義（恒真式・矛盾式・充足可能）

   命題変数の真理値をどのように定めても真になる論理式を恒真式（トートロジー）という。どのように定めても偽になる論理式を矛盾式という。真になる真理値の定め方が少なくとも 1 つある論理式を充足可能であるという。

たとえば :math:`P \lor \neg P` は恒真式であり、:math:`P \land \neg P` は矛盾式である。:math:`P \to Q` は恒真式でも矛盾式でもなく、充足可能である。

以下では、恒真式を代表する定数 :math:`\top`、矛盾式を代表する定数 :math:`\bot` も論理式として用いる。:math:`\top` は常に真、:math:`\bot` は常に偽である。

論理的同値
----------

.. admonition:: 定義（論理的同値）

   論理式 :math:`A` と :math:`B` が、命題変数の真理値のどのような定め方に対しても同じ真理値をとるとき、:math:`A` と :math:`B` は論理的に同値であるといい、:math:`A \equiv B` と書く。

:math:`A \equiv B` であることは、:math:`A \leftrightarrow B` が恒真式であることと同じである。また、:math:`A \equiv B` であることは、:math:`A` と :math:`B` の真理値表を作って最後の列が一致することを確かめれば判定できる。

記号 :math:`\equiv` は論理演算ではない点に注意する。:math:`A \leftrightarrow B` は真にも偽にもなりうる論理式だが、:math:`A \equiv B` は 2 つの論理式の間に成り立つ関係についての主張である。

同値法則
--------

よく使われる論理的同値を次の表にまとめる。これらはすべて真理値表で確かめられる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 名称
     - 法則
   * - 二重否定
     - :math:`\neg \neg P \equiv P`
   * - 交換法則
     - :math:`P \land Q \equiv Q \land P`、:math:`P \lor Q \equiv Q \lor P`
   * - 結合法則
     - :math:`(P \land Q) \land R \equiv P \land (Q \land R)`、:math:`(P \lor Q) \lor R \equiv P \lor (Q \lor R)`
   * - 分配法則
     - :math:`P \land (Q \lor R) \equiv (P \land Q) \lor (P \land R)`、:math:`P \lor (Q \land R) \equiv (P \lor Q) \land (P \lor R)`
   * - ド・モルガンの法則
     - :math:`\neg (P \land Q) \equiv \neg P \lor \neg Q`、:math:`\neg (P \lor Q) \equiv \neg P \land \neg Q`
   * - べき等法則
     - :math:`P \land P \equiv P`、:math:`P \lor P \equiv P`
   * - 吸収法則
     - :math:`P \land (P \lor Q) \equiv P`、:math:`P \lor (P \land Q) \equiv P`
   * - 排中律・矛盾律
     - :math:`P \lor \neg P \equiv \top`、:math:`P \land \neg P \equiv \bot`
   * - 定数の法則
     - :math:`P \land \top \equiv P`、:math:`P \lor \bot \equiv P`、:math:`P \land \bot \equiv \bot`、:math:`P \lor \top \equiv \top`
   * - 含意の書き換え
     - :math:`P \to Q \equiv \neg P \lor Q`
   * - 対偶
     - :math:`P \to Q \equiv \neg Q \to \neg P`
   * - 同値の書き換え
     - :math:`P \leftrightarrow Q \equiv (P \to Q) \land (Q \to P)`

例として、ド・モルガンの法則 :math:`\neg (P \land Q) \equiv \neg P \lor \neg Q` を真理値表で確かめる。左辺と右辺の列が一致している。

.. list-table::
   :header-rows: 1

   * - :math:`P`
     - :math:`Q`
     - :math:`P \land Q`
     - :math:`\neg (P \land Q)`
     - :math:`\neg P`
     - :math:`\neg Q`
     - :math:`\neg P \lor \neg Q`
   * - T
     - T
     - T
     - F
     - F
     - F
     - F
   * - T
     - F
     - F
     - T
     - F
     - T
     - T
   * - F
     - T
     - F
     - T
     - T
     - F
     - T
   * - F
     - F
     - F
     - T
     - T
     - T
     - T

論理式の一部を、それと論理的に同値な論理式で置き換えても、全体の真理値は変わらない。したがって、同値法則を繰り返し適用して論理式を変形できる。たとえば、含意の否定は次のように変形できる。

.. math::
   :nowrap:

   \[
   \begin{aligned}
   \neg (P \to Q)
   &\equiv \neg (\neg P \lor Q) && \text{（含意の書き換え）} \\
   &\equiv \neg \neg P \land \neg Q && \text{（ド・モルガンの法則）} \\
   &\equiv P \land \neg Q && \text{（二重否定）}
   \end{aligned}
   \]

つまり「:math:`P` ならば :math:`Q`」の否定は「:math:`P` ならば :math:`Q` でない」ではなく、「:math:`P` であり、かつ :math:`Q` でない」である。

同値変形はプログラムの条件式の整理にも使える。たとえば、次の 2 つの条件式は同じ意味である。

.. code-block:: python
   :linenos:

   if not (x < 0 or x > 100):
       print("範囲内")

   if x >= 0 and x <= 100:  # ド・モルガンの法則で否定を内側に移した
       print("範囲内")

さらに、Python では 2 つ目の条件式を ``0 <= x <= 100`` と書ける。

逆・裏・対偶
------------

含意 :math:`P \to Q` に対して、次の 3 つの含意を考える。

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - 名称
     - 論理式
     - :math:`P \to Q` との関係
   * - 逆
     - :math:`Q \to P`
     - 論理的に同値とは限らない
   * - 裏
     - :math:`\neg P \to \neg Q`
     - 論理的に同値とは限らない
   * - 対偶
     - :math:`\neg Q \to \neg P`
     - 論理的に同値である

たとえば、整数 :math:`x` についての命題「:math:`x = 2` ならば :math:`x^2 = 4`」は真である。その対偶「:math:`x^2 \neq 4` ならば :math:`x \neq 2`」も真である。一方、逆「:math:`x^2 = 4` ならば :math:`x = 2`」は :math:`x = -2` のときに成り立たない。

なお、逆と裏は互いに対偶の関係にあるので、逆と裏は論理的に同値である。「ある命題が真なら、その逆も真」と考えてしまう誤りは日常でもよく見られるので注意する。

標準形
------

論理式は同値変形によってさまざまな形に書き換えられる。そこで、決まった形に書き換えておくと、比較や機械的な処理がしやすくなる。

.. admonition:: 定義（リテラル・選言標準形・連言標準形）

   命題変数またはその否定をリテラルという。リテラルの論理積を、いくつか論理和で結んだ形の論理式を選言標準形という。リテラルの論理和を、いくつか論理積で結んだ形の論理式を連言標準形という。

たとえば :math:`(P \land \neg Q) \lor (\neg P \land Q)` は選言標準形、:math:`(P \lor Q) \land (\neg P \lor \neg Q)` は連言標準形である。

任意の論理式は、真理値表から次の手順で選言標準形に書き換えられる。

#. 真理値表で、論理式が T になる行をすべて選ぶ。
#. 選んだ行ごとに、その行で T の命題変数はそのまま、F の命題変数は否定をとったリテラルを作り、それらの論理積を作る。この論理積は、その行の真理値の定め方のときだけ T になる。
#. 作った論理積をすべて論理和で結ぶ。

連言標準形は逆に、論理式が F になる行に注目する。F になる行ごとに、その行でだけ F になるリテラルの論理和を作り、それらをすべて論理積で結べばよい。

例として :math:`P \leftrightarrow Q` を考える。T になる行は :math:`(P, Q) = (\mathrm{T}, \mathrm{T}), (\mathrm{F}, \mathrm{F})` なので、選言標準形は :math:`(P \land Q) \lor (\neg P \land \neg Q)` である。F になる行は :math:`(\mathrm{T}, \mathrm{F}), (\mathrm{F}, \mathrm{T})` なので、連言標準形は :math:`(\neg P \lor Q) \land (P \lor \neg Q)` である。

T になる行が 1 つも無い論理式（矛盾式）の選言標準形は :math:`\bot`、F になる行が 1 つも無い論理式（恒真式）の連言標準形は :math:`\top` とする。

連言標準形は、与えられた論理式が充足可能かどうかを判定する SAT ソルバーの入力形式として広く使われている。

真理値表から選言標準形と連言標準形を作るサンプルコードを示す。

:download:`normal_form.py <../examples/normal_form.py>`

.. literalinclude:: ../examples/normal_form.py
   :language: python
   :linenos:

実行結果は次のとおりである。

.. code-block:: text

   P ↔ Q
     選言標準形: (P ∧ Q) ∨ (¬P ∧ ¬Q)
     連言標準形: (¬P ∨ Q) ∧ (P ∨ ¬Q)
   P ⊕ Q（排他的論理和）
     選言標準形: (P ∧ ¬Q) ∨ (¬P ∧ Q)
     連言標準形: (¬P ∨ ¬Q) ∧ (P ∨ Q)
   (P ∧ Q) ∨ R
     選言標準形: (P ∧ Q ∧ R) ∨ (P ∧ Q ∧ ¬R) ∨ (P ∧ ¬Q ∧ R) ∨ (¬P ∧ Q ∧ R) ∨ (¬P ∧ ¬Q ∧ R)
     連言標準形: (¬P ∨ Q ∨ R) ∧ (P ∨ ¬Q ∨ R) ∧ (P ∨ Q ∨ R)

この方法で得られる標準形は最も短いものとは限らない。たとえば :math:`(P \land Q) \lor R` 自体も選言標準形である。

関数的完全性
------------

真理値表は、命題変数の真理値の組み合わせごとに T か F を対応させたものである。前節の手順により、どのような真理値表に対しても、それを真理値表に持つ論理式を :math:`\neg`、:math:`\land`、:math:`\lor` だけを使って作れる。このように、任意の真理値表を表せる論理演算の組を関数的完全であるという。

:math:`\{\neg, \land, \lor\}` は関数的完全である。さらに、ド・モルガンの法則と二重否定により :math:`P \lor Q \equiv \neg (\neg P \land \neg Q)` なので、:math:`\lor` は :math:`\neg` と :math:`\land` で表せる。したがって :math:`\{\neg, \land\}` だけでも関数的完全である。

論理積の否定 :math:`\neg (P \land Q)` を NAND といい、:math:`P \uparrow Q` と書く。NAND だけでも関数的完全である。実際、

.. math::

   \neg P &\equiv P \uparrow P \\
   P \land Q &\equiv (P \uparrow Q) \uparrow (P \uparrow Q)

が成り立つので、:math:`\neg` と :math:`\land` を NAND だけで表せる。デジタル回路が NAND ゲートだけで構成できるのは、この性質による。
