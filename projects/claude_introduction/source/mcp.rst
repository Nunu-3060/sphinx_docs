MCP によるツール連携
==========================================

MCP とは
------------------------------------------

:term:`MCP`\ （Model Context Protocol）は、AI アプリケーションと外部のツールやデータを接続するための標準規格です。Anthropic が提唱し、現在はオープンな仕様として多くの AI アプリケーションや開発ツールが対応しています。

:doc:`tool_use`\ で説明した方法では、ツールはアプリケーションごとに実装する必要があります。例えば、課題管理サービスと連携するツールを、チャットアプリケーション、IDE、社内ボットのそれぞれに別々に実装することになります。MCP では、ツールを MCP サーバーとして一度実装すれば、MCP に対応したどのアプリケーションからでも使えます。

構成要素
------------------------------------------

MCP は、ホスト、クライアント、サーバーの 3 つの役割で構成されます（:numref:`fig-mcp`）。

.. _fig-mcp:

.. graphviz::
   :caption: MCP の構成
   :align: center

   digraph mcp {
     rankdir=LR;
     compound=true;
     node [shape=box, style="rounded,filled", fillcolor="#EEF3FA", color="#4C78A8"];
     edge [color="#555555", fontsize=10];

     subgraph cluster_host {
       label="ホスト（Claude Code、デスクトップアプリなど）";
       style="rounded,dashed"; color="#888888";
       llm [label="Claude", shape=box3d, fillcolor="#E8F5E9", color="#2E7D32"];
       c1 [label="MCP クライアント"];
       c2 [label="MCP クライアント"];
       llm -> c1 [dir=both];
       llm -> c2 [dir=both];
     }

     s1 [label="MCP サーバー\n（課題管理）", fillcolor="#FFF4E5", color="#F58518"];
     s2 [label="MCP サーバー\n（社内データベース）", fillcolor="#FFF4E5", color="#F58518"];
     d1 [label="課題管理サービス", shape=cylinder, fillcolor="#FFFFFF"];
     d2 [label="データベース", shape=cylinder, fillcolor="#FFFFFF"];

     c1 -> s1 [label="stdio /\nHTTP", dir=both];
     c2 -> s2 [label="stdio /\nHTTP", dir=both];
     s1 -> d1;
     s2 -> d2;
   }

.. list-table:: MCP の役割
   :header-rows: 1
   :widths: 22 78

   * - 役割
     - 説明
   * - ホスト
     - 利用者が操作する AI アプリケーション。Claude Code、Claude のデスクトップアプリ、claude.ai などが該当します
   * - クライアント
     - ホストの中で動き、1 つのサーバーとの接続を管理します
   * - サーバー
     - ツールやデータを提供するプログラム。ローカルで動くものと、リモートで動くものがあります

サーバーが提供する機能
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

MCP サーバーは、主に次の 3 種類の機能を提供します。

.. list-table:: MCP サーバーが提供する機能
   :header-rows: 1
   :widths: 22 78

   * - 機能
     - 説明
   * - ツール
     - Claude が呼び出せる関数。:doc:`tool_use`\ のツールに相当します
   * - リソース
     - Claude に読ませるデータ。ファイル、データベースのレコード、API の応答など
   * - プロンプト
     - 定型的な作業のためのプロンプトの雛形。利用者が選んで呼び出します

通信方式
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

クライアントとサーバーの通信方式（トランスポート）には、主に次の 2 つがあります。

* **stdio**：ホストがサーバーを子プロセスとして起動し、標準入出力で通信します。ローカルのファイルやコマンドを扱うサーバーに向いています。
* **Streamable HTTP**：サーバーを Web サービスとして公開し、HTTP で通信します。複数の利用者で共有するリモートのサーバーに向いています。

MCP サーバーを使う
------------------------------------------

公式や各サービスの提供元が、多くの MCP サーバーを公開しています。まずは既存のサーバーを使ってみるのが、MCP を理解する近道です。

Claude Code では、``claude mcp add`` コマンドでサーバーを登録します。

.. code-block:: console
   :caption: Claude Code に MCP サーバーを登録する
   :linenos:

   # ローカルのサーバー（stdio）を登録する
   $ claude mcp add memo -- python /path/to/ex13_mcp_server.py

   # リモートのサーバー（HTTP）を登録する
   $ claude mcp add --transport http example https://mcp.example.com/mcp

   # 登録済みのサーバーを確認する
   $ claude mcp list

``--scope project`` を付けて登録すると、設定がプロジェクト直下の ``.mcp.json`` に保存され、リポジトリを通じてチームで共有できます。

API から MCP サーバーを使う
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Messages API の MCP コネクター（ベータ機能）を使うと、リモートの MCP サーバーのツールを API から直接使えます。ツールの呼び出しと結果の受け渡しは Anthropic のサーバーが行うため、アプリケーションでループを書く必要はありません。

.. code-block:: python
   :caption: MCP コネクターでリモートの MCP サーバーを使う
   :linenos:

   import os

   response = client.beta.messages.create(
       model="claude-opus-5-5",
       max_tokens=16000,
       betas=["mcp-client-2025-11-20"],
       mcp_servers=[
           {
               "type": "url",
               "url": "https://mcp.example.com/mcp",
               "name": "example",
               "authorization_token": os.environ["EXAMPLE_MCP_TOKEN"],
           },
       ],
       tools=[{"type": "mcp_toolset", "mcp_server_name": "example"}],
       messages=[{"role": "user", "content": "未完了の課題を一覧にして"}],
   )

``mcp_servers`` でサーバーへの接続方法を指定し（7 〜 14 行目）、``tools`` の ``mcp_toolset`` でそのサーバーのツールを使えるようにします（15 行目）。両方の指定が必要です。

MCP サーバーを作る
------------------------------------------

MCP の公式 Python SDK（``mcp`` パッケージ）を使うと、MCP サーバーを短いコードで作成できます。メモの追加と一覧を行うサーバーの例を示します。

.. literalinclude:: ../examples/ex13_mcp_server.py
   :language: python
   :caption: ex13_mcp_server.py
   :linenos:

``@server.tool()`` を付けた関数がツールとして、``@server.resource()`` を付けた関数がリソースとして公開されます。:doc:`tool_use`\ のツールランナーと同じく、型ヒントと docstring からツールの定義が生成されるため、docstring には Claude が読んで分かる説明を書いてください。

.. note::

   MCP の Python SDK は、バージョン 2 で API が変更されました。バージョン 1 の ``FastMCP`` クラスは ``MCPServer`` に名前が変わり、インポート元も ``mcp.server.mcpserver`` になっています。インターネット上の古い記事のコードを使う場合は注意してください。

作成したサーバーは、前節の ``claude mcp add`` で Claude Code に登録して動作を確認できます。登録するコマンドには、``mcp`` パッケージをインストールした仮想環境の Python を、``/path/to/.venv/bin/python`` のように絶対パスで指定してください。開発中は、MCP Inspector（``npx @modelcontextprotocol/inspector`` で起動するデバッグ用の Web ツール）を使うと、サーバーが公開するツールを直接呼び出して確かめられます。

セキュリティ上の注意
------------------------------------------

MCP サーバーは、Claude に外部のシステムを操作する能力を与えます。導入にあたっては次の点に注意してください。

* **提供元を確認する**：MCP サーバーは任意のコードを実行できます。信頼できる提供元のものだけを使い、ローカルで動かすサーバーはソースコードを確認します。
* **権限を最小限にする**：サーバーに渡す API トークンやデータベースの権限は、必要な範囲に限定します。読み取りだけで足りる用途には、読み取り専用の権限を使います。
* **外部の内容に含まれる指示に注意する**：Web ページ、メール、課題のコメントなど、サーバーが取得した内容に、Claude を誤った操作に誘導する文章が含まれていることがあります（:ref:`prompt-injection`\ 参照）。書き込みや送信を伴う操作は、実行前に人の承認を求める設定にします。
