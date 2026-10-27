付録 A p5.js 1.x と 2.x の違い
==============================

p5.js は 2025 年にバージョン 2.0 が公開されました。Web 上の記事やサンプルには 1.x 系を前提としたものがまだ多く、そのままでは 2.x で動かないことがあります。ここでは、入門の範囲で影響の大きい違いをまとめます。

主な違い
--------

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - 1.x
     - 2.x
   * - ファイルの読み込み
     - ``preload()`` の中で ``loadImage()`` などを呼ぶ。
     - ``preload()`` は廃止。``async function setup()`` の中で ``await loadImage()`` のように呼ぶ。
   * - 読み込み関数の戻り値
     - 読み込み途中のオブジェクトを返し、完了すると中身が埋まる。
     - :term:`Promise` を返す。
   * - 曲線の頂点
     - ``curveVertex()``
     - ``splineVertex()`` に名前が変わった。
   * - ベジェ曲線の頂点
     - ``bezierVertex()`` に制御点 2 つと終点を一度に渡す。
     - ``bezierVertex()`` に 1 回につき 1 点ずつ渡す。
   * - ``mouseButton``
     - ``LEFT`` などの定数（文字列）が入る。
     - ``mouseButton.left`` のように、ボタンごとの真偽値を持つオブジェクトになった。
   * - 矢印キーなどの定数
     - ``LEFT_ARROW`` などは数値のキーコード。
     - ``LEFT_ARROW`` などは ``'ArrowLeft'`` のような文字列。
   * - データ操作の補助関数
     - ``createStringDict()``、``append()`` などがある。
     - 削除された。JavaScript 標準の配列やオブジェクトを使う。

preload() からの書き換え
------------------------

1.x の書き方を 2.x の書き方に変える例を示します。まず 1.x の書き方です。

.. code-block:: javascript
   :linenos:

   // p5.js 1.x の書き方（2.x では動かない）
   let img;

   function preload() {
     img = loadImage('image.png');
   }

   function setup() {
     createCanvas(400, 400);
   }

同じ処理を 2.x では次のように書きます。

.. code-block:: javascript
   :linenos:

   // p5.js 2.x の書き方
   let img;

   async function setup() {
     createCanvas(400, 400);
     img = await loadImage('image.png');
   }

``preload()`` の中身を ``setup()`` に移し、``setup()`` に ``async`` を、読み込み関数の呼び出しに ``await`` を付けます。

1.x のコードを動かしたいとき
----------------------------

1.x 向けのコードをそのまま動かしたい場合は、次のどちらかの方法をとります。

* ``index.html`` で読み込む p5.js のバージョンを 1.x 系（たとえば ``p5@1.11.13``）にする。
* 公式の互換性アドオン（`p5.js-compatibility <https://github.com/processing/p5.js-compatibility>`__）を読み込み、2.x で廃止された機能を補う。

これから新しく書くスケッチでは、2.x の書き方を使うことをおすすめします。
