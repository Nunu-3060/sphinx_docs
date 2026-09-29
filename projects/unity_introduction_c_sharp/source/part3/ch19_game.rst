################################################################
第 19 章 簡単なゲームを作る
################################################################

この章では、これまでに学んだことを使って、ボールを転がしてアイテムを集めるゲームを作ります。

ゲームの仕様
================================================================

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 内容
   * - 目的
     - ボールを転がして、床の上に置かれたアイテムをすべて集めます。
   * - 操作
     - WASD キー、矢印キー、ゲームパッドの左スティックでボールを転がします。
   * - 表示
     - 画面の左上に、集めたアイテムの数と全体の数を表示します。
   * - クリア
     - すべてのアイテムを集めると「CLEAR!」と表示します。R キーを押すと最初からやり直します。
   * - やり直し
     - ボールが床から落ちると、最初からやり直します。

このゲームで使うスクリプトと、それぞれの役割は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - スクリプト
     - アタッチする GameObject
     - 役割
   * - ``PlayerController``
     - Player（ボール）
     - 入力に応じてボールに力を加えます。落下したらやり直します。
   * - ``CameraFollow``
     - Main Camera
     - ボールを追いかけます。
   * - ``Pickup``
     - アイテム
     - 回転し、ボールが触れたら取得されます。
   * - ``GameManager``
     - GameManager（空の GameObject）
     - 取得した数の管理、UI の表示、クリアの判定、やり直しを行います。

このように、1 つのスクリプトに 1 つの役割を持たせると、それぞれのスクリプトが短く、わかりやすくなります。

シーンの準備
================================================================

新しいシーンで作業する場合は、File > New Scene で Basic (URP) などのテンプレートを選んで作成し、File > Save で保存します。Universal 3D のテンプレートで作成したプロジェクトに最初からある SampleScene を使ってもかまいません。

床とボール
----------------------------------------------------------------

#. Hierarchy ウィンドウで右クリックし、3D Object > Plane を選びます。名前を Ground に変え、Transform の Position を (0, 0, 0)、Scale を (2, 1, 2) にします。これで 20 m × 20 m の床になります。
#. 同様に 3D Object > Sphere を選び、名前を Player に変えます。Position を (0, 0.5, 0) にします。
#. Player を選択した状態で、Inspector ウィンドウの Tag を Player にします。

アイテム
----------------------------------------------------------------

#. 3D Object > Cube を選び、名前を Pickup に変えます。Position を (3, 0.5, 3)、Rotation を (45, 45, 45)、Scale を (0.5, 0.5, 0.5) にします。
#. Inspector ウィンドウの Box Collider で、Is Trigger にチェックを入れます。
#. Hierarchy ウィンドウの Pickup を Project ウィンドウにドラッグして、プレハブにします。
#. Project ウィンドウの Pickup のプレハブをシーンにドラッグして、床の上に 8 個程度、配置します。

UI
----------------------------------------------------------------

#. Hierarchy ウィンドウで右クリックし、UI > Text - TextMeshPro を選びます（Unity のバージョンによっては UI (Canvas) > Text - TextMeshPro です）。初めて使うときは TMP Importer という画面が表示されるので、Import TMP Essentials ボタンを押します。Canvas と、その子として Text (TMP) が作られます。
#. Text (TMP) の名前を ScoreText に変えます。Rect Transform の左上にあるアンカーのプリセットのボタンを押し、Alt キー（macOS では Option キー）を押しながら top-left を選ぶと、画面の左上に配置されます。
#. 同様にもう 1 つ Text (TMP) を作り、名前を ClearMessage に変えます。表示する文字を「CLEAR! Press R to restart」にします。ClearMessage は、作成したときの位置（画面の中央）のままでかまいません。

.. note::

   TextMeshPro の標準のフォントには、日本語の文字が含まれていません。そのため、この章では表示する文字を英語にしています。日本語を表示するには、日本語のフォントからフォントアセットを作成する必要があります。

GameManager
----------------------------------------------------------------

#. Hierarchy ウィンドウで Create Empty を選び、名前を GameManager に変えます。

スクリプトの作成
================================================================

PlayerController
----------------------------------------------------------------

ボールを転がすスクリプトです。Player にアタッチします。``[RequireComponent(typeof(Rigidbody))]`` を付けているため、アタッチすると Rigidbody も自動で追加されます。

.. literalinclude:: ../../examples/ch19/PlayerController.cs
   :language: csharp
   :caption: PlayerController.cs

:download:`PlayerController.cs をダウンロード <../../examples/ch19/PlayerController.cs>`

第 14 章で説明した入力アクションの Move を使っています。入力は ``Update`` で読み取ってフィールドに保存し、``FixedUpdate`` で力を加えています（第 16 章）。

CameraFollow
----------------------------------------------------------------

カメラがボールを追いかけるスクリプトです。Main Camera にアタッチし、Target に Player を設定します。また、Main Camera の Position を (0, 10, -10)、Rotation を (45, 0, 0) にして、ボールを斜め上から見下ろすようにします。

.. literalinclude:: ../../examples/ch19/CameraFollow.cs
   :language: csharp
   :caption: CameraFollow.cs

:download:`CameraFollow.cs をダウンロード <../../examples/ch19/CameraFollow.cs>`

``Start`` で、カメラとボールの位置の差（オフセット）を記録しておき、毎フレーム「ボールの位置 + オフセット」にカメラを移動します。カメラを動かす処理を ``LateUpdate`` に書いているのは、ボールの移動がすべて終わった後にカメラを動かすためです（第 11 章）。

Pickup
----------------------------------------------------------------

アイテムのスクリプトです。Project ウィンドウの Pickup のプレハブを選び、Inspector ウィンドウでアタッチします。プレハブにアタッチすると、シーンに配置したすべての Pickup にスクリプトが追加されます。

.. literalinclude:: ../../examples/ch19/Pickup.cs
   :language: csharp
   :caption: Pickup.cs

:download:`Pickup.cs をダウンロード <../../examples/ch19/Pickup.cs>`

Pickup の Collider はトリガーで、Player は Rigidbody を持っているため、Player が触れると ``OnTriggerEnter`` が呼ばれます（第 16 章）。触れた相手が Player かどうかを ``CompareTag`` で確かめてから、``GameManager`` に取得したことを知らせ、自分自身を破棄します。

GameManager
----------------------------------------------------------------

ゲーム全体を管理するスクリプトです。GameManager にアタッチし、Score Text に ScoreText を、Clear Message に ClearMessage を、Hierarchy ウィンドウからドラッグして設定します。Score Text のフィールドの型は ``TextMeshProUGUI`` なので、ScoreText の GameObject をドラッグすると、その GameObject の TextMeshProUGUI コンポーネントが設定されます。

.. literalinclude:: ../../examples/ch19/GameManager.cs
   :language: csharp
   :caption: GameManager.cs

:download:`GameManager.cs をダウンロード <../../examples/ch19/GameManager.cs>`

``Start`` で使っている ``FindObjectsByType<Pickup>`` は、シーン内にある指定した型のコンポーネントをすべて探すメソッドです。シーン全体を調べるため処理に時間がかかりますが、``Start`` で 1 回だけ使うのであれば問題ありません（第 18 章）。

シングルトン
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pickup はプレハブなので、シーン内の GameManager への参照を Inspector ウィンドウで設定できません。プレハブのアセットは、特定のシーンのオブジェクトを参照できないためです。

そこで、``GameManager`` に ``static`` なプロパティ ``Instance`` を用意し、``Awake`` で自分自身を代入しています。こうすると、どのスクリプトからでも ``GameManager.Instance`` で ``GameManager`` を使えます。このように、1 つしか存在しないインスタンスをどこからでも使えるようにする設計を、シングルトンと呼びます。

シングルトンは便利ですが、多用すると、どのスクリプトがどのスクリプトに依存しているのかがわかりにくくなります。ゲーム全体を管理するクラスなど、本当に 1 つしか存在しないものに限って使ってください。

シーンの読み込み
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

やり直しは、``SceneManager.LoadScene`` で現在のシーンを読み込み直して実現しています。シーンを読み込み直すと、すべての GameObject が作り直され、取得したアイテムも元に戻ります。``SceneManager`` を使うには、``using UnityEngine.SceneManagement;`` を書きます。

.. note::

   ``SceneManager.LoadScene`` で読み込むシーンは、File > Build Profiles の Scene List に登録されている必要があります。新しく作ったシーンを使う場合は、Scene List に追加してください。

動作の確認
================================================================

Play ボタンを押して、次の点を確認してください。

* 移動のキーでボールが転がり、カメラがボールを追いかける。
* ボールがアイテムに触れると、アイテムが消えて、左上の数が増える。
* すべてのアイテムを集めると、CLEAR! と表示され、R キーで最初からやり直せる。
* ボールが床から落ちると、最初からやり直しになる。

うまく動かない場合は、次の点を確認してください。エラーの調べ方は、第 20 章で説明します。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - 症状
     - 確認すること
   * - ボールが動かない
     - Game ビューをクリックしたか。Player に PlayerController と Rigidbody がアタッチされているか。
   * - アイテムに触れても消えない
     - Pickup の Box Collider の Is Trigger にチェックが入っているか。Player の Tag が Player になっているか。
   * - ``UnassignedReferenceException`` が発生する
     - GameManager の Score Text と Clear Message、CameraFollow の Target が Inspector ウィンドウで設定されているか。
   * - 「Score: 0 / 0」と表示される
     - Pickup のプレハブに Pickup スクリプトがアタッチされているか。

発展課題
================================================================

余裕があれば、次のような改良に挑戦してみてください。

* 床の周りに Cube で壁を作り、ボールが落ちないようにする。
* 制限時間を設け、時間内にすべてのアイテムを集められなかったらゲームオーバーにする（``Time.deltaTime`` を使って残り時間を減らす）。
* アイテムを取得したときに効果音を鳴らす（``AudioSource`` コンポーネントを使う）。
* 取得したアイテムの数が変わったことをイベント（第 9 章）で知らせ、UI の更新を別のスクリプトに分ける。

まとめ
================================================================

* 1 つのスクリプトに 1 つの役割を持たせると、コードがわかりやすくなります。
* 入力は ``Update`` で読み取り、Rigidbody への力は ``FixedUpdate`` で加えます。
* カメラの追従は ``LateUpdate`` で行います。
* プレハブからシーン内のオブジェクトを使いたい場合は、シングルトンなどの方法を使います。
* ``SceneManager.LoadScene`` で、シーンを読み込み直せます。
