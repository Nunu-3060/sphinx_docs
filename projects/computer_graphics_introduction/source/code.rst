サンプルコード一覧
==================

本資料で使用した ``examples/`` 以下の Python スクリプトをまとめたページである。各章の本文では、スクリプトの一部だけを抜き出して示している。全体を通して読みたい場合は、このページを使う。

:download:`examples.zip <_static/downloads/examples.zip>` から全てのスクリプトをまとめてダウンロードできる。展開すると、``examples`` ディレクトリの中に、このページと同じ 8 個のスクリプトが入っている。

各スクリプトの実行方法は、:doc:`intro`\ の「サンプルコードの実行方法」の節で説明している。

.. contents:: このページの目次
   :local:
   :depth: 1

cg_utils.py
-----------

全ての章で使用する共通のモジュールである。ベクトルの正規化、sRGB のガンマ補正、画像の保存と拡大、図を横に並べる関数などを定義している。

:download:`examples/cg_utils.py <../examples/cg_utils.py>`

.. literalinclude:: ../examples/cg_utils.py
   :language: python
   :linenos:

image_basics.py
---------------

:doc:`image`\ で使用する。解像度の比較、R、G、B のチャンネル、ガンマ補正とグラデーション、アルファ値による合成の図を作る。

:download:`examples/image_basics.py <../examples/image_basics.py>`

.. literalinclude:: ../examples/image_basics.py
   :language: python
   :linenos:

raster2d.py
-----------

:doc:`raster2d`\ で使用する。ブレゼンハムのアルゴリズムによる線分、エッジ関数による三角形の塗りつぶし、重心座標による色の補間、スーパーサンプリングの図を作る。

:download:`examples/raster2d.py <../examples/raster2d.py>`

.. literalinclude:: ../examples/raster2d.py
   :language: python
   :linenos:

transform.py
------------

:doc:`transform`\ で使用する。2 次元と 3 次元の変換行列、ビュー変換、投影変換の関数を定義し、変換の順序と投影の方法を比べる図を作る。変換行列の関数は ``renderer.py`` などからも使う。

:download:`examples/transform.py <../examples/transform.py>`

.. literalinclude:: ../examples/transform.py
   :language: python
   :linenos:

renderer.py
-----------

:doc:`rasterization`\ で使用する。三角形メッシュの作成と、Z バッファー法によるラスタライズを行うソフトウェアレンダラーである。深度と透視補正補間の図を作る。``shading.py`` と ``texture.py`` からも使う。

:download:`examples/renderer.py <../examples/renderer.py>`

.. literalinclude:: ../examples/renderer.py
   :language: python
   :linenos:

shading.py
----------

:doc:`shading`\ で使用する。ランバート反射とブリン-フォンの反射モデルによる照明の計算と、フラット、グーロー、フォンの各シェーディングの図を作る。照明の関数は ``texture.py`` と ``raytracer.py`` からも使う。

:download:`examples/shading.py <../examples/shading.py>`

.. literalinclude:: ../examples/shading.py
   :language: python
   :linenos:

texture.py
----------

:doc:`texture`\ で使用する。テクスチャのサンプリング（最近傍補間、バイリニア補間、ミップマップとトライリニア補間）と、テクスチャを貼った物体の図を作る。

:download:`examples/texture.py <../examples/texture.py>`

.. literalinclude:: ../examples/texture.py
   :language: python
   :linenos:

raytracer.py
------------

:doc:`raytracing`\ で使用する。球、平面、三角形との交差判定、影と反射を含むレイトレーシング、パストレーシングの図を作る。

:download:`examples/raytracer.py <../examples/raytracer.py>`

.. literalinclude:: ../examples/raytracer.py
   :language: python
   :linenos:
