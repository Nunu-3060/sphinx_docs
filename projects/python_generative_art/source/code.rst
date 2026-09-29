サンプルコード一覧
====================

本資料中で使用した ``examples/`` 以下の Python スクリプトを、章をまたいで一括で閲覧できるようにまとめたページ。個別のファイルは各章の本文からも ``literalinclude`` で参照しているが、全体を通して読みたい場合や、手元にまとめて持っておきたい場合はこちらを使う。

:download:`examples.zip <_static/downloads/examples.zip>` として全ファイルをまとめてダウンロードできる。展開すると ``examples/`` ディレクトリの中に本ページと同じ 40 個のスクリプトが入っている。

.. contents:: このページの目次
   :local:
   :depth: 1

animation.py
--------------

:doc:`basics`\ で使用。ライフゲームとリサージュ曲線のアニメーション GIF の書き出し。

:download:`examples/animation.py <../examples/animation.py>`

.. literalinclude:: ../examples/animation.py
   :language: python
   :linenos:

easing.py
-----------

:doc:`basics`\ で使用。線形補間とイージング関数、それを使ったグラデーション・同心円。

:download:`examples/easing.py <../examples/easing.py>`

.. literalinclude:: ../examples/easing.py
   :language: python
   :linenos:

palette.py
------------

:doc:`color`\ で使用。HSV 変換の自前実装、配色パターン、PCCS トーン、グラデーション、パレット抽出。

:download:`examples/palette.py <../examples/palette.py>`

.. literalinclude:: ../examples/palette.py
   :language: python
   :linenos:

oklab.py
----------

:doc:`color`\ で使用。sRGB と OKLab・OKLCH の相互変換、明るさの比較、OKLab による補間。

:download:`examples/oklab.py <../examples/oklab.py>`

.. literalinclude:: ../examples/oklab.py
   :language: python
   :linenos:

color_pattern.py
------------------

:doc:`color`\ で使用。同じ単純な模様を、配色だけを変えて描き比べる。

:download:`examples/color_pattern.py <../examples/color_pattern.py>`

.. literalinclude:: ../examples/color_pattern.py
   :language: python
   :linenos:

truchet.py
------------

:doc:`tiling`\ で使用。トルシェ・タイルによるグリッド配置。

:download:`examples/truchet.py <../examples/truchet.py>`

.. literalinclude:: ../examples/truchet.py
   :language: python
   :linenos:

polygon_tiling.py
-------------------

:doc:`tiling`\ で使用。正三角形・正六角形格子によるモザイク。

:download:`examples/polygon_tiling.py <../examples/polygon_tiling.py>`

.. literalinclude:: ../examples/polygon_tiling.py
   :language: python
   :linenos:

wang_tiles.py
---------------

:doc:`tiling`\ で使用。辺のラベルが一致するように配置するワン・タイル。

:download:`examples/wang_tiles.py <../examples/wang_tiles.py>`

.. literalinclude:: ../examples/wang_tiles.py
   :language: python
   :linenos:

wfc.py
--------

:doc:`tiling`\ で使用。Wave Function Collapse による、隣接制約を満たす配管タイルの配置。

:download:`examples/wfc.py <../examples/wfc.py>`

.. literalinclude:: ../examples/wfc.py
   :language: python
   :linenos:

penrose.py
------------

:doc:`tiling`\ で使用。Robinson 三角形の細分割によるペンローズ・タイリング。

:download:`examples/penrose.py <../examples/penrose.py>`

.. literalinclude:: ../examples/penrose.py
   :language: python
   :linenos:

polar_remap.py
----------------

:doc:`tiling`\ で使用。極座標・対数極座標への変換による放射状・渦巻き状パターン。

:download:`examples/polar_remap.py <../examples/polar_remap.py>`

.. literalinclude:: ../examples/polar_remap.py
   :language: python
   :linenos:

maze.py
---------

:doc:`tiling`\ で使用。再帰的バックトラッキング法による迷路生成と、幅優先探索による経路探索。

:download:`examples/maze.py <../examples/maze.py>`

.. literalinclude:: ../examples/maze.py
   :language: python
   :linenos:

subdivision.py
----------------

:doc:`tiling`\ で使用。矩形の再帰的分割によるモンドリアン風の構成と、四分木による分割。

:download:`examples/subdivision.py <../examples/subdivision.py>`

.. literalinclude:: ../examples/subdivision.py
   :language: python
   :linenos:

symmetry.py
-------------

:doc:`tiling`\ で使用。角度の折り返しによる対称性・万華鏡表現。

:download:`examples/symmetry.py <../examples/symmetry.py>`

.. literalinclude:: ../examples/symmetry.py
   :language: python
   :linenos:

hyperbolic_tiling.py
-----------------------

:doc:`tiling`\ で使用。ポアンカレディスク模型による {p, q} 双曲タイリング。

:download:`examples/hyperbolic_tiling.py <../examples/hyperbolic_tiling.py>`

.. literalinclude:: ../examples/hyperbolic_tiling.py
   :language: python
   :linenos:

phyllotaxis.py
----------------

:doc:`spirals`\ で使用。フィロタキシスと貴金属比（黄金比・白銀比）による螺旋状の点配置。

:download:`examples/phyllotaxis.py <../examples/phyllotaxis.py>`

.. literalinclude:: ../examples/phyllotaxis.py
   :language: python
   :linenos:

spirograph.py
---------------

:doc:`spirals`\ で使用。サイクロイド・ハイポトロコイド・エピトロコイドによるスピログラフ模様。

:download:`examples/spirograph.py <../examples/spirograph.py>`

.. literalinclude:: ../examples/spirograph.py
   :language: python
   :linenos:

polar_curves.py
------------------

:doc:`spirals`\ で使用。対数螺旋（黄金螺旋）とバラ曲線。

:download:`examples/polar_curves.py <../examples/polar_curves.py>`

.. literalinclude:: ../examples/polar_curves.py
   :language: python
   :linenos:

lissajous.py
--------------

:doc:`spirals`\ で使用。リサージュ曲線とハーモノグラフ。

:download:`examples/lissajous.py <../examples/lissajous.py>`

.. literalinclude:: ../examples/lissajous.py
   :language: python
   :linenos:

bezier.py
-----------

:doc:`spirals`\ で使用。ベジェ曲線と Catmull-Rom スプライン、それを使ったブロブ・線の束。

:download:`examples/bezier.py <../examples/bezier.py>`

.. literalinclude:: ../examples/bezier.py
   :language: python
   :linenos:

perlin_noise.py
-----------------

:doc:`noise`\ で使用。パーリンノイズの自前実装、fBm、ドメインワーピング。

:download:`examples/perlin_noise.py <../examples/perlin_noise.py>`

.. literalinclude:: ../examples/perlin_noise.py
   :language: python
   :linenos:

worley.py
-----------

:doc:`noise`\ で使用。Worley ノイズ（セルラーノイズ）の :math:`F_1`・:math:`F_2` と、ドメインワーピングとの組み合わせ。

:download:`examples/worley.py <../examples/worley.py>`

.. literalinclude:: ../examples/worley.py
   :language: python
   :linenos:

flow_field.py
---------------

:doc:`noise`\ で使用。ノイズから作ったフローフィールドに沿ってパーティクルを流す。

:download:`examples/flow_field.py <../examples/flow_field.py>`

.. literalinclude:: ../examples/flow_field.py
   :language: python
   :linenos:

sdf.py
--------

:doc:`shapes`\ で使用。距離関数の基本図形、ブール演算、距離場の可視化。

:download:`examples/sdf.py <../examples/sdf.py>`

.. literalinclude:: ../examples/sdf.py
   :language: python
   :linenos:

circle_packing.py
-------------------

:doc:`shapes`\ で使用。距離関数の和集合で空き距離を求める円充填（サークルパッキング）。

:download:`examples/circle_packing.py <../examples/circle_packing.py>`

.. literalinclude:: ../examples/circle_packing.py
   :language: python
   :linenos:

poisson_disk.py
-----------------

:doc:`shapes`\ で使用。ポアソン円盤サンプリング（Bridson のアルゴリズム）による点配置。

:download:`examples/poisson_disk.py <../examples/poisson_disk.py>`

.. literalinclude:: ../examples/poisson_disk.py
   :language: python
   :linenos:

voronoi.py
------------

:doc:`shapes`\ で使用。ボロノイ図とドロネー三角形分割。

:download:`examples/voronoi.py <../examples/voronoi.py>`

.. literalinclude:: ../examples/voronoi.py
   :language: python
   :linenos:

lloyd.py
----------

:doc:`shapes`\ で使用。ロイド緩和（重み付きを含む）による種点の均等化。

:download:`examples/lloyd.py <../examples/lloyd.py>`

.. literalinclude:: ../examples/lloyd.py
   :language: python
   :linenos:

l_system.py
-------------

:doc:`fractals`\ で使用。L-system の文字列書き換えとタートルグラフィックス。

:download:`examples/l_system.py <../examples/l_system.py>`

.. literalinclude:: ../examples/l_system.py
   :language: python
   :linenos:

mandelbrot.py
---------------

:doc:`fractals`\ で使用。マンデルブロ集合・ジュリア集合の脱出時間アルゴリズム。

:download:`examples/mandelbrot.py <../examples/mandelbrot.py>`

.. literalinclude:: ../examples/mandelbrot.py
   :language: python
   :linenos:

ifs.py
--------

:doc:`fractals`\ で使用。反復関数系（IFS）とカオスゲーム。

:download:`examples/ifs.py <../examples/ifs.py>`

.. literalinclude:: ../examples/ifs.py
   :language: python
   :linenos:

attractors.py
---------------

:doc:`fractals`\ で使用。Clifford・De Jong・Gumowski-Mira のストレンジアトラクター。

:download:`examples/attractors.py <../examples/attractors.py>`

.. literalinclude:: ../examples/attractors.py
   :language: python
   :linenos:

automata.py
-------------

:doc:`automata`\ で使用。1 次元セルオートマトンとライフゲーム。

:download:`examples/automata.py <../examples/automata.py>`

.. literalinclude:: ../examples/automata.py
   :language: python
   :linenos:

reaction_diffusion.py
-----------------------

:doc:`automata`\ で使用。Gray-Scott モデルによる反応拡散系。

:download:`examples/reaction_diffusion.py <../examples/reaction_diffusion.py>`

.. literalinclude:: ../examples/reaction_diffusion.py
   :language: python
   :linenos:

particle.py
-------------

:doc:`particles`\ で使用。基本の Particle クラス、重力・粒子間反発・衝突判定。

:download:`examples/particle.py <../examples/particle.py>`

.. literalinclude:: ../examples/particle.py
   :language: python
   :linenos:

boids.py
----------

:doc:`particles`\ で使用。分離・整列・結合による Boids の群れ行動。

:download:`examples/boids.py <../examples/boids.py>`

.. literalinclude:: ../examples/boids.py
   :language: python
   :linenos:

neighbor_search.py
--------------------

:doc:`particles`\ で使用。格子による空間分割を使った固定半径の近傍探索と、総当たりとの比較。

:download:`examples/neighbor_search.py <../examples/neighbor_search.py>`

.. literalinclude:: ../examples/neighbor_search.py
   :language: python
   :linenos:

evolution.py
--------------

:doc:`evolution`\ で使用。半透明三角形の変異と選択による、(1+1) 進化戦略を使った画像近似。

:download:`examples/evolution.py <../examples/evolution.py>`

.. literalinclude:: ../examples/evolution.py
   :language: python
   :linenos:

image_effects.py
-------------------

:doc:`image_effects`\ で使用。ハーフトーン・誤差拡散法によるディザリング・ピクセルソート。

:download:`examples/image_effects.py <../examples/image_effects.py>`

.. literalinclude:: ../examples/image_effects.py
   :language: python
   :linenos:

stippling.py
--------------

:doc:`image_effects`\ で使用。重み付きボロノイ図による点描。

:download:`examples/stippling.py <../examples/stippling.py>`

.. literalinclude:: ../examples/stippling.py
   :language: python
   :linenos:
