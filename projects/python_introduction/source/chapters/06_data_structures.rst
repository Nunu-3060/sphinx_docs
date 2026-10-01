第 6 章 データ構造
==================

.. _data-structures-list:

リスト
------

第 5 章「制御構文」の ``for`` 文で簡単に紹介したリストについて、ここで詳しく説明します。リストは、複数の値を順序付けて格納できるデータ構造です。角括弧 ``[]`` を使って作成し、要素の追加や変更、削除ができます。

.. code-block:: python
   :linenos:

   fruits = ["りんご", "みかん", "ぶどう"]
   print(fruits[0])       # りんご（先頭の要素）
   print(fruits[-1])      # ぶどう（末尾の要素）

   fruits.append("バナナ")  # 末尾に要素を追加する
   fruits[1] = "メロン"     # インデックス 1 の要素を変更する
   print(fruits)

リストのインデックスは 0 から始まる点に注意してください。

タプル
------

タプルは、リストと同じく複数の値を順序付けて格納できるデータ構造ですが、一度作成すると要素を変更できません。丸括弧 ``()`` を使って作成します。変更されては困る値をまとめておきたい場合に利用します。

.. code-block:: python
   :linenos:

   point = (3, 5)
   print(point[0])  # 3
   print(point[1])  # 5

辞書
----

辞書は、キーと値の組み合わせでデータを格納するデータ構造です。波括弧 ``{}`` を使って作成し、キーを指定することで対応する値を取り出せます。

.. code-block:: python
   :linenos:

   person = {"name": "佐藤", "job": "エンジニア"}
   print(person["name"])  # 佐藤

   person["age"] = 30  # 新しいキーと値を追加する
   print(person)

このように、辞書には文字列以外の値を持つキーを追加することもできます。値の型が混在する辞書に型ヒントを付ける場合は、第 4 章で説明した ``str | int`` のような書き方を組み合わせて、``dict[str, str | int]`` のように指定します。

集合
----

集合は、重複しない値の集まりを表すデータ構造です。波括弧 ``{}`` を使って作成しますが、辞書とは異なりキーを持ちません。集合を利用すると、リストから重複した値を簡単に取り除けます。

.. code-block:: python
   :linenos:

   numbers = [1, 2, 2, 3, 3, 3]
   unique_numbers = set(numbers)
   print(unique_numbers)  # {1, 2, 3}

内包表記
--------

既存のリストの各要素に処理を行った結果から、新しいリストを作成したいことがあります。この処理は、``for`` 文と ``append`` メソッドを使って、次のように書けます。

.. code-block:: python
   :linenos:

   numbers = [1, 2, 3, 4, 5]

   squares = []
   for number in numbers:
       squares.append(number ** 2)
   print(squares)  # [1, 4, 9, 16, 25]

同じ処理は、リスト内包表記という書き方を使うと、次のように 1 行で書けます。

.. code-block:: python
   :linenos:

   numbers = [1, 2, 3, 4, 5]
   squares = [number ** 2 for number in numbers]
   print(squares)  # [1, 4, 9, 16, 25]

角括弧 ``[]`` の中に、``要素に対する処理 for 要素 in リスト`` という順序で書きます。どちらの書き方でも結果は同じですが、リスト内包表記のほうが簡潔に書けるため、Python ではよく使われます。

``for`` の後ろに ``if`` を続けて書くと、条件に合う要素だけを取り出した新しいリストを作成できます。

.. code-block:: python
   :linenos:

   numbers = [1, 2, 3, 4, 5, 6]
   even_numbers = [number for number in numbers if number % 2 == 0]
   print(even_numbers)  # [2, 4, 6]

同様の書き方は、辞書や集合を作成する場合にも使えます。角括弧 ``[]`` の代わりに波括弧 ``{}`` を使い、辞書の場合はキーと値の組を ``キー: 値`` の形で書きます。

.. code-block:: python
   :linenos:

   numbers = [1, 2, 3]

   squares_dict = {number: number ** 2 for number in numbers}
   print(squares_dict)  # {1: 1, 2: 4, 3: 9}

   squares_set = {number ** 2 for number in numbers}
   print(squares_set)  # {1, 4, 9}

型ヒントを付ける
----------------

リスト、タプル、辞書、集合にも、型ヒントを付けることができます。要素の型を角括弧 ``[]`` の中に指定します。

.. list-table::
   :header-rows: 1

   * - データ構造
     - 型ヒントの例
     - 説明
   * - リスト
     - ``list[str]``
     - 文字列を要素に持つリスト
   * - タプル
     - ``tuple[int, int]``
     - 整数を 2 つ持つタプル
   * - 辞書
     - ``dict[str, int]``
     - キーが文字列、値が整数の辞書
   * - 集合
     - ``set[int]``
     - 整数を要素に持つ集合

.. code-block:: python
   :linenos:

   fruits: list[str] = ["りんご", "みかん", "ぶどう"]
   point: tuple[int, int] = (3, 5)
   scores: dict[str, int] = {"佐藤": 30, "鈴木": 25}
   numbers: set[int] = {1, 2, 3}

タプルの型ヒントは、要素の数だけ型を書き並べます。``tuple[int, int]`` は、整数を 2 つ持つタプルであることを表します。同じ型の要素がいくつ入るか決まっていないタプルを表したい場合は、``tuple[int, ...]`` のように ``...`` を使用します。

データ構造の使い分け
--------------------

それぞれのデータ構造には、次のような特徴があります。目的に応じて使い分けてください。

* 順序が重要で、後から内容を変更したい場合はリストを使用します。
* 順序が重要で、後から内容を変更したくない場合はタプルを使用します。
* キーと値の組み合わせでデータを管理したい場合は辞書を使用します。
* 値の重複を許したくない場合、または重複を取り除きたい場合は集合を使用します。

サンプルコード
--------------

リスト、タプル、辞書、集合の基本的な操作をまとめたサンプルコードです。平均点を求める ``summarize_scores`` 関数では、リストの要素の合計を求める ``sum`` 関数と、要素の個数を求める ``len`` 関数を組み合わせています。``squares_of``、``squares_dict_of``、``unique_squares_of`` の 3 つの関数では、それぞれリスト内包表記、辞書内包表記、集合内包表記を使って新しいリスト、辞書、集合を作成しています。

:download:`data_structures.py <../../examples/ch06_data_structures/data_structures.py>`

.. literalinclude:: ../../examples/ch06_data_structures/data_structures.py
   :language: python3
   :linenos:
