JavaScript の基礎
=================

本章では、JavaScript の文法を Python と比較しながら説明する。JavaScript は Python と同じく動的型付けの言語であり、多くの概念はそのまま対応する。一方で、型変換や ``undefined`` の扱いなど、Python の感覚で書くと誤りやすい点もある。本章ではそうした違いを中心に扱う。

なお、JavaScript の正式な仕様は ECMAScript と呼ばれる。本章で扱う文法は、2015 年に策定された ECMAScript 2015（ES2015）以降のものである。

JavaScript の実行方法
---------------------

HTML から JavaScript を実行するには、``script`` 要素を使う。

.. code-block:: html

   <!-- 外部ファイルを読み込む -->
   <script src="app.js" defer></script>

   <!-- HTML の中に直接書く -->
   <script>
     console.log("Hello");
   </script>

ブラウザは HTML を先頭から解析し、``script`` 要素に出会うと、その場でスクリプトを読み込んで実行する。実行が終わるまで HTML の解析は中断される。そのため、``head`` 要素の中に書いたスクリプトから ``body`` 要素の中の要素を操作しようとすると、まだその要素が作られていないため失敗する。

``defer`` 属性を付けると、スクリプトの読み込みは HTML の解析と並行して行われ、実行は HTML の解析が終わってから行われる。複数の ``defer`` 付きスクリプトは、書かれた順に実行される。外部ファイルを読み込む場合は、``head`` 要素の中に ``defer`` 属性付きで書くのが一般的である。なお、``defer`` 属性は外部ファイルにのみ有効であり、HTML に直接書いたスクリプトには効果が無い。直接書く場合は、``body`` 要素の終了タグの直前に置く。

``console.log`` は、引数の値を開発者ツールのコンソールに出力する関数であり、Python の ``print`` に相当する。開発者ツールのコンソールには JavaScript のコードを直接入力して実行することもできるため、本章の例を試すときに利用するとよい。

本章のサンプルは、次の HTML から 2 つの JavaScript ファイルを読み込んで実行する。ページを開いたら、開発者ツールのコンソールで出力を確認すること。

.. literalinclude:: ../examples/ch06/js_basics.html
   :language: html
   :caption: examples/ch06/js_basics.html

:download:`js_basics.html をダウンロード <../examples/ch06/js_basics.html>` ／ `ブラウザで表示 <examples/ch06/js_basics.html>`__

文法の基本的な違い
~~~~~~~~~~~~~~~~~~

.. list-table:: Python と JavaScript の基本的な違い
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - Python
     - JavaScript
   * - ブロック
     - インデントで表す。
     - ``{`` と ``}`` で囲む。インデントは見やすさのためであり、意味を持たない。
   * - 文の終わり
     - 改行。
     - ``;``。省略しても多くの場合は自動で補われるが、補われ方が意図と異なることがあるため、本資料では常に書く。
   * - コメント
     - ``#``
     - ``//`` （1 行）、``/*`` ～ ``*/`` （複数行）。
   * - 命名の慣習
     - ``snake_case``
     - ``camelCase``。クラス名は ``PascalCase``、定数は ``UPPER_SNAKE_CASE`` とすることが多い。

変数宣言
--------

JavaScript では、変数を使う前に ``const`` または ``let`` で宣言する。

.. code-block:: javascript

   const PI = 3.14159; // 再代入できない
   let count = 0;      // 再代入できる
   count += 1;

.. list-table:: 変数の宣言方法
   :header-rows: 1
   :widths: 15 85

   * - 宣言
     - 意味
   * - ``const``
     - 再代入できない変数を宣言する。ただし、中身が配列やオブジェクトの場合、要素やプロパティの変更はできる。変数が指す先を変えられないだけである。
   * - ``let``
     - 再代入できる変数を宣言する。
   * - ``var``
     - 古い宣言方法。スコープがブロックではなく関数単位になる、宣言前に参照してもエラーにならないなど、誤りの原因になりやすい性質を持つため、現在は使わない。

``const`` と ``let`` の変数は、宣言したブロック（``{`` ～ ``}``）の中でだけ有効である。Python では ``if`` 文や ``for`` 文の中で作った変数がブロックの外でも使えるが、JavaScript では使えない。

基本的には ``const`` を使い、再代入が必要な場合だけ ``let`` を使うとよい。再代入されない変数が一目で分かるため、コードが読みやすくなる。

データ型
--------

.. list-table:: 主なデータ型
   :header-rows: 1
   :widths: 20 35 45

   * - 型
     - 例
     - Python との違い
   * - ``number``
     - ``42``、``3.14``
     - 整数と小数の区別が無く、どちらも浮動小数点数として扱われる。``7 / 2`` は ``3.5`` になる。整数除算は ``Math.floor(7 / 2)`` のように書く。
   * - ``string``
     - ``"text"``、``'text'``
     - Python と同様に、ダブルクォートとシングルクォートのどちらでもよい。
   * - ``boolean``
     - ``true``、``false``
     - Python の ``True``、``False`` と異なり、小文字で書く。
   * - ``undefined``
     - ``undefined``
     - 値が代入されていないことを表す。宣言だけした変数や、存在しないプロパティを参照したときの値になる。
   * - ``null``
     - ``null``
     - 値が無いことを明示的に表す。Python の ``None`` に近い。
   * - オブジェクト
     - ``{ name: "山田" }``、``[1, 2, 3]``
     - 上記以外の値はすべてオブジェクトである。配列や関数もオブジェクトの一種である。

値の型は ``typeof`` 演算子で調べられる。ただし、``typeof null`` は ``"object"`` を返す。これは初期の JavaScript の不具合が互換性のために残されたものである。値が ``null`` かどうかは ``value === null`` で調べる。

また、存在しない値を参照してもエラーにならず ``undefined`` が返る点に注意する。Python では存在しない辞書のキーを参照すると ``KeyError`` が発生するが、JavaScript では ``undefined`` が返り、処理が続いてしまう。

演算子
------

== と === の違い
~~~~~~~~~~~~~~~~

JavaScript には、等しいかどうかを比べる演算子が 2 種類ある。

.. list-table:: 比較演算子
   :header-rows: 1
   :widths: 20 50 30

   * - 演算子
     - 意味
     - 例
   * - ``===`` ／ ``!==``
     - 型と値の両方が等しいか（等しくないか）を比べる。
     - ``1 === "1"`` は ``false``
   * - ``==`` ／ ``!=``
     - 型が異なる場合、型を変換してから比べる。
     - ``1 == "1"`` は ``true``

``==`` の型変換の規則は複雑で、意図しない結果になりやすい。比較には常に ``===`` と ``!==`` を使う。

暗黙の型変換
~~~~~~~~~~~~

JavaScript は、型の異なる値どうしの演算でもエラーにせず、自動で型を変換する。Python では ``"5" + 2`` は ``TypeError`` になるが、JavaScript では次のようになる。

.. code-block:: javascript

   "5" * 2; // 10   (文字列が数値に変換される)
   "5" + 2; // "52" (+ の片方が文字列なら、文字列の連結になる)

フォームの入力値は常に文字列であるため、数値として計算するときは ``Number("5")`` のように明示的に変換する。

論理演算子
~~~~~~~~~~

論理演算子は Python の ``and``、``or``、``not`` に対応して、``&&``、``||``、``!`` と書く。

``??`` は、左辺が ``null`` または ``undefined`` のときに右辺の値を返す演算子である。値が無い場合の既定値を指定するときに使う。

.. code-block:: javascript

   const name = input ?? "ゲスト"; // input が null か undefined なら "ゲスト"

``||`` でも似たことができるが、``||`` は ``0`` や空文字列 ``""`` のときにも右辺を返す点が異なる。

条件分岐とループ
----------------

条件分岐
~~~~~~~~

``if`` 文の条件は ``(`` と ``)`` で囲む。Python の ``elif`` は ``else if`` と書く。

.. code-block:: javascript

   if (score >= 80) {
     console.log("優");
   } else if (score >= 60) {
     console.log("良");
   } else {
     console.log("可");
   }

Python の条件式 ``a if 条件 else b`` に相当するものとして、三項演算子 ``条件 ? a : b`` がある。

ループ
~~~~~~

.. list-table:: ループの書き方
   :header-rows: 1
   :widths: 40 60

   * - JavaScript
     - 意味
   * - ``for (let i = 0; i < 3; i++) { ... }``
     - 初期化・継続条件・更新処理を指定するループ。Python の ``for i in range(3):`` に相当する。``i++`` は ``i += 1`` と同じ意味である。
   * - ``for (const x of array) { ... }``
     - 配列の値を順に取り出す。Python の ``for x in array:`` に相当する。
   * - ``for (const key in object) { ... }``
     - オブジェクトのキーを順に取り出す。
   * - ``while (条件) { ... }``
     - 条件を満たす間繰り返す。Python の ``while`` 文と同じである。

``for...of`` と ``for...in`` の違いに注意する。配列に ``for...in`` を使うと、値ではなく添字が文字列として（``"0"``、``"1"``、…）取り出される。配列の値を取り出すには ``for...of`` を使う。

``break`` と ``continue`` は Python と同じように使える。

関数
----

JavaScript で関数を作る方法は主に 2 つある。

.. code-block:: javascript

   // 関数宣言
   function add(a, b) {
     return a + b;
   }

   // アロー関数 (Python の lambda に近いが、複数の文も書ける)
   const greet = (name = "ゲスト") => `こんにちは、${name} さん`;

アロー関数は ``(引数) => 式`` の形で書き、式の値が戻り値になる。複数の文を書く場合は ``(引数) => { 文; return 値; }`` のように ``{`` と ``}`` で囲み、``return`` で値を返す。引数が 1 つの場合は ``(`` と ``)`` を省略できるが、本資料では省略しない。

引数には、Python と同様に ``=`` で既定値を指定できる。一方、Python と異なり、関数を呼び出すときの引数の数が定義と一致しなくてもエラーにならない。渡されなかった引数は ``undefined`` になる。また、Python のキーワード引数（``f(name="山田")``）に相当する仕組みは無く、代わりにオブジェクトを渡すことが多い。

JavaScript の関数は値として扱えるため、変数に代入したり、他の関数の引数として渡したりできる。この性質は、後述する配列のメソッドや、第 7 章のイベント処理で多用する。

配列
----

配列は Python のリストに相当する。``[`` と ``]`` で囲んで作り、添字は 0 から始まる。要素の数は ``length`` プロパティで得られる。

JavaScript には Python のリスト内包表記が無い。代わりに、関数を引数に取る配列のメソッドを使う。

.. list-table:: 配列の主なメソッド
   :header-rows: 1
   :widths: 35 30 35

   * - JavaScript
     - Python での書き方
     - 意味
   * - ``a.map((x) => x * 2)``
     - ``[x * 2 for x in a]``
     - 各要素を変換した新しい配列を返す。
   * - ``a.filter((x) => x > 0)``
     - ``[x for x in a if x > 0]``
     - 条件を満たす要素だけの新しい配列を返す。
   * - ``a.reduce((s, x) => s + x, 0)``
     - ``sum(a)``
     - 要素を順に 1 つの値にまとめる。
   * - ``a.find((x) => x > 0)``
     - ``next((x for x in a if x > 0), None)``
     - 条件を満たす最初の要素を返す。無ければ ``undefined`` を返す。
   * - ``a.some((x) => x > 0)``
     - ``any(x > 0 for x in a)``
     - 条件を満たす要素が 1 つでもあれば ``true`` を返す。
   * - ``a.every((x) => x > 0)``
     - ``all(x > 0 for x in a)``
     - すべての要素が条件を満たせば ``true`` を返す。
   * - ``a.includes(3)``
     - ``3 in a``
     - 要素が含まれているかどうかを返す。
   * - ``a.push(4)``
     - ``a.append(4)``
     - 末尾に要素を追加する。
   * - ``a.slice(1)``
     - ``a[1:]``
     - 一部を取り出した新しい配列を返す。
   * - ``[...a, ...b]``
     - ``[*a, *b]``
     - 配列を展開して連結する（スプレッド構文）。

``sort`` メソッドには注意が必要である。引数なしで呼び出すと、要素を文字列として比較するため、``[10, 9, 1, 100].sort()`` は ``[1, 10, 100, 9]`` になる。数値として並べるには ``sort((a, b) => a - b)`` のように比較関数を渡す。また、``sort`` は Python の ``list.sort`` と同様に元の配列を並べ替える。

.. literalinclude:: ../examples/ch06/array_methods.js
   :language: javascript
   :caption: examples/ch06/array_methods.js

:download:`array_methods.js をダウンロード <../examples/ch06/array_methods.js>`

同じ処理を Python で書くと、次のようになる。

.. literalinclude:: ../examples/ch06/compare_python.py
   :language: python
   :caption: examples/ch06/compare_python.py

:download:`compare_python.py をダウンロード <../examples/ch06/compare_python.py>`

オブジェクトと JSON
-------------------

オブジェクト
~~~~~~~~~~~~

JavaScript のオブジェクトは、キーと値の組の集まりであり、Python の辞書に相当する。

.. code-block:: javascript

   const user = { name: "山田", age: 30 };
   console.log(user.name);   // "山田"
   console.log(user["age"]); // 30
   user.email = "yamada@example.com"; // プロパティの追加

キーは引用符で囲まずに書ける。値は ``user.name`` のようにドットでも、``user["name"]`` のように角括弧でも参照できる。キーを変数で指定する場合は角括弧を使う。

オブジェクトから値を取り出して変数に代入するには、分割代入を使う。Python のアンパック代入に近い機能である。

.. code-block:: javascript

   const { name, age } = user; // name = user.name, age = user.age と同じ

キーと値の組を順に処理するには ``Object.entries`` を使う。Python の ``dict.items()`` に相当する。

JSON
~~~~

JSON（JavaScript Object Notation）は、JavaScript のオブジェクトの書き方をもとにしたデータ形式であり、Web でデータをやり取りするときに広く使われる。JSON では、キーを必ずダブルクォートで囲む必要がある。

.. list-table:: JSON の変換
   :header-rows: 1
   :widths: 35 30 35

   * - JavaScript
     - Python
     - 意味
   * - ``JSON.stringify(obj)``
     - ``json.dumps(obj)``
     - オブジェクトを JSON 文字列に変換する。
   * - ``JSON.parse(text)``
     - ``json.loads(text)``
     - JSON 文字列をオブジェクトに変換する。

テンプレートリテラル
--------------------

バッククォート（`````）で囲んだ文字列をテンプレートリテラルと呼ぶ。``${`` と ``}`` の中に式を書くと、その値が埋め込まれる。Python の f-string に相当する。

.. code-block:: javascript

   const name = "山田";
   const message = `こんにちは、${name} さん`; // Python: f"こんにちは、{name} さん"

テンプレートリテラルは、途中で改行して複数行の文字列を書くこともできる。

スコープとクロージャ
--------------------

関数の中で定義した関数は、外側の関数の変数を参照できる。外側の関数の実行が終わった後も、内側の関数はその変数を参照し続けられる。このような関数をクロージャと呼ぶ。Python でも同じ仕組みがあるが、JavaScript では ``nonlocal`` 宣言をしなくても外側の変数に再代入できる。

.. code-block:: javascript

   function makeCounter() {
     let value = 0; // 外から直接は参照できない
     return () => {
       value += 1; // 外側の関数の変数を更新する
       return value;
     };
   }

   const counter = makeCounter();
   counter(); // 1
   counter(); // 2

クロージャは、第 7 章のイベント処理で、処理に必要な値を関数に持たせるときに自然に使われる。

クラス
------

JavaScript のクラスは、Python のクラスとほぼ同じように書ける。

.. list-table:: クラスの書き方の対応
   :header-rows: 1
   :widths: 35 35 30

   * - JavaScript
     - Python
     - 意味
   * - ``constructor(name) { ... }``
     - ``def __init__(self, name):``
     - コンストラクター。
   * - ``this.name``
     - ``self.name``
     - インスタンス自身のプロパティ。``this`` は引数に書かない。
   * - ``class Dog extends Animal``
     - ``class Dog(Animal):``
     - 継承。
   * - ``super.speak()``
     - ``super().speak()``
     - 親クラスのメソッドの呼び出し。
   * - ``new Dog("ポチ")``
     - ``Dog("ポチ")``
     - インスタンスの作成。JavaScript では ``new`` が必要である。

例外処理
--------

例外処理は ``try...catch`` 文で行う。Python の ``try...except`` に相当する。例外を発生させるには ``throw`` を使う。

.. code-block:: javascript

   try {
     throw new Error("エラーの内容");
   } catch (error) {
     console.log(error.message);
   } finally {
     console.log("必ず実行される");
   }

Python と異なり、例外の種類ごとに ``catch`` を分けて書く構文は無い。種類によって処理を分けたい場合は、``catch`` の中で ``error instanceof TypeError`` のように判定する。

また、JavaScript では Python で例外になる多くの操作がエラーにならない。たとえば ``1 / 0`` は ``Infinity`` に、数値に変換できない文字列の変換 ``Number("abc")`` は ``NaN`` （Not a Number）になる。

ここまでの内容をまとめたサンプルを次に示す。

.. literalinclude:: ../examples/ch06/basics.js
   :language: javascript
   :caption: examples/ch06/basics.js

:download:`basics.js をダウンロード <../examples/ch06/basics.js>`

モジュール
----------

プログラムが大きくなったら、ファイルを分割してモジュールにする。モジュールから外部に公開したい値には ``export`` を付け、使う側で ``import`` する。

.. list-table:: モジュールの書き方の対応
   :header-rows: 1
   :widths: 50 50

   * - JavaScript
     - Python
   * - ``import { withTax } from "./math_utils.js";``
     - ``from math_utils import with_tax``
   * - ``import formatYen from "./math_utils.js";``
     - （対応する構文は無い）

``export`` には、名前を付けて複数の値を公開する名前付きエクスポートと、モジュールごとに 1 つだけ公開するデフォルトエクスポート（``export default``）の 2 種類がある。デフォルトエクスポートは、``import`` する側で任意の名前を付けて受け取る。

Python と異なり、``export`` を付けていない値は外部から一切参照できない。また、``import`` のファイル名には ``./`` と拡張子 ``.js`` を含めて書く。

モジュールを使うには、``script`` 要素に ``type="module"`` を指定する。モジュールとして読み込んだスクリプトは、``defer`` 属性を付けた場合と同様に、HTML の解析が終わってから実行される。

モジュールは ``file://`` で開いたページでは読み込めない。次のサンプルは、第 1 章で説明したローカルサーバーを起動してから開くこと。

.. literalinclude:: ../examples/ch06/modules/math_utils.js
   :language: javascript
   :caption: examples/ch06/modules/math_utils.js

.. literalinclude:: ../examples/ch06/modules/main.js
   :language: javascript
   :caption: examples/ch06/modules/main.js

.. literalinclude:: ../examples/ch06/modules/index.html
   :language: html
   :caption: examples/ch06/modules/index.html

:download:`math_utils.js をダウンロード <../examples/ch06/modules/math_utils.js>` ／ :download:`main.js をダウンロード <../examples/ch06/modules/main.js>` ／ :download:`index.html をダウンロード <../examples/ch06/modules/index.html>` ／ `ブラウザで表示 <examples/ch06/modules/index.html>`__
