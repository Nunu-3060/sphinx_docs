サンプルコード一覧
==========================================

本書で使ったサンプルコードの一覧である。ファイル名のリンクからダウンロードできる。各ファイルの内容と解説は、表の「掲載箇所」の章で閲覧できる。

実行の準備
------------------------------------------

Python のサンプルは、実際の LLM API の代わりに、応答を模擬するクライアント（``llm_stub.py``）を使う。そのため、API キーや外部のパッケージは不要で、Python 3.10 以上の標準ライブラリだけで実行できる。``llm_stub.py`` を各サンプルと同じディレクトリに置いて実行する。

.. code-block:: console
   :caption: サンプルの実行と静的解析
   :linenos:

   $ python ex03_tool_agent.py
   $ pip install flake8 mypy   # 静的解析を行う場合
   $ flake8 .
   $ mypy *.py

静的解析の設定は ``setup.cfg`` にある。flake8 は行の長さを 120 文字まで許容し、mypy は strict モードで検査する。

Python のサンプル
------------------------------------------

.. list-table:: Python のサンプル
   :header-rows: 1
   :widths: 34 44 22

   * - ファイル
     - 内容
     - 掲載箇所
   * - :download:`llm_stub.py <../examples/llm_stub.py>`
     - LLM を模擬するクライアント（各サンプルで共通に使う）
     - このページ
   * - :download:`ex01_prompt_template.py <../examples/ex01_prompt_template.py>`
     - プロンプトのテンプレート
     - :doc:`prompt_engineering`
   * - :download:`ex02_context_builder.py <../examples/ex02_context_builder.py>`
     - 予算内でのコンテキストの組み立て
     - :doc:`context_engineering`
   * - :download:`ex03_tool_agent.py <../examples/ex03_tool_agent.py>`
     - ツールを使う最小のエージェント
     - :doc:`harness_engineering`
   * - :download:`ex04_fix_loop.py <../examples/ex04_fix_loop.py>`
     - 自己修正のループ
     - :doc:`loop_engineering`
   * - :download:`ex05_simple_eval.py <../examples/ex05_simple_eval.py>`
     - プロンプトの比較評価
     - :doc:`eval_driven`
   * - :download:`ex06_orchestrator.py <../examples/ex06_orchestrator.py>`
     - オーケストレーター・ワーカー
     - :doc:`multi_agent`
   * - :download:`stop_hook_run_tests.py <../examples/stop_hook_run_tests.py>`
     - テストが成功するまで作業を続けさせる Claude Code の Stop フック
     - :doc:`practice_claude_code`
   * - :download:`setup.cfg <../examples/setup.cfg>`
     - flake8 と mypy の設定
     - このページ

設定ファイルと文書のサンプル
------------------------------------------

.. list-table:: 設定ファイルと文書のサンプル
   :header-rows: 1
   :widths: 34 44 22

   * - ファイル
     - 内容
     - 掲載箇所
   * - :download:`spec.sample.md <../examples/spec.sample.md>`
     - 仕様書の例
     - :doc:`spec_driven`
   * - :download:`CLAUDE.sample.md <../examples/CLAUDE.sample.md>`
     - ``CLAUDE.md`` の例
     - :doc:`practice_claude_code`
   * - :download:`SKILL.sample.md <../examples/SKILL.sample.md>`
     - スキルの例
     - :doc:`practice_claude_code`
   * - :download:`settings.sample.json <../examples/settings.sample.json>`
     - Claude Code の ``settings.json`` の例（権限とフック）
     - :doc:`practice_claude_code`
   * - :download:`agent.sample.md <../examples/agent.sample.md>`
     - サブエージェントの例
     - :doc:`practice_claude_code`

実際に使うときは、ファイル名を ``CLAUDE.md``、``.claude/skills/<スキル名>/SKILL.md``、``.claude/settings.json``、``.claude/agents/<名前>.md`` に変えて配置する。Stop フックのスクリプトは ``.claude/hooks/stop_hook_run_tests.py`` に置く。

llm_stub.py
------------------------------------------

各サンプルが共通に使う模擬クライアントである。``LLMClient``\ （45 〜 50 行目）は、サンプルが前提とするインターフェースである。``ScriptedLLM`` はあらかじめ用意した応答を順に返し、``RuleBasedLLM`` は入力に応じて応答を決める関数を使う。``estimate_tokens``\ （83 〜 91 行目）は、トークン数を簡易的に概算する。

.. literalinclude:: ../examples/llm_stub.py
   :language: python
   :caption: LLM を模擬するクライアント（llm_stub.py）
   :linenos:

実際の API に差し替えるには、``LLMClient`` と同じ ``complete`` メソッドを持つクラスを作る。:numref:`code-anthropic-adapter` は、Anthropic の Python SDK（``anthropic`` パッケージ）を使う例である。ツール呼び出しの変換は省略している。

.. _code-anthropic-adapter:

.. code-block:: python
   :caption: 実際の API を使うクライアントの例（ツール呼び出しの変換は省略）
   :linenos:

   from collections.abc import Sequence

   import anthropic

   from llm_stub import Message, Response


   class AnthropicLLM:
       def __init__(self, model: str = "claude-opus-5-5") -> None:
           self._client = anthropic.Anthropic()  # 環境変数 ANTHROPIC_API_KEY を使う
           self._model = model

       def complete(self, system: str, messages: Sequence[Message]) -> Response:
           result = self._client.messages.create(
               model=self._model,
               max_tokens=2048,
               system=system,
               messages=[{"role": m.role, "content": m.content} for m in messages if m.role != "tool"],
           )
           text = "".join(block.text for block in result.content if block.type == "text")
           return Response(text)

実際の API を使うと、利用料金がかかる。
