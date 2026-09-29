第 7 章 描画
============

この章では、パーティクルの見た目を決める Renderer モジュール、マテリアル、テクスチャーのアニメーション、描画の順番を説明する。パーティクルの見た目は、動きと同じくらいエフェクトの印象を左右する。

Renderer モジュール
-------------------

Renderer モジュールは、パーティクルをどのような形で、どのマテリアルを使って描画するかを決める。

Render Mode
~~~~~~~~~~~

:guilabel:`Render Mode` で、パーティクルの形を選ぶ。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 値
     - 内容
   * - :guilabel:`Billboard`
     - 常にカメラの方を向く板ポリゴンとして描画する（第 2 章を参照）。最もよく使う。
   * - :guilabel:`Stretched Billboard`
     - 板ポリゴンを、パーティクルの進む向きに引き伸ばして描画する。:guilabel:`Speed Scale` を大きくすると、速いパーティクルほど長く伸びる。火花や雨粒のように、細長く流れて見えるものに使う。
   * - :guilabel:`Horizontal Billboard`
     - 地面に平行な板ポリゴンとして描画する。地面に広がる波紋や衝撃波に使う。
   * - :guilabel:`Vertical Billboard`
     - 地面に垂直に立ち、Y 軸まわりだけ回転してカメラの方を向く板ポリゴンとして描画する。
   * - :guilabel:`Mesh`
     - 指定したメッシュとして描画する。破片や落ち葉のように、立体的な形が必要なものに使う。
   * - :guilabel:`None`
     - 描画しない。Trails モジュールの軌跡だけを描画したいときに使う（第 8 章を参照）。

その他の設定項目
~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 内容
   * - :guilabel:`Material`
     - パーティクルの描画に使うマテリアル。
   * - :guilabel:`Trail Material`
     - Trails モジュールの軌跡の描画に使うマテリアル。
   * - :guilabel:`Sort Mode`
     - 1 つの Particle System の中で、パーティクルを描画する順番（後述）。
   * - :guilabel:`Sorting Fudge`
     - ほかの半透明のオブジェクトとの描画の順番を調整する値（後述）。
   * - :guilabel:`Min Particle Size`、:guilabel:`Max Particle Size`
     - 画面に対するパーティクルの大きさの下限と上限。画面の大きさに対する割合で指定する。カメラに近づいたパーティクルが画面を覆うのを防ぐ。
   * - :guilabel:`Render Alignment`
     - :guilabel:`Billboard` の板ポリゴンをどの向きにそろえるか。:guilabel:`View` はカメラの視線の向き、:guilabel:`World` はワールド座標の軸、:guilabel:`Local` は GameObject の軸にそろえる。
   * - :guilabel:`Cast Shadows`、:guilabel:`Receive Shadows`
     - 影を落とすか、影を受けるか。半透明のパーティクルでは、通常どちらも使わない。

パーティクル用のマテリアル
--------------------------

パーティクルの見た目は、Renderer モジュールの :guilabel:`Material` に設定したマテリアルで決まる。新しく作った Particle System には、URP の既定のパーティクル用マテリアルが設定されている。独自のテクスチャーを使うには、次の手順でマテリアルを作る。

#. Project ウィンドウで右クリックし、:menuselection:`Create --> Material` を選ぶ。
#. 作ったマテリアルの Inspector ウィンドウで、:guilabel:`Shader` に :menuselection:`Universal Render Pipeline --> Particles --> Unlit` を選ぶ。
#. :guilabel:`Surface Type` を :guilabel:`Transparent` にし、:guilabel:`Blending Mode` を選ぶ（後述）。
#. :guilabel:`Base Map` にテクスチャーを設定する。
#. マテリアルを、Renderer モジュールの :guilabel:`Material` に設定する。

URP のパーティクル用シェーダー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

URP には、パーティクル用のシェーダーが 3 つある。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - シェーダー
     - 内容
   * - Particles/Unlit
     - ライトの影響を受けない。炎、光、火花など、自分で光って見えるものに使う。処理が最も軽い。
   * - Particles/Simple Lit
     - 簡易的な計算で、ライトの影響を受ける。
   * - Particles/Lit
     - 物理ベースの計算で、ライトの影響を受ける。煙やちりのように、周りの明るさに合わせて見え方を変えたいものに使う。

エフェクトの多くは、Particles/Unlit で作れる。ライトの影響を受ける煙を作りたい場合でも、まず Particles/Simple Lit を試すとよい。

Blending Mode
~~~~~~~~~~~~~

:guilabel:`Surface Type` が :guilabel:`Transparent` のとき、:guilabel:`Blending Mode` で、パーティクルの色と背景の色の混ぜ方を選ぶ。パーティクルの色を :math:`C_s`、不透明度を :math:`\alpha_s`、背景の色を :math:`C_d` とすると、画面に描かれる色 :math:`C` は次のようになる。

.. list-table::
   :header-rows: 1
   :widths: 20 35 45

   * - 値
     - 色の計算
     - 使いどころ
   * - :guilabel:`Alpha`
     - :math:`C = \alpha_s C_s + (1 - \alpha_s) C_d`
     - 煙、ちり、雲など、背景を隠すもの
   * - :guilabel:`Premultiply`
     - :math:`C = C_s + (1 - \alpha_s) C_d`
     - あらかじめ不透明度を掛けた色を持つテクスチャー
   * - :guilabel:`Additive`
     - :math:`C = \alpha_s C_s + C_d`
     - 炎、光、火花、魔法など、光るもの
   * - :guilabel:`Multiply`
     - :math:`C = C_s C_d`
     - 焦げ跡や影のように、背景を暗くするもの

:guilabel:`Additive`\ （加算合成）は、背景の色にパーティクルの色を足すため、重なるほど明るくなる。光るものを表現するのに向いている。また、足し算は順番を入れ替えても結果が変わらないため、パーティクルを描画する順番を気にしなくてよい。

一方、:guilabel:`Alpha`\ （アルファブレンド）は、描画する順番によって結果が変わる。奥のパーティクルから順に描画しないと、手前のパーティクルが奥のパーティクルに隠れたように見えることがある（後述）。

その他の設定項目
~~~~~~~~~~~~~~~~

Particles/Unlit のマテリアルの主な設定項目を次の表にまとめる。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 内容
   * - :guilabel:`Render Face`
     - 表面、裏面、両面のどれを描画するか。
   * - :guilabel:`Alpha Clipping`
     - 有効にすると、不透明度がしきい値より小さい部分を描画しない。
   * - :guilabel:`Color Mode`
     - テクスチャーの色と、パーティクルの色（:guilabel:`Start Color` や Color over Lifetime モジュールの色）の混ぜ方。既定の :guilabel:`Multiply` では、2 つの色を掛け合わせる。
   * - :guilabel:`Flip-Book Blending`
     - Texture Sheet Animation モジュールのコマとコマの間を、2 つのコマを混ぜて滑らかに切り替える。
   * - :guilabel:`Soft Particles`
     - パーティクルが地面や壁と交わる部分を、ぼかして目立たなくする。使うには、URP Asset の :guilabel:`Depth Texture` を有効にする。
   * - :guilabel:`Camera Fading`
     - カメラに近づいたパーティクルを透明にする。
   * - :guilabel:`Distortion`
     - 背景をゆがめて、陽炎のような表現をする。使うには、URP Asset の :guilabel:`Opaque Texture` を有効にする。

:guilabel:`Soft Particles` を使わない場合、板ポリゴンのパーティクルが地面と交わると、交わった部分に直線の境目が見える。煙のように地面の近くに漂うパーティクルでは、:guilabel:`Soft Particles` を有効にするとよい。

:guilabel:`Flip-Book Blending` を有効にすると、マテリアルの Inspector ウィンドウの :guilabel:`Vertex Streams` に、必要なデータが足りないことを示す表示と :guilabel:`Fix Now` ボタンが表示される。ボタンを押すと、Renderer モジュールの設定が自動で修正される。

Built-in Render Pipeline のシェーダー
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Built-in Render Pipeline では、パーティクル用のシェーダーとして Particles/Standard Unlit と Particles/Standard Surface を使う。古い資料には、Legacy Shaders/Particles の下にあるシェーダーを使うものもある。

Built-in Render Pipeline 用のシェーダーを使ったマテリアルは、URP では正しく描画されず、パーティクルがピンク色（マゼンタ）で表示される。古いプロジェクトやアセットを URP で使う場合は、マテリアルのシェーダーを URP 用のものに変更する。:menuselection:`Window --> Rendering --> Render Pipeline Converter` で、マテリアルをまとめて変換することもできる。

テクスチャー
------------

パーティクル用のテクスチャーは、中心が明るく、外側に向かって透明になる画像を使うことが多い。外側を完全に透明にしておかないと、板ポリゴンの四角い輪郭が見えてしまう。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Blending Mode
     - テクスチャーの作り方
   * - :guilabel:`Alpha`
     - アルファチャンネルに形を描く。色の部分は、形の外側も含めて同じ色にしておくとよい。
   * - :guilabel:`Additive`
     - 背景を黒にして、形を明るい色で描く。黒い部分は足しても背景が変わらないため、透明に見える。

テクスチャーのインポート設定では、次の点を確認する。

* アルファチャンネルを使う場合は、:guilabel:`Alpha Source` を :guilabel:`Input Texture Alpha` にし、:guilabel:`Alpha Is Transparency` を有効にする。
* テクスチャーの端がほかのコマや反対側の端とにじまないように、:guilabel:`Wrap Mode` を :guilabel:`Clamp` にする。

Texture Sheet Animation モジュール
----------------------------------

Texture Sheet Animation モジュールは、1 枚のテクスチャーを格子状のコマに分け、コマを切り替えてアニメーションさせる。炎の揺らめきや爆発の煙のように、1 枚の画像では表せない変化を表現できる。コマを並べたテクスチャーを、フリップブックやスプライトシートという。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 設定項目
     - 内容
   * - :guilabel:`Mode`
     - :guilabel:`Grid` は、1 枚のテクスチャーを格子状に分ける。:guilabel:`Sprites` は、スプライトのリストを使う。
   * - :guilabel:`Tiles`
     - :guilabel:`Grid` のときの、横（X）と縦（Y）のコマの数。
   * - :guilabel:`Animation`
     - :guilabel:`Whole Sheet` は、全体のコマを順に使う。:guilabel:`Single Row` は、1 行のコマだけを使う。
   * - :guilabel:`Time Mode`
     - コマを進める基準。:guilabel:`Lifetime` は寿命、:guilabel:`Speed` はパーティクルの速さ、:guilabel:`FPS` は 1 秒あたりのコマ数で進める。
   * - :guilabel:`Frame over Time`
     - :guilabel:`Time Mode` が :guilabel:`Lifetime` のとき、寿命の間にどのコマを表示するかを示すカーブ。
   * - :guilabel:`Start Frame`
     - 最初に表示するコマ。ランダムにすると、パーティクルごとに異なるコマから始まる。
   * - :guilabel:`Cycles`
     - 寿命の間に、アニメーションを何回繰り返すか。

たとえば、横 4 コマ、縦 4 コマの合計 16 コマのテクスチャーを使う場合、:guilabel:`Tiles` を X = 4、Y = 4 にする。:guilabel:`Frame over Time` が既定の 0 から 1 に上がる直線のとき、寿命の間に 16 コマが順に表示される。

:guilabel:`Single Row` にして :guilabel:`Row Mode` を :guilabel:`Random` にすると、パーティクルごとにランダムな行のコマを使う。1 枚のテクスチャーに形の違う破片などを並べておき、パーティクルごとに異なる形を表示したいときに使う。

描画の順番
----------

半透明のパーティクルを :guilabel:`Alpha` のマテリアルで描画する場合、奥にあるものから順に描画しないと、前後関係が正しく表示されない。この順番は、次の 2 つの段階で決まる。

パーティクル同士の順番
~~~~~~~~~~~~~~~~~~~~~~

1 つの Particle System の中のパーティクルの順番は、Renderer モジュールの :guilabel:`Sort Mode` で決める。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 値
     - 内容
   * - :guilabel:`None`
     - 並べ替えない。
   * - :guilabel:`By Distance`
     - カメラから遠いパーティクルから順に描画する。
   * - :guilabel:`Oldest in Front`
     - 古いパーティクルを手前に描画する。
   * - :guilabel:`Youngest in Front`
     - 新しいパーティクルを手前に描画する。
   * - :guilabel:`By Depth`
     - カメラの視線の向きの深さで、遠いパーティクルから順に描画する。

煙のように :guilabel:`Alpha` で描画するパーティクルでは、:guilabel:`By Distance` を選ぶと前後関係が自然になる。並べ替えには計算が必要なため、:guilabel:`Additive` のように順番が結果に影響しない場合は :guilabel:`None` でよい。

Particle System 同士の順番
~~~~~~~~~~~~~~~~~~~~~~~~~~

URP は、半透明のオブジェクトを、オブジェクトごとにカメラから遠い順に描画する。Particle System は、1 つの Particle System 全体で 1 つのオブジェクトとして扱われる。そのため、炎と煙のように重なり合う 2 つの Particle System では、見る角度によって描画の順番が入れ替わり、ちらついて見えることがある。

この場合は、次のいずれかの方法で順番を固定する。

* Renderer モジュールの :guilabel:`Sorting Fudge` を調整する。値を小さくするほど、ほかの半透明のオブジェクトより手前に描画されやすくなる。
* マテリアルの :guilabel:`Sorting Priority` を調整する。値が大きいマテリアルほど後に描画され、手前に表示される。
* Renderer モジュールの :guilabel:`Order in Layer` を調整する。値が大きいほど後に描画され、手前に表示される。
