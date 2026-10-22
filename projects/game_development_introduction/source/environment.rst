開発環境の準備
==============

この章では、:doc:`practice`\ のサンプルコードを動かすための環境を整える。Python 自体のインストール方法は扱わない。`python.org <https://www.python.org/downloads/>`_ のインストーラーなどで、Python 3.10 以降を用意してほしい。

作業用のフォルダーと仮想環境
----------------------------

プロジェクトごとに\ **仮想環境**\ （venv）を作り、ライブラリーをその中にインストールする。こうすると、ほかのプロジェクトとライブラリーのバージョンが衝突しない。PowerShell で次のように実行する。

.. code-block:: powershell
   :linenos:
   :caption: 仮想環境の作成と有効化

   mkdir breakout
   cd breakout
   py -m venv .venv
   .venv\Scripts\Activate.ps1

4 行目で仮想環境を有効にする。スクリプトの実行が禁止されているというエラーが出た場合は、``Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`` を実行して、自分で作成したスクリプトの実行を許可する。コマンドプロンプトでは、4 行目の代わりに ``.venv\Scripts\activate.bat`` を実行する。

仮想環境が有効な間は、``py`` コマンドで仮想環境の Python が起動する。

pygame-ce のインストール
------------------------

pygame-ce を pip でインストールし、付属のサンプルゲームを起動して動作を確認する。

.. code-block:: powershell
   :linenos:
   :caption: pygame-ce のインストールと動作確認

   py -m pip install pygame-ce
   py -m pygame.examples.aliens

ウィンドウが開いてゲームが動けば成功である。

pygame-ce はパッケージ名こそ ``pygame-ce`` だが、プログラムからは元の pygame と同じく ``import pygame`` で読み込む。そのため、元の ``pygame`` パッケージと同じ環境に入れると互いに上書きし合って正しく動かない。すでに ``pygame`` が入っている場合は、``py -m pip uninstall pygame`` で削除してから pygame-ce をインストールする。

エディター
----------

コードを書くエディターは使い慣れたものでよい。`Visual Studio Code <https://code.visualstudio.com/>`_ に Python 拡張機能を入れると、補完、デバッガー、型チェックが使えて便利である。pygame-ce は型ヒントの情報を同梱しているため、``pygame.Rect`` などの補完も効く。

コードの検査
------------

本書のサンプルコードは、スタイルを flake8、型を mypy で検査している。自分でコードを書く場合も、これらを使うと誤りに早く気付ける。

.. code-block:: powershell
   :linenos:
   :caption: 検査ツールのインストールと実行

   py -m pip install flake8 mypy
   py -m flake8
   py -m mypy .

設定は、検査するファイルと同じフォルダーに置いた ``setup.cfg`` に書く。本書のサンプルコードでは、行の長さを 120 文字まで許し、mypy を最も厳しい ``strict`` モードで動かしている。

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :linenos:
   :caption: examples/setup.cfg

バージョン管理
--------------

小さなゲームでも、最初から Git でバージョン管理をしておく。調整を重ねて「前の版のほうが面白かった」と感じたときに戻れるからである。ゲーム制作に特有の注意点として、画像や音声などの大きなバイナリーファイルの扱いがある。Git はテキストファイルの差分管理に向いており、大きなバイナリーファイルを何度も更新するとリポジトリーが急速に肥大化する。これを避けるには、:term:`Git LFS`\ （Large File Storage）を使い、バイナリーファイルの実体をリポジトリーの外に保存する。

.. code-block:: powershell
   :linenos:
   :caption: Git LFS で画像と音声を管理する設定

   git init
   git lfs install
   git lfs track "*.png" "*.wav" "*.ogg"
   git add .gitattributes

3 行目で、LFS で管理するファイルの種類を指定している。この設定は ``.gitattributes`` ファイルに記録されるので、4 行目でそれをコミットの対象に加える。

また、仮想環境やビルド結果はリポジトリーに含めないよう、``.gitignore`` に書いておく。

.. code-block:: text
   :linenos:
   :caption: .gitignore の例

   .venv/
   __pycache__/
   .mypy_cache/
   build/
   dist/

``build/`` と ``dist/`` は、:doc:`build`\ で使う PyInstaller が出力するフォルダーである。
