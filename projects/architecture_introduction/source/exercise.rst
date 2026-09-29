総合演習
========

この章では、これまでの章で説明した考え方を 1 つのアプリケーションに適用します。題材は、小さな在庫管理の CLI（コマンドラインで使うツール）です。最初は思いつくままに書いた 1 本のスクリプトから始め、4 つの段階を経て改善していきます。各段階で、どの章の考え方を使ったのかを振り返ります。

題材: 在庫管理 CLI
------------------

倉庫の担当者が、商品の在庫数を管理するためのツールです。次の 4 つのコマンドを受け付けます。在庫のデータは、商品コードをキーとする JSON ファイル（``inventory.json``）に保存します。どの段階も同じ形式で保存するので、段階を切り替えても同じファイルを使い続けられます。保存形式に JSON ファイルを選んだ理由は、:doc:`documentation` の ADR の例に記録しています。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - コマンド
     - 動作
   * - ``register 商品コード 商品名``
     - 商品を登録します（在庫の数は 0 から始まります）。同じ商品コードは登録できません。
   * - ``receive 商品コード 数量``
     - 入庫します（在庫の数を増やします）。
   * - ``ship 商品コード 数量``
     - 出庫します（在庫の数を減らします）。在庫が足りない場合はエラーにします。
   * - ``list``
     - 在庫の一覧を表示します。在庫が 5 個を下回る商品には「（要発注）」と表示します。

どの段階のプログラムも、同じコマンドに対して同じように動きます（段階 4 だけは、入庫と出庫のあとに在庫の数も表示します）。実行の例は次のとおりです。

.. code-block:: console

   $ python inventory.py register A-1 ボールペン
   A-1 を登録しました
   $ python inventory.py receive A-1 10
   A-1 を 10 個入庫しました
   $ python inventory.py ship A-1 7
   A-1 を 7 個出庫しました
   $ python inventory.py list
   A-1 ボールペン: 3（要発注）

段階 1: 1 本のスクリプト
------------------------

最初のプログラムは、上から順に処理を書き下した 1 本のスクリプトです。

.. literalinclude:: ../examples/ch16_inventory/step1/inventory.py
   :language: python
   :caption: ch16_inventory/step1/inventory.py
   :start-at: import json

:download:`step1/inventory.py <../examples/ch16_inventory/step1/inventory.py>`

このスクリプトには、次のような問題があります。

* コマンドの解析、在庫の規則、保存、表示が混ざっていて、関心が分離されていません（:doc:`metrics`）。
* 「商品が登録されているか」「数量が正か」の確認が、コマンドごとに重複しています。
* 在庫の規則（出庫は在庫の数まで）を、コマンドの処理から切り離してテストできません。
* 数量に数字以外を指定すると、``int`` の ``ValueError`` でスクリプトが異常終了します。
* ``5`` という値の意味（発注する目安）が書かれていません。

flake8 で循環的複雑度を調べると、``if`` 文の塊の複雑度は 15 になります。

段階 2: 関数に分割する
----------------------

役割ごとに関数に分けます（:doc:`functions`）。

* 保存と読み込みを ``load_inventory`` と ``save_inventory`` に分けます。
* 在庫の操作を ``register``、``receive``、``ship`` に分け、重複していた確認の処理を ``_check_quantity`` にまとめます。
* エラーは独自の例外 ``InventoryError`` で表し、エラーの表示は ``main`` の 1 か所にまとめます。
* ``5`` を定数 ``REORDER_POINT`` にします。

.. literalinclude:: ../examples/ch16_inventory/step2/inventory.py
   :language: python
   :caption: ch16_inventory/step2/inventory.py（在庫の操作）
   :start-at: def register
   :end-before: def format_list

:download:`step2/inventory.py <../examples/ch16_inventory/step2/inventory.py>`

在庫の操作が関数になったので、辞書を渡して呼び出せば、ファイルを使わずにテストできるようになりました。しかし、在庫のデータは辞書のままなので、キーの綴りの誤りを型チェッカーで検出できず、``inventory[sku]["quantity"] -= quantity`` のように、規則を通さずに在庫の数を書き換えることもできます。

段階 3: データをクラスにする
----------------------------

辞書を、商品を表すデータクラス ``Item`` に置き換えます（:doc:`data`）。入庫と出庫は ``Item`` のメソッドにし、「数量は 1 以上」「出庫は在庫の数まで」という規則を ``Item`` の中で確かめます（:doc:`oop` の「尋ねるな、命じよ」）。また、コマンドの解析には、標準ライブラリの ``argparse`` を使います。数量が整数でない場合のエラーの表示も ``argparse`` に任せられます。

.. literalinclude:: ../examples/ch16_inventory/step3/inventory.py
   :language: python
   :caption: ch16_inventory/step3/inventory.py（商品のクラス）
   :pyobject: Item

:download:`step3/inventory.py <../examples/ch16_inventory/step3/inventory.py>`

``Item`` のメソッドは、ファイルにも画面にも依存しないので、単体でテストできます。しかし、``main`` 関数には、まだコマンドの解析、ファイルの読み書き、ユースケースの手順、表示が混ざっています。保存先をファイルから別のものに変えたり、``main`` の処理をテストしたりするのは困難です。

段階 4: レイヤーに分け、依存性注入とテストを加える
--------------------------------------------------

最後の段階では、プログラムをパッケージにし、役割ごとのモジュールに分けます。構成は、:doc:`architecture` のヘキサゴナルアーキテクチャに沿っています。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - モジュール
     - 役割
   * - ``domain.py``
     - 商品と在庫の規則（``Item``、``InventoryError``）と、商品の保存のインターフェース ``ItemRepository``。ほかのモジュールに依存しません。
   * - ``repository.py``
     - ``ItemRepository`` の実装（JSON ファイル版とメモリ版）。
   * - ``service.py``
     - ユースケース（登録、入庫、出庫、一覧）を実装する ``InventoryService``。リポジトリのインターフェースだけに依存します。
   * - ``cli.py``
     - コマンドライン引数の解析と、結果の表示。出力先を引数で受け取ります。
   * - ``main.py``
     - オブジェクトの組み立て（コンポジションルート）。
   * - ``test_service.py``
     - ドメイン、サービス、リポジトリ、CLI のテスト。

.. graphviz:: diagrams/exercise_step4.dot

``InventoryService`` は、リポジトリのインターフェースだけに依存します（:doc:`solid` の依存性逆転の原則）。

.. literalinclude:: ../examples/ch16_inventory/step4/service.py
   :language: python
   :caption: ch16_inventory/step4/service.py
   :pyobject: InventoryService

どのリポジトリを使うかは、コンポジションルートの ``main.py`` だけが知っています（:doc:`dependency`）。

.. literalinclude:: ../examples/ch16_inventory/step4/main.py
   :language: python
   :caption: ch16_inventory/step4/main.py
   :pyobject: main

``cli.py`` の ``execute`` は、表示の出力先 ``out`` を引数で受け取ります。本番では ``sys.stdout`` を、テストでは ``io.StringIO`` を渡すことで、表示の内容もテストで確かめられます。

.. literalinclude:: ../examples/ch16_inventory/step4/test_service.py
   :language: python
   :caption: ch16_inventory/step4/test_service.py（CLI のテスト）
   :pyobject: CliTest

段階 4 のプログラムとテストは、``examples`` フォルダーで次のように実行します。段階 1 から 3 とは異なり、``--file`` オプションで保存先のファイルを指定できます。

.. code-block:: console

   $ python -m ch16_inventory.step4.main register A-1 ボールペン
   $ python -m ch16_inventory.step4.main list
   $ python -m ch16_inventory.step4.main --file stock.json register B-1 ノート
   $ python -m ch16_inventory.step4.main --file stock.json list
   $ python -m unittest ch16_inventory.step4.test_service -v

段階 1 から 4 のすべてのファイルは、:doc:`samples/ch16` で閲覧できます。

振り返り
--------

各段階で適用した考え方と、その効果をまとめます。

.. list-table::
   :header-rows: 1
   :widths: 15 45 40

   * - 段階
     - 適用した考え方
     - 効果
   * - 2
     - 関数への分割、重複の除去、独自の例外、マジックナンバーの定数化（:doc:`functions`、:doc:`refactoring`）
     - 在庫の操作を、ファイルを使わずに呼び出せるようになりました。エラーの表示が 1 か所にまとまりました。
   * - 3
     - データクラス、「尋ねるな、命じよ」（:doc:`data`、:doc:`oop`）
     - 在庫の規則が ``Item`` のメソッドに集まり、在庫を操作するコードは、規則を確かめるメソッドを通すようになりました。
   * - 4
     - 関心の分離、依存性逆転の原則、依存性注入、ヘキサゴナルアーキテクチャ（:doc:`solid`、:doc:`dependency`、:doc:`architecture`）
     - ユースケースと CLI を、ファイルを使わずにテストできるようになりました。保存先の変更は、リポジトリの追加と ``main.py`` の変更だけで済みます。

段階 4 は、段階 1 よりもファイルの数もコードの量も増えています。:doc:`what_is_design` で説明したとおり、どの段階が適切かは、プログラムの寿命と変更の頻度によって決まります。一度きりの作業であれば段階 1 で十分です。チームで長く使い、機能を追加していくのであれば、段階 4 の構成が変更の費用を抑えます。実際の開発では、最初から段階 4 を目指すのではなく、変更の必要が生じたときに、リファクタリングによって段階を進めていくのが現実的です。

発展課題
--------

次の課題に取り組んで、段階 4 の設計の変更しやすさを確かめてください。

1. SQLite に保存するリポジトリ ``SqliteItemRepository`` を追加し、``--db`` オプションで切り替えられるようにしてください。``InventoryService`` を変更する必要がないことを確かめてください（ヒント: :doc:`domain` の ``SqliteOrderRepository``）。
2. 入庫と出庫の履歴を記録し、``history 商品コード`` コマンドで表示できるようにしてください。履歴をどのモジュールに持たせるのが適切かを考えてください。
3. 在庫が発注の目安を下回ったときに、担当者に通知する機能を追加してください。``InventoryService`` が通知の方法（メールやチャット）を知らずに済むようにしてください（ヒント: :doc:`patterns` の Observer パターン、:doc:`solid` の依存性逆転の原則）。
4. 追加した機能のテストを書いてください。
