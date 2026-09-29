第 5 章 制御構文
================

条件分岐（if 文）
-----------------

``if`` 文を使うと、条件に応じて実行する処理を切り替えられます。条件が真のときに実行したい処理は、インデント（字下げ）して記述します。

.. code-block:: python

   score = 85

   if score >= 80:
       print("合格です。")
   elif score >= 60:
       print("再試験です。")
   else:
       print("不合格です。")

Python では、``{`` や ``}`` の代わりにインデントによって処理のまとまり（ブロック）を表します。インデントの幅がそろっていないと、エラーが発生する点に注意してください。インデントの幅は、半角空白 4 つを使うのが Python の標準的な書き方です。タブ文字を使うこともできますが、半角空白とタブ文字を混在させるとエラーの原因になるため、どちらか一方に統一してください。本資料のサンプルコードは、すべて半角空白 4 つでインデントしています。

条件式（三項演算子）
--------------------

条件によって異なる値のどちらかを選び、その結果を 1 つの式として使いたい場合は、条件式（三項演算子と呼ばれることもあります）を使用します。``真の場合の値 if 条件 else 偽の場合の値`` のように書くと、条件が真であれば前者の値、偽であれば後者の値が得られます。

.. code-block:: python

   score = 85
   result = "合格" if score >= 60 else "不合格"
   print(result)  # 合格

上記は、次の ``if`` 文と同じ結果になります。

.. code-block:: python

   score = 85
   if score >= 60:
       result = "合格"
   else:
       result = "不合格"
   print(result)  # 合格

条件式は、条件によって決まる値をそのまま変数に代入したい場合などに、簡潔に書けます。条件やそれぞれの処理が複雑になる場合は、通常の ``if`` 文を使ったほうが読みやすくなります。

条件分岐（match 文）
--------------------

Python 3.10 以降では、``match`` 文を使って条件分岐を書くこともできます。``match`` 文は、1 つの値を複数のパターンと比較して処理を分けたい場合に、``if`` 文よりも見通しよく書けることがあります。

.. code-block:: python

   number = 2

   match number:
       case 0:
           print("ゼロです。")
       case 1 | 2 | 3:
           print("1 から 3 の数値です。")
       case _:
           print("その他の数値です。")

``case`` に続けてパターンを書き、値がそのパターンに一致した場合の処理を記述します。``case _`` は、どのパターンにも一致しなかった場合に実行される、デフォルトの分岐を表します。比較したい値の候補が少ない場合は ``if`` 文、候補が多い場合や複数の値の組み合わせを扱う場合は ``match`` 文というように、状況に応じて使い分けてください。

繰り返し（for 文）
------------------

``for`` 文は、リストや文字列などの要素を 1 つずつ取り出しながら処理を繰り返す構文です。指定した回数だけ繰り返したい場合は、``range`` 関数と組み合わせます。

.. code-block:: python

   fruits = ["りんご", "みかん", "ぶどう"]
   for fruit in fruits:
       print(fruit)

   for i in range(3):
       print(i, "回目の繰り返しです。")

``range(3)`` は、0、1、2 という 3 つの数値を順番に生成します。

繰り返し（while 文）
--------------------

``while`` 文は、指定した条件が真である間、処理を繰り返す構文です。条件が偽になるまでの繰り返し回数があらかじめ分からない場合に適しています。

.. code-block:: python

   count = 0
   while count < 3:
       print("カウント:", count)
       count += 1

繰り返しの制御
--------------

繰り返しの途中で処理を制御したい場合は、``break`` 文と ``continue`` 文を使用します。``break`` 文は繰り返しそのものを終了させ、``continue`` 文はその回の処理だけを飛ばして次の繰り返しに進みます。

.. code-block:: python

   for number in range(10):
       if number == 5:
           break  # number が 5 になった時点で繰り返しを終了する
       if number % 2 == 0:
           continue  # 偶数のときは以降の処理を飛ばす
       print(number)

サンプルコード
--------------

FizzBuzz
^^^^^^^^

条件分岐と繰り返しを組み合わせた、FizzBuzz のサンプルコードです。3 の倍数のときは「Fizz」、5 の倍数のときは「Buzz」、15 の倍数のときは「FizzBuzz」を表示し、それ以外のときは数値をそのまま表示します。

:download:`fizzbuzz.py <../../examples/ch05_control_flow/fizzbuzz.py>`

.. literalinclude:: ../../examples/ch05_control_flow/fizzbuzz.py
   :language: python3
   :linenos:

曜日の判定（match 文）
^^^^^^^^^^^^^^^^^^^^^^

``match`` 文を使って、数値から曜日を求めるサンプルコードです。

:download:`match_example.py <../../examples/ch05_control_flow/match_example.py>`

.. literalinclude:: ../../examples/ch05_control_flow/match_example.py
   :language: python3
   :linenos:
