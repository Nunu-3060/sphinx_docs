################################################################
第 5 章 抽象構文木と Tiny の構文解析器
################################################################

この章では、構文解析の結果を表す抽象構文木を設計し、第 4 章の手法を組み合わせて Tiny 全体の構文解析器を作ります。

具象構文木と抽象構文木
================================================================

第 4 章の構文木（具象構文木）は、文法の規則をそのまま反映しているため、後の処理にとって不要な情報を多く含んでいます。たとえば ``1 + 2 * 3`` の構文木には ``term`` や ``factor`` といった中間のノードや、括弧のトークンが含まれます。しかし、計算の内容を表すには「``1`` と、``2`` と ``3`` の積との和」が分かれば十分です。

そこで、プログラムの意味に必要な情報だけを残した木を作ります。これを\ :term:`抽象構文木`\ （AST: Abstract Syntax Tree）と呼びます。次の図は、``let x = 1 + 2 * 3;`` の抽象構文木です。

.. graphviz::
   :caption: 「let x = 1 + 2 * 3;」の抽象構文木

   digraph ast {
     node [shape=box, fontname="monospace"];
     let [label="Let\nname: x"];
     add [label="Binary\nop: +"];
     one [label="IntLit\nvalue: 1"];
     mul [label="Binary\nop: *"];
     two [label="IntLit\nvalue: 2"];
     three [label="IntLit\nvalue: 3"];
     let -> add [label=" value"];
     add -> one [label=" left"];
     add -> mul [label=" right"];
     mul -> two [label=" left"];
     mul -> three [label=" right"];
   }

括弧は木の形に反映されるので、抽象構文木には残りません。``(1 + 2) * 3`` なら、根が ``*`` で、その左の子が ``+`` の木になります。

抽象構文木の設計
================================================================

Tiny の抽象構文木は ``tiny_ast.py`` にデータクラスで定義します。まず、型を表すクラスです。型はソースコード中の型注釈（``[int]`` など）を表すほか、意味解析で式の型を記録するのにも使います。

.. literalinclude:: ../examples/tiny_ast.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 41-52
   :caption: tiny_ast.py（配列型と型の定数）

データクラスは ``==`` で値として比較できるので、``ArrayType(INT) == ArrayType(INT)`` は ``True`` になります。さらに ``frozen=True`` を指定すると、値を変更できなくなる代わりにハッシュ可能になり、辞書のキーにも使えます。

次に、式を表すノードです。すべてのノードは行番号 ``line`` を持ち、式のノードは意味解析で求めた型 ``ty`` を持ちます。これらは ``kw_only=True`` としてキーワード引数でだけ指定できるようにし、``compare=False`` として比較の対象から外しています。

.. literalinclude:: ../examples/tiny_ast.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 57-118
   :caption: tiny_ast.py（式のノード）

関数呼び出し ``Call`` の呼び出し先 ``callee`` を、式ではなく文字列にしている点に注意してください。Tiny では関数は値ではなく、呼び出せるのは関数名だけだからです。

文、関数、プログラムのノードも同様に定義します。``If`` の ``else_body`` は、``else`` 節がなければ ``None``、``else if`` なら ``If``、``else { ... }`` なら ``Block`` になります。

.. literalinclude:: ../examples/tiny_ast.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 122-187
   :caption: tiny_ast.py（文、関数、プログラムのノード）

Tiny の構文解析器
================================================================

構文解析器は ``tiny_parser.py`` に実装します。文と関数定義は再帰下降構文解析で、式は Pratt 構文解析で解析します。

文の解析
----------------------------------------------------------------

``parse_statement`` は、最初のトークンを見てどの種類の文かを判断します。``let``、``if``、``while``、``return``、``{`` のどれでもなければ、代入文か式文です。この 2 つは先頭を見ただけでは区別できないため、まず式として解析し、その後に ``=`` が続くかどうかで判断します。代入文の場合は、左辺が変数か添字式であることを確かめます。

.. literalinclude:: ../examples/tiny_parser.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Parser.parse_statement
   :caption: tiny_parser.py（文の解析）

``else if`` の連鎖は ``parse_if`` を再帰的に呼び出して解析します。

.. literalinclude:: ../examples/tiny_parser.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Parser.parse_if
   :caption: tiny_parser.py（if 文の解析）

式の解析
----------------------------------------------------------------

式の解析は第 4 章の Pratt 構文解析と同じ形です。違いは、文字列の代わりに抽象構文木のノードを作ることと、関数呼び出し ``f(...)`` と添字 ``a[...]`` という後置の演算子を扱うことです。後置の演算子にはどの二項演算子よりも大きな結合力 ``POSTFIX_POWER`` を与えているので、``-a[0]`` は ``-(a[0])`` と解釈されます。

.. literalinclude:: ../examples/tiny_parser.py
   :language: python
   :linenos:
   :lineno-match:
   :start-at: def parse_expr(self
   :end-before: def parse_list(self
   :caption: tiny_parser.py（式の解析）

被演算子になる式（リテラル、変数、単項演算子、括弧、配列リテラル）は ``parse_prefix`` で解析します。

.. literalinclude:: ../examples/tiny_parser.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Parser.parse_prefix
   :caption: tiny_parser.py（被演算子の解析）

エラー回復の実装
================================================================

第 4 章で説明したパニックモードのエラー回復を、``parse_block`` と ``synchronize`` で実装しています。文の解析中に構文エラー（``ParseError``）が起きたら、エラーを記録し、文の区切りまでトークンを読み飛ばして次の文から解析を再開します。

.. literalinclude:: ../examples/tiny_parser.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Parser.synchronize
   :caption: tiny_parser.py（読み飛ばし）

.. literalinclude:: ../examples/tiny_parser.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Parser.parse_block
   :caption: tiny_parser.py（ブロックの解析とエラー回復）

``synchronize`` がトークンを 1 つも読み進めなかった場合は、強制的に 1 つ進めています。そうしないと、同じ位置で同じエラーが起き続けて無限ループになるおそれがあるからです。

次のプログラムには 3 つの誤りがあります。2 行目は初期値がなく、3 行目は ``;`` がなく、4 行目は引数の間に ``,`` がありません。

.. code-block:: tiny
   :linenos:
   :caption: error.tiny

   fn main() {
       let x = ;
       let y = 1
       print(x y);
   }

.. code-block:: console
   :linenos:

   $ python tiny.py ast error.tiny
   error.tiny:2:13: 式が必要です（';' があります）
   error.tiny:4:5: ; が必要です（'print' があります）

2 行目と 3 行目の誤りは報告されましたが、4 行目の誤りは報告されていません。3 行目の誤りから回復するときに、``print`` が文の先頭になるキーワードではないため、4 行目の ``;`` まで読み飛ばしてしまったからです。このように、パニックモードは単純ですが、読み飛ばした範囲にある誤りは見逃します。また、``;`` の抜けのエラーは次の行の位置で報告されます。実用的なコンパイラは、「``;`` が抜けているとみなして解析を続ける」といった、より細かな回復の手法を組み合わせています。

構文木をたどる
================================================================

抽象構文木を使う処理（意味解析、インタプリタ、コード生成など）は、どれも「ノードの種類に応じて処理を変えながら木をたどる」という形になります。オブジェクト指向言語では、これを :term:`Visitor パターン`\ で書くのが伝統的な方法です。

.. code-block:: python
   :linenos:
   :caption: Visitor パターンによる評価（概略）

   class Visitor:
       def visit(self, node: Node) -> object:
           method = getattr(self, "visit_" + type(node).__name__)
           return method(node)


   class Evaluator(Visitor):
       def visit_IntLit(self, node: IntLit) -> object:
           return node.value

       def visit_Binary(self, node: Binary) -> object:
           left = self.visit(node.left)
           right = self.visit(node.right)
           ...

Python 3.10 以降では、``match`` 文の構造的パターンマッチを使うと、同じ処理をより直接的に書けます。データクラスは ``__match_args__`` を自動的に定義するので、``Binary(op, left, right)`` のように、フィールドを取り出しながらノードの種類で分岐できます。本書の処理系では、この ``match`` 文による書き方を使います。

.. code-block:: python
   :linenos:
   :caption: match 文による評価（概略）

   def evaluate(node: Expr) -> object:
       match node:
           case IntLit(value):
               return value
           case Binary("+", left, right):
               return evaluate(left) + evaluate(right)
           ...

実行例
================================================================

``tiny_parser.py`` を引数なしで実行すると、組み込みの例を解析して抽象構文木を表示します。

.. code-block:: console
   :linenos:

   $ python tiny_parser.py
   Program
     functions:
       FuncDef
         name: 'main'
         params: []
         return_type: void
         body:
           Block
             stmts:
               Let
                 name: 'x'
                 declared_type: None
                 value:
                   Binary
                     op: '+'
                     left:
                       IntLit
                         value: 1
                     right:
                       Binary
                         op: '*'
                         left:
                           IntLit
                             value: 2
                         right:
                           IntLit
                             value: 3
               ExprStmt
                 expr:
                   Call
                     callee: 'print'
                     args:
                       Name
                         name: 'x'

Python の ast モジュール
================================================================

:doc:`第 1 章 <01_overview>`\ で見たように、Python の ``ast`` モジュールを使うと Python のプログラムの抽象構文木を得られます。``ast`` モジュールには Visitor パターンの基底クラス ``ast.NodeVisitor`` も用意されており、``visit_クラス名`` というメソッドを定義すると、そのノードを訪れたときに呼び出されます。次の例は、式の中で読み出している変数の名前を集めます。

.. code-block:: python
   :linenos:
   :caption: ast.NodeVisitor の使用例

   import ast


   class NameCollector(ast.NodeVisitor):
       """読み出している変数の名前を集める."""

       def __init__(self) -> None:
           self.names: list[str] = []

       def visit_Name(self, node: ast.Name) -> None:
           if isinstance(node.ctx, ast.Load):
               self.names.append(node.id)
           self.generic_visit(node)


   tree = ast.parse("total = price * count + tax")
   collector = NameCollector()
   collector.visit(tree)
   print(collector.names)  # ['price', 'count', 'tax']

Python の ``Name`` ノードは、読み出し（``Load``）か書き込み（``Store``）かを ``ctx`` 属性で区別しています。そのため、代入先の ``total`` は集められていません。このような ``ast`` モジュールの機能は、flake8 などの静的解析ツールや、コードの自動変換ツールで広く使われています。

まとめ
================================================================

* 抽象構文木は、構文木から意味に必要な情報だけを残した木で、後の段階はすべて抽象構文木を入力とします。
* Tiny の構文解析器は、文を再帰下降構文解析で、式を Pratt 構文解析で解析します。
* パニックモードのエラー回復では、文の区切りまで読み飛ばして解析を続けます。単純ですが、読み飛ばした範囲の誤りは見逃します。
* 抽象構文木をたどる処理は、Visitor パターンや ``match`` 文で書けます。
