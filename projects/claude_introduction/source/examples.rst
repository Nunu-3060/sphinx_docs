サンプルコード一覧
==========================================

本書で使用したサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。各ファイルの内容は、表の「掲載箇所」の章で、解説とともに閲覧できます。

実行の準備
------------------------------------------

#. Python 3.10 以上をインストールします。
#. 下の表の ``requirements.txt`` をダウンロードし、仮想環境を作成して依存パッケージをインストールします。
#. 環境変数 ``ANTHROPIC_API_KEY`` に API キーを設定します（:doc:`api_basics`\ 参照）。
#. 使用するモデルを変える場合は、環境変数 ``CLAUDE_MODEL`` にモデル ID を設定します。設定しない場合は ``claude-opus-5-5`` を使います。

.. code-block:: console
   :caption: 依存パッケージのインストールと静的解析
   :linenos:

   $ python -m venv .venv
   $ source .venv/bin/activate      # Windows では .venv\Scripts\activate
   $ pip install -r requirements.txt
   $ flake8 *.py
   $ mypy *.py

API を呼び出すサンプルを実行すると、API の利用料金がかかります。

Python のサンプル
------------------------------------------

.. list-table:: Python のサンプル
   :header-rows: 1
   :widths: 34 44 22

   * - ファイル
     - 内容
     - 掲載箇所
   * - :download:`ex01_hello_claude.py <../examples/ex01_hello_claude.py>`
     - 最小構成のメッセージ送信
     - :doc:`api_basics`
   * - :download:`ex02_system_prompt.py <../examples/ex02_system_prompt.py>`
     - システムプロンプトの有無による応答の比較
     - :doc:`api_basics`
   * - :download:`ex03_multi_turn.py <../examples/ex03_multi_turn.py>`
     - 会話履歴を保持した複数ターンの対話
     - :doc:`api_basics`
   * - :download:`ex04_streaming.py <../examples/ex04_streaming.py>`
     - ストリーミングによる逐次表示
     - :doc:`api_basics`
   * - :download:`ex05_error_handling.py <../examples/ex05_error_handling.py>`
     - 例外処理と stop_reason の確認
     - :doc:`api_basics`
   * - :download:`ex06_count_tokens.py <../examples/ex06_count_tokens.py>`
     - トークン数の計測と料金の概算
     - :doc:`api_basics`
   * - :download:`ex07_structured_output.py <../examples/ex07_structured_output.py>`
     - 構造化出力による情報の抽出
     - :doc:`api_advanced`
   * - :download:`ex08_vision.py <../examples/ex08_vision.py>`
     - 画像の入力
     - :doc:`api_advanced`
   * - :download:`ex09_prompt_caching.py <../examples/ex09_prompt_caching.py>`
     - プロンプトキャッシュ
     - :doc:`api_advanced`
   * - :download:`ex10_batch.py <../examples/ex10_batch.py>`
     - Message Batches API によるバッチ処理
     - :doc:`api_advanced`
   * - :download:`ex11_tool_use_manual.py <../examples/ex11_tool_use_manual.py>`
     - ツール利用のループの自作
     - :doc:`tool_use`
   * - :download:`ex12_tool_runner.py <../examples/ex12_tool_runner.py>`
     - ツールランナーによるツール利用
     - :doc:`tool_use`
   * - :download:`ex13_mcp_server.py <../examples/ex13_mcp_server.py>`
     - 最小構成の MCP サーバー
     - :doc:`mcp`
   * - :download:`ex14_simple_eval.py <../examples/ex14_simple_eval.py>`
     - 分類プロンプトの評価
     - :doc:`operations`
   * - :download:`ex15_agent_sdk.py <../examples/ex15_agent_sdk.py>`
     - Claude Agent SDK によるコードベースの調査
     - :doc:`agents`

Claude Code の設定例
------------------------------------------

実際に使う際は、表の「配置先」のファイル名に変更してください。

.. list-table:: Claude Code の設定例
   :header-rows: 1
   :widths: 34 44 22

   * - ファイル
     - 配置先
     - 掲載箇所
   * - :download:`CLAUDE.sample.md <../examples/CLAUDE.sample.md>`
     - プロジェクト直下の ``CLAUDE.md``
     - :doc:`claude_code`
   * - :download:`settings.sample.json <../examples/settings.sample.json>`
     - ``.claude/settings.json``
     - :doc:`claude_code`
   * - :download:`SKILL.sample.md <../examples/SKILL.sample.md>`
     - ``.claude/skills/release-notes/SKILL.md``
     - :doc:`claude_code`
   * - :download:`agent.sample.md <../examples/agent.sample.md>`
     - ``.claude/agents/code-reviewer.md``
     - :doc:`claude_code`

環境設定ファイル
------------------------------------------

.. literalinclude:: ../examples/requirements.txt
   :language: text
   :caption: :download:`requirements.txt <../examples/requirements.txt>`
   :linenos:

.. literalinclude:: ../examples/setup.cfg
   :language: ini
   :caption: :download:`setup.cfg <../examples/setup.cfg>`\ （flake8 と mypy の設定）
   :linenos:
