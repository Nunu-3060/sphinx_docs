################################################################
第 6 章 意味解析
################################################################

構文解析が成功しても、プログラムが正しいとは限りません。``let x = 1 + "a";`` は文法上は正しい文ですが、整数と文字列を足すことはできません。この章では、文法では表せない規則を検査する\ :term:`意味解析`\ を実装します。

意味解析の役割
================================================================

文脈自由文法は、「変数は使う前に宣言されていなければならない」「``+`` の両辺は同じ型でなければならない」といった、離れた場所どうしの関係に関する規則を表せません。意味解析は、抽象構文木をたどりながら、このような規則を検査します。Tiny の意味解析器（``tiny_checker.py``）は次のことを行います。

* :term:`名前解決`：変数や関数の名前が、どの宣言を指しているかを決めます。宣言されていない名前を使っていればエラーにします。
* :term:`型検査`：各式の型を求め、演算子・代入・関数呼び出しの型が合っているかを検査します。求めた型は、式のノードの ``ty`` 属性に書き込みます。
* その他の検査：``main`` 関数の有無、値を返す関数がすべての経路で ``return`` しているか、などを検査します。

意味解析を通過したプログラムは、実行時に型の誤りが起きないことが保証されます。そのため、後の段階（インタプリタやコード生成）は型の検査を省略できます。

名前解決とスコープ
================================================================

変数の宣言が有効な範囲を\ :term:`スコープ`\ と呼びます。Tiny では、ブロック ``{ ... }`` ごとに新しいスコープができ、変数はその宣言からブロックの終わりまで有効です。

.. code-block:: tiny
   :linenos:

   fn main() {
       let x = 1;
       {
           let x = "inner";  // 外側の x を隠す
           print(x);         // inner
       }
       print(x);             // 1
   }

ソースコード上の位置だけでどの宣言を指すかが決まるこのようなスコープを、静的スコープ（レキシカルスコープ）と呼びます。

名前と、それに関する情報（ここでは型）の対応表を\ :term:`記号表`\ と呼びます。Tiny の意味解析器では、ブロックごとに ``Scope`` オブジェクトを作り、外側のスコープへの参照 ``parent`` を持たせます。名前を探すときは、内側のスコープから外側に向かって順にたどります。

.. literalinclude:: ../examples/tiny_checker.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Scope
   :caption: tiny_checker.py（記号表）

同じスコープで同じ名前を 2 度宣言するとエラーになりますが、内側のスコープでは同じ名前を宣言できます。

型検査
================================================================

型検査の規則は、:term:`型付け規則`\ という形で書くと簡潔に表せます。次の規則は、「環境 :math:`\Gamma` のもとで :math:`e_1` と :math:`e_2` の型がどちらも ``int`` ならば、:math:`e_1 + e_2` の型は ``int`` である」という意味です。横線の上が前提、下が結論です。

.. math::

   \frac{\Gamma \vdash e_1 : \mathtt{int} \qquad \Gamma \vdash e_2 : \mathtt{int}}
        {\Gamma \vdash e_1 + e_2 : \mathtt{int}}

環境 :math:`\Gamma` は記号表にあたり、変数の名前から型への対応です。Tiny の主な型付け規則を示します。

.. math::

   \frac{\Gamma \vdash e_1 : \mathtt{str} \qquad \Gamma \vdash e_2 : \mathtt{str}}
        {\Gamma \vdash e_1 + e_2 : \mathtt{str}}
   \qquad
   \frac{\Gamma \vdash e_1 : \mathtt{int} \qquad \Gamma \vdash e_2 : \mathtt{int}}
        {\Gamma \vdash e_1 < e_2 : \mathtt{bool}}

.. math::

   \frac{\Gamma \vdash e_1 : T \qquad \Gamma \vdash e_2 : T}
        {\Gamma \vdash e_1 == e_2 : \mathtt{bool}}
   \qquad
   \frac{\Gamma \vdash a : [T] \qquad \Gamma \vdash i : \mathtt{int}}
        {\Gamma \vdash a[i] : T}
   \qquad
   \frac{\Gamma \vdash s : \mathtt{str} \qquad \Gamma \vdash i : \mathtt{int}}
        {\Gamma \vdash s[i] : \mathtt{str}}
   \qquad
   \frac{\Gamma \vdash s : \mathtt{str} \qquad \Gamma \vdash i : \mathtt{int}}
        {\Gamma \vdash s[i] : \mathtt{str}}
   \qquad
   \frac{x : T \in \Gamma}{\Gamma \vdash x : T}

意味解析器は、これらの規則を式の構造に沿って再帰的に適用します。式の種類ごとの処理は ``infer`` メソッドにまとめています。

.. literalinclude:: ../examples/tiny_checker.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Checker.infer
   :caption: tiny_checker.py（式の型を求める）

二項演算子の規則は ``check_binary`` で検査します。``+`` は左辺の型によって、整数の加算と文字列の連結のどちらかに決まります。

.. literalinclude:: ../examples/tiny_checker.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Checker.check_binary
   :caption: tiny_checker.py（二項演算子の型検査）

期待される型を使う検査
================================================================

型は通常、式の内側から外側に向かって決まります（``1`` が ``int`` なので ``1 + 2`` も ``int``）。しかし、空の配列リテラル ``[]`` は要素がないため、内側から型を決められません。そこで Tiny の意味解析器では、式を検査するときに「その位置で期待される型」を外側から渡せるようにしています。

.. literalinclude:: ../examples/tiny_checker.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: Checker.check_expr
   :caption: tiny_checker.py（期待される型を使う検査）

``let a: [int] = [];`` では型注釈の ``[int]`` が、``return [];`` では関数の戻り値の型が、``f([])`` では引数の型が、期待される型として渡されます。このように、型を内側から求める処理と、外側から与える処理を組み合わせる方法を双方向の型検査と呼びます。

return の検査
================================================================

値を返す関数で ``return`` を書き忘れると、関数の末尾に達したときに返す値がありません。意味解析器は、関数の本体が必ず ``return`` で終わるかを判定します。

.. literalinclude:: ../examples/tiny_checker.py
   :language: python
   :linenos:
   :lineno-match:
   :pyobject: always_returns
   :caption: tiny_checker.py（必ず return するかの判定）

この判定は保守的です。``while (true) { return 1; }`` のように実際には必ず ``return`` する場合でも、``while`` 文は「必ず return する」とはみなしません。プログラムが実際にどう動くかを完全に判定することは一般には不可能なので、意味解析では「誤りを見逃さない代わりに、正しいプログラムを拒否することがある」という保守的な近似を使うのがふつうです。

エラーメッセージ
================================================================

意味解析器が報告するエラーの例を示します。

.. code-block:: tiny
   :linenos:
   :caption: programs/type_error.tiny

   // 意味解析でエラーになるプログラム
   fn twice(n: int) -> int {
       return n * 2;
   }

   fn main() {
       let s = "abc";
       print(twice(s));
   }

.. code-block:: console
   :linenos:

   $ python tiny.py check programs/type_error.tiny
   programs/type_error.tiny:8: 型 int が必要ですが、型 str の式があります

ほかにも、次のような誤りを検出します（行番号は省略しています）。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - プログラム
     - エラーメッセージ
   * - ``let a = [];``
     - 空の配列の型を決められません
   * - ``print(y);``
     - 変数 y は宣言されていません
   * - ``let x = 1; let x = 2;``
     - 変数 x はこのスコープで宣言済みです
   * - ``let s = "abc"; s[0] = "x";``
     - 文字列の要素には代入できません
   * - ``if (1) { }``
     - 型 bool が必要ですが、型 int の式があります
   * - ``else`` のない ``if`` の中でだけ ``return`` する関数
     - 関数 f の末尾に return がありません

Tiny の意味解析器は最初のエラーで処理を止めます。構文解析器と同じように複数のエラーを報告することもできますが、1 つの誤りから多数のエラーが連鎖的に発生しやすいので注意が必要です。たとえば宣言を誤った変数は、使うたびに「宣言されていません」というエラーになります。

Python の symtable モジュール
================================================================

CPython も、バイトコードを生成する前に記号表を作り、各変数の種類を決めます。Python では、関数内で代入される変数は局所変数、代入されずに参照されるだけの変数は大域変数（または外側の関数の変数）になります。``symtable`` モジュールを使うと、その結果を確認できます。

.. code-block:: python
   :linenos:
   :caption: symtable モジュールの使用例

   import symtable

   source = """
   def f(a):
       b = a + g
       def h():
           return b
       return h
   """
   table = symtable.symtable(source, "<example>", "exec")
   f = next(t for t in table.get_children() if t.get_name() == "f")
   h = next(t for t in f.get_children() if t.get_name() == "h")
   for scope in (f, h):
       print(f"関数 {scope.get_name()}")
       for sym in scope.get_symbols():
           kinds = [k for k, ok in [
               ("parameter", sym.is_parameter()), ("local", sym.is_local()),
               ("global", sym.is_global()), ("free", sym.is_free())] if ok]
           print(f"  {sym.get_name()}: {', '.join(kinds)}")

.. code-block:: text
   :linenos:

   関数 f
     a: parameter, local
     b: local
     g: global
     h: local
   関数 h
     b: free

``h`` の中の ``b`` は ``free``\ （自由変数）になっています。自由変数は、外側の関数 ``f`` の局所変数を参照する変数で、クロージャを作るために使われます。Tiny にはクロージャがないので、関数の中から参照できるのは引数と局所変数だけです。

まとめ
================================================================

* 意味解析は、名前解決や型検査など、文法では表せない規則を検査します。
* 記号表はスコープごとに作り、内側から外側に向かって名前を探します。
* 型検査の規則は型付け規則として書け、式の構造に沿って再帰的に適用します。
* 期待される型を外側から渡すと、空の配列のように内側から型を決められない式も扱えます。
* 意味解析の判定は保守的な近似であり、正しいプログラムを拒否する場合があります。
