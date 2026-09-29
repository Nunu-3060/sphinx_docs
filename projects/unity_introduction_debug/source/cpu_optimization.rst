.. _cpu-optimization:

CPU（スクリプト）の最適化
=========================

本章では、CPU バウンドの原因のうち、スクリプトに関するものの改善手法を紹介します。いずれの手法も、Profiler でボトルネックであることを確認してから適用してください。

.. _gc-allocation:

ガベージコレクションと GC アロケーションの削減
----------------------------------------------

ガベージコレクションの仕組み
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

C# でクラスのインスタンスや配列を ``new`` で生成すると、マネージドヒープと呼ばれるメモリ領域が確保されます。このメモリの確保を GC アロケーションと呼びます。使われなくなったメモリは、ガベージコレクター（GC）が自動的に探して解放します。この解放の処理をガベージコレクションと呼びます。

ガベージコレクションは、マネージドヒープの空きが足りなくなったときなどに実行されます。Unity のガベージコレクションは、実行中にメインスレッドの処理を止めるため、1 回に時間がかかるとスパイクの原因になります。毎フレーム GC アロケーションが発生するコードがあると、ガベージコレクションが頻繁に実行されます。

Unity では、インクリメンタル GC が既定で有効になっています。インクリメンタル GC は、ガベージコレクションの処理を複数のフレームに分割して実行し、1 フレームあたりの停止時間を短くします。ただし、処理の総量が減るわけではないため、GC アロケーションそのものを減らすことが基本です。設定は :menuselection:`Edit --> Project Settings --> Player` の :guilabel:`Use incremental GC` で変更できます。

GC アロケーションが発生しやすいコード
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``Update`` など毎フレーム実行されるメソッドでは、次のようなコードに注意してください。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - コード
     - 説明と対策
   * - 文字列の連結、書式設定
     - ``string`` は変更できない型のため、連結や ``$"..."`` による書式設定のたびに新しい文字列が生成されます。値が変わったときだけ文字列を生成するようにします。
   * - LINQ
     - ``Where`` や ``Select`` などは、呼び出しのたびに列挙用のオブジェクトを生成します。毎フレーム実行する処理では、``for`` 文で書き直します。
   * - コレクションや配列の ``new``
     - 毎回新しく生成せず、フィールドに保持したものを ``Clear`` して使い回します。
   * - ボックス化
     - ``int`` などの値型を ``object`` 型やインターフェイス型の変数に代入すると、値を包むオブジェクトが生成されます。
   * - 変数をキャプチャするラムダ式
     - ラムダ式の外側のローカル変数を参照すると、その変数を保持するためのオブジェクトが生成されます。
   * - 配列を返す Unity の API
     - ``Physics.RaycastAll``、``GetComponents``、``Mesh.vertices`` などは、呼び出しのたびに新しい配列を返します。GC アロケーションが発生しない API を使います（:ref:`non-alloc-api`）。
   * - ``gameObject.tag`` との比較
     - ``tag`` プロパティは、呼び出しのたびに新しい文字列を返します。タグの比較には ``CompareTag`` を使います。

次のサンプルでは、GC アロケーションが発生するコードと、改善後のコードを切り替えて比較できます。

.. literalinclude:: ../examples/GcAllocationExample.cs
   :language: csharp
   :caption: GcAllocationExample.cs

:download:`GcAllocationExample.cs をダウンロード <../examples/GcAllocationExample.cs>`

GetComponent と Find の結果のキャッシュ
---------------------------------------

``GetComponent`` は GameObject のコンポーネントを検索し、``GameObject.Find`` はシーン内のすべての有効な GameObject を名前で検索します。これらを毎フレーム呼び出すと、検索のコストが積み重なります。

一度取得した参照は、フィールドに保存（キャッシュ）して使い回します。自分自身のコンポーネントは ``Awake`` で、他のオブジェクトのコンポーネントは ``Start`` で取得するのが基本です。``GameObject.Find`` は特に処理が重いため、可能であれば Inspector ウィンドウで参照を設定する方法に置き換えます。

.. literalinclude:: ../examples/ComponentCacheExample.cs
   :language: csharp
   :caption: ComponentCacheExample.cs

:download:`ComponentCacheExample.cs をダウンロード <../examples/ComponentCacheExample.cs>`

.. note::

   シーン内のオブジェクトを型で検索する ``FindObjectOfType`` は、Unity 6 では非推奨になりました。代わりに ``FindFirstObjectByType`` または ``FindAnyObjectByType`` を使います。どのオブジェクトが返ってもよい場合は、より高速な ``FindAnyObjectByType`` を使います。

Update の呼び出し数の削減
-------------------------

``Update`` などのイベント関数は、Unity のエンジン（C++ で書かれたネイティブコード）から C# のスクリプトを呼び出す仕組みのため、1 回の呼び出しごとに一定のコストがかかります。1 つ 1 つのコストは小さくても、数千個の GameObject がそれぞれ ``Update`` を持っていると、無視できない負荷になります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 手法
     - 説明
   * - 空のイベント関数を削除する
     - 中身が空でも、定義されている ``Update`` は毎フレーム呼び出されます。スクリプトのテンプレートから作られた空の ``Update`` は削除します。
   * - 管理クラスにまとめる
     - 多数のオブジェクトが同じ処理を行う場合は、それぞれに ``Update`` を持たせず、1 つの管理クラスの ``Update`` からリストの全オブジェクトを処理します。
   * - イベント駆動にする
     - 「毎フレーム HP を確認して表示を更新する」のではなく、「HP が変化したときにイベントで通知して表示を更新する」ようにします。
   * - 処理を間引く
     - 毎フレーム実行する必要のない処理（遠くの敵の経路探索など）は、数フレームに 1 回や、一定時間ごとに実行します。

.. _object-pool:

オブジェクトプール
------------------

弾やエフェクトのように、短い時間で生成と破棄を繰り返すオブジェクトに ``Instantiate`` と ``Destroy`` を使うと、生成と破棄のコストに加えて GC アロケーションも発生します。

オブジェクトプールは、使い終わったオブジェクトを破棄せずに非表示にして保管し、次に必要になったときに再利用する手法です。Unity には、オブジェクトプールを実装するための ``UnityEngine.Pool.ObjectPool<T>`` クラスが用意されています。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メソッド・引数
     - 説明
   * - ``Get``
     - プールからオブジェクトを取り出します。プールが空の場合は、``createFunc`` で新しく生成します。
   * - ``Release``
     - オブジェクトをプールに戻します。
   * - ``actionOnGet``、``actionOnRelease``
     - 取り出すとき、戻すときに実行する処理です。表示・非表示の切り替えなどを行います。
   * - ``collectionCheck``
     - true にすると、同じオブジェクトを 2 回プールに戻したときに例外を発生させます。この確認はエディターでのみ行われます。
   * - ``maxSize``
     - プールに保持するオブジェクトの最大数です。これを超えて戻されたオブジェクトは、``actionOnDestroy`` で破棄されます。

.. literalinclude:: ../examples/BulletPool.cs
   :language: csharp
   :caption: BulletPool.cs

:download:`BulletPool.cs をダウンロード <../examples/BulletPool.cs>`

.. warning::

   再利用されるオブジェクトには、前回使われたときの状態（位置、速度、HP など）が残っています。プールから取り出すたびに、必要な状態を初期化してください。

.. _non-alloc-api:

GC アロケーションが発生しない API の利用
----------------------------------------

Unity の API には、結果を新しい配列で返すものと、呼び出し側が用意した配列やリストに結果を書き込むものがあります。毎フレーム呼び出す処理では、後者を使うことで GC アロケーションを避けられます。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - GC アロケーションが発生する API
     - 代わりに使う API
   * - ``Physics.RaycastAll``
     - ``Physics.RaycastNonAlloc``
   * - ``Physics.OverlapSphere``
     - ``Physics.OverlapSphereNonAlloc``
   * - ``GetComponents<T>()``
     - ``GetComponents<T>(List<T>)``
   * - ``Mesh.vertices``
     - ``Mesh.GetVertices(List<Vector3>)``
   * - ``gameObject.tag == "Player"``
     - ``gameObject.CompareTag("Player")``

.. literalinclude:: ../examples/RaycastNonAllocExample.cs
   :language: csharp
   :caption: RaycastNonAllocExample.cs

:download:`RaycastNonAllocExample.cs をダウンロード <../examples/RaycastNonAllocExample.cs>`

``RaycastNonAlloc`` などの API で取得できる結果の数は、渡した配列の長さが上限になります。また、結果は距離の順に並んでいるとは限りません。

発展的な手法
------------

本資料では詳しく扱いませんが、大量のデータを処理する場合には、次の手法も有効です。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 手法
     - 概要
   * - C# Job System
     - 処理を複数のワーカースレッドに分散し、CPU の複数のコアを活用します。
   * - Burst コンパイラー
     - Job System のジョブなどを、高度に最適化されたネイティブコードに変換します。数値計算の多い処理が大幅に高速になることがあります。
   * - IL2CPP
     - C# のコードを C++ に変換してからビルドするスクリプティングバックエンドです。:menuselection:`Edit --> Project Settings --> Player` の :guilabel:`Scripting Backend` で選択します。一般に Mono よりも実行速度が速く、iOS では IL2CPP が必須です。
