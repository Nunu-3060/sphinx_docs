第 6 章 時間変化のモジュール
============================

第 4 章の Main モジュールで決まるのは、放出したときの初期値だけである。この章では、放出後のパーティクルの速度、色、大きさ、回転を、寿命の間に変化させるモジュールを説明する。

寿命に対する経過時間
--------------------

名前に「over Lifetime」が付くモジュールでは、パーティクルごとの寿命に対する経過時間の割合を横軸にしたカーブやグラデーションで値を指定する。放出からの経過時間を :math:`a` 秒、パーティクルの寿命を :math:`L` 秒とすると、横軸の値 :math:`t_n` は次の式で表される。

.. math::

   t_n = \frac{a}{L} \quad (0 \le t_n \le 1)

:math:`t_n` は、放出された瞬間に 0、寿命が尽きて消える瞬間に 1 になる。寿命の長さがパーティクルごとに違っても、カーブの始まりと終わりは、それぞれのパーティクルの放出と消滅に対応する。

たとえば、Size over Lifetime モジュールのカーブの値を :math:`f(t_n)` とすると、パーティクルの大きさ :math:`s` は、Main モジュールの :guilabel:`Start Size` の値 :math:`s_0` を使って次の式で表される。

.. math::

   s = s_0 \times f(t_n)

カーブの値は、初期値に対する倍率である。カーブを 1 から 0 に下がる直線にすると、パーティクルは放出されたときの大きさから、少しずつ小さくなって消える。

カーブの編集
~~~~~~~~~~~~

カーブを指定する設定項目をクリックすると、Inspector ウィンドウの下部にカーブの編集画面が表示される。

* 編集画面の左上の数値は、カーブの縦軸の最大値である。カーブの値に、この数値が掛け合わされる。
* 線の上で右クリックし、:guilabel:`Add Key` を選ぶと、制御点を追加できる。
* 制御点をドラッグすると、値を変えられる。
* 編集画面の下部には、よく使う形のカーブが並んでいる。クリックすると、その形のカーブになる。

速度の変化
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - モジュール
     - 内容
   * - Velocity over Lifetime
     - 速度を加える。:guilabel:`Linear` は X、Y、Z 軸の向きの速度である。:guilabel:`Orbital` は、各軸のまわりを回る速度である。:guilabel:`Radial` は、中心から外に向かう速度である。:guilabel:`Speed Modifier` は、速度全体に掛ける倍率である。
   * - Limit Velocity over Lifetime
     - 速さの上限を決め、上限を超えた分を減らす。:guilabel:`Dampen` は、上限を超えた分の速さを減らす割合である。:guilabel:`Drag` は、空気抵抗のように速度を落とす力である。
   * - Inherit Velocity
     - Particle System の GameObject の移動速度を、パーティクルの速度に加える。
   * - Force over Lifetime
     - 力（加速度）を加える。風に流される煙のように、一定の向きに少しずつ加速する動きを作る。

Velocity over Lifetime と Force over Lifetime の違いは、加えるものが速度か加速度かである。Velocity over Lifetime で加えた速度は、カーブの値がそのまま速度になる。Force over Lifetime で加えた加速度は、時間とともに速度に積み重なるため、パーティクルはだんだん速くなる。

Limit Velocity over Lifetime の :guilabel:`Drag` を使うと、勢いよく飛び出したパーティクルがすぐに減速する動きを作れる。爆発の破片や火花に使うと、空気の抵抗を受けているように見える。

色の変化
--------

Color over Lifetime モジュールは、寿命の間の色と不透明度をグラデーションで指定する。グラデーションの色は、Main モジュールの :guilabel:`Start Color` の色に掛け合わされる。

グラデーションの編集画面では、上側のマーカーで不透明度（アルファ）、下側のマーカーで色を指定する。煙や炎では、次のように不透明度を変えると、パーティクルが急に現れたり消えたりせず、自然に見える。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 位置
     - 不透明度
   * - 0（放出時）
     - 0
   * - 0.1
     - 255（完全に不透明）
   * - 1（消滅時）
     - 0

Color by Speed モジュールは、寿命ではなく、パーティクルの速さによって色を変える。:guilabel:`Speed Range` で指定した速さの範囲が、グラデーションの左端から右端に対応する。速く飛ぶ火花ほど明るく光るような表現に使う。

大きさの変化
------------

Size over Lifetime モジュールは、寿命の間の大きさを、:guilabel:`Start Size` に対する倍率のカーブで指定する。:guilabel:`Separate Axes` を有効にすると、X、Y、Z 軸ごとにカーブを指定できる。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - カーブの形
     - 見え方
   * - 0 から 1 に上がる
     - 煙のように、放出後に広がっていく。
   * - 1 から 0 に下がる
     - 火の粉のように、燃え尽きて小さくなる。
   * - 0 から急に上がり、ゆっくり下がる
     - 爆発の閃光のように、一瞬で大きくなってから消える。

Size by Speed モジュールは、パーティクルの速さによって大きさを変える。

回転の変化
----------

Rotation over Lifetime モジュールは、パーティクルを回転させる角速度（度/秒）を指定する。煙や葉っぱのパーティクルをゆっくり回転させると、同じテクスチャーの繰り返しが目立たなくなる。

Rotation by Speed モジュールは、パーティクルの速さによって角速度を変える。

Noise モジュール
----------------

Noise モジュールは、パーティクルの位置を不規則に揺らす。炎の揺らめき、煙の渦、漂うちりの動きなどを作るのに使う。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Strength`
     - 揺れの強さ。
   * - :guilabel:`Frequency`
     - 揺れの細かさ。値が大きいほど、短い距離で揺れの向きが変わる。
   * - :guilabel:`Scroll Speed`
     - 揺れのパターンが時間とともに変化する速さ。
   * - :guilabel:`Damping`
     - 有効にすると、揺れの強さを :guilabel:`Frequency` に比例させる。:guilabel:`Frequency` を変えても、揺れの大きさが保たれる。
   * - :guilabel:`Octaves`
     - 細かさの異なる揺れを重ねる数。増やすと細かい揺れが加わるが、処理が重くなる。
   * - :guilabel:`Quality`
     - 揺れの計算の品質。:guilabel:`Low (1D)`、:guilabel:`Medium (2D)`、:guilabel:`High (3D)` から選ぶ。品質を上げるほど、処理が重くなる。
   * - :guilabel:`Position Amount`、:guilabel:`Rotation Amount`、:guilabel:`Size Amount`
     - 揺れを、位置、回転、大きさのそれぞれにどれだけ反映するか。

Noise モジュールの揺れは、場所によって向きが滑らかに変わる。近くにあるパーティクルは似た向きに動くため、ランダムな速度を加えた場合と違い、煙の流れのようなまとまりのある動きになる。

External Forces モジュール
--------------------------

External Forces モジュールを有効にすると、シーンに置いた Wind Zone や Particle System Force Field の影響を受けるようになる。

* Wind Zone は、風を表すコンポーネントである。木と同じ風で、パーティクルを流せる。
* Particle System Force Field は、パーティクルを引き寄せたり、渦を巻かせたりする範囲を作るコンポーネントである。:menuselection:`GameObject --> Effects --> Particle System Force Field` で作成する。

複数の Particle System に同じ力を加えたいときは、それぞれに Force over Lifetime モジュールを設定するより、シーンに置いた力の範囲を共有するほうが管理しやすい。
