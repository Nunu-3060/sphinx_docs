付録 A　Pyxel API 早見表
========================

本書で使った Pyxel 2.9.9 の API をまとめる。すべての API は `Pyxel API Reference <https://github.com/kitao/pyxel/blob/main/docs/api-reference.md>`__ に掲載されている。引数の col は色の番号（0 ～ 15）を表す。

システム
--------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - API
     - 説明
   * - ``pyxel.init(width, height, title, fps)``
     - 画面の大きさ、ウィンドウのタイトル、fps（既定は 30）を指定して初期化する。
   * - ``pyxel.run(update, draw)``
     - ゲームループを開始し、毎フレーム update と draw を呼ぶ。
   * - ``pyxel.quit()``
     - プログラムを終了する。
   * - ``pyxel.frame_count``
     - 経過したフレーム数。
   * - ``pyxel.width``、``pyxel.height``
     - 画面の幅と高さ。
   * - ``pyxel.perf_monitor(enabled)``
     - パフォーマンスモニターの表示を切り替える。
   * - ``pyxel.user_data_dir(vendor_name, app_name)``
     - セーブデータなどを保存するディレクトリのパスを返す。なければ作成する。

リソース
--------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - API
     - 説明
   * - ``pyxel.load(filename)``
     - リソースファイル（.pyxres）を読み込む。
   * - ``pyxel.save(filename)``
     - リソースファイルに保存する。
   * - ``pyxel.images[n]``
     - イメージバンク n（0 ～ 2）。``Image`` クラスのインスタンス。
   * - ``pyxel.tilemaps[n]``
     - タイルマップ n（0 ～ 7）。``Tilemap`` クラスのインスタンス。
   * - ``Image.set(x, y, data)``
     - 16 進数の文字列のリストで、(x, y) から絵を書き込む。
   * - ``Image.load(x, y, filename)``
     - PNG などの画像ファイルを (x, y) に読み込む。
   * - ``Tilemap.pset(x, y, (tx, ty))``
     - タイルマップの (x, y) のマスにタイル (tx, ty) を置く。

入力
----

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - API
     - 説明
   * - ``pyxel.btn(key)``
     - key が押されていれば True を返す。
   * - ``pyxel.btnp(key, hold, repeat)``
     - key が押されたフレームで True を返す。hold と repeat を指定すると、押し続けたときに一定間隔で True を返す。
   * - ``pyxel.btnr(key)``
     - key が離されたフレームで True を返す。
   * - ``pyxel.KEY_LEFT`` など
     - キーボードのキー。
   * - ``pyxel.GAMEPAD1_BUTTON_A`` など
     - ゲームパッドのボタン（GAMEPAD1 ～ GAMEPAD4）。

描画
----

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - API
     - 説明
   * - ``pyxel.cls(col)``
     - 画面を塗りつぶす。
   * - ``pyxel.pset(x, y, col)``
     - 点を描く。
   * - ``pyxel.line(x1, y1, x2, y2, col)``
     - 線を引く。
   * - ``pyxel.rect(x, y, w, h, col)``、``pyxel.rectb(...)``
     - 四角形を描く（rectb は枠だけ）。
   * - ``pyxel.circ(x, y, r, col)``、``pyxel.circb(...)``
     - 円を描く（circb は枠だけ）。
   * - ``pyxel.tri(x1, y1, x2, y2, x3, y3, col)``
     - 三角形を描く。
   * - ``pyxel.text(x, y, s, col)``
     - 文字列を描く。
   * - ``pyxel.blt(x, y, img, u, v, w, h, colkey, rotate=0.0, scale=1.0)``
     - イメージバンク img の (u, v) から w × h の絵を描く。colkey は透明色。rotate（回転の角度）と scale（拡大率）はキーワード引数で指定する。
   * - ``pyxel.bltm(x, y, tm, u, v, w, h, colkey)``
     - タイルマップ tm の (u, v) から w × h（ピクセル単位）を描く。
   * - ``pyxel.camera(x, y)``、``pyxel.camera()``
     - 以降の描画を (-x, -y) ずらす。引数なしで元に戻す。
   * - ``pyxel.pal(col1, col2)``、``pyxel.pal()``
     - 色 col1 を col2 に置き換えて描く。引数なしで元に戻す。
   * - ``pyxel.dither(alpha)``
     - 点を間引いて描く（0.0 ～ 1.0）。1.0 で元に戻る。
   * - ``pyxel.FONT_WIDTH``、``pyxel.FONT_HEIGHT``
     - 標準フォントの 1 文字の幅（4）と高さ（6）。

サウンド
--------

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - API
     - 説明
   * - ``pyxel.play(ch, snd, sec=0, loop=False)``
     - チャンネル ch でサウンド snd を鳴らす。snd には番号、番号のリスト、MML の文字列を指定できる。sec は再生を始める位置（秒）。loop はキーワード引数で指定する。
   * - ``pyxel.playm(msc, sec=0, loop=False)``
     - ミュージック msc を鳴らす。loop はキーワード引数で指定する。
   * - ``pyxel.stop(ch)``、``pyxel.stop()``
     - チャンネル ch の音を止める。引数なしですべて止める。
   * - ``pyxel.sounds[n]``
     - サウンド n（0 ～ 63）。``Sound`` クラスのインスタンス。
   * - ``pyxel.musics[n]``
     - ミュージック n（0 ～ 7）。``Music`` クラスのインスタンス。
   * - ``Sound.set(notes, tones, volumes, effects, speed)``
     - 文字列でサウンドを定義する。
   * - ``Music.set(seq0, seq1, ...)``
     - チャンネルごとのサウンドの番号のリストで、ミュージックを定義する。
   * - ``pyxel.gen_bgm(preset, transp, instr, seed, play=False)``
     - BGM を自動で作り、チャンネルごとの MML の文字列のリストを返す。

数学
----

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - API
     - 説明
   * - ``pyxel.rndi(a, b)``、``pyxel.rndf(a, b)``
     - a 以上 b 以下の乱数（整数、小数）を返す。
   * - ``pyxel.rseed(seed)``
     - 乱数の種を設定する。
   * - ``pyxel.clamp(x, lower, upper)``
     - x を lower ～ upper の範囲に収めた値を返す。
   * - ``pyxel.sin(deg)``、``pyxel.cos(deg)``
     - 正弦と余弦を返す。角度は度で指定する。
   * - ``pyxel.atan2(y, x)``
     - (x, y) の向きの角度を度で返す。
