第 4 章 Main モジュール
=======================

Main モジュールは、Particle System 全体の動作と、放出するパーティクルの初期値を決めるモジュールである。この章では、Main モジュールの主な設定項目と、値の指定方法を説明する。

再生時間の設定
--------------

Particle System は、:guilabel:`Duration` で決めた時間を 1 周期として動作する。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Duration`
     - 1 周期の長さ（秒）。放出を続ける時間であり、パーティクルの寿命とは別の値である。
   * - :guilabel:`Looping`
     - 有効にすると、1 周期が終わるたびに最初から繰り返す。炎のように出し続けるエフェクトでは有効にし、爆発のように 1 回で終わるエフェクトでは無効にする。
   * - :guilabel:`Prewarm`
     - 有効にすると、1 周期分の時間がすでに経過した状態から再生を始める。:guilabel:`Looping` が有効なときだけ使える。再生を始めた瞬間からパーティクルが満ちている状態にしたいときに使う。
   * - :guilabel:`Start Delay`
     - 再生を始めてから、放出を始めるまでの待ち時間（秒）。

:guilabel:`Looping` が無効のとき、:guilabel:`Duration` の時間が過ぎると放出が止まる。放出済みのパーティクルは、寿命が尽きるまで動き続ける。すべてのパーティクルが消えると、Particle System は停止した状態になる。

パーティクルの初期値
--------------------

次の設定項目は、パーティクルを放出するときの初期値を決める。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Start Lifetime`
     - パーティクルの寿命（秒）。放出されてからこの時間が経つと、パーティクルは消える。
   * - :guilabel:`Start Speed`
     - 初速の大きさ（m/s）。向きは Shape モジュールで決まる（第 5 章を参照）。
   * - :guilabel:`Start Size`
     - 大きさ（m）。:guilabel:`3D Start Size` を有効にすると、X、Y、Z 軸ごとに指定できる。
   * - :guilabel:`Start Rotation`
     - 回転の角度（度）。:guilabel:`3D Start Rotation` を有効にすると、X、Y、Z 軸ごとに指定できる。
   * - :guilabel:`Flip Rotation`
     - 0～1 の値で、回転の向きを逆にするパーティクルの割合を指定する。
   * - :guilabel:`Start Color`
     - 色と不透明度。テクスチャーの色に、この色が掛け合わされる。

:guilabel:`Start Speed` と :guilabel:`Start Size` の単位は、正確には Unity の座標の単位である。Unity では 1 単位を 1 m として扱うことが多いため、本資料では m と書く。

値の指定方法
------------

:guilabel:`Start Lifetime` や :guilabel:`Start Speed` などの数値の設定項目は、右端の ▼ のボタンで、値の指定方法を選べる。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 指定方法
     - 内容
   * - :guilabel:`Constant`
     - 1 つの固定の値。
   * - :guilabel:`Curve`
     - 時間とともに変わる値。カーブで指定する。
   * - :guilabel:`Random Between Two Constants`
     - 2 つの値の間のランダムな値。
   * - :guilabel:`Random Between Two Curves`
     - 2 本のカーブの間のランダムな値。

パーティクルごとに初期値をばらつかせると、自然な見た目になる。まずは :guilabel:`Random Between Two Constants` を使うとよい。たとえば、:guilabel:`Start Size` を 0.5～1.5 にすると、大きさの異なるパーティクルが混ざって放出される。

:guilabel:`Start Color` のような色の設定項目では、次の指定方法を選べる。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - 指定方法
     - 内容
   * - :guilabel:`Color`
     - 1 つの固定の色。
   * - :guilabel:`Gradient`
     - 時間とともに変わる色。グラデーションで指定する。
   * - :guilabel:`Random Between Two Colors`
     - 2 つの色の間のランダムな色。
   * - :guilabel:`Random Between Two Gradients`
     - 2 つのグラデーションの間のランダムな色。
   * - :guilabel:`Random Color`
     - 1 つのグラデーションの中から、ランダムに選んだ色。

カーブとグラデーションの横軸
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Main モジュールでカーブやグラデーションを使う場合、横軸は Particle System の周期の中での経過時間である。横軸の 0 が周期の始まり、1 が :guilabel:`Duration` の終わりにあたる。つまり、カーブで決まるのは「いつ放出されたパーティクルが、どの初期値を持つか」であり、放出後のパーティクルの値は変わらない。

たとえば、:guilabel:`Start Color` を赤から青へのグラデーションにすると、周期の始めに放出されたパーティクルは赤く、終わりに放出されたパーティクルは青くなる。1 つのパーティクルが寿命の間に赤から青に変わるわけではない。寿命の間に色を変えるには、Color over Lifetime モジュールを使う（第 6 章を参照）。

重力
----

:guilabel:`Gravity Modifier` は、パーティクルに掛かる重力の倍率である。重力の加速度は、:menuselection:`Edit --> Project Settings --> Physics` の :guilabel:`Gravity` の値（既定では :math:`(0,\ -9.81,\ 0)` m/s²）を使う。倍率が 0 のとき、重力は掛からない。

重力の加速度を :math:`\mathbf{g}`、:guilabel:`Gravity Modifier` を :math:`k` とする。放出位置を :math:`\mathbf{p}_0`、初速を :math:`\mathbf{v}_0` とすると、放出から :math:`t` 秒後のパーティクルの位置 :math:`\mathbf{p}(t)` は次の式で表される。ここでは、ほかのモジュールによる速度の変化はないものとする。

.. math::

   \mathbf{p}(t) = \mathbf{p}_0 + \mathbf{v}_0 t + \frac{1}{2} k \mathbf{g} t^2

たとえば、真上に初速 5 m/s で放出し、:guilabel:`Gravity Modifier` を 1 にした場合を考える。上向きの速度は :math:`5 - 9.81t` なので、パーティクルは約 0.51 秒後に最も高い位置に達する。その高さは、次の式から約 1.27 m である。

.. math::

   h = \frac{v_0^2}{2 k g} = \frac{5^2}{2 \times 1 \times 9.81} \approx 1.27

:guilabel:`Start Lifetime` が 1.02 秒より長ければ、パーティクルは放出位置より下まで落ちてから消える。噴水や火花のように、放物線を描いて落ちるエフェクトを作るときは、この関係を目安に初速、重力、寿命を決める。

Simulation Space
----------------

:guilabel:`Simulation Space` は、パーティクルの位置をどの座標系で計算するかを決める。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 値
     - 内容
   * - :guilabel:`Local`
     - Particle System の GameObject を基準にした座標系で計算する。GameObject を動かすと、放出済みのパーティクルも一緒に動く。
   * - :guilabel:`World`
     - ワールド座標系で計算する。放出済みのパーティクルは、GameObject を動かしてもその場に残る。
   * - :guilabel:`Custom`
     - 指定した別の GameObject を基準にした座標系で計算する。

移動するキャラクターの足元から出る土煙は、:guilabel:`World` にすると、キャラクターの通った跡に残る。キャラクターが持つ武器の周りを漂う光のように、発生源と一緒に動いてほしいエフェクトは :guilabel:`Local` にする。

Particle System の GameObject を動かさない場合は、どちらを選んでも見た目は変わらない。

その他の設定項目
----------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Simulation Speed`
     - Particle System 全体の再生速度の倍率。
   * - :guilabel:`Delta Time`
     - :guilabel:`Scaled` にすると、``Time.timeScale`` の影響を受ける。:guilabel:`Unscaled` にすると、``Time.timeScale`` を 0 にしてゲームを一時停止している間も動き続ける。一時停止中のメニュー画面のエフェクトに使う。
   * - :guilabel:`Scaling Mode`
     - Transform の :guilabel:`Scale` をどう反映するかを決める。:guilabel:`Hierarchy` は親を含めたスケールを反映する。:guilabel:`Local` は自分の Transform のスケールだけを反映する。:guilabel:`Shape` はスケールを放出する範囲の形だけに反映し、パーティクルの大きさには反映しない。
   * - :guilabel:`Play On Awake`
     - 有効にすると、GameObject が有効になったときに自動で再生を始める。スクリプトから再生する場合は無効にする。
   * - :guilabel:`Emitter Velocity`
     - Particle System の移動速度を、Rigidbody と Transform のどちらから求めるかを決める。Inherit Velocity モジュールと、Emission モジュールの :guilabel:`Rate over Distance` で使う。
   * - :guilabel:`Max Particles`
     - 同時に存在できるパーティクルの最大数。既定は 1000。この数に達すると、パーティクルが消えて数が減るまで、新しいパーティクルは放出されない。
   * - :guilabel:`Auto Random Seed`
     - 有効にすると、再生するたびに異なる乱数でパーティクルを放出する。無効にすると、:guilabel:`Random Seed` の値を使い、毎回同じ見た目で再生する。
   * - :guilabel:`Stop Action`
     - 再生が終わったときの動作。:guilabel:`None`\ （何もしない）、:guilabel:`Disable`\ （GameObject を無効にする）、:guilabel:`Destroy`\ （GameObject を削除する）、:guilabel:`Callback`\ （スクリプトの ``OnParticleSystemStopped`` メソッドを呼ぶ）から選ぶ。
   * - :guilabel:`Culling Mode`
     - 画面の外にあるときに、計算を止めるかどうかを決める（第 11 章を参照）。
   * - :guilabel:`Ring Buffer Mode`
     - :guilabel:`Max Particles` に達したときに、古いパーティクルを新しいパーティクルで置き換えるかどうかを決める。有効にすると、寿命が尽きてもパーティクルを消さずに残しておける。弾痕や足跡のように、一定の数だけ残し続けたい表現に使う。

:guilabel:`Stop Action` の「再生が終わったとき」とは、放出が止まり、すべてのパーティクルが消えたときである。:guilabel:`Looping` が有効な Particle System は、スクリプトから止めない限り再生が終わらない。
