付録
====

A. HTML 要素一覧
----------------

本資料で扱った主な HTML の要素を示す。

.. list-table:: 主な HTML の要素
   :header-rows: 1
   :widths: 25 20 55

   * - 要素
     - 種類
     - 意味
   * - ``html``
     - 文書
     - 文書全体を囲むルート要素。
   * - ``head``
     - 文書
     - メタ情報を書く部分。
   * - ``body``
     - 文書
     - 本体として表示される部分。
   * - ``title``
     - メタ情報
     - ページのタイトル。
   * - ``meta``
     - メタ情報
     - 文字コードや viewport などの情報。
   * - ``link``
     - メタ情報
     - 外部ファイル（主に CSS）の読み込み。
   * - ``script``
     - スクリプト
     - JavaScript の読み込みと実行。
   * - ``style``
     - スタイル
     - CSS の記述。
   * - ``h1`` ～ ``h6``
     - テキスト
     - 見出し。
   * - ``p``
     - テキスト
     - 段落。
   * - ``strong`` ／ ``em``
     - テキスト
     - 重要な内容／強調。
   * - ``br``
     - テキスト
     - 改行。
   * - ``pre`` ／ ``code``
     - テキスト
     - 整形済みテキスト／コードの断片。
   * - ``a``
     - リンク
     - リンク。
   * - ``img``
     - 埋め込み
     - 画像。
   * - ``ul`` ／ ``ol`` ／ ``li``
     - リスト
     - 順序なしリスト／順序付きリスト／リストの項目。
   * - ``table`` ／ ``tr`` ／ ``th`` ／ ``td``
     - 表
     - 表／行／見出しのセル／データのセル。
   * - ``thead`` ／ ``tbody`` ／ ``caption``
     - 表
     - 見出し部分／本体部分／表の題名。
   * - ``div`` ／ ``span``
     - 汎用
     - 意味を持たないブロック要素／インライン要素。
   * - ``header`` ／ ``footer``
     - セマンティック
     - ヘッダー／フッター。
   * - ``nav``
     - セマンティック
     - 主要なナビゲーション。
   * - ``main``
     - セマンティック
     - ページの主要な内容。
   * - ``article`` ／ ``section`` ／ ``aside``
     - セマンティック
     - 完結した内容／見出しを持つまとまり／補足的な内容。
   * - ``form``
     - フォーム
     - フォーム全体。
   * - ``input`` ／ ``textarea``
     - フォーム
     - 1 行の入力欄／複数行の入力欄。
   * - ``select`` ／ ``option``
     - フォーム
     - ドロップダウンリスト／その選択肢。
   * - ``button``
     - フォーム
     - ボタン。
   * - ``label``
     - フォーム
     - 入力欄の説明。
   * - ``fieldset`` ／ ``legend``
     - フォーム
     - 入力欄のまとまり／その題名。

B. よく使う CSS プロパティ一覧
------------------------------

.. list-table:: よく使う CSS のプロパティ
   :header-rows: 1
   :widths: 30 20 50

   * - プロパティ
     - 分類
     - 意味
   * - ``color``
     - 色
     - 文字の色。
   * - ``background-color``
     - 色
     - 背景色。
   * - ``font-family``
     - 文字
     - フォントの種類。
   * - ``font-size``
     - 文字
     - 文字の大きさ。
   * - ``font-weight``
     - 文字
     - 文字の太さ。
   * - ``line-height``
     - 文字
     - 行の高さ。
   * - ``text-align``
     - 文字
     - 行内での文字の揃え方。
   * - ``text-decoration``
     - 文字
     - 下線や取り消し線。
   * - ``width`` ／ ``height``
     - ボックス
     - 幅／高さ。
   * - ``max-width``
     - ボックス
     - 最大の幅。
   * - ``padding``
     - ボックス
     - 内側の余白。
   * - ``border``
     - ボックス
     - 枠線。
   * - ``border-radius``
     - ボックス
     - 角の丸み。
   * - ``margin``
     - ボックス
     - 外側の余白。``margin: 0 auto;`` で、幅を指定したブロック要素を左右中央に配置できる。
   * - ``box-sizing``
     - ボックス
     - ``width`` が表す範囲。
   * - ``box-shadow``
     - ボックス
     - 影。
   * - ``display``
     - レイアウト
     - 配置の方法（``block``、``inline``、``flex``、``grid``、``none`` など）。
   * - ``position``
     - レイアウト
     - 通常の配置から移動させる方法。
   * - ``flex-direction``
     - Flexbox
     - 主軸の方向。
   * - ``justify-content``
     - Flexbox
     - 主軸方向の配置。
   * - ``align-items``
     - Flexbox
     - 交差軸方向の配置。
   * - ``flex-grow``
     - Flexbox
     - 余った幅を分け合う比率。
   * - ``gap``
     - Flexbox ／ Grid
     - アイテムどうしの間隔。
   * - ``grid-template-columns``
     - Grid
     - 列の幅。
   * - ``grid-template-areas``
     - Grid
     - 名前を付けた領域の配置。
   * - ``opacity``
     - 効果
     - 不透明度。
   * - ``transform``
     - 効果
     - 移動・回転・拡大縮小。
   * - ``transition``
     - 効果
     - 値の変化を滑らかにする。
   * - ``animation``
     - 効果
     - キーフレームによるアニメーション。
   * - ``cursor``
     - その他
     - マウスカーソルの形。

C. Python と JavaScript の文法対応表
------------------------------------

.. list-table:: Python と JavaScript の文法の対応
   :header-rows: 1
   :widths: 25 35 40

   * - 項目
     - Python
     - JavaScript
   * - 出力
     - ``print(x)``
     - ``console.log(x)``
   * - 変数
     - ``x = 1``
     - ``const x = 1;`` ／ ``let x = 1;``
   * - 真偽値
     - ``True`` ／ ``False``
     - ``true`` ／ ``false``
   * - 値が無いこと
     - ``None``
     - ``null`` ／ ``undefined``
   * - 等価の比較
     - ``a == b``
     - ``a === b``
   * - 論理演算
     - ``and`` ／ ``or`` ／ ``not``
     - ``&&`` ／ ``||`` ／ ``!``
   * - 整数除算
     - ``7 // 2``
     - ``Math.floor(7 / 2)``
   * - 条件分岐
     - ``if a:`` ／ ``elif b:`` ／ ``else:``
     - ``if (a) {}`` ／ ``else if (b) {}`` ／ ``else {}``
   * - 条件式
     - ``x if c else y``
     - ``c ? x : y``
   * - 回数を指定したループ
     - ``for i in range(3):``
     - ``for (let i = 0; i < 3; i++) {}``
   * - 要素のループ
     - ``for x in items:``
     - ``for (const x of items) {}``
   * - 関数
     - ``def f(a, b=1):``
     - ``function f(a, b = 1) {}``
   * - 無名関数
     - ``lambda x: x * 2``
     - ``(x) => x * 2``
   * - 文字列への埋め込み
     - ``f"Hello {name}"``
     - ```Hello ${name}```
   * - リスト／配列
     - ``[1, 2, 3]``
     - ``[1, 2, 3]``
   * - 長さ
     - ``len(items)``
     - ``items.length``
   * - 末尾に追加
     - ``items.append(x)``
     - ``items.push(x)``
   * - 変換
     - ``[x * 2 for x in items]``
     - ``items.map((x) => x * 2)``
   * - 絞り込み
     - ``[x for x in items if x > 0]``
     - ``items.filter((x) => x > 0)``
   * - 辞書／オブジェクト
     - ``{"name": "山田"}``
     - ``{ name: "山田" }``
   * - キーと値の組
     - ``d.items()``
     - ``Object.entries(d)``
   * - JSON への変換
     - ``json.dumps(d)``
     - ``JSON.stringify(d)``
   * - JSON からの変換
     - ``json.loads(s)``
     - ``JSON.parse(s)``
   * - クラス
     - ``class Dog(Animal):``
     - ``class Dog extends Animal {}``
   * - コンストラクター
     - ``def __init__(self):``
     - ``constructor() {}``
   * - 自分自身
     - ``self``
     - ``this``
   * - インスタンスの作成
     - ``Dog()``
     - ``new Dog()``
   * - 例外処理
     - ``try:`` ／ ``except Exception as e:``
     - ``try {}`` ／ ``catch (e) {}``
   * - 例外の発生
     - ``raise ValueError("...")``
     - ``throw new Error("...");``
   * - モジュールの読み込み
     - ``from m import f``
     - ``import { f } from "./m.js";``
   * - 非同期関数
     - ``async def f():``
     - ``async function f() {}``
   * - 並行実行
     - ``await asyncio.gather(a(), b())``
     - ``await Promise.all([a(), b()])``

.. _sample-list:

D. サンプルコード一覧
---------------------

本資料のサンプルコードを示す。各ファイルのリンクからダウンロードできる。HTML ファイルは「表示」のリンクからブラウザで開ける。

`すべてのサンプルコードをまとめた ZIP ファイルをダウンロード <examples.zip>`__

.. list-table:: サンプルコード一覧
   :header-rows: 1
   :widths: 10 45 45

   * - 章
     - ファイル
     - 内容
   * - 1
     - `examples/index.html <examples/index.html>`__ （表示）
     - サンプルコードの一覧ページ。
   * - 1
     - :download:`hello.html <../examples/ch01/hello.html>` （`表示 <examples/ch01/hello.html>`__）
     - HTML・CSS・JavaScript の役割。
   * - 1
     - :download:`serve.py <../examples/ch01/serve.py>`
     - ローカルサーバーを起動する Python スクリプト。
   * - 2
     - :download:`basic_structure.html <../examples/ch02/basic_structure.html>` （`表示 <examples/ch02/basic_structure.html>`__）
     - 基本構造とテキストを表す要素。
   * - 2
     - :download:`link_image.html <../examples/ch02/link_image.html>` （`表示 <examples/ch02/link_image.html>`__）、:download:`sample.svg <../examples/ch02/sample.svg>`
     - リンクと画像。
   * - 2
     - :download:`list_table.html <../examples/ch02/list_table.html>` （`表示 <examples/ch02/list_table.html>`__）
     - リストと表。
   * - 3
     - :download:`semantic.html <../examples/ch03/semantic.html>` （`表示 <examples/ch03/semantic.html>`__）
     - セマンティック要素。
   * - 3
     - :download:`form.html <../examples/ch03/form.html>` （`表示 <examples/ch03/form.html>`__）
     - フォーム。
   * - 4
     - :download:`selector.html <../examples/ch04/selector.html>` （`表示 <examples/ch04/selector.html>`__）、:download:`style.css <../examples/ch04/style.css>`
     - セレクター・詳細度・継承。
   * - 4
     - :download:`box_model.html <../examples/ch04/box_model.html>` （`表示 <examples/ch04/box_model.html>`__）
     - ボックスモデル。
   * - 5
     - :download:`flexbox.html <../examples/ch05/flexbox.html>` （`表示 <examples/ch05/flexbox.html>`__）
     - Flexbox。
   * - 5
     - :download:`grid.html <../examples/ch05/grid.html>` （`表示 <examples/ch05/grid.html>`__）
     - Grid。
   * - 5
     - :download:`responsive.html <../examples/ch05/responsive.html>` （`表示 <examples/ch05/responsive.html>`__）
     - レスポンシブデザイン・CSS 変数・トランジション・アニメーション。
   * - 6
     - :download:`js_basics.html <../examples/ch06/js_basics.html>` （`表示 <examples/ch06/js_basics.html>`__）、:download:`basics.js <../examples/ch06/basics.js>`、:download:`array_methods.js <../examples/ch06/array_methods.js>`
     - JavaScript の基本文法と配列のメソッド。
   * - 6
     - :download:`compare_python.py <../examples/ch06/compare_python.py>`
     - 配列のメソッドに対応する Python のコード。
   * - 6
     - :download:`modules/index.html <../examples/ch06/modules/index.html>` （`表示 <examples/ch06/modules/index.html>`__）、:download:`modules/main.js <../examples/ch06/modules/main.js>`、:download:`modules/math_utils.js <../examples/ch06/modules/math_utils.js>`
     - モジュール（ローカルサーバーが必要）。
   * - 7
     - :download:`dom.html <../examples/ch07/dom.html>` （`表示 <examples/ch07/dom.html>`__）、:download:`dom.js <../examples/ch07/dom.js>`
     - DOM 操作。
   * - 7
     - :download:`event.html <../examples/ch07/event.html>` （`表示 <examples/ch07/event.html>`__）
     - イベント・フォームの検証・XSS。
   * - 8
     - :download:`async.html <../examples/ch08/async.html>` （`表示 <examples/ch08/async.html>`__）、:download:`async.js <../examples/ch08/async.js>`
     - Promise と ``async`` ／ ``await``。
   * - 8
     - :download:`fetch.html <../examples/ch08/fetch.html>` （`表示 <examples/ch08/fetch.html>`__）、:download:`data.json <../examples/ch08/data.json>`
     - ``fetch`` による JSON の取得（ローカルサーバーが必要）。
   * - 8
     - :download:`storage.html <../examples/ch08/storage.html>` （`表示 <examples/ch08/storage.html>`__）
     - Web Storage。
   * - 9
     - :download:`todo/index.html <../examples/ch09/todo/index.html>` （`表示 <examples/ch09/todo/index.html>`__）、:download:`todo/style.css <../examples/ch09/todo/style.css>`、:download:`todo/app.js <../examples/ch09/todo/app.js>`
     - ToDo アプリ。
