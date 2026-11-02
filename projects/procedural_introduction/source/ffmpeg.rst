付録 C　ffmpeg の早見表
============================================================

本書で使う ffmpeg のコマンドとオプションをまとめる。使い方の説明は第 14 章にある。コマンドは 1 行で入力する。``input.mp4`` などのファイル名は適宜置き換える。

コマンドの形
------------------------------------------------------------

ffmpeg のコマンドは、おおむね次の順に書く。オプションは、直後に書いた入力ファイル（``-i`` の前）または出力ファイル（出力ファイル名の前）に対して働く。

.. code-block:: bat
   :linenos:

   ffmpeg [全体のオプション] [入力のオプション] -i 入力 [出力のオプション] 出力

.. list-table:: 全体のオプション
   :header-rows: 1
   :widths: 30 70

   * - オプション
     - 意味
   * - ``-y``
     - 出力ファイルがあれば確認せずに上書きする
   * - ``-hide_banner``
     - 起動時の版や構成の表示を省く
   * - ``-loglevel error``
     - エラーだけを表示する（\ ``-v error`` と同じ）

入力
------------------------------------------------------------

.. list-table:: 入力のオプション
   :header-rows: 1
   :widths: 35 65

   * - オプション
     - 意味
   * - ``-i ファイル``
     - 入力ファイル。``-`` なら標準入力から読む
   * - ``-f rawvideo``
     - 入力がヘッダーの無い生の画素列であることを示す
   * - ``-pix_fmt rgb24``
     - （入力側に書いた場合）生の画素列の 1 画素の形式。``rgb24`` は RGB 各 8 bit
   * - ``-s 640x360``
     - 生の画素列の幅と高さ
   * - ``-r 30``
     - （入力側に書いた場合）生の画素列のフレームレート
   * - ``-framerate 30``
     - 連番画像を入力するときのフレームレート
   * - ``-f concat -safe 0``
     - 入力がファイルの一覧（連結用）であることを示す
   * - ``-ss 秒``・``-t 秒``
     - 開始位置と長さ。入力ファイルの一部だけを使う

Python から生の画素列を渡す（第 14 章の ``VideoWriter``）:

.. code-block:: bat
   :linenos:

   ffmpeg -y -f rawvideo -pix_fmt rgb24 -s 640x360 -r 30 -i - -c:v libx264 -preset slow -crf 28 -pix_fmt yuv420p -movflags +faststart -an out.mp4

連番の PNG を動画にする（第 15 章の Godot の書き出しなどに使う）。``%04d`` は 4 桁の 0 埋めの番号（``frame_0001.png`` など）を表す。番号の桁数がファイル名と合うように ``%08d`` などに変える。番号が 0〜4 以外から始まる場合は、入力の前に ``-start_number 番号`` を付ける。

.. code-block:: bat
   :linenos:

   ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -movflags +faststart out.mp4

出力: H.264（MP4）
------------------------------------------------------------

.. list-table:: H.264 の主なオプション
   :header-rows: 1
   :widths: 35 65

   * - オプション
     - 意味
   * - ``-c:v libx264``
     - 映像を H.264 で圧縮する
   * - ``-crf 23``
     - 画質の指定。0（劣化なし）〜51。標準は 23。6 増やすと容量はおよそ半分
   * - ``-preset slow``
     - 圧縮の手間。``ultrafast``・``superfast``・``veryfast``・``faster``・``fast``・``medium``\ （標準）・``slow``・``slower``・``veryslow``。遅いほど同じ画質で小さくなる傾向がある
   * - ``-pix_fmt yuv420p``
     - 色を縦横半分の解像度で持つ形式。ブラウザーで再生するために指定する。幅と高さは偶数にする
   * - ``-movflags +faststart``
     - 目次の情報をファイルの先頭に置き、Web で読み込みながら再生できるようにする
   * - ``-an``
     - 音声を出力しない
   * - ``-c copy``
     - 再圧縮せずにデータを書き写す（連結や切り出しで画質を保つ）

出力: VP9（WebM）
------------------------------------------------------------

VP9 で画質を指定して書き出すには、``-b:v 0``\ （ビットレートの上限なし）と ``-crf`` を組み合わせる。VP9 の CRF は 0〜63 で、大きいほど小さく粗くなる。``-row-mt 1`` は書き出しを複数のスレッドで並列に行う指定で、時間を短くできる。

.. code-block:: bat
   :linenos:

   ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 0 -crf 40 -row-mt 1 -an out.webm

ブラウザーで録画した WebM を、Web 向けの MP4 に変換する（第 14 章の GLSL の録画）:

.. code-block:: bat
   :linenos:

   ffmpeg -i loop_5s.webm -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -movflags +faststart -an loop.mp4

出力: GIF
------------------------------------------------------------

動画全体から最適なパレットを作り（``palettegen``）、それを使って減色する（``paletteuse``）。``split`` で映像を 2 つに分け、一方からパレットを作り、もう一方に適用する。``max_colors`` で色数を、``dither`` で減色の縞を目立たなくする点の模様の種類を指定する。

.. code-block:: bat
   :linenos:

   ffmpeg -i input.mp4 -vf "fps=15,scale=480:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer" out.gif

フィルター
------------------------------------------------------------

映像のフィルターは ``-vf "フィルター1,フィルター2"`` のようにコンマでつなぐ。フィルターのオプションは ``名前=値`` をコロンで区切って書く。

.. list-table:: 本書で使うフィルター
   :header-rows: 1
   :widths: 30 70

   * - フィルター
     - 意味
   * - ``scale=320:-2:flags=lanczos``
     - 幅 320 に縮小し、高さは縦横比を保って偶数に決める（``-1`` なら偶数に限らない）
   * - ``fps=15``
     - フレームレートを変える（フレームを間引く・複製する）
   * - ``drawtext=...``
     - 文字を重ねる。``fontfile``・``text``\ （または ``textfile``）・``fontsize``・``fontcolor``・``x``・``y``・``box``・``boxcolor`` などを指定する
   * - ``minterpolate=fps=60:mi_mode=mci``
     - 動き補償で中間のフレームを作り、フレームレートを上げる。計算が重い
   * - ``palettegen``・``paletteuse``
     - GIF 用のパレットを作る・使う

拡大縮小:

.. code-block:: bat
   :linenos:

   ffmpeg -i input.mp4 -vf "scale=320:-2:flags=lanczos" -c:v libx264 -crf 23 -preset slow -pix_fmt yuv420p small.mp4

連結（つなぐファイルを ``list.txt`` に ``file 'a.mp4'`` の形で 1 行ずつ書く）:

.. code-block:: bat
   :linenos:

   ffmpeg -f concat -safe 0 -i list.txt -c copy joined.mp4

文字の重ね合わせ（Windows のフォントを使う例。ドライブ名のコロンは ``\:`` と書く）:

.. code-block:: bat
   :linenos:

   ffmpeg -i input.mp4 -vf "drawtext=fontfile='C\:/Windows/Fonts/meiryo.ttc':text='タイトル':fontsize=28:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=8:x=(w-text_w)/2:y=h-text_h-24" -c:v libx264 -crf 23 -pix_fmt yuv420p titled.mp4

フレームの補間:

.. code-block:: bat
   :linenos:

   ffmpeg -i input15.mp4 -vf "minterpolate=fps=30:mi_mode=mci" -c:v libx264 -crf 23 -pix_fmt yuv420p smooth30.mp4

動画の情報を調べる（ffprobe）
------------------------------------------------------------

ffmpeg に付属する ffprobe で、動画の大きさ・フレームレート・フレーム数・長さを調べられる。``-count_frames`` は、実際にすべてのフレームを読んで数える指定である（時間がかかるが確実）。

.. code-block:: bat
   :linenos:

   ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames -of csv=p=0 input.mp4
   ffprobe -v error -show_entries format=duration,size,bit_rate -of default=noprint_wrappers=1 input.mp4

1 行目は ``640,360,30/1,150`` のように、幅・高さ・フレームレート・フレーム数を表示する。2 行目は長さ（秒）・容量（バイト）・ビットレート（bit/s）を表示する。動画の一部を画像として取り出して確かめるには、次のようにする（1 秒目の 1 フレームを PNG にする）。

.. code-block:: bat
   :linenos:

   ffmpeg -ss 1 -i input.mp4 -frames:v 1 frame.png

Web 向けに小さく書き出す設定の例
------------------------------------------------------------

Web ページに置く短い映像（背景のループ、作例の紹介など）の設定の例を示す。容量は映像の内容で大きく変わるので、書き出した後に確かめて CRF を調整する。

.. list-table:: Web 向けの設定の例
   :header-rows: 1
   :widths: 25 45 30

   * - 用途
     - 設定
     - 目安
   * - 標準（本書の動画）
     - 640 × 360、30 fps、H.264、CRF 28、preset slow、yuv420p、faststart
     - 10 秒で数百 KB〜2 MB
   * - 画質を優先
     - 1280 × 720、30 fps、H.264、CRF 23、preset slow
     - 細かい模様が多いと大きくなる
   * - さらに小さく
     - VP9 の WebM（CRF 35〜40）を MP4 と併せて用意する
     - 書き出しに時間がかかる
   * - 細かい粒や乱数のちらつきが多い映像
     - 解像度を下げる、粒を描かない・ぼかす、CRF を上げる
     - 粒は圧縮しにくく、容量が数十倍になることがある

.. code-block:: bat
   :linenos:

   ffmpeg -i input.mp4 -vf "scale=640:-2:flags=lanczos,fps=30" -c:v libx264 -preset slow -crf 28 -pix_fmt yuv420p -movflags +faststart -an web.mp4

ページへの埋め込みは、MP4 と WebM の両方を用意し、ブラウザーが再生できる方を選ばせることもできる。``<source>`` は上から順に試される。

.. code-block:: html
   :linenos:

   <video autoplay loop muted playsinline>
     <source src="web.webm" type="video/webm">
     <source src="web.mp4" type="video/mp4">
   </video>
