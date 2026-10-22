Python の re モジュール
=======================

第 8 章までは、主に ``re.search()`` と ``re.findall()`` を使って構文を説明してきた（``re.fullmatch()`` や ``re.sub()`` なども一部で使った）。この章では、``re`` モジュールが提供する関数と、その使い分けを整理する。

関数の一覧
----------

``re`` モジュールの主な関数を次に示す。

.. list-table:: re モジュールの主な関数
   :header-rows: 1
   :widths: 30 70

   * - 関数
     - 動作
   * - ``re.search(pattern, string)``
     - 文字列中で最初に一致した部分を Match オブジェクトで返す。一致しなければ ``None``
   * - ``re.match(pattern, string)``
     - 文字列の先頭から一致する場合だけ Match オブジェクトを返す
   * - ``re.fullmatch(pattern, string)``
     - 文字列全体が一致する場合だけ Match オブジェクトを返す
   * - ``re.findall(pattern, string)``
     - 一致した部分をすべてリストで返す
   * - ``re.finditer(pattern, string)``
     - 一致した部分ごとの Match オブジェクトを順に返すイテレーターを返す
   * - ``re.sub(pattern, repl, string)``
     - 一致した部分を ``repl`` で置換した文字列を返す
   * - ``re.subn(pattern, repl, string)``
     - ``re.sub()`` の結果と置換した回数をタプルで返す
   * - ``re.split(pattern, string)``
     - 一致した部分で文字列を分割したリストを返す
   * - ``re.compile(pattern)``
     - パターンを\ :term:`パターンオブジェクト`\ に変換する
   * - ``re.escape(string)``
     - 文字列中のメタ文字をエスケープする

目的に応じた関数の選び方を\ :numref:`fig-choose-function` に示す。

.. _fig-choose-function:

.. graphviz::
   :caption: 関数の選び方
   :align: center

   digraph choose {
       rankdir=TB;
       bgcolor="transparent";
       node [fontsize=12];
       edge [fontsize=11];
       q1 [shape=diamond, label="何をしたいか"];
       q2 [shape=diamond, label="どの範囲で\n一致を調べるか"];
       q3 [shape=diamond, label="位置などの情報も\n必要か"];
       search [shape=box, style=rounded, label="re.search()"];
       fullmatch [shape=box, style=rounded, label="re.fullmatch()"];
       findall [shape=box, style=rounded, label="re.findall()"];
       finditer [shape=box, style=rounded, label="re.finditer()"];
       sub [shape=box, style=rounded, label="re.sub()"];
       split [shape=box, style=rounded, label="re.split()"];
       q1 -> q2 [label="1 か所を探す・検証する"];
       q1 -> q3 [label="すべて取り出す"];
       q1 -> sub [label="置換する"];
       q1 -> split [label="分割する"];
       q2 -> search [label="文字列のどこか"];
       q2 -> fullmatch [label="文字列全体"];
       q3 -> findall [label="文字列だけでよい"];
       q3 -> finditer [label="必要"];
   }

search()、match()、fullmatch()
------------------------------

この 3 つの関数は、いずれも一致すれば Match オブジェクトを、一致しなければ ``None`` を返すが、一致を調べる範囲が異なる。

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_search_match_fullmatch
   :linenos:
   :caption: search()、match()、fullmatch() の違い

``re.search()`` は文字列のどこかで、``re.match()`` は文字列の先頭から、``re.fullmatch()`` は文字列全体で一致を調べる。``re.match()`` は、パターン全体を ``\A(?:...)`` で囲んだ ``re.search()`` と同じ動作である。

``re.match()`` は、名前から「全体が一致するか」を調べる関数と誤解されやすい。実際には先頭部分が一致すれば成功するので、5 行目のように ``123abc`` にも一致する。入力値の検証には ``re.fullmatch()`` を使う。

findall() と finditer()
-----------------------

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_findall_finditer
   :linenos:
   :caption: findall() と finditer()

``re.findall()`` は、一致した文字列だけをリストで返す。キャプチャグループを含むパターンでは戻り値の形が変わる点は、第 6 章で説明した。

``re.finditer()`` は、一致ごとの Match オブジェクトを順に返す。一致した位置や複数のグループを使いたい場合は、``re.finditer()`` のほうが扱いやすい。また、結果を一度にリストに格納しないので、大きなテキストを処理する場合にも向いている。

sub() で置換する
----------------

``re.sub()`` は、一致した部分を置換文字列で置き換える。置換文字列の中では、次の記法でグループを参照できる。

.. list-table:: 置換文字列で使える記法
   :header-rows: 1
   :widths: 25 75

   * - 記法
     - 意味
   * - ``\1``、``\2``、…
     - 番号で指定したグループが一致した文字列
   * - ``\g<1>``
     - ``\1`` と同じ。直後に数字が続く場合に使う（``\g<1>0`` と ``\10`` は意味が異なる）
   * - ``\g<name>``
     - 名前付きグループが一致した文字列
   * - ``\g<0>``
     - パターン全体が一致した文字列

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_sub
   :linenos:
   :caption: sub() と subn()

置換文字列もパターンと同様に raw 文字列で書く。6 行目のように ``count`` を指定すると、置換する回数の上限を決められる。7 行目の ``re.subn()`` は、置換後の文字列と置換した回数をタプルで返す。

関数で置換する
--------------

``re.sub()`` の第 2 引数には、置換文字列の代わりに関数を渡せる。関数は一致ごとに Match オブジェクトを受け取り、置換後の文字列を返す。

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_sub_with_function
   :linenos:
   :caption: 関数による置換

この例では、一致した数字を 2 倍にしている。数値の計算や辞書を使った変換など、置換文字列だけでは書けない処理ができる。

split() で分割する
------------------

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_split
   :linenos:
   :caption: split()

``str.split()`` に指定できる区切りは 1 つの固定の文字列だけだが、``re.split()`` を使うと、3 行目のように「前後の空白を含むカンマまたはセミコロン」といった柔軟な区切りで分割できる。4 行目の ``maxsplit`` は、分割する回数の上限である。

5 行目のように、パターンにキャプチャグループを含めると、区切りに一致した文字列も結果に含まれる。

compile() でパターンを再利用する
--------------------------------

``re.compile()`` は、パターンを解析した結果をパターンオブジェクトとして返す。パターンオブジェクトは、``re`` の関数と同じ名前のメソッドを持つ。

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_compile
   :linenos:
   :caption: compile()

``re.search()`` などの関数も、内部でパターンを解析してキャッシュしているので、同じパターンを繰り返し使っても毎回解析し直すわけではない。そのため、``re.compile()`` の主な利点は性能よりも読みやすさにある。よく使うパターンをモジュールの定数として ``re.compile()`` しておくと、名前でパターンの意味を表せ、フラグもパターンと一緒に管理できる。

Match オブジェクト
------------------

:term:`Match オブジェクト`\ は、一致した文字列と位置、グループの情報を持つ。

.. list-table:: Match オブジェクトの主なメソッドと属性
   :header-rows: 1
   :widths: 35 65

   * - メソッド・属性
     - 返す値
   * - ``group()``、``group(0)``、``m[0]``
     - パターン全体が一致した文字列
   * - ``group(n)``、``group("name")``、``m[n]``
     - 指定したグループが一致した文字列。一致しなかったグループは ``None``
   * - ``groups(default=None)``
     - すべてのグループのタプル。一致しなかったグループは ``default`` の値
   * - ``groupdict(default=None)``
     - 名前付きグループの辞書
   * - ``start()``、``end()``、``span()``
     - 一致した範囲の開始位置、終了位置、その 2 つのタプル。引数にグループを指定することもできる
   * - ``string``、``re``
     - 検索対象の文字列と、使われたパターンオブジェクト

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_match_object
   :linenos:
   :caption: Match オブジェクト

3 行目のパターンでは、``value`` グループに ``?`` が付いているので、グループが一致しなくても全体は一致する。一致しなかったグループの値は ``None`` になる。7 行目のように ``default`` を指定すると、``None`` の代わりの値を決められる。

escape() で文字列をエスケープする
---------------------------------

利用者の入力などをパターンに埋め込む場合は、必ず ``re.escape()`` でエスケープする。

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_escape
   :linenos:
   :caption: escape()

7 行目のように、エスケープしない ``*重要*`` は不正なパターンになり、エラーが発生する。11 行目のように、エラーにならなくても、括弧がグループとして解釈されるなどして意図と異なる結果になることもある。こちらはエラーが出ないので、気付きにくい。

エラー処理
----------

不正なパターンを渡すと、``re.error`` 例外が発生する。Python 3.13 以降では ``re.PatternError`` という名前も使え、``re.error`` はその別名になっている。

.. literalinclude:: ../examples/ch09_re_module.py
   :language: python
   :pyobject: demo_error
   :linenos:
   :caption: re.error

例外オブジェクトの ``msg`` 属性はエラーの内容を、``pos`` 属性はパターン中のエラーの位置を表す。利用者が入力したパターンを ``re.compile()`` する場合は、この例外を捕捉して分かりやすいメッセージを表示するとよい。

まとめ
------

* 文字列のどこかを探すには ``re.search()`` を、文字列全体を検証するには ``re.fullmatch()`` を使う。``re.match()`` は先頭部分だけを調べる。
* すべての一致を取り出すには ``re.findall()`` か ``re.finditer()`` を使う。
* ``re.sub()`` の置換文字列では ``\1`` や ``\g<name>`` でグループを参照できる。関数を渡すこともできる。
* よく使うパターンは ``re.compile()`` して名前を付けておく。
* 外部から受け取った文字列をパターンに埋め込むときは ``re.escape()`` を使う。

この章のサンプルコード: :download:`ch09_re_module.py <../examples/ch09_re_module.py>`
