マテリアルとレンダリング
========================

この章では、:doc:`modeling` で作った机に質感を付け、ライトとカメラを置いて、Houdini に付属するレンダラー Karma で画像を作る。Houdini でレンダリングのためのシーンを組む環境を Solaris と呼ぶ。Solaris は、USD という形式でシーンを表す。

USD と Solaris
--------------

USD（Universal Scene Description）は、3DCG のシーン全体（形状、マテリアル、ライト、カメラ、それらの配置）を記述するための形式である。もとは映画制作会社の Pixar が開発し、現在は OpenUSD としてオープンソースで公開されている。多くの 3DCG ソフトウェアが対応していて、異なるソフトウェアの間でシーンを受け渡すのに使われる。

USD のシーンをステージ（stage）と呼ぶ。ステージは、プリム（prim）と呼ばれる要素の木構造である。各プリムは ``/table`` や ``/materials/wood`` のようなパスを持つ。ファイルシステムのディレクトリとファイルに似ている。

Solaris では、LOP（``/stage`` のネットワーク）のノードをつないでステージを組み立てる。SOP のノードがジオメトリを受け取って加工するのと同じように、LOP のノードはステージを受け取って、プリムを追加したり変更したりする。ステージの木構造は、Scene Graph Tree というペインで確かめられる。

Houdini には、LOP の作業に向いた画面の配置が用意されている。メインメニューのバーにある最初のドロップダウンメニュー（デスクトップの切り替え。既定では :guilabel:`Build` と表示されている）で :guilabel:`Solaris` を選ぶと切り替わる。

.. list-table:: この章で使う主な LOP
   :header-rows: 1
   :widths: 30 70

   * - ノード
     - 機能
   * - SOP Import
     - SOP のネットワークの出力を、USD のプリムとして読み込む。
   * - SOP Create
     - LOP のノードの中に SOP のネットワークを作り、その出力をプリムにする。
   * - Merge
     - 複数のステージを 1 つにまとめる。
   * - Material Library
     - マテリアルを定義し、プリムに割り当てる。
   * - Camera
     - カメラを置く。
   * - Dome Light、Distant Light
     - 空全体から降り注ぐ光、太陽のような平行な光を置く。
   * - Karma Render Settings
     - Karma でレンダリングするときの設定（カメラ、解像度、品質、出力ファイル）を決める。
   * - USD Render ROP
     - レンダリングを実行し、画像をファイルに書き出す。

Karma
-----

Karma は、Houdini に付属するレンダラーで、:doc:`cg_basics` で説明したレイトレーシングで画像を計算する。CPU で計算する Karma CPU と、CPU と GPU の両方を使える Karma XPU がある。本資料では Karma CPU を使う。

Solaris のビューポートでは、上部のメニューで表示に使うレンダラーを選べる。Karma CPU を選ぶと、ビューポートの中でレンダリングの結果を確かめながら作業できる。最初はざらついた画像が表示され、時間とともに滑らかになる。

マテリアル
----------

Karma のマテリアルは、MaterialX という形式で定義するのが標準である。MaterialX も、異なるソフトウェアの間でマテリアルを受け渡すために作られたオープンな形式である。

MtlX Standard Surface ノードは、多くの質感を 1 個のノードで表せる汎用のマテリアルである。主なパラメーターは次のとおりである。

.. list-table:: MtlX Standard Surface の主なパラメーター
   :header-rows: 1
   :widths: 25 20 55

   * - タブとパラメーター
     - 内部名
     - 意味
   * - :guilabel:`Base` の :guilabel:`Color`
     - ``base_color``
     - 基本の色。
   * - :guilabel:`Base` の :guilabel:`Metalness`
     - ``metalness``
     - 金属らしさ。0 で非金属、1 で金属。
   * - :guilabel:`Specular` の :guilabel:`Roughness`
     - ``specular_roughness``
     - 表面の粗さ。小さいほど鏡のようにはっきり映り込む。

作例: 机をレンダリングする
--------------------------

:doc:`modeling` で作った ``/obj/table`` を読み込み、床と一緒にレンダリングする。ネットワークは :numref:`fig-render-network` のとおりである。サンプルコードの ``build_render.py`` でも同じネットワークを作れる。

.. graphviz::
   :caption: レンダリングのネットワーク（/stage）
   :name: fig-render-network

   digraph render {
     node [shape=box, style="rounded,filled", fillcolor="#d4e8f7", fontsize=11];
     table [label="table（SOP Import）\n/table"];
     floor [label="floor（SOP Create）\n/floor"];
     merge [label="merge（Merge）"];
     mat [label="materials（Material Library）\n/materials/wood、/materials/floor_mat"];
     cam [label="camera（Camera）\n/cameras/camera"];
     dome [label="dome_light（Dome Light）"];
     sun [label="sun（Distant Light）"];
     settings [label="render_settings（Karma Render Settings）"];
     rop [label="render（USD Render ROP）", fillcolor="#fff3b0"];
     table -> merge; floor -> merge;
     merge -> mat -> cam -> dome -> sun -> settings -> rop;
   }

シーンを読み込む
^^^^^^^^^^^^^^^^

ネットワークエディターで ``/stage`` を開き、次のノードを作る。

#. **SOP Import**\ （``table``）: :guilabel:`SOP Path` を ``/obj/table/OUT``、:guilabel:`Primitive Path` を ``/table`` にする。机の形状が、ステージの ``/table`` に読み込まれる。
#. **SOP Create**\ （``floor``）: :guilabel:`Primitive Path` を ``/floor`` にする。ノードをダブルクリックして中に入ると SOP のネットワークになっているので、Grid ノードを作り、:guilabel:`Size` を ``6``、``6`` にして Display フラグを立てる。:kbd:`U` で ``/stage`` に戻る。
#. **Merge**\ （``merge``）: ``table`` と ``floor`` をつなぐ。

マテリアルを割り当てる
^^^^^^^^^^^^^^^^^^^^^^

#. **Material Library**\ （``materials``）: ``merge`` をつなぐ。ダブルクリックして中に入り、MtlX Standard Surface ノードを 2 個作る。名前を ``wood`` と ``floor_mat`` にする。

   * ``wood``: :guilabel:`Base` タブの :guilabel:`Color` を ``0.45``、``0.28``、``0.15``\ （茶色）、:guilabel:`Specular` タブの :guilabel:`Roughness` を ``0.4`` にする。
   * ``floor_mat``: :guilabel:`Color` を ``0.6``、``0.6``、``0.6``\ （灰色）、:guilabel:`Roughness` を ``0.8`` にする。

#. :kbd:`U` で ``/stage`` に戻り、``materials`` のパラメーターを設定する。:guilabel:`Number of Materials` を ``2`` にし、それぞれの行を次のように設定する。

   .. list-table:: Material Library の設定
      :header-rows: 1
      :widths: 25 25 25 25

      * - :guilabel:`Material VOP`
        - :guilabel:`Material Path`
        - :guilabel:`Assign to Geometry`
        - :guilabel:`Geometry Path`
      * - ``wood``
        - ``/materials/wood``
        - オン
        - ``/table``
      * - ``floor_mat``
        - ``/materials/floor_mat``
        - オン
        - ``/floor``

   1 列目の :guilabel:`Material VOP` は Material Library の中のノードの名前、2 列目の :guilabel:`Material Path` はステージの中のマテリアルのパスである。:guilabel:`Assign to Geometry` をオンにすると、:guilabel:`Geometry Path` のプリムにそのマテリアルが割り当てられる。

カメラとライトを置く
^^^^^^^^^^^^^^^^^^^^

#. **Camera**\ （``camera``）: :guilabel:`Primitive Path` を ``/cameras/camera`` にする。:guilabel:`Translate` を ``3.2``、``2.4``、``3.8`` にし、:guilabel:`Enable Look At` をオンにして、:guilabel:`Look At Position` を ``0``、``0.4``、``0`` にする。カメラが、机の中心の少し上を向く。
#. **Dome Light**\ （``dome_light``）: :guilabel:`Intensity` を ``0.6`` にする。空全体からの柔らかい光で、影の部分も真っ暗にならない。
#. **Distant Light**\ （``sun``）: :guilabel:`Rotate` を ``-50``、``30``、``0``、:guilabel:`Intensity` を ``2`` にする。斜め上から差す平行な光で、はっきりした影を作る。

ライトとカメラも、ステージの中のプリム（``/lights/sun`` など）として追加される。

レンダリングする
^^^^^^^^^^^^^^^^

#. **Karma Render Settings**\ （``render_settings``）: 次のパラメーターを設定する。

   * :guilabel:`Camera`: ``/cameras/camera``
   * :guilabel:`Resolution`: 横を ``1280`` にする。縦は、カメラの縦横比（既定では 16:9）から自動的に ``720`` になる。
   * :guilabel:`Output Picture`: ``$HIP/render/table.jpg``
   * :guilabel:`Path Traced Samples`: ``32``\ （1 ピクセルあたりの光線の本数に関係する値。大きいほどノイズが減り、時間がかかる）

#. **USD Render ROP**\ （``render``）: ``render_settings`` をつなぎ、:guilabel:`Render to Disk` を押す。

レンダリングが終わると、hip ファイルを保存したディレクトリの ``render`` ディレクトリに ``table.jpg`` ができる。hip ファイルを保存する前は、``$HIP`` が Houdini を起動したときの作業ディレクトリなどを指すため、先に hip ファイルを保存しておく。本資料の環境では、レンダリングに約 1 分かかった。

Apprentice では、レンダリングした画像の右下に Houdini のロゴ（透かし）が入る。解像度は 1920 x 1080 までである。

``build_render.py`` を hython で実行した場合は、ネットワークを組み立ててステージのプリムの一覧を表示する。画像も書き出すには、``main()`` の後で ``hou.node("/stage/render").render()`` を実行する。

レンダリングの品質と時間
------------------------

レンダリングの時間は、主に解像度と光線の本数で決まる。作業中は解像度を下げ、:guilabel:`Path Traced Samples` を小さくして素早く確かめ、最後に値を上げて仕上げる。画像にざらつき（ノイズ）が残る場合は :guilabel:`Path Traced Samples` を上げる。
