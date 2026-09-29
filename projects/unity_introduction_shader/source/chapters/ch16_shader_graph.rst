第 16 章 Shader Graph
=====================

Shader Graph は、ノードと呼ばれる部品を線でつないで、シェーダーを作る機能である。コードを書かずにシェーダーを作れ、結果をプレビューで確かめながら編集できる。この章では、Shader Graph の基本と、これまでに手書きしたシェーダーとの対応を説明する。

この章のサンプルコードは、``examples/chapter16`` フォルダーにある。

Shader Graph と手書きのシェーダー
---------------------------------

Shader Graph で作ったグラフは、Unity によって ShaderLab と HLSL のコードに変換され、手書きのシェーダーと同じように GPU で実行される。両者の特徴を、次の表にまとめる。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 観点
     - Shader Graph
     - 手書きのシェーダー
   * - 作りやすさ
     - 結果を見ながら編集でき、試行錯誤しやすい
     - 文法と URP のライブラリの知識が必要
   * - ライティング
     - URP の Lit と同じ PBR のライティングを簡単に使える
     - 自分で計算する必要があるが、自由に変えられる
   * - パスの管理
     - ``ShadowCaster`` や ``DepthOnly`` などのパスが自動的に作られる
     - 必要なパスを自分で書く（第 11 章を参照）
   * - 細かい制御
     - ノードで表せない処理は、Custom Function ノードで補う
     - パスの構成や描画の設定を自由に書ける
   * - バージョンアップ
     - URP の変更に合わせて、生成されるコードが自動的に更新される
     - URP のライブラリの変更に合わせて、自分で修正する必要がある

Shader Graph のノードは、これまでに学んだ計算にほぼ 1 対 1 で対応している。手書きでしくみを理解していれば、Shader Graph でも目的のノードを見つけやすい。

グラフの作成
------------

#. Project ウィンドウで右クリックし、:menuselection:`Create --> Shader Graph --> URP --> Unlit Shader Graph` を選ぶ。
#. グラフの名前を付け、ダブルクリックして Shader Graph ウィンドウを開く。

Shader Graph ウィンドウの主な要素は、次のとおりである。

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - 要素
     - 役割
   * - Master Stack
     - グラフの出力。Vertex（頂点シェーダーの出力）と Fragment（フラグメントシェーダーの出力）のブロックがある。
   * - Blackboard
     - マテリアルのプロパティを定義する。手書きのシェーダーの ``Properties`` ブロックに相当する。
   * - Graph Inspector
     - グラフ全体の設定（Material の種類、Surface Type など）と、選択したノードの設定を表示する。
   * - Main Preview
     - グラフの結果をプレビューする。

ノードを追加するには、グラフの空いている場所で右クリックして :guilabel:`Create Node` を選び、名前で検索する。ノードの出力ポートから別のノードの入力ポートへドラッグすると、線でつながる。

リムライトのグラフ
------------------

第 14 章のリムライトを、Unlit Shader Graph で作る。ここでは、ライティングは行わず、ベースの色にリムライトの色を加えるだけにする。

#. Blackboard の :guilabel:`+` を押し、:guilabel:`Color` 型のプロパティ ``Base Color`` と ``Rim Color`` を追加する。``Rim Color`` は、Graph Inspector で :guilabel:`Mode` を :guilabel:`HDR` にする。
#. Blackboard に :guilabel:`Float` 型のプロパティ ``Rim Power`` を追加し、既定値を 3 にする。
#. 次の表のノードを追加し、表の順につなぐ。
#. グラフの左上の :guilabel:`Save Asset` を押して保存する。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ノード
     - つなぎ方
   * - Fresnel Effect
     - :guilabel:`Power` に ``Rim Power`` をつなぐ。:guilabel:`Normal` と :guilabel:`View Dir` は既定（ワールド空間の法線と視線の方向）のままにする。
   * - Multiply
     - Fresnel Effect の出力と ``Rim Color`` を掛ける。
   * - Add
     - ``Base Color`` と Multiply の出力を足す。
   * - Master Stack の Base Color
     - Add の出力をつなぐ。

Fresnel Effect ノードは、:math:`(1 - \mathrm{saturate}(\mathbf{N} \cdot \mathbf{V}))^{p}` を計算するノードで、第 14 章のリムライトの式と同じ計算である。

手書きのシェーダーとの対応
--------------------------

これまでに手書きしたシェーダーの要素と、Shader Graph のノードの対応を、次の表に示す。

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - 手書きのシェーダー
     - Shader Graph のノード
   * - ``Properties`` ブロックのプロパティ
     - Blackboard のプロパティ
   * - ``input.uv``
     - UV
   * - ``SAMPLE_TEXTURE2D``
     - Sample Texture 2D
   * - ``TRANSFORM_TEX``
     - Tiling And Offset
   * - ``_Time.y``
     - Time の :guilabel:`Time` 出力
   * - ``normalWS``
     - Normal Vector（:guilabel:`Space` を :guilabel:`World` にする）
   * - ``GetWorldSpaceNormalizeViewDir``
     - View Direction（:guilabel:`Space` を :guilabel:`World` にする）
   * - ``dot``、``lerp``、``smoothstep``、``step``
     - Dot Product、Lerp、Smoothstep、Step
   * - ``clip(a - cutoff)``
     - Master Stack の :guilabel:`Alpha` と :guilabel:`Alpha Clip Threshold`\ （Graph Inspector で :guilabel:`Alpha Clipping` を有効にする）
   * - 頂点シェーダーでの頂点の移動
     - Master Stack の Vertex ブロックの :guilabel:`Position`
   * - ``Blend``、``ZWrite``、``Queue``
     - Graph Inspector の :guilabel:`Surface Type`、:guilabel:`Blending Mode` など

.. note::

   Vertex ブロックの :guilabel:`Position` には、オブジェクト空間の位置を渡す。第 13 章の手書きのシェーダーのように、クリップ空間の位置を自分で計算する必要はない。

Custom Function ノード
----------------------

ノードの組み合わせで表しにくい処理は、Custom Function ノードを使って HLSL で書ける。次のファイルは、リムライトの計算を HLSL の関数として書いたものである。

.. literalinclude:: ../../examples/chapter16/RimLight.hlsl
   :language: hlsl
   :caption: RimLight.hlsl
   :linenos:

:download:`RimLight.hlsl をダウンロード <../../examples/chapter16/RimLight.hlsl>`

このファイルを使うには、次の手順で Custom Function ノードを設定する。

#. ``RimLight.hlsl`` をプロジェクトの ``Assets`` フォルダーの中にコピーする。
#. Shader Graph ウィンドウで Custom Function ノードを追加する。
#. Graph Inspector で、:guilabel:`Type` を :guilabel:`File` にし、:guilabel:`Source` に ``RimLight.hlsl`` を設定する。
#. :guilabel:`Name` に ``RimLight`` と入力する。関数名の末尾の ``_float`` や ``_half`` は入力しない。
#. :guilabel:`Inputs` に、Vector 3 型の ``Normal`` と ``ViewDir``、Float 型の ``Power`` を追加する。
#. :guilabel:`Outputs` に、Float 型の ``Out`` を追加する。
#. Normal Vector ノードと View Direction ノード（どちらも :guilabel:`Space` を :guilabel:`World` にする）、``Rim Power`` プロパティを入力につなぐ。

Custom Function ノードの関数には、次の決まりがある。

* 関数名の末尾に、精度を表す ``_float`` または ``_half`` を付ける。Shader Graph は、ノードの精度の設定に応じて、どちらかの関数を呼ぶ。
* 戻り値の型は ``void`` にし、出力は ``out`` を付けた引数で返す。
* 引数の名前と順序を、ノードの :guilabel:`Inputs` と :guilabel:`Outputs` の設定に合わせる。

ファイルの先頭の ``#ifndef`` ～ ``#endif`` は、インクルードガードである。同じファイルを複数の Custom Function ノードで使うと、ファイルが複数回読み込まれ、関数が重複して定義されたというエラーになる。インクルードガードは、これを防ぐ。
