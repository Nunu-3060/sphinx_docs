第 11 章 グラフィックスの基礎
=============================

この章では、ゲームの見た目を決めるカメラ、ライト、マテリアルの基本と、ライトのベイク、パーティクルによるエフェクトについて説明します。

この章のサンプルコードは、``examples/chapter11`` フォルダーにあります。

レンダーパイプライン
--------------------

**レンダーパイプライン** は、シーンを画面に描画するための一連の処理のことです。Unity には、次の 3 種類のレンダーパイプラインがあります。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - レンダーパイプライン
     - 特徴
   * - URP（Universal Render Pipeline）
     - スマートフォンから PC、家庭用ゲーム機まで、幅広いプラットフォームで動作します。性能と品質のバランスが良く、本資料ではこれを使います。
   * - HDRP（High Definition Render Pipeline）
     - 高性能な PC や家庭用ゲーム機向けに、写実的な高品質の描画を行います。
   * - Built-in Render Pipeline
     - 従来から使われているレンダーパイプラインです。現在は新規のプロジェクトでは URP が推奨されています。

レンダーパイプラインによって、使えるシェーダーやマテリアルの設定が異なります。インターネット上の資料や Asset Store のアセットを使うときは、どのレンダーパイプライン向けのものかを確認してください。Built-in Render Pipeline 向けのマテリアルを URP のプロジェクトで使うと、マゼンタ（ピンク色）で表示されます。

カメラ
------

Game ビューに表示される画面は、シーンに配置した **カメラ**\ （Camera コンポーネント）から見た映像です。新しいシーンには、``Main Camera`` という名前のカメラが最初から配置されています。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プロパティ
     - 意味
   * - :guilabel:`Projection`
     - 投影の方式です。:guilabel:`Perspective`\ （透視投影）では遠くの物ほど小さく見え、:guilabel:`Orthographic`\ （平行投影）では距離に関係なく同じ大きさで見えます。3D ゲームでは透視投影、2D ゲームや見下ろし型の画面では平行投影がよく使われます。
   * - :guilabel:`Field of View`
     - 透視投影での視野角（度）です。大きいほど広い範囲が映ります。
   * - :guilabel:`Clipping Planes`
     - 描画する距離の範囲です。:guilabel:`Near` より近い物と :guilabel:`Far` より遠い物は描画されません。
   * - :guilabel:`Background Type`
     - 何も描画されない部分（背景）に表示するものです。スカイボックスや単色を選べます。

カメラの動きを細かく制御したい場合は、**Cinemachine** パッケージが便利です。Cinemachine を使うと、対象の追従、なめらかな視点の切り替え、手ぶれのような揺れなどを、スクリプトを書かずに設定できます。

ライト
------

ライトの種類
~~~~~~~~~~~~

シーンを照らす光源は、Light コンポーネントで表します。新しいシーンには、太陽光を表す ``Directional Light`` が最初から配置されています。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - ライト
     - 特徴
   * - Directional Light
     - 太陽光のように、無限に遠くから一定の方向に照らします。位置は関係なく、向きだけが影響します。
   * - Point Light
     - 電球のように、1 点からすべての方向に照らします。距離が離れるほど暗くなります。
   * - Spot Light
     - 懐中電灯のように、1 点から円錐形の範囲を照らします。
   * - Area Light
     - 長方形や円盤の面から照らします。URP では、ライトのベイク（後述）でのみ使えます。

ライトの :guilabel:`Mode` の設定
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ライトの計算には時間がかかります。そのため、Unity では、ライトの計算をゲームの実行中に行うか、事前に行っておくかを、ライトごとに :guilabel:`Mode` で選べます。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Mode
     - 特徴
   * - Realtime
     - 実行中に毎フレーム計算します。ライトを動かしたり色を変えたりできますが、処理が重くなります。
   * - Baked
     - 事前に計算した結果をテクスチャ（ライトマップ）に保存し、実行中はそれを貼り付けるだけにします。処理は軽くなりますが、実行中にライトを変化させることはできません。
   * - Mixed
     - Realtime と Baked を組み合わせます。例えば、間接光は事前に計算しておき、直接光と動く物の影は実行中に計算する、といった使い方ができます。

ライトのベイク
--------------

**ライトのベイク** は、ライトの計算を事前に行い、その結果を保存しておくことです。ベイクすると、壁に反射した光が周囲を照らす効果（間接光、グローバルイルミネーション）など、実行中に計算すると重い効果も、軽い処理で表示できます。建物の中のように、動かない物が多いシーンで特に効果があります。

基本的な手順は次のとおりです。

#. ベイクの対象にする動かない GameObject（地面、壁、建物など）を選び、Inspector ウィンドウの右上にある :guilabel:`Static` のチェックボックスを有効にします。これにより、:guilabel:`Contribute GI` の設定も有効になり、ライトマップの計算の対象になります。
#. ベイクに使うライトを選び、Light コンポーネントの :guilabel:`Mode` を :guilabel:`Baked` または :guilabel:`Mixed` にします。
#. :menuselection:`Window --> Rendering --> Lighting` で Lighting ウィンドウを開きます。
#. :guilabel:`Scene` タブの :guilabel:`Lighting Settings Asset` が空の場合は、:guilabel:`New Lighting Settings` をクリックして設定のアセットを作成します。
#. ウィンドウの下部にある :guilabel:`Generate Lighting` をクリックします。計算が終わると、ベイクした結果がシーンに反映されます。

ベイクの結果は、シーンと同じ名前のフォルダーにアセットとして保存されます。ベイクの対象の GameObject を動かしたり、ライトの設定を変えたりした場合は、もう一度 :guilabel:`Generate Lighting` を実行する必要があります。

動く GameObject（キャラクターなど）はライトマップを使えないため、ベイクした間接光の効果を受けられません。動く GameObject にも間接光の効果を与えるには、**ライトプローブ** を使います。ライトプローブは、空間の各点での光の情報を事前に計算して保存しておくしくみです。:menuselection:`GameObject --> Light --> Light Probe Group` で配置できます。

.. note::

   ベイクの計算には、シーンの規模によっては数分から数十分かかることがあります。学習の段階では、まずすべてのライトを Realtime のままにしておき、処理の重さや見た目の品質が問題になってからベイクを検討してもかまいません。

マテリアル、シェーダー、テクスチャ
----------------------------------

GameObject の表面の見た目は、マテリアル、シェーダー、テクスチャの組み合わせで決まります。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 要素
     - 役割
   * - シェーダー
     - 光の当たり方から表面の色を計算するプログラムです。金属のような質感、透明なガラス、アニメ調の塗りなど、表現の方式を決めます。
   * - マテリアル
     - シェーダーと、そのシェーダーに渡す設定値（色、テクスチャ、滑らかさなど）の組み合わせです。アセットとして保存し、Mesh Renderer などに設定して使います。
   * - テクスチャ
     - 表面に貼り付ける画像です。色だけでなく、凹凸（ノーマルマップ）などの情報を表すテクスチャもあります。

マテリアルを作成するには、Project ウィンドウを右クリックし、:menuselection:`Create --> Material` を選びます。URP のプロジェクトでは、既定で ``Universal Render Pipeline/Lit`` シェーダーが使われます。このシェーダーの主な設定は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プロパティ
     - 意味
   * - :guilabel:`Base Map`
     - 表面の色と、色を表すテクスチャです。
   * - :guilabel:`Metallic Map`
     - 金属らしさです。1 に近いほど金属のように周囲を映り込ませます。
   * - :guilabel:`Smoothness`
     - 表面の滑らかさです。1 に近いほど、光沢が強くなります。
   * - :guilabel:`Normal Map`
     - 表面の細かな凹凸を表すテクスチャです。
   * - :guilabel:`Emission`
     - 自ら光っているように見せる設定です。

作成したマテリアルは、Scene ビューや Hierarchy ウィンドウの GameObject にドラッグ＆ドロップすると設定できます。

パーティクル
------------

炎、煙、火花、爆発、魔法の光など、細かな粒が大量に動く表現は **パーティクル** で作ります。Unity では、**Particle System** コンポーネントを使います。

Particle System の作成
~~~~~~~~~~~~~~~~~~~~~~

:menuselection:`GameObject --> Effects --> Particle System` を選ぶと、Particle System が付いた GameObject が作成され、Scene ビューで白い粒が上に向かって放出され始めます。

Particle System の設定は、機能ごとの **モジュール** に分かれています。Inspector ウィンドウで各モジュールの名前をクリックすると、設定が開きます。主なモジュールと設定は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - モジュール
     - 主な設定
   * - メインモジュール
     - :guilabel:`Duration`\ （放出を続ける時間）、:guilabel:`Looping`\ （繰り返すかどうか）、:guilabel:`Start Lifetime`\ （粒が消えるまでの時間）、:guilabel:`Start Speed`\ （初速）、:guilabel:`Start Size`\ （大きさ）、:guilabel:`Start Color`\ （色）、:guilabel:`Gravity Modifier`\ （重力の影響）、:guilabel:`Stop Action`\ （放出が終わったときの動作）
   * - Emission
     - 1 秒あたりに放出する粒の数（:guilabel:`Rate over Time`）や、一度に放出する粒の数（:guilabel:`Bursts`）
   * - Shape
     - 粒を放出する範囲の形状（円錐、球、箱など）
   * - Color over Lifetime
     - 粒が生まれてから消えるまでの色と透明度の変化
   * - Size over Lifetime
     - 粒が生まれてから消えるまでの大きさの変化
   * - Renderer
     - 粒の描画方法と、使用するマテリアル

例えば、アイテムを取ったときの火花のようなエフェクトは、次のように設定すると作れます。

#. メインモジュールの :guilabel:`Duration` を 0.5、:guilabel:`Looping` を無効、:guilabel:`Start Lifetime` を 0.5、:guilabel:`Start Speed` を 5、:guilabel:`Start Size` を 0.1 にします。
#. メインモジュールの :guilabel:`Stop Action` を :guilabel:`Destroy` にします。放出が終わり、すべての粒が消えると、GameObject が自動的に破棄されます。
#. :guilabel:`Emission` の :guilabel:`Rate over Time` を 0 にし、:guilabel:`Bursts` の :guilabel:`+` をクリックして、:guilabel:`Count` を 30 にします。再生を始めた瞬間に 30 個の粒が一度に放出されるようになります。
#. :guilabel:`Shape` の :guilabel:`Shape` を :guilabel:`Sphere` にします。すべての方向に粒が飛び散るようになります。
#. :guilabel:`Color over Lifetime` を有効にし、終わりに近づくにつれて透明になるように設定します。
#. 作成した GameObject を Project ウィンドウにドラッグ＆ドロップして Prefab にします。

この Prefab を ``Instantiate`` で生成すると、その位置でエフェクトが 1 回再生され、自動的に消えます。:doc:`ch16_tutorial` では、この方法でアイテムを取ったときのエフェクトを表示します。

スクリプトからの制御
~~~~~~~~~~~~~~~~~~~~

スクリプトからは、``Play``\ （再生）、``Stop``\ （停止）、``Emit``\ （指定した数の粒を即座に放出）などのメソッドで Particle System を制御できます。

.. literalinclude:: ../../examples/chapter11/ParticleBurst.cs
   :caption: ParticleBurst.cs
   :linenos:

:download:`ParticleBurst.cs をダウンロード <../../examples/chapter11/ParticleBurst.cs>`

このスクリプトを付けた GameObject の :guilabel:`Particle System` に Particle System を設定して再生すると、スペースキーを押すたびに 30 個の粒が放出されます。Particle System の :guilabel:`Emission` の :guilabel:`Rate over Time` を 0 にしておくと、スペースキーで放出した粒だけが表示されるので、わかりやすくなります。

.. note::

   Particle System は CPU で粒を計算します。数十万個といった大量の粒を扱う場合は、GPU で計算する **Visual Effect Graph**\ （VFX Graph）パッケージを使う方法もあります。ただし、VFX Graph は対応するプラットフォームが限られるため、まずは Particle System で作ることをお勧めします。
