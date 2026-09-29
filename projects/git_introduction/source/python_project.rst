Python プロジェクトでの Git の活用
==================================

この章では、Python のプロジェクトを Git で管理する際に注意すべき点を説明します。

管理するファイルと管理しないファイル
------------------------------------

リポジトリには、プロジェクトを再現するために必要なファイルだけをコミットします。実行時に自動で生成されるファイルや、各自の環境に依存するファイルは ``.gitignore`` で除外します。

.. list-table::
   :header-rows: 1
   :widths: 20 40 40

   * - 区分
     - 例
     - 理由
   * - 管理する
     - ソースコード（``*.py``）、テストコード、``pyproject.toml``、``requirements.txt``、``README.md``、``.gitignore``
     - プロジェクトの内容そのものであり、他の人が環境を再現するために必要です。
   * - 管理しない
     - ``__pycache__/``、``*.pyc``
     - Python が実行時に自動で生成するファイルです。
   * - 管理しない
     - ``.venv/`` などの仮想環境
     - OS や Python のバージョンに依存し、``requirements.txt`` などから再作成できます。
   * - 管理しない
     - ``build/``、``dist/``、``*.egg-info/``
     - パッケージのビルドで生成されるファイルです。
   * - 管理しない
     - ``.env``、認証情報を含む設定ファイル
     - パスワードや API キーなどの秘密情報が含まれます。

Python プロジェクト向けの ``.gitignore`` の例は :download:`python.gitignore <../examples/python.gitignore>` からダウンロードできます。GitHub でリポジトリを作成する際に「Add .gitignore」で「Python」を選ぶと、同様の ``.gitignore`` が自動で作成されます。

仮想環境と依存パッケージ
------------------------

仮想環境のディレクトリはコミットせず、依存パッケージの一覧をファイルとしてコミットします。他の人は、そのファイルから同じ環境を再作成できます。

.. code-block:: console

   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install requests
   $ pip freeze > requirements.txt
   $ git add requirements.txt
   $ git commit -m "Add requests to dependencies"

Windows の Git Bash では、仮想環境を有効にするコマンドは ``source .venv/Scripts/activate`` です。PowerShell では、次のように実行します。

.. code-block:: ps1con

   PS> python -m venv .venv
   PS> .venv\Scripts\Activate.ps1
   PS> pip install requests
   PS> pip freeze | Out-File -Encoding utf8 requirements.txt
   PS> git add requirements.txt
   PS> git commit -m "Add requests to dependencies"

Windows PowerShell 5.1 で ``pip freeze > requirements.txt`` のようにリダイレクトすると、ファイルが UTF-16 で作成され、Git で差分を確認できなくなります。そのため、上の例では ``Out-File -Encoding utf8`` を使っています。また、``Activate.ps1`` を実行できない場合は、実行ポリシーの設定が必要です。いずれも詳しくは :doc:`powershell` を参照してください。

リポジトリを複製した人は、次のように環境を再作成します。

.. code-block:: console

   $ python -m venv .venv
   $ source .venv/bin/activate
   $ pip install -r requirements.txt

秘密情報の扱い
--------------

パスワードや API キーなどの秘密情報は、ソースコードに直接書かず、環境変数や ``.env`` ファイルから読み込むようにします。``.env`` ファイルは ``.gitignore`` で除外し、必要な設定項目だけを記載した ``.env.example`` などのファイルをコミットしておくと、他の人が設定方法を理解しやすくなります。

.. warning::

   秘密情報を一度でもコミットしてしまった場合、後のコミットで削除しても、過去のコミットには残り続けます。特に、リモートリポジトリにプッシュした場合は、第三者に取得された可能性があります。この場合は、まず漏えいしたパスワードや API キーを無効化し、新しいものに交換してください。履歴から完全に削除するには ``git filter-repo`` などの専用のツールが必要ですが、履歴を書き換えるため、チームでの調整が必要になります。

Jupyter Notebook の扱い
-----------------------

Jupyter Notebook のファイル（``*.ipynb``）は JSON 形式で、コードのほかに実行結果や実行回数も保存されます。そのため、コードを変更していなくても、実行し直しただけで差分が発生します。

差分を小さく保つには、コミットする前に出力をクリアする方法があります。``nbstripout`` などのツールを使うと、コミット時に出力を自動で削除できます。

pre-commit によるコミット前のチェック
-------------------------------------

Git には、コミットやプッシュなどの操作の前後に、任意のスクリプトを自動で実行するフックという仕組みがあります。Python のプロジェクトでは、フックを簡単に管理できる `pre-commit <https://pre-commit.com/>`_ というツールがよく使われます。

pre-commit を使うと、コミットのたびにコードの静的解析や整形を自動で実行し、問題があればコミットを中止できます。設定は、リポジトリの最上位ディレクトリに置く ``.pre-commit-config.yaml`` に記述します。

.. literalinclude:: ../examples/pre-commit-config.yaml
   :language: yaml
   :caption: .pre-commit-config.yaml の例

:download:`pre-commit-config.yaml をダウンロード <../examples/pre-commit-config.yaml>`

ダウンロードしたファイルは、名前を ``.pre-commit-config.yaml`` に変更してから使います。設定ファイルを置いたら、次のコマンドでフックを有効にします。

.. code-block:: console

   $ pip install pre-commit
   $ pre-commit install

以降は、``git commit`` を実行するたびに設定したチェックが実行されます。すべてのファイルに対してチェックを実行したい場合は、``pre-commit run --all-files`` を実行します。
