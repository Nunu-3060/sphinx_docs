第 13 章 VFX Graph の実践
=========================

この章では、VFX Graph で数万個のパーティクルを使うエフェクトを作り、C# スクリプトからプロパティとイベントを操作する。最後に、Particle System と VFX Graph の使い分けを整理する。

この章のサンプルコードは、``examples/chapter13`` フォルダーにある。

作例：漂う光の粒
----------------

球の範囲の中に、数万個の光の粒を漂わせるエフェクトを作る。Particle System では処理が重くなる数だが、VFX Graph なら GPU で計算できる。

プロパティの作成
~~~~~~~~~~~~~~~~

#. 第 12 章の手順で、:guilabel:`Simple Loop` のテンプレートから VFX Graph のアセットを作り、名前を「Sparkles」にする。
#. アセットをダブルクリックして VFX Graph ウィンドウを開く。
#. Blackboard で、次の 2 つのプロパティを作り、どちらも :guilabel:`Exposed` を有効にする。

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 名前
     - 型
     - 初期値
   * - SpawnRate
     - Float
     - 10000
   * - ParticleColor
     - Color
     - 水色（R 0.3、G 0.8、B 1、A 1）

VFX Graph の Color 型のプロパティは、各成分を 0～1 の値で指定する。

グラフの編集
~~~~~~~~~~~~

テンプレートで最初から入っているブロックは、次の表にないものは削除してよい。各コンテキストに、表のブロックを上から順に並べる。

.. list-table::
   :header-rows: 1
   :widths: 25 30 45

   * - コンテキスト
     - ブロックまたは設定
     - 値
   * - Spawn
     - Constant Spawn Rate
     - :guilabel:`Rate` に SpawnRate をつなぐ
   * - Initialize Particle
     - :guilabel:`Capacity`
     - 50000
   * -
     - Set Position Shape
     - 形を球（Sphere）にし、半径を 2 にする
   * -
     - Set Velocity
     - ランダムにし、各成分を -0.2～0.2 にする
   * -
     - Set Lifetime
     - ランダムにし、2～4 にする
   * -
     - Set Color
     - ParticleColor をつなぐ
   * -
     - Set Size
     - 0.02
   * - Update Particle
     - Turbulence
     - 強さを 1、周波数を 1 程度にする
   * -
     - Linear Drag
     - 1
   * - Output Particle
     - :guilabel:`Blend Mode`
     - :guilabel:`Additive`
   * -
     - Orient
     - :guilabel:`Face Camera Plane`
   * -
     - Set Alpha over Life
     - 0 から 1 に上がり、1 から 0 に下がる山形のカーブ

ブロックの値を「ランダムにする」には、ブロックを選択し、Inspector ウィンドウでブロックの :guilabel:`Random` の設定を変える。値の入力欄が、最小値と最大値の 2 つになる。Set Lifetime のような 1 つの値のブロックでは :guilabel:`Uniform` にする。Set Velocity のような 3 つの成分を持つブロックでは :guilabel:`Per Component` にする。:guilabel:`Uniform` のままだと、3 つの成分が同じ割合で変わるため、すべてのパーティクルが 1 本の直線に沿った向きに飛んでしまう。

プロパティをブロックの入力につなぐには、Blackboard からプロパティをグラフにドラッグ＆ドロップし、プロパティのノードの出力を、ブロックの入力の左端の丸にドラッグする。

グラフを保存して、アセットをシーンに配置すると、球の範囲の中を光の粒が漂う。

パーティクルの数の見積もり
~~~~~~~~~~~~~~~~~~~~~~~~~~

放出の頻度が 1 秒あたり 10000 個、寿命の平均が 3 秒なので、同時に存在するパーティクルの数は :math:`10000 \times 3 = 30000` 個と見積もれる。寿命の最大の 4 秒で見積もっても 40000 個なので、:guilabel:`Capacity` の 50000 に収まる。

Visual Effect コンポーネントの Inspector ウィンドウの :guilabel:`Properties` で SpawnRate を変えると、光の粒の量が変わる。SpawnRate を 12500 より大きくすると、:guilabel:`Capacity` を超える場合があり、そのときは設定した頻度より少なくしか放出されない。

C# スクリプトからの操作
-----------------------

Visual Effect コンポーネントは、C# スクリプトから ``UnityEngine.VFX.VisualEffect`` 型として扱う。主なメソッドを次の表にまとめる。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - メソッド
     - 内容
   * - ``Play()``
     - OnPlay のイベントを送り、放出を始める。
   * - ``Stop()``
     - OnStop のイベントを送り、放出を止める。放出済みのパーティクルは、寿命が尽きるまで残る。
   * - ``Reinit()``
     - すべてのパーティクルを消して、最初の状態に戻す。
   * - ``SetFloat``、``SetVector3``、``SetVector4`` など
     - Exposed を有効にしたプロパティに値を設定する。
   * - ``GetFloat``、``GetVector3``、``GetVector4`` など
     - プロパティの値を取得する。
   * - ``HasFloat``、``HasVector3``、``HasVector4`` など
     - 指定した名前と型のプロパティがあるかどうかを調べる。
   * - ``SendEvent``
     - 指定した名前のイベントを送る。

イベントを追加する
~~~~~~~~~~~~~~~~~~

サンプルでは、Space キーを押したときに、光の粒をまとめて放出する。このために、Sparkles のグラフに独自のイベントを追加する。

#. グラフの何もない場所で右クリックし、:guilabel:`Create Node` から :guilabel:`Event` のコンテキストを追加する。名前を「OnBurst」にする。
#. :guilabel:`Spawn` のコンテキストをもう 1 つ追加し、OnBurst の出力をその :guilabel:`Start` の入力につなぐ。
#. 追加した Spawn コンテキストに Single Burst ブロックを追加し、:guilabel:`Count` を 5000 にする。
#. 追加した Spawn コンテキストの出力を、既存の Initialize Particle コンテキストの入力につなぐ。

Initialize Particle コンテキストには、複数の Spawn コンテキストをつなげる。どちらの Spawn コンテキストから放出されたパーティクルも、同じ初期化、更新、描画の処理を通る。

スクリプト
~~~~~~~~~~

.. literalinclude:: ../../examples/chapter13/VisualEffectController.cs
   :language: csharp
   :caption: VisualEffectController.cs
   :linenos:

:download:`VisualEffectController.cs をダウンロード <../../examples/chapter13/VisualEffectController.cs>`

スクリプトを Sparkles の GameObject にアタッチし、再生モードにする。上矢印キーと下矢印キーで SpawnRate が増減し、R キーで色が変わる。Space キーを押すと、5000 個の光の粒がまとめて放出される。

プロパティは、``SetFloat`` などのメソッドに名前の文字列を渡しても指定できる。サンプルでは、``Shader.PropertyToID`` メソッドで名前を整数の ID に変換しておき、その ID で指定している。文字列で指定すると、呼ぶたびに文字列から ID への変換が行われるため、毎フレーム値を変える場合は ID を使うほうがよい。

Color 型のプロパティは、C# からは ``SetVector4`` メソッドで設定する。``Color`` 型の値は、``Vector4`` 型に自動で変換される。

``SetFloat`` などのメソッドで指定したプロパティがグラフにない場合、値は設定されない。サンプルでは ``HasFloat`` などのメソッドでプロパティがあるかを確認し、名前の打ち間違いに気付けるようにしている。プロパティの名前は、大文字と小文字も含めてグラフと一致させる。

イベント属性
~~~~~~~~~~~~

イベントを送るときに、位置や色などの値を一緒に送れる。この値をイベント属性という。次のサンプルは、マウスでクリックした位置をイベント属性として送り、その位置に光の粒を放出する。

.. literalinclude:: ../../examples/chapter13/VisualEffectBurstOnClick.cs
   :language: csharp
   :caption: VisualEffectBurstOnClick.cs
   :linenos:

:download:`VisualEffectBurstOnClick.cs をダウンロード <../../examples/chapter13/VisualEffectBurstOnClick.cs>`

このサンプルには、Sparkles とは別の VFX Graph のアセットを用意する。

#. :guilabel:`Simple Loop` のテンプレートから VFX Graph のアセットを作り、名前を「ClickBurst」にする。
#. OnClick という名前の Event コンテキストを追加し、Spawn コンテキストの :guilabel:`Start` の入力につなぐ。OnPlay のイベントは、Spawn コンテキストからつながりを外す。
#. Spawn コンテキストの Constant Spawn Rate ブロックを削除し、Single Burst ブロックを追加して :guilabel:`Count` を 500 にする。
#. Initialize Particle コンテキストに Set Position ブロックを追加する。ブロックを選択し、Inspector ウィンドウで :guilabel:`Source` の設定を :guilabel:`Source` にする。
#. Set Position ブロックより下に、Set Velocity ブロックを追加し、ランダムにして各成分を -2～2 にする。
#. アセットを保存してシーンに配置し、GameObject の Transform を初期状態（位置が原点、回転なし、拡大率 1）にする。スクリプトをアタッチする。

再生モードで画面をクリックすると、クリックした位置から光の粒が飛び散る。

Set Position ブロックの :guilabel:`Source` の設定を :guilabel:`Source` にすると、ブロックは入力欄の値の代わりに、イベント属性の ``position`` の値を使う。スクリプトでは、``CreateVFXEventAttribute`` メソッドでイベント属性を入れる入れ物を作り、``SetVector3`` メソッドで位置を設定してから、``SendEvent`` メソッドでイベントと一緒に送っている。

パーティクルの位置の座標系は、コンテキストの右上の表示（:guilabel:`Local` または :guilabel:`World`）で決まる。:guilabel:`Local` の場合、位置は GameObject を基準にした座標になる。手順で GameObject の Transform を初期状態にしたのは、スクリプトが送るワールド座標の位置を、そのまま使えるようにするためである。

GPU イベント
------------

Particle System の Sub Emitters モジュールのように、パーティクルが消えたときなどに別のシステムからパーティクルを放出するには、GPU イベントを使う。Update Particle コンテキストに Trigger Event ブロックを追加し、パーティクルが消えたときにイベントを発生させる設定にすると、ブロックの出力を GPU Event コンテキストにつなげる。GPU Event コンテキストを別のシステムの Initialize Particle コンテキストにつなぐと、花火のように、消えたパーティクルの位置から新しいパーティクルを放出できる。

GPU イベントは、パーティクルの計算と同じく GPU の上で処理される。C# スクリプトに通知することはできない。

Particle System と VFX Graph の使い分け
---------------------------------------

第 2 章で説明した使い分けを、本資料で学んだ内容をもとに整理する。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 状況
     - 向いている機能
   * - パーティクルが数千個以下で、Inspector ウィンドウで手早く作りたい
     - Particle System
   * - 物理演算のコライダーとの衝突や、衝突したことのスクリプトへの通知が必要
     - Particle System（第 9 章）
   * - スクリプトから 1 つ 1 つのパーティクルを読み書きしたい
     - Particle System（第 9 章）
   * - コンピュートシェーダーに対応しない環境や、Built-in Render Pipeline も対象にする
     - Particle System
   * - 数万個以上のパーティクルを使いたい
     - VFX Graph
   * - 画面に映っているものとの衝突で十分で、大量のパーティクルを動かしたい
     - VFX Graph（深度バッファーとの衝突）
   * - ノードの計算を組み合わせて、複雑な動きを作りたい
     - VFX Graph

1 つのゲームの中で、両方を使い分けてもよい。たとえば、キャラクターの攻撃のヒットエフェクトは Particle System で作り、背景に漂う大量のちりや、画面全体に広がる派手な演出は VFX Graph で作る、といった分け方である。

さらに学ぶには
--------------

Package Manager ウィンドウで Visual Effect Graph パッケージを選び、:guilabel:`Samples` の :guilabel:`Learning Templates` をインポートすると、VFX Graph の機能ごとの作例が 20 個以上手に入る。グラフを開いて、ブロックやオペレーターの使い方を調べるとよい。
