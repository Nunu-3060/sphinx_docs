フラグ
======

:term:`フラグ`\ は、パターン全体の解釈の仕方を変える設定である。第 3 章と第 5 章で ``re.ASCII`` と ``re.MULTILINE`` を使ったが、この章ではフラグ全体を整理して説明する。

フラグの一覧
------------

``re`` モジュールの主なフラグを次に示す。各フラグには長い名前と 1 文字の短い名前があり、どちらを使ってもよい。

.. list-table:: 主なフラグ
   :header-rows: 1
   :widths: 25 10 15 50

   * - 名前
     - 短い名前
     - インライン
     - 効果
   * - ``re.IGNORECASE``
     - ``re.I``
     - ``(?i)``
     - 大文字と小文字を区別しない
   * - ``re.MULTILINE``
     - ``re.M``
     - ``(?m)``
     - ``^`` と ``$`` が各行の先頭と末尾にも一致する
   * - ``re.DOTALL``
     - ``re.S``
     - ``(?s)``
     - ``.`` が改行にも一致する
   * - ``re.VERBOSE``
     - ``re.X``
     - ``(?x)``
     - パターン中の空白とコメントを無視する
   * - ``re.ASCII``
     - ``re.A``
     - ``(?a)``
     - ``\d``、``\w``、``\s``、``\b`` などが ASCII 文字だけを対象にする

このほか、``bytes`` のパターンだけで使える ``re.LOCALE`` や、パターンの解析結果を表示する ``re.DEBUG`` がある。また、Python 3.11 では「フラグなし」を表す ``re.NOFLAG`` が追加された。

フラグの指定方法
----------------

フラグは、``re`` の各関数の ``flags`` 引数に指定する。``flags`` は必ずキーワード引数として渡すとよい。``re.sub()`` や ``re.split()`` では、位置引数で渡すと別の引数として解釈されてしまうからである。

.. code-block:: python
   :linenos:
   :caption: フラグを位置引数で渡す誤り

   # 誤り: 4 番目の位置引数は count (置換回数) なので、re.IGNORECASE (値は 2) が count になる
   re.sub(r"python", "Python", text, re.IGNORECASE)

   # 正しい書き方
   re.sub(r"python", "Python", text, flags=re.IGNORECASE)

Python 3.13 以降では、``re.sub()`` などの ``count``、``maxsplit``、``flags`` を位置引数で渡すと ``DeprecationWarning`` が出る。

大文字と小文字を区別しない
--------------------------

.. literalinclude:: ../examples/ch08_flags.py
   :language: python
   :pyobject: demo_ignorecase
   :linenos:
   :caption: re.IGNORECASE

``re.IGNORECASE`` は、文字クラスの範囲にも効く。たとえば ``[a-z]`` は大文字にも一致するようになる。ただし、Unicode の大文字と小文字の対応に従うため、``[a-z]`` が ``ſ``\ （U+017F、ロングエス）や ``K``\ （U+212A、ケルビン記号）にも一致するといった、意外な一致が起こることがある。入力値の検証で厳密に ASCII 文字だけを受け付けたい場合は、``re.ASCII`` を併せて指定する。

. を改行にも一致させる
----------------------

.. literalinclude:: ../examples/ch08_flags.py
   :language: python
   :pyobject: demo_dotall
   :linenos:
   :caption: re.DOTALL

既定では ``.`` は改行に一致しないので、4 行目のように改行をまたぐ範囲には一致しない。``re.DOTALL`` を指定すると、``.`` が改行を含む任意の 1 文字に一致する。

``re.MULTILINE`` と ``re.DOTALL`` は名前が似ているが、効果はまったく異なる。``re.MULTILINE`` は ``^`` と ``$`` の動作を、``re.DOTALL`` は ``.`` の動作を変える。

フラグを組み合わせる
--------------------

複数のフラグは ``|`` でつなげて指定する。

.. literalinclude:: ../examples/ch08_flags.py
   :language: python
   :pyobject: demo_combine
   :linenos:
   :caption: フラグの組み合わせ

``re.IGNORECASE`` で ``Error`` と ``ERROR`` の両方に一致させ、``re.MULTILINE`` で各行の先頭に ``^`` を一致させている。

インラインフラグ
----------------

フラグは、``(?i)`` のようにパターンの中に書くこともできる。これをインラインフラグと呼ぶ。

.. literalinclude:: ../examples/ch08_flags.py
   :language: python
   :pyobject: demo_inline_flags
   :linenos:
   :caption: インラインフラグ

3 行目のように、パターン全体に効くインラインフラグは、パターンの先頭に書かなければならない。Python 3.11 以降では、6 行目のように先頭以外に書くとエラーになる。

4 行目の ``(?i:py)`` のように ``(?フラグ:...)`` と書くと、そのグループの中だけにフラグが効く。この例では ``py`` の部分だけ大文字と小文字を区別しない。``thon`` の部分は区別されるので、``PYTHON`` には一致しない。

インラインフラグは、設定ファイルなどでパターンだけを受け渡す場合に便利である。

VERBOSE で読みやすく書く
------------------------

``re.VERBOSE`` を指定すると、パターン中の空白と改行が無視され、``#`` から行末までがコメントになる。長いパターンを分割し、各部分に説明を付けられる。

.. literalinclude:: ../examples/ch08_flags.py
   :language: python
   :pyobject: demo_verbose
   :linenos:
   :caption: re.VERBOSE

``re.VERBOSE`` を指定したパターンで空白や ``#`` そのものに一致させたい場合は、``[ ]`` や ``[#]`` のように文字クラスの中に書くか、``\#`` のようにバックスラッシュでエスケープする。文字クラスの中の空白と ``#`` は無視されない。

複雑なパターンは、第 10 章の例のように、``re.VERBOSE`` と名前付きグループを組み合わせて書くと保守しやすくなる。

ASCII 文字に限定する
--------------------

.. literalinclude:: ../examples/ch08_flags.py
   :language: python
   :pyobject: demo_ascii
   :linenos:
   :caption: re.ASCII

第 3 章で説明したとおり、``str`` のパターンでは ``\w`` などが Unicode 文字にも一致する。``re.ASCII`` を指定すると、ASCII 文字だけを対象にする。入力値の検証などで半角文字だけを受け付けたい場合に使う。

まとめ
------

* フラグは ``flags=`` のキーワード引数で指定し、複数のフラグは ``|`` で組み合わせる。
* ``re.MULTILINE`` は ``^`` と ``$`` を、``re.DOTALL`` は ``.`` の動作を変える。
* パターン全体に効くインラインフラグは先頭に書く。``(?i:...)`` のように一部だけに効かせることもできる。
* 長いパターンは ``re.VERBOSE`` で分割し、コメントを付ける。

この章のサンプルコード: :download:`ch08_flags.py <../examples/ch08_flags.py>`
