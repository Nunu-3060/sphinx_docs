フラクタル
==========

再帰による図形生成
------------------

**L-system**\ （Lindenmayer system）は、文字列の書き換え規則を繰り返し適用して得られる文字列を、タートルグラフィックスとして解釈することで図形を描く手法である。もともとは植物の成長パターンをモデル化するために考案されたが、コッホ曲線のような古典的フラクタル図形も同じ枠組みで表現できる。

手順は次の通り。

1. 開始となる文字列（axiom）を決める。
2. 各文字を、書き換え規則（production rule）に従って別の文字列に置き換える。これを全文字に対して同時に行い、1 回分の書き換えとする。
3. 書き換えを指定回数繰り返し、最終的な文字列を得る。
4. できあがった文字列を先頭から 1 文字ずつ読み、タートルグラフィックス（現在位置と向きを持ったペンを動かす描画方式）として解釈する。

タートルグラフィックスの解釈規則は自由に決められるが、本実装では次の記号を使う一般的な流儀に従う。

- ``F``: 現在の向きに一定距離だけ前進しながら線を引く
- ``+`` / ``-``: 向きを一定角度だけ左/右に回転する
- ``[`` / ``]``: 現在の位置と向きをスタックに退避/復帰する。分岐を表現するときに使い、``]`` で退避しておいた分岐の付け根に戻ってから続きを描く
- それ以外の文字（``X`` など）: 描画には影響しない。書き換え規則を複雑にするためだけに使うダミー記号

``F`` を前進、``X`` をダミーとして使う植物風の規則 ``X -> F+[[X]-X]-F[-FX]+X``, ``F -> FF`` を角度 25 度で適用すると、反復のたびに枝分かれが増えていく樹木状の構造が得られる。

.. literalinclude:: ../examples/l_system.py
   :linenos:
   :language: python
   :pyobject: generate
   :caption: examples/l_system.py の generate 関数

.. literalinclude:: ../examples/l_system.py
   :linenos:
   :language: python
   :pyobject: draw_l_system
   :caption: examples/l_system.py の draw_l_system 関数

.. image:: _static/gallery/l_system_tree.png
   :alt: L-system による樹木状の分岐フラクタル
   :width: 400px

同じ ``generate`` / ``draw_l_system`` の組み合わせで、axiom と規則を変えるだけでまったく違う図形になる。正三角形を初期形 ``F--F--F`` とし、各辺を ``F -> F+F--F+F``\ （角度 60 度）で置き換えると、おなじみのコッホ雪片になる。

.. code-block:: python
   :linenos:

   from l_system import draw_l_system, generate

   koch_str = generate("F--F--F", {"F": "F+F--F+F"}, iterations=4)
   koch_image = draw_l_system(
       koch_str,
       angle_deg=60.0,
       step=6.0,
       start_pos=(60.0, 450.0),
       start_angle_deg=0.0,
       image_size=(600, 620),
   )

.. image:: _static/gallery/koch_snowflake.png
   :alt: L-system の規則から生成したコッホ雪片
   :width: 400px

反復回数（``iterations``）を増やすほど、樹木は枝の階層が深くなり、コッホ雪片は輪郭のギザギザがより細かくなる。文字列の長さは反復ごとにおおよそ 4 倍前後に増えるため（コッホ雪片の規則 ``F -> F+F--F+F`` では文字数がちょうど 4 倍、樹木の規則でも反復を重ねるほど 4 倍に近づく）、反復回数を上げすぎると描画に時間がかかる点には注意する。

L-system でペンローズタイルを描く
-----------------------------------

:doc:`tiling`\ では、ペンローズタイルを Robinson 三角形の細分割によって構成したが、実は L-system でも同じ模様を描ける。ただし、ここまでの ``F`` を前進記号として使う流儀とは少し違う書き方をする。

.. code-block:: text
   :linenos:

   axiom: [N]++[N]++[N]++[N]++[N]
   M -> OA++PA----NA[-OA----MA]++
   N -> +OA--PA[---MA--NA]+
   O -> -MA++NA[+++OA++PA]-
   P -> --OA++++MA[+PA++++NA]--NA
   A -> (空文字列)
   角度: 36度

専用の終端記号 ``F`` を用意する代わりに、非終端記号 ``M`` / ``N`` / ``O`` / ``P`` 自体を「前進しながら線を引く」合図として使う。``A`` は使い切りの前進命令で、次の世代では空文字列に置き換わって消えるため、古い世代の線分が新しい世代に残ってしまうことがない。角度 36 度は、公理の ``++``\ （72 度の回転）5 個ぶんで一周する、5 回対称の構成に対応する。

この規則は ``generate`` をそのまま使って展開できる（``A`` の置き換え先が空文字列というだけで、特別な処理は必要ない）。描画側だけ、前進の合図とする文字集合を、先ほど示した ``draw_l_system`` の ``draw_chars`` 引数で切り替える。

.. image:: _static/gallery/penrose_lsystem.png
   :alt: L-system の文字列書き換えから生成したペンローズタイル。細分割による実装と同じ模様になる
   :width: 600px

:doc:`tiling`\ の三角形細分割による実装が「1 枚の三角形を 2〜3 枚に分割する」という幾何学的な操作を直接プログラムしていたのに対し、こちらは文字列の書き換えという、コッホ雪片や樹木と全く同じ枠組みでペンローズタイルを表現している。同じ図形でも複数のアルゴリズムで到達できるという、フラクタルらしい対応関係の一例と言える。

マンデルブロ集合・ジュリア集合
--------------------------------

マンデルブロ集合・ジュリア集合は、複素数平面上での単純な漸化式を反復するだけで無限に複雑な境界を持つ図形が現れる、フラクタルの代表例である。どちらも同じ漸化式を使う。

.. math::

   z_{n+1} = z_n^2 + c

この式を初期値 :math:`z_0` から反復したとき、:math:`|z_n|` が発散せずに有界にとどまるか、それとも無限大に発散するかで、平面上の各点を 2 種類に分類できる。実用上は「何回反復した時点で :math:`|z_n| > 2` を超えたか」という\ **脱出時間**\ （escape time）を数え、有界（発散しなかった）点は集合の内部として、発散した点は脱出時間の大小をカラーマップの濃淡や色相に対応させて描く。（:math:`|z_n|` が一度でも 2 を超えると、その後は必ず無限大に発散することが示せるため、2 が閾値として使われる。）

マンデルブロ集合とジュリア集合の違いは、この漸化式のどちらを画素座標に対応させるかだけである。

- **マンデルブロ集合**: :math:`z_0 = 0` に固定し、複素平面上の画素座標を :math:`c` として反復する。
- **ジュリア集合**: :math:`c` を 1 つの定数に固定し、複素平面上の画素座標を :math:`z_0` として反復する。

実装上のポイントは、画素ごとに Python のループを回すのではなく、「まだ発散していない画素」を表すブールマスクを使い、NumPy 配列全体に対する演算として反復することである。反復回数（``max_iter``）分だけ Python のループを回す必要はあるが、その内側は画素配列全体へのベクトル演算になっており、画像の解像度が上がってもループ本体の実行回数は増えない。

.. literalinclude:: ../examples/mandelbrot.py
   :linenos:
   :language: python
   :pyobject: _escape_time
   :caption: examples/mandelbrot.py の _escape_time 関数

.. literalinclude:: ../examples/mandelbrot.py
   :linenos:
   :language: python
   :pyobject: mandelbrot_escape
   :caption: examples/mandelbrot.py の mandelbrot_escape 関数

脱出時間の配列は、そのままではグレースケール画像にしかならないので、matplotlib のカラーマップで着色して見やすくする。反復回数の分布は外周ほど密になるため、平方根を取ってから正規化すると階調のメリハリが出やすい。

.. literalinclude:: ../examples/mandelbrot.py
   :linenos:
   :language: python
   :pyobject: render_image
   :caption: examples/mandelbrot.py の render_image 関数

.. image:: _static/gallery/mandelbrot.png
   :alt: 脱出時間アルゴリズムで描画したマンデルブロ集合
   :width: 400px

ジュリア集合は、``c`` を固定した上で ``z0`` 側を画素座標にして同じ ``_escape_time`` を呼ぶだけで得られる。``c`` の値によって形が大きく変わるのが特徴で、境界付近の値（例えば ``c = -0.7 + 0.27015j``）を選ぶと、渦を巻いたような複雑な模様になる。

.. literalinclude:: ../examples/mandelbrot.py
   :linenos:
   :language: python
   :pyobject: julia_escape
   :caption: examples/mandelbrot.py の julia_escape 関数

.. image:: _static/gallery/julia.png
   :alt: c = -0.7 + 0.27015j に対するジュリア集合
   :width: 400px

マンデルブロ集合上のある点 :math:`c` が集合の境界に近いほど、その :math:`c` を使ったジュリア集合は複雑な形状になる傾向がある。マンデルブロ集合を「どのジュリア集合が興味深い形になるかを示す地図」として眺めることもできる。

反復関数系（IFS）とカオスゲーム
--------------------------------

L-system が文字列の書き換え、マンデルブロ/ジュリア集合が複素数の反復だったのに対し、**反復関数系**\ （IFS: Iterated Function System）は、平面上の点にアフィン変換（拡大縮小・回転・平行移動の組み合わせ）を繰り返し適用することでフラクタルを生み出す、第 3 の手法である。

具体的な手続きは\ **カオスゲーム**\ と呼ばれ、次のように進める。

1. あらかじめ複数のアフィン変換と、それぞれを選ぶ確率を用意する。
2. 適当な点から出発し、毎ステップ、用意した変換の中から確率に従って 1 つをランダムに選び、現在の点に適用する。
3. 最初の数ステップ（原点付近をさまよう過渡的な部分）を捨て、それ以降の点を全て描画する。

驚くべきことに、変換とその確率さえ正しく選べば、点がどのような順序で変換を選んでも、十分な数の点を打てば同じ図形（アトラクター）が浮かび上がってくる。1 本の軌跡は「直前の点」に依存する逐次処理だが、独立した軌跡を多数同時に走らせれば、ステップごとの更新は NumPy でベクトル化できる。

.. literalinclude:: ../examples/ifs.py
   :linenos:
   :language: python
   :pyobject: chaos_game
   :caption: examples/ifs.py の chaos_game 関数

有名な例が\ **バーンズリーのシダ**\ で、4 つのアフィン変換（茎、小葉、左右の葉）を、偏った確率（茎はごくまれにしか選ばれない）で適用すると、本物のシダによく似た葉序が現れる。

.. literalinclude:: ../examples/ifs.py
   :linenos:
   :language: python
   :pyobject: barnsley_fern_ifs
   :caption: examples/ifs.py の barnsley_fern_ifs 関数

.. image:: _static/gallery/ifs_fern.png
   :alt: バーンズリーのシダ（カオスゲームによる IFS フラクタル）
   :width: 300px

もう 1 つの定番が\ **シェルピンスキーの三角形**\ である。正三角形の 3 頂点それぞれに対して「現在の点とその頂点の中点に移動する」という変換を用意し、等確率で選ぶだけで、無限に自己相似な三角形の抜け模様が現れる。

.. literalinclude:: ../examples/ifs.py
   :linenos:
   :language: python
   :pyobject: sierpinski_triangle_ifs
   :caption: examples/ifs.py の sierpinski_triangle_ifs 関数

.. image:: _static/gallery/ifs_sierpinski.png
   :alt: シェルピンスキーの三角形（カオスゲームによる IFS フラクタル）
   :width: 350px

打った点は密度にかなりの偏りがあるため、そのまま 2 次元ヒストグラムにすると濃い部分だけが目立ってしまう。対数を取ってから正規化することで、点数の少ない領域（シダで言えば葉の先端など）も見えるようにしている。

.. literalinclude:: ../examples/ifs.py
   :linenos:
   :language: python
   :pyobject: render_density
   :caption: examples/ifs.py の render_density 関数

L-system が「規則を厳密に適用した結果としての 1 つの図形」を作るのに対し、IFS のカオスゲームは点を打つたびに乱数が絡む確率的な手法である点が対照的である。ただしどちらも、ごく単純な規則の反復から複雑な自己相似図形が生まれるという、フラクタルに共通する性質を体現している。

ストレンジアトラクター
------------------------

IFS のカオスゲームは「複数の変換をランダムに選んで反復する」手法だったが、ここではさらに単純に、**ただ 1 つの非線形な写像を、ランダム選択なしにひたすら反復する**\ ことで複雑な図形を得る方法を扱う。それにもかかわらず、初期値のごくわずかな違いが反復のたびに指数的に拡大していく性質（**初期値鋭敏性**、いわゆるカオス）を持つ系では、軌跡がどこにも収束せず無限に複雑な模様を描き続ける。この極限の模様を\ **ストレンジアトラクター**\ と呼ぶ。

この現象自体は、1963 年に気象学者 Edward Lorenz が対流モデルを単純化した 3 本の常微分方程式（**ローレンツ方程式**）を数値計算した際、初期値のごくわずかな丸め誤差が計算結果を全く違う天気予報に導いてしまうことを発見した、いわゆる「バタフライ効果」として広く知られている。一方「ストレンジアトラクター」という言葉自体は、それから 8 年後の 1971 年に数理物理学者 David Ruelle と Floris Takens が乱流の発生を説明する論文の中で提唱したもので、Lorenz が見出した軌跡の形（ローレンツアトラクター）は、後にこの言葉が指す代表例の 1 つとして位置づけられることになった。ローレンツアトラクターは 3 次元の連続時間力学系であり、本資料のような 2 次元の静止画中心の作例とは相性が良くないため実装は割愛するが、「決定論的な式なのに、初期値のわずかな違いで予測不能なほど軌道が発散する」というカオスの本質は、これから扱う 2 次元の離散写像でも共通している。

2 次元平面上の点 :math:`(x, y)` を、非線形な三角関数を含む式で次の点に写す離散写像であれば、同様の性質を持つものが数多く知られている。実装上は IFS と同様、多数の点をわずかにばらけた初期位置から出発させて並行に反復し、密度を可視化する。レンダリングには、先ほどの IFS の節で使った ``render_density`` をそのまま使い回せる。

.. literalinclude:: ../examples/attractors.py
   :linenos:
   :language: python
   :pyobject: clifford_attractor
   :caption: examples/attractors.py の clifford_attractor 関数

.. image:: _static/gallery/attractor_clifford.png
   :alt: Clifford attractor の密度可視化。羽のように流れる有機的な模様
   :width: 350px

**De Jong attractor** も同様の形の写像で、パラメータが変わるだけで全く異なる印象の模様になる。

.. literalinclude:: ../examples/attractors.py
   :linenos:
   :language: python
   :pyobject: de_jong_attractor
   :caption: examples/attractors.py の de_jong_attractor 関数

.. image:: _static/gallery/attractor_de_jong.png
   :alt: De Jong attractor の密度可視化。ハート型に流れる有機的な模様
   :width: 350px

**Gumowski-Mira map** は、次の補助関数 :math:`g(x)` を介した、やや込み入った写像である。パラメータ次第で、花びらや渦が幾重にも重なったような、装飾的な模様が現れる。

.. math::

   g(x) = \mu x + \frac{2(1-\mu)x^2}{1+x^2}

.. literalinclude:: ../examples/attractors.py
   :linenos:
   :language: python
   :pyobject: gumowski_mira_attractor
   :caption: examples/attractors.py の gumowski_mira_attractor 関数

.. image:: _static/gallery/attractor_gumowski_mira.png
   :alt: Gumowski-Mira map の密度可視化。花びら状に広がる装飾的な模様
   :width: 350px

同じ「点を反復して打つ」手法でも、IFS のカオスゲームは角ばった自己相似図形に、ストレンジアトラクターはなめらかに流れる有機的な模様になる。前者は複数の縮小写像をランダムに選ぶことで図形に収束させ、後者はただ 1 つの写像を反復するだけで、初期値鋭敏性そのものが軌跡を面状に広げる。パラメータ（式中の :math:`a, b, c, d` など）を少し変えるだけで模様が大きく変わるため、値を振ってみるだけでも新しい発見がある。
