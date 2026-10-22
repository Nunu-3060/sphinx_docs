==========================================
道具に頼る
==========================================

ここまでの章で、良いコードを書くための方法を説明してきた。しかし、すべてを人間が気を付けて守り続けるのは難しい。見落としは必ず起きる。この章では、コードの品質を保つために役立つ道具を紹介する。

道具の全体像
==========================================

この章で紹介する道具と、その役割を次に示す。

.. list-table:: コードの品質を保つための道具
   :header-rows: 1
   :widths: 25 25 50

   * - 種類
     - 道具の例
     - 役割
   * - テスト
     - pytest
     - 関数などが期待どおりに動くことを確かめる。
   * - :term:`リンター`
     - flake8
     - PEP 8 違反や、使っていない変数などの問題を見つける。
   * - :term:`静的型チェッカー`
     - mypy
     - 型ヒントを手がかりに、型の誤りを実行前に見つける。
   * - :term:`フォーマッター`
     - Black、Ruff
     - コードの見た目を自動で整える。
   * - :term:`バージョン管理システム`
     - Git
     - コードの変更の履歴を記録する。

これらの道具を、例えば :numref:`fig-tool-workflow` のような流れで使う。

.. graphviz::
   :caption: 道具を使う流れの例
   :alt: コードを書き、フォーマッターで整え、リンターと静的型チェッカーで検査し、テストを実行し、問題が無ければバージョン管理システムに記録する流れを示す図
   :name: fig-tool-workflow

   digraph workflow {
       graph [rankdir=LR, fontname="Yu Gothic", nodesep=0.3, ranksep=0.35];
       node [shape=box, style="rounded,filled", fillcolor="#e8f0fe", color="#1f77b4", fontname="Yu Gothic", fontsize=11];
       edge [color="#555555", fontname="Yu Gothic", fontsize=10];

       write [label="コードを書く", fillcolor="#fff3cd", color="#b8860b"];
       format [label="整える\n（フォーマッター）"];
       lint [label="検査する\n（リンター）"];
       typecheck [label="型を検査する\n（静的型チェッカー）"];
       test [label="テストする\n（pytest）"];
       commit [label="記録する\n（Git）", fillcolor="#d4edda", color="#2e7d32"];

       write -> format -> lint -> typecheck -> test -> commit;
       test -> write [label="問題があれば直す", style=dashed, constraint=false];
   }

本書で紹介する道具は、次のコマンドでインストールできる（Black と Ruff、Git は除く）。

.. code-block:: console

   python -m pip install pytest flake8 mypy

テストを書く
==========================================

関数が期待どおりに動くことを確かめるコードを :term:`テスト` と呼ぶ。テストがあれば、コードを変更した後にテストを実行するだけで、変更によって既存の動作が壊れていないかを確かめられる。

次のファイルは、平均を求める関数 ``average`` と、そのテストである。

.. literalinclude:: ../examples/ch11_tools_test.py
   :language: python
   :linenos:
   :caption: ch11_tools_test.py

:download:`ch11_tools_test.py をダウンロードする <../examples/ch11_tools_test.py>`

``test_`` で始まる関数がテストである。``assert`` 文は、続く式が ``True`` でなければ ``AssertionError`` を送出する。``test_average_of_empty_list_raises_error`` は、空のリストを渡したときに ``ValueError`` が送出されることを確かめている。

テストは、pytest というテスト用のライブラリを使って実行するのが一般的である。pytest は、``test_`` で始まる関数を自動で探して実行し、結果をまとめて表示する。

.. code-block:: console

   python -m pytest ch11_tools_test.py

すべてのテストに合格すると、次のように表示される（かかった時間は環境によって異なる）。

.. code-block:: text
   :linenos:

   ...                                                                      [100%]
   3 passed in 0.05s

このファイルは、pytest が無くても ``python ch11_tools_test.py`` で実行できるようにしている。

なお、pytest には、例外が送出されることを確かめるための ``pytest.raises`` という仕組みがあり、``test_average_of_empty_list_raises_error`` はもっと簡潔に書ける。本書では、pytest が無い環境でも動くように、標準の機能だけで書いている。

テストがあると、安心してコードを改善できる。動作を変えずにコードの書き方を改善することを :term:`リファクタリング` と呼ぶ。テストが無い状態でリファクタリングを行うと、うっかり動作を変えてしまっても気付けない。第 6 章で、関数を小さく分けるとテストしやすくなると説明したのは、このためである。

リンターで問題を見つける
==========================================

コードを解析して、問題のある書き方を見つける道具を :term:`リンター` と呼ぶ。Python では flake8 がよく使われている。flake8 は、PEP 8 に違反している箇所や、定義したのに使っていない変数、``import`` したのに使っていないモジュールなどを見つける。

第 4 章の悪い例を ``layout_bad.py`` という名前で保存し、flake8 で検査すると、次のように表示される。

.. code-block:: console

   python -m flake8 layout_bad.py

.. code-block:: text
   :linenos:

   layout_bad.py:1:18: E401 multiple imports on one line
   layout_bad.py:1:18: E231 missing whitespace after ','
   layout_bad.py:2:1: E302 expected 2 blank lines, found 0
   layout_bad.py:2:17: E201 whitespace after '('
   layout_bad.py:2:24: E202 whitespace before ')'
   layout_bad.py:4:1: E302 expected 2 blank lines, found 0
   layout_bad.py:5:3: E111 indentation is not a multiple of 4
   layout_bad.py:5:10: E225 missing whitespace around operator
   layout_bad.py:6:3: E111 indentation is not a multiple of 4
   layout_bad.py:6:17: E201 whitespace after '('
   layout_bad.py:6:24: E202 whitespace before ')'
   layout_bad.py:7:3: E111 indentation is not a multiple of 4

各行は「ファイル名:行番号:列番号: コード メッセージ」の形式である。例えば 1 行目は、``layout_bad.py`` の 1 行目の 18 文字目で、「1 行に複数の ``import`` がある（E401）」という問題が見つかったことを表す。

静的型チェッカーで型の誤りを見つける
==========================================

プログラムを実行せずに、型ヒントを手がかりにして型の誤りを見つける道具を :term:`静的型チェッカー` と呼ぶ。Python では mypy がよく使われている。

次のコードは、整数を受け取る関数 ``add_tax`` に、文字列 ``"1000"`` を渡している。

.. code-block:: python
   :linenos:
   :caption: type_error.py

   def add_tax(price: int) -> int:
       return price * 110 // 100


   print(add_tax("1000"))

このコードを実行すると、``price * 110`` の部分はエラーにならず、``"1000"`` を 110 回繰り返した長い文字列が作られる。その文字列を ``100`` で割ろうとした時点で、ようやく ``TypeError`` が発生する。このように、型の誤りは、誤りの原因から離れた場所でエラーになることがある。mypy を使うと、実行する前に次のように誤りを見つけられる。

.. code-block:: console

   python -m mypy type_error.py

.. code-block:: text
   :linenos:

   type_error.py:5: error: Argument 1 to "add_tax" has incompatible type "str"; expected "int"  [arg-type]
   Found 1 error in 1 file (checked 1 source file)

設定ファイルを用意する
==========================================

flake8 と mypy の設定は、``setup.cfg`` というファイルに書ける。本書のサンプルコードでは、次の設定ファイルをサンプルコードと同じフォルダに置いている。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
   :caption: setup.cfg

:download:`setup.cfg をダウンロードする <../examples/setup.cfg>`

* 1 行目と 2 行目は flake8 の設定で、1 行の長さの上限を 120 文字にしている。
* 4 行目と 5 行目は mypy の設定である。``strict = True`` を指定すると、多くの検査が有効になる。例えば、型ヒントが書かれていない関数もエラーとして報告されるようになる。

flake8 と mypy は、コマンドを実行したフォルダにある ``setup.cfg`` を読み込む。サンプルコードのフォルダで次のコマンドを実行すると、すべてのファイルをまとめて検査できる。

.. code-block:: console

   python -m flake8 .

.. code-block:: console

   python -m mypy .

フォーマッターで見た目を整える
==========================================

コードの見た目を自動で整える道具を :term:`フォーマッター` と呼ぶ。Python では Black や Ruff がよく使われている。フォーマッターを使うと、インデントや空白、改行の位置などが決まった形にそろえられる。

チーム全員が同じフォーマッターを使えば、見た目について議論したり、手で直したりする必要がなくなる。その分、名前の付け方や関数の分け方など、道具では判断できない部分に集中できる。

なお、Ruff はフォーマッターとしての機能だけでなく、flake8 と同様のリンターとしての機能も持っている。

バージョン管理システムで履歴を残す
==========================================

コードの変更の履歴を記録する道具を :term:`バージョン管理システム` と呼ぶ。現在は Git が広く使われている。

バージョン管理システムを使うと、いつ、誰が、何を、なぜ変更したのかを記録できる。間違えて変更したときは、以前の状態に戻すことも、昔のコードを取り出すこともできる。第 5 章で、使わなくなったコードをコメントにして残す必要は無いと説明したのは、このためである。

道具の限界を知る
==========================================

道具は、決まった規則に従っているかどうかを確かめるのは得意だが、コードの意味までは理解できない。例えば、変数名が ``d`` であっても、規則に違反していなければリンターは何も報告しない。テストも、書かれていない場合については何も確かめない。

道具で確かめられることは道具に任せ、名前の付け方や関数の分け方など、人間にしか判断できないことに注意を向けるとよい。

まとめ
==========================================

* テストを書けば、変更によって動作が壊れていないかをすぐに確かめられる。テストがあると、安心してリファクタリングできる。
* リンター（flake8 など）で、PEP 8 違反などの問題を見つける。
* 静的型チェッカー（mypy など）で、型の誤りを実行前に見つける。
* フォーマッター（Black、Ruff など）で、見た目を自動で整える。
* バージョン管理システム（Git など）で、変更の履歴を残す。
* 道具で確かめられることは道具に任せ、人間は人間にしか判断できないことに集中する。
