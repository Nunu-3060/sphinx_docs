################################################################
第 13 章 GameObject とコンポーネントの操作
################################################################

この章では、スクリプトからほかのコンポーネントを取得する方法、Transform を使って位置や回転を変える方法、GameObject を生成・破棄する方法を学びます。

コンポーネントの取得
================================================================

GetComponent
----------------------------------------------------------------

同じ GameObject にアタッチされているほかのコンポーネントを使うには、``GetComponent<T>()`` を使います。``T`` には、取得したいコンポーネントの型を指定します。

.. code-block:: csharp

   Renderer renderer = GetComponent<Renderer>();
   renderer.material.color = Color.red;

指定した型のコンポーネントが見つからない場合、``GetComponent`` は ``null`` を返します。

``GetComponent`` は、``Update`` の中で毎フレーム呼ぶと処理の無駄になります。``Awake`` などで 1 回だけ取得し、フィールドに保存しておいて使ってください。

TryGetComponent
----------------------------------------------------------------

コンポーネントがあるかどうかわからない場合は、``TryGetComponent`` を使います。コンポーネントが見つかれば ``true`` を返し、``out`` 引数に結果を入れます。

.. code-block:: csharp

   if (TryGetComponent(out Rigidbody body))
   {
       Debug.Log(body.mass);
   }

RequireComponent
----------------------------------------------------------------

スクリプトが特定のコンポーネントを必ず必要とする場合は、クラスに ``[RequireComponent(typeof(Rigidbody))]`` のような属性を付けます。こうすると、スクリプトをアタッチしたときに、必要なコンポーネントも自動で追加されます。また、必要なコンポーネントを誤って削除することも防げます（第 16 章のサンプルコードで使います）。

ほかの GameObject の参照
----------------------------------------------------------------

ほかの GameObject やそのコンポーネントを使いたいときは、``[SerializeField]`` を付けたフィールドを用意し、Inspector ウィンドウで参照を設定するのが基本です。Hierarchy ウィンドウから GameObject をフィールドにドラッグすると、参照を設定できます。

.. code-block:: csharp

   [SerializeField] private GameObject _target;
   [SerializeField] private Transform _player;    // コンポーネントの型でも受け取れる

.. note::

   名前で GameObject を探す ``GameObject.Find`` というメソッドもありますが、シーン内のすべてのオブジェクトを調べるため処理が遅く、無効な GameObject は見つけられません。また、GameObject の名前を変えると見つからなくなります。できるだけ Inspector ウィンドウで参照を設定してください。

Transform の操作
================================================================

位置、回転、拡大縮小
----------------------------------------------------------------

GameObject の位置、回転、拡大縮小は、Transform コンポーネントのプロパティで操作します。

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - プロパティ
     - 型
     - 意味
   * - ``position``
     - ``Vector3``
     - ワールド座標（シーン全体を基準とした座標）での位置
   * - ``localPosition``
     - ``Vector3``
     - 親を基準とした位置（親がいなければ ``position`` と同じ）
   * - ``rotation``
     - ``Quaternion``
     - ワールド座標での回転（第 15 章）
   * - ``localScale``
     - ``Vector3``
     - 親を基準とした拡大縮小の倍率
   * - ``forward``、``right``、``up``
     - ``Vector3``
     - GameObject から見た前方、右方向、上方向の向き

position の一部だけを変更する
----------------------------------------------------------------

``transform.position.y += 1f;`` と書くと、コンパイルエラーになります。

.. code-block:: text

   error CS1612: Cannot modify the return value of 'Transform.position' because it is not a variable

これは、``position`` が ``Vector3``\ （値型）を返すプロパティで、得られるのは位置のコピーだからです。コピーの ``y`` を変えても、元の位置は変わりません（第 7 章）。位置の一部だけを変えるときは、いったん変数にコピーし、値を変えてから代入し直します。

.. code-block:: csharp

   Vector3 position = transform.position;
   position.y += 1f;
   transform.position = position;

親子関係
----------------------------------------------------------------

Hierarchy ウィンドウで GameObject をほかの GameObject の上にドラッグすると、親子関係を設定できます。子は、親の移動、回転、拡大縮小に合わせて一緒に動きます。スクリプトからは、``transform.SetParent(親の Transform)`` で親子関係を設定し、``transform.parent`` で親を、``transform.childCount`` と ``transform.GetChild(インデックス)`` で子を取得できます。

GameObject の有効と無効
----------------------------------------------------------------

``gameObject.SetActive(false)`` を呼ぶと、GameObject が無効になります。無効な GameObject は画面に表示されず、そのコンポーネントのイベント関数（``Update`` など）も呼ばれません。GameObject 自身が有効かどうかは ``activeSelf`` で調べられます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 書き方
     - 無効になるもの
   * - ``gameObject.SetActive(false)``
     - GameObject 全体（すべてのコンポーネントと、子の GameObject）
   * - ``enabled = false``
     - そのコンポーネントだけ（第 10 章）

コンポーネント操作のサンプルコード
================================================================

.. literalinclude:: ../../examples/ch13/ComponentAccessSample.cs
   :language: csharp
   :caption: ComponentAccessSample.cs

:download:`ComponentAccessSample.cs をダウンロード <../../examples/ch13/ComponentAccessSample.cs>`

Play モードを開始すると、Cube が赤くなり、1 m 上に移動し、Y 軸まわりに 45° 回転した向きになり、X 方向に 2 倍に引き伸ばされます。Target に設定した GameObject は Cube の子になり、2 秒ごとに表示と非表示が切り替わります。回転を作る ``Quaternion.Euler`` は第 15 章で、経過時間を表す ``Time.time`` は第 11 章で説明しています。

プレハブ
================================================================

同じ GameObject を何個も使いたい場合は、プレハブを使います。プレハブは、GameObject をコンポーネントや設定値ごと保存したアセットです。

プレハブを作るには、Hierarchy ウィンドウの GameObject を Project ウィンドウにドラッグします。Project ウィンドウに青い立方体のアイコンのアセットが作られれば、プレハブの完成です。プレハブを編集すると、そのプレハブから作ったすべての GameObject に変更が反映されます。

生成と破棄
================================================================

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - メソッド
     - 説明
   * - ``Instantiate(プレハブ, 位置, 回転)``
     - プレハブ（またはシーン内の GameObject）を複製して、シーンに生成します。生成したオブジェクトを戻り値で返します。
   * - ``Destroy(オブジェクト)``
     - GameObject やコンポーネントを破棄します。
   * - ``Destroy(オブジェクト, 秒数)``
     - 指定した秒数が経ってから破棄します。

``Destroy`` を呼んでも、オブジェクトはすぐには破棄されません。実際の破棄は、現在のフレームの ``Update`` がすべて終わった後に行われます。この性質による注意点は、第 18 章で説明します。

.. note::

   ``Destroy(this)`` と書くと、GameObject ではなく、このスクリプトのコンポーネントだけが破棄されます。GameObject ごと破棄するには、``Destroy(gameObject)`` と書きます。

ランダムな値
----------------------------------------------------------------

``Random.Range(最小値, 最大値)`` は、範囲内のランダムな値を返します。引数の型によって、最大値が含まれるかどうかが異なるので注意してください。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 呼び出し方
     - 返す値
   * - ``Random.Range(0f, 10f)``\ （``float``）
     - 0 以上 10 以下の小数
   * - ``Random.Range(0, 10)``\ （``int``）
     - 0 以上 10 未満の整数（0 から 9 まで）

生成と破棄のサンプルコード
================================================================

.. literalinclude:: ../../examples/ch13/Spawner.cs
   :language: csharp
   :caption: Spawner.cs

:download:`Spawner.cs をダウンロード <../../examples/ch13/Spawner.cs>`

Cube などをプレハブにして Prefab に設定し、Play モードを開始すると、1 秒ごとにランダムな位置にオブジェクトが生成され、3 秒後に消えます。``Quaternion.identity`` は回転していない状態を表します（第 15 章）。

まとめ
================================================================

* 同じ GameObject のコンポーネントは ``GetComponent`` で取得し、フィールドに保存して使います。
* ほかの GameObject への参照は、Inspector ウィンドウで設定するのが基本です。
* ``transform.position`` の一部を変更するときは、いったん変数にコピーしてから代入し直します。
* プレハブから GameObject を生成するには ``Instantiate`` を、破棄するには ``Destroy`` を使います。
