第 9 章 入力
============

この章では、キーボード、マウス、ゲームパッドからの入力を受け取る方法を説明します。

この章のサンプルコードは、``examples/chapter09`` フォルダーにあります。

Input System とは
-----------------

Unity には、入力を扱うしくみが 2 つあります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - しくみ
     - 特徴
   * - Input System パッケージ
     - 現在推奨されているしくみです。キーボード、マウス、ゲームパッド、タッチなどの入力を、「移動」「ジャンプ」のような **アクション** として抽象化して扱えます。キーの割り当ての変更や、複数のデバイスへの対応が容易です。
   * - Input Manager（旧方式）
     - 以前から使われているしくみです。``Input.GetKeyDown(KeyCode.Space)`` のように、キーやボタンを直接指定して入力を読み取ります。古い資料やサンプルで多く使われています。

Unity 6 のテンプレートで作成したプロジェクトでは、Input System パッケージが最初からインストールされ、有効になっています。本資料では Input System を使います。

どちらのしくみを使うかは、:menuselection:`Edit --> Project Settings` の :guilabel:`Player` の :guilabel:`Other Settings` にある :guilabel:`Active Input Handling` で設定します。:guilabel:`Input System Package (New)` が選ばれている状態で ``Input.GetKeyDown`` などの旧方式のコードを実行すると、``InvalidOperationException`` が発生します。古い資料のコードを動かす場合は、Input System の書き方に置き換えるか、:guilabel:`Both` を選んで両方を有効にしてください。

Input Actions
-------------

アクションとバインディング
~~~~~~~~~~~~~~~~~~~~~~~~~~

Input System では、ゲームの操作を次の 3 つの階層で管理します。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 階層
     - 意味
   * - Action Map
     - アクションのまとまりです。例えば、キャラクターの操作用の ``Player`` と、メニュー画面の操作用の ``UI`` のように、場面ごとに分けます。
   * - Action
     - 「移動する」「ジャンプする」など、ゲームの中での操作の意味です。
   * - Binding
     - アクションに割り当てる実際の入力です。例えば、``Jump`` アクションにキーボードのスペースキーとゲームパッドの下側のボタンを割り当てます。

スクリプトは、「スペースキーが押されたか」ではなく「``Jump`` アクションが実行されたか」を調べます。そのため、キーの割り当てを変えたり、ゲームパッドに対応したりするときに、スクリプトを変更する必要がありません。

プロジェクト全体のアクション
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unity 6 のテンプレートで作成したプロジェクトには、``Assets`` フォルダーに ``InputSystem_Actions`` というアセットが用意されています。このアセットは **プロジェクト全体のアクション**\ （Project-wide Actions）として登録されており、次のようなアクションが定義されています。

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Action Map
     - Action
     - 主なバインディング
   * - Player
     - Move
     - :kbd:`W`、:kbd:`A`、:kbd:`S`、:kbd:`D` キー、矢印キー、ゲームパッドの左スティック
   * - Player
     - Look
     - マウスの移動、ゲームパッドの右スティック
   * - Player
     - Jump
     - スペースキー、ゲームパッドの下側のボタン
   * - Player
     - Attack
     - マウスの左ボタン、ゲームパッドの左側のボタン
   * - UI
     - Navigate、Submit など
     - UI の操作用のバインディング

アセットをダブルクリックすると、アクションとバインディングを編集するウィンドウが開きます。プロジェクト全体のアクションとして使うアセットは、:menuselection:`Edit --> Project Settings` の :guilabel:`Input System Package` で確認、変更できます。

アクションを使った入力の読み取り
--------------------------------

``InputActionReference`` を使う方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

スクリプトでアクションを使う方法の 1 つは、Inspector ウィンドウで使うアクションを指定する方法です。

.. literalinclude:: ../../examples/chapter09/InputActionMover.cs
   :caption: InputActionMover.cs
   :linenos:

:download:`InputActionMover.cs をダウンロード <../../examples/chapter09/InputActionMover.cs>`

使い方は次のとおりです。

#. Cube などの GameObject に ``InputActionMover`` スクリプトを付けます。
#. Inspector ウィンドウの :guilabel:`Move Action` の右にある ◎ をクリックし、:guilabel:`Player/Move` を選びます。
#. 同じように、:guilabel:`Jump Action` に :guilabel:`Player/Jump` を設定します。
#. 再生して :kbd:`W`、:kbd:`A`、:kbd:`S`、:kbd:`D` キーを押すと GameObject が移動し、スペースキーを押すと Console ウィンドウにメッセージが表示されます。

アクションの値の読み取り方には、次の 2 種類があります。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 方法
     - 特徴
   * - ``ReadValue<T>()``
     - 現在の値を読み取ります。``Update`` で毎フレーム呼び出して使います。移動のように、押している間ずっと続く入力に向いています。
   * - ``performed`` イベント
     - アクションが実行されたときに、登録したメソッドが呼ばれます。ジャンプのように、押した瞬間だけ処理する入力に向いています。

名前でアクションを取得する方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

プロジェクト全体のアクションは、``InputSystem.actions`` から名前で取得することもできます。Inspector ウィンドウでの設定が不要になるため、:doc:`ch16_tutorial` ではこの方法を使います。

.. code-block:: csharp

   // Awake などで 1 回だけ取得して、フィールドに保持しておきます。
   _moveAction = InputSystem.actions.FindAction("Player/Move", throwIfNotFound: true);
   _jumpAction = InputSystem.actions.FindAction("Player/Jump", throwIfNotFound: true);

   // Update で読み取ります。
   Vector2 move = _moveAction.ReadValue<Vector2>();
   if (_jumpAction.WasPressedThisFrame())
   {
       // ジャンプの処理
   }

``WasPressedThisFrame`` は、そのフレームでボタンが押されたときだけ ``true`` を返します。``FindAction`` の引数 ``throwIfNotFound`` に ``true`` を指定すると、アクションの名前を間違えたときに、すぐに例外が発生して原因に気付けます。

デバイスを直接読み取る
----------------------

動作確認用の簡単な処理であれば、アクションを使わずに、デバイスの状態を直接読み取ることもできます。

.. literalinclude:: ../../examples/chapter09/DeviceInputExample.cs
   :caption: DeviceInputExample.cs
   :linenos:

:download:`DeviceInputExample.cs をダウンロード <../../examples/chapter09/DeviceInputExample.cs>`

``Keyboard.current``、``Mouse.current``、``Gamepad.current`` は、最後に使われたデバイスを返します。デバイスが接続されていない場合は ``null`` になるので、必ず確認してから使います。

この方法は手軽ですが、キーの割り当てがコードに直接書かれるため、割り当ての変更や他のデバイスへの対応が難しくなります。ゲームの操作には Input Actions を使ってください。

旧方式との対応
--------------

古い資料のコードを Input System の書き方に置き換えるときは、次の表を参考にしてください。

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Input Manager（旧方式）
     - Input System
   * - ``Input.GetKeyDown(KeyCode.Space)``
     - ``Keyboard.current.spaceKey.wasPressedThisFrame``
   * - ``Input.GetKey(KeyCode.Space)``
     - ``Keyboard.current.spaceKey.isPressed``
   * - ``Input.GetMouseButtonDown(0)``
     - ``Mouse.current.leftButton.wasPressedThisFrame``
   * - ``Input.mousePosition``
     - ``Mouse.current.position.ReadValue()``
   * - ``Input.GetAxis("Horizontal")`` と ``Input.GetAxis("Vertical")``
     - ``Move`` アクションの ``ReadValue<Vector2>()``
