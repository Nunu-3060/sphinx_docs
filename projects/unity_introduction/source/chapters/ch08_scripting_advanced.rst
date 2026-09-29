第 8 章 スクリプトの応用
========================

この章では、時間のかかる処理、オブジェクト間の連携、データの分離など、ゲームを作るときによく使うスクリプトの技法を説明します。また、Inspector ウィンドウの表示を整える方法と、エディター拡張の入り口も紹介します。

この章のサンプルコードは、``examples/chapter08`` フォルダーにあります。

コルーチン
----------

「0.2 秒ごとに点滅を 5 回繰り返す」のように、複数のフレームにまたがる処理を ``Update`` だけで書くと、経過時間や回数を管理するフィールドが増えて、コードが複雑になります。このような処理は、**コルーチン** を使うと簡潔に書けます。

.. literalinclude:: ../../examples/chapter08/Blinker.cs
   :caption: Blinker.cs
   :linenos:

:download:`Blinker.cs をダウンロード <../../examples/chapter08/Blinker.cs>`

コルーチンは、戻り値の型が ``IEnumerator`` のメソッドとして定義し、``StartCoroutine`` で開始します。``IEnumerator`` を使うには、ファイルの先頭に ``using System.Collections;`` が必要です。``yield return`` の行で処理がいったん中断され、指定した条件を満たすと、その続きから再開されます。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 書き方
     - 再開するタイミング
   * - ``yield return null;``
     - 次のフレーム
   * - ``yield return new WaitForSeconds(秒数);``
     - 指定した秒数が経過した後
   * - ``yield return new WaitForFixedUpdate();``
     - 次の ``FixedUpdate`` の後
   * - ``yield return new WaitUntil(() => 条件);``
     - 条件が ``true`` になったとき
   * - ``yield return StartCoroutine(別のコルーチン);``
     - 別のコルーチンが終わったとき

実行中のコルーチンは、``StopCoroutine`` で止められます。また、GameObject を無効にしたり破棄したりすると、その GameObject で実行していたコルーチンもすべて止まります。

.. note::

   コルーチンは、別のスレッドで並列に動くしくみではありません。すべてメインスレッドで実行されるので、コルーチンの中で重い計算をすると、その間はゲーム全体が止まります。

イベントによる連携
------------------

「プレイヤーの体力が 0 になったら、ゲームオーバーの画面を表示し、効果音を鳴らし、スコアを保存する」という処理を考えます。体力を管理するクラスが、画面、効果音、スコアのクラスを直接呼び出すと、クラス同士が強く結び付き、変更しにくいコードになります。

このような場合は **イベント** を使います。体力を管理するクラスは「体力が 0 になった」ことを通知するだけにして、通知を受け取りたいクラスがそれぞれ購読するようにします。Unity では、C# の ``event`` と、Unity の ``UnityEvent`` の 2 種類がよく使われます。

.. literalinclude:: ../../examples/chapter08/Health.cs
   :caption: Health.cs
   :linenos:

:download:`Health.cs をダウンロード <../../examples/chapter08/Health.cs>`

.. literalinclude:: ../../examples/chapter08/HealthLogger.cs
   :caption: HealthLogger.cs
   :linenos:

:download:`HealthLogger.cs をダウンロード <../../examples/chapter08/HealthLogger.cs>`

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 種類
     - 購読の方法
     - 向いている用途
   * - C# の ``event``
     - スクリプトで ``+=`` を使って登録し、``-=`` で解除します。
     - スクリプト同士の連携
   * - ``UnityEvent``
     - Inspector ウィンドウで、呼び出す GameObject とメソッドを設定します。
     - スクリプトを書かずに、Inspector ウィンドウで連携を設定したい場合

``Health`` の ``HealthChanged`` は C# の ``event`` です。``HealthLogger`` は、``OnEnable`` で購読を開始し、``OnDisable`` で解除しています。購読を解除し忘れると、破棄された GameObject のメソッドが呼ばれてエラーになることがあるため、購読の開始と解除は必ず対にしてください。

``_died`` は ``UnityEvent`` です。Inspector ウィンドウの :guilabel:`Died ()` の欄にある :guilabel:`+` をクリックし、GameObject とメソッドを選ぶと、体力が 0 になったときにそのメソッドが呼ばれます。例えば、GameObject を設定して、メソッドの一覧から :menuselection:`GameObject --> SetActive (bool)` を選び、チェックボックスをオフにしておくと、体力が 0 になったときにその GameObject を非表示にできます。

``Health`` と ``HealthLogger`` の使い方は次のとおりです。

#. 空の GameObject を作成し、``Health`` と ``HealthLogger`` を付けます。
#. ``HealthLogger`` の :guilabel:`Health` に、同じ GameObject の ``Health`` コンポーネントをドラッグ＆ドロップします。
#. 再生し、``Health`` のコンポーネントのメニュー（⋮）から「1 ダメージを与える」を選ぶと、Console ウィンドウに残りの体力が表示されます。

``Health`` に付けた ``[ContextMenu("1 ダメージを与える")]`` は、Inspector ウィンドウのコンポーネント名の右にあるメニュー（⋮）に項目を追加する属性です。再生中にこの項目を選ぶと ``TakeOneDamage`` が呼ばれるので、ダメージの処理を手軽に試せます。

ScriptableObject によるデータの分離
-----------------------------------

アイテムの名前や価格、敵の体力や攻撃力のような設定値を、スクリプトや Prefab に直接書き込むと、同じ値をあちこちで管理することになります。**ScriptableObject** を使うと、設定値をアセットとして独立させ、複数の GameObject から共有できます。

.. literalinclude:: ../../examples/chapter08/ItemData.cs
   :caption: ItemData.cs
   :linenos:

:download:`ItemData.cs をダウンロード <../../examples/chapter08/ItemData.cs>`

``[CreateAssetMenu]`` 属性を付けると、Project ウィンドウを右クリックして表示されるメニューから、アセットを作成できるようになります。この例では、:menuselection:`Create --> Unity Introduction --> Item Data` でアセットを作成し、Inspector ウィンドウで値を設定します。

作成したアセットは、次のようにスクリプトのフィールドに設定して使います。

.. literalinclude:: ../../examples/chapter08/ItemInfoLogger.cs
   :caption: ItemInfoLogger.cs
   :linenos:

:download:`ItemInfoLogger.cs をダウンロード <../../examples/chapter08/ItemInfoLogger.cs>`

ScriptableObject の値を複数の GameObject で共有すると、アセットの値を 1 か所変えるだけで、すべての GameObject に反映されます。また、データがシーンから独立するため、ゲームデザイナーなどプログラマー以外の人も値を調整しやすくなります。

.. warning::

   Unity Editor 上で再生中に ScriptableObject の値をスクリプトから変更すると、その変更は再生を終えても元に戻らず、アセットに保存されます。ScriptableObject は、ゲーム中に変化しない設定値の保存に使い、ゲーム中に変化する値（現在の体力など）は通常のフィールドで管理してください。

Inspector の表示を整える属性
----------------------------

フィールドに属性を付けると、Inspector ウィンドウでの表示を整えられます。スクリプトの設定項目がわかりやすくなり、誤った値の入力も防げます。

.. literalinclude:: ../../examples/chapter08/InspectorAttributesExample.cs
   :caption: InspectorAttributesExample.cs
   :linenos:

:download:`InspectorAttributesExample.cs をダウンロード <../../examples/chapter08/InspectorAttributesExample.cs>`

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 属性
     - 効果
   * - ``[Header("見出し")]``
     - フィールドの上に見出しを表示します。
   * - ``[Tooltip("説明")]``
     - マウスカーソルを項目名に重ねたときに説明を表示します。
   * - ``[Range(最小値, 最大値)]``
     - 数値をスライダーで入力するようにし、範囲外の値を入力できないようにします。
   * - ``[Min(最小値)]``
     - 最小値より小さい値を入力できないようにします。
   * - ``[Space(高さ)]``
     - フィールドの上に余白を入れます。
   * - ``[TextArea(最小行数, 最大行数)]``
     - 文字列を複数行の入力欄で入力するようにします。
   * - ``[ContextMenu("項目名")]``
     - メソッドに付けると、コンポーネントのメニュー（⋮）からそのメソッドを呼び出せるようにします。

エディター拡張の入り口
----------------------

Unity Editor そのものに、独自のメニューやウィンドウ、Inspector の表示を追加することを **エディター拡張** と呼びます。繰り返し行う作業を自動化したり、チームで使う専用のツールを作ったりできます。

エディター拡張のスクリプトは、``Editor`` という名前のフォルダーに置きます。``Editor`` フォルダー（``Assets/Scripts/Editor`` のように、どの階層にあってもかまいません）に置いたスクリプトは Unity Editor の中だけで使われ、ビルドしたアプリケーションには含まれません。エディター拡張では ``UnityEditor`` 名前空間のクラスを使いますが、このクラスはビルドしたアプリケーションでは使えないため、``Editor`` フォルダー以外に置くとビルドが失敗します。

次のスクリプトは、選択している GameObject の高さを 0 にそろえるメニューを、:menuselection:`Tools --> Unity Introduction --> Align To Ground` に追加します。

.. literalinclude:: ../../examples/chapter08/Editor/AlignToGroundMenu.cs
   :caption: Editor/AlignToGroundMenu.cs
   :linenos:

:download:`AlignToGroundMenu.cs をダウンロード <../../examples/chapter08/Editor/AlignToGroundMenu.cs>`

``[MenuItem]`` 属性を付けた ``static`` メソッドが、メニューの項目になります。第 2 引数に ``true`` を指定した ``[MenuItem]`` を同じパスで定義すると、メニューの項目を選べるかどうかを判定するメソッドになります。この例では、GameObject を 1 つも選んでいないときは、メニューの項目が灰色になって選べなくなります。

``Undo.RecordObjects`` で変更前の状態を記録しておくと、メニューで行った変更を :kbd:`Ctrl` + :kbd:`Z` で元に戻せるようになります。エディター拡張でシーンを変更するときは、Undo への登録を忘れないようにしてください。

ここで紹介したメニューの追加のほかに、独自のウィンドウ（``EditorWindow``）や、特定のコンポーネントの Inspector の表示を置き換える機能（``Editor`` クラスと ``[CustomEditor]`` 属性）などがあります。詳しくは :doc:`ch19_next_steps` で紹介する資料を参照してください。

よくある誤り
------------

Unity のスクリプトで初心者がつまずきやすい点をまとめます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 誤り
     - 説明と対策
   * - ``Update`` で重い処理を行う
     - ``Update`` は毎フレーム呼ばれるため、``GetComponent`` や ``GameObject.Find`` などの処理を毎回行うと、ゲームが重くなります。取得したものは ``Awake`` や ``Start`` でフィールドに保持してください。
   * - ``Update`` と ``FixedUpdate`` の使い分けを誤る
     - ``Rigidbody`` に力を加える処理は ``FixedUpdate`` に書きます。一方、キーが押された瞬間の判定など、入力の読み取りは ``Update`` に書きます。``FixedUpdate`` はフレームごとに呼ばれるとは限らないため、ここで入力を読み取ると、押した瞬間を取りこぼすことがあります。
   * - Inspector ウィンドウで参照を設定し忘れる
     - ``[SerializeField]`` のフィールドに何も設定しないまま使うと、``UnassignedReferenceException`` や ``NullReferenceException`` が発生します。エラーメッセージをダブルクリックして、どのフィールドが原因かを確認してください。
   * - Unity のオブジェクトに ``?.`` や ``??`` を使う
     - ``Destroy`` で破棄された GameObject やコンポーネントは、``== null`` で比較すると ``true`` になるように Unity が特別な処理をしています。しかし、``?.``、``??``、``is null`` はこの処理を通らないため、破棄済みのオブジェクトを正しく判定できません。``GameObject`` や ``Component`` などの Unity のオブジェクトは、``!= null`` で判定してください。
   * - ``Destroy`` の直後に破棄されたと考える
     - ``Destroy`` を呼んでも、GameObject が実際に破棄されるのは、そのフレームの処理が終わった後です。``Destroy`` を呼んだ後も、同じフレームの間はその GameObject が存在しています。
