記号一覧
========

本書で使う主な記号をまとめる。

集合と論理
----------

.. list-table:: 集合と論理の記号
   :header-rows: 1
   :widths: 25 55 20

   * - 記号
     - 意味
     - 初出
   * - :math:`a \in A`
     - :math:`a` は集合 :math:`A` の要素である
     - 第 2 章
   * - :math:`\emptyset`
     - 空集合
     - 第 2 章
   * - :math:`A \cup B`\ 、\ :math:`A \cap B`\ 、\ :math:`A \setminus B`
     - 和集合、共通部分、差集合
     - 第 2 章
   * - :math:`A \subseteq B`
     - :math:`A` は :math:`B` の部分集合である
     - 第 2 章
   * - :math:`A \times B`
     - 直積
     - 第 2 章
   * - :math:`2^A`
     - :math:`A` のべき集合
     - 第 2 章
   * - :math:`|A|`
     - 集合 :math:`A` の要素数
     - 第 2 章
   * - :math:`\overline{A}`
     - 集合（言語）\ :math:`A` の補集合
     - 第 8 章
   * - :math:`f : A \to B`
     - :math:`A` から :math:`B` への関数
     - 第 2 章
   * - :math:`\lor`\ 、\ :math:`\land`\ 、\ :math:`\neg`
     - 論理和（または）、論理積（かつ）、否定
     - 第 11 章
   * - :math:`\lfloor x \rfloor`
     - :math:`x` 以下の最大の整数（床関数）
     - 第 3 章
   * - :math:`a \bmod n`
     - :math:`a` を :math:`n` で割った余り
     - 第 8 章
   * - :math:`a \equiv b \pmod n`
     - :math:`a` と :math:`b` は :math:`n` を法として合同である（\ :math:`n` で割った余りが等しい）
     - 第 12 章

計算量
------

.. list-table:: 計算量の記号
   :header-rows: 1
   :widths: 25 55 20

   * - 記号
     - 意味
     - 初出
   * - :math:`O(g(n))`
     - 増え方が :math:`g(n)` 以下である（漸近的上界）
     - 第 2 章
   * - :math:`\Omega(g(n))`
     - 増え方が :math:`g(n)` 以上である（漸近的下界）
     - 第 2 章
   * - :math:`\Theta(g(n))`
     - 増え方が :math:`g(n)` と等しい
     - 第 2 章
   * - :math:`\log n`
     - 底が 2 の対数（漸近記法の中では底を区別しない）
     - 第 1 章
   * - :math:`n`
     - 入力サイズ
     - 第 2 章
   * - :math:`V`\ 、\ :math:`E`
     - グラフの頂点の集合と辺の集合。計算量の式の中では頂点数と辺の数を表す
     - 第 2 章
   * - :math:`\alpha(n)`
     - 逆アッカーマン関数
     - 第 4 章

形式言語と計算モデル
--------------------

.. list-table:: 形式言語と計算モデルの記号
   :header-rows: 1
   :widths: 25 55 20

   * - 記号
     - 意味
     - 初出
   * - :math:`\Sigma`
     - アルファベット（入力記号の集合）
     - 第 8 章
   * - :math:`\Sigma^*`
     - :math:`\Sigma` 上の文字列全体の集合
     - 第 8 章
   * - :math:`\varepsilon`
     - 空列
     - 第 8 章
   * - :math:`|w|`
     - 文字列 :math:`w` の長さ
     - 第 8 章
   * - :math:`w^R`
     - 文字列 :math:`w` を逆順にした文字列
     - 第 9 章
   * - :math:`a^n`
     - 記号 :math:`a` を :math:`n` 個並べた文字列
     - 第 8 章
   * - :math:`L(M)`
     - 計算モデル :math:`M` が認識する言語、または文法が生成する言語
     - 第 8 章
   * - :math:`\delta`
     - 遷移関数
     - 第 8 章
   * - :math:`q_0`
     - 開始状態
     - 第 8 章
   * - :math:`A \to \alpha`
     - 生成規則
     - 第 9 章
   * - :math:`\Rightarrow`
     - 導出の 1 ステップ
     - 第 9 章
   * - :math:`\sqcup`
     - チューリング機械のテープの空白記号（サンプルコードでは ``_``\ ）
     - 第 10 章
   * - :math:`\langle M \rangle`
     - チューリング機械 :math:`M` を文字列として符号化したもの
     - 第 10 章
   * - :math:`A \le_m B`
     - :math:`A` は :math:`B` に写像還元できる
     - 第 10 章
   * - :math:`A \le_p B`
     - :math:`A` は :math:`B` に多項式時間還元できる
     - 第 11 章
