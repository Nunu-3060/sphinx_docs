デザインパターン
================

:term:`デザインパターン` とは、ソフトウェアの設計でよく現れる問題と、その解決策に名前を付けてまとめたものです。この章では、デザインパターンの考え方と、Python でよく使われるパターンを説明します。また、Python では関数などの言語の機能で、パターンをより簡潔に実現できる場合があることも示します。

デザインパターンとは
--------------------

デザインパターンという言葉を広めたのは、E. Gamma、R. Helm、R. Johnson、J. Vlissides の 4 人（GoF: Gang of Four と呼ばれます）が 1994 年に出版した書籍です。この書籍では、23 のパターンが、目的によって次の 3 つに分類されています。

.. list-table::
   :header-rows: 1
   :widths: 20 35 45

   * - 分類
     - 目的
     - パターン
   * - 生成に関するパターン
     - オブジェクトの作り方を、使う側から切り離します。
     - Abstract Factory、Builder、Factory Method、Prototype、Singleton
   * - 構造に関するパターン
     - クラスやオブジェクトを組み合わせて、より大きな構造を作ります。
     - Adapter、Bridge、Composite、Decorator、Facade、Flyweight、Proxy
   * - 振る舞いに関するパターン
     - オブジェクトの間の責任の分担と、やり取りの方法を決めます。
     - Chain of Responsibility、Command、Interpreter、Iterator、Mediator、Memento、Observer、State、Strategy、Template Method、Visitor

パターンを学ぶ利点は、次の 2 つです。

* 先人が見つけた、実績のある解決策を使えます。
* 「ここは Strategy パターンにしよう」のように、設計の意図を短い言葉で伝えられます。

一方で、パターンを使うこと自体を目的にしてはいけません。パターンは特定の問題に対する解決策なので、その問題がないところにパターンを当てはめると、不要な複雑さを持ち込むだけです。

Strategy パターン
-----------------

**問題**: 処理の一部（アルゴリズム）を、状況に応じて切り替えたいとします。

**解決策**: 切り替えたい処理をインターフェースとして定義し、処理ごとにそのインターフェースを実装するクラスを作ります。利用する側は、インターフェースを通して処理を呼び出します。

会計の割引の計算を例にします。割引の方法（割引なし、一定の割合の割引、一定の金額の割引）を ``DiscountStrategy`` として定義し、``Checkout`` は受け取った戦略に計算を任せます。

.. literalinclude:: ../examples/ch08_strategy.py
   :language: python
   :caption: ch08_strategy.py（クラスによる実装）
   :start-at: class DiscountStrategy
   :end-before: # ----

戦略のインターフェースが 1 つのメソッドだけを持つ場合、Python では関数で十分です。Python の関数は、数値や文字列と同じように値として扱える（第一級のオブジェクトである）ので、引数として渡したり、変数に代入したりできます。

.. literalinclude:: ../examples/ch08_strategy.py
   :language: python
   :caption: ch08_strategy.py（関数による実装）
   :start-at: Discount = Callable
   :end-before: def main

:download:`ch08_strategy.py <../examples/ch08_strategy.py>`

``rate_discount`` は、割引率を受け取り、その割引率で計算する関数を作って返します。このように、関数が外側の関数の変数（ここでは ``rate``）を覚えている仕組みを :term:`クロージャー` と呼びます。戦略が設定値を持つ場合も、クロージャーを使えばクラスは不要です。

Factory（生成の分離）
---------------------

**問題**: 設定やデータの内容によって、作るオブジェクトのクラスを変えたいとします。しかし、利用する側に「どのクラスを作るか」の分岐を散らばらせたくはありません。

**解決策**: オブジェクトを作る処理を 1 か所（ファクトリ）にまとめます。

GoF の Factory Method パターンは、オブジェクトを作るメソッドをサブクラスで上書きするという、継承を使ったパターンです。Python では、次のように **名前と、オブジェクトを作る関数（またはクラス）の対応表** を使う単純なファクトリ関数で済むことが多くあります。Python のクラスは呼び出すとインスタンスを作るので、クラスそのものを「オブジェクトを作る関数」として表に登録できます。

.. literalinclude:: ../examples/ch08_factory.py
   :language: python
   :caption: ch08_factory.py
   :start-at: # 形式の名前と
   :end-before: def main

:download:`ch08_factory.py <../examples/ch08_factory.py>`

新しい出力形式を追加するときは、クラスを作って ``_EXPORTERS`` に 1 行追加するだけで済みます。``create_exporter`` を呼ぶ側は、変更する必要がありません。

Adapter パターン
----------------

**問題**: 使いたいクラスのインターフェースが、アプリケーションが期待するインターフェースと合いません。そのクラスは外部のライブラリのものなので、変更もできません。

**解決策**: インターフェースを変換するクラス（アダプター）を間に挟みます。

次の例では、アプリケーションは摂氏の気温を返す ``TemperatureSource`` を期待していますが、外部のライブラリの ``LegacyThermometer`` は、華氏の気温を 10 倍した整数で返します。``LegacyThermometerAdapter`` が、この違いを吸収します。

.. literalinclude:: ../examples/ch08_adapter.py
   :language: python
   :caption: ch08_adapter.py
   :start-at: class TemperatureSource
   :end-before: def main

:download:`ch08_adapter.py <../examples/ch08_adapter.py>`

アダプターを使うと、外部のライブラリの事情（単位や、値の表し方）が、アプリケーションの中に広がりません。ライブラリを別のものに変えるときも、アダプターを作り直すだけで済みます。この考え方は、:doc:`architecture` のヘキサゴナルアーキテクチャにおける「アダプター」の由来でもあります。

Decorator パターン
------------------

**問題**: オブジェクトに機能（ログの記録、キャッシュ、再試行など）を追加したいとします。しかし、元のクラスは変更したくありませんし、機能の組み合わせごとにサブクラスを作りたくもありません。

**解決策**: 元のオブジェクトと同じインターフェースを持つオブジェクトで、元のオブジェクトを包みます。包む側は、処理の前後に機能を追加し、本来の処理は元のオブジェクトに任せます。

:doc:`oop` の ``LoggingSender`` と ``RetryingSender`` は、Decorator パターンの例です。

関数に機能を追加したいだけであれば、Python の **デコレーター構文**\ （``@``）が使えます。デコレーターは、関数を受け取り、機能を追加した新しい関数を返す関数です。次の ``timed`` は、関数の処理時間を表示する機能を追加します。

.. literalinclude:: ../examples/ch08_decorator.py
   :language: python
   :caption: ch08_decorator.py
   :start-at: P = ParamSpec
   :end-before: def main

:download:`ch08_decorator.py <../examples/ch08_decorator.py>`

``functools.wraps`` は、元の関数の名前や docstring を、新しい関数に引き継ぎます。``ParamSpec`` と ``TypeVar`` を使うと、デコレーターを付けた関数の引数と戻り値の型が、mypy に正しく伝わります。標準ライブラリにも、結果をキャッシュする ``functools.cache`` など、便利なデコレーターが用意されています。

なお、Python のデコレーター構文と、GoF の Decorator パターンは、名前は同じですが別のものです。デコレーター構文は関数やクラスを変換する言語の仕組みで、Decorator パターンはオブジェクトを包んで機能を追加する設計の手法です。

Observer パターン
-----------------

**問題**: ある出来事が起きたときに、複数の処理を実行したいとします。しかし、出来事を起こす側が、実行される処理のすべてを知っているのは避けたいところです。

**解決策**: 出来事（イベント）に関心のある処理を、あらかじめ登録しておきます。出来事が起きたら、登録されている処理に通知します。

注文が確定したときに、確認のメールの送信とポイントの付与を行う例です。

.. literalinclude:: ../examples/ch08_observer.py
   :language: python
   :caption: ch08_observer.py
   :start-at: @dataclass(frozen=True)
   :end-before: if __name__

:download:`ch08_observer.py <../examples/ch08_observer.py>`

イベントを発行する側（この例では ``main``）は、``bus.publish(OrderPlaced(...))`` を呼ぶだけで、メールやポイントのことを知りません。「在庫を引き当てる」処理を追加したくなっても、新しい関数を登録するだけで済み、イベントを発行する側は変更しません。

一方で、Observer パターンを多用すると、「ある出来事が起きたときに、最終的に何が実行されるのか」をコードから追いにくくなります。処理の順序に意味がある場合や、処理が 1 つしかない場合は、直接呼び出すほうが分かりやすいこともあります。

Template Method パターン
------------------------

**問題**: 処理の大まかな手順は共通ですが、手順の一部だけが場合によって異なります。

**解決策**: 手順の全体を基底クラスのメソッド（テンプレートメソッド）に書き、異なる部分だけを抽象メソッドとしてサブクラスに実装させます。

データの取り込みの手順（解析 → 検証 → 結果の報告）を基底クラスで決め、解析の方法（と、必要に応じて検証の方法）をサブクラスで実装する例です。

.. literalinclude:: ../examples/ch08_template_method.py
   :language: python
   :caption: ch08_template_method.py
   :start-at: class Importer
   :end-before: def main

:download:`ch08_template_method.py <../examples/ch08_template_method.py>`

テンプレートメソッドの ``run`` には、``typing.final`` を付けています。サブクラスで ``run`` を上書きすると mypy がエラーとして検出するので、手順そのものがサブクラスごとに変えられてしまうことを防げます。

Template Method パターンは継承を使うので、:doc:`oop` で説明した継承の問題を抱えます。異なる部分が少ない場合は、Strategy パターンのように、異なる部分を関数やオブジェクトとして渡す方法も検討します。

State パターン
--------------

**問題**: オブジェクトの状態によって、できる操作や操作の結果が変わります。状態ごとの分岐が、多くのメソッドに散らばっています。

**解決策**: 状態ごとにクラスを作り、その状態でできる操作を、そのクラスのメソッドとして実装します。オブジェクトは現在の状態を表すオブジェクトを持ち、操作をそれに任せます。

注文の状態（下書き → 確定 → 発送済み、または取り消し）を例にします。悪い例では、すべてのメソッドに状態の分岐があります。

.. literalinclude:: ../examples/ch08_state.py
   :language: python
   :caption: ch08_state.py（悪い例）
   :pyobject: BadOrder

State パターンでは、状態ごとのクラスに、その状態でできる操作だけを実装します。基底クラスの ``OrderState`` では、すべての操作がエラーになるようにしておきます。

.. literalinclude:: ../examples/ch08_state.py
   :language: python
   :caption: ch08_state.py（State パターン）
   :start-at: class OrderState
   :end-before: # ----

状態と操作の組み合わせが単純な場合は、状態遷移を表（辞書）で表すだけで十分なこともあります。表にすると、すべての状態遷移を一覧でき、状態遷移図との対応も確かめやすくなります。

.. literalinclude:: ../examples/ch08_state.py
   :language: python
   :caption: ch08_state.py（状態遷移表）
   :start-at: # (現在の状態, 操作)
   :end-before: def main

:download:`ch08_state.py <../examples/ch08_state.py>`

この状態遷移表を図にすると、次のようになります。

.. graphviz:: diagrams/patterns_states.dot

状態ごとに多くの振る舞いが異なる場合は State パターンを、状態の遷移だけを管理したい場合は状態遷移表を選ぶとよいでしょう。

Python の機能で代替できるパターン
---------------------------------

GoF のパターンの多くは、C++ や Smalltalk を前提に考えられました。Python には、関数を値として扱える、クラスそのものをオブジェクトとして扱える、といった機能があるので、パターンをより簡潔に実現できることがあります。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - パターン
     - Python での代替
   * - Strategy
     - 戦略を関数として渡します。
   * - Factory Method、Abstract Factory
     - クラスや、オブジェクトを作る関数を、引数や辞書で渡します。
   * - Command
     - 実行したい処理を関数（必要なら ``functools.partial`` で引数を固定したもの）として保持します。
   * - Iterator
     - ジェネレーター関数（``yield``）で実現します。
   * - Template Method
     - 異なる部分を関数として受け取る、高階関数にします。
   * - Singleton
     - モジュールの変数を使います（モジュールは一度だけ読み込まれます）。ただし、次の節で説明する理由から、そもそも避けることを検討します。

Singleton を避ける理由
~~~~~~~~~~~~~~~~~~~~~~

Singleton パターンは、あるクラスのインスタンスが 1 つしか作られないことを保証し、どこからでもそのインスタンスを取得できるようにするパターンです。設定やデータベースの接続などによく使われますが、次のような問題があります。

* どこからでも取得できるということは、実質的にグローバル変数です。:doc:`metrics` で説明した共通結合を生みます。
* テストのときに、別のオブジェクト（テスト用のデータベースなど）に差し替えるのが難しくなります。
* テストの間で状態が共有されるので、テストの実行の順序によって結果が変わることがあります。

インスタンスを 1 つだけにしたい場合でも、そのインスタンスはプログラムの起動時に一度だけ作り、必要な部品に引数として渡すほうが安全です。この方法は :doc:`dependency` で説明します。

まとめ
------

* デザインパターンは、よくある設計の問題と、その解決策に付けられた名前です。
* パターンを使うこと自体を目的にせず、解決したい問題があるときに使います。
* Python では、関数やクラスを値として扱えるので、パターンをより簡潔に実現できることがあります。
* Singleton は実質的にグローバル変数なので、避けることを検討します。
