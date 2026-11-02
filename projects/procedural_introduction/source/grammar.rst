第 8 章　文法と成長による形状
============================================================

植物の枝分かれや建物の窓の並びは、ノイズのような「どこを見ても同じ性質の乱れ」では作れない。そこには、「枝の先がさらに枝分かれする」「各階を同じ幅の柱間に分け、各柱間に窓を 1 つ置く」といった\ **構造**\ がある。本章では、このような構造を、記号や形を書き換える規則（\ **文法**\ ）として書き、規則を繰り返し適用して形を作る方法を扱う。第 1 章の分類では文法型に当たる。あわせて、樹木を「空いた空間に向かって成長する」過程のシミュレーションで作る空間植民アルゴリズムも扱う。

本章の図は、次のスクリプトで作っている。

* :download:`lsystem.py <../examples/python/lsystem.py>`: L-system とタートルグラフィックス（2 次元の植物、3 次元の木）
* :download:`space_colonization.py <../examples/python/space_colonization.py>`: 空間植民アルゴリズムによる樹木
* :download:`shape_grammar.py <../examples/python/shape_grammar.py>`: 分割文法による建物の外壁

L-system
------------------------------------------------------------

書き換え規則
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**L-system**\ （Lindenmayer system）は、生物学者の Lindenmayer が 1968 年に、藻類の細胞が分裂して並んでいく様子を記述するために考えた文字列の書き換えの仕組みである。最初の文字列（\ **公理**\ 、axiom）と、文字ごとの書き換え規則を決め、各世代で、文字列のすべての文字を\ **同時に**\ 規則の右辺に置き換える。

Lindenmayer の藻類の例は、2 文字 A、B と、次の 2 つの規則から成る。

.. math::

   \mathrm{A} \rightarrow \mathrm{AB}, \qquad \mathrm{B} \rightarrow \mathrm{A}

公理を A とすると、A、AB、ABA、ABAAB、ABAABABA と育ち、文字数はフィボナッチ数になる。各文字が次の世代でどの文字に置き換わったかをたどると、:numref:`fig-grammar-algae` のような木になる。

.. _fig-grammar-algae:

.. graphviz::
   :caption: 藻類の L-system の書き換え（上から 0〜4 世代）
   :align: center

   digraph G {
       node [shape=circle, style="filled", fixedsize=true, width=0.35, fontsize=11];
       edge [color="#777777", arrowsize=0.5];
       node [fillcolor="#eef3fb", color="#4c72b0"];
       a0 [label="A"];
       a1 [label="A"]; a2 [label="A"]; a3 [label="A"]; a5 [label="A"]; a6 [label="A"];
       a8 [label="A"]; a10 [label="A"]; a11 [label="A"]; a13 [label="A"]; a15 [label="A"]; a16 [label="A"];
       node [fillcolor="#fdf0e6", color="#dd8452"];
       b1 [label="B"]; b2 [label="B"]; b3 [label="B"]; b4 [label="B"]; b5 [label="B"]; b6 [label="B"]; b7 [label="B"];
       a0 -> {a1 b1};
       a1 -> {a2 b2}; b1 -> a3;
       a2 -> {a5 b3}; b2 -> a6; a3 -> {a8 b4};
       a5 -> {a10 b5}; b3 -> a11; a6 -> {a13 b6}; a8 -> {a15 b7}; b4 -> a16;
   }

規則を持たない文字はそのまま残す。この書き換えは、Python では次のように書ける。後で使う確率的な規則にも対応させてある。

.. literalinclude:: ../examples/python/lsystem.py
   :language: python
   :pyobject: rewrite
   :lineno-match:
   :caption: examples/python/lsystem.py（rewrite）

すべての文字を同時に置き換えるのが、普通の文法（1 か所ずつ置き換える）との違いである。植物のすべての枝先が同時に伸びる様子に対応する。

タートルグラフィックスとブラケット
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

文字列を形にするには、各文字を描画の命令とみなして読む。ペンを持った亀を画面に置き、命令に従って歩かせる\ **タートルグラフィックス**\ （プログラミング言語 Logo に由来する）を使う。亀は位置と向きを持ち、次の命令を解釈する。

.. list-table:: 2 次元のタートルの命令
   :header-rows: 1
   :widths: 25 75

   * - 文字
     - 動作
   * - ``F``
     - 1 歩進み、線を引く
   * - ``f``
     - 1 歩進む（線を引かない）
   * - ``+``・``-``
     - 角度 :math:`\delta` だけ左・右に向きを変える
   * - ``[``
     - 今の状態（位置と向き）をスタックに積む
   * - ``]``
     - スタックから状態を取り出し、その位置と向きに戻る
   * - そのほか（``X`` など）
     - 何もしない。書き換えの途中の状態を表すためだけに使う

``[`` と ``]``\ （\ **ブラケット**\ ）が枝分かれを表す。``[`` で分岐点を覚え、枝を描き終えたら ``]`` で分岐点に戻って、幹の続きを描く。``[`` の入れ子の深さは、幹から何回枝分かれした先かを表すので、線の太さに使う。

.. literalinclude:: ../examples/python/lsystem.py
   :language: python
   :pyobject: turtle2d
   :lineno-match:
   :caption: examples/python/lsystem.py（turtle2d）

規則 :math:`\mathrm{F} \rightarrow \mathrm{F[+F]F[-F]F}` は、「1 本の線分を、途中で左右に 1 本ずつ枝を出す 3 本の線分に置き換える」ことを意味する。書き換えを繰り返すと、枝の 1 本 1 本が全体と同じ形を持つ、自己相似な植物になる（:numref:`fig-grammar-steps`）。

.. _fig-grammar-steps:

.. figure:: _generated/lsystem/lsystem_steps.png
   :alt: 1 本の線分から、世代を重ねるごとに枝分かれが細かくなる植物

   :math:`\mathrm{F} \rightarrow \mathrm{F[+F]F[-F]F}`、:math:`\delta = 25.7°` の 0〜4 世代（大きさをそろえて表示）

規則と角度を変えると、まったく違う植物になる。:numref:`fig-grammar-plants` は、Prusinkiewicz と Lindenmayer の本「The Algorithmic Beauty of Plants」（1990 年）の図 1.24 にある 6 つの例である。

.. literalinclude:: ../examples/python/lsystem.py
   :language: python
   :start-at: PLANTS = [
   :end-before: def draw_segments
   :lineno-match:
   :caption: examples/python/lsystem.py（PLANTS）

.. _fig-grammar-plants:

.. figure:: _generated/lsystem/lsystem_plants.png
   :alt: 規則と角度の異なる 6 種類の 2 次元の植物

   規則・角度・世代数の異なる植物

(d)〜(f) は、描画しない文字 X を「まだ育っていない芽」として使い、:math:`\mathrm{F} \rightarrow \mathrm{FF}` で「育った枝は世代ごとに 2 倍に伸びる」ことを表している。芽と枝を分けると、枝分かれの仕方と伸び方を別々に制御できる。L-system で制御できる主なパラメーターは次のとおりである。

* **規則**: 枝分かれの構造（何本に、どの順に分かれるか）。形の性格を決める。
* **角度** :math:`\delta`: 枝の開き方。小さいと細長く、大きいと横に広がる。
* **世代数**: 細かさ。文字数は世代ごとに数倍になるので、描画の負荷もそれに応じて増える。
* **線の長さと太さの減り方**: 先の枝ほど短く細くすると、より自然になる。

確率的 L-system
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

決定的な L-system は、同じ規則からは常に同じ形を作る。たくさんの植物を並べると、すべてが同じ形のコピーに見える。そこで、1 つの文字に複数の右辺を用意し、書き換えのたびに確率で選ぶ（\ **確率的 L-system**\ ）。同じ本にある次の例では、枝を左右両方に出すか、片方だけに出すかを、ほぼ等しい確率で選ぶ。

.. literalinclude:: ../examples/python/lsystem.py
   :language: python
   :start-at: STOCHASTIC_RULES
   :end-at: STOCHASTIC_RULES
   :lineno-match:
   :caption: examples/python/lsystem.py（STOCHASTIC_RULES）

.. _fig-grammar-stochastic:

.. figure:: _generated/lsystem/lsystem_stochastic.png
   :alt: 同じ確率的な規則から作った、大きさと枝ぶりの異なる 6 本の植物

   確率的 L-system でシードだけを変えた植物（5 世代、:math:`\delta = 25.7°`）

:numref:`fig-grammar-stochastic` の 6 本は、規則は同じで、シードだけが違う。枝ぶりは個体ごとに異なるが、「同じ種の植物」に見える。確率の値を変えれば、枝の多い個体が出やすい種、少ない種のように、種の性格を調整できる。確率のほかに、回転角や枝の長さへ少し乱数を加える方法もよく使われる。

3 次元の木
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

3 次元の亀は、位置のほかに、前 :math:`\boldsymbol{H}`、左 :math:`\boldsymbol{L}`、上 :math:`\boldsymbol{U}` の 3 本の単位ベクトルで姿勢を持つ。第 6 章の標構と同じものである。回転の命令は、これらのうちの 1 本を軸にして、残りの 2 本を回す。

.. list-table:: 3 次元のタートルの回転の命令
   :header-rows: 1
   :widths: 15 25 60

   * - 文字
     - 回転の軸
     - 動作
   * - ``+``・``-``
     - :math:`\boldsymbol{U}`
     - 左・右を向く
   * - ``&``・``^``
     - :math:`\boldsymbol{L}`
     - 下・上を向く（枝を幹から開く）
   * - ``/``・``\``
     - :math:`\boldsymbol{H}`
     - 進む向きの周りにひねる（枝を出す方向を変える）

本書では、これに ``!``\ （以降の枝の長さと太さを縮める）と ``A``\ （芽。枝先の位置を記録し、葉を付ける）を加えた。任意の軸の周りの回転は、ロドリゲスの回転公式（付録 A）で計算する。

.. literalinclude:: ../examples/python/lsystem.py
   :language: python
   :pyobject: turtle3d
   :lineno-match:
   :caption: examples/python/lsystem.py（turtle3d）

木の規則は、芽 A を「枝を縮め、120 度ずつひねりながら、幹から 32 度開いた 3 本の枝を出し、それぞれの先に新しい芽を付ける」に置き換えるものである。

.. literalinclude:: ../examples/python/lsystem.py
   :language: python
   :start-at: TREE_AXIOM
   :end-before: def tree_mesh
   :lineno-match:
   :caption: examples/python/lsystem.py（木の規則）

亀が描いた枝の 1 本 1 本を、第 6 章の円錐台のメッシュにし、芽の位置に葉の代わりの小さな球を置いた（:numref:`fig-grammar-tree3d`）。左は回転角をそのまま使ったもので、3 回対称の整いすぎた形になる。中央と右は、回転角に標準偏差 8 度の乱数を加えたものである。

.. _fig-grammar-tree3d:

.. figure:: _generated/lsystem/lsystem_tree3d.png
   :alt: 円柱の枝と球の葉でできた 3 本の木。左は対称、右の 2 本は少し不規則

   3 次元の L-system で作った木（5 世代、枝 365 本）

枝を 1 本ずつ別の円錐台にしたので、分岐点では枝どうしが重なっているだけで、つながっていない。遠目には問題ないが、近くで見せる場合は、分岐点で枝のメッシュを滑らかにつなぐ処理が要る。ゲームの実行中に、このようなメッシュを Godot の ``SurfaceTool`` で組み立てる方法は、第 15 章で扱う。

空間植民アルゴリズム
------------------------------------------------------------

L-system は、枝分かれの構造を規則として直接書く。一方、実際の木の形は、光を求めて空いている空間へ枝が伸びることで決まる部分が大きい。Runions、Lane、Prusinkiewicz は 2007 年に、この「空間の奪い合い」をまねた\ **空間植民アルゴリズム**\ （space colonization algorithm）を示した。枝の構造を規則で書かず、樹冠の形（枝が伸びてよい範囲）だけを与える。

樹冠の中に、多数の\ **誘引点**\ （枝を引き寄せる点）をばらまく。誘引点は、まだ枝が届いていない空間（光の当たる空間）を表す。木は、根元の節点（枝の途中の点）1 つから始め、次の手順を繰り返す。

1. 各誘引点について、\ **影響距離**\ :math:`d_i` 以内にある最も近い節点を探す。その節点だけが、この誘引点に引かれる。
2. 1 つ以上の誘引点に引かれた節点から、引いている誘引点への単位ベクトルを平均した向きへ、長さ :math:`D` の新しい節点を伸ばす。
3. 新しい節点から\ **消滅距離**\ :math:`d_k` 以内に入った誘引点を取り除く（その空間は枝で占められた）。

誘引点が無くなるか、伸びる節点が無くなったら終わる。最近傍の探索には、SciPy の k-d 木（``cKDTree``）を使う。

.. literalinclude:: ../examples/python/space_colonization.py
   :language: python
   :pyobject: colonize
   :lineno-match:
   :caption: examples/python/space_colonization.py（colonize）

1 つの誘引点に引かれる節点は 1 つだけなので、近い枝どうしが同じ空間を奪い合い、自然に枝の間隔が空く。誘引点が左右から引くと、1 つの節点から複数の枝が伸びて枝分かれが起きる。枝分かれの規則はどこにも書いていない。

.. _fig-grammar-colonization-steps:

.. figure:: _generated/space_colonization/colonization_steps.png
   :alt: 楕円形の樹冠に灰色の点が散らばり、幹から枝が伸びて点が消えていく 4 段階

   空間植民アルゴリズムの成長の途中経過（灰色の点は残っている誘引点）

.. video:: _generated/space_colonization/colonization.mp4
   :width: 360

   成長の様子。枝が届いた所から誘引点が消えていく

最初は、どの誘引点も根元から遠いので、幹をまっすぐ上へ伸ばし、樹冠に届いたところから本来の手順を始める。

枝の太さは、成長が終わった後で、先端から根元に向かって決める。枝分かれの前後で断面積の合計が保たれる（親の太さ :math:`r` と子の太さ :math:`r_k` の間に :math:`r^2 = \sum_k r_k^2` が成り立つ）という経験則がある。これを一般化して :math:`r^\gamma = \sum_k r_k^\gamma` とし、先端の太さと指数 :math:`\gamma` をパラメーターにする。

.. literalinclude:: ../examples/python/space_colonization.py
   :language: python
   :pyobject: branch_radii
   :lineno-match:
   :caption: examples/python/space_colonization.py（branch_radii）

:numref:`fig-grammar-colonization-params` は、樹冠の形とパラメーターを変えた結果である。樹冠の形を変えるだけで、木全体の輪郭がそれに従う。これは、L-system では規則の調整で間接的にしか実現できない制御である。

.. _fig-grammar-colonization-params:

.. figure:: _generated/space_colonization/colonization_params.png
   :alt: 楕円、円錐、2 つに分かれた樹冠の木と、影響距離・消滅距離・誘引点の数を変えた木

   樹冠の形（左 3 つ）とパラメーター（右 3 つ）による違い

.. list-table:: 空間植民アルゴリズムの主なパラメーター
   :header-rows: 1
   :widths: 25 75

   * - パラメーター
     - 効果
   * - 樹冠の形
     - 木全体の輪郭。建物の陰を避けた木や、刈り込んだ生け垣も、形を与えるだけで作れる
   * - 誘引点の数
     - 多いほど枝が細かく密になる。少ないと、枝がまばらで曲がりくねる
   * - 影響距離 :math:`d_i`
     - 大きいと遠くの誘引点にも引かれ、枝がまっすぐ長く伸びる。小さいと近くの空間だけを埋める
   * - 消滅距離 :math:`d_k`
     - 大きいと誘引点が早く消え、枝がまばらになる。小さいと枝が誘引点の近くまで細かく伸びる
   * - 成長の長さ :math:`D`
     - 節点の間隔。小さいほど滑らかだが、計算が増える

同じ手順は 3 次元でもそのまま使える。3 次元の場合は、節点をつないだ折れ線を、第 6 章のスイープで太さを変えながらメッシュにすればよい。また、葉脈のように平面の中で伸びる構造も、同じ考え方で作れる。

形状文法による建物
------------------------------------------------------------

分割文法
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

L-system は文字列を書き換えたが、図形そのものを書き換える文法も考えられる。Stiny と Gips が 1971 年に示した\ **形状文法**\ （shape grammar）がその始まりである。建物の生成では、長方形や箱を、より小さな長方形や箱に分ける規則に限った\ **分割文法**\ （split grammar）がよく使われる。Wonka らが 2003 年に「Instant Architecture」で示し、Müller らが 2006 年に箱形の建物全体を扱う CGA shape に発展させた。CGA shape は、都市を生成する商用ソフトウェア CityEngine で使われている。

分割文法の規則は、「名前の付いた長方形（記号）を、決まった向きと大きさで分け、分けた部分にそれぞれ新しい記号を付ける」ものである。本章では、建物の外壁を、:numref:`fig-grammar-facade-rules` の規則で分ける。大文字で始まる記号はさらに分割し、小文字の記号（壁・窓・扉など）は終端（これ以上分けない形）とする。

.. _fig-grammar-facade-rules:

.. graphviz::
   :caption: 外壁の分割文法の規則（矢印は「分けた結果に含まれる」を表す）
   :align: center

   digraph G {
       rankdir=TB;
       node [shape=box, style="rounded,filled", fillcolor="#eef3fb", color="#4c72b0", fontsize=11];
       edge [color="#777777"];
       Facade [label="Facade\n縦に 3 分割"];
       Ground [label="Ground（地上階）\n横に柱間を繰り返す"];
       Floors [label="Floors\n縦に階を繰り返す"];
       Floor [label="Floor（階）\n横に柱間を繰り返す"];
       Tile [label="Tile（柱間）\n横に 3 分割"];
       WindowColumn [label="WindowColumn\n縦に 3 分割"];
       DoorTile [label="DoorTile（中央）"];
       ShopTile [label="ShopTile"];
       node [shape=ellipse, fillcolor="#fdf0e6", color="#dd8452"];
       wall; window; door; shop; cornice [label="cornice（軒）"];
       Facade -> {Ground Floors cornice};
       Floors -> Floor;
       Floor -> {Tile wall};
       Tile -> {WindowColumn wall};
       WindowColumn -> {window wall};
       Ground -> {DoorTile ShopTile wall};
       DoorTile -> {door wall};
       ShopTile -> {shop wall};
   }

分割には 2 種類の操作を使う。``split`` は、指定した大きさで分ける。大きさは m 単位の固定値か、残りを等分する可変の値（``"~"``）で指定する。固定値と可変値を組み合わせると、「端の壁は 0.6 m、残りに窓を並べる」のように、外壁の幅が変わっても崩れない規則になる。

.. literalinclude:: ../examples/python/shape_grammar.py
   :language: python
   :pyobject: split
   :lineno-match:
   :caption: examples/python/shape_grammar.py（split）

``repeat`` は、指定した大きさに近い等しい大きさで、できるだけ多く並べる。幅 14 m の壁に幅 3 m の柱間を並べると 5 個（各 2.8 m）、幅 10 m なら 3 個（各 3.3 m）になる。数を固定せず大きさを目安にするので、どんな幅の外壁にも柱間が隙間なく並ぶ。

.. literalinclude:: ../examples/python/shape_grammar.py
   :language: python
   :pyobject: repeat
   :lineno-match:
   :caption: examples/python/shape_grammar.py（repeat）

規則は、記号の名前から、領域を分けて子の記号の列を返す関数への対応表として書く。各規則が短く、分割の大きさを建物ごとのパラメーター（``Style``）から取ることに注目してほしい。

.. literalinclude:: ../examples/python/shape_grammar.py
   :language: python
   :start-at: class FacadeGrammar
   :end-before: def derive
   :lineno-match:
   :caption: examples/python/shape_grammar.py（FacadeGrammar の規則）

記号を、規則が無くなるまで再帰的に分割すると、終端の長方形の列が得られる。途中の段で止めれば、分割の過程を見ることができる（:numref:`fig-grammar-facade-derivation`）。

.. literalinclude:: ../examples/python/shape_grammar.py
   :language: python
   :pyobject: FacadeGrammar.derive
   :lineno-match:
   :caption: examples/python/shape_grammar.py（FacadeGrammar.derive）

.. _fig-grammar-facade-derivation:

.. figure:: _generated/shape_grammar/facade_derivation.png
   :alt: 外壁が、地上階と上の階に、さらに各階と柱間に分かれ、最後に窓と扉が描かれる 5 段階

   外壁の分割の過程。白い部分は終端（壁・軒）

バリエーション
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

規則は同じまま、階数・階高・柱間の幅・窓の幅の割合・窓の種類・色を、建物ごとにシードから決める。値は、それぞれ建物として不自然にならない範囲の中で選ぶ。

.. literalinclude:: ../examples/python/shape_grammar.py
   :language: python
   :pyobject: random_style
   :lineno-match:
   :caption: examples/python/shape_grammar.py（random_style）

窓の種類（アーチ・鎧戸・バルコニー）は、終端の ``window`` を描くときの飾りとして表した。規則を増やして、窓をさらに枠・ガラス・窓台に分割してもよい。:numref:`fig-grammar-facades` は、シード 0〜5 から作った外壁である。

.. _fig-grammar-facades:

.. figure:: _generated/shape_grammar/facades.png
   :alt: 色・階数・窓の形の異なる 6 棟の建物の外壁が並んだ街並み

   シードだけを変えて作った外壁

どの建物も、1 階の中央に入口があり、上の階の窓が柱間ごとにそろっている。乱数で決めたのは数値だけで、構造は規則が保証している。これが文法型の生成の利点で、意図した構造を壊さずに多様性を出せる。逆に、規則に無い構造（中央が吹き抜けの建物、斜めの壁）は作れない。そのような建物は、規則を追加して表す。

立体の建物
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

外壁の分割は、そのまま立体の建物に使える。建物の敷地を箱に押し出し（第 6 章）、箱の 4 つの側面にそれぞれ外壁の規則を適用して、終端の長方形を側面の上の四角形として置く。側面の左下の角を :math:`\boldsymbol{c}`、外から見て右へ向かう単位ベクトルを :math:`\boldsymbol{u}` とすると、外壁の上の点 :math:`(x, y)` は :math:`\boldsymbol{c} + x \boldsymbol{u} + y (0, 0, 1)` になる。

.. literalinclude:: ../examples/python/shape_grammar.py
   :language: python
   :pyobject: building_quads
   :lineno-match:
   :caption: examples/python/shape_grammar.py（building_quads）

.. _fig-grammar-buildings:

.. figure:: _generated/shape_grammar/buildings3d.png
   :alt: 窓と扉の付いた、高さと色の異なる 5 棟の箱形の建物

   外壁の分割を箱の 4 面に貼った建物（窓の飾りは省略）

:numref:`fig-grammar-buildings` では、各建物の高さと幅が異なっていても、窓が各面の幅に合わせて並んでいる。CGA shape では、同じ考え方で、箱を屋根・階・外壁に分ける規則も文法に含めて、建物全体を 1 つの文法で記述する。

まとめ
------------------------------------------------------------

* L-system は、文字列のすべての文字を同時に書き換える。書き換えの規則が、枝分かれの構造を表す。
* タートルグラフィックスで文字列を描画命令として読む。ブラケット ``[`` ``]`` が枝分かれを表し、3 次元では前・左・上の 3 本のベクトルで姿勢を持つ。
* 規則・角度・世代数で形を制御する。確率的な規則や角度の乱数で、同じ種の異なる個体を作れる。
* 空間植民アルゴリズムは、樹冠に置いた誘引点に向かって枝を伸ばし、空間を奪い合わせて木を作る。樹冠の形で輪郭を直接制御でき、枝の太さは先端から根元へ断面積の規則で決める。
* 分割文法は、長方形を固定・可変の大きさで分ける規則と、大きさを目安に繰り返す規則で、外壁を階・柱間・窓に分ける。
* 構造は規則が、多様性はシードから決めるパラメーターが受け持つ。規則に無い構造は作れないので、必要に応じて規則を加える。
