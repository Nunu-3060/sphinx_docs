第 10 章 作例
=============

この章では、これまでに学んだモジュールを組み合わせて、焚き火、雨、爆発、ヒットエフェクトの 4 つのエフェクトを作る。各作例の設定値は一例である。値を変えて、見た目がどう変わるかを試してほしい。

表に書いていない設定項目は、既定の値のままでよい。数値が 2 つ書いてある設定項目は、:guilabel:`Random Between Two Constants` にして、2 つの値の間のランダムな値にする（第 4 章を参照）。色は、R、G、B、A の各成分を 0～255 の値で示す。

この章のサンプルコードは、``examples/chapter10`` フォルダーにある。

準備：マテリアルの作成
----------------------

作例では、次の 2 つのマテリアルを使う。第 7 章の手順で作成する。

.. list-table::
   :header-rows: 1
   :widths: 25 35 40

   * - マテリアル名
     - 設定
     - 用途
   * - FireAdditive
     - :guilabel:`Surface Type` を :guilabel:`Transparent`、:guilabel:`Blending Mode` を :guilabel:`Additive` にする。
     - 炎、火花、閃光など、光るもの
   * - SmokeAlpha
     - :guilabel:`Surface Type` を :guilabel:`Transparent`、:guilabel:`Blending Mode` を :guilabel:`Alpha` にする。
     - 煙、雨粒など、光らないもの

どちらも、:guilabel:`Shader` は :menuselection:`Universal Render Pipeline --> Particles --> Unlit` にする。:guilabel:`Base Map` には、Unity に組み込まれている Default-ParticleSystem テクスチャーを設定する。:guilabel:`Base Map` の左の丸いボタンを押し、表示されたウィンドウで「Default-ParticleSystem」を検索して選ぶ。中心が明るく、外側に向かって透明になる円のテクスチャーである。

独自のテクスチャーを用意できる場合は、炎や煙の形をしたテクスチャーを使うと、より本物らしくなる。

焚き火
------

焚き火は、炎、煙、火の粉の 3 つの Particle System を組み合わせて作る。炎を親にし、煙と火の粉を子にする。

#. :menuselection:`GameObject --> Effects --> Particle System` で Particle System を作り、名前を「Campfire」にする。これが炎になる。Transform の :guilabel:`Rotation` の X は -90 のままにする。
#. Campfire を右クリックし、:menuselection:`Effects --> Particle System` を選んで子の Particle System を 2 つ作る。名前を「Smoke」と「Sparks」にする。
#. 子の Transform の :guilabel:`Position` と :guilabel:`Rotation` は、すべて 0 にする。親の回転を引き継ぐため、子もパーティクルを上に向かって放出する。

炎（Campfire）
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Start Lifetime`
     - 0.6、1.0
   * -
     - :guilabel:`Start Speed`
     - 1、2
   * -
     - :guilabel:`Start Size`
     - 0.4、0.8
   * -
     - :guilabel:`Start Color`
     - R 255、G 140、B 40、A 255
   * -
     - :guilabel:`Simulation Space`
     - :guilabel:`World`
   * - Emission
     - :guilabel:`Rate over Time`
     - 30
   * - Shape
     - :guilabel:`Angle`
     - 5
   * -
     - :guilabel:`Radius`
     - 0.3
   * - Color over Lifetime
     - :guilabel:`Color`
     - 不透明度を 0 → 255（位置 0.1）→ 0 にする。色を黄色から赤にする。
   * - Size over Lifetime
     - :guilabel:`Size`
     - 1 から 0 に下がる直線
   * - Noise
     - :guilabel:`Strength`
     - 0.3
   * -
     - :guilabel:`Frequency`
     - 1.5
   * -
     - :guilabel:`Scroll Speed`
     - 1
   * - Renderer
     - :guilabel:`Material`
     - FireAdditive

炎は、下の方で大きく、上に行くほど小さく細くなる。Size over Lifetime モジュールで小さくしながら、Noise モジュールで揺らすことで、揺らめく炎の形を作る。

煙（Smoke）
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Start Lifetime`
     - 3、4
   * -
     - :guilabel:`Start Speed`
     - 0.5、1
   * -
     - :guilabel:`Start Size`
     - 0.8、1.5
   * -
     - :guilabel:`Start Rotation`
     - 0、360
   * -
     - :guilabel:`Start Color`
     - R 80、G 80、B 80、A 100
   * -
     - :guilabel:`Simulation Space`
     - :guilabel:`World`
   * - Emission
     - :guilabel:`Rate over Time`
     - 5
   * - Shape
     - :guilabel:`Angle`
     - 10
   * -
     - :guilabel:`Radius`
     - 0.3
   * -
     - :guilabel:`Position`
     - X 0、Y 0、Z 0.8
   * - Color over Lifetime
     - :guilabel:`Color`
     - 不透明度を 0 → 255（位置 0.2）→ 0 にする。
   * - Size over Lifetime
     - :guilabel:`Size`
     - 0.5 から 1 に上がる直線
   * - Rotation over Lifetime
     - :guilabel:`Angular Velocity`
     - -30、30
   * - Renderer
     - :guilabel:`Material`
     - SmokeAlpha
   * -
     - :guilabel:`Sort Mode`
     - :guilabel:`By Distance`

Shape モジュールの :guilabel:`Position` の Z を 0.8 にして、炎の先端のあたりから煙を出す。子の Particle System は親の回転を引き継いでいるため、ローカル座標の Z 軸がワールド座標の上向きになっている。

火の粉（Sparks）
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Start Lifetime`
     - 1、2
   * -
     - :guilabel:`Start Speed`
     - 1、3
   * -
     - :guilabel:`Start Size`
     - 0.03、0.06
   * -
     - :guilabel:`Start Color`
     - R 255、G 200、B 80、A 255
   * -
     - :guilabel:`Simulation Space`
     - :guilabel:`World`
   * - Emission
     - :guilabel:`Rate over Time`
     - 8
   * - Shape
     - :guilabel:`Angle`
     - 20
   * -
     - :guilabel:`Radius`
     - 0.2
   * - Size over Lifetime
     - :guilabel:`Size`
     - 1 から 0 に下がる直線
   * - Noise
     - :guilabel:`Strength`
     - 0.5
   * -
     - :guilabel:`Frequency`
     - 2
   * - Renderer
     - :guilabel:`Render Mode`
     - :guilabel:`Stretched Billboard`
   * -
     - :guilabel:`Speed Scale`
     - 0.05
   * -
     - :guilabel:`Material`
     - FireAdditive

第 5 章の式 :math:`N \approx r \times L` で、同時に存在するパーティクルの数を見積もってみる。寿命の平均を使うと、炎は :math:`30 \times 0.8 = 24`、煙は :math:`5 \times 3.5 \approx 18`、火の粉は :math:`8 \times 1.5 = 12` で、合計でおよそ 54 個である。数十個のパーティクルでも、組み合わせ方しだいで十分に焚き火らしく見える。

雨
--

雨は、空の広い範囲から雨粒を降らせ、地面に当たった位置でサブエミッターから水しぶきを出して作る。

#. 地面にする Plane を配置し、:guilabel:`Scale` を X 3、Y 1、Z 3 にする。
#. Particle System を作り、名前を「Rain」にする。Transform の :guilabel:`Position` を X 0、Y 10、Z 0 に、:guilabel:`Rotation` を X 90、Y 0、Z 0 にする。ローカル座標の Z 軸が下向きになり、パーティクルが下に向かって放出される。
#. Rain の Sub Emitters モジュールを有効にし、リストの :guilabel:`+` ボタンを押す。子の Particle System が作られるので、名前を「Splash」にする。

雨粒（Rain）
~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Start Lifetime`
     - 2
   * -
     - :guilabel:`Start Speed`
     - 15
   * -
     - :guilabel:`Start Size`
     - 0.03、0.05
   * -
     - :guilabel:`Start Color`
     - R 180、G 200、B 255、A 150
   * -
     - :guilabel:`Simulation Space`
     - :guilabel:`World`
   * - Emission
     - :guilabel:`Rate over Time`
     - 500
   * - Shape
     - :guilabel:`Shape`
     - :guilabel:`Box`
   * -
     - :guilabel:`Scale`
     - X 20、Y 20、Z 0
   * - Collision
     - :guilabel:`Type`
     - :guilabel:`World`
   * -
     - :guilabel:`Lifetime Loss`
     - 1
   * - Sub Emitters
     - きっかけ
     - :guilabel:`Collision`
   * - Renderer
     - :guilabel:`Render Mode`
     - :guilabel:`Stretched Billboard`
   * -
     - :guilabel:`Speed Scale`
     - 0.02
   * -
     - :guilabel:`Material`
     - SmokeAlpha

Shape モジュールの :guilabel:`Box` は、Z 軸の正の向きにパーティクルを放出する。Z の大きさを 0 にして、高さ 10 m の位置の 20 m 四方の平面から雨粒を降らせる。

雨粒は 15 m/s で 10 m 落ちるため、約 0.67 秒で地面に当たり、Collision モジュールの :guilabel:`Lifetime Loss` によって消える。同時に存在する雨粒の数は、:math:`500 \times 0.67 \approx 330` 個と見積もれる。:guilabel:`Start Lifetime` を 2 秒にしているのは、地面のない場所に落ちた雨粒をいずれ消すためである。その分を含めても、既定の :guilabel:`Max Particles` の 1000 に収まる。

水しぶき（Splash）
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Transform
     - :guilabel:`Rotation`
     - X 180、Y 0、Z 0
   * - Main
     - :guilabel:`Start Lifetime`
     - 0.2、0.4
   * -
     - :guilabel:`Start Speed`
     - 1、2
   * -
     - :guilabel:`Start Size`
     - 0.02、0.04
   * -
     - :guilabel:`Start Color`
     - R 180、G 200、B 255、A 150
   * -
     - :guilabel:`Gravity Modifier`
     - 1
   * -
     - :guilabel:`Simulation Space`
     - :guilabel:`World`
   * - Emission
     - :guilabel:`Rate over Time`
     - 0
   * -
     - :guilabel:`Bursts`
     - :guilabel:`Time` 0、:guilabel:`Count` 3
   * - Shape
     - :guilabel:`Shape`
     - :guilabel:`Hemisphere`
   * -
     - :guilabel:`Radius`
     - 0.05
   * - Renderer
     - :guilabel:`Material`
     - SmokeAlpha

Splash は Rain の子なので、親の回転（X 90）を引き継ぐ。Splash の :guilabel:`Rotation` の X を 180 にすると、親と合わせて X 270（-90）の回転になり、ローカル座標の Z 軸が上向きになる。:guilabel:`Hemisphere` は Z 軸の正の側の半球なので、水しぶきが上に向かって跳ねる。

爆発
----

爆発は、閃光、火の玉、煙、破片の 4 つの Particle System を組み合わせて作る。すべて Bursts で一度に放出し、Main モジュールの :guilabel:`Looping` は無効にする。

#. Particle System を作り、名前を「Explosion」にする。これが閃光になる。
#. Explosion の子として、「Fireball」「Smoke」「Debris」の 3 つの Particle System を作る。子の Transform の :guilabel:`Position` と :guilabel:`Rotation` は、すべて 0 にする。

どの Particle System も、Emission モジュールの :guilabel:`Rate over Time` を 0 にし、:guilabel:`Bursts` を 1 つ追加して :guilabel:`Time` を 0 にする。:guilabel:`Count` は各表のとおりにする。

閃光（Explosion）
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Duration`
     - 3.5
   * -
     - :guilabel:`Looping`
     - 無効
   * -
     - :guilabel:`Start Lifetime`
     - 0.15
   * -
     - :guilabel:`Start Speed`
     - 0
   * -
     - :guilabel:`Start Size`
     - 4
   * -
     - :guilabel:`Start Color`
     - R 255、G 220、B 150、A 255
   * -
     - :guilabel:`Stop Action`
     - :guilabel:`Destroy`
   * - Emission
     - :guilabel:`Bursts` の :guilabel:`Count`
     - 1
   * - Shape
     - （モジュール全体）
     - 無効
   * - Color over Lifetime
     - :guilabel:`Color`
     - 不透明度を 255 → 0 にする。
   * - Size over Lifetime
     - :guilabel:`Size`
     - 0.5 から 1 に上がる直線
   * - Renderer
     - :guilabel:`Material`
     - FireAdditive

:guilabel:`Stop Action` を :guilabel:`Destroy` にすると、再生が終わったときに GameObject が子と一緒に削除される。親の :guilabel:`Duration` を 3.5 秒にしているのは、子の Particle System のパーティクルがすべて消えるまで、親の再生を終わらせないためである。子のうち最も長く残るのは煙で、:guilabel:`Start Delay` の 0.1 秒と寿命の最大 3 秒を足した 3.1 秒で消える。

火の玉（Fireball）
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Looping`
     - 無効
   * -
     - :guilabel:`Start Lifetime`
     - 0.4、0.8
   * -
     - :guilabel:`Start Speed`
     - 2、6
   * -
     - :guilabel:`Start Size`
     - 1、2
   * -
     - :guilabel:`Start Rotation`
     - 0、360
   * -
     - :guilabel:`Start Color`
     - R 255、G 150、B 50、A 255
   * - Emission
     - :guilabel:`Bursts` の :guilabel:`Count`
     - 30
   * - Shape
     - :guilabel:`Shape`
     - :guilabel:`Sphere`
   * -
     - :guilabel:`Radius`
     - 0.5
   * - Limit Velocity over Lifetime
     - :guilabel:`Drag`
     - 3
   * - Color over Lifetime
     - :guilabel:`Color`
     - 不透明度を 255 → 0 にする。色を黄色から赤にする。
   * - Size over Lifetime
     - :guilabel:`Size`
     - 0.5 から 1 に上がる直線
   * - Renderer
     - :guilabel:`Material`
     - FireAdditive

煙（Smoke）
~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Looping`
     - 無効
   * -
     - :guilabel:`Start Delay`
     - 0.1
   * -
     - :guilabel:`Start Lifetime`
     - 2、3
   * -
     - :guilabel:`Start Speed`
     - 1、3
   * -
     - :guilabel:`Start Size`
     - 1.5、3
   * -
     - :guilabel:`Start Rotation`
     - 0、360
   * -
     - :guilabel:`Start Color`
     - R 60、G 60、B 60、A 180
   * -
     - :guilabel:`Gravity Modifier`
     - -0.05
   * - Emission
     - :guilabel:`Bursts` の :guilabel:`Count`
     - 20
   * - Shape
     - :guilabel:`Shape`
     - :guilabel:`Sphere`
   * -
     - :guilabel:`Radius`
     - 0.8
   * - Limit Velocity over Lifetime
     - :guilabel:`Drag`
     - 2
   * - Color over Lifetime
     - :guilabel:`Color`
     - 不透明度を 0 → 255（位置 0.1）→ 0 にする。
   * - Size over Lifetime
     - :guilabel:`Size`
     - 0.5 から 1 に上がる直線
   * - Renderer
     - :guilabel:`Material`
     - SmokeAlpha
   * -
     - :guilabel:`Sort Mode`
     - :guilabel:`By Distance`

:guilabel:`Gravity Modifier` を負の値にすると、重力と逆向き、つまり上向きの加速度が掛かる。熱い煙がゆっくり立ち上る様子を表せる。

破片（Debris）
~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - モジュール
     - 設定項目
     - 値
   * - Main
     - :guilabel:`Looping`
     - 無効
   * -
     - :guilabel:`Start Lifetime`
     - 0.8、1.5
   * -
     - :guilabel:`Start Speed`
     - 8、15
   * -
     - :guilabel:`Start Size`
     - 0.05、0.1
   * -
     - :guilabel:`Start Color`
     - R 255、G 200、B 100、A 255
   * -
     - :guilabel:`Gravity Modifier`
     - 1
   * - Emission
     - :guilabel:`Bursts` の :guilabel:`Count`
     - 40
   * - Shape
     - :guilabel:`Shape`
     - :guilabel:`Sphere`
   * -
     - :guilabel:`Radius`
     - 0.2
   * - Size over Lifetime
     - :guilabel:`Size`
     - 1 から 0 に下がる直線
   * - Renderer
     - :guilabel:`Render Mode`
     - :guilabel:`Stretched Billboard`
   * -
     - :guilabel:`Speed Scale`
     - 0.03
   * -
     - :guilabel:`Material`
     - FireAdditive

爆発の見た目は、複数の要素の時間差で決まる。閃光が 0.15 秒で消え、火の玉が 1 秒弱で燃え尽き、煙が 3 秒ほどかけて消える。この時間差が、爆発の迫力を生む。

ヒットエフェクト
----------------

ヒットエフェクトは、弾や攻撃が当たった位置に、一瞬だけ表示するエフェクトである。ここでは、火花と閃光でヒットエフェクトを作り、プレハブにしてスクリプトから生成する。

エフェクトの作成
~~~~~~~~~~~~~~~~

#. Particle System を作り、名前を「HitEffect」にする。Transform の :guilabel:`Rotation` をすべて 0 にする。ローカル座標の Z 軸の正の向きにパーティクルが放出されるようになる。これが火花になる。
#. HitEffect の子として Particle System を作り、名前を「Flash」にする。Transform の :guilabel:`Position` と :guilabel:`Rotation` は、すべて 0 にする。

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - 対象
     - モジュール
     - 設定項目
     - 値
   * - HitEffect
     - Main
     - :guilabel:`Duration`
     - 0.5
   * -
     -
     - :guilabel:`Looping`
     - 無効
   * -
     -
     - :guilabel:`Start Lifetime`
     - 0.2、0.4
   * -
     -
     - :guilabel:`Start Speed`
     - 5、10
   * -
     -
     - :guilabel:`Start Size`
     - 0.03、0.06
   * -
     -
     - :guilabel:`Start Color`
     - R 255、G 230、B 150、A 255
   * -
     -
     - :guilabel:`Gravity Modifier`
     - 0.5
   * -
     -
     - :guilabel:`Stop Action`
     - :guilabel:`Destroy`
   * -
     - Emission
     - :guilabel:`Rate over Time`
     - 0
   * -
     -
     - :guilabel:`Bursts`
     - :guilabel:`Time` 0、:guilabel:`Count` 15
   * -
     - Shape
     - :guilabel:`Angle`
     - 40
   * -
     -
     - :guilabel:`Radius`
     - 0.05
   * -
     - Limit Velocity over Lifetime
     - :guilabel:`Drag`
     - 5
   * -
     - Renderer
     - :guilabel:`Render Mode`
     - :guilabel:`Stretched Billboard`
   * -
     -
     - :guilabel:`Speed Scale`
     - 0.03
   * -
     -
     - :guilabel:`Material`
     - FireAdditive
   * - Flash
     - Main
     - :guilabel:`Looping`
     - 無効
   * -
     -
     - :guilabel:`Start Lifetime`
     - 0.1
   * -
     -
     - :guilabel:`Start Speed`
     - 0
   * -
     -
     - :guilabel:`Start Size`
     - 0.8
   * -
     - Emission
     - :guilabel:`Rate over Time`
     - 0
   * -
     -
     - :guilabel:`Bursts`
     - :guilabel:`Time` 0、:guilabel:`Count` 1
   * -
     - Shape
     - （モジュール全体）
     - 無効
   * -
     - Color over Lifetime
     - :guilabel:`Color`
     - 不透明度を 255 → 0 にする。
   * -
     - Size over Lifetime
     - :guilabel:`Size`
     - 0.5 から 1 に上がる直線
   * -
     - Renderer
     - :guilabel:`Material`
     - FireAdditive

HitEffect を Project ウィンドウにドラッグ＆ドロップしてプレハブにし、シーンからは削除する。

スクリプトからの生成
~~~~~~~~~~~~~~~~~~~~

次のサンプルは、クリックしたオブジェクトの表面に、ヒットエフェクトのプレハブを生成する。

.. literalinclude:: ../../examples/chapter10/HitEffectSpawner.cs
   :language: csharp
   :caption: HitEffectSpawner.cs
   :linenos:

:download:`HitEffectSpawner.cs をダウンロード <../../examples/chapter10/HitEffectSpawner.cs>`

使う手順は次のとおりである。

#. シーンに Cube や Plane など、コライダーを持つオブジェクトを配置する。
#. 空の GameObject を作り、スクリプトをアタッチする。
#. :guilabel:`Hit Effect Prefab` に、HitEffect のプレハブを設定する。

再生モードでオブジェクトをクリックすると、クリックした面から火花が飛び散る。``Quaternion.LookRotation`` メソッドは、Z 軸が引数の向きになる回転を作る。当たった面の法線を渡すことで、HitEffect の Z 軸、つまり火花の放出の向きが面の外側を向く。

生成したエフェクトは、:guilabel:`Stop Action` の :guilabel:`Destroy` によって、再生が終わると自動で削除される。スクリプトで ``Destroy`` を呼ぶ必要はない。ただし、エフェクトを頻繁に生成と削除すると、処理が重くなることがある。この問題と対策は第 11 章で説明する。
