第 5 章 放出と形状
==================

この章では、パーティクルをどれだけの頻度で放出するかを決める Emission モジュールと、どこからどの向きに放出するかを決める Shape モジュールを説明する。

Emission モジュール
-------------------

Emission モジュールは、パーティクルを放出する頻度を決める。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Rate over Time`
     - 1 秒あたりに放出するパーティクルの数。
   * - :guilabel:`Rate over Distance`
     - Particle System が 1 m 移動するごとに放出するパーティクルの数。止まっている間は放出しない。
   * - :guilabel:`Bursts`
     - 決まった時刻に、まとめて放出するパーティクルの設定。

:guilabel:`Rate over Distance` は、移動する物体の軌跡に沿ってパーティクルを並べたいときに使う。たとえば、走るキャラクターの足元の土煙や、飛んでいく弾の後ろに残る煙である。放出したパーティクルを軌跡に残すため、Main モジュールの :guilabel:`Simulation Space` を :guilabel:`World` にしておく（第 4 章を参照）。

同時に存在するパーティクルの数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:guilabel:`Rate over Time` を :math:`r`、Main モジュールの :guilabel:`Start Lifetime` を :math:`L` 秒とする。放出を始めてから :math:`L` 秒が経つと、放出される数と寿命で消える数がつり合い、同時に存在するパーティクルの数 :math:`N` はほぼ一定になる。

.. math::

   N \approx r \times L

たとえば、既定の設定（:math:`r = 10`、:math:`L = 5`）では、約 50 個のパーティクルが同時に存在する。ただし、:math:`N` は Main モジュールの :guilabel:`Max Particles` を超えない。:math:`r \times L` が :guilabel:`Max Particles` を超えると、上限に達した時点で放出が止まり、設定したとおりの頻度で放出されなくなる。

同時に存在するパーティクルの数は、処理の重さに直接影響する（第 11 章を参照）。見た目を変えずに数を減らしたい場合は、寿命を短くするか、1 つ 1 つのパーティクルを大きくして放出する頻度を下げる。

Bursts
~~~~~~

:guilabel:`Bursts` は、決まった時刻にまとめてパーティクルを放出する設定である。爆発や、打撃が当たった瞬間の火花のように、一瞬で大量のパーティクルを出すエフェクトに使う。リストの :guilabel:`+` ボタンで追加する。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Time`
     - 放出する時刻。周期の始まりからの経過時間（秒）で指定する。
   * - :guilabel:`Count`
     - 1 回に放出する数。
   * - :guilabel:`Cycles`
     - 放出する回数。
   * - :guilabel:`Interval`
     - :guilabel:`Cycles` が 2 以上のときの、放出の間隔（秒）。
   * - :guilabel:`Probability`
     - 0～1 の値で、放出する確率を指定する。1 のとき必ず放出する。

1 つの Burst で放出する数の合計は、:guilabel:`Count` と :guilabel:`Cycles` の積である。たとえば、:guilabel:`Count` が 20、:guilabel:`Cycles` が 3、:guilabel:`Interval` が 0.1 のとき、0.1 秒おきに 20 個ずつ、合計 60 個を放出する。

1 回で終わる爆発のエフェクトは、:guilabel:`Rate over Time` を 0 にし、:guilabel:`Time` が 0 の Burst を 1 つだけ設定して作る。Main モジュールの :guilabel:`Looping` は無効にしておく。

Shape モジュール
----------------

Shape モジュールは、パーティクルを放出する範囲の形と、放出する向きを決める。放出の向きは、Main モジュールの :guilabel:`Start Speed` の速度の向きになる。

Shape モジュールを選択している間は、Scene ビューに放出する範囲の形が表示される。形の表示についているハンドルをドラッグすると、大きさを変えられる。

:guilabel:`Shape` で選べる主な形を次の表にまとめる。

.. list-table::
   :header-rows: 1
   :widths: 25 45 30

   * - 形
     - 放出の位置と向き
     - 使いどころ
   * - :guilabel:`Cone`
     - 円の範囲から、円錐状に広がる向きに放出する。
     - 炎、噴水、煙突の煙
   * - :guilabel:`Sphere`
     - 球の範囲から、中心から外に向かう向きに放出する。
     - 爆発、光の粒の広がり
   * - :guilabel:`Hemisphere`
     - 半球の範囲から、中心から外に向かう向きに放出する。
     - 地面での爆発、着地の衝撃
   * - :guilabel:`Box`
     - 直方体の範囲から、Z 軸の正の向きに放出する。
     - 雨、雪、空間に漂うちり
   * - :guilabel:`Circle`
     - 円の範囲から、中心から外に向かう向きに放出する。放出の向きは円の平面の中に限られる。
     - 地面に広がる衝撃波
   * - :guilabel:`Edge`
     - 線分の上から、Y 軸の正の向きに放出する。
     - 滝、横一列に並んだ炎
   * - :guilabel:`Donut`
     - ドーナツ状の範囲から放出する。
     - 輪の形の光、魔法陣
   * - :guilabel:`Mesh`、:guilabel:`Mesh Renderer`、:guilabel:`Skinned Mesh Renderer`
     - メッシュの頂点、辺、面から放出する。
     - キャラクターの体から立ち上るオーラ

形ごとの設定項目
~~~~~~~~~~~~~~~~

形によって設定項目が異なる。よく使う設定項目を次の表にまとめる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Angle`
     - :guilabel:`Cone` の広がりの角度（度）。0 にすると、平行に放出する。
   * - :guilabel:`Radius`
     - :guilabel:`Cone`、:guilabel:`Sphere`、:guilabel:`Circle` などの半径（m）。
   * - :guilabel:`Radius Thickness`
     - 0～1 の値で、放出する範囲の厚みを指定する。0 のときは表面だけから、1 のときは内部全体から放出する。
   * - :guilabel:`Arc`
     - 円周のうち、放出に使う範囲の角度（度）。360 で円周全体になる。
   * - :guilabel:`Emit from`
     - :guilabel:`Cone` や :guilabel:`Box` で、底面、内部、表面、辺のどこから放出するかを選ぶ。

形の位置と向きの調整
~~~~~~~~~~~~~~~~~~~~

どの形でも、次の設定項目で位置、向き、放出の向きを調整できる。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 設定項目
     - 内容
   * - :guilabel:`Position`、:guilabel:`Rotation`、:guilabel:`Scale`
     - Particle System の GameObject に対する、形の位置、回転、拡大率。GameObject を動かさずに、放出する範囲だけを調整できる。
   * - :guilabel:`Align To Direction`
     - 有効にすると、パーティクルの向きを放出の向きに合わせる。
   * - :guilabel:`Randomize Direction`
     - 0～1 の値で、放出の向きをランダムな向きに近づける割合を指定する。
   * - :guilabel:`Spherize Direction`
     - 0～1 の値で、放出の向きを、形の中心から外に向かう向きに近づける割合を指定する。
   * - :guilabel:`Randomize Position`
     - 放出する位置を、指定した距離までランダムにずらす。

Shape モジュールを無効にすると、すべてのパーティクルが GameObject の位置から、Z 軸の正の向きに放出される。
