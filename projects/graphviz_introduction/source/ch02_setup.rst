環境構築
========

Graphviz を Python から使うには、次の 2 つが必要です。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - ソフトウェア
     - 役割
   * - Graphviz 本体
     - DOT 言語のテキストを読み込み、図を配置して画像に出力するコマンド群です。``dot`` コマンドなどが含まれます。
   * - Python の graphviz パッケージ
     - Python から DOT 言語のテキストを組み立て、Graphviz 本体のコマンドを呼び出すライブラリです。

graphviz パッケージは Graphviz 本体を内蔵していません。画像を出力する際には、内部で Graphviz 本体の ``dot`` コマンドを実行します。そのため、パッケージだけをインストールしても画像は出力できず、Graphviz 本体のインストールと PATH の設定が必要です。

Graphviz 本体のインストール
---------------------------

ここでは Windows の場合を説明します。次のどちらかの方法でインストールします。

公式のインストーラーを使う
^^^^^^^^^^^^^^^^^^^^^^^^^^

`Graphviz の公式サイトのダウンロードページ <https://graphviz.org/download/>`_ から、Windows 用のインストーラーをダウンロードして実行します。インストールの途中で PATH に関する選択肢が表示されたら、「Add Graphviz to the system PATH for all users」または「Add Graphviz to the system PATH for current user」を選びます。既定の「Do not add Graphviz to the system PATH」のまま進めると、PATH が設定されません。

winget を使う
^^^^^^^^^^^^^

Windows のパッケージマネージャーである winget を使う場合は、次のコマンドを実行します。

.. code-block:: console

   > winget install Graphviz.Graphviz

winget でインストールした場合、PATH が自動的には設定されないことがあります。その場合は次の節の手順で PATH を設定してください。

macOS と Linux の場合
^^^^^^^^^^^^^^^^^^^^^

macOS では Homebrew の ``brew install graphviz`` で、Debian 系の Linux では ``sudo apt install graphviz`` でインストールできます。いずれも PATH は自動的に設定されます。

PATH の設定
-----------

Windows で ``dot`` コマンドが見つからない場合は、Graphviz の ``bin`` フォルダーを環境変数 PATH に追加します。既定のインストール先は ``C:\Program Files\Graphviz\bin`` です。

#. スタートメニューで「環境変数」と入力し、「環境変数を編集」を開きます。
#. ユーザー環境変数の「Path」を選び、「編集」をクリックします。
#. 「新規」をクリックし、``C:\Program Files\Graphviz\bin`` を入力して「OK」をクリックします。
#. 開いているコマンドプロンプトやエディターをいったん閉じ、起動し直します。PATH の変更は、変更後に起動したプログラムにだけ反映されます。

インストールの確認
------------------

コマンドプロンプトで次のコマンドを実行し、バージョンが表示されればインストールは完了です。表示されるバージョンは、インストールした時期によって異なります。

.. code-block:: console

   > dot -V
   dot - graphviz version 16.1.0 (20260904.0139)

「'dot' は、内部コマンドまたは外部コマンド、操作可能なプログラムまたはバッチ ファイルとして認識されていません。」と表示される場合は、PATH が正しく設定されていません。前の節の手順を確認してください。

graphviz パッケージのインストール
---------------------------------

Python の graphviz パッケージは pip でインストールします。

.. code-block:: console

   > pip install graphviz

インストールできたことは、次のようにバージョンを表示して確認できます。

.. code-block:: console

   > python -c "import graphviz; print(graphviz.__version__)"
   0.21

似た名前のパッケージに pygraphviz と pydot があります。pygraphviz は Graphviz の C 言語のライブラリを直接呼び出すパッケージで、インストール時にコンパイルが必要になることがあります。pydot は DOT の読み書きに重点を置いたパッケージです。本資料では、インストールが簡単で、DOT 言語との対応がわかりやすい graphviz パッケージを使用します。

エディターの準備
----------------

DOT ファイルは普通のテキストファイルなので、どのエディターでも編集できます。拡張子は ``.dot`` または ``.gv`` が一般的です。本資料のサンプルでは ``.dot`` を使用します。

Visual Studio Code を使う場合は、「Graphviz Interactive Preview」などの拡張機能を入れると、DOT ファイルを編集しながら図をプレビューできます。図の配置を試行錯誤するときに便利です。
