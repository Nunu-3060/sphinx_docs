ゲームの公開
============

ゲームは、ほかの人に遊んでもらって初めて完成する。この章では、題材ゲームを配布できる形にまとめ、Web で公開する方法を説明する。

公開の形式
----------

Pyxel のゲームは、:numref:`table-publish-formats` の 3 つの形式で配布できる。

.. _table-publish-formats:

.. list-table:: 配布の形式
   :header-rows: 1
   :widths: 25 40 35

   * - 形式
     - 遊ぶ人に必要なもの
     - 作り方
   * - Pyxel アプリケーションファイル（.pyxapp）
     - Python と Pyxel
     - ``pyxel package``
   * - HTML ファイル
     - Web ブラウザとインターネット接続
     - ``pyxel app2html``
   * - 実行ファイル
     - なし（ただし OS ごとに作る必要がある）
     - ``pyxel app2exe``

最も手軽に多くの人に遊んでもらえるのは、HTML ファイルを Web で公開する方法である。遊ぶ人は何もインストールせず、URL を開くだけで遊べる。スマートフォンやタブレットでも、画面に表示される仮想のゲームパッドで遊べる。本書の題材ゲームも、この方法で公開している（`COSMO RUSH を遊ぶ <play/cosmo_rush.html>`__）。

どの形式も、まず ``.pyxapp`` ファイルを作り、それを変換して作る（:numref:`fig-publish-flow`）。

.. _fig-publish-flow:

.. graphviz::
   :caption: 公開までの流れ
   :align: center

   digraph publish {
     rankdir=LR;
     node [shape=box, style="rounded,filled", fillcolor="#eef3ff", fontsize=11];
     edge [fontsize=10];
     dir [label="ゲームのディレクトリ\n(main.py, .pyxres)", shape=folder, fillcolor="#fff4d6"];
     app [label="cosmo_rush.pyxapp"];
     html [label="cosmo_rush.html"];
     exe [label="cosmo_rush.exe など"];
     pages [label="GitHub Pages で公開", shape=box3d, fillcolor="#ffffff"];
     dir -> app [label="pyxel package"];
     app -> html [label="pyxel app2html"];
     app -> exe [label="pyxel app2exe"];
     html -> pages [label="git push"];
   }

Pyxel アプリケーションファイルを作る
------------------------------------

ディレクトリを整える
^^^^^^^^^^^^^^^^^^^^

``pyxel package`` は、指定したディレクトリの中身を 1 つのファイルにまとめる。そのため、ゲームに必要なファイルはすべてそのディレクトリの中に置く。題材ゲームでは、``examples/cosmo_rush`` に ``main.py`` とリソースファイル ``cosmo_rush.pyxres`` を置いている。ステップ 6 ～ 9 のように ``../assets/`` のようなディレクトリの外のファイルを読み込んでいると、パッケージにしたときに見つからなくなる。完成版の ``main.py`` が、``RESOURCE_FILE`` に ``"cosmo_rush.pyxres"`` と同じディレクトリのファイルを指定しているのはこのためである。

反対に、ゲームに不要なファイルはディレクトリに置かない。ドット（.）で始まるファイルとディレクトリ、``__pycache__``、拡張子が ``.gif`` と ``.zip`` のファイルは除かれるが、それ以外はすべてパッケージに含まれる。本書では、テストのファイルを ``cosmo_rush`` の外の ``tests`` ディレクトリに置いた。

メタデータを書く
^^^^^^^^^^^^^^^^

起動するスクリプトの先頭に決まった形式のコメントを書いておくと、パッケージにゲームの情報（メタデータ）が記録される。記録した情報は、``pyxel play`` で実行したときに端末に表示される（:numref:`list-metadata`）。

.. _list-metadata:

.. literalinclude:: ../examples/cosmo_rush/main.py
   :language: python
   :linenos:
   :lines: 1-5
   :caption: cosmo_rush/main.py（メタデータ）

書ける項目は title、author、desc（説明）、site（Web サイト）、license、version である。

パッケージを作って実行する
^^^^^^^^^^^^^^^^^^^^^^^^^^

``pyxel package`` には、ゲームのディレクトリと、最初に実行するスクリプトを指定する。``.pyxapp`` ファイルは、カレントディレクトリにディレクトリと同じ名前で作られる。

.. code-block:: console
   :linenos:

   > pyxel package cosmo_rush cosmo_rush/main.py
   -----------------------------------------------------------
   title   : COSMO RUSH
   author  : Nunu_3060
   desc    : A tiny vertical scrolling shooter made with Pyxel
   license : MIT
   version : 1.0
   -----------------------------------------------------------
   added 'cosmo_rush\.pyxapp_startup_script'
   added 'cosmo_rush\cosmo_rush.pyxres'
   added 'cosmo_rush\main.py'
   > pyxel play cosmo_rush.pyxapp

``pyxel play`` でゲームが起動すれば成功である。

Web で公開する
--------------

HTML ファイルに変換する
^^^^^^^^^^^^^^^^^^^^^^^

``pyxel app2html`` で、``.pyxapp`` ファイルを HTML ファイルに変換する。

.. code-block:: console
   :linenos:

   > pyxel app2html cosmo_rush.pyxapp

カレントディレクトリに ``cosmo_rush.html`` ができる。この HTML ファイルには、ゲームのプログラムとリソースがすべて埋め込まれている。Web ブラウザで動く版の Pyxel 本体は、HTML ファイルを開いたときにインターネット上（jsDelivr という配信サービス）から読み込まれる。このとき読み込まれるのは変換に使った Pyxel と同じバージョン（本書では 2.9.9）なので、後で Pyxel が更新されてもゲームの動きは変わらない。

手元で動作を確かめる
^^^^^^^^^^^^^^^^^^^^

生成した HTML ファイルをダブルクリックしてブラウザで開くと、ブラウザの制限により Pyxel の読み込みに失敗する。手元で確かめるときは、Python に付属する簡易 Web サーバーを使う。

.. code-block:: console
   :linenos:

   > python -m http.server 8000

ブラウザで ``http://localhost:8000/cosmo_rush.html`` を開き、「CLICK TO START」と表示された画面をクリックするとゲームが始まる。ブラウザは、ユーザーが操作するまで音を鳴らさないので、最初にクリックが必要になる。確かめ終わったら、端末で Ctrl + C を押してサーバーを止める。

GitHub Pages で公開する
^^^^^^^^^^^^^^^^^^^^^^^

**GitHub Pages** は、GitHub のリポジトリに置いたファイルを Web サイトとして無料で公開できるサービスである。HTML ファイルを 1 つ置くだけでゲームを公開できる。

#. GitHub で新しい公開リポジトリを作る（例：``cosmo-rush``）。
#. ``cosmo_rush.html`` を ``index.html`` という名前に変えてリポジトリの最上位に置き、コミットしてプッシュする。
#. リポジトリの Settings → Pages を開き、Source を「Deploy from a branch」に、Branch を ``main`` と ``/ (root)`` にして保存する。
#. 数分待つと、``https://<ユーザー名>.github.io/cosmo-rush/`` でゲームが遊べるようになる。

.. code-block:: console
   :linenos:

   > git init
   > git add index.html
   > git commit -m "Publish COSMO RUSH"
   > git branch -M main
   > git remote add origin https://github.com/<ユーザー名>/cosmo-rush.git
   > git push -u origin main

GitHub Pages の詳しい使い方は、`GitHub Pages のドキュメント <https://docs.github.com/ja/pages>`__ を参照してほしい。

Pyxel Web Launcher を使う
^^^^^^^^^^^^^^^^^^^^^^^^^

GitHub に ``.pyxapp`` ファイルを置いた場合は、`Pyxel Web Launcher <https://kitao.github.io/pyxel/web/launcher/>`__ を使って、HTML ファイルを作らずにブラウザで遊べるようにすることもできる。次の形式の URL を開くと、リポジトリの ``.pyxapp`` ファイルがブラウザで実行される。

.. code-block:: text
   :linenos:

   https://kitao.github.io/pyxel/web/launcher/?play=<ユーザー名>/<リポジトリ名>/<ブランチ名>/<パス>/<拡張子を除いたファイル名>

Pyxel Web Launcher は常に最新版の Pyxel を使う。将来の Pyxel の変更で動かなくなる可能性があるので、長く公開しておきたい場合は ``app2html`` で作った HTML ファイルを使うほうが安心である。

.. note::

   Web 版では、``pyxel.user_data_dir()`` が返すディレクトリは、ブラウザの中に用意された仮想的なファイルシステムの中にある。ハイスコアのようにページを閉じた後も残したいデータを扱う場合は、公開した環境で、ページを読み込み直してもデータが残るかを必ず確かめること。

実行ファイルを作る
------------------

Python をインストールしていない人に配る場合は、``pyxel app2exe`` で実行ファイルを作る。この機能は PyInstaller というツールを使うので、先にインストールしておく。

.. code-block:: console
   :linenos:

   > pip install pyinstaller
   > pyxel app2exe cosmo_rush.pyxapp

Windows では、``dist/cosmo_rush`` ディレクトリに ``cosmo_rush.exe`` と、実行に必要なファイルを入れた ``_internal`` ディレクトリができる。配布するときは、``dist/cosmo_rush`` ディレクトリごと zip ファイルにまとめる。

.. warning::

   ``pyxel app2exe`` は、作業の最後にカレントディレクトリの ``build`` ディレクトリを削除する。``build`` という名前のディレクトリに大切なファイルを置いている場所では実行しないこと。

実行ファイルは、作成した OS でしか動かない。Windows 用、macOS 用、Linux 用を配りたい場合は、それぞれの OS で作る必要がある。また、署名のない実行ファイルは、OS のセキュリティ機能によって警告が表示されることがある。この点でも、Web での公開のほうが遊んでもらうまでの手間が少ない。

ライセンスとクレジット
----------------------

ゲームを公開するときは、ライセンス（ほかの人がどこまで自由に使ってよいかの条件）を決めておく。題材ゲームのコードは MIT ライセンスとしている。MIT ライセンスは、著作権表示とライセンス文を残せば、改変や再配布を自由に認めるライセンスである。ライセンスの選び方は `Choose a License <https://choosealicense.com/>`__ が参考になる。

ほかの人が作った素材（画像、音楽、フォントなど）を使う場合は、次の点を必ず確かめる。

* ゲームでの利用と、ゲームに含めた再配布が許されているか。
* 作者名などのクレジットの表示が必要か。必要なら、タイトル画面やゲームの説明文に記載する。

Pyxel 自体も MIT ライセンスで公開されている。``app2exe`` で作った実行ファイルには Pyxel が含まれるので、配布物に Pyxel のライセンス文を同梱しておくとよい。

遊んでもらうために
------------------

公開したら、遊んでもらうための発信も行う。

* **スクリーンショットと動画**：実行中に Alt + 1 を押すと画面のスクリーンショットを、Alt + 3 を押すと直近の画面の GIF アニメーションをデスクトップに保存できる。動きのある GIF アニメーションは、ゲームの魅力を一目で伝える。
* **公開する場所**：自分の Web サイトや SNS のほか、インディーゲームの投稿サイトである `itch.io <https://itch.io/>`__ に HTML 版のゲームを登録する方法もある。
* **感想をもらう**：遊んだ人の感想は、次のゲームを作るときの何よりの参考になる。

まとめ
------

* ``pyxel package`` でゲームのディレクトリを ``.pyxapp`` ファイルにまとめる。必要なファイルはすべてディレクトリの中に置く。
* ``pyxel app2html`` で HTML ファイルに変換し、GitHub Pages などで公開すると、誰でもブラウザで遊べる。
* ``pyxel app2exe`` で実行ファイルを作れるが、OS ごとに作る必要がある。
* コードと素材のライセンスを確かめ、必要なクレジットを表示する。
