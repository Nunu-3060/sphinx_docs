==========================================
関数を小さく分ける
==========================================

1 つの関数にたくさんの処理を詰め込むと、その関数は長く、複雑になる。長い関数は、全体を理解するのに時間がかかり、一部を変更したときの影響も分かりにくい。この章では、関数を小さく分ける方法を説明する。

悪い例
==========================================

次のコードは、商品の一覧（商品名、単価、個数の組）を受け取り、レシートを表示する。合計金額が 5000 円以上の場合は 10% 割り引く。

.. literalinclude:: ../examples/ch06_functions_bad.py
   :language: python
   :linenos:
   :caption: ch06_functions_bad.py

:download:`ch06_functions_bad.py をダウンロードする <../examples/ch06_functions_bad.py>`

実行結果は次のとおりである。

.. code-block:: text
   :linenos:

   不正な商品: 消しゴム
   ノート x10 = 1500円
   ペン x30 = 3600円
   割引: 510円
   合計: 4590円

関数 ``process`` は、次の 5 つの役割を 1 つの関数で担っている。

#. 商品のデータが正しいかを確認する（8 行目から 10 行目）。
#. 小計と合計を計算する（11 行目と 12 行目）。
#. 表示用の文字列を作る（13 行目）。
#. 割引額を計算する（14 行目から 18 行目）。
#. 結果を表示する（19 行目から 22 行目）。

このように役割が混ざっていると、例えば「割引の条件を変えたい」ときに、関数全体を読んで割引に関係する部分を探さなければならない。また、関数名 ``process``\ （処理する）からは、何をする関数なのかが分からない。

良い例
==========================================

.. literalinclude:: ../examples/ch06_functions_good.py
   :language: python
   :linenos:
   :caption: ch06_functions_good.py

:download:`ch06_functions_good.py をダウンロードする <../examples/ch06_functions_good.py>`

それぞれの役割を、名前の付いた小さな関数に分けた。関数どうしの呼び出し関係を :numref:`fig-receipt-functions` に示す。

.. graphviz::
   :caption: 関数の呼び出し関係
   :alt: print_receipt が is_valid_item、subtotal_of、calculate_discount、format_item_line を呼び出し、format_item_line が subtotal_of を呼び出す関係を示す図
   :name: fig-receipt-functions

   digraph receipt {
       graph [rankdir=LR, fontname="Yu Gothic", nodesep=0.3, ranksep=0.6];
       node [shape=box, style="rounded,filled", fillcolor="#e8f0fe", color="#1f77b4", fontname="Yu Gothic", fontsize=11];
       edge [color="#555555"];

       print_receipt [label="print_receipt\nレシートを表示する", fillcolor="#fff3cd", color="#b8860b"];
       is_valid_item [label="is_valid_item\n商品が正しいか調べる"];
       subtotal_of [label="subtotal_of\n小計を求める"];
       calculate_discount [label="calculate_discount\n割引額を求める"];
       format_item_line [label="format_item_line\n1 行分の文字列を作る"];

       print_receipt -> is_valid_item;
       print_receipt -> subtotal_of;
       print_receipt -> calculate_discount;
       print_receipt -> format_item_line;
       format_item_line -> subtotal_of;
   }

関数 ``print_receipt`` を読むと、「正しくない商品を報告し、合計と割引額を求め、結果を表示する」という処理の流れが分かる。細かい計算の方法を知りたいときだけ、それぞれの関数を読めばよい。割引の条件を変えたいときは、``calculate_discount`` と定数だけを見ればよい。

1 つの関数には 1 つの役割を持たせる
==========================================

関数を分けるときの基本は、1 つの関数には 1 つの役割だけを持たせることである。役割が 1 つであれば、その役割を表す名前を付けやすい。逆に、関数に良い名前が付けられないときは、その関数が複数の役割を持っている可能性がある。名前に「and」が入ってしまう場合も同様である。

関数を小さく分けると、次の利点がある。

* 関数の名前が、処理の内容の説明になる。
* 1 つの関数が短くなり、理解しやすくなる。
* 変更が必要なとき、直す場所を特定しやすく、影響の範囲も限られる。
* 同じ処理を別の場所でも使える。例えば ``subtotal_of`` は ``print_receipt`` と ``format_item_line`` の両方から使われている。
* 関数ごとに動作を確かめられるため、テストしやすい（第 11 章を参照）。

関数の長さについて決まった基準は無いが、画面をスクロールせずに全体を見渡せる長さが 1 つの目安になる。

計算と表示を分ける
==========================================

悪い例の ``process`` は、計算と表示を 1 つの関数で行っている。このような関数は、計算結果を画面に表示する以外の用途（ファイルへの保存など）に使えず、計算が正しいかどうかを確かめるには、表示された文字を目で確認するしかない。

良い例では、``calculate_discount`` は値を受け取って値を返すだけで、画面への表示は ``print_receipt`` にまとめている。関数の外の状態を変える動作（画面への表示、ファイルへの書き込み、グローバル変数の変更など）を :term:`副作用` と呼ぶ。副作用を持つ処理と持たない処理を分けておくと、副作用の無い関数は、同じ引数に対して必ず同じ値を返すため、動作を理解しやすく、テストもしやすい。

引数は少なくする
==========================================

引数が多い関数は、呼び出すときに引数の順番や意味を間違えやすい。

.. code-block:: python
   :linenos:
   :caption: 悪い例

   create_user("山田", "太郎", 20, True, False, "東京都")

この呼び出しを見ても、``True`` と ``False`` が何を意味するのか分からない。次のような方法で改善できる。

* 関数が多くの役割を持っていないか見直し、分けられないか考える。
* 関係の深い引数を 1 つのデータにまとめる（第 9 章を参照）。
* キーワード引数を使って呼び出し、引数の意味を明示する。

.. code-block:: python
   :linenos:
   :caption: キーワード引数を使った例

   create_user(
       family_name="山田",
       given_name="太郎",
       age=20,
       is_admin=True,
       receives_newsletter=False,
       prefecture="東京都",
   )

型ヒントを書く
==========================================

本書のサンプルコードでは、関数の引数と戻り値に :term:`型ヒント` を付けている。

.. code-block:: python
   :linenos:

   def calculate_discount(total: int) -> int:
       ...

``total: int`` は「引数 ``total`` は整数」であることを、``-> int`` は「戻り値は整数」であることを表す。型ヒントを書くと、関数の使い方がコードから分かるようになる。また、第 11 章で紹介する mypy などの道具を使えば、型の誤りを実行前に見つけられる。

型ヒントは Python の実行時には検査されない。間違った型の値を渡しても、そのまま実行される点に注意が必要である。

まとめ
==========================================

* 1 つの関数には 1 つの役割を持たせ、その役割を表す名前を付ける。
* 良い名前が付けられない関数は、役割が多すぎないか見直す。
* 計算などの処理と、表示などの副作用を持つ処理を分ける。
* 引数が多くなりすぎないようにし、必要に応じてキーワード引数を使う。
* 引数と戻り値には型ヒントを書く。
