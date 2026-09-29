re
==

正規表現を用いた文字列のパターンマッチング・検索・置換を行うためのモジュール。
パターンは文字列（多くの場合 ``r"..."`` のような raw 文字列）で記述する。

re.match / re.search / re.fullmatch
-------------------------------------

``match`` は文字列の先頭、``fullmatch`` は文字列全体がパターンに一致するかを調べる。``search`` は文字列中のどこかにパターンと一致する箇所があるかを調べ、最初に見つかったものを返す。いずれも一致しなければ ``None`` を返す。

.. code-block:: python

   >>> import re
   >>> re.match(r"\d+", "123abc")
   <re.Match object; span=(0, 3), match='123'>
   >>> re.match(r"\d+", "abc123") is None
   True
   >>> re.search(r"\d+", "abc123")
   <re.Match object; span=(3, 6), match='123'>
   >>> re.fullmatch(r"\d+", "123abc") is None
   True

re.findall / re.finditer
--------------------------

パターンに一致するすべての部分を検索する。``findall`` は一致文字列（または
グループ）のリストを、``finditer`` は ``Match`` オブジェクトを返すイテレータを返す。
一致箇所の位置情報なども必要な場合は ``finditer`` を使うとよい。

.. code-block:: python

   >>> re.findall(r"\d+", "a1 b22 c333")
   ['1', '22', '333']
   >>> for m in re.finditer(r"\d+", "a1 b22 c333"):
   ...     print(m.start(), m.group())
   ...
   1 1
   4 22
   8 333

re.sub
------

パターンに一致した部分を別の文字列に置換する。置換文字列には ``\1`` のようにグループを埋め込むこともでき、関数を渡して動的に置換内容を決めることもできる。

.. code-block:: python

   >>> re.sub(r"\s+", " ", "a   b\tc\nd")
   'a b c d'
   >>> re.sub(r"(\d+)-(\d+)", r"\2-\1", "03-1234")
   '1234-03'
   >>> re.sub(r"\d+", lambda m: str(int(m.group()) * 2), "1 2 3")
   '2 4 6'

re.compile とグループ
----------------------

同じパターンを繰り返し使う場合は ``re.compile`` でコンパイルしておくと効率がよく、コード上もパターンの意図が明確になる。丸括弧 ``()`` はグループ化のための構文で、``?P<name>`` を使うと名前付きグループとして参照できる。

.. code-block:: python

   >>> pattern = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
   >>> m = pattern.match("2024-05-01")
   >>> m.group(0)
   '2024-05-01'
   >>> m.group("year"), m.group("month"), m.group("day")
   ('2024', '05', '01')
   >>> m.groupdict()
   {'year': '2024', 'month': '05', 'day': '01'}

re.split
--------

パターンに一致する部分を区切りとして文字列を分割する。

.. code-block:: python

   >>> re.split(r"[,;]\s*", "a, b;c,  d")
   ['a', 'b', 'c', 'd']

flags 引数（re.IGNORECASE など）
-----------------------------------

``match`` や ``search``、``findall`` などの関数、および ``re.compile`` には、マッチの挙動を変える ``flags`` 引数を渡せる。最もよく使うのは ``re.IGNORECASE``（``re.I``）で、大文字・小文字を区別せずにマッチさせる。

.. code-block:: python

   >>> re.findall(r"python", "Python PYTHON python", re.IGNORECASE)
   ['Python', 'PYTHON', 'python']

他にも、``^`` ``$`` を各行の先頭・末尾にもマッチさせる ``re.MULTILINE``、``.`` が改行文字にもマッチするようにする ``re.DOTALL`` がある。

.. code-block:: python

   >>> re.findall(r"^\w+", "foo\nbar\nbaz")
   ['foo']
   >>> re.findall(r"^\w+", "foo\nbar\nbaz", re.MULTILINE)
   ['foo', 'bar', 'baz']

複数のフラグを同時に指定したい場合は ``|`` で組み合わせる
（例: ``re.IGNORECASE | re.MULTILINE``）。

re.escape
---------

ユーザー入力や外部から受け取った文字列など、動的に組み立てた値を
そのまま正規表現パターンに埋め込むと、``.`` や ``(`` ``)`` などの
正規表現の特殊文字として解釈されてしまい、意図しないマッチや
エラーにつながることがある。``re.escape()`` は文字列中の特殊文字を
すべてエスケープし、その文字列をリテラルとして安全にパターンへ
埋め込めるようにする。

.. code-block:: python

   >>> keyword = "C++"
   >>> re.escape(keyword)
   'C\\+\\+'
   >>> re.findall(re.escape(keyword), "I love C++ and C")
   ['C++']

.. note::

   バックスラッシュ ``\`` を含むパターンは、Python 自体のエスケープと正規表現のエスケープが重なって読みにくくなるため、``r"\d+"`` のように raw 文字列で書くのが基本。また ``*`` や ``+`` は既定で「貪欲（greedy）」にできるだけ長く一致しようとするため、最短一致にしたい場合は ``*?`` や ``+?`` のように ``?`` を付けて非貪欲にする。

   .. code-block:: python

      >>> re.findall(r"<.+>", "<a><b>")
      ['<a><b>']
      >>> re.findall(r"<.+?>", "<a><b>")
      ['<a>', '<b>']
