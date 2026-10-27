.. _ch09:

=============
第 9 章　入力
=============

本章では、キーボード、マウス、ゲームパッドからの入力を受け取る方法を説明する。Godot では、具体的なキーではなく「入力アクション」という抽象的な操作の名前を使って入力を扱うのが基本である。サンプルは ``chapter09`` フォルダーにある。

入力アクション
==============

ゲームの操作は、キーボードの矢印キーと WASD キー、ゲームパッドのスティックなど、複数の入力装置で同じことができるようにすることが多い。スクリプトの中で「矢印キーの左か、A キーか、スティックの左なら」と毎回書くのは面倒で、後から操作方法を変えるのも大変である。

そこで Godot では、「左へ移動」「ジャンプ」のような操作に名前を付けた入力アクション（input action）を定義し、そこに実際のキーやボタンを割り当てる。スクリプトはアクション名だけを使う。

.. graphviz::
   :caption: 入力アクションと実際の入力の対応

   digraph actions {
     rankdir=LR;
     node [shape=box, style="rounded,filled", fontsize=11];
     a [label="A キー", fillcolor="#f2f2f2"];
     left [label="← キー", fillcolor="#f2f2f2"];
     stick [label="左スティックを左に倒す", fillcolor="#f2f2f2"];
     space [label="スペースキー", fillcolor="#f2f2f2"];
     pad_a [label="ゲームパッドの A ボタン", fillcolor="#f2f2f2"];
     move_left [label="move_left", fillcolor="#cfe2ff"];
     jump [label="jump", fillcolor="#cfe2ff"];
     script [label="スクリプト\nInput.is_action_pressed(\"jump\")", fillcolor="#d4edda"];
     a -> move_left;
     left -> move_left;
     stick -> move_left;
     space -> jump;
     pad_a -> jump;
     move_left -> script;
     jump -> script;
   }

インプットマップで定義する
--------------------------

入力アクションは、「プロジェクト設定」の「インプットマップ」タブで定義する。

#. 上部の「新しいアクションの追加」欄にアクション名（例：``jump``）を入力し、「追加」を押す。
#. 追加されたアクションの右にある「+」ボタンを押すと、「イベントの設定」ダイアログが開く。
#. 割り当てたいキーを押すか、ゲームパッドのボタンを押す。入力が検出されたら「OK」を押す。

「組み込みアクションを表示」をオンにすると、Godot があらかじめ定義している ``ui_accept``\ （決定）、``ui_cancel``\ （キャンセル）、``ui_left`` などのアクションが表示される。これらは UI の操作に使われるもので、自分のゲームの操作には独自のアクションを定義するとよい。

本書のサンプルプロジェクトでは、次のアクションを定義している。

.. list-table:: サンプルプロジェクトの入力アクション
   :header-rows: 1
   :widths: 25 45 30

   * - アクション名
     - キーボード
     - ゲームパッド
   * - ``move_left``
     - :kbd:`A`、:kbd:`←`
     - 左スティック（左）
   * - ``move_right``
     - :kbd:`D`、:kbd:`→`
     - 左スティック（右）
   * - ``move_up``
     - :kbd:`W`、:kbd:`↑`
     - 左スティック（上）
   * - ``move_down``
     - :kbd:`S`、:kbd:`↓`
     - 左スティック（下）
   * - ``jump``
     - :kbd:`Space`
     - A ボタン（下側のボタン）
   * - ``pause``
     - :kbd:`P`
     - スタートボタン
   * - ``back_to_launcher``
     - :kbd:`Esc`
     - なし

インプットマップの内容は ``project.godot`` の ``[input]`` セクションに保存される。

物理キーコード
--------------

キーを割り当てるとき、「イベントの設定」ダイアログでは、キーの指定方法を「物理キーコード」「キーコード」「キーラベル」から選べる。

* **物理キーコード**：キーボード上のキーの位置で判定する。US 配列で W の位置にあるキーは、フランス語の AZERTY 配列では Z だが、どちらも同じキーとして扱われる。WASD のように位置に意味がある操作に向く。
* **キーコード**：キーボードの配列に応じた、キーの意味で判定する。

本書のサンプルでは、すべて物理キーコードで割り当てている。

入力を受け取る 2 つの方法
=========================

スクリプトで入力を受け取る方法には、ポーリングとイベントの 2 種類がある。

ポーリング
----------

ポーリング（polling）は、``_process()`` や ``_physics_process()`` の中で、毎フレーム「今アクションが押されているか」を問い合わせる方法である。押している間ずっと続く操作（移動など）に向く。

.. list-table:: Input の主なメソッド
   :header-rows: 1
   :widths: 45 55

   * - メソッド
     - 戻り値
   * - ``Input.is_action_pressed("jump")``
     - 押されている間 ``true``
   * - ``Input.is_action_just_pressed("jump")``
     - 押された瞬間のフレームだけ ``true``
   * - ``Input.is_action_just_released("jump")``
     - 離された瞬間のフレームだけ ``true``
   * - ``Input.get_action_strength("move_right")``
     - 押し込みの強さ（0.0 ～ 1.0）。キーなら 0 か 1、スティックなら倒した量
   * - ``Input.get_axis("move_left", "move_right")``
     - 2 つのアクションから -1.0 ～ 1.0 の値を作る。左右移動に便利
   * - ``Input.get_vector("move_left", "move_right", "move_up", "move_down")``
     - 4 つのアクションから、長さが 1 以下の ``Vector2`` を作る。上下左右の移動に便利

``get_vector()`` は、斜めに入力したときにベクトルの長さが 1 を超えないように調整する。単純に左右と上下の値を組み合わせると、斜め移動のときだけ約 1.41 倍速くなってしまうが、``get_vector()`` を使えばその問題は起きない。

イベント
--------

イベント（event）は、入力が発生したときに Godot から呼び出してもらう方法である。キーを押した、マウスをクリックした、といった 1 回きりの出来事に向く。

イベントは、``_input(event)`` や ``_unhandled_input(event)`` で受け取る。引数の ``event`` は ``InputEvent`` を継承したクラスのインスタンスで、入力の種類に応じて次のクラスが使われる。

.. list-table:: 主な InputEvent のクラス
   :header-rows: 1
   :widths: 40 60

   * - クラス
     - 入力の種類
   * - ``InputEventKey``
     - キーボードのキー
   * - ``InputEventMouseButton``
     - マウスのボタン、ホイール
   * - ``InputEventMouseMotion``
     - マウスの移動
   * - ``InputEventJoypadButton``
     - ゲームパッドのボタン
   * - ``InputEventJoypadMotion``
     - ゲームパッドのスティック、トリガー
   * - ``InputEventScreenTouch``
     - タッチパネルへのタッチ

アクションかどうかは、``event.is_action_pressed("jump")`` で判定する。種類ごとの情報（クリックした位置など）が必要な場合は、``event is InputEventMouseButton`` のように型を確認してから使う。

サンプル
========

``input_demo.tscn`` は、ポーリングで上下左右に移動し、イベントでジャンプの回数を数え、クリックした位置へ瞬間移動するサンプルである。

.. literalinclude:: ../../examples/chapter09/input_demo.gd
   :tab-width: 4
   :language: gdscript
   :linenos:
   :caption: chapter09/input_demo.gd

``_process()`` では ``get_vector()`` で方向を取得し、速さと ``delta`` を掛けて移動している。``_unhandled_input()`` では、``jump`` アクションが押されたときに回数を数えている。

ジャンプのように「押した瞬間」に反応させたい処理は、ポーリングで ``is_action_just_pressed()`` を使っても、イベントで ``is_action_pressed()`` を使っても書ける。キャラクターの物理的な動きと一緒に処理するならポーリング（:ref:`ch11` の例）、メニューを開くなどの独立した操作ならイベント、と使い分けるとよい。

入力イベントが伝わる順番
========================

入力イベントは、次の順番でノードに渡される。どこかで「処理済み」とされると、それ以降には渡されない。

.. graphviz::
   :caption: 入力イベントが伝わる順番

   digraph propagation {
     rankdir=LR;
     node [shape=box, style="rounded,filled", fillcolor="#e8f0fe", fontsize=11];
     i [label="_input()"];
     g [label="UI（Control）の\n_gui_input()"];
     s [label="_shortcut_input()"];
     k [label="_unhandled_key_input()"];
     u [label="_unhandled_input()"];
     i -> g -> s -> k -> u;
   }

ボタンやテキストボックスなどの UI は、途中の ``_gui_input()`` でイベントを受け取り、処理済みにする。例えば、テキストボックスに文字を入力している間にスペースキーを押しても、ゲームのキャラクターがジャンプしてはいけない。ゲームの操作を ``_unhandled_input()`` で受け取るようにしておけば、UI が使った入力は届かないので、この問題を避けられる。

自分でイベントを処理済みにするには、``get_viewport().set_input_as_handled()`` を呼ぶ。``input_demo.gd`` の 24 行目がその例である。

.. tip::

   ゲームの操作は ``_unhandled_input()`` で受け取るのが基本である。``_input()`` は、UI より先に必ず受け取る必要がある場合（デバッグ用のキーなど）に使う。

マウスの位置
============

マウスの位置には、2 種類の座標がある。

* ``InputEventMouse`` の ``position``：ゲームのウィンドウ（ビューポート）上の座標。左上が (0, 0) である。
* ``get_global_mouse_position()``：ゲームの世界での座標。``Camera2D`` で画面がスクロールしている場合は、ビューポート上の座標とずれる。

ゲームの世界にある物体とマウスの位置を比べる場合は、``get_global_mouse_position()`` を使う。:ref:`ch10` のサンプルで使っている。
