第 11 章 パフォーマンス
=======================

パーティクルは、少しの設定の変更で数が何倍にも増えるため、気付かないうちにゲームの処理を重くしやすい。この章では、パーティクルの処理が重くなる原因と対策、処理の重さを調べる方法、エフェクトを使い回すオブジェクトプールを説明する。

この章のサンプルコードは、``examples/chapter11`` フォルダーにある。

処理が重くなる原因
------------------

パーティクルの処理の重さは、主に次の 3 つに分けられる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 原因
     - 内容
   * - シミュレーション（CPU）
     - パーティクルの位置や色などを毎フレーム計算する処理。パーティクルの数と、有効にしているモジュールの数に比例して重くなる。Noise モジュールと、:guilabel:`Type` が :guilabel:`World` の Collision モジュールは、特に計算が多い。
   * - 描画の命令（CPU）
     - GPU に描画を命令する処理。Particle System の数とマテリアルの数が多いほど、命令の数（ドローコール）が増える。
   * - オーバードロー（GPU）
     - 同じピクセルを何度も塗り重ねる処理。大きな半透明のパーティクルが重なるほど重くなる（後述）。

どれが原因かによって、有効な対策が異なる。まずは後述のプロファイラーで原因を調べてから対策する。

オーバードロー
~~~~~~~~~~~~~~

不透明なオブジェクトは、手前のオブジェクトに隠れたピクセルを塗らずに済ませられる。一方、半透明のパーティクルは、奥のパーティクルが透けて見えるため、重なったパーティクルをすべて塗る必要がある。同じピクセルを何度も塗り重ねることを、オーバードローという。

画面を覆うほど大きなパーティクルが 10 枚重なると、画面のすべてのピクセルを 10 回塗ることになる。パーティクルの数が少なくても、1 つ 1 つが大きいと GPU の負荷が高くなる。特に、カメラのすぐ近くにあるパーティクルは、画面の大部分を覆うため負荷が高い。

URP では、:menuselection:`Window --> Analysis --> Rendering Debugger` の :guilabel:`Rendering` タブで :guilabel:`Overdraw Mode` を選ぶと、オーバードローの多い場所が明るく表示される。

対策
----

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 対策
     - 内容
   * - パーティクルの数を減らす
     - :guilabel:`Rate over Time` や :guilabel:`Start Lifetime` を減らす。同時に存在する数は :math:`r \times L` で見積もれる（第 5 章を参照）。見た目を保つには、数を減らした分、1 つ 1 つを大きくしたり、テクスチャーの形を工夫したりする。
   * - :guilabel:`Max Particles` を設定する
     - 設定のミスや想定外の状況で、パーティクルが増えすぎるのを防ぐ上限になる。
   * - パーティクルを大きくしすぎない
     - オーバードローを減らす。Renderer モジュールの :guilabel:`Max Particle Size` で、画面に対する大きさの上限を決めることもできる。
   * - テクスチャーの透明な部分を減らす
     - 透明な部分も、塗る処理は行われる。形の周りの余白が小さいテクスチャーを使う。
   * - 重いモジュールを見直す
     - Noise モジュールの :guilabel:`Quality` や :guilabel:`Octaves` を下げる。衝突が平らな地面だけでよい場合は、Collision モジュールの :guilabel:`Type` を :guilabel:`Planes` にする。
   * - マテリアルを共有する
     - 同じ見た目のエフェクトには、同じマテリアルを使う。
   * - 画面外の計算を止める
     - Main モジュールの :guilabel:`Culling Mode` を設定する（後述）。

Culling Mode
~~~~~~~~~~~~

Main モジュールの :guilabel:`Culling Mode` は、Particle System が画面の外にあるときに、シミュレーションを止めるかどうかを決める。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 値
     - 内容
   * - :guilabel:`Automatic`
     - :guilabel:`Looping` が有効なら :guilabel:`Pause` と同じ動作、無効なら :guilabel:`Always Simulate` と同じ動作をする。
   * - :guilabel:`Pause And Catch-up`
     - 画面の外にある間は止め、画面に戻ったときに止めていた時間の分を一度に計算して、遅れを取り戻す。
   * - :guilabel:`Pause`
     - 画面の外にある間は止める。画面に戻ると、止めたところから再開する。
   * - :guilabel:`Always Simulate`
     - 画面の外にあっても計算を続ける。

画面の中にあるかどうかは、パーティクル全体を囲むバウンディングボックスで判定する。バウンディングボックスは、Particle Effect パネルの :guilabel:`Show Bounds` で確認できる（第 3 章を参照）。

処理の重さを調べる
------------------

プロファイラー
~~~~~~~~~~~~~~

:menuselection:`Window --> Analysis --> Profiler` で開くプロファイラーでは、フレームごとの処理時間の内訳を調べられる。

#. プロファイラーを開き、再生モードにする。
#. :guilabel:`CPU Usage` のグラフで、処理時間が長いフレームをクリックする。
#. 下部の表示を :guilabel:`Hierarchy` にし、名前に「Particle」を含む項目の処理時間を確認する。

プロファイラーは、Unity のエディター自体の処理も含めて計測する。正確な値を知りたい場合は、ゲームをビルドし、ビルドしたゲームにプロファイラーを接続して計測する。

Frame Debugger
~~~~~~~~~~~~~~

:menuselection:`Window --> Analysis --> Frame Debugger` で開く Frame Debugger では、1 フレームの描画の命令を 1 つずつ確認できる。:guilabel:`Enable` を押すと、再生中のフレームが止まり、描画の命令の一覧が表示される。一覧の項目を選ぶと、その命令までに描画された画面が表示される。どの Particle System が、どの順番で、何回の命令で描画されているかを確認できる。

Game ビューの :guilabel:`Stats` ボタンを押すと、描画の命令の数（:guilabel:`Batches`）などの統計情報が表示される。エフェクトを再生する前と後で値を比べると、エフェクトによって増えた命令の数が分かる。

オブジェクトプール
------------------

第 10 章では、ヒットエフェクトのプレハブを ``Instantiate`` メソッドで生成し、再生が終わると :guilabel:`Stop Action` の :guilabel:`Destroy` で削除した。GameObject の生成と削除は処理が重く、削除したオブジェクトのメモリーはガベージコレクションで回収される。ガベージコレクションが動くと、ゲームが一瞬止まることがある。弾が当たるたびにエフェクトを生成するような、頻繁に使うエフェクトでは、この処理が問題になる。

そこで、一度生成したエフェクトを削除せずに無効にして取っておき、次に必要になったときに有効にして使い回す。この方法をオブジェクトプールという。Unity には、オブジェクトプールを作るための ``UnityEngine.Pool.ObjectPool<T>`` クラスが用意されている。

次の 3 つのスクリプトで、第 10 章のヒットエフェクトをオブジェクトプールで使い回す。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - スクリプト
     - 役割
   * - EffectPool.cs
     - エフェクトを保持するプール。取り出されたエフェクトを、指定した位置で再生する。
   * - PooledEffect.cs
     - エフェクトのプレハブに付けるスクリプト。再生が終わると、自分をプールに戻す。
   * - PooledHitEffectSpawner.cs
     - クリックした位置で、プールのエフェクトを再生する。

.. literalinclude:: ../../examples/chapter11/EffectPool.cs
   :language: csharp
   :caption: EffectPool.cs
   :linenos:

:download:`EffectPool.cs をダウンロード <../../examples/chapter11/EffectPool.cs>`

``ObjectPool<T>`` のコンストラクターには、次の引数を渡す。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 引数
     - 内容
   * - ``createFunc``
     - プールに空きがないときに、新しいオブジェクトを生成するメソッド。
   * - ``actionOnGet``
     - プールからオブジェクトを取り出すときに呼ぶメソッド。
   * - ``actionOnRelease``
     - プールにオブジェクトを戻すときに呼ぶメソッド。
   * - ``actionOnDestroy``
     - プールがいっぱいで戻せないオブジェクトを削除するメソッド。
   * - ``collectionCheck``
     - ``true`` にすると、同じオブジェクトを 2 回戻すような誤りを検出する。検出の処理はエディター上でだけ行われる。
   * - ``defaultCapacity``
     - オブジェクトを保持するリストの、最初の大きさ。
   * - ``maxSize``
     - プールに保持するオブジェクトの最大数。

.. literalinclude:: ../../examples/chapter11/PooledEffect.cs
   :language: csharp
   :caption: PooledEffect.cs
   :linenos:

:download:`PooledEffect.cs をダウンロード <../../examples/chapter11/PooledEffect.cs>`

``Awake`` メソッドで Main モジュールの :guilabel:`Stop Action` を :guilabel:`Callback` にしている。再生が終わると ``OnParticleSystemStopped`` メソッドが呼ばれ、自分をプールに戻す。プールに戻すと、EffectPool.cs の ``OnReleaseEffect`` メソッドで GameObject が無効になる。

.. literalinclude:: ../../examples/chapter11/PooledHitEffectSpawner.cs
   :language: csharp
   :caption: PooledHitEffectSpawner.cs
   :linenos:

:download:`PooledHitEffectSpawner.cs をダウンロード <../../examples/chapter11/PooledHitEffectSpawner.cs>`

使う手順は次のとおりである。

#. 第 10 章の HitEffect のプレハブを複製し、名前を「PooledHitEffect」にする。
#. PooledHitEffect のルートの GameObject に、PooledEffect.cs をアタッチする。Main モジュールの :guilabel:`Play On Awake` を無効にする。子の Flash の :guilabel:`Play On Awake` も無効にする。
#. シーンに空の GameObject を作り、名前を「EffectPool」にする。EffectPool.cs をアタッチし、:guilabel:`Effect Prefab` に PooledHitEffect を設定する。
#. 第 10 章の HitEffectSpawner の GameObject から HitEffectSpawner.cs を削除し、代わりに PooledHitEffectSpawner.cs をアタッチする。:guilabel:`Effect Pool` に EffectPool の GameObject を設定する。

再生モードでオブジェクトをクリックすると、第 10 章と同じようにヒットエフェクトが表示される。Hierarchy ウィンドウで EffectPool の子を見ると、エフェクトの GameObject が削除されずに残り、再生が終わると無効になって、次のクリックで再び使われることが分かる。

:guilabel:`Play On Awake` を無効にするのは、プールから取り出して GameObject を有効にした時点で、位置を設定する前に再生が始まるのを防ぐためである。再生は、位置を設定した後に EffectPool.cs の ``Play`` メソッドから始める。
