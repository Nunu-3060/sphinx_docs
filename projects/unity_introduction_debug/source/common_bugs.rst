.. _common-bugs:

よくある不具合と対処法
======================

本章では、Unity の開発で頻繁に遭遇する不具合と、その原因、対処法を紹介します。

.. _null-reference:

NullReferenceException と UnassignedReferenceException
------------------------------------------------------

``NullReferenceException`` は、null（何も参照していない状態）の変数を通してメンバーにアクセスしたときに発生する例外です。Unity の開発で最もよく目にするエラーのひとつです。

Unity で null になる主な原因は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 原因
     - 例
   * - Inspector ウィンドウでの設定忘れ
     - ``[SerializeField]`` のフィールドに、オブジェクトを設定していません。
   * - コンポーネントが見つからない
     - ``GetComponent`` で取得しようとしたコンポーネントが、GameObject に追加されていません。
   * - オブジェクトが見つからない
     - ``GameObject.Find`` に渡した名前が誤っているか、対象の GameObject が無効になっています。
   * - 初期化前のアクセス
     - 他のスクリプトの ``Awake`` で初期化される変数に、それより先にアクセスしています（:ref:`execution-order`）。

なお、エディター上では、Inspector ウィンドウで設定していない ``UnityEngine.Object`` 型のフィールドにアクセスすると、``NullReferenceException`` ではなく ``UnassignedReferenceException`` が発生します。エラーメッセージにフィールド名が表示されるため、設定忘れであることがすぐに分かります。

主な対策は次のとおりです。

* 必要なコンポーネントには ``[RequireComponent]`` 属性を付け、追加し忘れを防ぎます。
* ``Awake`` や ``Start`` で参照が設定されているかを確認し、設定されていなければ context を付けてエラーを出力します。
* 取得できないことがあり得るコンポーネントは、``TryGetComponent`` で取得し、戻り値で成否を判定します。

.. code-block:: csharp

   [SerializeField]
   private Transform target;

   private void Awake()
   {
       if (target == null)
       {
           // どの GameObject の設定漏れかが分かるように、context に this を渡します。
           Debug.LogError("Target が設定されていません。", this);
       }
   }

.. _missing-reference:

MissingReferenceException と破棄されたオブジェクト
--------------------------------------------------

``MissingReferenceException`` は、``Destroy`` で破棄された GameObject やコンポーネントにアクセスしたときに発生する例外です。

破棄されたオブジェクトの扱いには、Unity 特有の注意点が 2 つあります。

1 つ目は、``Destroy`` を呼び出しても、オブジェクトはすぐには破棄されないことです。実際の破棄は、現在のフレームの Update 処理が終わった後に行われます。そのため、``Destroy`` を呼び出した直後のコードでは、オブジェクトはまだ有効です。すぐに無効にしたい場合は、``Destroy`` の前に ``SetActive(false)`` を呼び出します。

2 つ目は、null との比較の結果が、比較の方法によって異なることです。``UnityEngine.Object`` は ``==`` 演算子を独自に定義しており、破棄されたオブジェクトを null と等しいと判定します。一方で、C# の ``?.`` 演算子、``??`` 演算子、``is null`` は ``==`` 演算子を使わずに参照そのものを調べるため、破棄されたオブジェクトを null と判定しません。

破棄された GameObject を参照している変数 ``obj`` に対する結果は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 式
     - 結果
   * - ``obj == null``
     - true（null として扱われる）
   * - ``obj != null``、``if (obj)``
     - false（null として扱われる）
   * - ``obj is null``
     - false（null として扱われない）
   * - ``obj?.name``
     - ``MissingReferenceException`` が発生する
   * - ``obj ?? other``
     - ``other`` ではなく、破棄された ``obj`` が返る

``UnityEngine.Object`` を継承した型（GameObject、コンポーネント、アセットなど）の null チェックには、``==`` 演算子、``!=`` 演算子、または ``if (obj)`` のような bool への暗黙の変換を使ってください。

.. literalinclude:: ../examples/NullCheckExample.cs
   :language: csharp
   :caption: NullCheckExample.cs

:download:`NullCheckExample.cs をダウンロード <../examples/NullCheckExample.cs>`

.. _execution-order:

イベント関数の実行順序
----------------------

``Awake`` や ``Update`` のように、Unity から自動的に呼び出されるメソッドをイベント関数と呼びます。イベント関数が呼び出される順序を理解していないと、初期化前の変数にアクセスする不具合が起こります。

代表的なイベント関数と、呼び出されるタイミングは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - イベント関数
     - 呼び出されるタイミング
   * - ``Awake``
     - オブジェクトが読み込まれたときに 1 回だけ呼び出されます。GameObject が有効であれば、コンポーネントが無効でも呼び出されます。
   * - ``OnEnable``
     - コンポーネントが有効になるたびに呼び出されます。初回は ``Awake`` の直後です。
   * - ``Start``
     - 最初の ``Update`` の直前に 1 回だけ呼び出されます。コンポーネントが無効な場合は、有効になるまで呼び出されません。
   * - ``FixedUpdate``
     - 物理演算の更新に合わせて、一定の間隔で呼び出されます（:ref:`update-fixedupdate`）。
   * - ``Update``
     - 毎フレーム 1 回呼び出されます。
   * - ``LateUpdate``
     - 毎フレーム、すべての ``Update`` の後に呼び出されます。キャラクターを追いかけるカメラの処理などに使います。
   * - ``OnDisable``
     - コンポーネントが無効になるたびに呼び出されます。オブジェクトが破棄される直前にも呼び出されます。
   * - ``OnDestroy``
     - オブジェクトが破棄される直前に呼び出されます。

シーンの読み込み時には、すべてのオブジェクトの ``Awake`` と ``OnEnable`` が呼び出された後で、各オブジェクトの ``Start`` が呼び出されます。ただし、異なるオブジェクトの間で ``Awake`` 同士がどの順序で呼び出されるかは決まっていません。そのため、次のように役割を分けるのが基本です。

* ``Awake`` では、自分自身の初期化（自分のコンポーネントの取得など）だけを行います。
* ``Start`` では、他のオブジェクトを参照する初期化を行います。

どうしても特定のスクリプトを先に実行したい場合は、:menuselection:`Edit --> Project Settings --> Script Execution Order` で順序を指定するか、クラスに ``[DefaultExecutionOrder]`` 属性を付けます。属性の引数の値が小さいスクリプトほど先に実行されます。

.. literalinclude:: ../examples/ExecutionOrderExample.cs
   :language: csharp
   :caption: ExecutionOrderExample.cs

:download:`ExecutionOrderExample.cs をダウンロード <../examples/ExecutionOrderExample.cs>`

.. _update-fixedupdate:

Update と FixedUpdate、Time.deltaTime の使い分け
------------------------------------------------

``Update`` と ``FixedUpdate`` は、呼び出される間隔が異なります。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 項目
     - ``Update``
     - ``FixedUpdate``
   * - 呼び出される間隔
     - 毎フレーム 1 回。間隔はフレームレートによって変わる。
     - 一定の時間ごと。既定では 0.02 秒（1 秒に 50 回）。1 フレームの間に 0 回のことも、複数回のこともある。
   * - 主な用途
     - 入力の読み取り、Rigidbody を使わない移動、ゲームの進行管理
     - Rigidbody に力を加えるなど、物理演算に関わる処理

``FixedUpdate`` で入力を読み取ると、``FixedUpdate`` が呼び出されなかったフレームの入力を取りこぼすことがあります。入力は ``Update`` で読み取り、その結果を ``FixedUpdate`` で物理演算に反映してください。

``Update`` で物体を移動させる場合は、移動量に ``Time.deltaTime``\ （前のフレームからの経過時間）を掛けます。

.. code-block:: csharp

   // 悪い例: 1 フレームごとに 0.1 ずつ移動するため、60 fps では 1 秒間に 6、30 fps では 3 進む。
   transform.position += Vector3.forward * 0.1f;

   // 良い例: 1 秒間に 6 進む。フレームレートに関係なく同じ速さになる。
   transform.position += Vector3.forward * 6f * Time.deltaTime;

``Time.deltaTime`` を掛けないと、フレームレートによって移動速度が変わってしまい、性能の低い端末ではゲームの進行が遅くなります。なお、``FixedUpdate`` の中で ``Time.deltaTime`` を参照すると、``FixedUpdate`` の呼び出し間隔（``Time.fixedDeltaTime``）が返ります。

浮動小数点数の比較
------------------

``float`` 型の値は、誤差を含むことがあります。たとえば 0.1 は ``float`` 型で正確に表せないため、``0.1f`` を 10 回足した結果は ``1.0f`` と等しくなりません。

.. code-block:: csharp

   float sum = 0f;
   for (int i = 0; i < 10; i++)
   {
       sum += 0.1f;
   }

   Debug.Log(sum == 1.0f);                   // False（sum は 1.0000001 になる）
   Debug.Log(Mathf.Approximately(sum, 1.0f)); // True

``float`` 型の値が等しいかどうかを調べるときは、``==`` 演算子ではなく ``Mathf.Approximately`` を使うか、差の絶対値が許容範囲内かどうかで判定します。目的地に着いたかどうかの判定なども、``Vector3.Distance(a, b) < 0.01f`` のように、許容範囲を設けて判定します。

.. note::

   ``Vector3`` の ``==`` 演算子は、内部で誤差を許容した比較を行います。そのため、ごくわずかに異なる 2 つのベクトルも等しいと判定されます。

コルーチンと async / await の落とし穴
-------------------------------------

コルーチン
^^^^^^^^^^

コルーチンは、``StartCoroutine`` を呼び出した MonoBehaviour に結び付いて動作します。次の点に注意してください。

* GameObject が無効になるか破棄されると、その GameObject で実行中のコルーチンはすべて停止します。GameObject を再び有効にしても、コルーチンは再開しません。
* コンポーネントの ``enabled`` を false にしても、コルーチンは停止しません。
* 無効な GameObject では ``StartCoroutine`` を呼び出せず、エラーになります。

async / await
^^^^^^^^^^^^^

``async`` / ``await`` を使った非同期処理は、GameObject とは無関係に動作します。そのため、処理の途中で GameObject が破棄されたり再生が停止されたりしても、非同期処理は続きます。その結果、破棄されたオブジェクトにアクセスして ``MissingReferenceException`` が発生することがあります。

MonoBehaviour の ``destroyCancellationToken`` プロパティを使うと、オブジェクトの破棄と同時に非同期処理をキャンセルできます。待機には、Unity が提供する ``Awaitable`` クラスを使うと便利です。

.. code-block:: csharp

   private async Awaitable ShowMessageLaterAsync()
   {
       try
       {
           // オブジェクトが破棄されると、待機中に OperationCanceledException が発生します。
           await Awaitable.WaitForSecondsAsync(3f, destroyCancellationToken);
           Debug.Log("3 秒経過しました。", this);
       }
       catch (OperationCanceledException)
       {
           // 破棄によるキャンセルなので、何もしません。
       }
   }

また、戻り値が ``Task`` や ``Awaitable`` の非同期メソッドを ``await`` せずに呼び出すと、その中で発生した例外が Console ウィンドウに表示されず、不具合に気付けないことがあります。非同期メソッドは原則として ``await`` で呼び出してください。

シリアライズに関する不具合
--------------------------

「コードで初期値を変更したのに反映されない」「再生中に変更した値が元に戻った」といった不具合の多くは、シリアライズの仕組みが原因です。シリアライズとは、Inspector ウィンドウで設定した値をシーンやプレハブに保存する仕組みです。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 症状
     - 原因と対処
   * - コードでフィールドの初期値を変更したのに反映されない
     - 既に GameObject に追加されているコンポーネントでは、シーンに保存された値がコードの初期値よりも優先されます。コンポーネントの ⋮ メニューから :guilabel:`Reset` を選ぶと、コードの初期値に戻せます。
   * - 再生中に Inspector ウィンドウで変更した値が、再生を終えると元に戻る
     - 再生中の変更は保存されない仕様です。残したい値は、再生を終える前にメモしておくか、コンポーネントの ⋮ メニューから :guilabel:`Copy Component` でコピーし、再生後に :guilabel:`Paste Component Values` で貼り付けます。
   * - フィールドの名前を変更したら、設定していた値が消えた
     - 値はフィールドの名前で保存されているためです。名前を変更する場合は、``[FormerlySerializedAs("旧名")]`` 属性を付けると、以前の値を引き継げます。
   * - フィールドが Inspector ウィンドウに表示されない
     - private のフィールドには ``[SerializeField]`` 属性が必要です。また、``Dictionary`` など、Unity がシリアライズできない型は表示されません。
