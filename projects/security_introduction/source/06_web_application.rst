Web アプリケーションのセキュリティ
==================================

この章では、Web アプリケーションに見られる代表的な脆弱性の仕組みと対策を説明します。多くの脆弱性は、「利用者から受け取ったデータを、プログラムの一部として解釈させてしまう」か、「確認すべきことを確認していない」かのどちらかに分類できます。

OWASP Top 10
------------

OWASP（Open Worldwide Application Security Project）は、Web アプリケーションのセキュリティに関する情報を公開している非営利の団体です。OWASP が数年ごとに公開する OWASP Top 10 は、Web アプリケーションの重大なリスクを 10 項目にまとめたもので、開発者が最初に押さえるべき項目の一覧として広く参照されています。2025 年版の項目を次の表に示します。

.. list-table:: OWASP Top 10:2025
   :header-rows: 1
   :widths: 12 38 50

   * - 番号
     - 項目
     - 本書で関連する箇所
   * - A01
     - アクセス制御の不備（Broken Access Control）
     - 本章の「アクセス制御の不備」、:doc:`04_authentication`
   * - A02
     - セキュリティ設定のミス（Security Misconfiguration）
     - 本章の「セキュリティ関連の HTTP ヘッダー」、:doc:`09_cloud_and_container`
   * - A03
     - ソフトウェアサプライチェーンの不備（Software Supply Chain Failures）
     - :doc:`08_supply_chain`
   * - A04
     - 暗号の不備（Cryptographic Failures）
     - :doc:`03_cryptography`
   * - A05
     - インジェクション（Injection）
     - 本章の「インジェクション」「クロスサイトスクリプティング」
   * - A06
     - 安全でない設計（Insecure Design）
     - :doc:`11_testing_and_threat_modeling`
   * - A07
     - 認証の不備（Authentication Failures）
     - :doc:`04_authentication`
   * - A08
     - ソフトウェアやデータの完全性の不備（Software or Data Integrity Failures）
     - :doc:`07_secure_coding`、:doc:`08_supply_chain`
   * - A09
     - セキュリティのログ記録とアラートの不備（Security Logging and Alerting Failures）
     - :doc:`12_operations`
   * - A10
     - 例外的な状況の不適切な処理（Mishandling of Exceptional Conditions）
     - :doc:`07_secure_coding`

同一オリジンポリシーと CORS
---------------------------

Web のセキュリティを理解するうえで前提となるのが、ブラウザーの\ :term:`同一オリジンポリシー`\ です。

オリジンとは、URL のスキーム（``https`` など）、ホスト名、ポート番号の組み合わせです。この 3 つがすべて一致する場合に、同一オリジンとみなされます。

.. list-table:: ``https://example.com/page`` と同一オリジンかどうか
   :header-rows: 1
   :widths: 50 15 35

   * - URL
     - 判定
     - 理由
   * - ``https://example.com/other``
     - 同一
     - パスは関係しません。
   * - ``http://example.com/page``
     - 別
     - スキームが異なります。
   * - ``https://api.example.com/page``
     - 別
     - ホスト名が異なります。
   * - ``https://example.com:8443/page``
     - 別
     - ポート番号が異なります。

同一オリジンポリシーは、あるオリジンのページで動く JavaScript が、別のオリジンのデータを読み取ることを制限します。もしこの制限がなければ、利用者が悪意のあるサイトを開いただけで、そのサイトの JavaScript が、利用者がログインしている銀行のサイトから残高を読み取れてしまいます。ブラウザーは銀行のサイトへのリクエストに、利用者の Cookie を自動的に付けて送るからです。

ただし、同一オリジンポリシーが制限するのは、主に「別のオリジンからの応答を読み取ること」です。別のオリジンへのリクエストを送ること自体は、フォームの送信などで可能です。この点が、後で説明する CSRF の原因になります。

別のオリジンの API を正当に利用したい場合のために、サーバーが許可するオリジンを宣言する仕組みが :term:`CORS`\ （Cross-Origin Resource Sharing）です。サーバーが次のようなヘッダーを返すと、ブラウザーは指定されたオリジンのページに応答の読み取りを許可します。

.. code-block:: text
   :linenos:

   Access-Control-Allow-Origin: https://app.example.com
   Access-Control-Allow-Credentials: true

CORS の設定では、次のような誤りがよく見られます。

* リクエストの ``Origin`` ヘッダーの値を検証せずに、そのまま ``Access-Control-Allow-Origin`` に返しています。どのサイトからでも、Cookie 付きで応答を読み取れるようになります。
* ``null`` オリジンを許可しています。``null`` オリジンは、サンドボックス化された iframe などから攻撃者が作り出せます。
* ``example.com`` を含むかどうかを部分一致で判定しています。``example.com.attacker.net`` のようなドメインを許可してしまいます。

許可するオリジンは、完全一致の許可リストで判定します。

Cookie の属性
-------------

:doc:`04_authentication`\ で説明したように、セッション ID は Cookie で送られます。Cookie には、送信される条件や読み取りを制限する属性があり、セッションを守るために重要な役割を果たします。

.. list-table:: セキュリティに関係する Cookie の属性
   :header-rows: 1
   :widths: 20 50 30

   * - 属性
     - 効果
     - 推奨
   * - Secure
     - HTTPS の通信でだけ Cookie を送ります。
     - 常に付けます。
   * - HttpOnly
     - JavaScript から Cookie を読み取れなくします。XSS が発生しても、セッション ID を盗まれにくくなります。
     - セッション ID には常に付けます。
   * - SameSite
     - 別のサイトから発生したリクエストに Cookie を付けるかを制御します。``Strict`` は常に付けず、``Lax`` はリンクをたどるなどの画面遷移の場合だけ付け、``None`` は常に付けます（Secure 属性が必須です）。
     - ``Lax`` または ``Strict`` にします。
   * - Domain
     - Cookie を送るドメインの範囲を指定します。指定するとサブドメインにも送られます。
     - 必要がなければ指定しません。

Cookie の名前を ``__Host-`` で始めると、ブラウザーは Secure 属性があり、Domain 属性がなく、Path が ``/`` である場合にだけその Cookie を受け入れます。サブドメインから Cookie を上書きされる攻撃を防げるため、セッション ID の Cookie に適しています。

.. code-block:: text
   :linenos:

   Set-Cookie: __Host-session=6fQ1...; Secure; HttpOnly; SameSite=Lax; Path=/

アクセス制御の不備
------------------

OWASP Top 10:2025 で最も重大なリスクとされているのが、アクセス制御の不備です。典型的な例が、URL やリクエストのパラメーターに含まれる ID を書き換えるだけで、他人のデータにアクセスできてしまう脆弱性で、:term:`IDOR`\ （Insecure Direct Object Reference）と呼ばれます。

例えば、``https://example.com/invoices/1001`` で自分の請求書を表示できるときに、``1001`` を ``1002`` に書き換えると他人の請求書が表示される、という脆弱性です。サーバーが「ログインしているか」だけを確認し、「この請求書を参照する権限があるか」を確認していないことが原因です。

次のサンプルで、悪い例と良い例を比較します。

.. literalinclude:: ../examples/access_control.py
   :language: python
   :linenos:
   :caption: access_control.py

:download:`access_control.py をダウンロード <../examples/access_control.py>`

.. code-block:: text
   :caption: 実行結果

   [悪い例] alice が ID を 1002 に書き換えた場合
     Invoice(invoice_id=1002, owner='bob', amount=98000)
   [良い例]
     alice が自分の請求書を参照: Invoice(invoice_id=1001, owner='alice', amount=12000)
     alice が他人の請求書を参照: 拒否（請求書 1002 は見つかりません）
     管理者が参照: Invoice(invoice_id=1002, owner='bob', amount=98000)

良い例では、権限がない場合と存在しない場合で同じエラーを返しています。「権限がありません」と返すと、その ID のデータが存在することを攻撃者に教えてしまうためです。

ID を推測しにくいランダムな値にすることも被害の軽減には役立ちますが、それだけでは対策になりません。ID は URL の共有やログなどを通じて漏れることがあるためです。必ずサーバー側で権限を確認します。

インジェクション
----------------

:term:`インジェクション`\ は、利用者の入力が、SQL 文やコマンドなどの「プログラムの一部」として解釈されてしまう脆弱性の総称です。根本的な対策は、**データとプログラムを分離する**\ ことです。

SQL インジェクション
^^^^^^^^^^^^^^^^^^^^

利用者の入力を文字列連結で SQL 文に埋め込むと、入力に含まれる引用符などの記号によって、SQL 文の構造そのものが変えられてしまいます。これを :term:`SQL インジェクション`\ と呼びます。データベースの情報の漏えいや改ざん、認証の回避などにつながる、深刻な脆弱性です。

対策は、**プレースホルダー**\ を使うことです。プレースホルダーを使うと、SQL 文の構造と値が別々にデータベースに渡されるため、値に何が含まれていても、SQL 文の構造は変わりません。次のサンプルで確認します。

.. literalinclude:: ../examples/sql_injection.py
   :language: python
   :linenos:
   :caption: sql_injection.py

:download:`sql_injection.py をダウンロード <../examples/sql_injection.py>`

.. code-block:: text
   :caption: 実行結果

   [文字列連結（悪い例）]
     実行される SQL: SELECT name FROM users WHERE name = 'alice'
     通常の入力: ['alice']
     実行される SQL: SELECT name FROM users WHERE name = '' OR '1'='1'
     攻撃の入力: ['alice', 'bob', 'admin']
   [プレースホルダー（良い例）]
     通常の入力: ['alice']
     攻撃の入力: []

悪い例では、入力の ``' OR '1'='1`` によって WHERE 句が常に真になり、すべての利用者の情報が返されています。良い例では、入力全体が 1 つの文字列の値として扱われるため、該当する利用者はいません。

ORM（Object-Relational Mapping）のライブラリを使う場合も、生の SQL 文を書ける機能に入力を文字列連結で渡すと、同じ脆弱性が生じます。また、テーブル名や列名、``ORDER BY`` の並び順のように、プレースホルダーを使えない箇所に入力を使う場合は、許可リストに含まれる値だけを受け付けます。

OS コマンドインジェクション
^^^^^^^^^^^^^^^^^^^^^^^^^^^

外部のコマンドを実行する機能で、利用者の入力をシェルに渡すと、入力に含まれる ``&``、``;``、``|`` などの記号がシェルに解釈され、攻撃者の任意のコマンドが実行されます。これを :term:`OS コマンドインジェクション`\ と呼びます。サーバーを完全に乗っ取られるおそれがある、非常に深刻な脆弱性です。

Python では、``subprocess`` モジュールに ``shell=True`` を指定し、入力を含む文字列を渡すと、この脆弱性が生じます。コマンドと引数をリストで渡せば、シェルを経由しないため、入力に含まれる記号は解釈されません。次のサンプルでは、無害な ``echo`` コマンドを使って確認します。

.. literalinclude:: ../examples/command_injection.py
   :language: python
   :linenos:
   :caption: command_injection.py

:download:`command_injection.py をダウンロード <../examples/command_injection.py>`

.. code-block:: text
   :caption: 実行結果（Windows で実行した例）

   [shell=True（悪い例）]
     シェルに渡す文字列: echo Hello, alice & echo INJECTED
     出力: 'Hello, alice \nINJECTED'
   [引数のリスト（良い例）]
     出力: 'Hello, alice & echo INJECTED'

悪い例では、``&`` の後ろの ``echo INJECTED`` が 2 つ目のコマンドとして実行されています。実際の攻撃では、ここにファイルの削除やマルウェアのダウンロードなどのコマンドが指定されます。

そもそも外部のコマンドを呼び出さずに、Python の標準ライブラリやライブラリの関数で同じ処理ができないかを検討することも重要です。

クロスサイトスクリプティング
----------------------------

:term:`XSS`\ （クロスサイトスクリプティング）は、攻撃者が用意したスクリプトを、脆弱な Web サイトのページの一部として利用者のブラウザーで実行させる攻撃です。スクリプトは脆弱なサイトのオリジンで動くため、同一オリジンポリシーによる保護が働きません。攻撃者は、利用者の画面を書き換えて偽の入力フォームを表示したり、利用者になりすまして操作したりできます。

XSS は、スクリプトが埋め込まれる経路によって、次の 3 種類に分けられます。

.. list-table:: XSS の種類
   :header-rows: 1
   :widths: 25 75

   * - 種類
     - 内容
   * - 反射型
     - URL のパラメーターなどに含まれるスクリプトが、そのまま応答のページに出力されます。攻撃者は細工したリンクを利用者に開かせます。
   * - 格納型
     - 掲示板の投稿などに含まれるスクリプトがデータベースに保存され、そのページを表示したすべての利用者のブラウザーで実行されます。
   * - DOM ベース
     - サーバーを経由せず、ページの JavaScript が URL の値などを ``innerHTML`` などで HTML として挿入することで発生します。

基本的な対策は、利用者の入力を HTML に出力する直前に\ **エスケープ**\ することです。エスケープとは、``<`` を ``&lt;`` に置き換えるなど、HTML として特別な意味を持つ文字を、文字そのものとして表示される表現に変換することです。

.. literalinclude:: ../examples/xss_escape.py
   :language: python
   :linenos:
   :caption: xss_escape.py

:download:`xss_escape.py をダウンロード <../examples/xss_escape.py>`

.. code-block:: text
   :caption: 実行結果

   悪い例: <p><script>alert("XSS")</script></p>
   良い例: <p>&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;</p>
   属性値: <a href="https://example.com/?q=1&amp;r=2">リンク</a>
   属性値: <a href="#">リンク</a>
   属性値: <a href="https://x/&quot; onclick=&quot;evil()">リンク</a>

エスケープの方法は、出力する場所（コンテキスト）によって異なります。HTML の本文、属性値、JavaScript の中、URL の中では、それぞれ特別な意味を持つ文字が違うためです。特に、``href`` 属性に ``javascript:`` で始まる URL を出力すると、エスケープしてもスクリプトが実行されます。サンプルの ``render_attribute_safe()`` のように、URL のスキームを許可リストで検証する必要があります。

実際の開発では、出力を自動的にエスケープするテンプレートエンジンやフレームワーク（Jinja2、React など）を使い、自動エスケープを無効にする機能（Jinja2 の ``|safe`` フィルターや React の ``dangerouslySetInnerHTML`` など）は、やむを得ない場合を除いて使わないようにします。

多層防御として、次の対策も組み合わせます。

* セッション ID の Cookie に HttpOnly 属性を付け、XSS が発生してもセッション ID を読み取られにくくします。
* 後で説明する Content-Security-Policy ヘッダーで、実行できるスクリプトを制限します。

クロスサイトリクエストフォージェリ
----------------------------------

:term:`CSRF`\ （クロスサイトリクエストフォージェリ）は、利用者が攻撃者のサイトを開いたときに、利用者が意図しないリクエストを、利用者がログインしている別のサイトに送らせる攻撃です。

例えば、攻撃者のサイトに、銀行の送金処理に向けて自動的に送信されるフォームを置いておきます。銀行にログインしている利用者がこのサイトを開くと、ブラウザーは銀行へのリクエストに利用者の Cookie を付けて送るため、銀行は利用者本人の操作と区別できず、送金が実行されてしまいます。

CSRF への対策は次のとおりです。

* **CSRF トークンを使ってください。**\ フォームを表示するときに、推測できないトークンを埋め込んでおき、送信されたトークンがセッションに保存した値と一致するかを検証します。攻撃者のサイトは、同一オリジンポリシーによって正規のページの内容を読み取れないため、トークンを知ることができません。
* **SameSite 属性を設定してください。**\ セッション ID の Cookie に ``SameSite=Lax`` 以上を設定すると、別のサイトからの POST リクエストに Cookie が付かなくなります。
* **状態を変更する処理に GET を使わないでください。**\ ``SameSite=Lax`` でも、リンクをたどる GET リクエストには Cookie が付くためです。

フレームワークの多くは CSRF 対策の機能を備えているので、それを有効にして使います。CSRF トークンの実装例は、この章の最後の Flask のサンプルで示します。

サーバーサイドリクエストフォージェリ
------------------------------------

:term:`SSRF`\ （サーバーサイドリクエストフォージェリ）は、利用者が指定した URL にサーバーがアクセスする機能を悪用して、外部からは直接アクセスできない内部のシステムにリクエストを送らせる攻撃です。URL のプレビュー機能、Webhook の送信先の登録、URL を指定した画像の取り込みなどが攻撃の入口になります。

特に危険なのが、クラウドのメタデータサービスです。AWS などのクラウドでは、仮想マシンの中から ``169.254.169.254`` というアドレスにアクセスすると、その仮想マシンに割り当てられた認証情報を取得できます。SSRF でこの認証情報を盗まれると、クラウドの他のリソースにまでアクセスされます。クラウド側の対策は\ :doc:`09_cloud_and_container`\ で説明します。

アプリケーション側では、次の対策を組み合わせます。

* 許可するスキームを ``https`` などに限定します。
* アクセス先のホストが固定できる場合は、許可リストで判定します。
* 任意のホストを許可する必要がある場合は、ホスト名を名前解決した IP アドレスが、内部のアドレス（プライベートアドレス、ループバックアドレス、リンクローカルアドレスなど）でないことを確認します。
* リダイレクトを自動的にたどりません。たどる場合は、リダイレクト先も同じように検証します。

次のサンプルは、3 つ目の対策を実装したものです。

.. literalinclude:: ../examples/ssrf_url_check.py
   :language: python
   :linenos:
   :caption: ssrf_url_check.py

:download:`ssrf_url_check.py をダウンロード <../examples/ssrf_url_check.py>`

.. code-block:: text
   :caption: 実行結果の例

   https://www.python.org/                       -> 許可
   http://www.python.org/                        -> 拒否（スキーム 'http' は許可されていません）
   https://127.0.0.1/admin                       -> 拒否（内部アドレス 127.0.0.1 に解決されました）
   https://169.254.169.254/latest/meta-data/     -> 拒否（内部アドレス 169.254.169.254 に解決されました）
   https://10.0.0.5/                             -> 拒否（内部アドレス 10.0.0.5 に解決されました）
   https://localhost/                            -> 拒否（内部アドレス 127.0.0.1 に解決されました）
   file:///etc/passwd                            -> 拒否（スキーム 'file' は許可されていません）

.. warning::

   このサンプルの検証には限界があります。検証時の名前解決と、実際にアクセスするときの名前解決の結果を攻撃者が変える攻撃（DNS リバインディング）を防ぐには、検証した IP アドレスに対して直接接続する必要があります。外部へのアクセスを、内部ネットワークに到達できない専用のプロキシー経由に限定する方法も有効です。

パストラバーサル
----------------

利用者が指定したファイル名をそのままパスに連結すると、``../`` を使って公開用のディレクトリの外にあるファイルを読み書きされてしまいます。これを\ :term:`パストラバーサル`\ と呼びます。設定ファイルや秘密鍵が読み取られる、プログラムが上書きされるなどの被害につながります。

対策は、パスを正規化（``..`` やシンボリックリンクを解決）したうえで、その結果が許可したディレクトリの配下にあることを確認することです。

.. literalinclude:: ../examples/path_traversal.py
   :language: python
   :linenos:
   :caption: path_traversal.py

:download:`path_traversal.py をダウンロード <../examples/path_traversal.py>`

.. code-block:: text
   :caption: 実行結果

   [悪い例]
     ../secret.txt -> 秘密の情報
   [良い例]
     hello.txt -> 公開ファイル
     ../secret.txt -> 拒否（公開ディレクトリの外は参照できません: ../secret.txt）

文字列から ``../`` を取り除くだけの対策は、``....//`` のような入力や、URL エンコードされた入力で回避されることがあるため、避けてください。可能であれば、利用者にはファイル名ではなく ID を指定させ、サーバー側で ID とファイルを対応付けるのが最も安全です。

その他の頻出する脆弱性
----------------------

ここまでに説明したもの以外にも、次のような脆弱性がよく見られます。

.. list-table:: その他の頻出する脆弱性
   :header-rows: 1
   :widths: 22 43 35

   * - 脆弱性
     - 内容
     - 対策
   * - クリックジャッキング
     - 正規のサイトを透明な iframe で重ねて表示し、利用者に気付かれないようにボタンをクリックさせます。
     - Content-Security-Policy の ``frame-ancestors`` で、他のサイトからの埋め込みを禁止します。
   * - オープンリダイレクト
     - ``?next=`` などのパラメーターで指定された任意の URL にリダイレクトする機能が、フィッシングサイトへの誘導に悪用されます。
     - リダイレクト先を、自サイト内のパスや許可リストのドメインに限定します。
   * - ファイルアップロードの不備
     - アップロードされたファイルが、サーバーでプログラムとして実行されたり、HTML として表示されて XSS を引き起こしたりします。
     - ファイルの種類を許可リストで検証し、ファイル名はサーバー側で付け直し、公開ディレクトリの外や別のドメインに保存します。
   * - XXE
     - XML の外部エンティティの機能を悪用して、サーバー上のファイルを読み取ったり、SSRF を引き起こしたりします。
     - 外部エンティティを無効にした XML パーサーを使います（Python では defusedxml ライブラリが利用できます）。
   * - マスアサインメント
     - リクエストのパラメーターを、そのままデータベースのレコードに一括で反映するため、``is_admin`` などの変更してはいけない項目まで書き換えられます。
     - 更新を許可する項目を明示的に列挙します。

セキュリティ関連の HTTP ヘッダー
--------------------------------

ブラウザーには、サーバーが返す HTTP ヘッダーによって有効になる保護機能があります。代表的なものを次の表に示します。

.. list-table:: セキュリティ関連の HTTP レスポンスヘッダー
   :header-rows: 1
   :widths: 32 43 25

   * - ヘッダー
     - 効果
     - 設定例
   * - Content-Security-Policy
     - スクリプトや画像などを読み込める場所を制限します。インラインのスクリプトの実行も禁止でき、XSS の被害を大きく軽減できます。
     - ``default-src 'self'``
   * - Strict-Transport-Security
     - 指定した期間、HTTPS だけで接続させます（\ :doc:`05_network`\ を参照）。
     - ``max-age=31536000``
   * - X-Content-Type-Options
     - ブラウザーが Content-Type を無視して内容から種類を推測する動作を禁止します。
     - ``nosniff``
   * - Referrer-Policy
     - 遷移先のサイトに送る遷移元の URL の範囲を制限します。
     - ``strict-origin-when-cross-origin``
   * - X-Frame-Options
     - 他のサイトからの iframe での埋め込みを禁止します（``frame-ancestors`` の旧来の方法です）。
     - ``DENY``

Content-Security-Policy（CSP）は強力ですが、既存のアプリケーションにいきなり厳しい設定を適用すると、正常な機能まで動かなくなることがあります。最初は ``Content-Security-Policy-Report-Only`` ヘッダーで違反の報告だけを受け取り、問題がないことを確認してから適用するとよいでしょう。

Flask による対策の実装例
------------------------

ここまでに説明した対策のうち、XSS、CSRF、Cookie の属性、セキュリティ関連のヘッダーを、Flask で実装したサンプルを示します。比較のため、XSS の脆弱性がある悪い例のページも含めています。

.. literalinclude:: ../examples/flask_security_demo.py
   :language: python
   :linenos:
   :caption: flask_security_demo.py

:download:`flask_security_demo.py をダウンロード <../examples/flask_security_demo.py>`

このサンプルのポイントは次のとおりです。

* ``render_template_string()`` で使われるテンプレートエンジン Jinja2 は、変数を自動的にエスケープします。``/search?q=<b>bold</b>`` を開くと、タグは文字としてそのまま表示されます。
* ``/search-unsafe`` は、入力を f 文字列で HTML に埋め込んでいる悪い例です。``?q=<b>bold</b>`` を開くと、文字が太字で表示され、HTML として解釈されていることが分かります。ただし、``<script>`` を入力しても実行はされません。``set_security_headers()`` で設定した CSP がインラインのスクリプトを禁止しているためです。これは多層防御の効果を示す例です。
* 送金のフォームには CSRF トークンを埋め込み、``transfer()`` で検証しています。トークンがない、または一致しない場合は 403 エラーになります。
* セッション Cookie には HttpOnly と SameSite=Lax を設定しています。このデモは HTTP で動かすため Secure 属性を無効にしていますが、本番環境では必ず有効にします。
* Flask の標準のセッションは、内容に署名して改ざんを防ぎますが、暗号化はしません。利用者は Cookie の内容を読めるため、秘密にすべき情報を保存してはいけません。

起動したアプリケーションに Flask のテストクライアントからアクセスすると、次のようなヘッダーが返されます。

.. code-block:: text
   :caption: 応答ヘッダーの例（抜粋）
   :linenos:

   Content-Security-Policy: default-src 'self'; frame-ancestors 'none'
   X-Content-Type-Options: nosniff
   Referrer-Policy: strict-origin-when-cross-origin
   Set-Cookie: session=eyJjc3JmX3Rva2VuIjoi...; HttpOnly; Path=/; SameSite=Lax

API のセキュリティ
------------------

画面を持たず、JSON などでデータをやり取りする API も、ここまでに説明した脆弱性の多くの影響を受けます。加えて、API に特有の注意点があります。OWASP は、API に特化したリスクの一覧として OWASP API Security Top 10 を公開しています。主な項目と対策を次の表に示します。

.. list-table:: API に特有の主なリスク
   :header-rows: 1
   :widths: 30 40 30

   * - リスク
     - 内容
     - 対策
   * - オブジェクトレベルの認可の不備
     - ID を書き換えると他人のデータにアクセスできます（IDOR と同じです）。
     - データごとに権限を確認します。
   * - プロパティレベルの認可の不備
     - 応答に不要な項目（パスワードのハッシュ値など）が含まれる、または更新してはいけない項目を更新できます。
     - 応答に含める項目と、更新を許可する項目を明示的に定義します。
   * - 機能レベルの認可の不備
     - 一般の利用者が、管理者向けの API を呼び出せます。
     - API ごとに必要なロールを確認します。
   * - リソース消費の制限の不備
     - 大量のリクエストや巨大なデータで、サービスの停止や高額な課金を引き起こされます。
     - レート制限、ページサイズとリクエストサイズの上限
   * - API の管理の不備
     - 古いバージョンや開発用の API が公開されたまま放置されています。
     - 公開している API の一覧を管理し、不要なものを廃止します。

API は画面からは見えないため、「隠れているから安全」と考えがちですが、攻撃者はブラウザーの開発者ツールやスマートフォンアプリの通信から、API の仕様を簡単に調べられます。すべての API で、認証と認可を確実に行う必要があります。
