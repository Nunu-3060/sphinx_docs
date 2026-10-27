実践：Claude Code
==========================================

本章では、Anthropic のコーディングエージェントである Claude Code を題材に、これまでの章で説明した手法を実際に適用する方法を示す。Claude Code の機能は頻繁に更新されるため、詳細は公式文書 :ref:`[ClaudeCode-Docs] <ref-claudecode-docs>` で確認してほしい。本章の内容は、2026 年 10 月時点の情報に基づく。

Claude Code の概要
------------------------------------------

Claude Code は、利用者が自然言語で依頼すると、ソースコードを読み、コマンドを実行し、ファイルを編集しながら作業を進めるエージェントである。ターミナル、VS Code や JetBrains 系の IDE、デスクトップアプリ、Web ブラウザから使える。作業したいプロジェクトのディレクトリで ``claude`` コマンドを実行すると、対話画面が始まる。

Claude Code の主な機能を、本書の 4 つの層に対応付けると\ :numref:`table-claude-code-layers` のようになる。

.. _table-claude-code-layers:

.. list-table:: Claude Code の機能と本書の各層の対応
   :header-rows: 1
   :widths: 30 70

   * - 層
     - Claude Code の機能
   * - プロンプト
     - 依頼の文面
   * - コンテキスト
     - ``CLAUDE.md``、``@`` によるファイルの参照、スキル、``/clear``、``/compact``、``/context``、サブエージェント
   * - ハーネス
     - 権限の設定、フック、サンドボックス、MCP サーバー、``settings.json``
   * - ループ
     - 計画モード（計画の承認）、Stop フック、``/goal``、``/loop``、``claude -p`` による非対話の実行、GitHub Actions

本章では、注文管理の Web API（Python、FastAPI）を開発する架空のプロジェクトを例に、これらを順に設定していく。

コンテキストを整える
------------------------------------------

CLAUDE.md
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``CLAUDE.md`` は Claude Code の規約ファイルであり、セッションの開始時に自動的に読み込まれる :ref:`[ClaudeCode-Memory] <ref-claudecode-memory>`。

.. list-table:: CLAUDE.md の主な置き場所
   :header-rows: 1
   :widths: 35 65

   * - 場所
     - 用途
   * - プロジェクト直下の ``CLAUDE.md``
     - プロジェクト固有の情報。リポジトリに含めてチームで共有する
   * - サブディレクトリの ``CLAUDE.md``
     - そのディレクトリ配下で作業するときにだけ必要な情報
   * - ``~/.claude/CLAUDE.md``
     - すべてのプロジェクトに共通する個人の好み

``/init`` コマンドを実行すると、Claude Code がプロジェクトを調査して ``CLAUDE.md`` の雛形を作る。雛形をもとに、:doc:`context_engineering`\ で述べた「コードを読むだけでは分からないこと」を追記していく。:numref:`code-claude-md` は記述の例である。

.. _code-claude-md:

.. literalinclude:: ../examples/CLAUDE.sample.md
   :language: markdown
   :caption: CLAUDE.md の例（CLAUDE.sample.md）
   :linenos:

規約には理由を添え（15 行目では、金額に ``Decimal`` を使う規則）、作業の進め方（19 〜 21 行目）と、してはいけないこと（25 〜 26 行目）を明示している。21 行目の「仕様と実装が食い違ったら報告する」は、:doc:`spec_driven`\ で述べた仕様と実装の同期のための指示である。

コンテキストの管理
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: コンテキストの管理に使うコマンド
   :header-rows: 1
   :widths: 25 75

   * - コマンド
     - 内容
   * - ``/context``
     - 現在のコンテキストの使用状況を、要素ごとに表示する
   * - ``/clear``
     - 会話の履歴を消去し、新しい会話を始める。別の作業に移るときに使う
   * - ``/compact``
     - これまでの会話を要約して、コンテキストを空ける。作業を続けたまま整理したいときに使う
   * - ``/memory``
     - ``CLAUDE.md`` を編集する
   * - ``/rewind``
     - 会話やファイルの変更を、過去の時点に巻き戻す

:doc:`context_engineering`\ で述べたとおり、最も効果的なのは作業ごとに ``/clear`` で会話を分けることである。また、AI が誤った前提で作業を重ねてしまったときは、誤りを指摘し続けるより、``/rewind`` で誤る前の時点に戻すか、``/clear`` でやり直すほうが早い。

スキル
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:term:`スキル`\ は、特定の作業の手順や知識をまとめたものである :ref:`[ClaudeCode-Skills] <ref-claudecode-skills>`。``.claude/skills/<スキル名>/SKILL.md`` に置くと、Claude は関連する作業を頼まれたときにスキルを読み込み、その手順に従う。``/<スキル名>`` で明示的に呼び出すこともできる。

.. literalinclude:: ../examples/SKILL.sample.md
   :language: markdown
   :caption: スキルの例（SKILL.sample.md）
   :linenos:

先頭の ``name`` と ``description``\ （2 〜 3 行目）は常に Claude に示され、Claude はこの説明を見てスキルを使うかどうかを判断する。本文は使うときにだけ読み込まれる。:doc:`context_engineering`\ で述べた「情報を段階的に見せる」方法であり、多くのスキルを用意してもコンテキストを圧迫しない。毎回必要な情報は ``CLAUDE.md`` に、特定の作業のときだけ必要な手順はスキルに書く、と使い分ける。

依頼の進め方
------------------------------------------

Claude Code に大きな作業を任せるときは、「調査 → 計画 → 実装 → 検証 → コミット」の順に進める :ref:`[ClaudeCode-BestPractices] <ref-claudecode-bestpractices>`。

計画の段階では\ :term:`計画モード`\ を使う。計画モードでは、Claude はファイルを変更せずに調査と計画だけを行う。Shift + Tab キーで権限モードを切り替えるか、``/plan`` コマンドで計画モードに入る。計画を確認して合意したら、通常のモードに戻して実装を依頼する。これは\ :doc:`loop_engineering`\ で述べた「計画の承認」の時点で人間が関与する方法である。

.. code-block:: text
   :caption: 計画モードでの依頼の例
   :linenos:

   /plan docs/specs/order-cancel.md の仕様を実装したい。
   関係する既存のコードを調べ、仕様書の「実装計画」のタスク T1 〜 T4 それぞれについて、
   変更するファイルと変更内容を示して。不明な点があれば質問して。

計画に合意したら、タスクを 1 つずつ依頼する。

.. code-block:: text
   :caption: 実装の依頼の例
   :linenos:

   計画どおり T2 を実装して。受け入れ条件 4 と 5 に対応するテストも追加し、
   python -m pytest -q と mypy src が成功するまで修正すること。既存のテストは変更しないこと。
   終わったら、変更したファイル、確認したこと、未確認のことを報告して。

1 行目で対象と範囲を、2 行目で完了条件を、3 行目で報告の形式を示している。:doc:`prompt_engineering`\ で述べた要素がそろっていることを確認してほしい。

ハーネスを整える
------------------------------------------

権限モード
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Claude Code が利用者の許可なしにどこまで操作してよいかは、:term:`権限モード`\ で切り替える :ref:`[ClaudeCode-Permissions] <ref-claudecode-permissions>`。

.. list-table:: 主な権限モード
   :header-rows: 1
   :widths: 25 75

   * - モード
     - 内容
   * - ``default``
     - ファイルの編集やコマンドの実行のたびに許可を求める
   * - ``acceptEdits``
     - ファイルの編集は許可なしで行い、コマンドの実行には許可を求める
   * - ``plan``
     - 調査と計画だけを行い、ファイルの変更や、変更を伴うコマンドの実行はしない
   * - ``auto``
     - 安全と判断された操作は自動で実行し、危険の可能性がある操作は止める
   * - ``dontAsk``
     - 設定ファイルで事前に許可した操作だけを実行し、それ以外は確認せずに拒否する。無人で動かす自動化向けである
   * - ``bypassPermissions``
     - ほぼすべての操作を許可なしで実行する。コンテナや仮想マシンなどの隔離された環境以外では使わない

権限の設定とフック
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

権限の規則とフックは ``settings.json`` に書く :ref:`[ClaudeCode-Settings] <ref-claudecode-settings>`。プロジェクトの ``.claude/settings.json`` に書けばチームで共有でき、``.claude/settings.local.json`` に書けば自分だけに適用される。

.. _code-settings:

.. literalinclude:: ../examples/settings.sample.json
   :language: json
   :caption: settings.json の例（settings.sample.json）
   :linenos:

* ``permissions`` の ``allow``\ （3 〜 10 行目）には許可なしで実行してよい操作を、``deny``\ （11 〜 15 行目）には禁止する操作を書く。この例では、テスト、静的解析、差分の確認を許可し、秘密情報の読み取りと ``git push`` を禁止している。
* ``hooks`` の ``PostToolUse``\ （18 〜 28 行目）は、ファイルを編集するたびに flake8 を実行するフックである。コマンドが終了コード 2 で終わると、標準エラー出力の内容が Claude に伝えられる。flake8 が違反を検出すると終了コード 2 を返すようにしているため（24 行目）、Claude は違反の内容を読んで修正する。
* ``Stop``\ （29 〜 38 行目）は、後述するループのためのフックである。

フックには、ほかにも次のような種類がある :ref:`[ClaudeCode-Hooks] <ref-claudecode-hooks>`。

.. list-table:: 主なフックの種類
   :header-rows: 1
   :widths: 28 72

   * - 種類
     - 実行される時点
   * - ``PreToolUse``
     - ツールを使う直前。ツールの使用を止めることもできる
   * - ``PostToolUse``
     - ツールを使った直後。整形ツールや静的解析の実行に使う
   * - ``UserPromptSubmit``
     - 利用者が依頼を送信したとき
   * - ``Stop``
     - Claude が応答を終えようとしたとき。作業を続けさせることもできる
   * - ``SubagentStop``
     - サブエージェントが応答を終えようとしたとき
   * - ``SessionStart``
     - セッションを開始したとき

``CLAUDE.md`` に書いた指示は Claude が判断して従うものだが、フックは必ず実行される。:doc:`harness_engineering`\ で述べたとおり、例外なく守らせたい規則はフックで実現する。

MCP サーバーとサンドボックス
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

MCP サーバーを登録すると、課題管理サービスやデータベース、ブラウザなどを Claude Code から操作できる :ref:`[ClaudeCode-MCP] <ref-claudecode-mcp>`。例えば課題管理サービスの MCP サーバーを登録すれば、「課題 123 の内容を読んで仕様書の案を作って」のような依頼ができる。

また、``/sandbox`` コマンドでサンドボックスを有効にすると、Claude が実行するコマンドのファイルシステムやネットワークへのアクセスを制限できる（対応している環境のみ）。

ループを組む
------------------------------------------

Stop フックによる自己修正のループ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:numref:`code-settings` の ``Stop`` フックは、Claude が作業を終えようとしたときに\ :numref:`code-stop-hook` のスクリプトを実行する。

.. _code-stop-hook:

.. literalinclude:: ../examples/stop_hook_run_tests.py
   :language: python
   :caption: テストが成功するまで作業を続けさせる Stop フック（stop_hook_run_tests.py）
   :linenos:

スクリプトは pytest を実行し（23 〜 29 行目）、失敗したテストがあれば ``{"decision": "block", "reason": ...}`` を出力する（34 〜 38 行目）。``decision`` が ``block`` のとき、Claude は終了せず、``reason`` の内容を読んで作業を続ける。つまり、「テストがすべて成功するまで終わらない」という完了条件を、Claude の判断に任せず、仕組みとして強制している。

ただし、:doc:`loop_engineering`\ で述べたとおり、ループには終了条件が必要である。テストがいつまでも成功しない場合に備え、このスクリプトは、フックによってすでに作業を続けている状態（``stop_hook_active`` が真）では終了を止めない（20 〜 21 行目）。これにより、フックによる差し戻しは 1 回までになる。より多く差し戻したい場合は、回数をファイルに記録するなどして上限を設ける。

``/goal`` と ``/loop``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

フックの設定を書かずに、同様のループを手軽に作る方法もある。

* ``/goal`` コマンドに条件を与えると、Claude はその条件を満たすまで、ターンをまたいで作業を続ける。例えば ``/goal python -m pytest -q がすべて成功する``\ のように使う。
* ``/loop`` コマンドは、指示を一定の間隔で繰り返し実行する。例えば ``/loop 5m デプロイが完了したか確認して``\ のように、外部の状態の監視に使う。

非対話の実行と CI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``-p`` オプションを付けると、Claude Code を対話画面なしで実行し、結果を標準出力に出力できる :ref:`[ClaudeCode-Headless] <ref-claudecode-headless>`。シェルスクリプトや CI に組み込めるため、:doc:`loop_engineering`\ で述べた外側のループを自動化できる。

.. code-block:: console
   :caption: 非対話の実行の例
   :linenos:

   $ # 結果を JSON で受け取り、jq で処理する
   $ claude -p "直近のコミットの変更点を要約して" --output-format json | jq -r .result

   $ # 許可するツールと、反復・費用の上限を指定して実行する
   $ claude -p "tests/ の失敗しているテストを直して" \
       --allowedTools "Read,Edit,Bash(python -m pytest *)" \
       --max-turns 30 --max-budget-usd 5

7 行目の ``--max-turns`` と ``--max-budget-usd`` は、それぞれ反復の回数と費用の上限を指定する。無人で動かす場合は、:doc:`loop_engineering`\ で述べたとおり、必ずこうした上限を設ける。

GitHub Actions と連携すると、プルリクエストや課題のコメントで Claude に依頼し、レビューや修正を任せることもできる :ref:`[ClaudeCode-GitHubActions] <ref-claudecode-githubactions>`。

マルチエージェントを使う
------------------------------------------

サブエージェント
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Claude Code は、作業の一部を\ :term:`サブエージェント`\ に任せられる :ref:`[ClaudeCode-Subagents] <ref-claudecode-subagents>`。サブエージェントはメインの会話とは別のコンテキストで作業し、結果だけを返す。独自のサブエージェントは ``.claude/agents/<名前>.md`` に定義する。

.. literalinclude:: ../examples/agent.sample.md
   :language: markdown
   :caption: サブエージェントの例（agent.sample.md）
   :linenos:

この例は、実装が仕様書を満たしているかを確認するレビュー担当である。``tools``\ （4 行目）で ``Edit`` や ``Write`` を与えず、本文（13 行目）でも編集しないよう指示している。ただし、``Bash`` を与えているため、コマンドによる変更は技術的には可能である。厳密に禁止したい場合は、権限の設定で禁止する。``model``\ （5 行目）では、作業に応じたモデルを指定できる。:doc:`multi_agent`\ で述べた「専門化」と「相互の検証」の例である。

並列の作業
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* ``claude --worktree <名前>``\ （または ``-w``）で起動すると、Git の worktree を作り、隔離された作業場所で Claude Code を動かせる。複数の Claude Code を同時に動かしても、互いの変更が衝突しない。
* ``/batch`` コマンドは、大規模な変更を独立した作業に分割し、計画を示したうえで、承認後に複数のエージェントで並列に処理する。

ハーネスを改善し続ける
------------------------------------------

最後に、:doc:`loop_engineering`\ で述べたハーネス改善のループを Claude Code で回す方法をまとめる。

#. Claude が誤った振る舞いをしたら、その場で直させるだけでなく、原因を考える。
#. 情報の不足が原因なら ``CLAUDE.md`` やスキルに追記する。規則が守られなかったのが原因なら、フックや権限の設定で強制する。検証の不足が原因なら、テストやリンターの規則を追加する。
#. 変更をリポジトリにコミットし、チームで共有する。
#. 同じ種類の作業で効果を確かめる。重要な変更であれば、:doc:`eval_driven`\ の方法で、``claude -p`` を使って同じ課題を複数回実行し、変更前後の成功率を比べる。

このループを続けることで、Claude Code はそのプロジェクトに特化した、信頼できる開発の担い手になっていく。
