はじめに
========

本資料の目的
------------

Houdini は、映画の視覚効果（VFX）やゲーム開発などで使われている 3DCG ソフトウェアである。他の多くの 3DCG ソフトウェアでは、画面上の形状をマウスで直接編集してモデルを作る。これに対して Houdini では、「箱を作る」「穴を開ける」「点の位置にコピーする」といった処理を表すノードをつないで、形状を作る手順そのものを組み立てる。この作り方をプロシージャル（procedural、手続き的）と呼ぶ。

手順を組み立てるという考え方は、プログラムを書くことによく似ている。そのため Houdini は、モデリングの経験が無くても、プログラミングの経験があるエンジニアにとって入りやすいソフトウェアである。本資料は、この強みを活かして、Houdini の基本的な考え方と操作を短い時間で身に付けることを目的とする。

対象読者と前提知識
------------------

本資料は、次のような読者を想定している。

* 3DCG のモデリングやアニメーションの経験は無い。
* Python の基本的な文法（変数、関数、リスト、辞書、for 文）を理解している。
* コマンドラインでスクリプトを実行したことがある。

3DCG の用語や数学の知識は前提としない。必要な知識は :doc:`cg_basics` で説明する。C 言語に似た文法（波かっこ、セミコロン、型宣言）を見たことがあると、:doc:`vex` を読みやすい。

本資料の構成
------------

.. list-table:: 本資料の構成
   :header-rows: 1
   :widths: 30 70

   * - 章
     - 内容
   * - :doc:`overview`
     - プロシージャルの考え方、エンジニアから見た Houdini、エディションと Apprentice の制限
   * - :doc:`cg_basics`
     - 座標系、ポリゴン、法線、UV、変換、レンダリングまでの流れ
   * - :doc:`ui`
     - 画面の構成、ビューポートとネットワークエディターの操作、ファイルの保存
   * - :doc:`nodes`
     - ネットワークの種類（コンテキスト）、ノードの接続、フラグ、クック
   * - :doc:`modeling`
     - 作例「机」で基本的なノードを使う
   * - :doc:`attributes`
     - ポイント、バーテックス、プリミティブ、ディテールとアトリビュート、グループ
   * - :doc:`expressions`
     - パラメーターの参照、エクスプレッション、キーフレームアニメーション
   * - :doc:`vex`
     - Attribute Wrangle と VEX の文法、よく使う関数
   * - :doc:`procedural`
     - 作例「階段」「建物群」でプロシージャルモデリングを実践する
   * - :doc:`python`
     - hou モジュール、Python SOP、シェルフツール、hython
   * - :doc:`hda`
     - ネットワークを部品化するデジタルアセット（HDA）
   * - :doc:`rendering`
     - Solaris、USD、Karma によるレンダリング
   * - :doc:`simulation`
     - 剛体シミュレーションとキャッシュ
   * - :doc:`next`
     - 本資料で扱わなかった分野と、学習の進め方

巻末に :doc:`glossary`、:doc:`code`、:doc:`references` を付けた。

:doc:`overview` から :doc:`nodes` までは、Houdini を使うための準備である。:doc:`modeling` 以降は、実際に Houdini を操作しながら読み進めることを勧める。

動作確認環境
------------

本資料の内容とサンプルコードは、次の環境で確認した。

.. list-table:: 動作確認環境
   :header-rows: 1
   :widths: 30 70

   * - 項目
     - バージョンなど
   * - OS
     - Windows 11
   * - Houdini
     - Houdini 22.0.466（Houdini Apprentice のライセンスで使用）
   * - Python
     - 3.13（Houdini に付属するもの）
   * - レンダラー
     - Karma CPU（Houdini に付属するもの）

Houdini は、バージョンによって画面の見た目、ノードの名前、パラメーターの名前が変わることがある。異なるバージョンを使う場合は、Houdini のヘルプ（:doc:`ui` を参照）で該当するノードの説明を確認する。

表記の約束事
------------

本資料では、次のように表記する。

.. list-table:: 表記の約束事
   :header-rows: 1
   :widths: 35 65

   * - 表記
     - 意味
   * - :menuselection:`File --> Save`
     - メニューの :guilabel:`File` から :guilabel:`Save` を選ぶ。
   * - :guilabel:`Size`
     - 画面に表示されるボタンやパラメーターの名前（ラベル）。Houdini の画面は英語で表示されるため、英語のまま書く。
   * - :kbd:`Ctrl+S`
     - キーボードのキー。:kbd:`Ctrl+S` は、:kbd:`Ctrl` を押しながら :kbd:`S` を押すことを表す。
   * - LMB、MMB、RMB
     - マウスの左ボタン（Left Mouse Button）、中ボタン（Middle）、右ボタン（Right）。Houdini のヘルプと同じ略記である。
   * - Box ノード
     - ノードの種類。画面の表示（ラベル）を英語のまま書く。
   * - ``sizex``
     - パラメーターやアトリビュートの内部名、コード、ファイル名。

長さの単位は、特に断らない限りメートルとする。Houdini の既定の長さの単位はメートルである。

サンプルコードの使い方
----------------------

本資料のサンプルコードは、:doc:`code` からまとめてダウンロードできる。展開すると ``examples`` ディレクトリができる。以降の説明では、``C:\houdini_intro\examples`` に置いたものとする。

サンプルコードの多くは、Houdini の中にノードのネットワークを組み立てる Python スクリプトである。本文の操作手順で作るネットワークと同じものを、スクリプトで一度に作れる。手順の途中で分からなくなったときに、完成形と見比べるのに使う。

Houdini の画面から実行する
^^^^^^^^^^^^^^^^^^^^^^^^^^

:menuselection:`Windows --> Python Shell` で Python Shell を開き、次のように入力する。``build_table`` の部分は、実行したいスクリプトの名前（拡張子 ``.py`` を除いたもの）に置き換える。

.. code-block:: python
   :linenos:

   import sys
   sys.path.append(r"C:\houdini_intro\examples")
   import build_table
   build_table.build()

1 行目と 2 行目は、Python がモジュールを探す場所に ``examples`` ディレクトリを追加している。3 行目でスクリプトをモジュールとして読み込み、4 行目でネットワークを組み立てる関数を呼んでいる。Python は一度読み込んだモジュールを再び読み込まないので、スクリプトを書き換えた後は、``import importlib`` を実行してから ``importlib.reload(build_table)`` で読み込み直す。

hython から実行する
^^^^^^^^^^^^^^^^^^^

hython は、Houdini に付属する Python のインタープリターである。画面を開かずに Houdini の機能を使える（:doc:`python` を参照）。コマンドプロンプトで次のように実行すると、ネットワークを組み立てて結果を表示し、シーンファイル ``table.hipnc`` に保存する。

.. code-block:: bat
   :linenos:

   cd C:\houdini_intro\examples
   "C:\Program Files\Side Effects Software\Houdini 22.0.466\bin\hython.exe" build_table.py table.hipnc

本資料の執筆時に、hython は Apprentice のライセンスでも動作することを確認した。

.. note::

   サンプルコードと同じディレクトリに、Houdini が内部で使う Python モジュールと同じ名前のファイル（例えば ``dbg.py``）を置かない。Houdini がそのファイルを誤って読み込み、一部の機能が動かなくなることがある（:doc:`python` の「モジュールの名前に注意する」を参照）。
