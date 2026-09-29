第 12 章 VFX Graph の基礎
=========================

VFX Graph（Visual Effect Graph）は、パーティクルの計算を GPU で行う機能である。Particle System との違いは、第 2 章で説明した。この章では、VFX Graph の導入方法、グラフの構成要素、パーティクルが放出されてから消えるまでの流れを説明する。

VFX Graph は、URP と HDRP で使える。Built-in Render Pipeline では使えない。また、コンピュートシェーダーに対応した GPU が必要である。

導入
----

VFX Graph は、Visual Effect Graph パッケージとして提供されている。次の手順でプロジェクトに追加する。

#. :menuselection:`Window --> Package Manager` を選び、Package Manager ウィンドウを開く。
#. 左側の一覧で :guilabel:`Unity Registry` を選ぶ。
#. パッケージの一覧から :guilabel:`Visual Effect Graph` を選び、:guilabel:`Install` を押す。

VFX Graph のバージョンは、プロジェクトの URP のバージョンに合わせたものが自動で選ばれる。

VFX Graph のアセットの作成
--------------------------

VFX Graph では、エフェクトの内容を VFX Graph のアセットに保存する。アセットは次の手順で作る。

#. Project ウィンドウで右クリックし、:menuselection:`Create --> Visual Effects --> Visual Effect Graph` を選ぶ。
#. テンプレートを選ぶウィンドウが開く。:guilabel:`Simple Loop` を選び、:guilabel:`Create` を押す。
#. アセットの名前を付ける。

作ったアセットをダブルクリックすると、VFX Graph ウィンドウが開き、グラフを編集できる。

シーンへの配置
~~~~~~~~~~~~~~

VFX Graph のアセットを Project ウィンドウから Hierarchy ウィンドウか Scene ビューにドラッグ＆ドロップすると、Visual Effect コンポーネントを持つ GameObject が作られ、エフェクトが再生される。Visual Effect コンポーネントは、Particle System コンポーネントにあたるもので、:guilabel:`Asset Template` に設定した VFX Graph のアセットを再生する。

Visual Effect コンポーネントを持つ GameObject を選択すると、Scene ビューに再生を操作するパネルが表示される。このパネルで、再生、一時停止、停止、再生の速さの変更などを行える。

グラフの構成要素
----------------

VFX Graph のグラフは、次の要素でできている。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 要素
     - 内容
   * - コンテキスト
     - 処理の段階を表す大きな枠。上から下に向かって、放出、初期化、更新、描画の順に処理される。
   * - ブロック
     - コンテキストの中に積み重ねる処理の単位。上のブロックから順に実行される。Particle System のモジュールの設定項目にあたる。
   * - オペレーター
     - 値を計算するノード。出力をブロックの入力につなぐと、計算した値をブロックで使える。
   * - プロパティ
     - グラフの外から値を変えられる変数。Blackboard で定義する（後述）。
   * - システム
     - 放出から描画までのひとつながりのコンテキスト。1 つのグラフに、複数のシステムを置ける。

Particle System では、Inspector ウィンドウでモジュールを有効にして値を設定した。VFX Graph では、コンテキストにブロックを追加し、必要ならオペレーターで計算した値をつないで設定する。

コンテキストの流れ
~~~~~~~~~~~~~~~~~~

:guilabel:`Simple Loop` のテンプレートで作ったグラフには、上から次のコンテキストが並んでいる。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - コンテキスト
     - 内容
   * - Spawn
     - 1 フレームに何個のパーティクルを放出するかを決める。Particle System の Emission モジュールにあたる。
   * - Initialize Particle
     - 放出したパーティクルの初期値（位置、速度、寿命など）を決める。Particle System の Main モジュールと Shape モジュールにあたる。
   * - Update Particle
     - 毎フレーム、パーティクルの値を更新する。重力、空気抵抗、揺らぎなどを加える。
   * - Output Particle
     - パーティクルを描画する。形、テクスチャー、色、大きさ、合成の方法を決める。描画する形によって、Output Particle Quad などの種類がある。

Spawn コンテキストの上には、再生と停止のイベント（OnPlay と OnStop）が表示される。Visual Effect コンポーネントが再生を始めると、OnPlay のイベントが Spawn コンテキストに送られ、放出が始まる。

ブロックとオペレーターの追加
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

コンテキストの上で右クリックして :guilabel:`Create Block` を選ぶか、Space キーを押すと、ブロックを検索して追加できる。グラフの何もない場所で右クリックして :guilabel:`Create Node` を選ぶか、Space キーを押すと、オペレーターやコンテキストを検索して追加できる。

ブロックを追加したり値を変えたりすると、グラフは自動でコンパイルされ、Scene ビューのエフェクトに反映される。変更をアセットに保存するには、VFX Graph ウィンドウの :guilabel:`Save` ボタンを押すか、Ctrl + S キーを押す。

属性
----

VFX Graph では、パーティクルが持つ値を属性（アトリビュート）という。主な属性を次の表にまとめる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 属性
     - 内容
   * - ``position``
     - 位置
   * - ``velocity``
     - 速度
   * - ``lifetime``
     - 寿命（秒）
   * - ``age``
     - 放出されてからの経過時間（秒）
   * - ``size``
     - 大きさ
   * - ``color``
     - 色
   * - ``alpha``
     - 不透明度

ブロックの多くは、属性に値を設定する。たとえば、Set Lifetime ブロックは ``lifetime`` 属性に、Set Velocity ブロックは ``velocity`` 属性に値を設定する。ブロックの設定で、値を固定にするか、2 つの値の間のランダムな値にするかを選べる。

寿命に対する経過時間は、第 6 章と同じく次の式で表される。

.. math::

   t_n = \frac{\mathit{age}}{\mathit{lifetime}}

名前の最後に「over Life」が付くブロック（Set Size over Life や Set Color over Life など）は、:math:`t_n` を横軸にしたカーブやグラデーションで値を設定する。Particle System の Size over Lifetime モジュールや Color over Lifetime モジュールにあたる。

各コンテキストの主な設定
------------------------

Spawn コンテキスト
~~~~~~~~~~~~~~~~~~

Spawn コンテキストには、放出の頻度を決めるブロックを追加する。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ブロック
     - 内容
   * - Constant Spawn Rate
     - 1 秒あたり :guilabel:`Rate` 個のパーティクルを放出し続ける。
   * - Single Burst
     - 1 回だけ、まとめてパーティクルを放出する。
   * - Periodic Burst
     - 一定の間隔で、まとめてパーティクルを放出する。

Initialize Particle コンテキスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initialize Particle コンテキストは、ブロックのほかに、次の設定を持つ。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定
     - 内容
   * - :guilabel:`Capacity`
     - 同時に存在できるパーティクルの最大数。この数に応じて、GPU のメモリーが最初に確保される。Particle System の :guilabel:`Max Particles` にあたる。
   * - :guilabel:`Bounds Setting Mode`
     - エフェクト全体を囲むバウンディングボックスの決め方。:guilabel:`Manual` は手で指定する。:guilabel:`Recorded` は、エディター上で再生して記録した範囲を使う。:guilabel:`Automatic` は、実行中に自動で計算する。
   * - :guilabel:`Bounds`
     - :guilabel:`Manual` のときの、バウンディングボックスの中心と大きさ。

同時に存在するパーティクルの数は、Particle System と同じく :math:`N \approx r \times L` で見積もれる（第 5 章を参照）。:guilabel:`Capacity` は、この値より大きくしておく。:guilabel:`Capacity` を超えた分のパーティクルは放出されない。一方、:guilabel:`Capacity` を必要以上に大きくすると、使わないメモリーを確保することになる。

バウンディングボックスは、エフェクトが画面の中にあるかどうかの判定に使う。バウンディングボックスが実際のパーティクルの範囲より小さいと、パーティクルが画面に映っているのに、バウンディングボックスが画面の外に出た時点でエフェクト全体が描画されなくなる。

Initialize Particle コンテキストには、次のようなブロックを追加する。

* Set Position Shape ブロック：パーティクルを放出する範囲の形（球、円柱、箱など）を決める。Particle System の Shape モジュールにあたる。
* Set Velocity ブロック：初速を決める。
* Set Lifetime ブロック：寿命を決める。

Update Particle コンテキスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Update Particle コンテキストは、毎フレーム、速度に従ってパーティクルの位置を動かし、``age`` を増やす。``age`` が ``lifetime`` を超えたパーティクルは消える。これらの処理は、ブロックを追加しなくても自動で行われる。

Update Particle コンテキストには、次のようなブロックを追加する。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ブロック
     - 内容
   * - Gravity
     - 重力の加速度を加える。
   * - Linear Drag
     - 空気抵抗のように、速度を落とす。
   * - Turbulence
     - 不規則な揺らぎを加える。Particle System の Noise モジュールにあたる。
   * - Collision Shape
     - 球、箱、平面などの形状と衝突させる。
   * - Collision Depth Buffer
     - カメラの深度バッファーを使って、画面に映っているものと衝突させる。

VFX Graph のパーティクルは GPU で計算されるため、Particle System のように物理演算のコライダーと衝突させることはできない。代わりに、形状や深度バッファーとの衝突を使う。

Output Particle コンテキスト
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Output Particle コンテキストは、パーティクルの描画の方法を決める。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定
     - 内容
   * - :guilabel:`Blend Mode`
     - 背景との合成の方法。:guilabel:`Alpha`、:guilabel:`Additive`、:guilabel:`Alpha Premultiplied`、:guilabel:`Opaque` から選ぶ。考え方は第 7 章の :guilabel:`Blending Mode` と同じである。
   * - :guilabel:`Main Texture`
     - パーティクルに貼るテクスチャー。
   * - :guilabel:`UV Mode`
     - テクスチャーの使い方。:guilabel:`Flipbook` にすると、フリップブックのコマ送りのアニメーションに使える。

Output Particle コンテキストには、次のようなブロックを追加する。

* Orient ブロック：パーティクルの向きを決める。:guilabel:`Face Camera Plane` にすると、ビルボードになる。
* Set Size over Life ブロック：寿命の間の大きさの変化を決める。
* Set Color over Life ブロック：寿命の間の色と不透明度の変化を決める。

Blackboard とプロパティ
-----------------------

Blackboard は、グラフで使うプロパティを定義するパネルである。VFX Graph ウィンドウの :guilabel:`Blackboard` ボタンで表示と非表示を切り替える。

プロパティは、次の手順で作る。

#. Blackboard の :guilabel:`+` ボタンを押し、型（Float、Vector3、Color など）を選ぶ。
#. プロパティの名前を付ける。
#. プロパティを Blackboard からグラフにドラッグ＆ドロップし、ブロックの入力につなぐ。

プロパティの :guilabel:`Exposed` を有効にすると、Visual Effect コンポーネントの Inspector ウィンドウの :guilabel:`Properties` に表示される。Inspector ウィンドウで値を変えると、同じ VFX Graph のアセットを使うエフェクトでも、GameObject ごとに異なる値にできる。たとえば、1 つの炎のグラフから、色の違う炎を複数作れる。

Exposed を有効にしたプロパティは、C# スクリプトからも値を変えられる（第 13 章を参照）。
