API の応用
==========================================

本章では、:doc:`api_basics`\ の内容を踏まえ、実際のアプリケーション開発でよく使う機能を説明します。

思考と effort
------------------------------------------

適応的思考
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Claude Haiku 4.5 を除く現行のモデルは、回答を書く前に内部で検討を行う\ :term:`適応的思考`\ （adaptive thinking）を備えています。問題が簡単ならほとんど考えずに答え、難しければ時間をかけて考えるというように、思考の量をモデル自身が判断します。

Claude Opus 5.5 と Claude Fable 5.1 では思考を無効にできず、常に適応的思考が働きます。思考の量は、次に説明する effort で調整します。

思考の内容は、既定では応答に含まれません（``thinking`` ブロックは返されますが、本文は空です）。検討の過程を利用者に見せたい場合は、思考の要約を返すように指定します。

.. code-block:: python
   :caption: 思考の要約を受け取る
   :linenos:

   response = client.messages.create(
       model="claude-opus-5-5",
       max_tokens=16000,
       thinking={"type": "adaptive", "display": "summarized"},
       messages=[{"role": "user", "content": "この SQL が遅い原因を調べて..."}],
   )
   for block in response.content:
       if block.type == "thinking":
           print("[思考の要約]", block.thinking)
       elif block.type == "text":
           print(block.text)

思考に使われたトークンは、表示の有無にかかわらず出力トークンとして課金されます。

effort
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:term:`effort` は、思考の深さと応答全体の丁寧さを調整するパラメーターで、``output_config`` に指定します。

.. code-block:: python
   :caption: effort の指定
   :linenos:

   response = client.messages.create(
       model="claude-opus-5-5",
       max_tokens=16000,
       output_config={"effort": "high"},
       messages=[{"role": "user", "content": "..."}],
   )

.. list-table:: effort の段階
   :header-rows: 1
   :widths: 15 85

   * - 値
     - 用途の目安
   * - ``low``
     - 分類、短い質問への回答など、速度と料金を優先する処理
   * - ``medium``
     - 一般的な処理。Claude Opus 5.5 の既定値
   * - ``high``
     - 品質を重視する処理。多くのモデルの既定値
   * - ``xhigh``
     - コーディングやエージェントなど、多段階の複雑な作業
   * - ``max``
     - 料金より正確さが重要な、最も難しい問題

effort は Claude Haiku 4.5 では使えません（指定するとエラーになります）。また、effort は思考の量だけでなく、応答の長さやツールを呼び出す回数にも影響します。effort を上げると品質は上がる傾向にありますが、出力トークンと応答時間も増えます。既定値はモデルによって異なるため、明示的に指定しておくと、モデルを変更したときの挙動の変化を防げます。適切な段階は処理の内容によって異なるので、:doc:`operations`\ で説明する評価を使って決めるのが確実です。

サンプリングパラメーター
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

古いモデルでは、出力のばらつきを ``temperature`` などのパラメーターで調整していました。現行のモデルではこれらのパラメーターは使えず、指定するとエラーになります。出力の傾向は、プロンプトと effort で調整してください。

構造化出力
------------------------------------------

応答をプログラムで処理する場合、「JSON で答えて」とプロンプトで頼むだけでは、形式が崩れる可能性を排除できません。:term:`構造化出力`\ を使うと、応答が指定したスキーマに必ず従うようになります。

Python SDK では、Pydantic のモデルを ``messages.parse()`` の ``output_format`` に渡すのが最も簡単です。

.. literalinclude:: ../examples/ex07_structured_output.py
   :language: python
   :caption: ex07_structured_output.py
   :linenos:

``response.parsed_output`` には、検証済みの ``Ticket`` オブジェクトが入ります（51 行目）。応答が拒否された場合や ``max_tokens`` に達した場合は ``None`` になるため、確認してから使います。

Pydantic を使わない場合は、``messages.create()`` の ``output_config`` に JSON スキーマを直接指定します。

.. code-block:: python
   :caption: JSON スキーマを直接指定する
   :linenos:

   response = client.messages.create(
       model="claude-opus-5-5",
       max_tokens=4096,
       messages=[{"role": "user", "content": "..."}],
       output_config={
           "format": {
               "type": "json_schema",
               "schema": {
                   "type": "object",
                   "properties": {
                       "title": {"type": "string"},
                       "tags": {"type": "array", "items": {"type": "string"}},
                   },
                   "required": ["title", "tags"],
                   "additionalProperties": False,
               },
           },
       },
   )

画像と PDF の入力
------------------------------------------

画像
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Claude は画像の内容を理解できます。スクリーンショットの読み取り、図表の解釈、手書きメモの文字起こしなどに使えます。画像は、``content`` をブロックのリストにして、テキストと一緒に送ります。

.. literalinclude:: ../examples/ex08_vision.py
   :language: python
   :caption: ex08_vision.py
   :linenos:

画像は Base64 で符号化して送るほか、URL で指定することもできます（``"source": {"type": "url", "url": "https://..."}``）。画像のサイズが大きいほど入力トークンが増えるため、必要以上に高い解像度の画像は縮小してから送ると料金を抑えられます。

PDF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PDF は ``document`` ブロックで送ります。Claude は本文のテキストだけでなく、ページ上の図や表も読み取ります。

.. code-block:: python
   :caption: PDF を入力する
   :linenos:

   import base64
   from pathlib import Path

   pdf_data = base64.standard_b64encode(Path("spec.pdf").read_bytes())

   response = client.messages.create(
       model="claude-opus-5-5",
       max_tokens=16000,
       messages=[
           {
               "role": "user",
               "content": [
                   {
                       "type": "document",
                       "source": {
                           "type": "base64",
                           "media_type": "application/pdf",
                           "data": pdf_data.decode("ascii"),
                       },
                       "citations": {"enabled": True},
                   },
                   {"type": "text", "text": "この仕様書の要件を一覧にしてください。"},
               ],
           },
       ],
   )

引用（``citations``）を有効にすると（20 行目）、応答の各部分に、根拠となった文書の箇所（PDF ではページ番号）が付きます。回答の根拠を利用者に示したい場合に便利です。

同じファイルを何度も送る場合は、Files API でファイルを一度アップロードし、発行されたファイル ID で参照すると、毎回ファイルの内容を送らずに済みます。

プロンプトキャッシュ
------------------------------------------

仕組み
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

長い資料に対して質問を繰り返すアプリケーションでは、毎回同じ資料を入力として送ることになります。:term:`プロンプトキャッシュ`\ を使うと、入力の先頭から指定した位置までの処理結果がサーバーに一定時間（既定では 5 分）保存され、次の呼び出しで再利用されます。

キャッシュに書き込むトークンは通常の入力より少し高く、キャッシュから読み出すトークンは通常の入力よりはるかに安く課金されます。また、読み出した部分の処理が省かれるため、応答までの時間も短くなります。

.. literalinclude:: ../examples/ex09_prompt_caching.py
   :language: python
   :caption: ex09_prompt_caching.py
   :linenos:

キャッシュは前方一致で判定されます。入力は ``tools``、``system``、``messages`` の順に並べられ、``cache_control`` を付けた位置までが、前回と 1 文字でも異なるとキャッシュは使われません。次の点に注意してください。

* 変化しない内容（資料、ツール定義、固定の指示）を前に、変化する内容（利用者の質問）を後ろに置きます
* システムプロンプトに現在時刻やリクエスト ID のような毎回変わる値を入れません
* キャッシュされるには一定以上の長さ（モデルによって異なり、数百から数千トークン）が必要
* 効いているかどうかは ``usage.cache_read_input_tokens`` で確認します。0 のままなら、前方の内容がどこかで変わっています

料金の試算
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

共通部分のトークン数を :math:`N_{\mathrm{c}}`、同じ共通部分を使う呼び出しの回数を :math:`n`、入力単価を :math:`P_{\mathrm{in}}` とします。キャッシュへの書き込み単価を入力単価の :math:`w` 倍、読み出し単価を :math:`r` 倍とすると、共通部分にかかる料金は次のようになります。

.. math::

   C_{\mathrm{none}}(n) = n \, N_{\mathrm{c}} \, P_{\mathrm{in}}

.. math::

   C_{\mathrm{cache}}(n) = \{ w + (n - 1) \, r \} \, N_{\mathrm{c}} \, P_{\mathrm{in}}

:math:`C_{\mathrm{none}}` はキャッシュを使わない場合、:math:`C_{\mathrm{cache}}` は 1 回目に書き込み、2 回目以降に読み出す場合の料金です。例えば :math:`w = 1.25`、:math:`r = 0.1` のとき、:math:`n = 2` で :math:`C_{\mathrm{cache}} = 1.35 \, N_{\mathrm{c}} P_{\mathrm{in}}` となり、キャッシュを使わない場合の :math:`2 \, N_{\mathrm{c}} P_{\mathrm{in}}` を下回ります。つまり、1 回でも再利用されれば元が取れます。:math:`w` と :math:`r` の実際の値はモデルとキャッシュの保存期間によって異なるため、公式の料金ページで確認してください。

.. plot::
   :caption: キャッシュの有無による共通部分の料金（w = 1.25、r = 0.1 の場合）

   import matplotlib.pyplot as plt
   import numpy as np

   n = np.arange(1, 11)
   w, r = 1.25, 0.1
   no_cache = n * 1.0
   with_cache = w + (n - 1) * r

   fig, ax = plt.subplots(figsize=(7, 3.6))
   ax.plot(n, no_cache, marker="o", color="#4C78A8", label="キャッシュなし")
   ax.plot(n, with_cache, marker="s", color="#F58518", label="キャッシュあり")
   ax.set_xlabel("呼び出し回数 n")
   ax.set_ylabel("料金（1 回分の入力料金を 1 とする）")
   ax.set_xticks(n)
   ax.grid(axis="y", alpha=0.3)
   ax.legend(frameon=False)
   ax.spines[["top", "right"]].set_visible(False)
   fig.tight_layout()

バッチ処理
------------------------------------------

大量のデータを処理するが、結果がすぐに必要ではない場合は、Message Batches API を使います。多数のリクエストをまとめて送信し、非同期に処理させる仕組みで、料金は通常の半額です。処理は多くの場合 1 時間以内に終わり、最長で 24 時間かかります。

.. literalinclude:: ../examples/ex10_batch.py
   :language: python
   :caption: ex10_batch.py
   :linenos:

結果は送信した順に返るとは限らないため、各リクエストに付けた ``custom_id`` で対応付けます（34 行目と 65 行目）。夜間の大量分類、過去データの一括要約、評価データセットの実行などに向いています。

.. _long-conversation:

長い会話の管理
------------------------------------------

チャットアプリケーションやエージェントでは、会話が長くなると入力トークンが増え続け、最終的にはコンテキストウィンドウの上限に達します。対策には次のようなものがあります。

.. list-table:: 長い会話への対策
   :header-rows: 1
   :widths: 25 75

   * - 方法
     - 内容
   * - コンパクション
     - 会話が一定の長さを超えたら、サーバー側で古い部分を自動的に要約して置き換えます（ベータ機能）
   * - コンテキスト編集
     - 古いツールの実行結果など、不要になった部分を自動的に取り除きます（ベータ機能）
   * - アプリケーション側での要約
     - 一定のターン数ごとに、それまでの会話の要約を Claude に作らせ、履歴を要約で置き換えます
   * - 外部への記録
     - 重要な情報をファイルやデータベースに書き出し、必要なときに読み込ませます

どの方法でも、履歴の途中を書き換えるとプロンプトキャッシュが効かなくなる点に注意してください。履歴は末尾に追加していく形を基本とし、書き換えは必要な場面に限ります。
