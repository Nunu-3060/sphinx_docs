第 9 章 スクリプトからの制御
============================

ここまでは、Inspector ウィンドウの設定だけでエフェクトを作ってきた。ゲームでは、ボタンを押したときに再生したり、状況に応じて量や色を変えたりする必要がある。この章では、C# スクリプトから Particle System を制御する方法を説明する。

この章のサンプルコードは、``examples/chapter09`` フォルダーにある。サンプルは、キーボードとマウスの入力に Input System パッケージを使う（第 1 章を参照）。

再生と停止
----------

スクリプトから Particle System を操作するには、``ParticleSystem`` 型のコンポーネントを取得する。再生と停止には、次のメソッドを使う。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - メソッド
     - 内容
   * - ``Play()``
     - 再生する。停止中なら最初から再生し、一時停止中なら続きから再生する。
   * - ``Pause()``
     - 一時停止する。パーティクルはその場で止まる。
   * - ``Stop()``
     - 停止する。止め方は引数で指定する（後述）。
   * - ``Clear()``
     - 放出済みのパーティクルをすべて消す。
   * - ``Emit(int count)``
     - 指定した数のパーティクルを、すぐに放出する。

また、次のプロパティで状態を調べられる。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - プロパティ
     - 内容
   * - ``isPlaying``
     - 再生中なら ``true``。放出が止まった後も、パーティクルが残っている間は ``true`` である。
   * - ``isEmitting``
     - 放出中なら ``true``。
   * - ``isPaused``
     - 一時停止中なら ``true``。
   * - ``particleCount``
     - 現在存在するパーティクルの数。

``Play``、``Pause``、``Stop``、``Clear`` の各メソッドは、既定では子の GameObject の Particle System にも同じ操作を行う。第 1 引数に ``false`` を渡すと、自分だけを操作する。

次のサンプルは、キー入力で再生と停止を切り替える。

.. literalinclude:: ../../examples/chapter09/ParticlePlayback.cs
   :language: csharp
   :caption: ParticlePlayback.cs
   :linenos:

:download:`ParticlePlayback.cs をダウンロード <../../examples/chapter09/ParticlePlayback.cs>`

スクリプトを Particle System の GameObject にアタッチし、再生モードにする。P キーで再生、Space キーで一時停止、S キーと C キーで停止する。

``Stop`` メソッドの第 2 引数には、止め方を指定する。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 値
     - 内容
   * - ``ParticleSystemStopBehavior.StopEmitting``
     - 放出だけを止める。放出済みのパーティクルは、寿命が尽きるまで動き続ける。
   * - ``ParticleSystemStopBehavior.StopEmittingAndClear``
     - 放出を止め、放出済みのパーティクルもすべて消す。

炎を消すときに ``StopEmitting`` を使うと、残ったパーティクルが燃え尽きるように自然に消えていく。``StopEmittingAndClear`` を使うと、その瞬間にすべてが消える。

好きなタイミングで放出する
--------------------------

``Emit`` メソッドを使うと、Emission モジュールの設定とは関係なく、好きなタイミングでパーティクルを放出できる。次のサンプルは、マウスでクリックした位置にパーティクルをまとめて放出する。

.. literalinclude:: ../../examples/chapter09/BurstOnClick.cs
   :language: csharp
   :caption: BurstOnClick.cs
   :linenos:

:download:`BurstOnClick.cs をダウンロード <../../examples/chapter09/BurstOnClick.cs>`

使う前に、Particle System を次のように設定しておく。

* Main モジュールの :guilabel:`Simulation Space` を :guilabel:`World` にする。:guilabel:`Local` のままだと、次にクリックしたときに GameObject と一緒に、放出済みのパーティクルも移動してしまう。
* Emission モジュールを無効にする。有効のままだと、クリックしなくてもパーティクルが放出される。
* Shape モジュールの :guilabel:`Shape` を :guilabel:`Sphere` にすると、クリックした位置から四方に広がる。

Particle System は、Main モジュールの :guilabel:`Play On Awake` によって、再生モードになると同時に再生を始める。Emission モジュールが無効なので、再生中でも ``Emit`` を呼ぶまでパーティクルは放出されない。

``Emit`` メソッドは、Main モジュールの初期値と Shape モジュールの形を使ってパーティクルを放出する。位置や色などを 1 回の放出ごとに変えたい場合は、``ParticleSystem.EmitParams`` 型の値を渡す（後述の ParticleCollisionHandler.cs を参照）。

モジュールの値を変える
----------------------

モジュールの値を変えるには、``main`` や ``emission`` などのプロパティでモジュールを取得し、そのプロパティに値を代入する。

.. literalinclude:: ../../examples/chapter09/ModifyModules.cs
   :language: csharp
   :caption: ModifyModules.cs
   :linenos:

:download:`ModifyModules.cs をダウンロード <../../examples/chapter09/ModifyModules.cs>`

スクリプトを Particle System の GameObject にアタッチし、再生モードにする。上矢印キーと下矢印キーで放出数が増減し、R キーで色が変わる。色が変わるのはこれから放出するパーティクルだけで、放出済みのパーティクルの色は変わらない。

モジュールは構造体
~~~~~~~~~~~~~~~~~~

``ParticleSystem.MainModule`` や ``ParticleSystem.EmissionModule`` は構造体（値型）である。C# では、プロパティで取得した構造体は元の値のコピーになるため、次のように書くとコンパイルエラー（CS1612）になる。

.. code-block:: csharp

   // コンパイルエラーになる
   _particleSystem.emission.rateOverTime = 20f;

そのため、サンプルの ``SetRate`` メソッドのように、いったんモジュールを変数に代入してから値を設定する。

.. code-block:: csharp

   ParticleSystem.EmissionModule emission = _particleSystem.emission;
   emission.rateOverTime = 20f;

モジュールの構造体は、Particle System の本体への参照を持っている。そのため、変数に代入したモジュールのプロパティに値を代入すると、Particle System に直接反映される。通常の構造体と違い、変更したモジュールを Particle System に代入し直す必要はない。

カーブとランダムな値
~~~~~~~~~~~~~~~~~~~~

``rateOverTime`` や ``startSpeed`` などのプロパティは、``ParticleSystem.MinMaxCurve`` 型である。この型は、第 4 章で説明した 4 つの指定方法のどれでも表せる。``float`` 型の値を代入すると、:guilabel:`Constant` の指定になる。2 つの値の間のランダムな値にするには、次のように書く。

.. code-block:: csharp

   ParticleSystem.MainModule main = _particleSystem.main;
   main.startSpeed = new ParticleSystem.MinMaxCurve(2f, 5f);

色の ``startColor`` プロパティは、``ParticleSystem.MinMaxGradient`` 型である。``Color`` 型の値を代入すると、:guilabel:`Color` の指定になる。

Inspector ウィンドウで設定したカーブの形は変えずに、全体の大きさだけを変えたい場合は、``startSpeedMultiplier`` のように名前の最後に ``Multiplier`` が付いたプロパティを使う。カーブの値に、このプロパティの値が掛け合わされる。

衝突を検出する
--------------

Collision モジュールの :guilabel:`Send Collision Messages` を有効にすると、パーティクルがコライダーに衝突したときに ``OnParticleCollision`` メソッドが呼ばれる。このメソッドは、Particle System の GameObject のスクリプトと、衝突した相手の GameObject のスクリプトの両方で呼ばれる。

次のサンプルは、パーティクルが衝突した位置に、別の Particle System で水しぶきを出す。

.. literalinclude:: ../../examples/chapter09/ParticleCollisionHandler.cs
   :language: csharp
   :caption: ParticleCollisionHandler.cs
   :linenos:

:download:`ParticleCollisionHandler.cs をダウンロード <../../examples/chapter09/ParticleCollisionHandler.cs>`

使う手順は次のとおりである。

#. 地面にする Plane を配置する。Plane には、最初から Mesh Collider が付いている。
#. 地面の上に、下向きにパーティクルを放出する Particle System を置く。Collision モジュールを有効にし、:guilabel:`Type` を :guilabel:`World` に、:guilabel:`Send Collision Messages` を有効にする。:guilabel:`Lifetime Loss` を 1 にすると、衝突したパーティクルが消える。
#. 水しぶき用の Particle System を作る。Main モジュールの :guilabel:`Simulation Space` を :guilabel:`World` に、:guilabel:`Gravity Modifier` を 1 にし、Emission モジュールを無効にする。Shape モジュールの :guilabel:`Shape` を :guilabel:`Hemisphere` にし、:guilabel:`Radius` を 0.1 程度にする。
#. 1 つ目の Particle System にスクリプトをアタッチし、:guilabel:`Splash Effect` に水しぶき用の Particle System を設定する。

``OnParticleCollision`` メソッドの引数は衝突した相手の GameObject で、どこに衝突したかは分からない。衝突の位置や速度は、``GetCollisionEvents`` メソッドで取得する。1 フレームの間に複数のパーティクルが同じ相手に衝突した場合、``OnParticleCollision`` メソッドは相手ごとに 1 回だけ呼ばれ、``GetCollisionEvents`` メソッドでそのすべての衝突の情報を取得する。

``EmitParams`` 型の値で放出位置を指定すると、Main モジュールの初期値のうち、指定した値だけを置き換えて放出できる。``applyShapeToPosition`` を ``true`` にすると、指定した位置を中心にして、Shape モジュールの形の分だけ放出位置がばらつく。

なお、Triggers モジュールで :guilabel:`Callback` を選んだ場合は、``OnParticleTrigger`` メソッドが呼ばれる。条件に当てはまるパーティクルは、``GetTriggerParticles`` メソッドで取得する。

パーティクルを直接操作する
--------------------------

``GetParticles`` メソッドを使うと、放出済みのパーティクルの位置、速度、色などを配列にコピーできる。配列の値を書き換えて ``SetParticles`` メソッドで書き戻すと、モジュールでは作れない独自の動きを付けられる。

次のサンプルは、パーティクルを目標の位置に向かって加速させる。

.. literalinclude:: ../../examples/chapter09/ParticleAttractor.cs
   :language: csharp
   :caption: ParticleAttractor.cs
   :linenos:

:download:`ParticleAttractor.cs をダウンロード <../../examples/chapter09/ParticleAttractor.cs>`

使う手順は次のとおりである。

#. Particle System の Main モジュールの :guilabel:`Simulation Space` を :guilabel:`World` にする。
#. 目標にする GameObject（Sphere など）をシーンに配置する。
#. Particle System の GameObject にスクリプトをアタッチし、:guilabel:`Target` に目標の GameObject を設定する。

再生モードにすると、放出されたパーティクルが目標の方に曲がっていく。再生中に目標を動かすと、パーティクルが目標を追いかける。

パーティクルの位置 :math:`\mathbf{p}` から目標の位置 :math:`\mathbf{q}` に向かう単位ベクトルを :math:`\hat{\mathbf{d}}`、加速度の大きさを :math:`a`、前のフレームからの経過時間を :math:`\Delta t` とする。サンプルは、毎フレーム次の式で速度 :math:`\mathbf{v}` を更新している。

.. math::

   \hat{\mathbf{d}} = \frac{\mathbf{q} - \mathbf{p}}{|\mathbf{q} - \mathbf{p}|}, \qquad \mathbf{v} \leftarrow \mathbf{v} + a \, \hat{\mathbf{d}} \, \Delta t

更新した速度に従ってパーティクルを動かすのは、Particle System 自身である。スクリプトは速度を変えるだけでよい。

``GetParticles`` メソッドで取得するパーティクルの位置は、:guilabel:`Simulation Space` の座標系で表される。:guilabel:`Local` の場合は、Particle System の GameObject を基準にした座標になるため、ワールド座標の目標の位置とそのまま比べることはできない。サンプルで :guilabel:`Simulation Space` を :guilabel:`World` にしているのはこのためである。

``GetParticles`` と ``SetParticles`` は、すべてのパーティクルを C# の配列にコピーするため、パーティクルの数が多いと処理が重くなる。同じことをモジュールで実現できる場合は、モジュールを使うほうがよい。たとえば、この例の動きは、Particle System Force Field（第 6 章を参照）でも作れる。

再生の終わりを知る
------------------

Main モジュールの :guilabel:`Stop Action` を :guilabel:`Callback` にすると、再生が終わったときに ``OnParticleSystemStopped`` メソッドが呼ばれる。このメソッドは、Particle System の GameObject にアタッチしたスクリプトで受け取る。使い方は、第 11 章のオブジェクトプールのサンプルで説明する。
