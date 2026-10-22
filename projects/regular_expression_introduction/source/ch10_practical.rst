実践パターン集
==============

この章では、これまでに説明した構文と関数を組み合わせて、実務でよく出会う処理を書く。

ログを解析する
--------------

次のようなログファイルを解析し、エラーの行を表示して、ログレベルごとの件数を数える。6 行目のように、形式に合わない行も混ざっているものとする。

.. literalinclude:: ../examples/sample.log
   :language: text
   :linenos:
   :caption: 解析するログファイル（sample.log）

まず、1 行の形式を名前付きグループと ``re.VERBOSE`` で記述する。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :start-at: LOG_PATTERN = re.compile(
   :end-before: def parse_log_line
   :linenos:
   :caption: ログ 1 行のパターン

各部分にコメントを付けておくと、ログの形式が変わったときにどこを直せばよいかが分かりやすい。ログレベルの後の空白は、``INFO`` の後のように 2 個以上になる場合があるので ``\s+`` としている。``[`` と ``]`` はメタ文字なので、9 行目ではエスケープしている。

このパターンを使って、1 行を辞書に変換する関数を作る。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: parse_log_line
   :linenos:
   :caption: ログ 1 行を解析する関数

行全体が形式に合っているかを確かめるため、``fullmatch()`` を使う。ファイルから読み込んだ行は末尾に改行を含むので、あらかじめ ``rstrip("\n")`` で取り除いている。``groupdict()`` を使うと、名前付きグループの名前がそのまま辞書のキーになる。

この関数を使ってファイル全体を処理する。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: demo_parse_log
   :linenos:
   :caption: ログファイル全体の解析

形式に合わない行は ``None`` が返るので、7 行目で判定して読み飛ばしている。

ログから特定の情報を取り出す
----------------------------

ファイル全体を 1 つの文字列として読み込み、``finditer()`` で必要な部分だけを取り出すこともできる。次の例では、HTTP のステータスコードが 300 以上のリクエストを表示する。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: demo_http_status
   :linenos:
   :caption: ステータスコードと応答時間の抽出

``(?P<method>GET|POST)`` のように選択をグループで囲むと、どの選択肢に一致したかを取り出せる。取り出した値は文字列なので、数値として比較するには 6 行目のように ``int()`` で変換する。

日付の表記をそろえる
--------------------

``2026/4/1``、``2026年7月15日``、``2027-3-31`` のように表記がばらばらな日付を、``YYYY-MM-DD`` 形式にそろえる。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: demo_normalize_date
   :linenos:
   :caption: 日付の表記の統一

区切り文字の違いは ``[/年-]`` のような文字クラスで、桁数の違いは ``\d{1,2}`` で吸収している。月と日を 2 桁にそろえる処理は置換文字列だけでは書けないので、関数で置換している。

このパターンは形だけを見ているので、``2026/13/45`` のような存在しない日付にも一致する。日付として正しいかどうかまで確かめる場合は、取り出した値を ``datetime.date()`` に渡して検証する。

key=value 形式を解析する
------------------------

設定やコマンドの引数でよく見る ``key=value`` 形式の文字列を、辞書に変換する。値が空白を含む場合は ``"`` で囲まれているものとする。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: demo_key_value
   :linenos:
   :caption: key=value 形式の解析

4 行目の値の部分 ``("[^"]*"|\S+)`` は、「``"`` で囲まれた文字列」または「空白以外の文字の並び」に一致する。引用符で囲まれた場合を先に書いているので、``"John Smith"`` は空白で途切れずに 1 つの値になる。第 6 章で説明したとおり、選択肢は左から順に試されるためである。

空白を正規化する
----------------

連続する空白、タブ、改行を 1 つの半角空白にまとめる。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: demo_normalize_space
   :linenos:
   :caption: 空白の正規化

``\s+`` は全角空白にも一致するので、全角空白も半角空白にそろえられる。前後の空白は ``strip()`` で取り除いている。

入力値を検証する
----------------

郵便番号のように形式の決まった入力値は、``fullmatch()`` で検証する。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: demo_validate
   :linenos:
   :caption: 郵便番号の検証

検証では次の 2 点が重要である。

* ``search()`` ではなく ``fullmatch()`` を使う。``search()`` では、``100-00012`` の一部が一致してしまう。
* ``re.ASCII`` を指定するか ``[0-9]`` を使う。指定しないと、``\d`` が全角数字にも一致し、``１００-０００１`` を受け付けてしまう。

全角数字も受け付けたい場合は、検証の前に ``unicodedata.normalize("NFKC", value)`` で半角に変換しておく方法がある。

メールアドレスと URL について
-----------------------------

メールアドレスや URL を正規表現で厳密に検証しようとすると、パターンは非常に複雑になる。メールアドレスの形式を定めた規格（RFC 5322 など）を忠実に表現しようとした正規表現には数千文字に及ぶものもあり、それでも実際のメールサービスの制約とは一致しない。

実務では、正規表現では「明らかにおかしいもの」を弾く程度にとどめるのが現実的である。

.. literalinclude:: ../examples/ch10_practical.py
   :language: python
   :pyobject: demo_email_rough_check
   :linenos:
   :caption: メールアドレスの簡易的な検査

3 行目のパターンは、「``@`` と空白を含まない文字列、``@``、ドメイン部分（``.`` を 1 つ以上含む）」という最低限の形だけを調べる。メールアドレスが実際に使えるかどうかは、確認メールを送って確かめるのが確実である。URL の場合は、``urllib.parse.urlparse()`` で分解してから各部分を確かめるとよい。

まとめ
------

* 複雑なパターンは ``re.VERBOSE`` と名前付きグループで書き、``groupdict()`` で辞書として取り出す。
* 置換文字列で表現できない変換は、関数による置換で行う。
* 入力値の検証には ``fullmatch()`` を使い、必要に応じて ``re.ASCII`` を指定する。
* 正規表現で調べられるのは形だけである。値の正しさは別の方法で確かめる。

この章のサンプルコード: :download:`ch10_practical.py <../examples/ch10_practical.py>`、:download:`sample.log <../examples/sample.log>`
