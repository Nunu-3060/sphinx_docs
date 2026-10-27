シミュレーション入門
====================

Houdini は、物理法則に従って物を動かすシミュレーションの機能が充実している。この章では、シミュレーションがここまでのプロシージャルなネットワークとどう違うかを説明し、剛体（変形しない固い物）のシミュレーションを 1 つ作る。

シミュレーションの特徴
----------------------

ここまでに作ったネットワークは、どのフレームの結果も、そのフレームの値だけから計算できた。例えば :doc:`expressions` の弾むボールは、``$F`` さえ分かれば、60 フレーム目の位置を直接計算できる。

シミュレーションでは、あるフレームの状態を、1 つ前のフレームの状態から計算する。物の位置と速度に、重力や衝突による力を加えて、少しずつ時間を進める。そのため、次の性質がある。

* 60 フレーム目の結果を得るには、最初のフレームから 59 フレーム目までを順に計算する必要がある。プレイバーで途中のフレームに飛ぶと、そこまでの計算が行われる。
* パラメーターを変えると、最初のフレームから計算し直しになる。
* 計算に時間がかかるので、結果をファイルに保存（キャッシュ）しておき、後の工程ではそのファイルを読み込むのが一般的である。

.. graphviz::
   :caption: プロシージャルな計算とシミュレーションの違い
   :name: fig-simulation

   digraph sim {
     rankdir=LR;
     node [shape=box, style="rounded,filled", fillcolor="#d4e8f7", fontsize=11];
     subgraph cluster_proc {
       label="プロシージャル（各フレームを独立に計算）"; fontsize=11; style=rounded; color="#999999";
       f1 [label="$F = 1"]; r1 [label="結果 1", fillcolor="#fff3b0"];
       f60 [label="$F = 60"]; r60 [label="結果 60", fillcolor="#fff3b0"];
       f1 -> r1; f60 -> r60;
     }
     subgraph cluster_sim {
       label="シミュレーション（前のフレームから順に計算）"; fontsize=11; style=rounded; color="#999999";
       s1 [label="状態 1", fillcolor="#fff3b0"]; s2 [label="状態 2", fillcolor="#fff3b0"];
       s3 [label="…", shape=plaintext, style=""]; s60 [label="状態 60", fillcolor="#fff3b0"];
       s1 -> s2 -> s3 -> s60;
     }
   }

DOP と SOP のソルバー
---------------------

Houdini のシミュレーションは、DOP（Dynamics OPerator）のネットワークで行う。DOP では、シミュレーションする物（オブジェクト）、計算方法（ソルバー）、重力などの力を、それぞれノードで組み立てる。

DOP のネットワークを一から組むのは手間がかかるため、よく使うシミュレーションには、SOP の中で使えるノードが用意されている。これらのノードは、内部に DOP のネットワークを持っていて、入力されたジオメトリをシミュレーションして結果を出力する。

.. list-table:: SOP で使える主なシミュレーションのノード
   :header-rows: 1
   :widths: 30 70

   * - ノード
     - シミュレーションの対象
   * - RBD Bullet Solver
     - 剛体（積み木、壁の破片など）
   * - Vellum Solver
     - 布、髪の毛、柔らかい物
   * - Pyro Solver
     - 煙と炎

このほかに、液体（FLIP）、粒子（POP）、雪や砂のような物質（MPM）などのシミュレーションがある。シミュレーションの多くの機能は Houdini Core では使えないが、Apprentice では使える。

作例: 箱の壁を崩す
------------------

36 個の箱を積んだ壁に、球をぶつけて崩す。ネットワークは :numref:`fig-rbd-network` のとおりである。サンプルコードの ``build_rbd.py`` でも同じネットワークを作れる。

.. graphviz::
   :caption: 剛体シミュレーションのネットワーク
   :name: fig-rbd-network

   digraph rbd {
     node [shape=box, style="rounded,filled", fillcolor="#d4e8f7", fontsize=11];
     pts [label="wall_points（Grid）\n6 x 6 のポイント"];
     brick [label="brick（Box）"];
     wall [label="wall（Copy to Points）"];
     ball [label="ball（Sphere）"];
     vel [label="ball_velocity（Attribute Wrangle）\n初速度 v を与える"];
     merge [label="merge（Merge）"];
     solver [label="rbd_solver（RBD Bullet Solver）"];
     out [label="OUT（Null）", fillcolor="#fff3b0"];
     brick -> wall; pts -> wall; wall -> merge;
     ball -> vel -> merge;
     merge -> solver -> out;
   }

``/obj`` に Geometry ノード ``rbd`` を作り、その中で次のように作る。

#. **Grid**\ （``wall_points``）: 壁の箱を置く位置を作る。次のパラメーターを設定する。

   * :guilabel:`Orientation`: :guilabel:`XY Plane`\ （正面を向いた縦の面）
   * :guilabel:`Size`: ``2.5``、``2.5``
   * :guilabel:`Rows`: ``6``、:guilabel:`Columns`: ``6``
   * :guilabel:`Center` の Y: ``1.5``

   0.5 m 間隔で 6 x 6 のポイントができる。一番下の行のポイントの高さは 0.25 m である。

#. **Box**\ （``brick``）: :guilabel:`Size` を ``0.49``、``0.49``、``0.49`` にする。箱の一辺を間隔の 0.5 m より少し小さくして、最初から箱どうしが重ならないようにする。
#. **Copy to Points**\ （``wall``）: 1 番目の入力に ``brick``、2 番目の入力に ``wall_points`` をつなぐ。:guilabel:`Transform Using Implicit Target Point Normals If No Point N Attribute` をオフにする（:doc:`modeling` を参照）。
#. **Sphere**\ （``ball``）: :guilabel:`Primitive Type` を :guilabel:`Polygon Mesh`、:guilabel:`Radius` を ``0.6``、``0.6``、``0.6``、:guilabel:`Center` を ``0``、``1.2``、``4`` にする。壁の正面 4 m の位置に球を置く。
#. **Attribute Wrangle**\ （``ball_velocity``）: ``ball`` をつなぎ、:guilabel:`VEXpression` に次のコードを入力する。

   .. code-block:: vex
      :linenos:

      v@v = {0, 1, -12};   // 毎秒 12 m で -Z 方向へ

   ``v`` は速度を表すアトリビュートである。RBD Bullet Solver は、シミュレーションを始めるときの速度として ``v`` を読む。

#. **Merge**\ （``merge``）: ``wall`` と ``ball_velocity`` をつなぐ。
#. **RBD Bullet Solver**\ （``rbd_solver``）: ``merge`` を 1 番目の入力につなぐ。:guilabel:`Ground Type` を :guilabel:`Ground Plane` にすると、y = 0 の位置に地面ができる。
#. **Null**\ （``OUT``）: Display フラグを立てる。

プレイバーで再生すると、球が壁にぶつかり、箱が崩れ落ちる。RBD Bullet Solver は、入力のジオメトリのうち、つながっている部分（ここでは箱 1 個、球 1 個）をそれぞれ 1 個の剛体として扱う。出力では、各剛体に ``piece0``、``piece1`` のような名前（``name`` アトリビュート）が付く。

``build_rbd.py`` を hython で実行すると、1、24、48 フレーム目のポイントの高さの平均を表示する。壁が崩れるにつれて値が小さくなることを確かめられる。

キャッシュ
----------

シミュレーションの結果をファイルに保存するには、File Cache ノードを使う。RBD Bullet Solver の後ろ（``OUT`` の前）に File Cache ノードをつなぎ、:guilabel:`Save to Disk` を押すと、全てのフレームの結果がファイルに書き出される。保存先は、:guilabel:`Base Folder`\ （既定は ``$HIP/geo``）と :guilabel:`Base Name`\ （既定は hip ファイルの名前とノードの名前）から決まる。ファイルの形式は、Houdini のジオメトリの形式 ``.bgeo.sc`` である。

書き出した後で :guilabel:`Load from Disk` をオンにすると、File Cache ノードはシミュレーションを計算せず、ファイルから結果を読み込む。どのフレームにもすぐに移動でき、後の工程（マテリアルやレンダリング）の作業が軽くなる。シミュレーションの設定を変えたときは、もう一度 :guilabel:`Save to Disk` を押して書き出し直す。
