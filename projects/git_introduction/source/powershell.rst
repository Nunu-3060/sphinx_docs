PowerShell での実行例
=====================

Windows では、Git Bash のほかに PowerShell でも Git を使えます。``git`` コマンドの入力方法は Git Bash と同じですが、PowerShell 自体の文法やコマンドが bash と異なるため、いくつか注意すべき点があります。この付録では、その違いと PowerShell 版のサンプルスクリプトをまとめます。

本付録の内容は、Windows に標準で搭載されている Windows PowerShell 5.1 で動作を確認しています。PowerShell 7 以降では動作が異なる点は、その都度記載します。

プロンプトの表記
----------------

本資料では、PowerShell の実行例を次のように表記します。行頭の ``PS>`` はプロンプトを表しているため、入力する必要はありません。

.. code-block:: ps1con

   PS> git --version
   git version 2.40.0.windows.1

コマンドの対応
--------------

本資料の Git Bash の実行例で使っているコマンドのうち、PowerShell では入力が異なるものは次のとおりです。

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - 操作
     - Git Bash
     - PowerShell
   * - ファイルの内容を表示する
     - ``cat hello.py``
     - ``Get-Content hello.py``
   * - ディレクトリを削除する
     - ``rm -rf practice-basic``
     - ``Remove-Item -Recurse -Force practice-basic``
   * - 環境変数を設定する
     - ``export GIT_PAGER=cat``
     - ``$env:GIT_PAGER = 'cat'``
   * - 仮想環境を有効にする
     - ``source .venv/Scripts/activate``
     - ``.venv\Scripts\Activate.ps1``
   * - SSH の公開鍵をクリップボードにコピーする
     - ``cat ~/.ssh/id_ed25519.pub | clip``
     - ``Get-Content ~\.ssh\id_ed25519.pub | Set-Clipboard``

PowerShell では ``cat``、``ls``、``rm`` などが対応するコマンドの別名として定義されているため、単純な使い方であれば bash と同じように入力しても動作します。ただし、``rm -rf`` のようにオプションを付けた場合は動作しません。

``{}`` を含む引数は引用符で囲む
-------------------------------

PowerShell では ``{`` と ``}`` が特別な意味を持つため、``HEAD@{1}`` や ``stash@{0}`` のような引数は、そのままでは Git に正しく渡されず、エラーになります。このような引数は、``'``\ （単一引用符）で囲んでください。

.. code-block:: ps1con

   PS> git reset --hard 'HEAD@{1}'
   PS> git stash pop 'stash@{1}'

コミットメッセージに ``"`` を含めない
-------------------------------------

Windows PowerShell 5.1 では、``"``\ （二重引用符）を含む引数を ``git`` などの外部のコマンドに渡すと、引数が正しく渡されません。たとえば次のコマンドは、メッセージが途中で区切られてエラーになります。

.. code-block:: ps1con

   PS> git commit -m 'Say "hi"'
   error: pathspec 'hi' did not match any file(s) known to git

コミットメッセージに ``"`` を含めたい場合は、``-m`` を使わずにエディターでメッセージを入力してください。この問題は PowerShell 7.3 以降では解消されています。

リダイレクトで作成したファイルの文字コード
------------------------------------------

Windows PowerShell 5.1 では、``>`` や ``Out-File`` で作成したファイルの文字コードが、標準で UTF-16 になります。Git は UTF-16 の ``.gitignore`` を読み取れないため、次のように作成した ``.gitignore`` は効果がありません。また、UTF-16 のテキストファイルは Git からバイナリファイルとして扱われるため、``git diff`` で差分を確認できなくなります。

.. code-block:: ps1con

   PS> echo "*.log" > .gitignore

PowerShell でテキストファイルを作成する場合は、``-Encoding utf8`` を指定してください。Windows PowerShell 5.1 では BOM 付きの UTF-8 になりますが、Git や pip は BOM 付きの UTF-8 のファイルも正しく読み取れます。

.. code-block:: ps1con

   PS> "*.log" | Out-File -Encoding utf8 .gitignore
   PS> pip freeze | Out-File -Encoding utf8 requirements.txt

PowerShell 7 以降では、標準の文字コードが BOM なしの UTF-8 に変更されているため、この問題は起こりません。

スクリプトの実行ポリシー
------------------------

Windows の標準の設定では、PowerShell のスクリプト（拡張子が ``.ps1`` のファイル）の実行が禁止されています。サンプルスクリプトは、次のように実行ポリシーを一時的に変更して実行します。この方法では、PowerShell の設定は変更されません。

.. code-block:: ps1con

   PS> powershell -ExecutionPolicy Bypass -File .\basic_workflow.ps1

仮想環境を有効にする ``Activate.ps1`` もスクリプトであるため、同じ理由で実行できないことがあります。この場合は、次のコマンドで、現在のユーザーに対して、ローカルで作成したスクリプトと署名されたスクリプトの実行を許可してください。

.. code-block:: ps1con

   PS> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

.. _powershell-samples:

サンプルスクリプト（PowerShell 版）
-----------------------------------

各章のサンプルスクリプトの PowerShell 版です。動作は Git Bash 版と同じです。スクリプトの文字コードは BOM 付きの UTF-8 にしています。Windows PowerShell 5.1 は、BOM のない UTF-8 のスクリプトを、日本語版の Windows では Shift_JIS として読み込むため、日本語が文字化けして正しく実行できないためです。

基本操作
^^^^^^^^

:doc:`basic` のサンプルスクリプトの PowerShell 版です。

:download:`basic_workflow.ps1 をダウンロード <../examples/basic_workflow.ps1>`

.. literalinclude:: ../examples/basic_workflow.ps1
   :language: powershell
   :caption: basic_workflow.ps1

変更の取り消し
^^^^^^^^^^^^^^

:doc:`undo` のサンプルスクリプトの PowerShell 版です。

:download:`undo_demo.ps1 をダウンロード <../examples/undo_demo.ps1>`

.. literalinclude:: ../examples/undo_demo.ps1
   :language: powershell
   :caption: undo_demo.ps1

ブランチとマージ
^^^^^^^^^^^^^^^^

:doc:`branch` のサンプルスクリプトの PowerShell 版です。

:download:`branch_merge.ps1 をダウンロード <../examples/branch_merge.ps1>`

.. literalinclude:: ../examples/branch_merge.ps1
   :language: powershell
   :caption: branch_merge.ps1

コンフリクトの解消
^^^^^^^^^^^^^^^^^^

:doc:`branch` のコンフリクトのサンプルスクリプトの PowerShell 版です。

:download:`conflict_demo.ps1 をダウンロード <../examples/conflict_demo.ps1>`

.. literalinclude:: ../examples/conflict_demo.ps1
   :language: powershell
   :caption: conflict_demo.ps1
