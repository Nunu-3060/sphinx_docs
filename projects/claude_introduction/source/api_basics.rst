API 入門
==========================================

本章では、Python から Claude API を呼び出す方法を説明します。Claude API の中心は、メッセージを送って応答を受け取る :term:`Messages API`\ （``POST /v1/messages``）です。ツール利用や構造化出力などの機能も、すべてこのエンドポイントのパラメーターとして提供されています。

準備
------------------------------------------

API キーの取得
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Claude Console（`https://platform.claude.com/ <https://platform.claude.com/>`_）でアカウントを作成し、支払い方法を登録したうえで API キーを発行します。API キーは発行時に一度しか表示されないため、安全な場所に保管してください。

API キーは、ソースコードに直接書かず、環境変数 ``ANTHROPIC_API_KEY`` で渡すのが原則です。ソースコードに書いたキーは、リポジトリへのコミットなどを通じて漏えいする危険があります。

.. code-block:: console
   :caption: 環境変数の設定（1 行目は Linux / macOS、2 行目は Windows PowerShell）
   :linenos:

   $ export ANTHROPIC_API_KEY="sk-ant-..."
   PS> $env:ANTHROPIC_API_KEY = "sk-ant-..."

SDK のインストール
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Anthropic は Python、TypeScript、Java、Go、Ruby、C#、PHP の公式 SDK を提供しています。本書では Python SDK（``anthropic`` パッケージ）を使います。仮想環境を作成してインストールします。

.. code-block:: console
   :caption: 仮想環境の作成と SDK のインストール
   :linenos:

   $ python -m venv .venv
   $ source .venv/bin/activate      # Windows では .venv\Scripts\activate
   $ pip install anthropic

本書のサンプルコードをまとめて実行する場合は、:doc:`examples`\ の ``requirements.txt`` を使って ``pip install -r requirements.txt`` を実行してください。

最初のリクエスト
------------------------------------------

最小構成のプログラムは次のとおりです。

.. literalinclude:: ../examples/ex01_hello_claude.py
   :language: python
   :caption: ex01_hello_claude.py
   :linenos:

``anthropic.Anthropic()`` は、環境変数 ``ANTHROPIC_API_KEY`` から API キーを読み込んでクライアントを生成します（19 行目）。``client.messages.create()`` の主な引数は次のとおりです。

.. list-table:: messages.create() の主な引数
   :header-rows: 1
   :widths: 22 12 66

   * - 引数
     - 必須
     - 説明
   * - ``model``
     - ○
     - 使用するモデルの ID。本書のサンプルでは環境変数 ``CLAUDE_MODEL`` で変更できるようにしています
   * - ``max_tokens``
     - ○
     - 出力トークン数の上限。上限に達すると応答は途中で打ち切られます
   * - ``messages``
     - ○
     - 会話の履歴。``role``\ （``user`` または ``assistant``）と ``content`` の組のリスト
   * - ``system``
     -
     - システムプロンプト。役割や応答の方針を指定します
   * - ``tools``
     -
     - Claude が使えるツールの定義（:doc:`tool_use`\ 参照）
   * - ``output_config``
     -
     - effort（思考の深さ）や構造化出力の形式を指定します（:doc:`api_advanced`\ 参照）
   * - ``stop_sequences``
     -
     - 出力されると生成を停止する文字列のリスト

応答の構造
------------------------------------------

``messages.create()`` は ``Message`` オブジェクトを返します。主な属性は次のとおりです。

.. list-table:: Message の主な属性
   :header-rows: 1
   :widths: 22 78

   * - 属性
     - 説明
   * - ``content``
     - 応答本体。:term:`コンテンツブロック`\ のリスト
   * - ``stop_reason``
     - 生成が止まった理由
   * - ``usage``
     - 入力と出力のトークン数。料金の計算に使います
   * - ``model``
     - 実際に応答したモデルの ID
   * - ``id``
     - メッセージの ID

コンテンツブロック
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

応答の ``content`` は、文字列ではなくブロックのリストです。ブロックには種類（``type``）があり、テキストは ``text``、思考の内容は ``thinking``、ツールの呼び出し要求は ``tool_use`` というブロックで返されます。

1 つの応答に複数の種類のブロックが含まれることがあるため、``response.content[0].text`` のように先頭のブロックを決め打ちで読むのは避けてください。``ex01_hello_claude.py`` の 30 〜 32 行目のように、``type`` を確認してから読むのが安全です。

stop_reason
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``stop_reason`` は、応答を利用する前に必ず確認すべき属性です。

.. list-table:: stop_reason の値
   :header-rows: 1
   :widths: 22 78

   * - 値
     - 意味と対処
   * - ``end_turn``
     - 応答が自然に完了しました
   * - ``max_tokens``
     - ``max_tokens`` の上限に達し、応答が途中で切れています。``max_tokens`` を引き上げます（大きな値にする場合はストリーミングを使います）
   * - ``stop_sequence``
     - ``stop_sequences`` に指定した文字列が出力されました
   * - ``tool_use``
     - Claude がツールの呼び出しを求めています（:doc:`tool_use`\ 参照）
   * - ``pause_turn``
     - サーバー側のツールの処理が長くなり、一時停止しました。応答をそのまま送り返すと処理が再開されます
   * - ``refusal``
     - 安全上の理由で応答が拒否されました。``stop_details`` に分類が入ります

システムプロンプト
------------------------------------------

:term:`システムプロンプト`\ は、会話全体に適用される前提や方針を指定するための入力で、``system`` 引数に渡します。役割、応答の方針、出力の形式、利用できる資料などを書きます。

.. literalinclude:: ../examples/ex02_system_prompt.py
   :language: python
   :caption: ex02_system_prompt.py
   :linenos:

利用者が入力する内容は ``messages`` に、アプリケーション側で固定する指示は ``system`` に、と分けるのが基本です。

複数ターンの対話
------------------------------------------

Messages API は\ :term:`ステートレス`\ です。サーバーは過去のやり取りを記憶しないため、会話を続けるには、これまでの履歴をすべて ``messages`` に含めて毎回送信します（:numref:`fig-multiturn`）。

.. _fig-multiturn:

.. graphviz::
   :caption: 複数ターンの対話では履歴全体を毎回送る
   :align: center

   digraph multiturn {
     rankdir=LR;
     node [shape=record, style=filled, fillcolor="#EEF3FA", color="#4C78A8"];
     edge [color="#555555"];

     r1 [label="1 回目の送信|user: 質問 1"];
     r2 [label="2 回目の送信|user: 質問 1|assistant: 回答 1|user: 質問 2"];
     r3 [label="3 回目の送信|user: 質問 1|assistant: 回答 1|user: 質問 2|assistant: 回答 2|user: 質問 3"];
     r1 -> r2 [label="回答 1 を\n履歴に追加"];
     r2 -> r3 [label="回答 2 を\n履歴に追加"];
   }

.. literalinclude:: ../examples/ex03_multi_turn.py
   :language: python
   :caption: ex03_multi_turn.py
   :linenos:

40 〜 42 行目では、応答のテキストだけでなく、コンテンツブロックのリスト（``response.content``）をそのまま履歴に追加しています。応答には ``thinking`` ブロックや ``tool_use`` ブロックが含まれることがあり、それらを落とすと後続の応答の質が下がったり、エラーになったりするためです。

``messages`` の先頭は ``user`` でなければなりません。また、履歴が長くなるほど入力トークンが増え、料金も増えます。長い会話の扱いについては\ :ref:`long-conversation`\ を参照してください。

ストリーミング
------------------------------------------

通常の呼び出しでは、応答がすべて生成されるまで結果が返りません。:term:`ストリーミング`\ を使うと、生成された部分から順に受け取れます。チャット画面のように応答を逐次表示したい場合や、出力が長くなる場合に使います。

.. literalinclude:: ../examples/ex04_streaming.py
   :language: python
   :caption: ex04_streaming.py
   :linenos:

``client.messages.stream()`` をコンテキストマネージャーとして使い、``text_stream`` からテキストの断片を受け取ります（31 〜 32 行目）。ストリームを読み終えた後は ``get_final_message()`` で、通常の呼び出しと同じ ``Message`` オブジェクトを取得できます（35 行目）。

``max_tokens`` を大きくする場合や入力が長い場合は、応答に時間がかかり、通常の呼び出しでは HTTP のタイムアウトに達することがあります。生成に時間がかかりそうな処理では、表示の必要がなくてもストリーミングを使い、``get_final_message()`` で結果を受け取るのが安全です。

エラー処理
------------------------------------------

API の呼び出しは、ネットワークの障害、レート制限、サーバーの過負荷などで失敗することがあります。主な HTTP ステータスコードは次のとおりです。

.. list-table:: 主なエラー
   :header-rows: 1
   :widths: 12 30 58

   * - コード
     - SDK の例外クラス
     - 意味と対処
   * - 400
     - ``BadRequestError``
     - リクエストの形式や内容に誤りがあります。再試行しても成功しないため、内容を修正します
   * - 401
     - ``AuthenticationError``
     - API キーが無効
   * - 403
     - ``PermissionDeniedError``
     - API キーに必要な権限がありません
   * - 404
     - ``NotFoundError``
     - モデル ID などが存在しません
   * - 429
     - ``RateLimitError``
     - レート制限を超えました。``retry-after`` ヘッダーの秒数だけ待って再試行します
   * - 500
     - ``InternalServerError``
     - サーバー内部のエラー。時間をおいて再試行します
   * - 529
     - ``OverloadedError``
     - サーバーが過負荷の状態。時間をおいて再試行します

SDK は、408、409、429、5xx のような再試行で回復しうるエラーと接続エラーを、間隔を空けながら自動で再試行します（既定は 2 回）。それでも失敗した場合に備え、例外を具体的なクラスから順に捕捉します。

.. literalinclude:: ../examples/ex05_error_handling.py
   :language: python
   :caption: ex05_error_handling.py
   :linenos:

ポイントは次のとおりです。

* 例外は具体的なクラスから順に捕捉します（27 〜 39 行目）。``APIStatusError`` は HTTP エラー全般の親クラスなので、個別のクラスより後に置きます。
* ``stop_reason`` が ``refusal`` の場合は、``content`` を読む前に判定します（48 〜 53 行目）。
* 問い合わせの際に必要になるリクエスト ID は ``_request_id`` で取得できます（46 行目）。名前は下線で始まりますが、公開された属性です。
* 再試行の回数とタイムアウトは、クライアントの生成時に ``max_retries`` と ``timeout`` で変更できます（64 行目）。

レート制限
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

API には、1 分あたりのリクエスト数、入力トークン数、出力トークン数の上限（レート制限）があります。上限は利用実績に応じた利用枠（ティア）によって決まり、利用額が増えると引き上げられます。現在の上限は Claude Console で確認できます。

大量のリクエストを送る処理では、同時実行数を制限する、即時性の不要な処理を :doc:`api_advanced`\ のバッチ処理に回す、プロンプトキャッシュで入力トークンを減らす、といった対策を組み合わせます。

トークン数と料金
------------------------------------------

API の料金は、入力と出力のトークン数に応じて決まります。入力トークン数を :math:`N_{\mathrm{in}}`、出力トークン数を :math:`N_{\mathrm{out}}`、100 万トークンあたりの入力と出力の単価をそれぞれ :math:`P_{\mathrm{in}}`、:math:`P_{\mathrm{out}}` とすると、1 回の呼び出しの料金 :math:`C` は次の式で求められます。

.. math::

   C = \frac{N_{\mathrm{in}} \, P_{\mathrm{in}} + N_{\mathrm{out}} \, P_{\mathrm{out}}}{10^{6}}

例えば Claude Opus 5.5（:math:`P_{\mathrm{in}} = 4`、:math:`P_{\mathrm{out}} = 20`）に 20,000 トークンを入力し、2,000 トークンの出力を得た場合の料金は次のとおりです。

.. math::

   C = \frac{20000 \times 4 + 2000 \times 20}{10^{6}} = 0.12 \ \text{(米ドル)}

出力の単価は入力の 5 倍なので、出力が短くても料金に占める割合は小さくありません。

トークン数の計測
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

実際のトークン数は、応答の ``usage`` で確認できます。送信前にトークン数を知りたい場合は、トークン計測 API（``messages.count_tokens()``）を使います。トークン計測 API は無料で、メッセージは生成されません。

.. literalinclude:: ../examples/ex06_count_tokens.py
   :language: python
   :caption: ex06_count_tokens.py
   :linenos:

トークンの数え方はモデルによって異なります。同じ文章でもモデルを変えるとトークン数が変わることがあるため、料金の見積もりは使用するモデルで計測してください。

非同期クライアント
------------------------------------------

Web アプリケーションなど、複数のリクエストを並行して処理する場合は、非同期クライアント ``AsyncAnthropic`` を使います。使い方は同期版と同じで、呼び出しに ``await`` を付けます。

.. code-block:: python
   :caption: 非同期クライアントで複数の要約を並行して実行する例
   :linenos:

   import asyncio

   import anthropic

   MAX_CONCURRENCY = 5  # 同時に送るリクエストの上限


   async def summarize(
       client: anthropic.AsyncAnthropic, limit: asyncio.Semaphore, text: str
   ) -> str:
       async with limit:  # 上限を超えるリクエストはここで待つ
           response = await client.messages.create(
               model="claude-opus-5-5",
               max_tokens=1024,
               messages=[{"role": "user", "content": f"100 字で要約して:\n{text}"}],
           )
       return "".join(b.text for b in response.content if b.type == "text")


   async def main(texts: list[str]) -> list[str]:
       client = anthropic.AsyncAnthropic()
       limit = asyncio.Semaphore(MAX_CONCURRENCY)
       return await asyncio.gather(*(summarize(client, limit, t) for t in texts))


   summaries = asyncio.run(main(["文書 1 の本文...", "文書 2 の本文..."]))

並行数を増やしすぎるとレート制限に達するため、この例では ``asyncio.Semaphore`` で同時実行数を制限しています（11 行目と 22 行目）。
