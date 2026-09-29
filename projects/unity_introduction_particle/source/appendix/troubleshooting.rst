付録 B よくあるトラブルと対処法
===============================

Particle System と VFX Graph でよく起こるトラブルと、その対処法をまとめる。

Particle System
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 症状
     - 原因と対処法
   * - パーティクルが表示されない
     - Emission モジュールの :guilabel:`Rate over Time` が 0 になっていないか、Emission モジュールが無効になっていないかを確認する。:guilabel:`Start Lifetime`、:guilabel:`Start Size`、:guilabel:`Start Color` の不透明度が 0 になっていないかも確認する。
   * - エディターで再生されない
     - エディター上では、Particle System は選択している間だけ再生される（第 3 章を参照）。Hierarchy ウィンドウで GameObject を選択する。
   * - パーティクルがピンク色で表示される
     - マテリアルのシェーダーが、URP に対応していない。Built-in Render Pipeline 用のシェーダーを使っている場合は、:menuselection:`Universal Render Pipeline --> Particles --> Unlit` などに変更する（第 7 章を参照）。
   * - パーティクルの四角い輪郭が見える
     - テクスチャーの外側が透明になっていないか、マテリアルの :guilabel:`Surface Type` が :guilabel:`Opaque` になっている。テクスチャーとマテリアルの設定を確認する（第 7 章を参照）。
   * - パーティクルが地面と交わる部分に直線の境目が見える
     - マテリアルの :guilabel:`Soft Particles` を有効にし、URP Asset の :guilabel:`Depth Texture` を有効にする（第 7 章を参照）。
   * - 半透明のパーティクルの前後関係がおかしい、ちらつく
     - Renderer モジュールの :guilabel:`Sort Mode` を :guilabel:`By Distance` にする。複数の Particle System の間の順番は、:guilabel:`Sorting Fudge` やマテリアルの :guilabel:`Sorting Priority` で固定する（第 7 章を参照）。
   * - GameObject を動かすと、放出済みのパーティクルが付いてくる
     - Main モジュールの :guilabel:`Simulation Space` を :guilabel:`World` にする（第 4 章を参照）。
   * - 設定した頻度でパーティクルが放出されない
     - 同時に存在するパーティクルの数が :guilabel:`Max Particles` に達している。:math:`r \times L` を見積もり、:guilabel:`Max Particles` を増やすか、放出の頻度か寿命を減らす（第 5 章を参照）。
   * - パーティクルがコライダーをすり抜ける
     - Collision モジュールの :guilabel:`Quality` を :guilabel:`High` にする。動いているコライダーの場合は、:guilabel:`Enable Dynamic Colliders` を有効にする（第 8 章を参照）。
   * - ``OnParticleCollision`` が呼ばれない
     - Collision モジュールの :guilabel:`Send Collision Messages` を有効にする。:guilabel:`Collides With` に、相手のレイヤーが含まれているかも確認する（第 8 章、第 9 章を参照）。
   * - スクリプトでモジュールの値を代入するとコンパイルエラー（CS1612）になる
     - モジュールをいったん変数に代入してから、値を設定する（第 9 章を参照）。
   * - 画面の端でエフェクトが急に消える
     - バウンディングボックスが、実際のパーティクルの範囲より小さい可能性がある。Particle Effect パネルの :guilabel:`Show Bounds` で確認する（第 3 章、第 11 章を参照）。

VFX Graph
---------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 症状
     - 原因と対処法
   * - VFX Graph のアセットを作るメニューがない
     - Visual Effect Graph パッケージが導入されていない。Package Manager ウィンドウから導入する（第 12 章を参照）。
   * - エフェクトが再生されない
     - Spawn コンテキストが OnPlay などのイベントにつながっているか、Visual Effect コンポーネントの :guilabel:`Asset Template` にアセットが設定されているかを確認する。コンピュートシェーダーに対応しない環境では、VFX Graph は動作しない。
   * - グラフの変更が反映されない
     - VFX Graph ウィンドウで変更を保存したかを確認する（第 12 章を参照）。
   * - 放出されるパーティクルが設定より少ない
     - Initialize Particle コンテキストの :guilabel:`Capacity` が足りない。:math:`r \times L` を見積もって :guilabel:`Capacity` を増やす（第 12 章を参照）。
   * - カメラの向きによってエフェクトが消える
     - Initialize Particle コンテキストのバウンディングボックスが小さすぎる。:guilabel:`Bounds` を大きくするか、:guilabel:`Bounds Setting Mode` を変える（第 12 章を参照）。
   * - C# から設定したプロパティの値が反映されない
     - Blackboard でプロパティの :guilabel:`Exposed` が有効になっているか、名前と型がスクリプトと一致しているかを確認する（第 13 章を参照）。
