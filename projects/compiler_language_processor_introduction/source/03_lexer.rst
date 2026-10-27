################################################################
第 3 章 字句解析
################################################################

この章では、処理系の最初の段階である\ :term:`字句解析`\ を扱います。字句解析器は、ソースコードという文字の列を、意味のある最小単位である\ :term:`トークン`\ の列に変換します。

字句解析の役割
================================================================

次の Tiny のコードを考えます。

.. code-block:: tiny
   :linenos:

   let x = 10 * (y + 2); // コメント

人間はこれを「``let``、``x``、``=``、``10``、``*``、…」という単語の並びとして読みます。しかしプログラムにとっては、``l``、``e``、``t``、空白、``x``、… という文字の並びにすぎません。字句解析器はこの文字の並びを次のようなトークンの列に変換します。

.. list-table::
   :header-rows: 1
   :widths: 30 30 40

   * - トークンの種類
     - 字句
     - 値
   * - ``LET``
     - ``let``
     -
   * - ``IDENT``
     - ``x``
     -
   * - ``ASSIGN``
     - ``=``
     -
   * - ``INT``
     - ``10``
     - 整数 10
   * - ``STAR``
     - ``*``
     -
   * - …
     - …
     -

ソースコード上の文字列そのもの（``let`` や ``10``）を\ :term:`字句`\ （lexeme）と呼び、それを分類したもの（``LET`` や ``INT``）をトークンの種類と呼びます。空白とコメントは、この段階で読み飛ばします。

字句解析を構文解析から独立させると、次の利点があります。

* 構文解析器は空白やコメントのことを考えずに済み、文法を簡潔に書けます。
* ``<=`` のような 2 文字の演算子や、エスケープシーケンスを含む文字列リテラルの処理を 1 か所にまとめられます。
* 文字単位の処理は実行時間の大きな部分を占めるため、字句解析器だけを高速化しやすくなります。

トークンの設計
================================================================

Tiny の字句解析器は ``tiny_lexer.py`` に実装します。まず、トークンの種類を列挙型で定義します。

.. literalinclude:: ../examples/tiny_lexer.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: TokenKind
   :caption: tiny_lexer.py（トークンの種類、一部を抜粋）
   :end-before: # 演算子と区切り記号

トークンは、種類・字句・位置（行と列）・値を持つデータクラスで表します。位置は、エラーメッセージで問題のか所を示すために使います。

.. literalinclude:: ../examples/tiny_lexer.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Token
   :caption: tiny_lexer.py（トークン）

正規表現と有限オートマトン
================================================================

各トークンの形は\ :term:`正規表現`\ で記述できます。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - トークン
     - 正規表現
   * - 識別子
     - ``[A-Za-z_][A-Za-z0-9_]*``
   * - 整数リテラル
     - ``[0-9]+``
   * - 文字列リテラル
     - ``"([^"\\\n]|\\[nt"\\])*"``
   * - 演算子 ``<=``
     - ``<=``

正規表現で表せる文字列の集合は、:term:`有限オートマトン`\ で受理できることが知られています。有限オートマトンは、有限個の状態と、入力文字に応じた状態の遷移からなる機械です。次の図は、識別子・整数・``<`` / ``<=`` を認識する有限オートマトンです。二重丸は受理状態（そこで止まればトークンとして認める状態）を表します。

.. graphviz::
   :caption: 識別子・整数・「<」「<=」を認識する有限オートマトン

   digraph dfa {
     rankdir=LR;
     node [shape=circle, fontname="sans-serif"];
     start [shape=point];
     s0 [label="開始"];
     id [label="識別子", shape=doublecircle];
     num [label="整数", shape=doublecircle];
     lt [label="<", shape=doublecircle];
     le [label="<=", shape=doublecircle];
     start -> s0;
     s0 -> id [label="英字, _"];
     id -> id [label="英数字, _"];
     s0 -> num [label="数字"];
     num -> num [label="数字"];
     s0 -> lt [label="<"];
     lt -> le [label="="];
   }

字句解析器は、受理状態に到達した後も遷移できる限り読み進め、最も長い字句を 1 つのトークンにします。これを\ :term:`最長一致`\ の規則と呼びます。たとえば ``<=`` は ``<`` と ``=`` の 2 つのトークンではなく、1 つのトークン ``<=`` になります。同様に ``letter`` はキーワード ``let`` と識別子 ``ter`` ではなく、1 つの識別子になります。

flex などの\ :term:`字句解析器生成系`\ は、トークンの正規表現から有限オートマトンを自動的に作り、それを実行するプログラムを生成します。本書では、有限オートマトンの動きを素直にプログラムとして書き下す方法で字句解析器を作ります。

字句解析器の実装
================================================================

字句解析器 ``Lexer`` は、ソースコード上の現在位置 ``pos`` と、行番号・列番号を持ちます。``peek`` で先読みし、``advance`` で 1 文字読み進めます。

.. literalinclude:: ../examples/tiny_lexer.py
   :language: python
   :linenos:
   :lineno-match:
   :start-at: class Lexer:
   :end-before: def next_token
   :caption: tiny_lexer.py（Lexer の補助メソッド）

``next_token`` が字句解析器の中心です。空白とコメントを読み飛ばした後、先頭の 1 文字を見て、どの種類のトークンかを判断します。これは有限オートマトンの開始状態からの遷移に対応します。

.. literalinclude:: ../examples/tiny_lexer.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Lexer.next_token
   :caption: tiny_lexer.py（トークンを 1 つ切り出す）

数字や英字の判定には、ASCII の文字だけを受け付ける関数を使っています。Python の ``str.isdigit`` や ``str.isalpha`` は、全角数字や漢字に対しても ``True`` を返すため、そのまま使うと Tiny の字句の規則より広い文字を受け付けてしまうからです。

.. literalinclude:: ../examples/tiny_lexer.py
   :language: python
   :linenos:
   :lineno-match:
   :start-at: def is_digit
   :end-before: @dataclass(frozen=True)
   :caption: tiny_lexer.py（文字の判定）

識別子を読み終えた後で ``KEYWORDS`` 辞書を引き、キーワードかどうかを判定しています。キーワードごとに有限オートマトンの状態を作るよりも、この方法のほうが簡潔です。記号は、2 文字の記号を 1 文字の記号より先に調べることで最長一致を実現しています。

文字列リテラルは、エスケープシーケンスを解釈して値を作ります。閉じる ``"`` がないまま行末やファイルの終わりに達したらエラーにします。

.. literalinclude:: ../examples/tiny_lexer.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Lexer.read_string
   :caption: tiny_lexer.py（文字列リテラル）

エラーの報告
================================================================

処理系が報告するエラーは、すべて ``TinyError`` の派生クラスにします。``TinyError`` は行番号と列番号を持ち、``行:列: メッセージ`` の形式で表示されます。列が分からないエラー（意味解析のエラーなど）は ``行: メッセージ`` の形式になります。

.. literalinclude:: ../examples/tiny_lexer.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: TinyError
   :caption: tiny_lexer.py（エラーの基底クラス）

位置情報を正しく記録しておくことは、使いやすい処理系を作るうえで重要です。本書の処理系では、トークンが位置を持ち、構文解析器がその位置を抽象構文木のノードに引き継ぎます。

実行例
================================================================

``tiny_lexer.py`` を引数なしで実行すると、組み込みの例をトークンに分割して表示します。

.. code-block:: console
   :linenos:

   $ python tiny_lexer.py
     1:1   LET        let
     1:5   IDENT      x
     1:7   ASSIGN     =
     1:9   INT        10
     1:12  STAR       *
     1:14  LPAREN     (
     1:15  IDENT      y
     1:17  PLUS       +
     1:19  INT        2
     1:20  RPAREN     )
     1:21  SEMICOLON  ;
     2:1   IDENT      print
     2:6   LPAREN     (
     2:7   STRING     "x="
     2:11  COMMA      ,
     2:13  IDENT      x
     2:15  GE         >=
     2:18  INT        3
     2:19  RPAREN     )
     2:20  SEMICOLON  ;
     2:21  EOF

1 行目の末尾のコメントは読み飛ばされています。``print`` は組み込み関数ですが、字句解析の段階ではふつうの識別子として扱います。

Python の tokenize モジュール
================================================================

Python の標準ライブラリの ``tokenize`` モジュールを使うと、Python のソースコードがどのようなトークンに分割されるかを確認できます。

.. code-block:: console
   :linenos:

   $ echo "x = 1 + 2 * y" > example.py
   $ python -m tokenize example.py
   0,0-0,0:            ENCODING       'utf-8'
   1,0-1,1:            NAME           'x'
   1,2-1,3:            OP             '='
   1,4-1,5:            NUMBER         '1'
   1,6-1,7:            OP             '+'
   1,8-1,9:            NUMBER         '2'
   1,10-1,11:          OP             '*'
   1,12-1,13:          NAME           'y'
   1,13-1,14:          NEWLINE        '\n'
   2,0-2,0:            ENDMARKER      ''

Python では改行とインデントに意味があるため、``NEWLINE`` や、インデントの増減を表す ``INDENT`` / ``DEDENT`` というトークンがあります。字句解析器は行頭の空白の量をスタックで管理し、インデントが深くなったら ``INDENT`` を、浅くなったら ``DEDENT`` を出力します。これにより、構文解析器は ``{`` と ``}`` で囲まれたブロックと同じようにインデントを扱えます。

まとめ
================================================================

* 字句解析は、文字の列をトークンの列に変換し、空白とコメントを取り除きます。
* トークンの形は正規表現で記述でき、有限オートマトンで認識できます。
* 字句解析器は最長一致の規則に従ってトークンを切り出します。
* トークンに位置情報を持たせておくと、後の段階で分かりやすいエラーメッセージを出せます。
