基本操作
========

この章では、簡単な Python のスクリプトを例に、リポジトリの作成からコミット、履歴の確認までの基本操作を説明します。

この章の操作をまとめて実行するサンプルスクリプトは、:ref:`basic-sample` にあります。

リポジトリの作成
----------------

新しくリポジトリを作成するには、プロジェクトのディレクトリで ``git init`` を実行します。

.. code-block:: console

   $ mkdir hello-git
   $ cd hello-git
   $ git init
   Initialized empty Git repository in /home/taro/hello-git/.git/

``git init`` を実行すると ``.git`` ディレクトリが作成され、このディレクトリがリポジトリになります。``.git`` ディレクトリには履歴や設定がすべて保存されているため、手動で編集したり削除したりしないでください。

既に存在するリモートリポジトリを手元に複製する場合は、``git init`` ではなく ``git clone`` を使います。``git clone`` については :doc:`remote` で説明します。

状態の確認
----------

``git status`` は、ワーキングツリーとステージングエリアの状態を表示します。Git を使っていて迷ったときは、まず ``git status`` を実行して現在の状態を確認する習慣を付けましょう。

``hello.py`` を作成してから ``git status`` を実行すると、次のように表示されます。

.. code-block:: console

   $ git status
   On branch main

   No commits yet

   Untracked files:
     (use "git add <file>..." to include in what will be committed)
           hello.py

   nothing added to commit but untracked files present (use "git add" to track)

``Untracked files`` は、``hello.py`` がまだ Git の管理対象になっていない（未追跡である）ことを表しています。

``-s``\ （``--short``）オプションを付けると、状態を 1 行ずつ簡潔に表示できます。

.. code-block:: console

   $ git status -s
   ?? hello.py

簡潔な表示では、ファイル名の前に 2 文字の記号で状態が表示されます。左の文字がステージングエリアの状態、右の文字がワーキングツリーの状態を表します。

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - 表示
     - 意味
   * - ``??``
     - 未追跡のファイル
   * - ``A``\ （左）
     - 新しく追加され、ステージされたファイル
   * - ``M``\ （左）
     - 変更がステージされたファイル
   * - ``M``\ （右）
     - 変更されているが、ステージされていないファイル
   * - ``D``
     - 削除されたファイル

変更のステージ
--------------

``git add`` で、変更をステージングエリアに追加します。

.. code-block:: console

   $ git add hello.py
   $ git status -s
   A  hello.py

``git add`` には、ファイル名のほかにディレクトリも指定できます。よく使う指定方法は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - コマンド
     - 説明
   * - ``git add hello.py``
     - 指定したファイルの変更をステージします。
   * - ``git add src/``
     - 指定したディレクトリ以下の変更をすべてステージします。
   * - ``git add .``
     - カレントディレクトリ以下の変更をすべてステージします。
   * - ``git add -p``
     - 変更を部分（ハンク）ごとに表示し、ステージするかどうかを 1 つずつ選びます。

``git add .`` は便利ですが、意図しないファイルまでステージしてしまうことがあります。実行後は ``git status`` で、ステージされたファイルを確認してください。

コミット
--------

``git commit`` で、ステージングエリアの内容をリポジトリに記録します。``-m`` オプションでコミットメッセージを指定します。

.. code-block:: console

   $ git commit -m "Add greeting script"
   [main (root-commit) b71dd7d] Add greeting script
    1 file changed, 6 insertions(+)
    create mode 100644 hello.py

``-m`` を省略すると、``core.editor`` で設定したエディターが起動し、コミットメッセージを入力できます。複数行のメッセージを書く場合はエディターを使うと便利です。

管理対象のファイルの変更だけをコミットする場合は、``-a`` オプションで ``git add`` を省略できます。ただし、``-a`` では未追跡のファイルはコミットされません。

.. code-block:: console

   $ git commit -a -m "Fix typo"

コミットメッセージの書き方
^^^^^^^^^^^^^^^^^^^^^^^^^^

コミットメッセージは、後から履歴を読む人（未来の自分を含む）のために書きます。一般に、次のような書き方が推奨されています。

* 1 行目に、変更内容の要約を 50 文字程度で書きます。
* 詳しい説明が必要な場合は、2 行目を空行にして、3 行目以降に書きます。
* 「何を変更したか」だけでなく、「なぜ変更したか」を書きます。

.. code-block:: text

   Fix division by zero in average()

   average() raised ZeroDivisionError when the input list was empty.
   Return 0.0 for an empty list instead.

コミットメッセージを英語と日本語のどちらで書くかは、チームで統一しておきましょう。

コミットの単位
^^^^^^^^^^^^^^

1 つのコミットには、1 つの目的の変更だけを含めるようにします。たとえば「バグの修正」と「コードの整形」は別のコミットに分けます。コミットの単位が小さく目的が明確であれば、履歴を読みやすくなり、問題のある変更だけを取り消すことも簡単になります。

履歴の確認
----------

``git log`` で、コミットの履歴を新しい順に表示します。

.. code-block:: console

   $ git log
   commit b1df4590c2e3a7f8d6b5e4c3a2f1e0d9c8b7a6f5 (HEAD -> main)
   Author: Taro Yamada <taro@example.com>
   Date:   Sun Sep 27 10:00:00 2026 +0900

       Change greeting from Hello to Hi

   commit b71dd7d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9
   Author: Taro Yamada <taro@example.com>
   Date:   Sun Sep 27 09:50:00 2026 +0900

       Add greeting script

履歴が長い場合は、ページャーで表示されます。矢印キーでスクロールし、``q`` キーで終了します。

``git log`` には多くのオプションがあります。よく使うものは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - コマンド
     - 説明
   * - ``git log --oneline``
     - 1 つのコミットを 1 行で簡潔に表示します。
   * - ``git log --graph --all``
     - すべてのブランチの履歴を、分岐と合流が分かるグラフで表示します。
   * - ``git log -p``
     - 各コミットでの変更内容（差分）も表示します。
   * - ``git log -n 5``
     - 新しい順に 5 件だけ表示します。
   * - ``git log -- hello.py``
     - 指定したファイルを変更したコミットだけを表示します。

特定のコミットの詳細は ``git show`` で表示できます。コミット ID を省略すると、最新のコミットが表示されます。

.. code-block:: console

   $ git show b71dd7d

差分の確認
----------

``git diff`` で、変更内容を確認します。比較の対象によって、次のように使い分けます。

.. list-table::
   :header-rows: 1
   :widths: 35 65

   * - コマンド
     - 比較の対象
   * - ``git diff``
     - ワーキングツリーとステージングエリア（まだステージしていない変更）
   * - ``git diff --staged``
     - ステージングエリアと最新のコミット（次にコミットされる変更）
   * - ``git diff HEAD``
     - ワーキングツリーと最新のコミット（ステージの有無にかかわらず、すべての変更）
   * - ``git diff <commit1> <commit2>``
     - 2 つのコミットの間の変更

``git diff`` の出力では、削除された行が ``-``、追加された行が ``+`` で表されます。

.. code-block:: console

   $ git diff
   diff --git a/hello.py b/hello.py
   index 620c2ef..12f16d1 100644
   --- a/hello.py
   +++ b/hello.py
   @@ -1,5 +1,5 @@
    def greet(name):
   -    return f"Hello, {name}!"
   +    return f"Hi, {name}!"

コミットする前に ``git diff --staged`` で、次のコミットに含まれる変更を確認する習慣を付けると、意図しない変更をコミットしてしまうことを防げます。

ファイルの削除と移動
--------------------

管理対象のファイルを削除する場合や、名前を変更する場合は、次のコマンドを使います。どちらのコマンドも、ワーキングツリーでの操作とステージを同時に行います。

.. code-block:: console

   $ git rm old.py
   $ git mv utils.py helpers.py

``git rm --cached`` を使うと、ワーキングツリーのファイルは残したまま、Git の管理対象からだけ外せます。誤ってコミットしたファイルを管理対象から外したい場合に使います。

.. code-block:: console

   $ git rm --cached secret.txt

管理対象から除外するファイルの指定
----------------------------------

仮想環境のディレクトリや、実行時に生成されるキャッシュファイルなどは、リポジトリに含めるべきではありません。このようなファイルは ``.gitignore`` というファイルに記述すると、Git の管理対象から除外できます。``.gitignore`` はリポジトリの最上位ディレクトリに置き、``.gitignore`` 自体もコミットしてチームで共有します。

``.gitignore`` の主な書き方は次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - 記述例
     - 意味
   * - ``*.log``
     - 拡張子が ``.log`` のファイルをすべて除外します。
   * - ``__pycache__/``
     - ``__pycache__`` という名前のディレクトリをすべて除外します。
   * - ``/config.ini``
     - 最上位ディレクトリにある ``config.ini`` だけを除外します。
   * - ``!important.log``
     - それより前の行で除外したファイルのうち、``important.log`` だけは除外しません。
   * - ``# コメント``
     - ``#`` で始まる行はコメントとして扱われます。

``.gitignore`` は、まだ管理対象になっていないファイルにだけ効果があります。既にコミットしたファイルを除外したい場合は、``.gitignore`` に追加したうえで ``git rm --cached`` を実行して管理対象から外します。

PowerShell で ``.gitignore`` を作成する場合は、文字コードに注意が必要です。詳しくは :doc:`powershell` を参照してください。

Python プロジェクト向けの ``.gitignore`` の例は :download:`python.gitignore <../examples/python.gitignore>` からダウンロードできます。管理すべきファイルの考え方は :doc:`python_project` で説明します。

.. _basic-sample:

サンプルスクリプト
------------------

この章で説明した操作を順に実行するサンプルスクリプトです。Git Bash などで ``bash basic_workflow.sh`` を実行すると、``practice-basic`` というディレクトリを作成して操作を行います。PowerShell 版の内容は :ref:`powershell-samples` で確認できます。

* :download:`basic_workflow.sh をダウンロード <../examples/basic_workflow.sh>`
* :download:`basic_workflow.ps1（PowerShell 版）をダウンロード <../examples/basic_workflow.ps1>`

.. literalinclude:: ../examples/basic_workflow.sh
   :language: bash
   :caption: basic_workflow.sh
