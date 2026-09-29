関数の設計
==========

関数は、設計の最小の単位です。関数の名前、引数、戻り値、副作用の有無を適切に決めるだけで、コードは大きく読みやすくなります。この章では、関数を設計するときの考え方を説明します。

名前を付ける
------------

関数の名前は、その関数が **何をするか** を表します。どのように実現しているか（実装の方法）は、名前に含めません。名前を読んだだけで、中身を読まずに使えるのが理想です。処理を行う関数は動詞で始めますが、計算した値を返すだけの関数は、``average`` や ``shipping_fee`` のように、返す値を表す名詞にしても構いません。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - 悪い例
     - 良い例
     - 理由
   * - ``data()``
     - ``load_sales()``
     - 何のデータを、どうするのかが分かりません。処理を行う関数の名前は、動詞で始めるのが基本です。
   * - ``check(user)``
     - ``is_active(user)``
     - 真偽値を返す関数は、``is_``、``has_``、``can_`` などで始めると、``if`` 文の中で自然に読めます。
   * - ``calc(w)``
     - ``shipping_fee(weight_kg)``
     - 省略した名前は、書いた本人以外には意味が伝わりません。単位のある値は、名前に単位を含めると誤解を防げます。
   * - ``process_list(items)``
     - ``remove_expired(items)``
     - 「処理する」「扱う」のような意味の広い言葉は、何も説明していません。
   * - ``get_and_save_user()``
     - 2 つの関数に分ける
     - 名前に「and」が入るのは、関数が 2 つのことをしている証拠です。

良い名前が思いつかない場合は、関数の役割そのものがあいまいになっている可能性があります。名前を考えることは、設計を見直すきっかけになります。

1 つの関数は 1 つのことをする
-----------------------------

関数は、1 つのことだけを行うようにします。「1 つのこと」の目安は、その関数が何をするのかを、「〜と〜をする」とつなげずに 1 文で説明できることです。

また、1 つの関数の中では、処理の **抽象度** をそろえます。次の関数では、「注文を確定する」という高い抽象度の処理と、「SQL を組み立てる」という低い抽象度の処理が混ざっています。

.. code-block:: python

   # 悪い例: 抽象度の異なる処理が混ざっている
   def place_order(order):
       validate(order)
       sql = "UPDATE orders SET status = 'placed' WHERE id = " + str(order.id)
       connection.execute(sql)
       send_confirmation(order)

.. code-block:: python

   # 良い例: 同じ抽象度の処理だけを並べる
   def place_order(order):
       validate(order)
       mark_as_placed(order)
       send_confirmation(order)

抽象度がそろっていると、関数を上から読むだけで処理の流れが分かります。詳細を知りたいときだけ、呼び出している関数の中を読めば済みます。

引数を設計する
--------------

引数は少なく
~~~~~~~~~~~~

引数が多い関数は、呼び出すときに引数の順序を間違えやすく、テストでも組み合わせが増えます。引数が 4 つ、5 つと増えてきたら、関連する引数を 1 つのデータクラスにまとめられないかを検討します（:doc:`data` を参照）。

キーワード専用引数
~~~~~~~~~~~~~~~~~~

引数の意味が値だけでは分かりにくい場合は、``*`` を使ってキーワード専用引数にします。呼び出し側に引数の名前を書かせることで、コードの意味が明確になります。

.. code-block:: python

   def resize(image, *, width: int, height: int, keep_aspect: bool = True):
       ...

   resize(image, 800, 600)                    # TypeError になる
   resize(image, width=800, height=600)       # 意味が明確

フラグ引数を避ける
~~~~~~~~~~~~~~~~~~

真偽値の引数で関数の動作を切り替える（:term:`フラグ引数`）と、呼び出し側のコードを読んだだけでは、``True`` が何を意味するのか分かりません。また、1 つの関数が 2 つのことをすることになります。このような場合は、関数を 2 つに分けます。

.. literalinclude:: ../examples/ch04_functions.py
   :language: python
   :caption: ch04_functions.py（悪い例）
   :pyobject: bad_format_name

.. literalinclude:: ../examples/ch04_functions.py
   :language: python
   :caption: ch04_functions.py（良い例）
   :start-at: def format_name_western
   :end-before: def main

可変なデフォルト引数に注意する
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python では、デフォルト引数の値は、関数を定義したときに一度だけ作られます。リストや辞書のような可変なオブジェクトをデフォルト引数にすると、すべての呼び出しで同じオブジェクトが共有されてしまいます。

.. code-block:: python

   # 悪い例: 呼び出しのたびに同じリストに追加される
   def add_tag(tag: str, tags: list[str] = []) -> list[str]:
       tags.append(tag)
       return tags

   add_tag("a")  # ['a']
   add_tag("b")  # ['a', 'b'] になってしまう

   # 良い例: None をデフォルト値にし、関数の中で新しいリストを作る
   def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
       result = [] if tags is None else list(tags)
       result.append(tag)
       return result

副作用を分離する
----------------

関数が戻り値を返す以外に、外の状態を変えることを :term:`副作用` と呼びます。引数のオブジェクトの書き換え、グローバル変数の変更、ファイルへの書き込み、画面への表示、ネットワークの通信などは、すべて副作用です。

同じ引数に対して常に同じ戻り値を返し、副作用を持たない関数を :term:`純粋関数` と呼びます。純粋関数は、引数と戻り値だけを見れば動作が分かるので、理解しやすく、テストも簡単です。

プログラムから副作用をなくすことはできません（ファイルに保存しないプログラムは役に立ちません）。目標は、副作用をなくすことではなく、**副作用を持つ部分と、純粋な計算の部分を分ける** ことです。

引数を書き換えない
~~~~~~~~~~~~~~~~~~

次の悪い例の関数は、引数で受け取ったリストの中身を書き換えます。呼び出し側は、関数を呼んだあとに元のデータが変わっていることに気付かないかもしれません。

.. literalinclude:: ../examples/ch04_functions.py
   :language: python
   :caption: ch04_functions.py（悪い例）
   :pyobject: bad_apply_discount

良い例では、元のリストは変更せず、割り引いた価格の新しいリストを作って返します。``Item`` は不変のデータクラス（``frozen=True``）なので、``dataclasses.replace`` で一部の値だけを変えた新しいオブジェクトを作ります。

.. literalinclude:: ../examples/ch04_functions.py
   :language: python
   :caption: ch04_functions.py（良い例）
   :pyobject: Item

.. literalinclude:: ../examples/ch04_functions.py
   :language: python
   :caption: ch04_functions.py（良い例）
   :pyobject: apply_discount

計算と入出力を分ける
~~~~~~~~~~~~~~~~~~~~

計算の結果を関数の中で ``print`` すると、その計算の結果をほかの用途（ファイルへの保存や、別の計算の入力）に使えず、テストで結果を確かめることも難しくなります。計算は値を返す関数にし、表示は呼び出し側で行います。

.. literalinclude:: ../examples/ch04_functions.py
   :language: python
   :caption: ch04_functions.py（悪い例）
   :pyobject: bad_print_average

.. literalinclude:: ../examples/ch04_functions.py
   :language: python
   :caption: ch04_functions.py（良い例）
   :start-at: def average
   :end-before: # ----

:download:`ch04_functions.py <../examples/ch04_functions.py>`

コマンドとクエリを分ける
~~~~~~~~~~~~~~~~~~~~~~~~

B. Meyer は、メソッドを次の 2 種類に分け、1 つのメソッドが両方を兼ねないようにすべきだと提唱しました。これを :term:`コマンドとクエリの分離` と呼びます。

* コマンド: 状態を変更します。値は返しません。
* クエリ: 値を返します。状態は変更しません。

たとえば、スタックから値を取り出す ``pop`` は、状態の変更と値の返却を兼ねています。Python の ``list.pop`` のように、実用上の理由からこの原則に従わないメソッドもあります。しかし、自分で設計するメソッドでこの原則に従えば、クエリのつもりで呼んだメソッドが状態を変えてしまう、という事態を避けられます。

早期リターンで入れ子を浅くする
------------------------------

条件の確認が入れ子になると、本来の処理がどこにあるのかが分かりにくくなります。前提条件を満たさない場合を先に処理して関数を抜ける（:term:`早期リターン`）と、入れ子が浅くなり、本来の処理が関数の最後に残ります。

.. code-block:: python

   # 悪い例: 入れ子が深い
   def withdraw(account, amount):
       if account.is_active:
           if amount > 0:
               if account.balance >= amount:
                   account.balance -= amount
               else:
                   raise ValueError("残高が足りません")
           else:
               raise ValueError("金額は正の数です")
       else:
           raise ValueError("口座が無効です")

   # 良い例: 前提条件を先に確認する
   def withdraw(account, amount):
       if not account.is_active:
           raise ValueError("口座が無効です")
       if amount <= 0:
           raise ValueError("金額は正の数です")
       if account.balance < amount:
           raise ValueError("残高が足りません")
       account.balance -= amount

型ヒントで約束を明示する
------------------------

型ヒントは、関数と呼び出し側の間の **約束** を明示します。引数に何を渡せばよいのか、戻り値として何が返るのかが、ドキュメントを読まなくても分かります。また、mypy などの型チェッカーを使えば、約束に反する呼び出しを実行前に検出できます。

型ヒントを書くときは、次の点を意識します。

* **受け取る型は広く、返す型は具体的に** します。引数を順に読むだけなら ``list[int]`` ではなく ``Iterable[int]`` や ``Sequence[int]`` にすると、タプルやジェネレーターも渡せるようになります。戻り値は、呼び出し側が使えるメソッドが多いように、具体的な型にします。
* 値がない場合があるなら、戻り値の型を ``X | None`` にします。呼び出し側は ``None`` の確認を忘れると、mypy に指摘されます。
* ``Any`` は、型の検査を止めてしまうので、できるだけ使いません。

.. code-block:: python

   from collections.abc import Iterable

   def total(prices: Iterable[int]) -> int:   # リストもタプルも渡せる
       return sum(prices)

   def find_user(user_id: int) -> User | None:  # 見つからない場合がある
       ...

エラーを伝える
--------------

関数が処理を続けられない状況（ファイルが見つからない、在庫が足りないなど）を呼び出し側に伝える方法には、主に次の 2 つがあります。

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - 方法
     - 向いている場面
     - 例
   * - 例外を送出する
     - 通常は起きない、または起きたら処理を中断すべき状況
     - 在庫が足りない、引数が不正、通信に失敗した
   * - ``None`` などの値を返す
     - 「見つからない」ことが通常の結果の 1 つである状況
     - 辞書の ``get``、検索の結果が 0 件

Python では、例外を使ってエラーを伝えるのが一般的です。エラーを表す特別な戻り値（``-1`` や空文字列など）は、呼び出し側が確認を忘れても処理が進んでしまうので避けます。

独自の例外を設計する
~~~~~~~~~~~~~~~~~~~~

アプリケーションに固有のエラーは、独自の例外クラスとして定義します。そのとき、アプリケーションの例外をすべて 1 つの基底クラスから派生させると、呼び出し側は「このアプリケーションが意図して送出したエラー」をまとめて捕捉できます。また、エラーの原因を属性として持たせると、呼び出し側はメッセージの文字列を解析せずに原因を判別できます。

.. literalinclude:: ../examples/ch04_exceptions.py
   :language: python
   :caption: ch04_exceptions.py
   :start-at: class ShopError
   :end-before: def main

.. literalinclude:: ../examples/ch04_exceptions.py
   :language: python
   :caption: ch04_exceptions.py（呼び出し側）
   :pyobject: main

:download:`ch04_exceptions.py <../examples/ch04_exceptions.py>`

``reserve`` は、``quantity`` が正でない場合には独自の例外ではなく、組み込みの ``ValueError`` を送出しています。これは、呼び出し側のプログラムの誤り（関数の使い方の誤り）であり、業務上起こり得るエラー（在庫切れ）とは性質が異なるからです。

例外を扱うときは、次の点に注意します。

* ``except Exception:`` で例外をまとめて捕捉し、何もせずに処理を続ける（例外を握りつぶす）ことは避けます。不具合の原因が分からなくなります。
* 例外を別の例外に変換して送出し直すときは、``raise NewError(...) from error`` のように ``from`` を付けて、元の例外の情報を残します。
* 捕捉するのは、その場で適切に対処できる例外だけにします。対処できない例外は、呼び出し側に伝えます。

まとめ
------

* 関数の名前は、何をするかを表します。
* 1 つの関数は 1 つのことをし、処理の抽象度をそろえます。
* 引数は少なくし、フラグ引数は避けます。
* 副作用を持つ部分と純粋な計算の部分を分けます。
* 型ヒントで、関数と呼び出し側の約束を明示します。
* エラーは例外で伝え、アプリケーションの例外は 1 つの基底クラスにまとめます。
