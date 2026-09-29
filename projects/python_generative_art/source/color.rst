色彩設計
========

ジェネラティブアートでは、形を生み出すアルゴリズムに目が向きがちだが、作品の印象は配色によって大きく変わる。単純な模様でも配色が整っていれば見栄えがし、逆に凝った模様でも、配色を考えずに色を決めると雑然とした印象になる。本章では、以降の章で扱うどの技法にも共通して使える、配色の考え方と、パレットを機械的に作る道具をまとめる。

配色理論の基礎
--------------

アルゴリズムで配色を決める場合、RGB よりも HSB（色相・彩度・明度、HSV とも呼ぶ）で色を表現した方が扱いやすい。RGB の 3 成分は「どれだけ近い色か」「反対の色は何か」といった感覚的な関係を素直には表現できない。例えば ``(255, 100, 50)`` に近い色や、その正反対の色を RGB の数値操作だけで求めるのは難しい。一方 HSB では、色相（Hue）を 0-360 度（あるいは 0.0-1.0）の環状の値として扱うため、色相環の上での「角度」の操作がそのまま配色の操作になる。彩度・明度を固定して色相だけを動かせば、鮮やかさのそろった配色を機械的に作れる。ただし、HSB の明度は人が感じる明るさとは一致しない。この点は\ :ref:`oklab`\ で扱う。

色相環さえ意識すれば、古典的な配色パターンは、基準の色相へのオフセット加算として実装できる。

- **類似色（analogous）**: 基準の色相から見て近い範囲（例えば±15 度程度）に収まる色を複数選ぶ。トーンが近く、まとまりのある配色になる。
- **補色（complementary）**: 基準の色相の 180 度反対を選ぶ。もっとも強いコントラストが得られる。
- **スプリットコンプリメンタリー（split-complementary）**: 補色そのものではなく、補色の両隣（:math:`180 \pm \alpha` 度）を選ぶ。補色ほど強くない、やや穏やかな対比になる。
- **トライアド（triadic）**: 色相環を 120 度おきに三等分した 3 色を選ぶ。バランスの取れた鮮やかな配色になる。

いずれも「基準の色相 + オフセットのリスト」という共通の形で表現でき、コード上は 1 つの関数にまとめられる。

トーン（PCCS）による配色
--------------------------

上記の配色パターンは全て「色相を動かし、彩度・明度は固定する」という軸だけを使っている。もう一方の軸として、彩度と明度の組み合わせを固定・変化させる、という考え方がある。日本色彩研究所が定めた **PCCS**\ （Practical Color Co-ordinate System）では、彩度・明度の組み合わせを\ **トーン**\ と呼び、「ビビッド（鮮やかな）」「ペール（淡い）」「ダル（くすんだ）」「ダーク（暗い）」のような色の調子・印象をひとまとまりの概念として扱う。PCCS のトーン図は、彩度を横軸・明度を縦軸にとってトーンを配置したものだが、本資料では扱いやすさを優先し、代表的な 12 トーンを次のような 4 列×3 行のグリッドに簡略化して扱う（配置も数値も大まかな傾向を表す近似であり、厳密な PCCS の定義とは異なる）。

.. list-table::
   :header-rows: 0

   * - vivid（鮮やか）
     - bright（明るい）
     - strong（強い）
     - deep（深い）
   * - light（浅い）
     - soft（柔らかい）
     - dull（くすんだ）
     - dark（暗い）
   * - pale（薄い）
     - light grayish（明るい灰みの）
     - grayish（灰みの）
     - dark grayish（暗い灰みの）

上段ほど彩度が高く、下段ほど彩度が低い（グレーに近づく）。各段の中では、おおむね右の列ほど暗くなる（上段の bright だけは vivid より明るい）。この「トーン」というまとまりを使うと、色相の配色パターンと対になる、次の 2 つの技法が定義できる。

- **トーンオントーン（tone on tone）**: 色相は同じ（または近い）まま、トーンだけを変化させる配色。同系色の濃淡・調子のバリエーションになり、まとまりがありながら単調になりにくい。
- **トーンイントーン（tone in tone）**: 色相はばらばらでも、トーン（彩度・明度の組み合わせ）をそろえる配色。個々の色は違っても「淡い」「くすんだ」といった全体の印象は統一される。

いずれも「色相を固定してトーンを変える」「トーンを固定して色相を変える」という、色相スキームとは軸を入れ替えただけの操作であり、コード上は同じ ``hsv_to_rgb`` の呼び出し方を変えるだけで実装できる。

HSV から RGB への変換
----------------------

配色を HSV で考えたとしても、画像として書き出す最終段階では必ず RGB の数値が必要になる。標準ライブラリの ``colorsys`` に頼らず、この変換を NumPy で自前実装する。

HSV は、色相（Hue）を角度、彩度（Saturation）を中心からの距離、明度（Value）を高さとする円柱状の空間として考えられる。この円柱を RGB の立方体に対応させる際、断面を円ではなく六角形として扱うと（RGB の 3 成分のうち最大値・最小値・中間値がどれかによって 6 つの場合分けができるため）、比較的単純な式で RGB に変換できる。

まず、彩度と明度から\ **クロマ**\ （彩度に応じた RGB 成分の幅、:math:`\max(R,G,B) - \min(R,G,B)` に対応する量）を求める。

.. math::

   C = V \cdot S

色相を 60 度（:math:`H'=H/60°`、あるいは色相を 0.0-1.0 で表しているなら :math:`H' = H \times 6`）ごとの 6 つの区間に分け、区間内での位置から中間値となる成分 :math:`X` を求める。

.. math::

   X = C \bigl(1 - |H' \bmod 2 - 1|\bigr)

あとは :math:`H'` がどの区間に入るかで、RGB のうちどれが最大（:math:`C`）でどれが中間（:math:`X`）でどれが最小（:math:`0`）になるかが決まる。

.. list-table::
   :header-rows: 1

   * - 区間 :math:`H'`
     - :math:`(R_1, G_1, B_1)`
   * - :math:`[0, 1)`
     - :math:`(C, X, 0)`
   * - :math:`[1, 2)`
     - :math:`(X, C, 0)`
   * - :math:`[2, 3)`
     - :math:`(0, C, X)`
   * - :math:`[3, 4)`
     - :math:`(0, X, C)`
   * - :math:`[4, 5)`
     - :math:`(X, 0, C)`
   * - :math:`[5, 6)`
     - :math:`(C, 0, X)`

最後に、最小成分が 0 になっている :math:`(R_1, G_1, B_1)` 全体に :math:`m = V - C` を加えることで、最小成分を :math:`m` へ、最大成分を :math:`C + m = V` へ底上げする。

.. math::

   (R, G, B) = (R_1 + m,\ G_1 + m,\ B_1 + m)

実装では、区間ごとの場合分けを ``if`` 文で書くと配列全体を一度に処理できなくなる。区間番号を NumPy 配列として求めた上で、``np.select`` で 6 つの区間それぞれの候補値から実際の値を選び出すことで、色 1 つでも配列（例えば画像全体の色相配列）でも同じコードで扱えるようにしている。

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: hsv_to_rgb
   :caption: examples/palette.py の hsv_to_rgb 関数

カラーパレットの生成
----------------------

上記の配色パターンを実際にコードで生成し、画像として確認する。先ほどの自前実装の ``hsv_to_rgb`` で HSV→RGB 変換を行い、基準色相とオフセットのリストから、PIL でスウォッチ（色見本）画像を描画する。

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: hue_scheme
   :caption: examples/palette.py の hue_scheme 関数

この ``hue_scheme`` を土台に、代表的な配色パターンをオフセットの違いとして定義できる。

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: analogous_palette
   :caption: examples/palette.py の analogous_palette 関数

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: complementary_palette
   :caption: examples/palette.py の complementary_palette 関数

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: split_complementary_palette
   :caption: examples/palette.py の split_complementary_palette 関数

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: triadic_palette
   :caption: examples/palette.py の triadic_palette 関数

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: render_swatches
   :caption: examples/palette.py の render_swatches 関数

同じ基準色相（0.55、水色寄りの青）から 4 種類の配色パターンを生成し、上から類似色・補色・スプリットコンプリメンタリー・トライアドの順に並べると次のようになる。

.. image:: _static/gallery/hsb_palette.png
   :alt: 同じ基準色相から生成した類似色・補色・スプリットコンプリメンタリー・トライアドの 4 種類の配色パレット（上から順）
   :width: 400px

トーンオントーン・トーンイントーンも、同じ ``hsv_to_rgb`` を使い、彩度・明度の組み合わせ（トーン）をあらかじめ 12 種類定義しておくことで実装できる。

.. literalinclude:: ../examples/palette.py
   :language: python
   :start-at: # PCCS
   :end-at: }
   :caption: examples/palette.py の PCCS_TONES

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: tone_on_tone_palette
   :caption: examples/palette.py の tone_on_tone_palette 関数

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: tone_in_tone_palette
   :caption: examples/palette.py の tone_in_tone_palette 関数

``tone_on_tone_palette`` は基準の色相を固定し、PCCS のトーンを 4 列×3 行のグリッドとして並べたものである（トーンの定義順序がそのまま PCCS のグリッド順になっている）。

.. image:: _static/gallery/tone_on_tone.png
   :alt: 同じ色相で PCCS の 12 トーンを変化させたトーンオントーンの配色（4 列 3 行、左上が vivid、右下が dark grayish）
   :width: 300px

``tone_in_tone_palette`` は逆に、トーンを 1 つ（ここでは "soft"）に固定し、色相環を 6 等分した色を並べたものである。色はばらばらでも、彩度・明度がそろっているため、パレット全体の印象がまとまっている。ただし、HSB の彩度・明度をそろえても、黄系の色は明るく、青系の色は暗く見える。見た目の明るさまでそろえたい場合は、:ref:`oklab`\ で扱う OKLCH を使う。

.. image:: _static/gallery/tone_in_tone.png
   :alt: soft トーンに固定し、6 色相を変化させたトーンイントーンの配色
   :width: 400px

配色パターンは離散的な色の集合だが、2 色の間をなめらかに補間したグラデーションが欲しい場合もある。ここで注意が必要なのは、色相が環状の値だという点である。色相をそのまま線形補間すると、例えば赤 (0.98) から橙 (0.08) へは、本来はすぐ隣り合う色なのに、色相環をほぼ一周する遠回りの補間になってしまう。差分を ``[-0.5, 0.5)`` の範囲に正規化してから補間すれば、常に短い方の弧を通るようにできる。

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: hsb_gradient
   :caption: examples/palette.py の hsb_gradient 関数

赤 (0.98) から橙 (0.08) へのグラデーションを、単純な線形補間（``shortest_path=False``）と短い弧を通る補間（``shortest_path=True``）の両方で生成して比べると、違いは一目瞭然である。

.. image:: _static/gallery/gradient.png
   :alt: 上段は色相を単純に線形補間したグラデーション（色相環を遠回りして虹色に近い経路を通る）、下段は短い弧を通るように補間したグラデーション（赤から橙へ直接つながる）
   :width: 400px

逆に、既存の画像から配色を抽出したい場合もある。手描きで配色を決めるのではなく、写真やこれまで生成した画像から「使われている色」を取り出し、別の作品のパレットとして転用するという使い方である。PIL の ``Image.quantize`` はメディアンカット法によるパレット量子化を実装しており、画像全体を指定した色数に減色できる。減色後のパレットと、量子化画像上での各色の出現画素数を突き合わせれば、使用頻度の高い色から順にパレットとして取り出せる。

.. literalinclude:: ../examples/palette.py
   :language: python
   :pyobject: extract_palette
   :caption: examples/palette.py の extract_palette 関数

例として、:doc:`fractals`\ で生成するジュリア集合の画像 ``julia.png`` から 8 色を抽出すると、次のようなパレットになる。

.. image:: _static/gallery/extracted_palette.png
   :alt: julia.png から Image.quantize で抽出した 8 色のパレット
   :width: 400px

.. _oklab:

知覚的に均等な色空間（OKLab）
--------------------------------

HSB の明度（Value）は、RGB の 3 成分のうち最大のものをそのまま表した値であり、人が感じる明るさとは一致しない。人の目は緑から黄の光に敏感で、青の光には鈍いため、明度が同じでも、黄は明るく、青は暗く見える。HSB で彩度・明度を固定して色相だけを動かすと、鮮やかさはそろっても、色によって明るさが大きくばらつく。

そこで、色どうしの数値の差が見た目の差に近くなるように設計された\ **知覚的に均等な色空間**\ が考案されてきた。古くから使われている CIELAB に続き、Björn Ottosson が 2020 年に提案した **OKLab** は、計算が簡単で、明るさや彩度を変えたときの色相のずれも少ない。CSS の色指定（CSS Color Module Level 4）にも採用されている。OKLab は、明るさ :math:`L`\ （黒が 0、白が 1）、緑から赤への軸 :math:`a`、青から黄への軸 :math:`b` の 3 成分で色を表す。

sRGB から OKLab への変換は、次の 3 段階で行う。

1. sRGB の値からガンマ補正を取り除き、光の強さに比例する線形の値に戻す。
2. 線形の RGB に 3×3 の行列を掛けて、目の錐体細胞の応答に近い 3 成分を求め、それぞれの立方根を取る。立方根は、光の強さに対して感じる明るさの増え方が緩やかになる性質を近似している。
3. 立方根を取った 3 成分に別の 3×3 の行列を掛けて、:math:`(L, a, b)` を得る。

1 段目のガンマ補正の除去は、sRGB の各成分 :math:`c`\ （0〜1）について次の式で行う。

.. math::

   c_{\mathrm{linear}} =
   \begin{cases}
   c / 12.92 & (c \le 0.04045) \\
   \left(\dfrac{c + 0.055}{1.055}\right)^{2.4} & (c > 0.04045)
   \end{cases}

OKLab から sRGB への逆変換は、各段階を逆にたどればよい。行列は逆行列に、立方根は 3 乗に置き換える。

.. literalinclude:: ../examples/oklab.py
   :language: python
   :start-at: # 線形 sRGB
   :end-at: -0.8086757660]])
   :caption: examples/oklab.py の変換行列

.. literalinclude:: ../examples/oklab.py
   :language: python
   :pyobject: srgb_to_linear
   :caption: examples/oklab.py の srgb_to_linear 関数

.. literalinclude:: ../examples/oklab.py
   :language: python
   :pyobject: srgb_to_oklab
   :caption: examples/oklab.py の srgb_to_oklab 関数

.. literalinclude:: ../examples/oklab.py
   :language: python
   :pyobject: oklab_to_srgb
   :caption: examples/oklab.py の oklab_to_srgb 関数

HSB のように色相を角度として扱いたい場合は、:math:`(a, b)` 平面を極座標で表した **OKLCH** を使う。彩度 :math:`C = \sqrt{a^2 + b^2}` は色の鮮やかさを、色相 :math:`h = \operatorname{atan2}(b, a)` は色合いを表す。HSB と同じく色相環の上で角度を操作できるうえに、:math:`L` がそのまま見た目の明るさになる点が異なる。ただし、:math:`L` と :math:`C` の組み合わせによっては、sRGB では表せない色（色域外の色）になる。本資料の実装では、範囲外の成分を 0〜1 に切り詰めている。

.. literalinclude:: ../examples/oklab.py
   :language: python
   :pyobject: oklch_to_srgb
   :caption: examples/oklab.py の oklch_to_srgb 関数

次の図は、HSB と OKLCH で色相を 1 周させた帯と、その明るさを比べたものである。1 段目は HSB の彩度・明度を 1 に固定した帯で、2 段目は 1 段目の各色を、OKLab の明るさ :math:`L` が等しいグレーに置き換えたものである。3 段目は OKLCH の :math:`L = 0.75`、:math:`C = 0.12` を固定した帯で、4 段目はその明るさである。HSB では黄やシアンの付近が明るく、青の付近が暗いのに対し、OKLCH では明るさが一様である。この組み合わせの :math:`L` と :math:`C` は、全ての色相で sRGB の範囲に収まる。

.. image:: _static/gallery/oklab_hue_lightness.png
   :alt: 上から HSB で色相を 1 周させた帯、その明るさのグレー、OKLCH で色相を 1 周させた帯、その明るさのグレー。HSB の明るさはむらがあり、OKLCH の明るさは一様
   :width: 480px

2 色の間のグラデーションも、どの色空間で補間するかによって見え方が変わる。sRGB の値のまま線形補間すると、中間の色が両端より暗く沈んだり、くすんだりしやすい。OKLab で補間すると、明るさ :math:`L` は両端の値の間を一定の割合で変化する。

.. literalinclude:: ../examples/oklab.py
   :language: python
   :pyobject: mix_srgb
   :caption: examples/oklab.py の mix_srgb 関数

.. literalinclude:: ../examples/oklab.py
   :language: python
   :pyobject: mix_oklab
   :caption: examples/oklab.py の mix_oklab 関数

次の図の 1・2 段目は青から黄への補間、3・4 段目は赤から緑への補間で、それぞれ上が sRGB、下が OKLab で補間したものである。青から黄では、sRGB の補間は前半で明るさがほとんど変わらず、後半で急に明るくなる。赤から緑では、sRGB の補間の中央が両端のどちらよりも暗くなり、濁った色になる。OKLab の補間では、どちらの組み合わせでも明るさが一定の割合で変化する。

.. image:: _static/gallery/oklab_gradient.png
   :alt: 青から黄、赤から緑への 2 通りのグラデーションを、それぞれ sRGB と OKLab で補間して上下に並べた画像。sRGB の補間は途中で暗く濁り、OKLab の補間は明るさが一定の割合で変化する
   :width: 480px

ただし、青と黄のように色相環の上で反対に近い色どうしでは、OKLab で補間しても中間で彩度が下がり、灰色に近い色を通る。中間でも鮮やかさを保ちたい場合は、``hsb_gradient`` と同じ考え方で、OKLCH の色相を短い弧に沿って回しながら補間するとよい。

.. _color-application:

配色を模様に適用する
----------------------

ここまでに作ったパレットは、色見本として眺めるだけでなく、模様に色を割り当てるときに使ってこそ意味がある。その効果を確かめるために、格子の各マスに背景色と、円・四分円・半円のどれか 1 つの図形を描くだけの単純な模様を使う。図形の種類と向き、各マスでどの色を選ぶかを決める乱数は 1 度だけ作っておき、色を取り出すパレットだけを差し替えて描く。こうすると、描いた画像どうしの違いは、配色だけによるものになる。

.. literalinclude:: ../examples/color_pattern.py
   :language: python
   :pyobject: make_layout
   :caption: examples/color_pattern.py の make_layout 関数

.. literalinclude:: ../examples/color_pattern.py
   :language: python
   :pyobject: render_pattern
   :caption: examples/color_pattern.py の render_pattern 関数

パレットの中の色を均等に使うのではなく、特定の色を少しだけ使いたい場合もある。そこで、色ごとに重みを与え、重みに比例した確率で色を選べるようにしている。

.. literalinclude:: ../examples/color_pattern.py
   :language: python
   :pyobject: pick_index
   :caption: examples/color_pattern.py の pick_index 関数

同じ模様を、3 種類のパレットで描くと次のようになる。1 枚目は RGB の各成分を一様乱数で決めた 12 色、2 枚目は soft トーンに固定して色相環を 5 等分したトーンイントーン、3 枚目は青のトーンオントーン 5 色を主役にし、補色に近い橙を差し色として少量だけ加えたものである。

.. image:: _static/gallery/color_pattern_random.png
   :alt: RGB の一様乱数で選んだ 12 色で塗った模様。彩度も明度もばらばらな色が隣り合い、雑然としている
   :width: 220px

.. image:: _static/gallery/color_pattern_tone.png
   :alt: soft トーンに固定して 5 色相を使ったトーンイントーンで塗った同じ模様。色相は異なるが全体の印象がそろっている
   :width: 220px

.. image:: _static/gallery/color_pattern_accent.png
   :alt: 青のトーンオントーン 5 色に、橙の差し色を少量だけ加えて塗った同じ模様。明暗の差で形が見え、橙が目を引く
   :width: 220px

1 枚目では、彩度も明度もばらばらな色が隣り合うため、どこに目を向ければよいか分からない雑然とした印象になる。2 枚目は、色相がばらばらでもトーンがそろっているため、全体がまとまって見える。3 枚目は、色相を 1 つに絞ることで明暗の差だけで形を見せ、少ない差し色の橙が目を引くアクセントになっている。形も乱数の使い方も全く同じであるにもかかわらず、3 枚の印象は大きく異なる。

本資料の以降の章の作例は、アルゴリズムの説明を優先しており、色を手作業で選んだり、RGB の乱数や matplotlib のカラーマップで決めたりしている。これらの作例も、色を決める部分を本章のパレットに差し替えるだけで、印象の異なる作品にできる。

本章で扱った配色パターン・PCCS トーン・グラデーション・OKLab による補間は、いずれも「手描きで色を決めるのではなく、色空間の構造そのものを操作して配色を機械的に導く」という発想で共通している。一方 ``extract_palette`` だけは逆に、既存の画像から色を取り出すという、ここまでとは向きの異なる技法だった。この「既存の画像を素材として扱う」という発想は、後の\ :doc:`image_effects`\ でさらに推し進める。
