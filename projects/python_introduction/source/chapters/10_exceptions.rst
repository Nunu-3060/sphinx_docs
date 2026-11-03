第 10 章 例外処理
=================

例外とは
--------

プログラムの実行中に発生するエラーのことを、Python では例外（exception）と呼ぶ。たとえば、0 で割り算をしようとしたときや、存在しないファイルを開こうとしたときに例外が発生する。例外が発生すると、対処をしない限りプログラムはそこで終了してしまう。

エラーメッセージ（トレースバック）の読み方
--------------------------------------------

発生した例外が対処されなかった場合、Python はエラーの内容を「トレースバック（traceback）」と呼ばれる形式でコンソールに表示し、プログラムを終了する。次のプログラムを例に、トレースバックの読み方を説明する。

.. code-block:: python
   :linenos:

   def divide(a: int, b: int) -> float:
       return a / b


   print(divide(10, 0))

このプログラムを実行すると、次のようなトレースバックが表示される。

.. code-block:: console

   $ python example.py
   Traceback (most recent call last):
     File "C:\work\example.py", line 5, in <module>
       print(divide(10, 0))
             ~~~~~~^^^^^^^
     File "C:\work\example.py", line 2, in divide
       return a / b
              ~~^~~
   ZeroDivisionError: division by zero

トレースバックは、まず一番下の行に注目して読む。``ZeroDivisionError: division by zero`` の部分が、発生した例外の種類（``ZeroDivisionError``）と、その内容を説明するメッセージ（``division by zero``）である。どのような種類のエラーが起きたのかは、まずここで確認できる。

続いて、``File "...", line ..., in ...`` という行に注目する。これは、例外に関係する処理が書かれているファイル名、行番号、関数名を表している。ファイル名は、実行したファイルの場所（この例では ``C:\work``）を含めて表示される。トレースバックには、呼び出し元をさかのぼる形で複数の行が表示される。一番下に近い ``File`` の行（この例では 2 行目の ``return a / b``）が、実際に例外が発生した箇所である。``~`` と ``^`` の記号は、エラーの原因となった式の位置を示しており、``^`` が付いた部分が直接の原因である。この記号による位置の表示は、Python 3.11 から追加された機能である。また、Python 3.13 以降では、対応するコマンドラインでトレースバックが色付きで表示される。

代表的な例外の種類には、次のようなものがある。

.. list-table::
   :header-rows: 1

   * - 例外の種類
     - 主な原因
   * - ``ZeroDivisionError``
     - 0 で割り算をした
   * - ``TypeError``
     - データ型が処理に適していない
   * - ``ValueError``
     - 値の型は正しいが、内容が処理に適していない
   * - ``NameError``
     - 定義されていない変数や関数を参照した
   * - ``FileNotFoundError``
     - 指定したファイルが見つからない
   * - ``KeyError``
     - 辞書に存在しないキーを指定した
   * - ``IndexError``
     - リストなどの範囲外のインデックスを指定した

エラーが発生した場合は、まず例外の種類とメッセージを確認し、次にトレースバックが示すファイルと行番号を確認して、該当する箇所のコードを見直す。原因を修正できない場合や、エラーが発生してもプログラムを続行させたい場合は、この後説明する ``try`` 文を使って例外を捕捉する。

try 文による例外処理
--------------------

発生する可能性のある例外に対処するには、``try`` 文を使用する。``try`` ブロックの中で例外が発生すると、対応する ``except`` ブロックの処理が実行される。

.. code-block:: python
   :linenos:

   try:
       result = 10 / 0
   except ZeroDivisionError:
       print("エラー: 0 で割ることはできません。")

``else`` ブロックと ``finally`` ブロック
-----------------------------------------

``try`` 文には、``else`` ブロックと ``finally`` ブロックを追加できる。``else`` ブロックは、例外が発生しなかったときにだけ実行され、``finally`` ブロックは、例外の発生有無にかかわらず必ず実行される。

.. code-block:: python
   :linenos:

   try:
       result = 10 / 2
   except ZeroDivisionError:
       print("エラー: 0 で割ることはできません。")
   else:
       print("計算結果:", result)
   finally:
       print("処理が終了しました。")

独自の例外クラス
----------------

Python では、``Exception`` クラスを継承することで、独自の例外クラスを定義できる。プログラム固有のエラーを表現したい場合に利用する。

.. code-block:: python
   :linenos:

   class InvalidScoreError(Exception):
       """点数が 0 から 100 の範囲外である場合に送出する例外。"""

   def validate_score(score: int) -> int:
       if score < 0 or score > 100:
           raise InvalidScoreError(f"点数は 0 から 100 の範囲で指定してください: {score}")
       return score

定義した例外は、``raise`` 文で送出し、呼び出し元の ``except`` ブロックで受け取る。

.. code-block:: python
   :linenos:

   try:
       validate_score(150)
   except InvalidScoreError as error:
       print("エラー:", error)

assert 文
---------

``assert`` 文を使うと、プログラムの前提条件を確認できる。``assert`` に続けて書いた条件式が偽であった場合、``AssertionError`` という例外が発生し、プログラムが停止する。条件式の後にカンマで区切ってメッセージを書くと、``AssertionError`` が発生した際にそのメッセージが表示される。

.. code-block:: python
   :linenos:

   def calculate_average(scores: list[int]) -> float:
       assert len(scores) > 0, "scores は空にできません。"
       return sum(scores) / len(scores)

上記の例では、``scores`` が空のリストであった場合に、``"scores は空にできない。"`` というメッセージとともに ``AssertionError`` が発生する。``assert`` 文は、本来あり得ないはずの状態を検知するデバッグ用途で使用する。ユーザーの入力値を検証するような場面では、``assert`` 文ではなく、これまでに説明した ``raise`` 文と独自の例外クラスを使用する。``assert`` 文は、Python を ``-O`` オプション付きで実行した場合などに無効化されるため、必ず実行したい検証処理には向いていない。

サンプルコード
--------------

例外処理の基本的な書き方をまとめたサンプルコードである。

:download:`exceptions.py <../../examples/ch10_exceptions/exceptions.py>`

.. literalinclude:: ../../examples/ch10_exceptions/exceptions.py
   :language: python3
   :linenos:
