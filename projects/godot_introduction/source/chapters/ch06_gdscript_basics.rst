.. _ch06:

========================
第 6 章　GDScript の基礎
========================

本章では、Godot のスクリプト言語 GDScript の基本的な文法を、Python と比較しながら説明する。サンプルは ``chapter06`` フォルダーにある。``basics.tscn`` を実行すると、本章で紹介するコードの実行結果が「出力」パネルに表示される。

Python との対応
===============

GDScript は Python によく似ているが、ゲームエンジン用の言語として設計されているため、いくつかの違いがある。まず全体像として、主な対応関係を表にまとめる。

.. list-table:: Python と GDScript の主な対応
   :header-rows: 1
   :widths: 24 38 38

   * - 項目
     - Python
     - GDScript
   * - ブロック
     - インデント
     - インデント。Godot のエディターでは、既定でタブ文字を使う。
   * - 変数の宣言
     - ``x = 1``
     - ``var x = 1``。宣言には ``var`` が必要
   * - 定数
     - 慣習として大文字の変数
     - ``const MAX_HP = 100``。再代入するとエラーになる。
   * - 型ヒント
     - ``x: int = 1``
     - ``var x: int = 1``。型を指定すると、実行時にも型が強制される。
   * - 関数
     - ``def f(a: int) -> int:``
     - ``func f(a: int) -> int:``
   * - 真偽値、空の値
     - ``True``、``False``、``None``
     - ``true``、``false``、``null``
   * - 論理演算子
     - ``and``、``or``、``not``
     - ``and``、``or``、``not``。``&&``、``||``、``!`` も使える。
   * - 整数の割り算
     - ``7 // 2`` は 3、``-7 // 2`` は -4
     - ``7 / 2`` は 3、``-7 / 2`` は -3（0 の方向へ切り捨て）
   * - リスト、辞書
     - ``list``、``dict``
     - ``Array``、``Dictionary``
   * - クラス
     - 1 つのファイルに複数のクラスを書ける。
     - 1 つのファイルが 1 つのクラスになる。
   * - コンストラクター
     - ``__init__``
     - ``_init``
   * - 文字列への変換
     - ``__str__``
     - ``_to_string``
   * - モジュールの読み込み
     - ``import``
     - ``class_name`` で登録したクラスはどこからでも使える。ファイルは ``preload()`` または ``load()`` で読み込む。
   * - 例外
     - ``try``、``except``、``raise``
     - なし。エラーは戻り値（``Error`` 型）で知らせる。
   * - リスト内包表記
     - ``[x * 2 for x in a]``
     - なし。``a.map(func(x): return x * 2)`` のように書く。
   * - タプルの展開
     - ``a, b = b, a``
     - なし

以降の節で、それぞれを詳しく見ていく。

スクリプトの基本構造
====================

GDScript のファイル（``.gd``）は、それ自体が 1 つのクラスである。ファイルの先頭の ``extends`` で継承元のクラスを指定する。ノードに付けるスクリプトは、そのノードの種類（またはその継承元）を ``extends`` で指定する。

.. code-block:: gdscript
   :linenos:
   :caption: スクリプトの構造（Godot 公式のスタイルガイドが推奨する順序）

   class_name Player   # クラス名を登録する（省略可能）
   extends CharacterBody2D   # 継承元のクラス
   ## ドキュメントコメント（クラスの説明）

   signal died   # シグナル（第 7 章）

   enum State { IDLE, RUN }   # 列挙型（第 7 章）

   const SPEED: float = 300.0   # 定数

   @export var max_hp: int = 100   # インスペクターに表示する変数

   var hp: int = 0   # 通常の変数（メンバー変数）

   @onready var sprite: Sprite2D = $Sprite2D   # ノードの準備ができたときに初期化する変数


   func _ready() -> void:   # Godot が呼び出す組み込みの関数
       hp = max_hp


   func take_damage(amount: int) -> void:   # 自分で定義する関数
       hp -= amount

関数と関数の間は 2 行空ける。名前は、クラス名が ``PascalCase``、関数名と変数名が ``snake_case``、定数が ``CONSTANT_CASE`` である。先頭に ``_`` を付けた名前は、クラスの外から使うことを想定していないことを表す（Python と同じく慣習であり、外から使うことは禁止されていない）。

変数と型
========

.. literalinclude:: ../../examples/chapter06/variables.gd
   :language: gdscript
   :linenos:
   :tab-width: 4
   :caption: chapter06/variables.gd

実行結果は次のとおりである。

.. code-block:: text
   :linenos:

   --- 変数と型 ---
   ゴドー の HP: 70 / 100
   speed の型: float
   target は null か: true
   7 / 2 = 3、7.0 / 2 = 3.5
   -7 / 2 = -3（Python の -7 // 2 は -4）
   -7 % 3 = -1、posmod(-7, 3) = 2
   ゴドー のスコアは 00420 点
   ゴドー は 10, 20 にいる
   円周率は約 3.14

型の指定
--------

変数の型は次の 3 通りで書ける。

.. list-table:: 変数の型の書き方
   :header-rows: 1
   :widths: 35 65

   * - 書き方
     - 意味
   * - ``var a = 1``
     - 型を指定しない。後から別の型の値も代入できる（動的型付け）。
   * - ``var b: int = 1``
     - 型を明示する。``int`` 以外の値を代入しようとするとエラーになる。
   * - ``var c := 1``
     - 右辺の値から型を推論する。この例では ``int`` になり、以降は ``b`` と同じく型が固定される。

Python の型ヒントは実行時には無視されるが、GDScript の型指定は実行時にも有効である。型を指定すると、次の利点がある。

* 間違った型の代入を、エディターが実行前に指摘してくれる。
* コード補完が正確になる。
* 型が決まっている演算は、Godot が最適化した命令で実行するので速くなる。

本書のサンプルでは、すべての変数、引数、戻り値に型を指定している。型を指定する習慣については :ref:`ch07` でもう一度説明する。

数値の演算で注意する点
----------------------

GDScript の ``int`` は 64 ビットの整数、``float`` は 64 ビットの浮動小数点数である。数値の演算は Python とほぼ同じだが、次の点が異なる。

* **整数どうしの割り算**：``/`` の両辺が整数なら、結果も整数になる。小数点以下は 0 の方向へ切り捨てられるので、負の数では Python の ``//`` と結果が異なる。小数の結果が欲しい場合は、どちらかを ``float`` にする（``7.0 / 2`` や ``float(a) / b``）。エディターは整数どうしの割り算に警告を出すので、意図した割り算であることを確かめる手がかりにするとよい。
* **剰余**：``%`` の結果の符号は左辺と同じになる。Python のように常に 0 以上の値が欲しい場合は ``posmod()`` を使う。浮動小数点数の剰余は ``fmod()`` または ``fposmod()`` を使う。

組み込みの型
------------

GDScript には、ゲームでよく使う値を表す型が組み込まれている。

.. list-table:: よく使う組み込みの型
   :header-rows: 1
   :widths: 25 75

   * - 型
     - 内容
   * - ``int``、``float``、``bool``
     - 整数、浮動小数点数、真偽値
   * - ``String``
     - 文字列。``"..."`` と ``'...'`` のどちらでも書ける。
   * - ``Vector2``、``Vector2i``
     - 2 次元のベクトル（位置や速度）。``Vector2i`` は整数版
   * - ``Vector3``
     - 3 次元のベクトル
   * - ``Color``
     - 色。赤、緑、青、不透明度を 0.0 ～ 1.0 で持つ。
   * - ``Rect2``
     - 長方形（位置と大きさ）
   * - ``Array``、``Dictionary``
     - 配列、辞書
   * - ``PackedInt32Array``、``PackedVector2Array`` など
     - 要素の型が決まった、メモリー効率の良い配列
   * - ``Callable``
     - 関数への参照（:ref:`ch07`）
   * - ``Signal``
     - シグナルへの参照（:ref:`ch07`）
   * - ``NodePath``、``StringName``
     - ノードのパスと、比較が高速な文字列。``^"Path/To/Node"``、``&"name"`` と書く。
   * - ``Object`` を継承したクラス
     - ノードやリソースなど。``null`` を代入できる。

``int`` や ``Vector2`` などの組み込みの型は値として扱われ、代入するとコピーされる。``Array``、``Dictionary``、``Object`` は参照として扱われる（後述）。

文字列の書式指定
----------------

``%`` 演算子による書式指定は、Python の古い書式指定と同じように書ける。``format()`` メソッドを使うと、``{名前}`` の部分を辞書の値で置き換えられる。Python の f 文字列に相当する機能はない。単純に連結する場合は ``+`` を使うが、数値は ``str()`` で文字列に変換してから連結する。

制御構文
========

.. literalinclude:: ../../examples/chapter06/control_flow.gd
   :language: gdscript
   :linenos:
   :tab-width: 4
   :caption: chapter06/control_flow.gd

``if``、``elif``、``else``、``for``、``while``、``break``、``continue`` は Python と同じように使える。``for i in 3:`` のように整数を直接書くと、``range(3)`` と同じ意味になる。``for`` の変数にも ``fruit: String`` のように型を指定できる。

``match`` は、値に応じて処理を分ける構文で、他の言語の ``switch`` 文に相当する。``"attack", "shoot":`` のようにカンマで区切ると、いずれかに一致した場合に実行される。``_`` はどの値にも一致する。Python の ``match`` と異なり、分岐の先頭に ``case`` は書かない。

関数
====

.. literalinclude:: ../../examples/chapter06/functions.gd
   :language: gdscript
   :linenos:
   :tab-width: 4
   :caption: chapter06/functions.gd

関数は ``func`` で定義する。引数と戻り値の型は Python の型ヒントと同じ形で書く。戻り値がない関数は ``-> void`` とする。引数には既定値を指定できる。Python のキーワード引数（``greet(message="やあ")`` のような呼び出し方）はない。

``static`` を付けた関数（静的関数）は、インスタンスを作らずに ``クラス名.関数名()`` の形で呼び出せる。静的関数の中では、メンバー変数は使えない。

配列と辞書
==========

.. literalinclude:: ../../examples/chapter06/collections.gd
   :language: gdscript
   :linenos:
   :tab-width: 4
   :caption: chapter06/collections.gd

``Array`` は Python のリスト、``Dictionary`` は Python の辞書に相当する。``Array[String]`` のように要素の型を指定すると、異なる型の値を追加しようとしたときにエラーになる。辞書も ``Dictionary[String, int]`` のようにキーと値の型を指定できる。

辞書は Python と同じく、要素を追加した順番を保つ。存在しないキーを ``prices["鎧"]`` のように参照するとエラーになるので、あるかどうか分からない場合は ``get()`` で既定値を指定するか、``has()`` で確認する。

配列と辞書は参照で扱われる。``var copied := items`` は同じ配列を指す別名を作るだけで、複製はしない。この点は Python と同じである。複製が必要な場合は ``duplicate()`` を使う。入れ子になった配列や辞書まで複製する場合は ``duplicate(true)`` とする。

``Array`` には ``map()``、``filter()``、``reduce()``、``any()``、``all()`` などのメソッドがある。これらは関数（:ref:`ch07` で説明する ``Callable``）を引数に取り、Python のリスト内包表記や組み込み関数の代わりに使える。

クラス
======

GDScript では、1 つのファイルが 1 つのクラスになる。先頭に ``class_name`` を書くと、そのクラスがプロジェクト全体に登録され、どのスクリプトからもクラス名で使えるようになる。

.. literalinclude:: ../../examples/chapter06/enemy_stats.gd
   :language: gdscript
   :linenos:
   :tab-width: 4
   :caption: chapter06/enemy_stats.gd

``RefCounted`` は、参照カウントで自動的に解放されるオブジェクトの基底クラスである。ノードではないデータだけのクラスを作るときに使う。``extends`` を省略した場合も ``RefCounted`` を継承する。

``_init()`` はコンストラクターで、``EnemyStats.new("スライム", 10, 2)`` のように ``new()`` に渡した引数を受け取る。メソッドの中でメンバー変数を使うときは、Python のように ``self.`` を付ける必要はない（付けてもよい）。引数とメンバー変数の名前が同じだと区別しにくくなるので、この例では引数を ``new_name`` のように別の名前にしている。

このクラスを使う側のスクリプトは次のとおりである。

.. literalinclude:: ../../examples/chapter06/classes.gd
   :language: gdscript
   :linenos:
   :tab-width: 4
   :caption: chapter06/classes.gd

6 行目の ``class Counter:`` は内部クラス（inner class）である。そのスクリプトの中でだけ使う小さなクラスは、このように 1 つのファイルの中に定義できる。

ライフサイクル関数
==================

ノードに付けたスクリプトには、Godot が決まったタイミングで呼び出す関数を定義できる。これらの関数は名前が ``_`` で始まり、ライフサイクル関数（または仮想関数）と呼ばれる。

.. list-table:: 主なライフサイクル関数
   :header-rows: 1
   :widths: 35 65

   * - 関数
     - 呼ばれるタイミング
   * - ``_init()``
     - オブジェクトが作られたとき。まだシーンツリーには入っていない。
   * - ``_enter_tree()``
     - ノードがシーンツリーに追加されたとき
   * - ``_ready()``
     - ノードとそのすべての子ノードの準備ができたとき。最初の 1 回だけ呼ばれる。
   * - ``_process(delta)``
     - 毎フレーム（描画のたびに）呼ばれる。``delta`` は前のフレームからの経過秒数
   * - ``_physics_process(delta)``
     - 物理演算の更新のたびに、一定の間隔（既定では 1 秒に 60 回）で呼ばれる。
   * - ``_input(event)``、``_unhandled_input(event)``
     - キーやマウスなどの入力があったとき（:ref:`ch09`）
   * - ``_exit_tree()``
     - ノードがシーンツリーから取り除かれるとき

``chapter06/lifecycle.tscn`` は、親ノード ``Parent`` と子ノード ``Child`` の両方に同じスクリプトを付けて、呼ばれる順番を表示するサンプルである。

.. literalinclude:: ../../examples/chapter06/lifecycle.gd
   :language: gdscript
   :linenos:
   :tab-width: 4
   :caption: chapter06/lifecycle.gd

実行すると、次のように出力される（``delta`` の値は環境によって異なる）。

.. code-block:: text
   :linenos:

   _init
   _init
   Parent: _enter_tree
   Child: _enter_tree
   Child: _ready
   Parent: _ready
   Parent: _physics_process delta=0.0167
   Child: _physics_process delta=0.0167
   Parent: _process delta=0.0487
   Child: _process delta=0.0487
   （中略）
   Child: _exit_tree
   Parent: _exit_tree

``_enter_tree()`` は親から子の順に呼ばれるが、``_ready()`` は子から親の順に呼ばれる。つまり、親の ``_ready()`` が呼ばれた時点で、子ノードの準備はすべて終わっている。そのため、子ノードを使う初期化処理は ``_ready()`` に書く。

``_process()`` と ``_physics_process()`` の違いは、:ref:`ch08` で説明する。

@export と @onready
===================

``@`` で始まる記述はアノテーションと呼ばれ、変数や関数に追加の意味を与える。特によく使うのが ``@export`` と ``@onready`` である。

``@export`` を付けた変数はインスペクターに表示され、エディターで値を設定できる。設定した値はシーンファイルに保存される。同じシーンの複数のインスタンスで値を変えたい場合や、プログラマー以外の人が調整する値に使う。``@export_range(0, 100)`` や ``@export_multiline`` のように、入力方法を指定する種類もある。

``@onready`` を付けた変数は、``_ready()`` が呼ばれる直前に初期化される。子ノードを取得して変数に入れておく場合によく使う。

.. code-block:: gdscript
   :linenos:

   # 誤り：スクリプトの初期化時点では子ノードがまだ使えないので、null になる
   var sprite: Sprite2D = $Sprite2D

   # 正しい：_ready() の直前に取得する
   @onready var sprite: Sprite2D = $Sprite2D

ノードを毎回 ``$Sprite2D`` で取得することもできるが、``@onready`` の変数に型を付けて保存しておくと、補完が効き、実行時の検索も 1 回で済む。
