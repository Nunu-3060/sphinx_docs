非同期処理と通信
================

イベントループとシングルスレッド
--------------------------------

ブラウザの JavaScript は、シングルスレッドで動作する。つまり、同時に実行されるのは常に 1 つの処理だけである。そのため、時間のかかる処理（サーバーからの応答待ちなど）を実行中に待ち続けると、その間はボタンのクリックにも反応できず、ページ全体が固まってしまう。

これを避けるため、JavaScript では時間のかかる処理を非同期処理として扱う。非同期処理では、処理を開始したらその完了を待たずに次の処理へ進み、完了したときに、あらかじめ登録しておいた関数（コールバック）が呼び出される。

この仕組みを支えているのがイベントループである。ブラウザは、実行を待っているコールバックを待ち行列（キュー）に保持し、実行中の処理が終わるたびに、キューから次のコールバックを取り出して実行する。第 7 章で扱ったイベントリスナーも、イベントの発生時にこのキューに入れられて実行される。

Python の ``asyncio`` も同じくイベントループによる仕組みだが、Python では ``asyncio.run`` などで明示的にイベントループを起動する必要がある。ブラウザの JavaScript では、イベントループは最初から動いている。

コールバックと setTimeout
-------------------------

``setTimeout`` は、指定した時間が経過した後に関数を実行するよう予約する関数である。

.. code-block:: javascript

   console.log("1");
   setTimeout(() => console.log("3"), 1000); // 1000 ms (1 秒) 後に実行する
   console.log("2");

この例の出力は 1、2、3 の順になる。``setTimeout`` は予約をするだけですぐに戻り、1 秒待つのはブラウザの役割だからである。待ち時間に 0 を指定しても、コールバックは現在実行中の処理がすべて終わってから実行される。

非同期処理の完了をコールバックで受け取る書き方は、処理を順番に行いたい場合に、コールバックの中にさらにコールバックを書くことになり、入れ子が深くなって読みにくくなる。この問題を解決するのが、次に説明する Promise である。

Promise
-------

Promise は、非同期処理の結果を表すオブジェクトである。Promise は次の 3 つの状態のいずれかを持つ。

.. list-table:: Promise の状態
   :header-rows: 1
   :widths: 25 75

   * - 状態
     - 意味
   * - pending（待機）
     - 処理が完了していない。
   * - fulfilled（成功）
     - 処理が成功し、結果の値を持つ。
   * - rejected（失敗）
     - 処理が失敗し、失敗の理由（通常は ``Error`` オブジェクト）を持つ。

Promise の結果は、``then`` メソッドと ``catch`` メソッドにコールバックを登録して受け取る。

.. code-block:: javascript

   fetchScore("Alice")
     .then((data) => console.log(data))            // 成功したときに呼ばれる
     .catch((error) => console.log(error.message)); // 失敗したときに呼ばれる

Promise を返す関数を自分で作るには、``new Promise`` に関数を渡す。この関数は ``resolve`` と ``reject`` の 2 つの関数を引数に受け取る。処理が成功したら ``resolve(結果)`` を、失敗したら ``reject(理由)`` を呼び出す。

.. code-block:: javascript

   // 指定したミリ秒後に成功する Promise を返す
   function sleep(ms) {
     return new Promise((resolve) => setTimeout(resolve, ms));
   }

``Promise.resolve()`` のように完了済みの Promise であっても、``then`` に登録したコールバックはすぐには実行されず、現在実行中の処理が終わってから実行される。また、Promise のコールバックは ``setTimeout`` のコールバックよりも優先して実行される。

async / await
-------------

``async`` と ``await`` を使うと、Promise を使った非同期処理を、同期処理と同じように上から順に書ける。

.. code-block:: javascript

   async function main() {
     await sleep(1000); // 1 秒待つ
     const data = await fetchScore("Bob"); // 結果が得られるまで待つ
     console.log(data);
   }

.. list-table:: async / await の要点
   :header-rows: 1
   :widths: 30 70

   * - 記述
     - 意味
   * - ``async function``
     - 非同期関数を定義する。非同期関数は常に Promise を返す。``return`` した値は、その Promise の結果になる。
   * - ``await Promise``
     - Promise が完了するまで関数の実行を中断し、結果の値を取り出す。``async`` を付けた関数の中と、モジュールの最上位でだけ使える。
   * - ``try...catch``
     - ``await`` した Promise が失敗すると例外が発生するため、``try...catch`` で受け取れる。

``await`` で中断している間も、ブラウザは他のイベントを処理できる。中断するのはその非同期関数だけであり、ページ全体が止まるわけではない。

書き方は Python の ``asyncio`` とよく似ている。

.. list-table:: Python の asyncio との対応
   :header-rows: 1
   :widths: 50 50

   * - JavaScript
     - Python
   * - ``async function f() { ... }``
     - ``async def f(): ...``
   * - ``await sleep(1000)`` （自作の関数）
     - ``await asyncio.sleep(1)``
   * - ``await Promise.all([a(), b()])``
     - ``await asyncio.gather(a(), b())``
   * - ``main();`` （そのまま呼び出す）
     - ``asyncio.run(main())``

``Promise.all`` は、複数の Promise がすべて成功するのを待ち、結果を配列で返す。複数の処理を並行して実行できるため、1 つずつ ``await`` するよりも短い時間で済む。どれか 1 つでも失敗すると、``Promise.all`` の結果も失敗になる。

.. literalinclude:: ../examples/ch08/async.js
   :language: javascript
   :caption: examples/ch08/async.js

:download:`async.js をダウンロード <../examples/ch08/async.js>` ／ :download:`async.html をダウンロード <../examples/ch08/async.html>` ／ `ブラウザで表示 <examples/ch08/async.html>`__

fetch による HTTP 通信
----------------------

``fetch`` は、HTTP リクエストを送り、レスポンスを Promise で返す関数である。Python の ``requests`` ライブラリや ``urllib.request`` に相当するが、非同期で動作する点が異なる。

.. code-block:: javascript

   const response = await fetch("data.json");
   if (!response.ok) {
     throw new Error(`HTTP エラー: ${response.status}`);
   }
   const data = await response.json(); // 本体を JSON として解析する

.. list-table:: レスポンスの主なプロパティとメソッド
   :header-rows: 1
   :widths: 30 70

   * - 記述
     - 意味
   * - ``response.ok``
     - ステータスコードが 200 番台なら ``true``。
   * - ``response.status``
     - ステータスコード（200、404 など）。
   * - ``response.json()``
     - 本体を JSON として解析した結果を、Promise で返す。
   * - ``response.text()``
     - 本体を文字列として、Promise で返す。

``fetch`` は、ネットワークに接続できないなど通信自体が失敗した場合にだけ失敗の Promise を返す。サーバーが 404（ファイルが見つからない）や 500（サーバー内部のエラー）を返した場合は、通信自体は成功しているため、失敗にはならない。そのため、``response.ok`` を確認して自分でエラーとして扱う必要がある。

データを送信する場合は、第 2 引数にリクエストの内容を指定する。

.. code-block:: javascript

   const response = await fetch("/api/users", {
     method: "POST",
     headers: { "Content-Type": "application/json" },
     body: JSON.stringify({ name: "山田" }),
   });

次のサンプルは、同じフォルダーにある data.json を取得し、表に表示する。``fetch`` は ``file://`` で開いたページでは使えないため、第 1 章で説明したローカルサーバーを起動してから開くこと。

.. literalinclude:: ../examples/ch08/data.json
   :language: json
   :caption: examples/ch08/data.json

.. literalinclude:: ../examples/ch08/fetch.html
   :language: html
   :caption: examples/ch08/fetch.html

:download:`data.json をダウンロード <../examples/ch08/data.json>` ／ :download:`fetch.html をダウンロード <../examples/ch08/fetch.html>` ／ `ブラウザで表示 <examples/ch08/fetch.html>`__

同一オリジンポリシーと CORS
---------------------------

オリジンとは、URL のスキーム・ホスト・ポートの組み合わせである。たとえば ``https://example.com`` と ``https://api.example.com`` は、ホストが異なるため別のオリジンになる。

ブラウザには、あるオリジンのページで動く JavaScript が、別のオリジンのデータを勝手に読み取れないようにする仕組みがある。これを同一オリジンポリシーと呼ぶ。この制限が無いと、悪意のあるページを開いただけで、そのページの JavaScript が、利用者がログイン中の別のサイトから個人情報を読み取れてしまう。

別のオリジンのデータを ``fetch`` で読み取れるのは、相手のサーバーがレスポンスのヘッダーで許可している場合だけである。この許可の仕組みを CORS（Cross-Origin Resource Sharing）と呼ぶ。サーバーが ``Access-Control-Allow-Origin`` ヘッダーで読み取りを許可するオリジンを示し、ブラウザはそれを確認してから JavaScript にデータを渡す。

公開されている API を ``fetch`` で使おうとして「CORS」を含むエラーがコンソールに表示された場合、それはサーバー側が許可していないことを意味する。これはブラウザ側の JavaScript だけでは解決できない。Python のプログラムからは同じ API にアクセスできることがあるのは、同一オリジンポリシーがブラウザ独自の仕組みだからである。

Web Storage
-----------

Web Storage は、ブラウザの中にデータを保存する仕組みである。キーと値の組でデータを保存し、2 種類がある。

.. list-table:: Web Storage の種類
   :header-rows: 1
   :widths: 25 75

   * - 名前
     - データが保存される期間
   * - ``localStorage``
     - 明示的に削除するまで。ブラウザを閉じても残る。
   * - ``sessionStorage``
     - タブを閉じるまで。

.. list-table:: Web Storage の主なメソッド
   :header-rows: 1
   :widths: 45 55

   * - 記述
     - 意味
   * - ``localStorage.setItem("key", "value")``
     - 値を保存する。
   * - ``localStorage.getItem("key")``
     - 値を取得する。キーが無ければ ``null`` を返す。
   * - ``localStorage.removeItem("key")``
     - 値を削除する。

保存できる値は文字列だけである。数値は文字列に変換され、オブジェクトや配列はそのままでは保存できない。オブジェクトや配列を保存するには ``JSON.stringify`` で文字列に変換し、取り出すときに ``JSON.parse`` で元に戻す。

保存されたデータは、オリジンごとに分けて管理される。また、利用者は開発者ツールの「アプリケーション」タブ（Firefox では「ストレージ」タブ）で内容を確認・変更できる。パスワードなどの機密情報を保存してはならない。

.. literalinclude:: ../examples/ch08/storage.html
   :language: html
   :caption: examples/ch08/storage.html

:download:`storage.html をダウンロード <../examples/ch08/storage.html>` ／ `ブラウザで表示 <examples/ch08/storage.html>`__
