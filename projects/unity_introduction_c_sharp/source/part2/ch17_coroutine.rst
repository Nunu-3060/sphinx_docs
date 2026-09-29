################################################################
第 17 章 コルーチンと非同期処理
################################################################

「3 秒待ってから敵を出す」「0.2 秒ごとに点滅させる」のように、時間をかけて進む処理はゲームでよく使われます。この章では、このような処理を書くためのコルーチンと、async と await を使った非同期処理を学びます。

時間のかかる処理の問題
================================================================

``Update`` や ``Start`` の中で、次のように書いて 3 秒待つことはできません。

.. code-block:: csharp

   // 誤った例: Time.time が変わらないため、この while は終わらず、Unity エディターが応答しなくなる
   float start = Time.time;
   while (Time.time - start < 3f)
   {
   }

Unity は、1 つのフレームの中ですべてのスクリプトの ``Update`` を順番に呼び出し、それが終わってから画面を描画します。そのため、1 つのメソッドの中で待ち続けると、画面の更新も止まってしまいます。この例では、フレームが進まないため ``Time.time`` も変わらず、ループが終わらなくなります。

コルーチンを使うと、処理を途中で中断し、次のフレーム以降に続きから再開できます。

コルーチン
================================================================

コルーチンは、戻り値の型を ``IEnumerator`` にしたメソッドです。``IEnumerator`` を使うには、ファイルの先頭に ``using System.Collections;`` を書きます。

.. code-block:: csharp

   private IEnumerator Countdown()
   {
       Debug.Log(3);
       yield return new WaitForSeconds(1f);    // ここで中断し、1 秒後に再開する
       Debug.Log(2);
   }

``yield return`` を実行すると、コルーチンはそこで中断します。そして、``yield return`` の後に指定した条件を満たすと、中断したところから再開します。

コルーチンは、``StartCoroutine(Countdown());`` のように ``StartCoroutine`` を使って開始します。``Countdown();`` のように普通のメソッドとして呼び出しても、処理は実行されません。なお、``Start`` は、``private IEnumerator Start()`` と書くとそれ自体をコルーチンにでき、``StartCoroutine`` を使わずに ``yield return`` を書けます（第 18 章のサンプルコードで使います）。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - yield return の書き方
     - 再開するタイミング
   * - ``yield return null;``
     - 次のフレームの ``Update`` の後
   * - ``yield return new WaitForSeconds(秒数);``
     - 指定した秒数が経った後（``Time.timeScale`` の影響を受けます）
   * - ``yield return new WaitForSecondsRealtime(秒数);``
     - 指定した秒数が経った後（``Time.timeScale`` の影響を受けません）
   * - ``yield return new WaitUntil(() => 条件);``
     - 条件が ``true`` になった後
   * - ``yield return new WaitForFixedUpdate();``
     - 次の ``FixedUpdate`` の後
   * - ``yield return StartCoroutine(別のコルーチン);``
     - 別のコルーチンが終わった後

``Time.timeScale`` は、ゲーム内の時間の進む速さです。一時停止の機能を作るときに 0 にすることがあります。

.. literalinclude:: ../../examples/ch17/CountdownCoroutine.cs
   :language: csharp
   :caption: CountdownCoroutine.cs

:download:`CountdownCoroutine.cs をダウンロード <../../examples/ch17/CountdownCoroutine.cs>`

.. code-block:: text
   :caption: 実行結果（1 秒ごとに 1 行ずつ表示される）

   3
   2
   1
   スタート！

コルーチンの停止
----------------------------------------------------------------

コルーチンは、次の場合に停止します。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 状況
     - 停止するか
   * - コルーチンの最後まで実行した
     - 停止する
   * - ``StopCoroutine`` を呼んだ
     - そのコルーチンが停止する
   * - ``StopAllCoroutines`` を呼んだ
     - そのコンポーネントで実行中のすべてのコルーチンが停止する
   * - GameObject を無効にした、または破棄した
     - 停止する
   * - コンポーネントを無効にした（``enabled = false``）
     - 停止しない

``StopCoroutine`` には、``StartCoroutine`` の戻り値の ``Coroutine`` を渡します。

.. literalinclude:: ../../examples/ch17/BlinkCoroutine.cs
   :language: csharp
   :caption: BlinkCoroutine.cs

:download:`BlinkCoroutine.cs をダウンロード <../../examples/ch17/BlinkCoroutine.cs>`

``while (true)`` は無限ループですが、毎回 ``yield return`` で中断するため、ゲームが止まることはありません。``yield return`` を書き忘れると、第 4 章で説明した無限ループになるので注意してください。

.. note::

   コルーチンは、``Update`` などと同じく、Unity のメインの処理の流れの中で少しずつ実行されます。別のスレッドで並行して実行されるわけではありません。

async と await
================================================================

Unity 6 では、C# の ``async`` と ``await`` を使って、コルーチンと同じような処理を書けます。Unity が用意している ``Awaitable`` クラスを使います。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 書き方
     - 意味
   * - ``await Awaitable.WaitForSecondsAsync(秒数);``
     - 指定した秒数だけ待ちます。
   * - ``await Awaitable.NextFrameAsync();``
     - 次のフレームまで待ちます。
   * - ``await Awaitable.FixedUpdateAsync();``
     - 次の ``FixedUpdate`` まで待ちます。

``await`` を使うメソッドには ``async`` を付け、戻り値の型を ``Awaitable`` にします。``Start`` も、``private async Awaitable Start()`` と書けば ``async`` メソッドにできます。

.. literalinclude:: ../../examples/ch17/AwaitableSample.cs
   :language: csharp
   :caption: AwaitableSample.cs

:download:`AwaitableSample.cs をダウンロード <../../examples/ch17/AwaitableSample.cs>`

.. warning::

   コルーチンと異なり、``async`` メソッドは GameObject が破棄されても自動的には止まりません。破棄された後で GameObject を操作しようとすると、エラーになります。待つときは、サンプルコードのように ``destroyCancellationToken`` を渡し、オブジェクトが破棄されたら処理が中止されるようにしてください。中止されると ``OperationCanceledException`` が発生するため、``try`` と ``catch`` で処理します。

コルーチンと async / await の使い分け
================================================================

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 項目
     - コルーチン
     - async / await
   * - 開始のしかた
     - ``StartCoroutine`` で開始する
     - 普通のメソッドとして呼び出す
   * - GameObject が破棄されたとき
     - 自動的に停止する
     - ``destroyCancellationToken`` を使って止める
   * - 結果を返す
     - 返せない
     - ``Awaitable<T>`` で返せる
   * - 例外の扱い
     - ``yield return`` を含む部分を ``try`` と ``catch`` で囲めない
     - ``try`` と ``catch`` で処理できる

どちらを使ってもかまいませんが、初めのうちは、自動的に停止するコルーチンの方が扱いやすいでしょう。

まとめ
================================================================

* 1 つのメソッドの中で待ち続けると、ゲーム全体が止まってしまいます。
* コルーチンは、``yield return`` で処理を中断し、後から続きを再開できます。
* コルーチンは ``StartCoroutine`` で開始し、``StopCoroutine`` で停止します。
* Unity 6 では、``Awaitable`` を使って ``async`` と ``await`` で書くこともできます。その場合は、``destroyCancellationToken`` を使って処理を止められるようにします。
