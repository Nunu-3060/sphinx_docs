.. _ch07:

========================
第 7 章　GDScript の応用
========================

本章では、Godot のスクリプトで特に重要なシグナルと ``await`` を中心に、列挙型、関数オブジェクト、静的型付けの活用、エラーの扱い方を説明する。最後に、Python の経験者がつまずきやすい点をまとめる。サンプルは ``chapter07`` フォルダーにある。

シグナル
========

シグナル（signal）は、ノードが「何かが起きた」ことをほかのノードに知らせる仕組みである。デザインパターンのオブザーバーパターンや、GUI プログラミングのイベントに相当する。

例えば、ボタンは押されたときに ``pressed`` シグナルを発行（emit）する。ボタンを押したときの処理を書きたいノードは、このシグナルに自分の関数を接続（connect）しておく。すると、ボタンが押されるたびにその関数が呼ばれる。ボタンの側は、誰が接続しているかを知らなくてよい。

Godot のノードには、多くのシグナルがあらかじめ定義されている。

.. list-table:: よく使う組み込みのシグナル
   :header-rows: 1
   :widths: 40 60

   * - シグナル
     - 発行されるタイミング
   * - ``Button.pressed``
     - ボタンが押されたとき
   * - ``Timer.timeout``
     - タイマーが設定時間に達したとき
   * - ``Area2D.body_entered(body)``
     - 物理的な物体が領域に入ったとき
   * - ``AnimationPlayer.animation_finished(anim_name)``
     - アニメーションの再生が終わったとき
   * - ``Node.tree_exited``
     - ノードがシーンツリーから取り除かれたとき

エディターでシグナルを接続する
------------------------------

:ref:`ch05` の ``coin.tscn`` では、``Area2D`` の ``body_entered`` シグナルを、エディターで ``coin.gd`` の ``_on_body_entered()`` に接続している。手順は次のとおりである。

#. シーンドックで ``Coin`` ノードを選び、インスペクターの右にある「シグナル」ドックを開く。
#. シグナルの一覧から ``body_entered(body: Node2D)`` をダブルクリックする。
#. 「メソッドにシグナルを接続」ダイアログで、接続先のノード（ここでは ``Coin`` 自身）を選び、「接続」を押す。

スクリプトに ``_on_body_entered(body: Node2D)`` という関数がなければ、自動で作られる。接続の情報はシーンファイルの ``[connection]`` に保存される。接続されている関数の行には、スクリプトエディターの左端に緑色のアイコンが表示される。

独自のシグナルを定義して使う
----------------------------

シグナルは自分で定義することもできる。次の ``Health`` は、体力を管理するだけのノードである。体力が変化したときと 0 になったときに、シグナルを発行する。

.. literalinclude:: ../../examples/chapter07/health.gd
   :tab-width: 4
   :language: gdscript
   :linenos:
   :caption: chapter07/health.gd

シグナルは ``signal 名前(引数)`` で定義し、``名前.emit(引数)`` で発行する。``Health`` は、誰が体力の変化に関心を持っているかを知らない。体力の表示を更新するのか、効果音を鳴らすのか、ゲームオーバーにするのかは、シグナルを受け取る側が決める。こうしておくと、``Health`` をプレイヤーにも敵にも使い回せる。

``Health`` を使う側のスクリプトは次のとおりである。体力をプログレスバーで表示し、ボタンでダメージと回復を与える。

.. literalinclude:: ../../examples/chapter07/signal_demo.gd
   :tab-width: 4
   :language: gdscript
   :linenos:
   :caption: chapter07/signal_demo.gd

18 行目と 19 行目で、``Health`` のシグナルをコードで接続している。``connect()`` には、呼び出してほしい関数を渡す。``_on_health_changed`` のように括弧を付けずに関数名を書くと、関数を呼び出すのではなく、関数そのものを表す値（``Callable``）になる。

.. graphviz::
   :caption: signal_demo.tscn でのシグナルの流れ

   digraph signals {
     rankdir=LR;
     node [shape=box, style="rounded,filled", fillcolor="#e8f0fe", fontsize=11];
     edge [fontsize=10];
     button [label="DamageButton\n（Button）"];
     demo [label="SignalDemo\n（signal_demo.gd）"];
     health [label="Health\n（health.gd）"];
     bar [label="HealthBar と\nStatusLabel"];
     button -> demo [label="pressed"];
     demo -> health [label="take_damage(30)\nを呼ぶ", style=dashed];
     health -> demo [label="health_changed\ndied"];
     demo -> bar [label="表示を更新", style=dashed];
   }

図の実線はシグナル、破線はメソッドの呼び出しである。親（``SignalDemo``）は子（``Health``）のメソッドを直接呼び、子は親にシグナルで知らせている。:ref:`ch05` で説明した「呼び出しは下へ、通知は上へ」の形になっている。

.. figure:: ../images/screenshots/ch07_signal.png
   :class: screenshot
   :width: 70%

   signal_demo.tscn の実行結果

関数を値として扱う
==================

GDScript では、関数を ``Callable`` という型の値として変数に入れたり、引数として渡したりできる。

ラムダ式
--------

``func(引数) -> 戻り値の型: 処理`` の形で、名前のない関数（ラムダ式）を書ける。``signal_demo.gd`` の 21 行目と 22 行目では、ボタンの ``pressed`` シグナルにラムダ式を接続している。1 行で書ける短い処理を、わざわざ別の関数として定義せずに済む。

ラムダ式は複数行にもできる。その場合は、通常の関数と同じようにインデントして本体を書く。

.. code-block:: gdscript
   :linenos:

   var doubled := [1, 2, 3].map(func(v: int) -> int: return v * 2)  # [2, 4, 6]

   button.pressed.connect(func() -> void:
       print("押された")
       score += 1
   )

ラムダ式は、作られた時点のローカル変数の値を取り込む。取り込んだ後に元の変数へ別の値を代入しても、ラムダ式の中の値は変わらない。この点は Python のクロージャー（変数そのものを参照する）と異なる。ただし、配列や辞書のように参照で扱われる値は、中身の変更が共有される。

引数を追加する bind()
---------------------

``Callable`` の ``bind()`` を使うと、呼び出し時に渡す引数を追加できる。同じ関数を複数のシグナルに接続し、どこから呼ばれたかを引数で区別したい場合に便利である。:ref:`ch14` のサンプルでは、3 つのボタンを 1 つの関数に接続し、鳴らす音を ``bind()`` で渡している。

.. code-block:: gdscript
   :linenos:

   %JumpButton.pressed.connect(_play_se.bind(preload("res://assets/jump.wav")))
   %CoinButton.pressed.connect(_play_se.bind(preload("res://assets/coin.wav")))

await
=====

``await`` は、シグナルが発行されるまで関数の実行を一時停止する。``signal_demo.gd`` の ``_on_died()`` は、倒れたことを表示してから 2 秒待ち、体力を回復する。

.. code-block:: gdscript
   :linenos:

   await get_tree().create_timer(RESPAWN_SECONDS).timeout

``get_tree().create_timer()`` は、指定した秒数が過ぎると ``timeout`` シグナルを発行する使い捨てのタイマーを作る。``await`` はこのシグナルを待つ。

``await`` で一時停止している間も、ゲームは止まらない。``_on_died()`` を呼び出した側には、``await`` の時点で制御が戻る。2 秒後にシグナルが発行されると、``await`` の次の行から実行が再開される。Python の ``async`` と ``await`` に似ているが、GDScript では関数に ``async`` を付ける必要はない。

``await`` を使うと、時間の経過を伴う一連の処理（演出、チュートリアルの進行、敵の行動パターンなど）を上から順に書ける。ただし、待っている間にノードが削除されると、再開されない。また、同じ関数が待っている間に再び呼ばれると、複数の実行が同時に進行する。こうした状況が起こりうる場合は、状態を表す変数を確認するなどの対策が必要になる。

列挙型
======

``enum`` で列挙型を定義できる。``signal_demo.gd`` では、キャラクターの状態を ``State`` として定義している。

.. code-block:: gdscript
   :linenos:

   enum State { ALIVE, DEAD }

   var state: State = State.ALIVE

列挙型の値の実体は整数で、先頭から 0、1、2 と番号が振られる。``State.keys()`` で名前の配列を取得できるので、デバッグ時に ``State.keys()[state]`` で名前を表示できる。変数の型を ``State`` にすると、エディターが補完で候補を示してくれる。``@export var state: State`` とすれば、インスペクターにドロップダウンとして表示される。

セッターとゲッター
==================

変数への代入や参照のときに処理を挟みたい場合は、セッター（``set``）とゲッター（``get``）を定義する。Python のプロパティ（``@property``）に相当する。

.. code-block:: gdscript
   :linenos:
   :caption: 値が変わるたびにシグナルを発行する変数（chapter15/game_state.gd より）

   signal score_changed(score: int)

   var score: int = 0:
       set(value):
           score = value
           score_changed.emit(score)

``score = 10`` や ``score += 5`` と書くと、セッターが呼ばれてシグナルが発行される。セッターの中で ``score`` に代入しても、セッターは再帰的には呼ばれない。

継承と super
============

スクリプトは、別のスクリプトを継承できる。``extends`` には、組み込みのクラス名のほか、``class_name`` で登録したクラス名や、スクリプトのパスを書ける。

.. code-block:: gdscript
   :linenos:

   class_name Boss
   extends Enemy  # class_name Enemy を付けたスクリプトを継承する


   func take_damage(amount: int) -> void:
       super(maxi(amount - 5, 0))  # ダメージを 5 減らして、親クラスの take_damage() を呼ぶ

親クラスの同じ名前の関数を呼ぶには ``super()`` を使う。親クラスの別の関数は ``super.関数名()`` で呼べる。

``_ready()`` などのライフサイクル関数は、親クラスと子クラスの両方に定義されていても、子クラスのものだけが呼ばれる。親クラスの処理も必要なら、子クラスの関数の中で ``super()`` を呼ぶ。

ただし、:ref:`ch05` で述べたとおり、Godot では継承を深くするよりも、ノードの組み合わせで機能を作るほうが扱いやすいことが多い。

静的型付けを活用する
====================

:ref:`ch06` で説明したように、GDScript では型を省略できるが、型を書くことでエディターがより多くの誤りを見つけてくれる。

型の指定漏れを警告する
----------------------

プロジェクト設定で、型を指定していない宣言を警告にできる。「プロジェクト設定」の右上にある「高度な設定」をオンにし、「デバッグ」→「GDScript」の「Untyped Declaration」を「Warn」にする（この項目名は日本語に翻訳されていない）。本書のサンプルプロジェクトでは、この設定を有効にしている。

型が確定している行は、スクリプトエディターの行番号が緑色で表示される。型が分からないまま実行される行は、行番号が灰色のままになる。

型の変換と判定
--------------

``$`` や ``get_node()`` で取得したノードは、型が ``Node`` として扱われる。具体的な型として使うには、型を指定した変数に代入するか、``as`` で変換する。

.. code-block:: gdscript
   :linenos:

   @onready var bar: ProgressBar = %HealthBar   # 型を指定した変数に代入する

   var body := collision.get_collider() as RigidBody2D   # as で変換する
   if body != null:   # 変換できなかった場合は null になる
       body.apply_central_impulse(Vector2.UP * 100.0)

   if node is CharacterBody2D:   # is で型を判定する
       print("キャラクターである")

``as`` は、変換できない場合にエラーにはならず ``null`` を返す。``is`` は、継承元のクラスも含めて型が一致するかを調べる。Python の ``isinstance()`` に相当する。

エラーの扱い
============

GDScript には例外（``try``、``except``）がない。失敗する可能性のある処理は、成功したかどうかを戻り値で知らせる。

.. code-block:: gdscript
   :linenos:

   var config := ConfigFile.new()
   var error := config.load("user://settings.cfg")
   if error != OK:
       push_error("設定を読み込めない: %s" % error_string(error))
       return

``Error`` 型の戻り値は、成功なら ``OK``、失敗なら ``ERR_FILE_NOT_FOUND`` などのエラーコードである。``error_string()`` でエラーコードを説明文に変換できる。オブジェクトを返す関数は、失敗すると ``null`` を返すことが多い。

実行中に致命的な誤り（``null`` のメソッド呼び出しなど）が起きると、エディターから実行している場合はゲームが一時停止し、スクリプトエディターにエラーの行が表示される。エクスポートしたゲームでは、エラーを出力したうえで、その関数の残りの処理を飛ばして実行を続ける。エラー処理については :ref:`ch18` でも説明する。

Python の経験者がつまずきやすい点
=================================

最後に、Python に慣れた人が GDScript で間違えやすい点をまとめる。

.. list-table:: Python と GDScript の違いで注意する点
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 注意する点
   * - 変数の宣言
     - 初めて使う変数には ``var`` が必要。``var`` を付け忘れると、未定義の変数としてエラーになる。
   * - ``print()``
     - 複数の引数を区切り文字なしで連結して出力する。``print("a", 1)`` は ``a1`` になる。空白で区切りたい場合は ``prints()`` を使う。
   * - 文字列の連結
     - ``"点数: " + 10`` はエラーになる。``"点数: " + str(10)`` のように変換するか、``%`` で書式指定する。
   * - 長さ
     - ``len()`` はない。配列や辞書は ``size()``、文字列は ``length()`` を使う。
   * - 整数の割り算と剰余
     - ``-7 / 2`` は -3、``-7 % 3`` は -1 になる（:ref:`ch06`）。
   * - 小数から整数への変換
     - ``int(-3.7)`` は -3（0 の方向へ切り捨て）。小さい方向へ切り捨てるには ``floori()`` を使う。
   * - ``None`` の判定
     - ``null`` との比較は ``== null`` で行う。``is`` は型の判定に使う。
   * - タプル
     - タプルはない。複数の値を返したい場合は、配列や辞書、またはクラスを使う。
   * - 例外
     - 例外はない。戻り値でエラーを確認する。
   * - ラムダ式の変数の取り込み
     - ラムダ式は作られた時点のローカル変数の値を取り込む。後から変数を変更しても反映されない。
   * - スクリプトの読み込み
     - ``import`` はない。``class_name`` を付けたクラスはどこからでも使える。付けていないスクリプトは ``preload("res://...")`` で読み込む。
