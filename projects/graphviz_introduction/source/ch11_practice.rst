実践例
======

この章では、これまでに説明した機能を組み合わせて、実務でよく使う図を描きます。前半では DOT を手で書く例を、後半では Python でソースコードやフォルダーから図を自動生成する例を紹介します。

状態遷移図
----------

注文の状態が、どの操作でどの状態に移るかを表す状態遷移図です。状態を角の丸い箱で、開始と終了を黒丸で表しています。

.. literalinclude:: ../examples/dot/ch11_state_machine.dot
   :language: dot
   :caption: examples/dot/ch11_state_machine.dot

.. graphviz:: ../examples/dot/ch11_state_machine.dot
   :align: center

ポイントは次のとおりです。

* ``rankdir=LR`` で、状態が左から右へ進むように配置しています。
* ノードの ID は英語の短い名前にし、表示する日本語は ``label`` で指定しています。ID を英語にしておくと、プログラムの状態の名前と対応させやすくなります。
* 開始は ``shape=point``、終了は塗りつぶした ``shape=doublecircle`` で表しています。

フローチャート
--------------

ログイン処理の流れを表すフローチャートです。処理を箱で、分岐をひし形で、入力を平行四辺形で表しています。

.. literalinclude:: ../examples/dot/ch11_flowchart.dot
   :language: dot
   :caption: examples/dot/ch11_flowchart.dot

.. graphviz:: ../examples/dot/ch11_flowchart.dot
   :align: center

フローチャートでは、ノードの形で役割を区別するのが一般的です。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 形
     - 役割
   * - ``oval``
     - 開始、終了。
   * - ``box``
     - 処理。
   * - ``diamond``
     - 分岐。
   * - ``parallelogram``
     - 入力、出力。

分岐から出る「はい」と「いいえ」のエッジが左右のどちらに描かれるかは、dot が交差の少なさなどから決めます。位置を揃えたい場合は、7 章のポートを使って ``check:s -> home`` や ``check:e -> count`` のように、エッジを出す位置を指定します。

ER 図
-----

データベースのテーブルの関係を表す ER 図です。HTML 風ラベルでテーブルを表し、ポートを使って、外部キーの列と参照先の主キーの列を結んでいます。主キーの列には下線を引いています。

.. literalinclude:: ../examples/dot/ch11_er.dot
   :language: dot
   :caption: examples/dot/ch11_er.dot

.. graphviz:: ../examples/dot/ch11_er.dot
   :align: center

エッジの両端の記号で、テーブルの間の「1 対多」の関係を表しています。「1」の側には ``tee``\ （縦線）、「多」の側には ``crow``\ （鳥の足のような形）を使います。これは、ER 図でよく使われる IE 記法（鳥の足記法）にならったものです。``dir=both`` を指定して、エッジの両側に記号を表示しています。

クラス図
--------

クラスの継承と集約の関係を表すクラス図です。record シェイプで、クラス名、属性、メソッドを 3 段に分けて表しています。

.. literalinclude:: ../examples/dot/ch11_class.dot
   :language: dot
   :caption: examples/dot/ch11_class.dot

.. graphviz:: ../examples/dot/ch11_class.dot
   :align: center

ポイントは次のとおりです。

* 継承は、子クラスから親クラスへ、白抜きの三角（``arrowhead=empty``）のエッジで表します。
* 集約は、全体の側に白抜きのひし形（``odiamond``）を付けたエッジで表します。ひし形を始点側に付けるため、``dir=back`` と ``arrowtail`` を組み合わせています。
* 集約のエッジに ``constraint=false`` を指定し、継承の関係による上下の配置を崩さないようにしています。
* record シェイプでは ``>`` が特別な意味を持つため、``->`` を表示するために ``-\>`` と書いています。

import の依存関係図
-------------------

ここからは、Python で図を自動生成する例です。次のサンプルは、Python のパッケージの中の各モジュールを解析し、パッケージ内のどのモジュールがどのモジュールを import しているかを図にします。

解析の対象には、サンプルの ``examples/py/sample_app`` パッケージを使います。これは、タスクを管理する小さなアプリケーションで、次の 4 つのモジュールからなります。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - モジュール
     - 内容
   * - ``models``
     - タスクを表すデータクラス。
   * - ``storage``
     - タスクを保存するクラス。
   * - ``services``
     - タスクの追加や検索などの処理。
   * - ``main``
     - アプリケーションの入口。

.. literalinclude:: ../examples/py/ch11_import_graph.py
   :language: python
   :caption: examples/py/ch11_import_graph.py

``examples/py`` フォルダーで ``python ch11_import_graph.py`` を実行すると、次の図が出力されます。

.. graphviz:: ../build/generated/ch11_import_graph.gv
   :align: center

``ast`` モジュールは Python の標準ライブラリで、ソースコードを構文木に変換します。``ast.walk()`` で構文木のすべての要素をたどり、``ast.Import``\ （``import x`` の文）と ``ast.ImportFrom``\ （``from x import y`` の文）を探しています。モジュールを実際に import するわけではないので、解析の対象のコードが実行されることはありません。

引数に別のパッケージのフォルダーを指定すると、そのパッケージの依存関係図を出力できます。モジュールの数が多い場合は、``rankdir`` を既定の ``TB`` に戻したり、9 章の sfdp を試したりしてください。

フォルダーのツリー図
--------------------

次のサンプルは、フォルダーの中のフォルダーとファイルを再帰的にたどり、ツリー図にします。

.. literalinclude:: ../examples/py/ch11_directory_tree.py
   :language: python
   :caption: examples/py/ch11_directory_tree.py

``examples/py`` フォルダーで ``python ch11_directory_tree.py`` を実行すると、``examples/py`` フォルダー自身のツリー図が出力されます。

.. graphviz:: ../build/generated/ch11_directory_tree.gv
   :align: center

ノードの ID には、対象のフォルダーからの相対パスを使っています。ファイル名だけを ID にすると、別のフォルダーにある同じ名前のファイル（たとえば複数の ``__init__.py``）が、1 つのノードにまとめられてしまうためです。ID とラベルを分けて、ID で区別し、ラベルで短い名前を表示する、という考え方は、プログラムでグラフを生成する際の基本です。
