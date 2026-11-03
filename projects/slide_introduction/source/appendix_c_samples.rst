付録 C サンプル一覧
===================

本書で使った Marp のサンプルスライドと、図を生成する Python のスクリプトの一覧である。

Marp のサンプルスライド
-----------------------

サンプルは、本書のビルド時に Marp CLI で HTML と PDF に変換している。HTML はブラウザで開き、矢印キーでスライドを送れる。:kbd:`P` キーを押すと、発表者ノート付きの発表者用の画面が開く。

.. list-table:: Marp のサンプルスライド
   :header-rows: 1
   :widths: 24 36 40

   * - ファイル
     - 内容
     - 閲覧・ダウンロード
   * - ``tech_talk.md``
     - 技術発表（11 枚）。社内勉強会での「ログ検索を 10 倍速くした話」
     - `HTML <_static/marp/tech_talk.html>`__、`PDF <_static/marp/tech_talk.pdf>`__、:download:`Markdown <../examples/marp/tech_talk.md>`
   * - ``progress_report.md``
     - 進捗報告（6 枚）。決済 API の移行プロジェクトの週次報告
     - `HTML <_static/marp/progress_report.html>`__、`PDF <_static/marp/progress_report.pdf>`__、:download:`Markdown <../examples/marp/progress_report.md>`
   * - ``lightning_talk.md``
     - LT（8 枚）。5 分の LT「レビューの指摘を半分にした話」
     - `HTML <_static/marp/lightning_talk.html>`__、`PDF <_static/marp/lightning_talk.pdf>`__、:download:`Markdown <../examples/marp/lightning_talk.md>`
   * - ``themes/simple.css``
     - 3 つのサンプルで使っているテーマ CSS
     - :download:`CSS <../examples/marp/themes/simple.css>`

サンプルの内容はすべて架空のものである。

フォルダ構成
~~~~~~~~~~~~

サンプルをダウンロードして使う場合は、次の構成で保存する。

.. code-block:: text
   :linenos:

   marp/
   ├── tech_talk.md
   ├── progress_report.md
   ├── lightning_talk.md
   └── themes/
       └── simple.css

変換の方法
~~~~~~~~~~

Marp CLI を使う場合は、``marp`` フォルダで次のコマンドを実行する。Marp CLI の導入方法は 7 章を参照してほしい。

.. code-block:: bash
   :linenos:

   # HTML に変換する
   marp tech_talk.md --theme-set themes/simple.css -o tech_talk.html

   # PDF に変換する
   marp tech_talk.md --theme-set themes/simple.css --pdf

   # すべてのスライドを PNG 画像に変換する（tech_talk.001.png、tech_talk.002.png、...）
   marp tech_talk.md --theme-set themes/simple.css --images png

   # ファイルの変更を監視して、保存するたびに HTML を作り直す
   marp tech_talk.md --theme-set themes/simple.css -w

Marp for VS Code でテーマ ``simple`` を使う場合は、``marp`` フォルダを VS Code で開き、``.vscode/settings.json`` に次の設定を書く。

.. code-block:: json
   :linenos:

   {
     "markdown.marp.themes": ["./themes/simple.css"]
   }

サンプルのテーマは、フォントに Noto Sans JP を指定し、なければ Yu Gothic UI、Meiryo の順に使う。いずれもない環境では、別のフォントで表示され、文字の幅が変わることがある。

図の生成スクリプト
------------------

本文の図のうち、スライドの見本とグラフは、Python のスクリプトでビルド時に生成している。スクリプトは本書のソースの ``source/_scripts`` フォルダにあり、``source/conf.py`` から呼び出している。

.. list-table:: 図の生成スクリプト
   :header-rows: 1
   :widths: 30 70

   * - ファイル
     - 内容
   * - ``generate_figures.py``
     - Pillow と matplotlib で、改善前と改善後のスライドの見本、グラフ、配色の図、色覚のシミュレーションなど 16 点の図を生成する
   * - ``convert_marp.py``
     - Marp CLI を呼び出し、Marp のサンプルを HTML、PDF、PNG に変換する。Marp CLI が見つからない場合は、ビルドに警告を出して変換を省略する

フロー図やピラミッド構造などの図は、Graphviz で rst ファイルの中に記述している。

これらのスクリプトは、flake8（1 行 120 文字まで）と mypy（``strict = True``）の検査を通している。
