################################################################
第 18 章 Unity 固有の注意点
################################################################

Unity のスクリプトは C# で書きますが、Unity 独自の仕組みのために、普通の C# のプログラムとは異なる動きをする部分があります。この章では、初心者がつまずきやすい点と、データを管理するための ScriptableObject について説明します。

Unity のオブジェクトと null
================================================================

破棄したオブジェクトは null と等しくなる
----------------------------------------------------------------

GameObject やコンポーネントなど、Unity のオブジェクトは ``UnityEngine.Object`` クラスを継承しています。``UnityEngine.Object`` では、``==`` 演算子が特別な動きをするように作られています。

``Destroy`` で破棄したオブジェクトは、変数の中身が ``null`` になるわけではありません。C# のオブジェクトとしては残っていますが、Unity の内部のデータは破棄されています。``UnityEngine.Object`` の ``==`` 演算子は、このような破棄済みのオブジェクトを ``null`` と等しいと判定します。そのため、``if (target != null)`` と書けば、「参照が設定されていて、かつ破棄されていない」ことを確かめられます。

.. literalinclude:: ../../examples/ch18/NullCheckSample.cs
   :language: csharp
   :caption: NullCheckSample.cs

:download:`NullCheckSample.cs をダウンロード <../../examples/ch18/NullCheckSample.cs>`

.. code-block:: text
   :caption: 実行結果

   Destroy の直後: cube == null は False
   1 フレーム後: cube == null は True
   1 フレーム後: cube is null は False

第 13 章で説明したとおり、``Destroy`` を呼んでもすぐには破棄されないため、``Destroy`` の直後の比較は ``False`` になります。

?. と ?? を使ってはいけない理由
----------------------------------------------------------------

第 9 章で説明した ``?.``、``??``、``is null`` は、``==`` 演算子を使わずに「本当に ``null`` かどうか」だけを調べます。そのため、破棄済みのオブジェクトを ``null`` とみなしません。

.. code-block:: csharp

   // 誤った例: _target が破棄済みでも SetActive が呼ばれ、MissingReferenceException が発生する
   _target?.SetActive(false);

   // 正しい例
   if (_target != null)
   {
       _target.SetActive(false);
   }

Unity のオブジェクトが ``null`` かどうかを調べるときは、必ず ``==`` か ``!=`` を使ってください。

パフォーマンスの注意点
================================================================

``Update`` は毎フレーム呼ばれるため、その中に重い処理を書くと、ゲーム全体が遅くなります。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 避けたい書き方
     - 改善方法
   * - ``Update`` の中で ``GetComponent`` を呼ぶ
     - ``Awake`` で 1 回だけ取得し、フィールドに保存します（第 13 章）。
   * - ``Update`` の中で ``GameObject.Find`` などを使ってオブジェクトを探す
     - Inspector ウィンドウで参照を設定するか、``Start`` で 1 回だけ探して保存します。
   * - ``Update`` の中で ``new`` を使って配列やクラスのインスタンスを作る
     - 使い回せるものはフィールドに保存して再利用します。不要になったメモリを回収する処理（ガベージコレクション）が頻繁に起きると、ゲームが一瞬止まる原因になります。
   * - ``Update`` の中で ``Debug.Log`` を呼ぶ
     - ``Debug.Log`` は処理に時間がかかります。調査が終わったら削除します。

.. note::

   ``Vector3`` や ``Quaternion`` は構造体なので、``new Vector3(...)`` と書いてもガベージコレクションの対象にはなりません。

static なデータとシーンの読み込み
================================================================

シーンを読み込み直すと、シーン内の GameObject はすべて破棄され、作り直されます。一方、``static`` なフィールドやプロパティの値は、シーンを読み込み直しても残ります。第 19 章の ``GameManager`` では、この性質を考慮して ``OnDestroy`` で ``static`` なプロパティを ``null`` に戻しています。

また、Project Settings の Editor にある Enter Play Mode Settings で、Play モードの開始時にドメイン（スクリプトの状態）を再読み込みしない設定にしている場合は、Play モードを終了しても ``static`` な値が残ります。``static`` なデータを使うときは、初期化するタイミングに注意してください。

ScriptableObject
================================================================

敵の種類ごとの HP や速さのように、複数の GameObject で共有したいデータがあります。このようなデータは、ScriptableObject を使ってアセットとして保存すると便利です。

ScriptableObject は、``ScriptableObject`` クラスを継承したクラスです。``MonoBehaviour`` と異なり GameObject にはアタッチせず、Project ウィンドウに独立したアセットとして保存します。

.. literalinclude:: ../../examples/ch18/EnemyData.cs
   :language: csharp
   :caption: EnemyData.cs

:download:`EnemyData.cs をダウンロード <../../examples/ch18/EnemyData.cs>`

``[CreateAssetMenu]`` 属性を付けると、Project ウィンドウの右クリックメニューに、アセットを作成する項目が追加されます。この例では、Create > Samples > Enemy Data を選ぶと EnemyData のアセットが作成され、Inspector ウィンドウで値を設定できます。

作成したアセットは、コンポーネントの ``[SerializeField]`` のフィールドに、Project ウィンドウからドラッグして設定します。

.. literalinclude:: ../../examples/ch18/EnemyStatus.cs
   :language: csharp
   :caption: EnemyStatus.cs

:download:`EnemyStatus.cs をダウンロード <../../examples/ch18/EnemyStatus.cs>`

同じ EnemyData のアセットを 100 体の敵で共有しても、データは 1 つだけです。値を変更するときも、アセットを 1 つ編集するだけで済みます。

.. warning::

   Unity エディターの Play モード中にスクリプトから ScriptableObject のフィールドを書き換えると、その変更は Play モードを終了してもアセットに残ります。敵ごとに変化する現在の HP などは、サンプルコードの ``_currentHp`` のように、コンポーネント側に持たせてください。

まとめ
================================================================

* 破棄した Unity のオブジェクトは、``==`` で ``null`` と比べると ``true`` になります。
* Unity のオブジェクトには、``?.``、``??``、``is null`` を使わず、``==`` と ``!=`` を使います。
* ``Update`` の中では、``GetComponent``、オブジェクトの検索、``new`` によるインスタンスの生成を避けます。
* ``static`` な値は、シーンを読み込み直しても残ります。
* 複数のオブジェクトで共有するデータは、ScriptableObject にまとめます。
