付録 B　サンプルコード一覧
============================================================

本書のサンプルコードを種類ごとにまとめる。各ファイルは、本ページで内容を閲覧できるほか、ファイル名のリンクから個別にダウンロードできる。種類ごとの zip ファイルもある。

.. list-table:: サンプルコードの zip ファイル
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - :download:`python_examples.zip <_generated/downloads/python_examples.zip>`
     - Python のスクリプトと検査用の設定ファイル setup.cfg
   * - :download:`glsl_examples.zip <_generated/downloads/glsl_examples.zip>`
     - GLSL（WebGL2）のデモ。HTML ファイルを Chrome で開くと動く
   * - :download:`godot_examples.zip <_generated/downloads/godot_examples.zip>`
     - Godot 4.7 のプロジェクト（第 15 章）
   * - :download:`houdini_examples.zip <_generated/downloads/houdini_examples.zip>`
     - Houdini の hython 用スクリプトと VEX（第 16 章）

Python のスクリプトは、PEP 8 に沿って型ヒントを付け、flake8（行長 120 文字まで）と mypy（``strict = True``）の検査を通している。検査の設定は ``examples/setup.cfg`` にある。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
   :caption: examples/setup.cfg

.. contents:: このページの目次
   :local:
   :depth: 2

Python：共通ライブラリ
------------------------------------------------------------

複数のスクリプトから import して使うモジュールである。単独では実行しない。

.. list-table:: Python：共通ライブラリの一覧
   :header-rows: 1
   :widths: 28 50 22

   * - ファイル
     - 内容
     - 使用する章

   * - ``color.py``
     - 色の生成と変換。
     - :doc:`第 2 章 <basics>`

   * - ``common.py``
     - サンプルスクリプトに共通する出力まわりの処理。
     - ほぼすべてのスクリプト

   * - ``draw2d.py``
     - 2 次元のアニメーションを描くための簡単な描画ライブラリ（Pillow を使う）。
     - :doc:`第 12 章 <animation>`

   * - ``heightmap.py``
     - ハイトマップ（高さの 2 次元配列）を作り、表示する関数（第 7 章）。
     - :doc:`第 7 章 <terrain>`

   * - ``marching_tetrahedra.py``
     - マーチング・テトラヘドラ法による等値面のメッシュ化。
     - :doc:`第 9 章 <implicit>`

   * - ``mesh.py``
     - 三角形メッシュの表現、OBJ 形式での保存、matplotlib による簡易表示。
     - :doc:`第 6 章 <mesh>`、:doc:`第 16 章 <houdini>`

   * - ``meshgen.py``
     - 手続きでメッシュを作る関数（第 6 章）。
     - :doc:`第 6 章 <mesh>`

   * - ``noise.py``
     - ノイズ関数（NumPy でベクトル化した実装）。
     - :doc:`第 3 章 <noise>`、:doc:`第 4 章 <patterns>`

   * - ``poisson_disk.py``
     - ポアソンディスク・サンプリング（Bridson の方法、2007 年）。
     - :doc:`第 10 章 <scattering>`

   * - ``prng.py``
     - 状態を持たない乱数（ハッシュ関数）。
     - :doc:`第 2 章 <basics>`

   * - ``sdf3d.py``
     - 3 次元の距離関数（SDF）と、その組み合わせ方。
     - :doc:`第 9 章 <implicit>`

   * - ``spring.py``
     - ばねと減衰による追従（第 12 章）。
     - :doc:`第 12 章 <animation>`

   * - ``texture.py``
     - テクスチャを作るための小さな道具（第 3〜5 章で使う）。
     - :doc:`第 4 章 <patterns>`

   * - ``video.py``
     - ffmpeg を使った動画の書き出し。
     - :doc:`第 14 章 <video>`

color.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

色の生成と変換。

:download:`color.py をダウンロード <../examples/python/color.py>`

.. literalinclude:: ../examples/python/color.py
   :language: python
   :linenos:

common.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

サンプルスクリプトに共通する出力まわりの処理。

:download:`common.py をダウンロード <../examples/python/common.py>`

.. literalinclude:: ../examples/python/common.py
   :language: python
   :linenos:

draw2d.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

2 次元のアニメーションを描くための簡単な描画ライブラリ（Pillow を使う）。

:download:`draw2d.py をダウンロード <../examples/python/draw2d.py>`

.. literalinclude:: ../examples/python/draw2d.py
   :language: python
   :linenos:

heightmap.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ハイトマップ（高さの 2 次元配列）を作り、表示する関数（第 7 章）。

:download:`heightmap.py をダウンロード <../examples/python/heightmap.py>`

.. literalinclude:: ../examples/python/heightmap.py
   :language: python
   :linenos:

marching_tetrahedra.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

マーチング・テトラヘドラ法による等値面のメッシュ化。

:download:`marching_tetrahedra.py をダウンロード <../examples/python/marching_tetrahedra.py>`

.. literalinclude:: ../examples/python/marching_tetrahedra.py
   :language: python
   :linenos:

mesh.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

三角形メッシュの表現、OBJ 形式での保存、matplotlib による簡易表示。

:download:`mesh.py をダウンロード <../examples/python/mesh.py>`

.. literalinclude:: ../examples/python/mesh.py
   :language: python
   :linenos:

meshgen.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

手続きでメッシュを作る関数（第 6 章）。

:download:`meshgen.py をダウンロード <../examples/python/meshgen.py>`

.. literalinclude:: ../examples/python/meshgen.py
   :language: python
   :linenos:

noise.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ノイズ関数（NumPy でベクトル化した実装）。

:download:`noise.py をダウンロード <../examples/python/noise.py>`

.. literalinclude:: ../examples/python/noise.py
   :language: python
   :linenos:

poisson_disk.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ポアソンディスク・サンプリング（Bridson の方法、2007 年）。

:download:`poisson_disk.py をダウンロード <../examples/python/poisson_disk.py>`

.. literalinclude:: ../examples/python/poisson_disk.py
   :language: python
   :linenos:

prng.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

状態を持たない乱数（ハッシュ関数）。

:download:`prng.py をダウンロード <../examples/python/prng.py>`

.. literalinclude:: ../examples/python/prng.py
   :language: python
   :linenos:

sdf3d.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3 次元の距離関数（SDF）と、その組み合わせ方。

:download:`sdf3d.py をダウンロード <../examples/python/sdf3d.py>`

.. literalinclude:: ../examples/python/sdf3d.py
   :language: python
   :linenos:

spring.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ばねと減衰による追従（第 12 章）。

:download:`spring.py をダウンロード <../examples/python/spring.py>`

.. literalinclude:: ../examples/python/spring.py
   :language: python
   :linenos:

texture.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

テクスチャを作るための小さな道具（第 3〜5 章で使う）。

:download:`texture.py をダウンロード <../examples/python/texture.py>`

.. literalinclude:: ../examples/python/texture.py
   :language: python
   :linenos:

video.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ffmpeg を使った動画の書き出し。

:download:`video.py をダウンロード <../examples/python/video.py>`

.. literalinclude:: ../examples/python/video.py
   :language: python
   :linenos:

Python：図・動画を作るスクリプト
------------------------------------------------------------

``examples/python`` で ``py <ファイル名>`` と実行すると、``out/<スクリプト名>/`` に図や動画を出力する。本書のビルドでは、conf.py がこれらを実行して本文の図を作る。

.. list-table:: Python：図・動画を作るスクリプトの一覧
   :header-rows: 1
   :widths: 28 50 22

   * - ファイル
     - 内容
     - 使用する章

   * - ``boids.py``
     - 第 13 章「群れと粒子」: ボイド（Reynolds、1987 年）と近傍探索。
     - :doc:`第 13 章 <particles>`

   * - ``cave_generation.py``
     - 第 11 章「レベルとダンジョン」: ランダムウォークとセル・オートマトンで洞窟を作る。
     - :doc:`第 11 章 <dungeon>`

   * - ``cellular_automata.py``
     - 第 5 章「規則から生まれる模様」: セル・オートマトンの図と動画を作る。
     - :doc:`第 5 章 <emergent_patterns>`

   * - ``colors.py``
     - 第 2 章「基礎の道具箱」: 色の生成の図を作る。
     - :doc:`第 2 章 <basics>`

   * - ``domain_warp.py``
     - 第 3 章「ノイズ」: ドメインワーピング（座標をノイズで歪める手法）の図を作る。
     - :doc:`第 3 章 <noise>`

   * - ``dungeon_bsp.py``
     - 第 11 章「レベルとダンジョン」: 二分空間分割（BSP）で部屋と通路を作る。
     - :doc:`第 11 章 <dungeon>`

   * - ``easing.py``
     - 第 2 章「基礎の道具箱」: 補間・イージング・範囲変換の図を作る。
     - :doc:`第 2 章 <basics>`

   * - ``expressive_range.py``
     - 第 17 章「生成の設計と評価」: 表現範囲の分析と、生成して検査する方式の図を作る。
     - :doc:`第 17 章 <design>`

   * - ``fabrik.py``
     - 第 12 章「プロシージャルアニメーション」: 逆運動学 FABRIK（Aristidou と Lasenby、2011 年）。
     - :doc:`第 12 章 <animation>`

   * - ``flow_field.py``
     - 第 13 章「群れと粒子」: ノイズから作るベクトル場（流れ場）と、それに沿った粒子の運動。
     - :doc:`第 13 章 <particles>`

   * - ``implicit_meshing.py``
     - 第 9 章「陰関数と体積表現」: 等値面のメッシュ化の図を作る。
     - :doc:`第 9 章 <implicit>`

   * - ``implicit_sdf.py``
     - 第 9 章「陰関数と体積表現」: 3 次元の距離関数と、その組み合わせの図を作る。
     - :doc:`第 9 章 <implicit>`

   * - ``lock_and_key.py``
     - 第 11 章「レベルとダンジョン」: 部屋のグラフに鍵と扉を置き、到達できるかを検証する。
     - :doc:`第 11 章 <dungeon>`

   * - ``loop_noise.py``
     - 第 14 章「映像の生成」: 完全にループするアニメーション（4 次元ノイズを円周上でサンプリングする）。
     - :doc:`第 14 章 <video>`

   * - ``lsystem.py``
     - 第 8 章「文法と成長による形状」: L-system とタートルグラフィックス。
     - :doc:`第 8 章 <grammar>`

   * - ``materials.py``
     - 第 4 章「パターンとマテリアル」: ノイズを組み合わせた素材の図を作る。
     - :doc:`第 4 章 <patterns>`

   * - ``mesh_basics.py``
     - 第 6 章「メッシュの基礎と生成」: メッシュの表現と基本形状の図を作る。
     - :doc:`第 6 章 <mesh>`

   * - ``mesh_sweep.py``
     - 第 6 章「メッシュの基礎と生成」: 回転体とスイープの図、OBJ ファイルを作る。
     - :doc:`第 6 章 <mesh>`

   * - ``motion_basics.py``
     - 第 12 章「プロシージャルアニメーション」: 時間の関数としての動きと、ばねによる追従の図を作る。
     - :doc:`第 12 章 <animation>`

   * - ``motion_graphics.py``
     - 第 14 章「映像の生成」: モーショングラフィックス（イージング、時間差、合成）。
     - :doc:`第 14 章 <video>`

   * - ``noise_animation.py``
     - 第 3 章「ノイズ」: 3 次元ノイズの断面を時間とともに動かすアニメーションと、ループの考え方の図を作る。
     - :doc:`第 3 章 <noise>`

   * - ``noise_fractal.py``
     - 第 3 章「ノイズ」: ノイズを重ねる手法（fBm・乱流・リッジ）と周波数の図を作る。
     - :doc:`第 3 章 <noise>`

   * - ``noise_types.py``
     - 第 3 章「ノイズ」: ノイズの種類と仕組みの図を作る。
     - :doc:`第 1 章 <intro>`、:doc:`第 3 章 <noise>`

   * - ``normal_map.py``
     - 第 4 章「パターンとマテリアル」: ハイトマップから法線マップを作る図を作る。
     - :doc:`第 4 章 <patterns>`

   * - ``particle_system.py``
     - 第 13 章「群れと粒子」: パーティクルシステム（発生・寿命・力・寿命に応じた色）。
     - :doc:`第 13 章 <particles>`

   * - ``patterns_regular.py``
     - 第 4 章「パターンとマテリアル」: 座標の分割による規則パターンの図を作る。
     - :doc:`第 4 章 <patterns>`

   * - ``pbr_maps.py``
     - 第 4 章「パターンとマテリアル」: 1 つの手続きから PBR 用のテクスチャ一式を出力する。
     - :doc:`第 4 章 <patterns>`

   * - ``pixel_sprites.py``
     - 第 5 章「規則から生まれる模様」: 左右対称化とマスクによるドット絵スプライトの生成。
     - :doc:`第 5 章 <emergent_patterns>`

   * - ``procedural_walk.py``
     - 第 12 章「プロシージャルアニメーション」: 足の接地点を予測して踏み替える、手続き的な歩行。
     - :doc:`第 12 章 <animation>`

   * - ``randomness.py``
     - 第 2 章「基礎の道具箱」: 乱数とハッシュ関数の図を作る。
     - :doc:`第 2 章 <basics>`

   * - ``raymarching.py``
     - 第 9 章「陰関数と体積表現」: レイマーチングで距離関数と雲を直接描く。
     - :doc:`第 9 章 <implicit>`

   * - ``reaction_diffusion.py``
     - 第 5 章「規則から生まれる模様」: 反応拡散（Gray-Scott モデル）の図と動画を作る。
     - :doc:`第 5 章 <emergent_patterns>`

   * - ``scatter_points.py``
     - 第 10 章「配置と散布」: 点の配置方法の比較と、ポアソンディスク・サンプリングの図を作る。
     - :doc:`第 10 章 <scattering>`

   * - ``sdf2d.py``
     - 第 4 章「パターンとマテリアル」: 2 次元の距離関数（SDF）で図形を描く図を作る。
     - :doc:`第 4 章 <patterns>`

   * - ``seamless.py``
     - 第 4 章「パターンとマテリアル」: 繰り返し可能（シームレス）なテクスチャの図を作る。
     - :doc:`第 4 章 <patterns>`

   * - ``secondary_motion.py``
     - 第 12 章「プロシージャルアニメーション」: 尻尾や髪のような揺れものを、鎖状につないだばねで動かす。
     - :doc:`第 12 章 <animation>`

   * - ``shape_grammar.py``
     - 第 8 章「文法と成長による形状」: 分割文法（split grammar）による建物の外壁。
     - :doc:`第 8 章 <grammar>`

   * - ``space_colonization.py``
     - 第 8 章「文法と成長による形状」: 空間植民アルゴリズム（Runions ら、2007 年）による樹木。
     - :doc:`第 8 章 <grammar>`

   * - ``street_network.py``
     - 第 11 章「レベルとダンジョン」: 道路の成長規則で街路網を作る（Parish と Müller の方法を簡略化したもの）。
     - :doc:`第 11 章 <dungeon>`

   * - ``terrain_biomes.py``
     - 第 7 章「地形」: 高さと湿度によるバイオームの割り当て。
     - :doc:`第 7 章 <terrain>`

   * - ``terrain_erosion.py``
     - 第 7 章「地形」: 熱侵食と、水滴による水力侵食。
     - :doc:`第 7 章 <terrain>`

   * - ``terrain_heightmap.py``
     - 第 7 章「地形」: ハイトマップの生成（fBm とダイアモンドスクエア法）の図を作る。
     - :doc:`第 7 章 <terrain>`

   * - ``terrain_mesh.py``
     - 第 7 章「地形」: ハイトマップから地形のメッシュを作り、チャンクと LOD を説明する図を作る。
     - :doc:`第 7 章 <terrain>`

   * - ``terrain_rivers.py``
     - 第 7 章「地形」: 窪地の埋め立て、D8 法による流向、集水量から川と湖を求める。
     - :doc:`第 7 章 <terrain>`

   * - ``vegetation.py``
     - 第 10 章「配置と散布」: 地形の高さ・傾斜と密度マップに従って、木と岩を配置する。
     - :doc:`第 10 章 <scattering>`

   * - ``verlet_cloth.py``
     - 第 13 章「群れと粒子」: ベルレ積分と距離の拘束による紐と布（Jakobsen、2001 年の方法）。
     - :doc:`第 13 章 <particles>`

   * - ``video_formats.py``
     - 第 14 章「映像の生成」: 動画の形式と圧縮の設定による容量の違いを測る。
     - :doc:`第 14 章 <video>`

   * - ``voronoi_patterns.py``
     - 第 4 章「パターンとマテリアル」: ボロノイ図（セルラーノイズ）を使った模様の図を作る。
     - :doc:`第 4 章 <patterns>`

   * - ``wfc_overlap.py``
     - 第 5 章「規則から生まれる模様」: 例示からのテクスチャ合成（Wave Function Collapse の重複モデル）。
     - :doc:`第 5 章 <emergent_patterns>`

   * - ``wfc_tiles.py``
     - 第 11 章「レベルとダンジョン」: Wave Function Collapse（タイルモデル）で地図を作る。
     - :doc:`第 11 章 <dungeon>`

boids.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 13 章「群れと粒子」: ボイド（Reynolds、1987 年）と近傍探索。

:download:`boids.py をダウンロード <../examples/python/boids.py>`

.. literalinclude:: ../examples/python/boids.py
   :language: python
   :linenos:

cave_generation.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 11 章「レベルとダンジョン」: ランダムウォークとセル・オートマトンで洞窟を作る。

:download:`cave_generation.py をダウンロード <../examples/python/cave_generation.py>`

.. literalinclude:: ../examples/python/cave_generation.py
   :language: python
   :linenos:

cellular_automata.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 5 章「規則から生まれる模様」: セル・オートマトンの図と動画を作る。

:download:`cellular_automata.py をダウンロード <../examples/python/cellular_automata.py>`

.. literalinclude:: ../examples/python/cellular_automata.py
   :language: python
   :linenos:

colors.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 2 章「基礎の道具箱」: 色の生成の図を作る。

:download:`colors.py をダウンロード <../examples/python/colors.py>`

.. literalinclude:: ../examples/python/colors.py
   :language: python
   :linenos:

domain_warp.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 3 章「ノイズ」: ドメインワーピング（座標をノイズで歪める手法）の図を作る。

:download:`domain_warp.py をダウンロード <../examples/python/domain_warp.py>`

.. literalinclude:: ../examples/python/domain_warp.py
   :language: python
   :linenos:

dungeon_bsp.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 11 章「レベルとダンジョン」: 二分空間分割（BSP）で部屋と通路を作る。

:download:`dungeon_bsp.py をダウンロード <../examples/python/dungeon_bsp.py>`

.. literalinclude:: ../examples/python/dungeon_bsp.py
   :language: python
   :linenos:

easing.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 2 章「基礎の道具箱」: 補間・イージング・範囲変換の図を作る。

:download:`easing.py をダウンロード <../examples/python/easing.py>`

.. literalinclude:: ../examples/python/easing.py
   :language: python
   :linenos:

expressive_range.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 17 章「生成の設計と評価」: 表現範囲の分析と、生成して検査する方式の図を作る。

:download:`expressive_range.py をダウンロード <../examples/python/expressive_range.py>`

.. literalinclude:: ../examples/python/expressive_range.py
   :language: python
   :linenos:

fabrik.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 12 章「プロシージャルアニメーション」: 逆運動学 FABRIK（Aristidou と Lasenby、2011 年）。

:download:`fabrik.py をダウンロード <../examples/python/fabrik.py>`

.. literalinclude:: ../examples/python/fabrik.py
   :language: python
   :linenos:

flow_field.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 13 章「群れと粒子」: ノイズから作るベクトル場（流れ場）と、それに沿った粒子の運動。

:download:`flow_field.py をダウンロード <../examples/python/flow_field.py>`

.. literalinclude:: ../examples/python/flow_field.py
   :language: python
   :linenos:

implicit_meshing.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 9 章「陰関数と体積表現」: 等値面のメッシュ化の図を作る。

:download:`implicit_meshing.py をダウンロード <../examples/python/implicit_meshing.py>`

.. literalinclude:: ../examples/python/implicit_meshing.py
   :language: python
   :linenos:

implicit_sdf.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 9 章「陰関数と体積表現」: 3 次元の距離関数と、その組み合わせの図を作る。

:download:`implicit_sdf.py をダウンロード <../examples/python/implicit_sdf.py>`

.. literalinclude:: ../examples/python/implicit_sdf.py
   :language: python
   :linenos:

lock_and_key.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 11 章「レベルとダンジョン」: 部屋のグラフに鍵と扉を置き、到達できるかを検証する。

:download:`lock_and_key.py をダウンロード <../examples/python/lock_and_key.py>`

.. literalinclude:: ../examples/python/lock_and_key.py
   :language: python
   :linenos:

loop_noise.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 14 章「映像の生成」: 完全にループするアニメーション（4 次元ノイズを円周上でサンプリングする）。

:download:`loop_noise.py をダウンロード <../examples/python/loop_noise.py>`

.. literalinclude:: ../examples/python/loop_noise.py
   :language: python
   :linenos:

lsystem.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 8 章「文法と成長による形状」: L-system とタートルグラフィックス。

:download:`lsystem.py をダウンロード <../examples/python/lsystem.py>`

.. literalinclude:: ../examples/python/lsystem.py
   :language: python
   :linenos:

materials.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 4 章「パターンとマテリアル」: ノイズを組み合わせた素材の図を作る。

:download:`materials.py をダウンロード <../examples/python/materials.py>`

.. literalinclude:: ../examples/python/materials.py
   :language: python
   :linenos:

mesh_basics.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 6 章「メッシュの基礎と生成」: メッシュの表現と基本形状の図を作る。

:download:`mesh_basics.py をダウンロード <../examples/python/mesh_basics.py>`

.. literalinclude:: ../examples/python/mesh_basics.py
   :language: python
   :linenos:

mesh_sweep.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 6 章「メッシュの基礎と生成」: 回転体とスイープの図、OBJ ファイルを作る。

:download:`mesh_sweep.py をダウンロード <../examples/python/mesh_sweep.py>`

.. literalinclude:: ../examples/python/mesh_sweep.py
   :language: python
   :linenos:

motion_basics.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 12 章「プロシージャルアニメーション」: 時間の関数としての動きと、ばねによる追従の図を作る。

:download:`motion_basics.py をダウンロード <../examples/python/motion_basics.py>`

.. literalinclude:: ../examples/python/motion_basics.py
   :language: python
   :linenos:

motion_graphics.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 14 章「映像の生成」: モーショングラフィックス（イージング、時間差、合成）。

:download:`motion_graphics.py をダウンロード <../examples/python/motion_graphics.py>`

.. literalinclude:: ../examples/python/motion_graphics.py
   :language: python
   :linenos:

noise_animation.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 3 章「ノイズ」: 3 次元ノイズの断面を時間とともに動かすアニメーションと、ループの考え方の図を作る。

:download:`noise_animation.py をダウンロード <../examples/python/noise_animation.py>`

.. literalinclude:: ../examples/python/noise_animation.py
   :language: python
   :linenos:

noise_fractal.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 3 章「ノイズ」: ノイズを重ねる手法（fBm・乱流・リッジ）と周波数の図を作る。

:download:`noise_fractal.py をダウンロード <../examples/python/noise_fractal.py>`

.. literalinclude:: ../examples/python/noise_fractal.py
   :language: python
   :linenos:

noise_types.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 3 章「ノイズ」: ノイズの種類と仕組みの図を作る。

:download:`noise_types.py をダウンロード <../examples/python/noise_types.py>`

.. literalinclude:: ../examples/python/noise_types.py
   :language: python
   :linenos:

normal_map.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 4 章「パターンとマテリアル」: ハイトマップから法線マップを作る図を作る。

:download:`normal_map.py をダウンロード <../examples/python/normal_map.py>`

.. literalinclude:: ../examples/python/normal_map.py
   :language: python
   :linenos:

particle_system.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 13 章「群れと粒子」: パーティクルシステム（発生・寿命・力・寿命に応じた色）。

:download:`particle_system.py をダウンロード <../examples/python/particle_system.py>`

.. literalinclude:: ../examples/python/particle_system.py
   :language: python
   :linenos:

patterns_regular.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 4 章「パターンとマテリアル」: 座標の分割による規則パターンの図を作る。

:download:`patterns_regular.py をダウンロード <../examples/python/patterns_regular.py>`

.. literalinclude:: ../examples/python/patterns_regular.py
   :language: python
   :linenos:

pbr_maps.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 4 章「パターンとマテリアル」: 1 つの手続きから PBR 用のテクスチャ一式を出力する。

:download:`pbr_maps.py をダウンロード <../examples/python/pbr_maps.py>`

.. literalinclude:: ../examples/python/pbr_maps.py
   :language: python
   :linenos:

pixel_sprites.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 5 章「規則から生まれる模様」: 左右対称化とマスクによるドット絵スプライトの生成。

:download:`pixel_sprites.py をダウンロード <../examples/python/pixel_sprites.py>`

.. literalinclude:: ../examples/python/pixel_sprites.py
   :language: python
   :linenos:

procedural_walk.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 12 章「プロシージャルアニメーション」: 足の接地点を予測して踏み替える、手続き的な歩行。

:download:`procedural_walk.py をダウンロード <../examples/python/procedural_walk.py>`

.. literalinclude:: ../examples/python/procedural_walk.py
   :language: python
   :linenos:

randomness.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 2 章「基礎の道具箱」: 乱数とハッシュ関数の図を作る。

:download:`randomness.py をダウンロード <../examples/python/randomness.py>`

.. literalinclude:: ../examples/python/randomness.py
   :language: python
   :linenos:

raymarching.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 9 章「陰関数と体積表現」: レイマーチングで距離関数と雲を直接描く。

:download:`raymarching.py をダウンロード <../examples/python/raymarching.py>`

.. literalinclude:: ../examples/python/raymarching.py
   :language: python
   :linenos:

reaction_diffusion.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 5 章「規則から生まれる模様」: 反応拡散（Gray-Scott モデル）の図と動画を作る。

:download:`reaction_diffusion.py をダウンロード <../examples/python/reaction_diffusion.py>`

.. literalinclude:: ../examples/python/reaction_diffusion.py
   :language: python
   :linenos:

scatter_points.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 10 章「配置と散布」: 点の配置方法の比較と、ポアソンディスク・サンプリングの図を作る。

:download:`scatter_points.py をダウンロード <../examples/python/scatter_points.py>`

.. literalinclude:: ../examples/python/scatter_points.py
   :language: python
   :linenos:

sdf2d.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 4 章「パターンとマテリアル」: 2 次元の距離関数（SDF）で図形を描く図を作る。

:download:`sdf2d.py をダウンロード <../examples/python/sdf2d.py>`

.. literalinclude:: ../examples/python/sdf2d.py
   :language: python
   :linenos:

seamless.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 4 章「パターンとマテリアル」: 繰り返し可能（シームレス）なテクスチャの図を作る。

:download:`seamless.py をダウンロード <../examples/python/seamless.py>`

.. literalinclude:: ../examples/python/seamless.py
   :language: python
   :linenos:

secondary_motion.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 12 章「プロシージャルアニメーション」: 尻尾や髪のような揺れものを、鎖状につないだばねで動かす。

:download:`secondary_motion.py をダウンロード <../examples/python/secondary_motion.py>`

.. literalinclude:: ../examples/python/secondary_motion.py
   :language: python
   :linenos:

shape_grammar.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 8 章「文法と成長による形状」: 分割文法（split grammar）による建物の外壁。

:download:`shape_grammar.py をダウンロード <../examples/python/shape_grammar.py>`

.. literalinclude:: ../examples/python/shape_grammar.py
   :language: python
   :linenos:

space_colonization.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 8 章「文法と成長による形状」: 空間植民アルゴリズム（Runions ら、2007 年）による樹木。

:download:`space_colonization.py をダウンロード <../examples/python/space_colonization.py>`

.. literalinclude:: ../examples/python/space_colonization.py
   :language: python
   :linenos:

street_network.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 11 章「レベルとダンジョン」: 道路の成長規則で街路網を作る（Parish と Müller の方法を簡略化したもの）。

:download:`street_network.py をダウンロード <../examples/python/street_network.py>`

.. literalinclude:: ../examples/python/street_network.py
   :language: python
   :linenos:

terrain_biomes.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 7 章「地形」: 高さと湿度によるバイオームの割り当て。

:download:`terrain_biomes.py をダウンロード <../examples/python/terrain_biomes.py>`

.. literalinclude:: ../examples/python/terrain_biomes.py
   :language: python
   :linenos:

terrain_erosion.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 7 章「地形」: 熱侵食と、水滴による水力侵食。

:download:`terrain_erosion.py をダウンロード <../examples/python/terrain_erosion.py>`

.. literalinclude:: ../examples/python/terrain_erosion.py
   :language: python
   :linenos:

terrain_heightmap.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 7 章「地形」: ハイトマップの生成（fBm とダイアモンドスクエア法）の図を作る。

:download:`terrain_heightmap.py をダウンロード <../examples/python/terrain_heightmap.py>`

.. literalinclude:: ../examples/python/terrain_heightmap.py
   :language: python
   :linenos:

terrain_mesh.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 7 章「地形」: ハイトマップから地形のメッシュを作り、チャンクと LOD を説明する図を作る。

:download:`terrain_mesh.py をダウンロード <../examples/python/terrain_mesh.py>`

.. literalinclude:: ../examples/python/terrain_mesh.py
   :language: python
   :linenos:

terrain_rivers.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 7 章「地形」: 窪地の埋め立て、D8 法による流向、集水量から川と湖を求める。

:download:`terrain_rivers.py をダウンロード <../examples/python/terrain_rivers.py>`

.. literalinclude:: ../examples/python/terrain_rivers.py
   :language: python
   :linenos:

vegetation.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 10 章「配置と散布」: 地形の高さ・傾斜と密度マップに従って、木と岩を配置する。

:download:`vegetation.py をダウンロード <../examples/python/vegetation.py>`

.. literalinclude:: ../examples/python/vegetation.py
   :language: python
   :linenos:

verlet_cloth.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 13 章「群れと粒子」: ベルレ積分と距離の拘束による紐と布（Jakobsen、2001 年の方法）。

:download:`verlet_cloth.py をダウンロード <../examples/python/verlet_cloth.py>`

.. literalinclude:: ../examples/python/verlet_cloth.py
   :language: python
   :linenos:

video_formats.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 14 章「映像の生成」: 動画の形式と圧縮の設定による容量の違いを測る。

:download:`video_formats.py をダウンロード <../examples/python/video_formats.py>`

.. literalinclude:: ../examples/python/video_formats.py
   :language: python
   :linenos:

voronoi_patterns.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 4 章「パターンとマテリアル」: ボロノイ図（セルラーノイズ）を使った模様の図を作る。

:download:`voronoi_patterns.py をダウンロード <../examples/python/voronoi_patterns.py>`

.. literalinclude:: ../examples/python/voronoi_patterns.py
   :language: python
   :linenos:

wfc_overlap.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 5 章「規則から生まれる模様」: 例示からのテクスチャ合成（Wave Function Collapse の重複モデル）。

:download:`wfc_overlap.py をダウンロード <../examples/python/wfc_overlap.py>`

.. literalinclude:: ../examples/python/wfc_overlap.py
   :language: python
   :linenos:

wfc_tiles.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 11 章「レベルとダンジョン」: Wave Function Collapse（タイルモデル）で地図を作る。

:download:`wfc_tiles.py をダウンロード <../examples/python/wfc_tiles.py>`

.. literalinclude:: ../examples/python/wfc_tiles.py
   :language: python
   :linenos:

GLSL（WebGL2）
------------------------------------------------------------

HTML ファイルを Chrome で開くと、シェーダーがその場で動く。下の各ファイルの説明にある「ブラウザーで開く」のリンクからも実行できる。

.. list-table:: GLSL（WebGL2）の一覧
   :header-rows: 1
   :widths: 28 50 22

   * - ファイル
     - 内容
     - 使用する章

   * - ``loop_recorder.html``
     - ループする映像の録画（第 14 章）
     - :doc:`第 14 章 <video>`

   * - ``noise.html``
     - ノイズ（第 3 章）
     - :doc:`第 3 章 <noise>`

   * - ``patterns.html``
     - パターンとマテリアル（第 4 章）
     - :doc:`第 4 章 <patterns>`

   * - ``raymarching.html``
     - レイマーチング（距離関数と雲）
     - :doc:`第 9 章 <implicit>`

   * - ``reaction_diffusion.html``
     - 反応拡散（第 5 章）
     - :doc:`第 5 章 <emergent_patterns>`

loop_recorder.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ループする映像の録画（第 14 章）

`ブラウザーで開く <_static/glsl/loop_recorder.html>`__ ／ :download:`loop_recorder.html をダウンロード <../examples/glsl/loop_recorder.html>`

.. literalinclude:: ../examples/glsl/loop_recorder.html
   :language: html
   :linenos:

noise.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ノイズ（第 3 章）

`ブラウザーで開く <_static/glsl/noise.html>`__ ／ :download:`noise.html をダウンロード <../examples/glsl/noise.html>`

.. literalinclude:: ../examples/glsl/noise.html
   :language: html
   :linenos:

patterns.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

パターンとマテリアル（第 4 章）

`ブラウザーで開く <_static/glsl/patterns.html>`__ ／ :download:`patterns.html をダウンロード <../examples/glsl/patterns.html>`

.. literalinclude:: ../examples/glsl/patterns.html
   :language: html
   :linenos:

raymarching.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

レイマーチング（距離関数と雲）

`ブラウザーで開く <_static/glsl/raymarching.html>`__ ／ :download:`raymarching.html をダウンロード <../examples/glsl/raymarching.html>`

.. literalinclude:: ../examples/glsl/raymarching.html
   :language: html
   :linenos:

reaction_diffusion.html
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

反応拡散（第 5 章）

`ブラウザーで開く <_static/glsl/reaction_diffusion.html>`__ ／ :download:`reaction_diffusion.html をダウンロード <../examples/glsl/reaction_diffusion.html>`

.. literalinclude:: ../examples/glsl/reaction_diffusion.html
   :language: html
   :linenos:

Godot
------------------------------------------------------------

Godot 4.7 で ``examples/godot/project.godot`` を開いて実行する。シーンの説明は\ :doc:`godot`\ にある。Pygments の GDScript 用の色分けは ``@onready`` などを含むファイル全体を扱えないため、本ページでは、GDScript の色分けで扱えないファイルを、文法の近い Python の色分けか、色分けなしで表示する。

.. list-table:: Godotの一覧
   :header-rows: 1
   :widths: 28 50 22

   * - ファイル
     - 内容
     - 使用する章

   * - ``project.godot``
     - プロジェクトの設定（メインシーン、画面の大きさなど）
     - :doc:`第 15 章 <godot>`

   * - ``boids.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``dungeon.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``main.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``mesh_primitives.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``procedural_walk.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``scatter.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``terrain.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``world.tscn``
     - シーンの定義（ノードの構成と、割り当てるスクリプト）
     - :doc:`第 15 章 <godot>`

   * - ``scripts/back_to_menu.gd``
     - どのシーンからでも Esc キーでメニュー（main.tscn）に戻れるようにするオートロード。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/boids.gd``
     - ボイド（第 13 章に対応）。分離・整列・結合の 3 つの規則で群れを動かす。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/chunk_job.gd``
     - 1 つのチャンクの生成を表す仕事。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/creature.gd``
     - 手続き的に歩く生き物（第 12 章に対応）。上から見た 4 本足のトカゲ。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/dungeon.gd``
     - 空間の 2 分割（BSP）で部屋と通路を作るダンジョン（第 11 章に対応）。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/fabrik.gd``
     - FABRIK（Forward And Backward Reaching Inverse Kinematics）。第 12 章に対応する。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/main_menu.gd``
     - サンプルのシーンを選んで起動するメニュー。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/mesh_builder.gd``
     - SurfaceTool で基本的な形のメッシュを作る関数集（第 6 章に対応）。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/mesh_primitives.gd``
     - 格子・円柱・回転体のメッシュを実行時に作って並べる（第 6 章に対応）。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/poisson_disk.gd``
     - ポアソンディスク・サンプリング（Bridson の方法）。第 10 章に対応する。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/scatter_demo.gd``
     - 地形の上に木と岩を散布し、MultiMesh で描く（第 10 章に対応）。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/scatterer.gd``
     - 地形の上に木と岩を散布する（第 10 章に対応）。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/terrain_demo.gd``
     - 3 × 3 個のチャンクから成る地形を作り、周りを回りながら見る（第 7 章に対応）。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/terrain_generator.gd``
     - ノイズから地形のチャンクを作る（第 7 章に対応）。
     - :doc:`第 15 章 <godot>`

   * - ``scripts/world.gd``
     - 統合例: カメラが飛ぶにつれて、周りのチャンク（地形と木・岩）を別スレッドで生成する。
     - :doc:`第 15 章 <godot>`

project.godot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`project.godot をダウンロード <../examples/godot/project.godot>`

.. literalinclude:: ../examples/godot/project.godot
   :language: text
   :linenos:

boids.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`boids.tscn をダウンロード <../examples/godot/boids.tscn>`

.. literalinclude:: ../examples/godot/boids.tscn
   :language: text
   :linenos:

dungeon.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`dungeon.tscn をダウンロード <../examples/godot/dungeon.tscn>`

.. literalinclude:: ../examples/godot/dungeon.tscn
   :language: text
   :linenos:

main.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`main.tscn をダウンロード <../examples/godot/main.tscn>`

.. literalinclude:: ../examples/godot/main.tscn
   :language: text
   :linenos:

mesh_primitives.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`mesh_primitives.tscn をダウンロード <../examples/godot/mesh_primitives.tscn>`

.. literalinclude:: ../examples/godot/mesh_primitives.tscn
   :language: text
   :linenos:

procedural_walk.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`procedural_walk.tscn をダウンロード <../examples/godot/procedural_walk.tscn>`

.. literalinclude:: ../examples/godot/procedural_walk.tscn
   :language: text
   :linenos:

scatter.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`scatter.tscn をダウンロード <../examples/godot/scatter.tscn>`

.. literalinclude:: ../examples/godot/scatter.tscn
   :language: text
   :linenos:

terrain.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`terrain.tscn をダウンロード <../examples/godot/terrain.tscn>`

.. literalinclude:: ../examples/godot/terrain.tscn
   :language: text
   :linenos:

world.tscn
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`world.tscn をダウンロード <../examples/godot/world.tscn>`

.. literalinclude:: ../examples/godot/world.tscn
   :language: text
   :linenos:

scripts/back_to_menu.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

どのシーンからでも Esc キーでメニュー（main.tscn）に戻れるようにするオートロード。

:download:`back_to_menu.gd をダウンロード <../examples/godot/scripts/back_to_menu.gd>`

.. literalinclude:: ../examples/godot/scripts/back_to_menu.gd
   :language: gdscript
   :linenos:

scripts/boids.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ボイド（第 13 章に対応）。分離・整列・結合の 3 つの規則で群れを動かす。

:download:`boids.gd をダウンロード <../examples/godot/scripts/boids.gd>`

.. literalinclude:: ../examples/godot/scripts/boids.gd
   :language: python
   :linenos:

scripts/chunk_job.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1 つのチャンクの生成を表す仕事。

:download:`chunk_job.gd をダウンロード <../examples/godot/scripts/chunk_job.gd>`

.. literalinclude:: ../examples/godot/scripts/chunk_job.gd
   :language: gdscript
   :linenos:

scripts/creature.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

手続き的に歩く生き物（第 12 章に対応）。上から見た 4 本足のトカゲ。

:download:`creature.gd をダウンロード <../examples/godot/scripts/creature.gd>`

.. literalinclude:: ../examples/godot/scripts/creature.gd
   :language: gdscript
   :linenos:

scripts/dungeon.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

空間の 2 分割（BSP）で部屋と通路を作るダンジョン（第 11 章に対応）。

:download:`dungeon.gd をダウンロード <../examples/godot/scripts/dungeon.gd>`

.. literalinclude:: ../examples/godot/scripts/dungeon.gd
   :language: python
   :linenos:

scripts/fabrik.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

FABRIK（Forward And Backward Reaching Inverse Kinematics）。第 12 章に対応する。

:download:`fabrik.gd をダウンロード <../examples/godot/scripts/fabrik.gd>`

.. literalinclude:: ../examples/godot/scripts/fabrik.gd
   :language: gdscript
   :linenos:

scripts/main_menu.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

サンプルのシーンを選んで起動するメニュー。

:download:`main_menu.gd をダウンロード <../examples/godot/scripts/main_menu.gd>`

.. literalinclude:: ../examples/godot/scripts/main_menu.gd
   :language: python
   :linenos:

scripts/mesh_builder.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SurfaceTool で基本的な形のメッシュを作る関数集（第 6 章に対応）。

:download:`mesh_builder.gd をダウンロード <../examples/godot/scripts/mesh_builder.gd>`

.. literalinclude:: ../examples/godot/scripts/mesh_builder.gd
   :language: gdscript
   :linenos:

scripts/mesh_primitives.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

格子・円柱・回転体のメッシュを実行時に作って並べる（第 6 章に対応）。

:download:`mesh_primitives.gd をダウンロード <../examples/godot/scripts/mesh_primitives.gd>`

.. literalinclude:: ../examples/godot/scripts/mesh_primitives.gd
   :language: python
   :linenos:

scripts/poisson_disk.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ポアソンディスク・サンプリング（Bridson の方法）。第 10 章に対応する。

:download:`poisson_disk.gd をダウンロード <../examples/godot/scripts/poisson_disk.gd>`

.. literalinclude:: ../examples/godot/scripts/poisson_disk.gd
   :language: gdscript
   :linenos:

scripts/scatter_demo.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

地形の上に木と岩を散布し、MultiMesh で描く（第 10 章に対応）。

:download:`scatter_demo.gd をダウンロード <../examples/godot/scripts/scatter_demo.gd>`

.. literalinclude:: ../examples/godot/scripts/scatter_demo.gd
   :language: text
   :linenos:

scripts/scatterer.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

地形の上に木と岩を散布する（第 10 章に対応）。

:download:`scatterer.gd をダウンロード <../examples/godot/scripts/scatterer.gd>`

.. literalinclude:: ../examples/godot/scripts/scatterer.gd
   :language: gdscript
   :linenos:

scripts/terrain_demo.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3 × 3 個のチャンクから成る地形を作り、周りを回りながら見る（第 7 章に対応）。

:download:`terrain_demo.gd をダウンロード <../examples/godot/scripts/terrain_demo.gd>`

.. literalinclude:: ../examples/godot/scripts/terrain_demo.gd
   :language: text
   :linenos:

scripts/terrain_generator.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ノイズから地形のチャンクを作る（第 7 章に対応）。

:download:`terrain_generator.gd をダウンロード <../examples/godot/scripts/terrain_generator.gd>`

.. literalinclude:: ../examples/godot/scripts/terrain_generator.gd
   :language: gdscript
   :linenos:

scripts/world.gd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

統合例: カメラが飛ぶにつれて、周りのチャンク（地形と木・岩）を別スレッドで生成する。

:download:`world.gd をダウンロード <../examples/godot/scripts/world.gd>`

.. literalinclude:: ../examples/godot/scripts/world.gd
   :language: text
   :linenos:

Houdini
------------------------------------------------------------

hython で実行し、ノードのネットワークを作って .hip ファイルに保存する。説明は\ :doc:`houdini`\ にある。VEX のファイルは、Pygments に VEX 用の色分けが無いため、色分けせずに表示する。

.. list-table:: Houdiniの一覧
   :header-rows: 1
   :widths: 28 50 22

   * - ファイル
     - 内容
     - 使用する章

   * - ``build_lsystem.py``
     - 第 16 章: L-System SOP で植物を作るネットワーク（/obj/lsystem）を組む。
     - :doc:`第 16 章 <houdini>`

   * - ``build_scatter.py``
     - 第 16 章: 島の地形に木を散布するネットワーク（/obj/scatter）を組む。
     - :doc:`第 16 章 <houdini>`

   * - ``build_terrain.py``
     - 第 16 章: 地形を作るネットワーク（/obj/terrain）を組む。
     - :doc:`第 16 章 <houdini>`

   * - ``export_variations.py``
     - 第 16 章: シードを変えながら島と木を生成し、ファイルに書き出す。
     - :doc:`第 16 章 <houdini>`

   * - ``hou_common.py``
     - 第 16 章の Houdini のサンプルで共通に使う関数。
     - :doc:`第 16 章 <houdini>`

   * - ``render_previews.py``
     - 第 16 章の図: Houdini が書き出した OBJ ファイルを matplotlib で描く。
     - :doc:`第 16 章 <houdini>`

   * - ``vex/instance_attribs.vex``
     - Attribute Wrangle ノードで実行する VEX のコード
     - :doc:`第 16 章 <houdini>`、:doc:`第 17 章 <design>`

   * - ``vex/island.vex``
     - Attribute Wrangle ノードで実行する VEX のコード
     - :doc:`第 16 章 <houdini>`

   * - ``vex/slope_density.vex``
     - Attribute Wrangle ノードで実行する VEX のコード
     - :doc:`第 16 章 <houdini>`

build_lsystem.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 16 章: L-System SOP で植物を作るネットワーク（/obj/lsystem）を組む。

:download:`build_lsystem.py をダウンロード <../examples/houdini/build_lsystem.py>`

.. literalinclude:: ../examples/houdini/build_lsystem.py
   :language: python
   :linenos:

build_scatter.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 16 章: 島の地形に木を散布するネットワーク（/obj/scatter）を組む。

:download:`build_scatter.py をダウンロード <../examples/houdini/build_scatter.py>`

.. literalinclude:: ../examples/houdini/build_scatter.py
   :language: python
   :linenos:

build_terrain.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 16 章: 地形を作るネットワーク（/obj/terrain）を組む。

:download:`build_terrain.py をダウンロード <../examples/houdini/build_terrain.py>`

.. literalinclude:: ../examples/houdini/build_terrain.py
   :language: python
   :linenos:

export_variations.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 16 章: シードを変えながら島と木を生成し、ファイルに書き出す。

:download:`export_variations.py をダウンロード <../examples/houdini/export_variations.py>`

.. literalinclude:: ../examples/houdini/export_variations.py
   :language: python
   :linenos:

hou_common.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 16 章の Houdini のサンプルで共通に使う関数。

:download:`hou_common.py をダウンロード <../examples/houdini/hou_common.py>`

.. literalinclude:: ../examples/houdini/hou_common.py
   :language: python
   :linenos:

render_previews.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

第 16 章の図: Houdini が書き出した OBJ ファイルを matplotlib で描く。

:download:`render_previews.py をダウンロード <../examples/houdini/render_previews.py>`

.. literalinclude:: ../examples/houdini/render_previews.py
   :language: python
   :linenos:

vex/instance_attribs.vex
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`instance_attribs.vex をダウンロード <../examples/houdini/vex/instance_attribs.vex>`

.. literalinclude:: ../examples/houdini/vex/instance_attribs.vex
   :language: text
   :linenos:

vex/island.vex
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`island.vex をダウンロード <../examples/houdini/vex/island.vex>`

.. literalinclude:: ../examples/houdini/vex/island.vex
   :language: text
   :linenos:

vex/slope_density.vex
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:download:`slope_density.vex をダウンロード <../examples/houdini/vex/slope_density.vex>`

.. literalinclude:: ../examples/houdini/vex/slope_density.vex
   :language: text
   :linenos:
