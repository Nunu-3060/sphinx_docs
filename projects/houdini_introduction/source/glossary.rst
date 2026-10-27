用語集
======

本資料で使った主な用語をまとめる。英字の用語をアルファベット順に、その後に日本語の用語を五十音順に並べた。括弧の中は、詳しく説明している章である。

英字
----

.. glossary::

   Apprentice
      Houdini の無償の非商用版。保存するファイルの形式、レンダリングの解像度などに制限がある。（:doc:`overview`）

   Attribute Wrangle
      VEX のコードを、ジオメトリの要素ごとに実行する SOP。（:doc:`vex`）

   Copy to Points
      形状を、別の形状の各ポイントにコピーする SOP。ポイントの ``pscale``、``scale``、``orient`` などのアトリビュートで、コピーの大きさや向きを変えられる。（:doc:`modeling`、:doc:`procedural`）

   DAG
      閉路の無い有向グラフ（Directed Acyclic Graph）。Houdini のネットワークはこの形になる。（:doc:`overview`）

   DOP
      シミュレーションを行うノードとネットワーク。Dynamics OPerator の略。（:doc:`nodes`、:doc:`simulation`）

   For-Each ループ
      Block Begin ノードと Block End ノードの間のノードを、要素ごとに繰り返し実行する仕組み。（:doc:`procedural`）

   HDA
      Houdini Digital Asset の略。:term:`デジタルアセット` を参照。

   hip ファイル
      Houdini のシーンファイル。Apprentice では拡張子が ``.hipnc`` になる。（:doc:`ui`）

   HOM
      Houdini Object Model の略。Houdini の Python API（``hou`` モジュール）のこと。（:doc:`python`）

   Hscript
      Houdini 独自の式言語とコマンド言語。パラメーターの式は、既定では Hscript で書く。（:doc:`expressions`）

   hython
      Houdini に付属する Python のインタープリター。画面を開かずに Houdini の機能を使える。（:doc:`python`）

   Karma
      Houdini に付属するレンダラー。CPU で計算する Karma CPU と、GPU も使える Karma XPU がある。（:doc:`rendering`）

   LOP
      USD のステージを組み立てるノードとネットワーク。Solaris とも呼ぶ。（:doc:`nodes`、:doc:`rendering`）

   MaterialX
      マテリアルを記述するためのオープンな形式。Karma のマテリアルの標準である。（:doc:`rendering`）

   Null ノード
      入力をそのまま出力するノード。ネットワークの出口の目印（``OUT``）として使う。（:doc:`nodes`）

   OBJ
      シーンに置く物（オブジェクト）を扱うノードとネットワーク。``/obj`` にある。（:doc:`nodes`）

   Python SOP
      Python のコードでジオメトリを作ったり変更したりする SOP。（:doc:`python`）

   ROP
      レンダリングやファイルの書き出しを行うノード。Render OPerator の略。（:doc:`nodes`）

   Solaris
      Houdini で、USD を使ってレンダリングのためのシーンを組む環境。:term:`LOP` を参照。（:doc:`rendering`）

   SOP
      ジオメトリを作り、加工するノードとネットワーク。Surface OPerator の略。（:doc:`nodes`）

   USD
      Universal Scene Description の略。3DCG のシーン全体を記述する形式。（:doc:`rendering`）

   UV 座標
      形状の表面に画像を貼るための、2 次元の座標。（:doc:`cg_basics`）

   VEX
      ジオメトリの要素ごとの処理を並列に実行する、C 言語に似た言語。（:doc:`vex`）

   VOP
      VEX のプログラムをノードで組み立てる仕組み。マテリアルの定義にも使う。（:doc:`vex`）

日本語
------

.. glossary::

   アトリビュート
      ジオメトリの要素ごとに持たせる名前付きのデータ。位置（``P``）や色（``Cd``）もアトリビュートである。（:doc:`attributes`）

   インスタンス
      デジタルアセットの定義から作った個々のノード。（:doc:`hda`）

   エクスプレッション
      パラメーターに入力する式。値が必要になるたびに計算される。（:doc:`expressions`）

   オブジェクト
      ``/obj`` に置く、シーンの中の 1 個の物。位置や表示の有無を持つ。（:doc:`nodes`）

   キーフレーム
      あるフレームでのパラメーターの値を指定したもの。間のフレームの値は補間される。（:doc:`expressions`）

   キャッシュ
      計算の結果を保存しておき、再利用すること。また、保存したファイル。（:doc:`nodes`、:doc:`simulation`）

   クック
      ノードが処理を実行して結果を作ること。（:doc:`nodes`）

   グループ
      ジオメトリの要素に付ける名前付きの集合。ノードの処理の対象を絞るのに使う。（:doc:`attributes`）

   コンテキスト
      ネットワークが扱うデータの種類。SOP、LOP、DOP などがある。（:doc:`nodes`）

   シェルフツール
      シェルフに置くボタン。押すとスクリプトが実行される。（:doc:`ui`、:doc:`python`）

   ジオメトリ
      形状のデータ。ポイント、バーテックス、プリミティブ、ディテールと、それらのアトリビュートからなる。（:doc:`attributes`）

   シミュレーション
      物理法則に従って、前のフレームの状態から次のフレームの状態を計算すること。（:doc:`simulation`）

   ステージ
      USD のシーン。プリムの木構造である。（:doc:`rendering`）

   スペアパラメーター
      ノードに後から追加したパラメーター。（:doc:`vex`）

   タプル
      パラメーターの、複数の成分をまとめたもの。例えば ``t`` は ``tx``、``ty``、``tz`` のタプルである。（:doc:`expressions`）

   チャンネル参照
      ``ch()`` 関数で、他のパラメーターの値を参照すること。（:doc:`expressions`）

   ディスプレイフラグ
      ビューポートに表示するノードを示すフラグ。（:doc:`nodes`）

   ディテール
      ジオメトリ全体を表す要素。ジオメトリに 1 つだけある。（:doc:`attributes`）

   デジタルアセット
      ネットワークを 1 個の新しい種類のノードとしてまとめたもの。HDA とも呼ぶ。（:doc:`hda`）

   ネットワーク
      ノードをワイヤーでつないだもの。（:doc:`nodes`）

   ノード
      1 つの処理を表す部品。入力を受け取り、パラメーターに従って処理し、結果を出力する。（:doc:`nodes`）

   バーテックス
      プリミティブの角。プリミティブがどのポイントを使うかを表す。（:doc:`attributes`）

   バイパスフラグ
      ノードの処理を無効にし、入力をそのまま出力させるフラグ。（:doc:`nodes`）

   パラメーター
      ノードの動作を決める値。（:doc:`ui`、:doc:`expressions`）

   非破壊編集
      作った結果を壊さずに、途中の手順を編集できること。（:doc:`nodes`）

   フラグ
      ノードの左右の端にある、ノードの状態を切り替えるスイッチ。（:doc:`nodes`）

   プリミティブ
      ポイントをつないで作る形状の単位。ポリゴン、曲線、球などがある。（:doc:`attributes`）

   プリム
      USD のステージの要素。``/table`` のようなパスを持つ。（:doc:`rendering`）

   プロシージャル
      形状を直接編集するのではなく、形状を作る手順を組み立てて形状を作る方法。（:doc:`overview`）

   ポイント
      空間の中の位置を表す要素。（:doc:`attributes`）

   法線
      面がどちらを向いているかを表す、長さ 1 のベクトル。（:doc:`cg_basics`）

   マテリアル
      物の表面の質感（色、粗さ、金属らしさなど）を表すもの。（:doc:`cg_basics`、:doc:`rendering`）

   レイトレーシング
      カメラから光線を飛ばし、物に当たって反射する光をたどって画像を計算する方法。（:doc:`cg_basics`）

   レンダリング
      シーンの情報から画像を計算する処理。（:doc:`cg_basics`、:doc:`rendering`）

   ローカル変数
      ノードが要素を 1 つずつ処理するときに、処理中の要素の値を表す変数。``$TY`` など。（:doc:`attributes`）
