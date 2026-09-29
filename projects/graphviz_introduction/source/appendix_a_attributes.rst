属性早見表
==========

本資料で使用した主な属性の一覧です。すべての属性は、公式ドキュメントの Attributes（付録 D）で確認できます。

「対象」の列は、その属性を指定できる要素を表します。G はグラフ、C はクラスター、S はサブグラフ、N はノード、E はエッジです。「意味」の列の末尾の括弧内にレイアウトエンジンの名前がある属性は、そのレイアウトエンジンでだけ使えます。

.. list-table::
   :header-rows: 1
   :widths: 20 12 20 38 10

   * - 属性
     - 対象
     - 既定値
     - 意味
     - 参照
   * - ``label``
     - G、C、N、E
     - ノードは ``\N``\ （ID）、ほかはなし
     - ラベル
     - 6 章
   * - ``xlabel``
     - N、E
     - なし
     - ノードやエッジの外側に表示するラベル
     - 6 章
   * - ``headlabel``、``taillabel``
     - E
     - なし
     - エッジの終点側、始点側に表示するラベル
     - 6 章
   * - ``labelloc``
     - G、C、N
     - グラフは ``b``、クラスターは ``t``、ノードは ``c``
     - ラベルの縦の位置（``t`` は上、``c`` は中央、``b`` は下）
     - 6 章
   * - ``labeljust``
     - G、C
     - ``c``
     - グラフやクラスターのラベルの横の位置（``l`` は左、``r`` は右）
     - 8 章
   * - ``shape``
     - N
     - ``ellipse``
     - ノードの形
     - 5 章
   * - ``style``
     - G、C、N、E
     - なし
     - 塗りつぶし、角の丸め、線の種類など
     - 5 章
   * - ``color``
     - C、N、E
     - ``black``
     - 枠線、線の色
     - 5 章
   * - ``fillcolor``
     - C、N
     - ノードは ``lightgrey``、クラスターは ``black``
     - 塗りつぶしの色（``style=filled`` のとき）
     - 5 章
   * - ``fontcolor``
     - G、C、N、E
     - ``black``
     - 文字の色
     - 5 章
   * - ``bgcolor``
     - G、C
     - なし
     - 背景色
     - 5 章
   * - ``fontname``
     - G、C、N、E
     - ``Times-Roman``
     - フォント名
     - 5 章
   * - ``fontsize``
     - G、C、N、E
     - 14
     - 文字の大きさ（ポイント）
     - 5 章
   * - ``penwidth``
     - C、N、E
     - 1
     - 線の太さ（ポイント）
     - 5 章
   * - ``width``、``height``
     - N
     - 0.75、0.5
     - ノードの最小の幅と高さ（インチ）
     - 5 章
   * - ``fixedsize``
     - N
     - ``false``
     - ``true`` でノードの大きさを ``width`` と ``height`` に固定する
     - 5 章
   * - ``arrowhead``、``arrowtail``
     - E
     - ``normal``
     - 終点側、始点側の矢印の形
     - 5 章
   * - ``dir``
     - E
     - 有向グラフは ``forward``、無向グラフは ``none``
     - 矢印を付ける側
     - 5 章
   * - ``rankdir``
     - G
     - ``TB``
     - 段を並べる方向（dot）
     - 7 章
   * - ``rank``
     - S
     - なし
     - サブグラフのノードの段の揃え方（``same``、``min``、``max``、``source``、``sink``）（dot）
     - 7 章
   * - ``nodesep``
     - G
     - 0.25
     - 同じ段の中のノードの間隔（インチ）
     - 7 章
   * - ``ranksep``
     - G
     - 0.5
     - 段と段の間隔（インチ）
     - 7 章
   * - ``weight``
     - E
     - 1
     - エッジを短くまっすぐに描く重要度
     - 7 章
   * - ``constraint``
     - E
     - ``true``
     - ``false`` でエッジを段の決定に使わない（dot）
     - 7 章
   * - ``splines``
     - G
     - ``spline``
     - エッジの描き方
     - 7 章
   * - ``ordering``
     - G、N
     - なし
     - ``out`` でエッジの終点を書いた順に並べる（dot）
     - 7 章
   * - ``compound``
     - G
     - ``false``
     - ``true`` で ``lhead`` と ``ltail`` を使えるようにする（dot）
     - 8 章
   * - ``lhead``、``ltail``
     - E
     - なし
     - エッジの終点側、始点側を切るクラスター（dot）
     - 8 章
   * - ``layout``
     - G
     - なし
     - 使用するレイアウトエンジン
     - 9 章
   * - ``root``
     - G、N
     - なし
     - 中心に置くノード（twopi、circo）
     - 9 章
   * - ``overlap``
     - G
     - ``true``
     - ``false`` でノードの重なりを取り除く（neato、fdp、sfdp など）
     - 9 章
   * - ``concentrate``
     - G
     - ``false``
     - ``true`` で並行するエッジをまとめる（dot）
     - 13 章
