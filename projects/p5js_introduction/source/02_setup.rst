環境構築
========

p5.js のスケッチを動かす方法は、大きく分けて次の 2 つです。

.. list-table::
   :header-rows: 1
   :widths: 25 40 35

   * - 方法
     - 特徴
     - 向いている場面
   * - p5.js Web Editor
     - ブラウザーだけで編集と実行ができる。インストールは不要。
     - 手軽に試したいとき、作品を共有したいとき
   * - ローカル環境
     - 手元のエディターでファイルを編集し、ブラウザーで開く。
     - 複数のファイルを扱うとき、普段の開発環境で書きたいとき

まずは Web Editor で動かしてみて、慣れてきたらローカル環境に移るのがおすすめです。

p5.js Web Editor
----------------

`p5.js Web Editor <https://editor.p5js.org/>`__ は、p5.js の公式のオンラインエディターです。開くと、次のようなコードがすでに入力されています。

.. code-block:: javascript
   :linenos:

   function setup() {
     createCanvas(400, 400);
   }

   function draw() {
     background(220);
   }

画面上部の再生ボタン（▶）を押すと、右側のプレビューに灰色の正方形が表示されます。これが :term:`キャンバス` です。コードを書き換えて再生ボタンを押すと、結果が更新されます。

アカウントを登録すると、スケッチを保存したり、URL で他の人と共有したりできます。

ローカル環境
------------

ローカル環境では、次の 2 つのファイルを 1 つのフォルダーに置きます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - ファイル
     - 役割
   * - ``index.html``
     - ブラウザーが最初に開くファイル。p5.js 本体とスケッチを読み込む。
   * - ``sketch.js``
     - スケッチ本体。p5.js の関数を使って描画の処理を書く。

``index.html`` の内容は次のとおりです。本書のサンプルは、すべてこの形をしています。

.. literalinclude:: ../examples/ch02_hello/index.html
   :language: html
   :linenos:
   :caption: ch02_hello/index.html

8 行目で p5.js 本体を :term:`CDN` から読み込み、15 行目でスケッチ本体の ``sketch.js`` を読み込んでいます。``sketch.js`` は p5.js が提供する関数を使うため、必ず p5.js より後に読み込みます。

URL の ``p5@2.3.4`` の部分はバージョンの指定です。バージョンを固定しておくと、p5.js が更新されてもスケッチの動作が変わりません。

``sketch.js`` には、マウスに付いてくる円を描くコードを書きます。

.. literalinclude:: ../examples/ch02_hello/sketch.js
   :language: javascript
   :linenos:
   :caption: ch02_hello/sketch.js

* `実行する <examples/ch02_hello/index.html>`__
* ダウンロード：:download:`index.html <../examples/ch02_hello/index.html>`、:download:`sketch.js <../examples/ch02_hello/sketch.js>`

``index.html`` をダブルクリックしてブラウザーで開き、キャンバスの上でマウスを動かすと、円が付いてきます。コードの意味は :doc:`04_structure` で詳しく説明します。

エディターは何を使ってもかまいません。Visual Studio Code などの、JavaScript の入力補完や構文の色分けに対応したエディターを使うと便利です。

ローカルサーバー
----------------

``index.html`` をダブルクリックして開くと、ブラウザーのアドレス欄は ``file://`` で始まります。この状態では、ブラウザーのセキュリティ制限により、JSON などの外部ファイルを読み込めません。:doc:`12_media` のように外部ファイルを使うスケッチは、:term:`ローカルサーバー` を経由して開く必要があります。

Python がインストールされていれば、標準ライブラリの ``http.server`` モジュールでローカルサーバーを起動できます。サンプルのフォルダーで次のコマンドを実行します。

.. code-block:: console
   :linenos:

   python -m http.server 8000

ブラウザーで ``http://localhost:8000/`` を開くと、フォルダーの中身が一覧表示されます。終了するには、コマンドを実行した端末で :kbd:`Ctrl+C` を押します。

本書のサンプルには、同じことをするスクリプト ``serve.py`` も含めています。``serve.py`` は、起動と同時にブラウザーを開き、JavaScript ファイルを正しい MIME タイプで返します。Windows では、レジストリの設定によって ``.js`` ファイルが ``text/plain`` として返され、スクリプトが動かない場合があるため、その対策を入れています。

.. literalinclude:: ../examples/serve.py
   :language: python
   :linenos:
   :caption: serve.py

* ダウンロード：:download:`serve.py <../examples/serve.py>`

``serve.py`` を置いたフォルダーで次のように実行します。

.. code-block:: console
   :linenos:

   python serve.py
   python serve.py --port 8080

開発者ツール
------------

スケッチが思ったとおりに動かないときは、ブラウザーの :term:`開発者ツール` を開きます。Chrome や Edge では :kbd:`F12` キー、macOS では :kbd:`Command+Option+I` キーで開けます。

開発者ツールの「コンソール」タブには、次の内容が表示されます。

* JavaScript のエラー（エラーが起きたファイル名と行番号を含む）
* ``console.log()`` で出力した値

``console.log()`` は Python の ``print()`` に相当し、変数の値を確認するのに使います。

.. code-block:: javascript
   :linenos:

   console.log('x の値:', x);

p5.js には、よくある間違いを分かりやすいメッセージで教えてくれる :term:`Friendly Error System`\ （FES）があります。ただし、FES は圧縮版の ``p5.min.js`` では無効になっています。学習中にエラーの原因が分からないときは、``index.html`` の読み込み先を圧縮していない ``p5.js`` に変えると、詳しいメッセージが表示されます。

.. code-block:: html
   :linenos:

   <script src="https://cdn.jsdelivr.net/npm/p5@2.3.4/lib/p5.js"></script>
