第 8 章 衝突・サブエミッター・トレイル
======================================

この章では、パーティクルをシーンのオブジェクトとやり取りさせるモジュールと、パーティクルをきっかけに別の表現を加えるモジュールを説明する。

Collision モジュール
--------------------

Collision モジュールを有効にすると、パーティクルが地面や壁にぶつかって跳ね返るようになる。

:guilabel:`Type` で、衝突の相手を選ぶ。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 内容
   * - :guilabel:`Planes`
     - :guilabel:`Planes` のリストに設定した Transform を、無限に広がる平面として扱う。平面の向きは、Transform の Y 軸が法線になる。コライダーは必要ない。計算が軽い。
   * - :guilabel:`World`
     - シーンのコライダーと衝突する。複雑な形の地形とも衝突できるが、計算が重い。:guilabel:`Mode` で、3D と 2D のどちらの物理演算のコライダーと衝突するかを選ぶ。

平らな地面にだけ跳ね返ればよい場合は、:guilabel:`Planes` を使うと処理を軽くできる。

衝突したときの動き
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Dampen`
     - 0～1 の値で、衝突したときに失う速さの割合を指定する。
   * - :guilabel:`Bounce`
     - 衝突した面から跳ね返る速さの割合。1 のとき、ぶつかったときと同じ速さで跳ね返る。0 のとき、跳ね返らずに面に沿って滑る。
   * - :guilabel:`Lifetime Loss`
     - 0～1 の値で、衝突するたびに失う寿命の割合を指定する。1 のとき、衝突したパーティクルはすぐに消える。
   * - :guilabel:`Min Kill Speed`
     - 衝突した後の速さがこの値より小さいパーティクルを消す。
   * - :guilabel:`Radius Scale`
     - 衝突を判定するときの、パーティクルの半径の倍率。見た目の大きさと衝突の範囲を合わせるときに調整する。

:guilabel:`Lifetime Loss` を 1 にすると、雨粒が地面に当たって消えるような表現になる。消える瞬間に水しぶきを出すには、後述の Sub Emitters モジュールを使う。

World の衝突の設定
~~~~~~~~~~~~~~~~~~

:guilabel:`Type` が :guilabel:`World` のときは、次の設定項目がある。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 内容
   * - :guilabel:`Collides With`
     - 衝突するレイヤー。必要なレイヤーだけを選ぶと、処理が軽くなる。
   * - :guilabel:`Quality`
     - 衝突の計算の品質。:guilabel:`High` は、パーティクルごとに毎フレーム物理演算で衝突を調べる。:guilabel:`Medium` と :guilabel:`Low` は、衝突の結果を空間の格子ごとにまとめて使い回すため軽いが、パーティクルが薄い壁をすり抜けることがある。
   * - :guilabel:`Enable Dynamic Colliders`
     - 有効にすると、動いているコライダーとも衝突する。
   * - :guilabel:`Send Collision Messages`
     - 有効にすると、衝突したときにスクリプトの ``OnParticleCollision`` メソッドが呼ばれる（第 9 章を参照）。

Triggers モジュール
-------------------

Triggers モジュールは、パーティクルが指定したコライダーの内側に入ったり、外側に出たりしたときの動作を決める。跳ね返りはしない。

:guilabel:`Colliders` のリストに、判定に使うコライダーを設定する。次の 4 つの状況ごとに、動作を :guilabel:`Ignore`\ （何もしない）、:guilabel:`Kill`\ （パーティクルを消す）、:guilabel:`Callback`\ （スクリプトの ``OnParticleTrigger`` メソッドを呼ぶ）から選ぶ。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 状況
   * - :guilabel:`Inside`
     - パーティクルがコライダーの内側にある。
   * - :guilabel:`Outside`
     - パーティクルがコライダーの外側にある。
   * - :guilabel:`Enter`
     - パーティクルがコライダーの内側に入った。
   * - :guilabel:`Exit`
     - パーティクルがコライダーの外側に出た。

たとえば、屋根の下に置いたコライダーで :guilabel:`Inside` を :guilabel:`Kill` にすると、雨が屋根の下に降らないようにできる。

Sub Emitters モジュール
-----------------------

Sub Emitters モジュールは、パーティクルの発生や消滅などをきっかけに、別の Particle System からパーティクルを放出する。この別の Particle System を、サブエミッターという。花火のように、打ち上げた玉が空中で弾けて火花が広がる表現は、サブエミッターで作る。

リストの :guilabel:`+` ボタンを押すと、子の GameObject としてサブエミッター用の Particle System が作られる。リストの各行で、放出のきっかけと、サブエミッターに引き継ぐ値を選ぶ。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - きっかけ
     - 内容
   * - :guilabel:`Birth`
     - パーティクルが存在している間、パーティクルの位置から放出を続ける。
   * - :guilabel:`Collision`
     - パーティクルが衝突したときに、衝突した位置から放出する。Collision モジュールが必要である。
   * - :guilabel:`Death`
     - パーティクルが寿命で消えたときに、消えた位置から放出する。
   * - :guilabel:`Trigger`
     - Triggers モジュールで :guilabel:`Callback` を選んだ状況になったときに放出する。
   * - :guilabel:`Manual`
     - スクリプトから ``TriggerSubEmitter`` メソッドを呼んだときに放出する。

引き継ぐ値には、:guilabel:`Color`\ （色）、:guilabel:`Size`\ （大きさ）、:guilabel:`Rotation`\ （回転）、:guilabel:`Lifetime`\ （寿命）、:guilabel:`Duration`\ （周期）などがある。:guilabel:`Color` を引き継ぐと、元のパーティクルと同じ色の火花が出る。

サブエミッターが放出する数は、サブエミッター自身の Emission モジュールで決まる。:guilabel:`Birth` では :guilabel:`Rate over Time` や :guilabel:`Rate over Distance` で出し続ける。:guilabel:`Collision` と :guilabel:`Death` では、1 回のきっかけごとに :guilabel:`Bursts` の分を放出する。

サブエミッターの放出数は、元のパーティクルの数に比例して増える。元のパーティクルが 100 個あり、それぞれが消えるときに 50 個の火花を出すと、合計 5000 個になる。サブエミッターの Main モジュールの :guilabel:`Max Particles` を超えると放出されなくなるため、数に注意する。

Trails モジュール
-----------------

Trails モジュールは、パーティクルが通った跡に帯状の軌跡を描く。流れ星、剣の軌跡、飛んでいく魔法の弾などに使う。軌跡の描画には、Renderer モジュールの :guilabel:`Trail Material` に設定したマテリアルを使う。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 内容
   * - :guilabel:`Mode`
     - :guilabel:`Particles` は、パーティクルごとに、通った跡に軌跡を描く。:guilabel:`Ribbon` は、放出した順にパーティクルを結んで 1 本の帯を描く。
   * - :guilabel:`Ratio`
     - 0～1 の値で、軌跡を描くパーティクルの割合を指定する。
   * - :guilabel:`Lifetime`
     - 0～1 の値で、軌跡の長さを、パーティクルの寿命に対する割合で指定する。軌跡の各点は、この時間が経つと消える。
   * - :guilabel:`Minimum Vertex Distance`
     - 軌跡の点を追加する最小の距離。値を小さくすると、軌跡が滑らかになるが、点の数が増える。
   * - :guilabel:`Die with Particles`
     - 有効にすると、パーティクルが消えたときに軌跡も消える。無効にすると、軌跡は自然に消えるまで残る。
   * - :guilabel:`Width over Trail`
     - 軌跡の先端から末端までの幅の変化。
   * - :guilabel:`Color over Trail`
     - 軌跡の先端から末端までの色の変化。

パーティクル自体を表示せず、軌跡だけを表示したい場合は、Renderer モジュールの :guilabel:`Render Mode` を :guilabel:`None` にする。

Lights モジュール
-----------------

Lights モジュールは、パーティクルの一部にライトを付けて、周りを照らす。火の粉や魔法の光が、周囲の壁や地面を照らす表現に使う。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 内容
   * - :guilabel:`Light`
     - パーティクルに付けるライト。シーンやプレハブの Light コンポーネントを設定する。
   * - :guilabel:`Ratio`
     - 0～1 の値で、ライトを付けるパーティクルの割合を指定する。
   * - :guilabel:`Use Particle Color`
     - 有効にすると、ライトの色にパーティクルの色を掛け合わせる。
   * - :guilabel:`Size Affects Range`
     - 有効にすると、パーティクルの大きさに応じてライトの範囲を変える。
   * - :guilabel:`Alpha Affects Intensity`
     - 有効にすると、パーティクルの不透明度に応じてライトの強さを変える。
   * - :guilabel:`Maximum Lights`
     - ライトを付けるパーティクルの最大数。

リアルタイムのライトは処理が重い。URP の Forward のレンダリングパスでは、1 つのオブジェクトを照らせるライトの数にも上限がある。:guilabel:`Ratio` と :guilabel:`Maximum Lights` を小さくして、ライトを付けるパーティクルを少数に絞るとよい。
