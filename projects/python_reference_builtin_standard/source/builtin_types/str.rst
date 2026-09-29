str
===

Python の文字列型 ``str`` が持つメソッド群。文字列はイミュータブル（変更不可）なオブジェクトであり、以下のメソッドはいずれも元の文字列を変更せず、新しい文字列（またはリストなどの列）を返す。

str.split / str.join
---------------------

``split`` は文字列を区切り文字で分割してリストにする。``join`` はその逆に、リストなどの文字列の列を区切り文字で連結して 1 つの文字列にする。

.. code-block:: python

   >>> "2024-01-15".split("-")
   ['2024', '01', '15']
   >>> "  a  b  c  ".split()
   ['a', 'b', 'c']
   >>> "-".join(["2024", "01", "15"])
   '2024-01-15'
   >>> ", ".join(["apple", "banana", "cherry"])
   'apple, banana, cherry'

str.strip / str.lstrip / str.rstrip
--------------------------------------

前後の空白や指定した文字を取り除く。``strip`` は両端、``lstrip`` は左端、``rstrip`` は右端のみを対象とする。引数に文字を指定すると、その文字集合に含まれる文字を取り除く。

.. code-block:: python

   >>> "  hello world  ".strip()
   'hello world'
   >>> "  hello world  ".lstrip()
   'hello world  '
   >>> "  hello world  ".rstrip()
   '  hello world'
   >>> "***important***".strip("*")
   'important'

str.replace
-----------

文字列中の部分文字列を別の文字列に置き換える。第 3 引数で置換回数の上限を指定できる。

.. code-block:: python

   >>> "I like cats. Cats are cute.".replace("cats", "dogs")
   'I like dogs. Cats are cute.'
   >>> "aaa".replace("a", "b", 2)
   'bba'

str.startswith / str.endswith
--------------------------------

文字列が指定した接頭辞・接尾辞を持つかどうかを判定する。ファイルの拡張子や URL のスキームの確認などによく使う。

.. code-block:: python

   >>> "sample.rst".endswith(".rst")
   True
   >>> "https://example.com".startswith("https://")
   True
   >>> "sample.rst".startswith(("sample", "test"))
   True

str.find / str.index
---------------------

部分文字列が最初に現れる位置（インデックス）を調べる。``find`` は見つからない場合に ``-1`` を返すのに対し、``index`` は見つからない場合に ``ValueError`` を発生させる点が異なる。

.. code-block:: python

   >>> "hello world".find("world")
   6
   >>> "hello world".find("python")
   -1
   >>> "hello world".index("world")
   6
   >>> "hello world".index("python")
   Traceback (most recent call last):
       ...
   ValueError: substring not found

.. note::

   存在しない可能性がある場合は ``find`` で ``-1`` を判定し、必ず存在するはずの場合は ``index`` を使うことで、想定外の事態にエラーとして早期に気付けるようにするとよい。

str.upper / str.lower / str.title
------------------------------------

文字列の大文字・小文字を変換する。``upper`` は全て大文字、``lower`` は全て小文字、``title`` は各単語の先頭を大文字にする。

.. code-block:: python

   >>> "Hello World".upper()
   'HELLO WORLD'
   >>> "Hello World".lower()
   'hello world'
   >>> "hello world".title()
   'Hello World'

str.count
---------

文字列中に指定した部分文字列が出現する回数を返す。``list.count`` や ``tuple.count`` と同じ「値の出現回数を数える」メソッドだが、``str.count`` は開始位置・終了位置を指定して検索範囲を絞ることもできる。

.. code-block:: python

   >>> "I like cats. Cats are cute.".count("cats")
   1
   >>> "I like cats. Cats are cute.".lower().count("cats")
   2
   >>> "abababab".count("ab")
   4
   >>> "abababab".count("ab", 3)
   2

str.isdigit / str.isalpha / str.isupper / str.islower / str.isalnum
-----------------------------------------------------------------------

文字列の内容を判定するメソッド群で、いずれも判定結果を ``bool`` で返す。ユーザー入力の検証などによく使われる。

- ``isdigit()``: すべての文字が数字であれば ``True``
- ``isalpha()``: すべての文字がアルファベットであれば ``True``
- ``isupper()``: すべてのアルファベットが大文字であれば ``True``
- ``islower()``: すべてのアルファベットが小文字であれば ``True``
- ``isalnum()``: すべての文字が英数字（アルファベットまたは数字）であれば ``True``

.. code-block:: python

   >>> "12345".isdigit()
   True
   >>> "12a45".isdigit()
   False
   >>> "hello".isalpha()
   True
   >>> "hello123".isalpha()
   False
   >>> "HELLO".isupper()
   True
   >>> "Hello".isupper()
   False
   >>> "hello".islower()
   True
   >>> "Hello123".islower()
   False
   >>> "hello123".isalnum()
   True
   >>> "hello 123".isalnum()
   False

.. note::

   空文字列に対してはいずれも ``False`` を返す点に注意する（判定対象となる文字が 1 つもないため）。

f-string / str.format
-------------------------

文字列中に値を埋め込むための機能。``f"{value}"`` の形式で書く f-string と、``"{}".format(value)`` の形式で書く ``str.format`` メソッドがある。

.. code-block:: python

   >>> name = "Python"
   >>> version = 3.12
   >>> f"{name} {version}"
   'Python 3.12'
   >>> f"{version:.1f}"
   '3.1'
   >>> "{} {}".format(name, version)
   'Python 3.12'

.. note::

   現在では、より簡潔で読みやすい f-string の使用が、多くの場面で ``str.format`` よりも推奨される。

書式指定のミニ言語
~~~~~~~~~~~~~~~~~~~~

``{value:書式指定}`` の書式指定部分では、幅・アライメント・0埋め・桁区切り・パーセント表示などを指定できる。この記法は f-string と ``str.format`` のどちらでも共通して使える。

.. code-block:: python

   >>> f"{42:5d}"        # 幅5で右揃え
   '   42'
   >>> f"{42:<5d}|"      # 左揃え
   '42   |'
   >>> f"{42:05d}"       # 0埋め
   '00042'
   >>> f"{1234567:,}"    # 3桁ごとの桁区切り
   '1,234,567'
   >>> f"{0.256:.1%}"    # パーセント表示（小数点以下1桁）
   '25.6%'

``=`` によるデバッグ出力
~~~~~~~~~~~~~~~~~~~~~~~~~~~

f-string では、式の後ろに ``=`` を付けると「``式名=値``」の形式で出力される。``print`` デバッグの際に変数名を手で書く必要がなくなり便利。

.. code-block:: python

   >>> name = "Python"
   >>> count = 3
   >>> f"{name=}, {count=}"
   "name='Python', count=3"
   >>> f"{count * 2=}"
   'count * 2=6'

波括弧のエスケープ
~~~~~~~~~~~~~~~~~~~~

f-string・``str.format`` の中で波括弧そのものを出力したい場合は、``{{``・``}}`` のように2つ重ねてエスケープする。

.. code-block:: python

   >>> f"{{literal braces}}"
   '{literal braces}'
   >>> f"{{{name}}}"
   '{Python}'

t-string（テンプレート文字列）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3.14 で追加された ``t"..."`` の形式で書く構文（PEP 750）。見た目は f-string に似ているが、その場で文字列に変換されるのではなく、埋め込んだ式と値を保持したままの ``string.templatelib.Template`` オブジェクトを生成する。呼び出し側で値ごとにエスケープ処理などを挟めるため、SQL や HTML を組み立てる際に、埋め込み値をそのまま文字列連結してしまう事故を防ぎやすい。登場したばかりの機能で実務での採用はまだ広がっていないため、基本的な文字列の組み立てにはこれまで通り f-string を使えばよい。

.. code-block:: python

   >>> name = "World"
   >>> template = t"Hello, {name}!"
   >>> template
   Template(strings=('Hello, ', '!'), interpolations=(Interpolation('World', 'name', None, ''),))
   >>> "".join(
   ...     part if isinstance(part, str) else str(part.value)
   ...     for part in template
   ... )
   'Hello, World!'

str.encode
----------

文字列を指定したエンコーディングでバイト列（``bytes``）に変換する。逆にバイト列から文字列に戻すには、対になる :meth:`bytes.decode` を使う。

.. code-block:: python

   >>> "こんにちは".encode("utf-8")
   b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf'
   >>> "こんにちは".encode("utf-8").decode("utf-8")
   'こんにちは'
