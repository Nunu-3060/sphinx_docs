################################################################
第 14 章 入力処理
################################################################

この章では、キーボード、マウス、ゲームパッドからの入力を読み取る方法を学びます。本書では、Unity 6 で標準的に使われる Input System パッケージを使います。

Input System の準備
================================================================

Unity 6 のテンプレートから作成したプロジェクトには、Input System パッケージが最初から導入されています。Edit > Project Settings > Player の Other Settings にある Active Input Handling が、Input System Package (New) または Both になっていることを確認してください。

Input System のクラスを使うには、ファイルの先頭に次の 1 行を書きます。

.. code-block:: csharp

   using UnityEngine.InputSystem;

.. note::

   古い Unity の解説では、``Input.GetKey`` などを使う Input Manager という仕組みが使われていることがあります。Active Input Handling が Input System Package (New) の場合、Input Manager の機能を使うと例外が発生します。本書では Input Manager は扱いません。

Input System で入力を読み取る方法には、主に次の 2 つがあります。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 方法
     - 特徴
     - 向いている場面
   * - デバイスを直接読み取る
     - 「スペースキー」のように、特定のキーやボタンを直接指定します。
     - 試作、デバッグ用の操作
   * - 入力アクションを使う
     - 「ジャンプ」のような操作の意味を定義し、キーやボタンを割り当てます。
     - ゲームの操作全般

デバイスを直接読み取る
================================================================

``Keyboard.current`` で現在のキーボードを、``Mouse.current`` で現在のマウスを取得できます。デバイスが接続されていない場合は ``null`` になるため、使う前に確認します。

キーやボタンの状態は、次のプロパティで調べます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - プロパティ
     - ``true`` になるとき
   * - ``isPressed``
     - 押されている間ずっと
   * - ``wasPressedThisFrame``
     - 押されたフレームだけ
   * - ``wasReleasedThisFrame``
     - 離されたフレームだけ

たとえば、スペースキーは ``Keyboard.current.spaceKey``、A キーは ``Keyboard.current.aKey``、マウスの左ボタンは ``Mouse.current.leftButton`` で表します。

.. literalinclude:: ../../examples/ch14/KeyboardInputSample.cs
   :language: csharp
   :caption: KeyboardInputSample.cs

:download:`KeyboardInputSample.cs をダウンロード <../../examples/ch14/KeyboardInputSample.cs>`

.. note::

   Play モード中に入力が反応しない場合は、Game ビューをクリックしてください。キーボードの入力は、Game ビューが選択されているときにだけゲームに送られます。

入力アクションを使う
================================================================

入力アクションとは
----------------------------------------------------------------

デバイスを直接読み取る方法では、「WASD キーでも矢印キーでもゲームパッドのスティックでも移動できるようにする」といった処理を書くのが大変です。また、後からキーの割り当てを変えるには、コードを書き換える必要があります。

入力アクションを使うと、「移動（Move）」や「ジャンプ（Jump）」のような操作を定義し、それぞれにキーやボタンを割り当てられます。スクリプトは「ジャンプの入力があったか」だけを調べればよく、どのキーが押されたかを知る必要がありません。

プロジェクト全体の入力アクション
----------------------------------------------------------------

Unity 6 のプロジェクトには、よく使う入力アクションが最初から用意されています。Edit > Project Settings > Input System Package を開くと、設定されている入力アクションを確認・編集できます。主な入力アクションは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 20 25 55

   * - 名前
     - 種類
     - 主な割り当て
   * - Move
     - 値（``Vector2``）
     - WASD キー、矢印キー、ゲームパッドの左スティック
   * - Look
     - 値（``Vector2``）
     - マウスの移動、ゲームパッドの右スティック
   * - Jump
     - ボタン
     - スペースキー、ゲームパッドの右側の 4 つのボタンのうち下のボタン
   * - Attack
     - ボタン
     - マウスの左ボタン、ゲームパッドの右側の 4 つのボタンのうち左のボタン

スクリプトからは、``InputSystem.actions.FindAction("Move")`` のように、名前を指定して入力アクションを取得します。取得した入力アクションは、次のメソッドで読み取ります。

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - メソッド
     - 説明
   * - ``ReadValue<Vector2>()``
     - 現在の値を読み取ります。Move の場合、左右の入力が ``x``\ （-1 から 1）、上下の入力が ``y``\ （-1 から 1）に入ります。
   * - ``IsPressed()``
     - ボタンが押されている間 ``true`` を返します。
   * - ``WasPressedThisFrame()``
     - ボタンが押されたフレームだけ ``true`` を返します。
   * - ``WasReleasedThisFrame()``
     - ボタンが離されたフレームだけ ``true`` を返します。

``FindAction`` は、指定した名前の入力アクションが見つからないと ``null`` を返します。名前のつづりに注意してください。

.. literalinclude:: ../../examples/ch14/ActionInputSample.cs
   :language: csharp
   :caption: ActionInputSample.cs

:download:`ActionInputSample.cs をダウンロード <../../examples/ch14/ActionInputSample.cs>`

入力の値の ``y`` を、3 次元空間の ``z`` に割り当てている点に注意してください。Unity の 3D 空間では Y 軸が上方向なので、地面の上を前後に移動するには Z 方向に動かします。

.. note::

   Move の入力アクションでは、キーボードで斜めに入力したときに、``Vector2`` の長さが 1 になるように調整されています。そのため、斜め方向に移動しても速くなりすぎません。

入力を読み取る場所
================================================================

入力は、``Update`` の中で読み取ります。``wasPressedThisFrame`` や ``WasPressedThisFrame()`` は、押されたフレームだけ ``true`` になります。``FixedUpdate`` はフレームごとに呼ばれるとは限らないため、``FixedUpdate`` の中で調べると、押された瞬間を取りこぼすことがあります。物理演算を使って動かす場合の書き方は、第 16 章で説明します。

まとめ
================================================================

* Input System を使うには、``using UnityEngine.InputSystem;`` を書きます。
* ``Keyboard.current`` や ``Mouse.current`` を使うと、デバイスを直接読み取れます。
* ゲームの操作には、入力アクションを使います。``InputSystem.actions.FindAction`` で取得し、``ReadValue`` や ``WasPressedThisFrame`` で読み取ります。
* 入力は ``Update`` の中で読み取ります。
