DOM 操作とイベント
==================

DOM とは
--------

ブラウザは HTML を解析し、各要素をオブジェクトとした木構造をメモリ上に作る。これを DOM（Document Object Model）と呼ぶ。たとえば、次の HTML からは、``html`` 要素を根とし、``head`` 要素と ``body`` 要素を子に持つ木構造が作られる。

.. code-block:: html

   <html>
     <head><title>例</title></head>
     <body>
       <h1>見出し</h1>
       <p>本文</p>
     </body>
   </html>

画面に表示されるのは、HTML ファイルそのものではなく、この DOM である。JavaScript で DOM を変更すると、その変更は即座に画面に反映される。一方、DOM を変更しても元の HTML ファイルは変わらないため、ページを再読み込みすると元の状態に戻る。

JavaScript からは、グローバル変数 ``document`` を通じて DOM を操作する。

要素の取得
----------

DOM を操作するには、まず対象の要素を取得する。

.. list-table:: 要素を取得するメソッド
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 戻り値
   * - ``document.querySelector("セレクター")``
     - CSS のセレクターに一致する最初の要素。無ければ ``null``。
   * - ``document.querySelectorAll("セレクター")``
     - CSS のセレクターに一致するすべての要素の一覧（``NodeList``）。``for...of`` で順に処理できる。
   * - ``document.getElementById("id")``
     - 指定した ``id`` 属性を持つ要素。無ければ ``null``。

``querySelector`` と ``querySelectorAll`` は、第 4 章で扱った CSS のセレクターをそのまま使えるため、覚えることが少なくて済む。また、``document`` だけでなく個々の要素からも呼び出すことができ、その場合はその要素の中だけを検索する。

``querySelectorAll`` が返す一覧は、呼び出した時点の状態を表す。後から追加された要素は含まれないため、必要になったときに改めて取得する。

要素の内容・属性・スタイルの変更
--------------------------------

.. list-table:: 要素を変更する主なプロパティとメソッド
   :header-rows: 1
   :widths: 40 60

   * - 記述
     - 意味
   * - ``element.textContent = "文字列"``
     - 要素の内容を、指定した文字列に置き換える。
   * - ``element.innerHTML = "HTML"``
     - 要素の内容を、指定した文字列を HTML として解釈した結果に置き換える（後述の注意を参照）。
   * - ``element.setAttribute("href", "...")``
     - 属性の値を設定する。``getAttribute`` で取得、``removeAttribute`` で削除する。
   * - ``element.classList.add("name")``
     - クラスを追加する。``remove`` で削除、``toggle`` で有無を切り替える。
   * - ``element.style.color = "red"``
     - ``style`` 属性を設定する。CSS のプロパティ名の ``-`` は取り除いて、次の文字を大文字にする（``background-color`` は ``backgroundColor``）。
   * - ``input.value``
     - 入力欄の現在の値。値は常に文字列である。

見た目を変えるときは、``style`` プロパティで直接指定するよりも、CSS にクラスごとのスタイルを定義しておき、``classList`` でクラスを付け外しする方がよい。見た目の定義を CSS に集められるため、保守しやすくなる。

要素の作成と削除
----------------

新しい要素は ``document.createElement`` で作り、``append`` で親要素の末尾に追加する。

.. code-block:: javascript

   const item = document.createElement("li"); // <li></li> を作る
   item.textContent = "みかん";                // <li>みかん</li> になる
   list.append(item);                          // list の末尾に追加する

``createElement`` で作った直後の要素は、まだ画面に表示されていない。``append`` などで DOM に追加したときに初めて表示される。

要素を削除するには、削除したい要素の ``remove`` メソッドを呼ぶ。また、``replaceChildren`` メソッドは、要素の子をすべて引数の要素に置き換える。引数を省略すると、子をすべて削除する。

.. literalinclude:: ../examples/ch07/dom.html
   :language: html
   :caption: examples/ch07/dom.html

.. literalinclude:: ../examples/ch07/dom.js
   :language: javascript
   :caption: examples/ch07/dom.js

:download:`dom.html をダウンロード <../examples/ch07/dom.html>` ／ :download:`dom.js をダウンロード <../examples/ch07/dom.js>` ／ `ブラウザで表示 <examples/ch07/dom.html>`__

イベントとイベントリスナー
--------------------------

ブラウザ上の JavaScript は、イベント駆動で動く。イベントとは、クリックやキー入力など、ページ上で起きた出来事のことである。あらかじめ「このイベントが起きたらこの関数を実行する」と登録しておくと、イベントが発生するたびに、ブラウザがその関数を呼び出す。登録する関数をイベントリスナーと呼ぶ。

Python のプログラムは通常、先頭から順に実行されて最後に終了する。これに対し、ブラウザの JavaScript は、最初にイベントリスナーを登録し終えた後も、ページが開いている間はイベントを待ち続ける。GUI アプリケーションの作り方に近い。

イベントリスナーは ``addEventListener`` で登録する。

.. code-block:: javascript

   const button = document.querySelector("#greet-button");
   button.addEventListener("click", () => {
     console.log("クリックされた");
   });

第 1 引数はイベントの種類、第 2 引数はイベントが起きたときに呼ばれる関数である。第 2 引数には関数そのものを渡す。``button.addEventListener("click", handleClick())`` のように括弧を付けて書くと、登録時に関数が実行され、その戻り値が登録されてしまうので注意する。

.. list-table:: 主なイベント
   :header-rows: 1
   :widths: 25 75

   * - イベント
     - 発生するタイミング
   * - ``click``
     - 要素がクリックされたとき。
   * - ``input``
     - 入力欄の値が変わるたび。
   * - ``change``
     - 入力欄の値が確定したとき（フォーカスが外れたときや、選択肢を選んだときなど）。
   * - ``submit``
     - フォームが送信されるとき。``form`` 要素で発生する。
   * - ``keydown``
     - キーが押されたとき。
   * - ``DOMContentLoaded``
     - HTML の解析が終わり、DOM が完成したとき。``document`` で発生する。

イベントオブジェクトとバブリング
--------------------------------

イベントオブジェクト
~~~~~~~~~~~~~~~~~~~~

イベントリスナーの関数は、引数としてイベントオブジェクトを受け取る。イベントオブジェクトには、イベントに関する情報が含まれる。

.. list-table:: イベントオブジェクトの主なプロパティとメソッド
   :header-rows: 1
   :widths: 35 65

   * - 記述
     - 意味
   * - ``event.target``
     - イベントが実際に発生した要素（クリックされた要素など）。
   * - ``event.currentTarget``
     - イベントリスナーを登録した要素。
   * - ``event.key``
     - 押されたキー（``keydown`` イベントの場合）。
   * - ``event.preventDefault()``
     - イベントに対するブラウザの既定の動作を止める。

``preventDefault`` は、たとえばフォームの送信時に使う。``submit`` イベントの既定の動作は、フォームの内容をサーバーに送ってページを移動することである。``preventDefault`` を呼ぶと送信とページの移動が止まり、JavaScript で入力値を処理できるようになる。

バブリング
~~~~~~~~~~

要素で発生したイベントは、その要素のイベントリスナーを呼び出した後、親要素、さらにその親要素へと順に伝わっていく。これをバブリングと呼ぶ。

たとえば、``#outer`` の中に ``#inner`` がある場合、``#inner`` をクリックすると、``#inner`` のイベントリスナーに続いて ``#outer`` のイベントリスナーも呼び出される。このとき ``#outer`` のイベントリスナーでは、``event.target`` は ``#inner``、``event.currentTarget`` は ``#outer`` になる。

バブリングを利用すると、多数の子要素のイベントを、親要素に登録した 1 つのイベントリスナーでまとめて処理できる。これをイベント委譲と呼ぶ。後から追加された子要素のイベントも処理できるため、第 9 章の ToDo アプリで利用する。

フォーム入力の取得と検証
------------------------

フォームの入力値は、入力欄の要素の ``value`` プロパティで取得する。``form`` 要素の ``elements`` プロパティを使うと、``form.elements.username`` のように、``name`` 属性の値で入力欄を取得できる。

入力値を JavaScript で検証するには、``form`` 要素の ``submit`` イベントにイベントリスナーを登録し、``preventDefault`` で送信を止めてから値を確認する。``button`` 要素の ``click`` イベントではなく ``submit`` イベントを使うと、入力欄で Enter キーを押して送信した場合も同じように処理できる。

サンプルの ``form`` 要素に付けた ``novalidate`` 属性は、第 3 章で扱ったブラウザによる検証を無効にする。ここでは JavaScript による検証の動作を確認するために指定している。

innerHTML の危険性と XSS 対策
-----------------------------

``innerHTML`` に代入した文字列は HTML として解釈される。そのため、利用者が入力した文字列を ``innerHTML`` に代入すると、入力に含まれるタグがそのまま HTML として動作してしまう。

たとえば、利用者が次の文字列を入力したとする。

.. code-block:: html

   <img src=x onerror="alert('XSS')">

これを ``innerHTML`` で表示すると、存在しない画像 ``x`` の読み込みに失敗した時点で ``onerror`` 属性の JavaScript が実行される。この例ではメッセージが表示されるだけだが、悪意のある入力であれば、利用者の情報を盗み出すスクリプトを実行することもできる。このような攻撃をクロスサイトスクリプティング（XSS）と呼ぶ。

利用者の入力や外部から取得したデータを表示するときは、``innerHTML`` ではなく ``textContent`` を使う。``textContent`` に代入した文字列は HTML として解釈されず、``<`` なども文字としてそのまま表示される。HTML の構造を組み立てる必要がある場合は、``createElement`` で要素を作り、その ``textContent`` に文字列を代入する。

次のサンプルで、バブリング、フォームの検証、``innerHTML`` と ``textContent`` の違いを確認できる。

.. literalinclude:: ../examples/ch07/event.html
   :language: html
   :caption: examples/ch07/event.html

:download:`event.html をダウンロード <../examples/ch07/event.html>` ／ `ブラウザで表示 <examples/ch07/event.html>`__
