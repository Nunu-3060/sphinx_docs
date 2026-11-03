第 7 章 関数
============

関数とは
--------

関数とは、一連の処理をひとまとまりにして、名前を付けたものである。同じ処理を何度も使う場合に関数として定義しておくと、コードの重複を減らし、修正が必要になったときも 1 箇所を直すだけで済む。

関数の定義と呼び出し
--------------------

Python では、``def`` キーワードを使って関数を定義する。処理の結果を呼び出し元に返したい場合は、``return`` 文を使用する。

.. code-block:: python
   :linenos:

   def celsius_to_fahrenheit(celsius):
       return celsius * 9 / 5 + 32

   result = celsius_to_fahrenheit(25.0)
   print(result)  # 77.0

``def`` の後ろに関数名を書き、続く丸括弧 ``()`` の中に、関数が受け取る値を入れる変数を書く。この変数（この例では ``celsius``）を引数と呼ぶ。関数を呼び出すと、呼び出し時に渡した値（この例では ``25.0``）が引数に代入され、関数の本体の処理が実行される。``return`` の後ろに書いた式の値は、戻り値として呼び出し元に返される。この例では、戻り値の ``77.0`` が変数 ``result`` に代入される。

引数と戻り値には、次のように型ヒントを付けることもできる。型ヒントを付けることで、関数がどのような値を受け取り、どのような値を返すのかが明確になる。

.. code-block:: python
   :linenos:

   def celsius_to_fahrenheit(celsius: float) -> float:
       return celsius * 9 / 5 + 32

docstring（関数の説明文）
-------------------------

関数の定義の直後に、三重引用符（``"""``）で囲んだ文字列を書くことがある。これを docstring（ドキュメンテーション文字列）と呼び、その関数が何をするものかを説明するために使用する。

.. code-block:: python
   :linenos:

   def celsius_to_fahrenheit(celsius: float) -> float:
       """摂氏温度を華氏温度に変換して返す。"""
       return celsius * 9 / 5 + 32

docstring は、``#`` で書くコメントとは異なり、``関数名.__doc__`` として実行時に取得したり、``help(関数名)`` で内容を表示したりできる。docstring は関数だけでなく、ファイルの先頭やクラスの定義の直後にも書ける。

.. code-block:: python
   :linenos:

   """このファイル全体の説明を書く。"""

ファイルの先頭に書かれた docstring は、そのファイル（モジュール）全体の説明を表す。本資料のサンプルコードでは、ファイルの先頭とすべての関数に docstring を付けている。クラスに付ける docstring については、第 12 章「クラスとオブジェクト指向」で説明する。

pass 文
-------

Python では、``if`` 文や関数、クラスの本体を空にすることはできず、必ず何らかの文を書く必要がある。処理の内容をまだ決めていない場合の仮置きとして、何も処理を行わない ``pass`` 文を使用できる。

.. code-block:: python
   :linenos:

   def not_implemented_yet() -> None:
       pass  # TODO: 後で処理を実装する

なお、関数やクラスの本体に docstring だけを書いた場合は、その docstring 自体が有効な文として扱われるため、``pass`` を追加で書く必要はない。本資料のサンプルコードでは、この理由から、本体が空になる箇所では ``pass`` の代わりに docstring を使用している。

デフォルト引数
--------------

引数にあらかじめ値を設定しておくと、呼び出し時にその引数を省略できる。これをデフォルト引数と呼ぶ。

.. code-block:: python
   :linenos:

   def introduce(name: str, age: int = 20) -> str:
       return "私は " + name + " です。年齢は " + str(age) + " 歳です。"

   print(introduce("鈴木"))       # age は省略され、20 が使われる
   print(introduce("田中", 35))   # age に 35 が指定される

キーワード引数
--------------

これまでの例のように、引数の値を順番に並べて渡す方法のほかに、``引数名=値`` の形で引数を指定して渡す方法もある。この方法で渡す引数をキーワード引数と呼ぶ。キーワード引数を使うと、どの引数にどの値を渡しているかが分かりやすくなり、引数の順番を入れ替えて書くこともできる。

.. code-block:: python
   :linenos:

   print(introduce(name="田中", age=35))  # 私は 田中 です。年齢は 35 歳です。
   print(introduce(age=35, name="田中"))  # 同じ結果になる

None を使ったオプション引数
----------------------------

第 4 章で説明した ``str | None`` のような型ヒントは、値が指定されないかもしれない引数のデフォルト値として ``None`` を使いたい場合によく使われる。

.. code-block:: python
   :linenos:

   def greet(name: str, nickname: str | None = None) -> str:
       if nickname is None:
           return name + " です。"
       return name + "（" + nickname + "）です。"

   print(greet("田中"))            # 田中 です。
   print(greet("田中", "たなか"))  # 田中（たなか）です。

引数 ``nickname`` を省略すると、デフォルト値の ``None`` が使われる。関数の内部では、``if`` 文で ``nickname`` が ``None`` かどうかを判定し、処理を分けている。

可変長引数
----------

引数の数があらかじめ決まっていない場合は、``*`` を付けた可変長引数を使用する。可変長引数は、関数の内部ではタプルとして扱われる。

.. code-block:: python
   :linenos:

   def total(*numbers: int) -> int:
       return sum(numbers)

   print(total(1, 2, 3, 4, 5))  # 15

可変長のキーワード引数
-----------------------

キーワード引数の数があらかじめ決まっていない場合は、``**`` を付けた可変長のキーワード引数を使用する。可変長のキーワード引数は、関数の内部では辞書として扱われる。

.. code-block:: python
   :linenos:

   def show_profile(**info: str) -> dict[str, str]:
       return info

   print(show_profile(name="田中", city="東京"))
   # {'name': '田中', 'city': '東京'}

ラムダ式（無名関数）
--------------------

``lambda`` を使うと、名前を付けずに、その場限りの小さな関数（無名関数）を作成できる。``lambda 引数: 式`` という形式で書き、式を評価した結果がそのまま戻り値になる。

.. code-block:: python
   :linenos:

   add_one = lambda number: number + 1
   print(add_one(5))  # 6

上記は、次の関数定義と同じ処理である。

.. code-block:: python
   :linenos:

   def add_one(number: int) -> int:
       return number + 1

   print(add_one(5))  # 6

ラムダ式は、``return`` 文を書かずに 1 つの式だけで戻り値を表す点や、型ヒントを付けられない点が、``def`` を使った通常の関数定義と異なる。複雑な処理を書きたい場合や、同じ処理を繰り返し呼び出したい場合は、``def`` を使った通常の関数定義を使用するとよい。ラムダ式は、``sorted`` 関数の ``key`` 引数のように、他の関数に処理の内容だけを短く渡したい場面でよく使われる。

サンプルコード
--------------

関数の定義と、デフォルト引数や可変長引数、可変長のキーワード引数、``None`` を使ったオプション引数など、さまざまな引数の使い方をまとめたサンプルコードである。

:download:`functions.py <../../examples/ch07_functions/functions.py>`

.. literalinclude:: ../../examples/ch07_functions/functions.py
   :language: python3
   :linenos:
