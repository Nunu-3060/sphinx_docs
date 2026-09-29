第 9 章 ライティング
====================

現実の物体が立体的に見えるのは、光の当たり方によって面ごとに明るさが異なるためである。この章では、ライトの方向と面の向きから明るさを計算し、オブジェクトに陰影を付ける方法を説明する。

この章のサンプルコードは、``examples/chapter09`` フォルダーにある。

光の反射のモデル
----------------

物体の表面で反射する光は、大きく次の 3 つに分けて考えられる。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 成分
     - 内容
   * - 拡散反射
     - 表面であらゆる方向に均等に散らばる光。見る方向によらず、同じ明るさに見える。物体の基本的な色と陰影を決める。
   * - 鏡面反射
     - 鏡のように特定の方向に強く反射する光。見る方向によって位置が変わる、つやのあるハイライトになる。
   * - 環境光
     - 周囲の物や空から間接的に届く光。ライトが直接当たらない面も、完全には真っ暗にならない。

ここで説明するモデルは、現実の光の振る舞いを簡略化した近似である。Unity の標準の Lit シェーダーは、より現実に近い物理ベースレンダリング（PBR）を使っている。本資料では、しくみを理解しやすい古典的なモデルを扱う。

ライティングの計算では、次のベクトルを使う。すべて表面の点から見た単位ベクトルである。

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - 記号
     - 意味
   * - :math:`\mathbf{N}`
     - 法線（面の向き）
   * - :math:`\mathbf{L}`
     - 表面からライトへ向かう方向
   * - :math:`\mathbf{V}`
     - 表面からカメラへ向かう方向（視線の逆向き）
   * - :math:`\mathbf{H}`
     - :math:`\mathbf{L}` と :math:`\mathbf{V}` の中間の方向（ハーフベクトル）

拡散反射（Lambert 反射）
------------------------

面に当たる光の量は、光が面に垂直に当たるときに最も多く、斜めに当たるほど少なくなる。光の束が斜めに当たると、同じ量の光がより広い面積に広がるためである。この関係を式にしたのが Lambert 反射である。

.. math::

   I_{diffuse} = C_{base} \, C_{light} \max(0,\ \mathbf{N} \cdot \mathbf{L})

:math:`C_{base}` は物体の色、:math:`C_{light}` はライトの色である。:math:`\mathbf{N}` と :math:`\mathbf{L}` はどちらも単位ベクトルなので、内積 :math:`\mathbf{N} \cdot \mathbf{L}` は 2 つのなす角の余弦（cos）になる（第 2 章を参照）。面の裏側からライトが当たる場合は内積が負になるため、0 に切り詰める。

次のシェーダーは、メインライトによる Lambert 反射だけを計算する。

.. literalinclude:: ../../examples/chapter09/Lambert.shader
   :language: hlsl
   :caption: Lambert.shader
   :linenos:

:download:`Lambert.shader をダウンロード <../../examples/chapter09/Lambert.shader>`

球に適用すると、ライトの方向の面が明るく、反対側が真っ暗に表示される。Directional Light を回転させると、明るい面の位置が変わる。

コードのポイントは、次のとおりである。

* ``Lighting.hlsl`` を読み込み、ライトの情報を取得する関数を使えるようにしている。
* 頂点シェーダーでは、``TransformObjectToWorldNormal`` 関数で法線をワールド空間に変換し、フラグメントシェーダーに渡している。ライトの方向もワールド空間で与えられるため、同じ座標空間にそろえる必要がある。
* フラグメントシェーダーでは、補間された法線を ``normalize`` 関数で正規化し直している（第 4 章を参照）。
* ``GetMainLight`` 関数で、メインライトの情報を ``Light`` 構造体として取得している。``direction`` は :math:`\mathbf{L}`、``color`` は :math:`C_{light}` である。``color`` には、ライトの :guilabel:`Intensity` を掛けた値が入っている。
* HLSL の ``saturate`` 関数で、内積を 0～1 に切り詰めている。内積は 1 を超えないため、:math:`\max(0,\ \mathbf{N} \cdot \mathbf{L})` と同じ結果になる。

.. note::

   メインライトは、シーンの中で最も明るい Directional Light である。Lighting ウィンドウの :guilabel:`Sun Source` でライトを指定した場合は、そのライトがメインライトになる。本資料のサンプルは、メインライト以外のライト（ほかの Directional Light、Point Light、Spot Light）を計算しない。

Half Lambert
~~~~~~~~~~~~

Lambert 反射では、ライトが当たらない面が真っ暗になる。明るさの変化をなだらかにしたい場合は、内積を 0～1 の範囲に変換して使う Half Lambert がよく使われる。

.. math::

   I_{diffuse} = C_{base} \, C_{light} \left(\frac{\mathbf{N} \cdot \mathbf{L}}{2} + \frac{1}{2}\right)^2

Half Lambert は、物理的な根拠のない表現上の工夫である。ゲームのキャラクターなど、陰影を柔らかく見せたい場合に使われる。コードでは、``nDotL`` を求める行を次のように変える。

.. code-block:: hlsl

   half nDotL = dot(normalWS, mainLight.direction) * 0.5 + 0.5;
   nDotL = nDotL * nDotL;

鏡面反射と環境光
----------------

Phong 反射
~~~~~~~~~~

鏡面反射は、光がちょうど鏡のように反射する方向から見たときに最も強く見える。Phong 反射では、:math:`\mathbf{L}` を法線に対して反射させた方向 :math:`\mathbf{R}` と、視線の方向 :math:`\mathbf{V}` の内積で、ハイライトの強さを求める。

.. math::

   \mathbf{R} = 2(\mathbf{N} \cdot \mathbf{L})\mathbf{N} - \mathbf{L}, \quad
   I_{specular} = C_{specular} \, C_{light} \max(0,\ \mathbf{R} \cdot \mathbf{V})^{s}

:math:`s` は光沢度（Shininess）で、値が大きいほどハイライトが小さく鋭くなる。

Blinn-Phong 反射
~~~~~~~~~~~~~~~~

Blinn-Phong 反射は、Phong 反射の :math:`\mathbf{R} \cdot \mathbf{V}` の代わりに、ハーフベクトル :math:`\mathbf{H}` と法線の内積を使う。反射ベクトルを計算するより少ない計算で済み、視線とライトの角度が大きい場合でも自然なハイライトになるため、Phong 反射より広く使われている。

.. math::

   \mathbf{H} = \mathrm{normalize}(\mathbf{L} + \mathbf{V}), \quad
   I_{specular} = C_{specular} \, C_{light} \max(0,\ \mathbf{N} \cdot \mathbf{H})^{s}

同じ光沢度では、Blinn-Phong のハイライトは Phong より大きくなる。Phong と同じくらいの大きさにするには、光沢度を 2～4 倍程度にする。

環境光
~~~~~~

Unity では、Lighting ウィンドウの :guilabel:`Environment Lighting` の設定（スカイボックスの色など）から、あらゆる方向から届く環境光が計算される。この環境光は、球面調和関数（Spherical Harmonics、SH）と呼ばれる形式で保存されている。URP では、``SampleSH`` 関数に法線を渡すと、その方向から届く環境光の色が得られる。

.. math::

   I_{ambient} = C_{base} \, C_{SH}(\mathbf{N})

最終的な色は、3 つの成分の和になる。

.. math::

   I = I_{ambient} + I_{diffuse} + I_{specular}

Blinn-Phong のシェーダー
~~~~~~~~~~~~~~~~~~~~~~~~

次のシェーダーは、環境光、拡散反射、鏡面反射を組み合わせる。

.. literalinclude:: ../../examples/chapter09/BlinnPhong.shader
   :language: hlsl
   :caption: BlinnPhong.shader
   :linenos:

:download:`BlinnPhong.shader をダウンロード <../../examples/chapter09/BlinnPhong.shader>`

球に適用すると、ライトの当たる側につやのあるハイライトが表示される。ライトが当たらない側も、環境光によって真っ暗にはならない。カメラを動かすと、ハイライトの位置が変わる。

Lambert のシェーダーからの変更点は、次のとおりである。

* 視線の方向を求めるため、頂点シェーダーでワールド空間の位置 ``positionWS`` を計算し、フラグメントシェーダーに渡している。
* ``GetWorldSpaceNormalizeViewDir`` 関数で、表面からカメラへ向かう単位ベクトル :math:`\mathbf{V}` を求めている。
* ``SampleSH`` 関数で環境光を求め、物体の色を掛けている。

.. note::

   ライティングの計算を頂点シェーダーで行い、結果の色を補間する方法もある（頂点ライティング、Gouraud シェーディング）。計算の回数は減るが、頂点の少ないメッシュではハイライトの形が崩れる。本資料のサンプルは、ライティングの計算をすべてフラグメントシェーダーで行っている（ピクセルライティング）。
