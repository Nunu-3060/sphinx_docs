第 10 章 法線マップ
===================

れんがの壁の目地や、岩の表面の細かい凹凸を、すべてメッシュの頂点で表現すると、頂点の数が膨大になる。法線マップは、凹凸による法線の変化をテクスチャーに記録しておき、ライティングの計算で使う法線をピクセルごとに変えることで、少ない頂点のまま細かい凹凸があるように見せる技法である。

この章のサンプルコードは、``examples/chapter10`` フォルダーにある。

法線マップのしくみ
------------------

第 9 章で見たように、面の明るさは法線の向きで決まる。法線マップを使うと、平らな面でも、ピクセルごとに異なる法線でライティングを計算できる。形そのものは変わらないため、オブジェクトの輪郭や、横から見たときの形は平らなままである。

法線マップのテクスチャーには、法線ベクトルの x、y、z の各成分（-1～1）を 0～1 の範囲に変換した値が、R、G、B に記録されている。

.. math::

   (r, g, b) = \frac{\mathbf{n} + 1}{2}

凹凸のない部分の法線は (0, 0, 1) なので、色は (0.5, 0.5, 1) になる。法線マップが全体的に青紫色に見えるのはこのためである。

接空間
------

法線マップに記録されている法線は、ワールド空間やオブジェクト空間ではなく、接空間と呼ばれる座標空間の値である。接空間は、メッシュの表面の各点で定義される座標空間で、次の 3 つの軸を持つ。

.. list-table::
   :header-rows: 1
   :widths: 25 20 55

   * - 軸
     - 対応する成分
     - 向き
   * - 接線（Tangent）
     - x
     - 表面に沿って、テクスチャーの U 座標が増える方向
   * - 従法線（Bitangent）
     - y
     - 表面に沿って、テクスチャーの V 座標が増える方向
   * - 法線（Normal）
     - z
     - 表面に垂直な方向

接空間の値として記録しておくと、同じ法線マップを、どの向きの面にも使える。例えば、床に貼っても壁に貼っても、テクスチャーに対する凹凸の向きは同じになる。

メッシュの頂点には、法線に加えて接線（``TANGENT`` セマンティクス）が記録されている。接線は ``float4`` 型で、xyz が接線の方向、w が従法線の向き（1 または -1）である。従法線は、法線と接線の外積に w を掛けて求める。

.. math::

   \mathbf{B} = (\mathbf{N} \times \mathbf{T}) \, w

w が必要なのは、UV 座標が左右反転しているメッシュ（左右対称のモデルで、テクスチャーを共有している場合など）では、従法線の向きが逆になるためである。

TBN 行列
--------

接空間の法線 :math:`\mathbf{n}_{TS}` をワールド空間に変換するには、ワールド空間の接線 :math:`\mathbf{T}`、従法線 :math:`\mathbf{B}`、法線 :math:`\mathbf{N}` を使う。接空間の x、y、z の各成分は、それぞれ :math:`\mathbf{T}`、:math:`\mathbf{B}`、:math:`\mathbf{N}` の方向の成分なので、次の式で変換できる。

.. math::

   \mathbf{n}_{WS} = n_x \mathbf{T} + n_y \mathbf{B} + n_z \mathbf{N}

:math:`\mathbf{T}`、:math:`\mathbf{B}`、:math:`\mathbf{N}` を行として並べた 3×3 行列を、TBN 行列という。上の式は、行ベクトル :math:`\mathbf{n}_{TS}` に TBN 行列を右から掛ける計算と同じである。

.. math::

   \mathbf{n}_{WS} = \mathbf{n}_{TS}
   \begin{pmatrix}
   \mathbf{T} \\ \mathbf{B} \\ \mathbf{N}
   \end{pmatrix}

URP の ``TransformTangentToWorld`` 関数は、この計算を行う。

法線マップのシェーダー
----------------------

次のシェーダーは、ベースのテクスチャーと法線マップを使い、環境光と拡散反射を計算する。

.. literalinclude:: ../../examples/chapter10/NormalMap.shader
   :language: hlsl
   :caption: NormalMap.shader
   :linenos:

:download:`NormalMap.shader をダウンロード <../../examples/chapter10/NormalMap.shader>`

使い方は、次のとおりである。

#. 法線マップの画像をプロジェクトにインポートする。
#. 画像の Inspector ウィンドウで、:guilabel:`Texture Type` を :guilabel:`Normal map` にして、:guilabel:`Apply` を押す。
#. マテリアルの :guilabel:`Normal Map` に法線マップを設定する。

Directional Light を回転させると、凹凸の陰影がライトの方向に合わせて変わる。:guilabel:`Normal Scale` を 0 にすると凹凸がなくなり、値を大きくすると凹凸が強調される。

コードのポイントは、次のとおりである。

* 頂点シェーダーでは、``GetVertexNormalInputs`` 関数で法線、接線、従法線をワールド空間に変換している。従法線の計算（w の考慮を含む）もこの関数が行う。
* フラグメントシェーダーでは、``UnpackNormalScale`` 関数で、法線マップの色から接空間の法線を取り出している。0～1 の値を -1～1 に戻す処理と、凹凸の強さ（``_NormalScale``）の適用を、この関数が行う。
* ``TransformTangentToWorld`` 関数で、接空間の法線をワールド空間に変換している。補間によって 3 つの軸の長さや直交性が崩れているため、変換した法線を正規化している。
* 法線マップは、ベースのテクスチャーと同じ UV 座標で読み取る。そのため、``_NormalMap`` には ``[NoScaleOffset]`` を付け、Tiling と Offset の入力欄を表示しないようにしている。

.. important::

   法線マップのテクスチャーは、必ず :guilabel:`Texture Type` を :guilabel:`Normal map` にしてインポートする。Unity は、法線マップを環境に応じた形式（例えば、x と y の成分だけを保存する形式）に圧縮する。``UnpackNormalScale`` 関数は、この形式を前提にして法線を取り出すため、:guilabel:`Default` のままでは正しい法線にならない。
