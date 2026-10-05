コンピューターグラフィックス入門
================================

本資料は、コンピューターグラフィックス（CG）で画像が作られる仕組みを、エンジニア向けにまとめたものである。デジタル画像の基礎から始め、2 次元の図形の描画、座標変換、Z バッファー法による 3 次元の描画、ライティング、テクスチャマッピング、レイトレーシングまでを、Python で小さなレンダラーを作りながら学ぶ。最後に、学んだ内容が GPU を使うリアルタイム CG とどのように対応するかを説明する。

.. toctree::
   :maxdepth: 2
   :caption: 目次

   intro
   overview
   image
   raster2d
   math
   transform
   rasterization
   shading
   texture
   raytracing
   gpu
   glossary
   code
   references

索引と検索
==========

* :ref:`genindex`
* :ref:`search`
