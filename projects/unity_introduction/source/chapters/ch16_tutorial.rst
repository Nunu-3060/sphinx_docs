第 16 章 チュートリアル：玉転がしゲームの制作
=============================================

この章では、これまでに学んだ内容を組み合わせて、簡単な 3D ゲームを作ります。各手順で使う機能の詳しい説明は、手順の中で示す章を参照してください。

この章のサンプルコードは、``examples/chapter16`` フォルダーにあります。

完成イメージと仕様
------------------

プレイヤーはボールを転がして、ステージ上に置かれたアイテムをすべて集めます。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 仕様
   * - 操作
     - :kbd:`W`、:kbd:`A`、:kbd:`S`、:kbd:`D` キー、矢印キー、ゲームパッドの左スティックで、ボールを前後左右に転がします。
   * - アイテム
     - ステージ上で回転しています。ボールが触れると、エフェクトと効果音とともに消え、スコアが 1 増えます。
   * - ゲームクリア
     - すべてのアイテムを集めると、画面に「Clear!」と表示されます。
   * - ゲームオーバー
     - ボールがステージから落ちると、画面に「Game Over」と表示されます。
   * - リトライ
     - ゲームクリアまたはゲームオーバーになると :guilabel:`Retry` ボタンが表示され、クリックすると最初からやり直せます。

作成するスクリプトは次の 5 つです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - スクリプト
     - 役割
   * - ``PlayerController``
     - 入力に応じてボールを転がします。
   * - ``CameraFollow``
     - カメラをボールに追従させます。
   * - ``Rotator``
     - アイテムを回転させます。
   * - ``Pickup``
     - ボールが触れたときに、アイテムを回収します。
   * - ``GameManager``
     - スコアの管理、ゲームクリアとゲームオーバーの判定、リトライを行います。

手順 1：プロジェクトとシーンの準備
----------------------------------

#. :doc:`ch03_setup` の手順で、:guilabel:`Universal 3D` テンプレートの新しいプロジェクトを作成します。
#. :menuselection:`File --> New Scene` で :guilabel:`Basic (URP)` を選んで新しいシーンを作成し、:menuselection:`File --> Save As` で ``Assets/Scenes`` フォルダーに ``RollABall`` という名前で保存します。
#. :menuselection:`File --> Build Profiles` を開き、:guilabel:`Scene List` に ``RollABall`` シーンを追加します。リトライのときにシーンを読み込み直すために必要です（:doc:`ch15_scenes_and_data` を参照）。
#. Project ウィンドウの ``Assets`` フォルダーに、``Scripts``、``Materials``、``Prefabs`` の 3 つのフォルダーを作成します。
#. サンプルコードの ``examples/chapter16`` フォルダーにある 5 つのスクリプトを、``Assets/Scripts`` フォルダーにコピーします。自分で入力する場合は、この章のコードを見ながら作成してください。

手順 2：ステージの作成
----------------------

#. :menuselection:`GameObject --> 3D Object --> Plane` で平面を作成し、名前を ``Ground`` にします。
#. Transform の :guilabel:`Position` を (0, 0, 0)、:guilabel:`Scale` を (2, 1, 2) にします。Plane は初期状態で 10 m 四方の大きさなので、20 m 四方の地面になります。
#. ``Assets/Materials`` フォルダーを右クリックし、:menuselection:`Create --> Material` でマテリアルを作成して、名前を ``GroundMaterial`` にします。:guilabel:`Base Map` の色を好きな色に設定し、``Ground`` にドラッグ＆ドロップします。

このゲームでは、ステージの周りに壁を置きません。ボールが地面の端から落ちるとゲームオーバーになります。

手順 3：プレイヤーの作成
------------------------

#. :menuselection:`GameObject --> 3D Object --> Sphere` で球を作成し、名前を ``Player`` にします。
#. Transform の :guilabel:`Position` を (0, 0.5, 0) にします。球の直径は 1 m なので、地面の上にちょうど乗ります。
#. Inspector ウィンドウの :guilabel:`Tag` で :guilabel:`Player` を選びます。``Pickup`` スクリプトは、このタグでプレイヤーを見分けます。
#. :guilabel:`Add Component` で Rigidbody を追加し、:guilabel:`Interpolate` を :guilabel:`Interpolate` にします。カメラが追従したときに、ボールの動きがなめらかに見えるようになります（:doc:`ch10_physics` を参照）。
#. ``PlayerController`` スクリプトを ``Player`` に付けます。
#. 手順 2 と同じようにマテリアルを作成して、``Player`` に設定します。

.. literalinclude:: ../../examples/chapter16/PlayerController.cs
   :caption: PlayerController.cs
   :linenos:

:download:`PlayerController.cs をダウンロード <../../examples/chapter16/PlayerController.cs>`

``PlayerController`` は、:doc:`ch09_input` で説明したプロジェクト全体のアクションから ``Move`` アクションを取得し、入力の値を ``Update`` で読み取ります。そして、``FixedUpdate`` で Rigidbody に力を加えます。``StopMoving`` は、ゲームクリアやゲームオーバーのときに ``GameManager`` から呼ばれ、ボールを止めて操作を受け付けないようにします。

ここで一度再生して、キーボードでボールが転がることを確認してください。ボールの転がる速さは、:guilabel:`Move Force` の値で調整できます。

手順 4：カメラの追従
--------------------

#. Hierarchy ウィンドウで ``Main Camera`` を選び、Transform の :guilabel:`Position` を (0, 10, -10)、:guilabel:`Rotation` を (45, 0, 0) にします。ステージを斜め上から見下ろす視点になります。
#. ``CameraFollow`` スクリプトを ``Main Camera`` に付け、:guilabel:`Target` に ``Player`` をドラッグ＆ドロップします。

.. literalinclude:: ../../examples/chapter16/CameraFollow.cs
   :caption: CameraFollow.cs
   :linenos:

:download:`CameraFollow.cs をダウンロード <../../examples/chapter16/CameraFollow.cs>`

``CameraFollow`` は、再生開始時のカメラとボールの位置の差を覚えておき、``LateUpdate`` でカメラの位置を「ボールの位置 + 位置の差」に更新します。ボールが転がって回転しても、カメラは回転せずに同じ向きで追いかけます。

.. tip::

   カメラの動きをもっと凝ったものにしたい場合は、:doc:`ch11_graphics` で紹介した Cinemachine を使うと、スクリプトを書かずに、なめらかな追従や、遅れて追いかける動きを設定できます。

手順 5：アイテムの作成
----------------------

#. :menuselection:`GameObject --> 3D Object --> Cube` で立方体を作成し、名前を ``Pickup`` にします。
#. Transform の :guilabel:`Position` を (3, 0.5, 3)、:guilabel:`Rotation` を (45, 45, 45)、:guilabel:`Scale` を (0.5, 0.5, 0.5) にします。
#. Box Collider の :guilabel:`Is Trigger` を有効にします。ボールがアイテムに触れても跳ね返らず、触れたことだけを検出するようになります。
#. ``Rotator`` スクリプトと ``Pickup`` スクリプトを付けます。
#. 黄色などの目立つ色のマテリアルを作成して設定します。

.. literalinclude:: ../../examples/chapter16/Rotator.cs
   :caption: Rotator.cs
   :linenos:

:download:`Rotator.cs をダウンロード <../../examples/chapter16/Rotator.cs>`

.. literalinclude:: ../../examples/chapter16/Pickup.cs
   :caption: Pickup.cs
   :linenos:

:download:`Pickup.cs をダウンロード <../../examples/chapter16/Pickup.cs>`

``Pickup`` は、トリガーに入った GameObject のタグが ``Player`` のときだけ処理を行います。``Pickup`` には Rigidbody を付けていませんが、ボールに Rigidbody が付いているため、トリガーイベントが呼ばれます（:doc:`ch10_physics` を参照）。

回収されたことは、``static`` なイベント ``Collected`` で通知します（:doc:`ch08_scripting_advanced` を参照）。``static`` なイベントは、どの ``Pickup`` が回収されても同じイベントとして通知されるため、``GameManager`` は ``Pickup`` を 1 つずつ参照しなくても、すべての ``Pickup`` の回収を受け取れます。

アイテムを Prefab にして並べる
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Hierarchy ウィンドウの ``Pickup`` を ``Assets/Prefabs`` フォルダーにドラッグ＆ドロップして、Prefab にします（:doc:`ch05_concepts` を参照）。
#. シーンの ``Pickup`` を選び、:kbd:`Ctrl` + :kbd:`D` で複製して、地面の上のさまざまな位置に配置します。8 個程度を目安にしてください。

アイテムの見た目や設定を変えたいときは、Prefab を編集すれば、すべてのアイテムに反映されます。

手順 6：エフェクトと効果音
--------------------------

#. :doc:`ch11_graphics` の「パーティクル」の手順で、火花のエフェクトの Prefab を作成し、``Assets/Prefabs`` フォルダーに保存します。:guilabel:`Stop Action` を :guilabel:`Destroy` にすることを忘れないでください。
#. アイテムを取ったときの効果音の音声ファイルを用意し、``Assets`` フォルダーにドラッグ＆ドロップして読み込みます。
#. ``Pickup`` の Prefab をダブルクリックして Prefab モードで開き、``Pickup`` コンポーネントの :guilabel:`Effect Prefab` にエフェクトの Prefab を、:guilabel:`Sound` に効果音の AudioClip を設定します。

エフェクトと効果音は省略することもできます。設定しない場合は、アイテムが消えるだけになります。効果音には、:doc:`ch13_audio` で説明した ``AudioSource.PlayClipAtPoint`` を使っています。アイテムの GameObject はすぐに破棄されるため、アイテム自身の AudioSource では最後まで再生できないからです。``PlayClipAtPoint`` の音は 3D サウンドになり、カメラから離れた位置で鳴らすと小さく聞こえます。そのため、再生する位置にはカメラの位置（``Camera.main.transform.position``）を指定しています。

手順 7：UI の作成
-----------------

:doc:`ch12_ui` の内容に従って、スコアとメッセージを表示する UI を作ります。

#. :menuselection:`GameObject --> UI --> Text - TextMeshPro` でテキストを作成し、名前を ``ScoreText`` にします。TMP Importer ウィンドウが表示された場合は、:guilabel:`Import TMP Essentials` をクリックします。
#. ``ScoreText`` の RectTransform のアンカーを、:kbd:`Shift` と :kbd:`Alt` を押しながら左上に設定し、位置を少し内側にずらします。
#. もう 1 つテキストを作成して名前を ``MessageText`` にし、アンカーを中央にします。:guilabel:`Font Size` を 72 程度にし、:guilabel:`Alignment` を中央ぞろえにします。
#. :menuselection:`GameObject --> UI --> Button - TextMeshPro` でボタンを作成し、名前を ``RetryButton`` にします。``MessageText`` の少し下に配置し、ボタンの子の Text (TMP) の文字を ``Retry`` にします。
#. Canvas の Canvas Scaler の :guilabel:`UI Scale Mode` を :guilabel:`Scale With Screen Size` にし、:guilabel:`Reference Resolution` を 1920 × 1080 にします。

TextMeshPro の既定のフォントは日本語を表示できないため、このゲームでは画面に表示する文字をすべて英語にしています。

手順 8：ゲームの管理
--------------------

#. :menuselection:`GameObject --> Create Empty` で空の GameObject を作成し、名前を ``GameManager`` にします。
#. ``GameManager`` スクリプトを付け、次の表のとおりにフィールドを設定します。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - フィールド
     - 設定する GameObject
   * - :guilabel:`Player`
     - ``Player``
   * - :guilabel:`Score Text`
     - ``ScoreText``
   * - :guilabel:`Message Text`
     - ``MessageText``
   * - :guilabel:`Retry Button`
     - ``RetryButton``

3. ``RetryButton`` を選び、Button コンポーネントの :guilabel:`On Click ()` の :guilabel:`+` をクリックします。追加された欄に ``GameManager`` の GameObject をドラッグ＆ドロップし、メソッドの一覧から :menuselection:`GameManager --> Retry ()` を選びます。

.. literalinclude:: ../../examples/chapter16/GameManager.cs
   :caption: GameManager.cs
   :linenos:

:download:`GameManager.cs をダウンロード <../../examples/chapter16/GameManager.cs>`

``GameManager`` の処理の流れは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - タイミング
     - 処理
   * - ``OnEnable``
     - ``Pickup.Collected`` イベントの購読を開始します。
   * - ``Start``
     - シーン内の ``Pickup`` の数を ``FindObjectsByType`` で数え、スコアを表示します。メッセージと :guilabel:`Retry` ボタンは非表示にします。
   * - ``Update``
     - ボールの高さが :guilabel:`Fall Threshold`\ （初期値は -10 m）より下になったら、ゲームオーバーにします。
   * - アイテムの回収時
     - スコアを 1 増やして表示を更新します。すべて集めたら、ゲームクリアにします。
   * - ゲームの終了時
     - ボールを止め、メッセージと :guilabel:`Retry` ボタンを表示します。
   * - :guilabel:`Retry` ボタンのクリック時
     - 現在のシーンを読み込み直して、最初からやり直します。
   * - ``OnDisable``
     - ``Pickup.Collected`` イベントの購読を解除します。シーンを読み込み直すときにも呼ばれます。

手順 9：動作の確認
------------------

シーンを保存し、再生して次のことを確認してください。

* ボールを転がして、アイテムに触れると消え、スコアが増える。
* すべてのアイテムを集めると「Clear!」と :guilabel:`Retry` ボタンが表示される。
* ボールを地面の端から落とすと「Game Over」と :guilabel:`Retry` ボタンが表示される。
* :guilabel:`Retry` ボタンをクリックすると、最初の状態に戻る。

うまく動かない場合は、Console ウィンドウにエラーが表示されていないかを確認してください。よくある原因は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 症状
     - 確認すること
   * - ボールが動かない
     - ``Player`` に Rigidbody と ``PlayerController`` が付いているか。Console ウィンドウに ``Player/Move`` が見つからないというエラーが出ていないか（:doc:`ch09_input` を参照）。
   * - アイテムに触れても消えない
     - ``Player`` のタグが :guilabel:`Player` になっているか。アイテムの Box Collider の :guilabel:`Is Trigger` が有効になっているか。
   * - ``NullReferenceException`` が発生する
     - ``GameManager`` や ``CameraFollow`` のフィールドがすべて設定されているか。
   * - :guilabel:`Retry` ボタンを押してもやり直せない
     - ``RollABall`` シーンが Scene List に登録されているか。シーンに EventSystem があるか。

発展課題
--------

基本のゲームが完成したら、次のような改造に挑戦してみてください。

* :doc:`ch09_input` を参考に、``Jump`` アクションでボールをジャンプさせる（``AddForce`` と ``ForceMode.Impulse`` を使います）。
* 制限時間を設け、時間内にすべて集められなかったらゲームオーバーにする。
* 地面の上に障害物や坂道を置き、ステージを複雑にする。
* :doc:`ch15_scenes_and_data` を参考に、クリアまでにかかった時間の最短記録を PlayerPrefs に保存する。
* ステージを複数のシーンに分け、クリアしたら次のステージに進むようにする。
