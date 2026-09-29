第 3 章 最初のパーティクル
==========================

この章では、シーンに Particle System を追加し、エディター上で再生して動きを確かめる。あわせて、Inspector ウィンドウでの Particle System の設定画面の見方を説明する。

Particle System の作成
----------------------

Particle System を作成するには、次の手順で操作する。

#. Unity 6 で Universal 3D のテンプレートから新しいプロジェクトを作成し、シーンを開く。
#. :menuselection:`GameObject --> Effects --> Particle System` を選ぶ。Hierarchy ウィンドウで右クリックし、:menuselection:`Effects --> Particle System` を選んでもよい。

「Particle System」という名前の GameObject が作られ、Scene ビューで白い粒が上に向かって放出される。これが最初のパーティクルである。

作られた GameObject には、Particle System コンポーネントが付いている。既存の GameObject に Particle System を追加するには、Inspector ウィンドウの :guilabel:`Add Component` から :menuselection:`Effects --> Particle System` を選ぶ。

作られた GameObject は、Transform の :guilabel:`Rotation` の X が -90 になっている。既定の設定では、パーティクルはローカル座標の Z 軸の正の向きに放出される。X 軸まわりに -90 度回転させることで、Z 軸がワールド座標の上向きになり、パーティクルが上に向かって放出される。

エディターでの再生
------------------

Particle System の GameObject を選択すると、Scene ビューに Particle Effect パネルが表示される。このパネルで、エディター上でのパーティクルの再生を操作できる。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - 内容
   * - :guilabel:`Pause` と :guilabel:`Play`
     - 再生を一時停止する。一時停止中は、再生を再開するボタンになる。
   * - :guilabel:`Restart`
     - パーティクルを消して、最初から再生し直す。
   * - :guilabel:`Stop`
     - 再生を止めて、パーティクルを消す。
   * - :guilabel:`Playback Speed`
     - 再生の速さの倍率。0.1 にすると、動きを 10 分の 1 の速さでじっくり確認できる。
   * - :guilabel:`Playback Time`
     - 再生を始めてからの経過時間。値を左右にドラッグすると、時間を戻したり進めたりできる。
   * - :guilabel:`Particles`
     - 現在存在するパーティクルの数。
   * - :guilabel:`Resimulate`
     - 有効にすると、設定を変えたときに、放出済みのパーティクルにも変更を反映する。
   * - :guilabel:`Show Bounds`
     - パーティクル全体を囲む範囲（バウンディングボックス）を表示する。

エディター上では、Particle System は選択している間だけ再生される。選択を外すと再生が止まる。再生モードでは、選択しているかどうかに関係なく再生される。

Inspector ウィンドウの見方
--------------------------

Particle System コンポーネントの設定は、モジュールと呼ばれるまとまりに分かれている。Inspector ウィンドウには、モジュールの名前が縦に並んで表示される。

* モジュールの名前をクリックすると、そのモジュールの設定項目が開いたり閉じたりする。
* モジュールの名前の左にあるチェックボックスで、モジュールを有効にするか無効にするかを切り替える。無効にしたモジュールの設定は、パーティクルに影響しない。
* 一番上のモジュールは、GameObject の名前が表示されている。これが Main モジュールで、無効にはできない。

既定では、Main モジュールのほかに、Emission モジュール、Shape モジュール、Renderer モジュールが有効になっている。この 4 つがあれば、パーティクルを放出して描画できる。

主なモジュールの役割を次の表にまとめる。各モジュールの詳細は、第 4 章～第 8 章で説明する。

.. list-table::
   :header-rows: 1
   :widths: 35 50 15

   * - モジュール
     - 役割
     - 説明する章
   * - Main
     - 再生時間、寿命、初速、大きさ、色などの初期値と、Particle System 全体の設定
     - 第 4 章
   * - Emission
     - 放出の頻度
     - 第 5 章
   * - Shape
     - 放出する範囲の形と向き
     - 第 5 章
   * - Velocity over Lifetime など
     - 寿命の間の速度、色、大きさ、回転の変化
     - 第 6 章
   * - Noise
     - 不規則な揺らぎ
     - 第 6 章
   * - Renderer
     - 描画の方法とマテリアル
     - 第 7 章
   * - Texture Sheet Animation
     - テクスチャーのコマ送りのアニメーション
     - 第 7 章
   * - Collision、Triggers
     - コライダーとの衝突と接触
     - 第 8 章
   * - Sub Emitters
     - パーティクルの発生や消滅をきっかけにした、別の Particle System の放出
     - 第 8 章
   * - Trails、Lights
     - パーティクルの軌跡と、パーティクルに付いて動くライト
     - 第 8 章

Inspector ウィンドウの :guilabel:`Open Editor` ボタンを押すと、Particle System の設定を編集するための専用のウィンドウが開く。複数の Particle System を組み合わせたエフェクトを編集するときは、このウィンドウを使うと全体を見渡しやすい。

Particle System の親子関係
--------------------------

炎と煙のように、性質の異なるパーティクルを組み合わせたエフェクトは、Particle System を持つ GameObject を親子にして作る。親の Particle System を再生すると、子の Particle System も一緒に再生される。Particle Effect パネルの操作も、子の Particle System にまとめて反映される。

エフェクトの保存
----------------

作ったエフェクトは、プレハブにして保存する。Hierarchy ウィンドウから Project ウィンドウに GameObject をドラッグ＆ドロップすると、プレハブになる。プレハブにしたエフェクトは、別のシーンで使ったり、スクリプトから生成したりできる（第 10 章を参照）。

Particle System の設定は、プレハブの中にすべて保存される。マテリアルは別のアセットとして保存されるため、プレハブと一緒に管理する。
