おわりに
========

本資料のまとめ
--------------

本資料では、Web ページを構成する 3 つの言語について、次の内容を扱った。

.. list-table:: 各章の要点
   :header-rows: 1
   :widths: 25 75

   * - 章
     - 要点
   * - HTML（第 2 章・第 3 章）
     - 要素で文書の構造と意味を表す。見た目ではなく意味で要素を選ぶ。フォームで利用者の入力を受け付ける。
   * - CSS（第 4 章・第 5 章）
     - セレクターで要素を選び、見た目を指定する。複数のルールの優先度はカスケードと詳細度で決まる。レイアウトには Flexbox と Grid を使い、メディアクエリで画面幅に対応する。
   * - JavaScript（第 6 章～第 8 章）
     - Python と似た文法を持つが、``===``、``undefined``、暗黙の型変換などの違いがある。DOM を操作して画面を変え、イベントリスナーで利用者の操作に応答する。時間のかかる処理は Promise と ``async`` ／ ``await`` で非同期に扱う。

次に学ぶこと
------------

本資料の内容を理解したら、目的に応じて次のような分野に進むとよい。

.. list-table:: 次に学ぶ分野
   :header-rows: 1
   :widths: 25 75

   * - 分野
     - 内容
   * - TypeScript
     - JavaScript に静的な型を追加した言語である。Python の型ヒントと mypy の組み合わせに近く、規模の大きい開発で誤りを早期に発見できる。
   * - フレームワーク
     - React、Vue、Svelte などがある。第 9 章で扱った「状態から画面を作る」考え方を、より効率的に実現する。
   * - ビルドツール
     - npm（パッケージ管理）や Vite（開発サーバーとビルド）など。フレームワークや TypeScript を使う場合に必要になる。
   * - サーバーサイド
     - フォームの送信を受け取ったり、``fetch`` で呼び出す API を提供したりするプログラムである。Python の Flask、Django、FastAPI などで作れるため、Python の経験を活かせる。
   * - アクセシビリティとセキュリティ
     - 第 3 章と第 7 章で扱った内容をさらに深める。実際にサービスを公開する場合には欠かせない知識である。

参考資料
--------

* `MDN Web Docs <https://developer.mozilla.org/ja/>`_：Mozilla が運営する、HTML・CSS・JavaScript のリファレンスとチュートリアル。日本語訳も充実しており、まず最初に参照するとよい。
* `HTML Living Standard <https://html.spec.whatwg.org/multipage/>`_：HTML の仕様書（英語）。
* `CSS Specifications <https://www.w3.org/Style/CSS/specs.en.html>`_：W3C による CSS の仕様書の一覧（英語）。
* `ECMAScript Language Specification <https://tc39.es/ecma262/>`_：JavaScript の仕様書（英語）。
* `Can I use <https://caniuse.com/>`_：各ブラウザが HTML・CSS・JavaScript のどの機能に対応しているかを調べられるサイト（英語）。
* `Markup Validation Service <https://validator.w3.org/>`_：HTML の誤りを検出する W3C のサービス（英語）。
