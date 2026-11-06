ast
===

Python のソースコードを抽象構文木（AST: Abstract Syntax Tree）として扱うためのモジュール。抽象構文木とは、ソースコードを空白やコメントなどの表記上の情報を取り除いた木構造で表したものであり、Python インタプリタ自身もソースコードをいったん AST に変換してからバイトコードにコンパイルしている。``ast`` モジュールを使うと、この木を Python のオブジェクトとして取得・調査・書き換えできる。

``ast`` は日常のアプリケーション開発で直接使う機会は多くないが、次のような場面で役に立つ。

* 文字列で与えられたリテラル（設定値など）を安全に評価する（``ast.literal_eval()``）。
* ソースコードを実行せずに解析する（使われている関数名や ``import`` の一覧を集める、など）。
* Lint ツール、コードフォーマッタ、テストフレームワークなどの開発ツールを作る。実際に pytest や多くの静的解析ツールは ``ast`` を利用している。

.. note::

   AST のノードの種類や属性は、新しい構文の追加に合わせて Python のバージョンごとに変わることがある。本ページの出力例は Python 3.14 のものである。

ソースコードを AST に変換する
-----------------------------

``ast.parse()`` はソースコードの文字列を受け取り、木の根に当たる ``Module`` ノードを返す。木の内容は ``ast.dump()`` で文字列として確認できる。``indent`` 引数を指定すると、入れ子の構造が読みやすいように字下げして表示される。

.. code-block:: python
   :linenos:

   >>> import ast
   >>> tree = ast.parse("x = 1 + 2")
   >>> print(ast.dump(tree, indent=2))
   Module(
     body=[
       Assign(
         targets=[
           Name(id='x', ctx=Store())],
         value=BinOp(
           left=Constant(value=1),
           op=Add(),
           right=Constant(value=2)))])

代入文 ``x = 1 + 2`` が、代入（``Assign``）ノードの下に、代入先の名前（``Name``）と二項演算（``BinOp``）がぶら下がった木として表されていることが分かる。``ctx=Store()`` は、その名前が値を読み出す側（``Load``）ではなく書き込まれる側であることを示す。

各ノードは通常の Python オブジェクトであり、属性をたどって中身を取り出せる。文（statement）を表すノードは ``lineno`` や ``col_offset`` などの位置情報も持つ。

.. code-block:: python
   :linenos:

   >>> stmt = tree.body[0]
   >>> stmt.value.op
   <ast.Add object at 0x...>
   >>> stmt.lineno, stmt.col_offset, stmt.end_col_offset
   (1, 0, 9)

.. note::

   Python 3.13 以降の ``ast.dump()`` は、空のリストや ``None`` の属性を既定で省略して表示する。省略せずにすべて表示したい場合は ``show_empty=True`` を指定する。

構文として正しくないソースコードを ``ast.parse()`` に渡すと ``SyntaxError`` が送出される。ソースコードは解析されるだけで実行はされないため、構文チェックの用途にも使える。

.. code-block:: python
   :linenos:

   >>> ast.parse("x = = 1")
   Traceback (most recent call last):
     ...
   SyntaxError: invalid syntax

主なノードの種類
----------------

AST のノードは、大きく「文（``ast.stmt`` のサブクラス）」と「式（``ast.expr`` のサブクラス）」に分かれる。よく登場するものを以下に示す。

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - ノード
     - 分類
     - 対応する構文
   * - ``Module``
     - 根
     - ソースファイル全体（``body`` に文のリストを持つ）
   * - ``FunctionDef`` / ``AsyncFunctionDef``
     - 文
     - ``def`` / ``async def`` による関数定義
   * - ``ClassDef``
     - 文
     - ``class`` によるクラス定義
   * - ``Assign`` / ``AugAssign``
     - 文
     - 代入文 ``x = 1`` / 累算代入文 ``x += 1``
   * - ``Import`` / ``ImportFrom``
     - 文
     - ``import x`` / ``from x import y``
   * - ``If`` / ``For`` / ``While``
     - 文
     - 条件分岐とループ
   * - ``Name``
     - 式
     - 変数名などの識別子
   * - ``Constant``
     - 式
     - 数値・文字列・``None`` などのリテラル
   * - ``BinOp``
     - 式
     - ``a + b`` などの二項演算
   * - ``Call``
     - 式
     - 関数呼び出し ``f(x)``
   * - ``Attribute``
     - 式
     - 属性参照 ``obj.attr``

すべてのノードの一覧は、公式ドキュメントの :mod:`ast` に掲載されている抽象文法（abstract grammar）で確認できる。

literal_eval() による安全なリテラルの評価
------------------------------------------

組み込み関数 ``eval()`` は任意の式を実行するため、外部から受け取った文字列に使うと、ファイルの削除やコマンドの実行など意図しない処理を実行されるおそれがある。文字列で表された「値」を Python のオブジェクトに戻したいだけであれば、``ast.literal_eval()`` を使う。

``ast.literal_eval()`` が評価するのは、文字列・バイト列・数値・タプル・リスト・辞書・集合・真偽値・``None`` から成るリテラルだけである。関数呼び出しや名前の参照、演算子を含む式は評価せず、``ValueError`` を送出する。

.. code-block:: python
   :linenos:

   >>> ast.literal_eval("{'a': [1, 2], 'b': (3, None)}")
   {'a': [1, 2], 'b': (3, None)}
   >>> ast.literal_eval("-5")
   -5
   >>> ast.literal_eval("__import__('os').system('echo hi')")
   Traceback (most recent call last):
     ...
   ValueError: malformed node or string on line 1: ...
   >>> ast.literal_eval("2 ** 10")
   Traceback (most recent call last):
     ...
   ValueError: malformed node or string on line 1: ...

.. note::

   ``literal_eval()`` はコードを実行しない点で ``eval()`` より安全だが、非常に大きな入力や深く入れ子になった入力を与えると、メモリ不足や ``RecursionError`` を起こすことがある。信頼できない入力には事前に長さの上限を設けるとよい。また、データの受け渡しが目的であれば、最初から :doc:`../data_format/json` などのデータ形式を使う方が適切である。

NodeVisitor による木の走査
----------------------------

木全体から特定の種類のノードを探すには ``ast.NodeVisitor`` を継承したクラスを作る。``visit_ノード名`` という名前のメソッドを定義すると、``visit()`` で木をたどる途中でその種類のノードに出会うたびに呼び出される。メソッドの中で ``generic_visit()`` を呼ぶと、そのノードの子ノードの走査が続行される。

次の例は、ソースコードを実行せずに ``import`` されているモジュール名を集める。

.. code-block:: python
   :linenos:

   import ast

   SOURCE = """
   import os
   import sys
   from pathlib import Path

   def main():
       print(os.getcwd())
   """


   class ImportCollector(ast.NodeVisitor):
       def __init__(self) -> None:
           self.modules: list[str] = []

       def visit_Import(self, node: ast.Import) -> None:
           for alias in node.names:
               self.modules.append(alias.name)
           self.generic_visit(node)

       def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
           if node.module is not None:
               self.modules.append(node.module)
           self.generic_visit(node)


   collector = ImportCollector()
   collector.visit(ast.parse(SOURCE))
   print(collector.modules)  # ['os', 'sys', 'pathlib']

ノードの種類を問わず木のすべてのノードを順に取り出すだけであれば、``ast.walk()`` を使う方が簡単である。ただし、``ast.walk()`` が返すノードの順序は保証されていない。

.. code-block:: python
   :linenos:

   >>> tree = ast.parse(SOURCE)
   >>> [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
   ['main']

NodeTransformer による木の書き換えと unparse()
------------------------------------------------

``ast.NodeTransformer`` は ``NodeVisitor`` のサブクラスで、``visit_ノード名`` メソッドの戻り値で元のノードを置き換える。戻り値に ``None`` を返すとそのノードは削除される。書き換えた木は ``ast.unparse()`` でソースコードの文字列に戻したり、組み込み関数 ``compile()`` でコードオブジェクトにして実行したりできる。

次の例は、加算（``+``）をすべて乗算（``*``）に置き換える。

.. code-block:: python
   :linenos:

   import ast


   class AddToMult(ast.NodeTransformer):
       def visit_BinOp(self, node: ast.BinOp) -> ast.BinOp:
           self.generic_visit(node)  # 先に子ノードを書き換える
           if isinstance(node.op, ast.Add):
               node.op = ast.Mult()
           return node


   tree = AddToMult().visit(ast.parse("result = 3 + 4"))
   ast.fix_missing_locations(tree)
   print(ast.unparse(tree))  # result = 3 * 4

   namespace: dict[str, object] = {}
   exec(compile(tree, "<ast>", "exec"), namespace)
   print(namespace["result"])  # 12

新しく作ったノードには ``lineno`` などの位置情報が設定されていないため、``compile()`` に渡す前に ``ast.fix_missing_locations()`` で補っておく。

.. note::

   ``ast.unparse()`` が生成するのは、元の AST と等価なソースコードであり、元のソースコードそのものではない。コメントは AST に含まれないため失われ、空白や引用符の種類、括弧の付け方も元とは異なることがある。元の表記を保ったまま書き換えたい場合は、AST ではなく位置情報（``lineno``、``col_offset`` など）を使って元の文字列を部分的に編集する必要がある。元のソースコードからノードに対応する部分を取り出すには ``ast.get_source_segment()`` が使える。

その他の便利な機能
------------------

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 機能
     - 説明
   * - ``ast.get_docstring(node)``
     - 関数・クラス・モジュールのノードから docstring を取り出す。
   * - ``ast.get_source_segment(source, node)``
     - ソースコードのうち、ノードに対応する部分の文字列を返す。
   * - ``ast.increment_lineno(node, n)``
     - 木に含まれるノードの行番号をまとめて ``n`` だけずらす。
   * - ``ast.compare(a, b)``
     - 2 つの木の構造が等しいかを比較する（Python 3.14 で追加）。
   * - ``python -m ast ファイル名``
     - コマンドラインからファイルを解析し、``ast.dump()`` の結果を表示する。

関連するモジュール
------------------

* :mod:`symtable`: コンパイラが作成するシンボルテーブル（各スコープにどの名前が定義されているか）を調べる。
* :mod:`dis`: コンパイル後のバイトコードを逆アセンブルして表示する。AST の次の段階を確認できる。
* :mod:`tokenize`: ソースコードを AST よりも低い水準のトークン列に分解する。コメントや空白の情報も保持されるため、元の表記を保ったまま処理したい場合に使う。
* :mod:`inspect`: ``inspect.getsource()`` で関数などのソースコードを取得でき、``ast.parse()`` と組み合わせて使われることが多い。
