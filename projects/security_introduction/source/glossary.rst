用語集
======

本書で使用した主な用語を、英字で始まる用語と、日本語で始まる用語（五十音順）に分けて掲載します。

英字で始まる用語
----------------

.. glossary::

   AI エージェント
      LLM が、与えられた目標に向けて自律的にツールを選んで実行し、作業を進める仕組み。:doc:`10_ai_llm`\ を参照。

   CORS
      Cross-Origin Resource Sharing。サーバーが、別のオリジンのページに応答の読み取りを許可するための仕組み。:doc:`06_web_application`\ を参照。

   CSIRT
      Computer Security Incident Response Team。組織内でインシデントへの対応を担うチーム。:doc:`12_operations`\ を参照。

   CSRF
      Cross-Site Request Forgery（クロスサイトリクエストフォージェリ）。利用者が意図しないリクエストを、ログイン中の別のサイトに送らせる攻撃。:doc:`06_web_application`\ を参照。

   CVE
      Common Vulnerabilities and Exposures。公開された脆弱性に割り当てられる識別番号。:doc:`08_supply_chain`\ を参照。

   CVSS
      Common Vulnerability Scoring System。脆弱性の深刻度を 0.0 から 10.0 の数値で表す指標。:doc:`08_supply_chain`\ を参照。

   DNS
      Domain Name System。ドメイン名と IP アドレスを対応付ける仕組み。:doc:`05_network`\ を参照。

   DoS 攻撃
      Denial of Service 攻撃（サービス拒否攻撃）。大量の通信や処理を発生させ、サービスを利用できない状態にする攻撃。多数の機器から行うものを DDoS 攻撃と呼びます。:doc:`02_basic_concepts`\ を参照。

   IaC
      Infrastructure as Code。インフラストラクチャーの構成をコードとして記述し、管理する手法。:doc:`09_cloud_and_container`\ を参照。

   IAM
      Identity and Access Management。クラウドなどで、誰がどのリソースに対してどの操作を行えるかを管理する仕組み。:doc:`09_cloud_and_container`\ を参照。

   IDOR
      Insecure Direct Object Reference。リクエストに含まれる ID を書き換えるだけで、権限のないデータにアクセスできてしまう脆弱性。:doc:`06_web_application`\ を参照。

   JWT
      JSON Web Token。ヘッダー、ペイロード、署名からなる、署名付きのトークンの形式。:doc:`04_authentication`\ を参照。

   LLM
      Large Language Model（大規模言語モデル）。大量の文章で学習し、自然言語の指示に応じて文章を生成するモデル。:doc:`10_ai_llm`\ を参照。

   MAC
      Message Authentication Code（メッセージ認証コード）。共有の秘密鍵を使って、データの改ざんを検知するための値。HMAC はその代表的な方式。:doc:`03_cryptography`\ を参照。

   OAuth 2.0
      利用者の同意に基づいて、アプリケーションに API へのアクセス権限を与えるための認可の仕組み。:doc:`04_authentication`\ を参照。

   OpenID Connect
      OAuth 2.0 の上に、利用者が誰であるかを伝える仕組みを加えた認証の規格。:doc:`04_authentication`\ を参照。

   OS コマンドインジェクション
      利用者の入力がシェルに解釈され、任意の OS のコマンドが実行される脆弱性。:doc:`06_web_application`\ を参照。

   PKI
      Public Key Infrastructure（公開鍵基盤）。認証局が証明書を発行し、公開鍵とその持ち主の対応を保証する仕組み。:doc:`05_network`\ を参照。

   ReDoS
      Regular expression Denial of Service。特定の入力に対して正規表現の照合に膨大な時間がかかることを悪用した、サービス拒否攻撃。:doc:`07_secure_coding`\ を参照。

   SBOM
      Software Bill of Materials（ソフトウェア部品表）。ソフトウェアに含まれるすべての部品を列挙したもの。:doc:`08_supply_chain`\ を参照。

   SQL インジェクション
      利用者の入力によって SQL 文の構造が変えられ、データベースを不正に操作される脆弱性。:doc:`06_web_application`\ を参照。

   SSRF
      Server-Side Request Forgery（サーバーサイドリクエストフォージェリ）。サーバーに、外部から直接アクセスできない内部のシステムへのリクエストを送らせる攻撃。:doc:`06_web_application`\ を参照。

   STRIDE
      脅威を、なりすまし、改ざん、否認、情報漏えい、サービス拒否、権限昇格の 6 種類に分類する手法。:doc:`11_testing_and_threat_modeling`\ を参照。

   TLS
      Transport Layer Security。通信の暗号化、改ざんの検知、通信相手の確認を行うプロトコル。:doc:`05_network`\ を参照。

   TOTP
      Time-based One-Time Password。共有の秘密鍵と現在時刻から、一定時間ごとに変わる確認コードを計算する方式。:doc:`04_authentication`\ を参照。

   VPN
      Virtual Private Network。共有のネットワーク上に、暗号化された仮想的な専用の通信路を作る技術。:doc:`05_network`\ を参照。

   XSS
      Cross-Site Scripting（クロスサイトスクリプティング）。攻撃者が用意したスクリプトを、脆弱な Web サイトのページの一部として利用者のブラウザーで実行させる攻撃。:doc:`06_web_application`\ を参照。

日本語で始まる用語
------------------

.. glossary::

   インシデント
      セキュリティを損なう事象、またはその疑いのある事象。:doc:`12_operations`\ を参照。

   インジェクション
      利用者の入力が、SQL 文やコマンドなどのプログラムの一部として解釈されてしまう脆弱性の総称。:doc:`06_web_application`\ を参照。

   危殆化
      計算機の性能向上や新しい攻撃手法の発見によって、暗号アルゴリズムの安全性が低下すること。:doc:`03_cryptography`\ を参照。

   脅威
      損害を与える可能性のある事象や、それを引き起こす主体。:doc:`02_basic_concepts`\ を参照。

   脅威モデリング
      システムの設計をもとに、考えられる脅威を体系的に洗い出し、対策を決める活動。:doc:`11_testing_and_threat_modeling`\ を参照。

   競合状態
      複数の処理が同時に実行されるときに、実行の順序によって結果が変わってしまう不具合。:doc:`07_secure_coding`\ を参照。

   共通鍵暗号
      暗号化と復号に同じ鍵を使う暗号方式。AES が代表的です。:doc:`03_cryptography`\ を参照。

   公開鍵暗号
      公開鍵と秘密鍵という対になる 2 つの鍵を使う暗号方式。RSA が代表的です。:doc:`03_cryptography`\ を参照。

   最小権限の原則
      利用者やプログラムに、目的を果たすために必要な最小限の権限だけを与える考え方。:doc:`02_basic_concepts`\ を参照。

   シークレット
      パスワード、API キー、暗号鍵など、秘密にすべき情報。:doc:`07_secure_coding`\ を参照。

   ストレッチング
      パスワードのハッシュ値の計算を意図的に重くし、総当たり攻撃を困難にする手法。:doc:`04_authentication`\ を参照。

   脆弱性
      脅威によって悪用される可能性のある、システムの弱点。:doc:`02_basic_concepts`\ を参照。

   静的解析
      プログラムを実行せずに、ソースコードを解析して脆弱性の可能性がある箇所を見つける手法。SAST とも呼びます。:doc:`11_testing_and_threat_modeling`\ を参照。

   責任共有モデル
      クラウドのセキュリティを、クラウド事業者と利用者が分担して担うという考え方。:doc:`09_cloud_and_container`\ を参照。

   セッション ID
      ログインした状態を維持するために、サーバーが利用者に発行する識別子。:doc:`04_authentication`\ を参照。

   ゼロトラスト
      ネットワーク上の位置によって通信を信頼せず、すべてのアクセスを確認したうえで許可する考え方。:doc:`05_network`\ を参照。

   前方秘匿性
      サーバーの秘密鍵が将来漏えいしても、過去の通信を解読できない性質。:doc:`05_network`\ を参照。

   ソーシャルエンジニアリング
      人間の心理や習慣の隙を突いて、情報を盗んだり不正な操作をさせたりする手口の総称。:doc:`02_basic_concepts`\ を参照。

   ソルト
      パスワードのハッシュ値を計算する前に加える、利用者ごとに異なるランダムな値。:doc:`04_authentication`\ を参照。

   タイポスクワッティング
      有名なパッケージやドメインとよく似た名前を使い、入力の誤りによって悪意のあるものを利用させる手口。:doc:`08_supply_chain`\ を参照。

   タイミング攻撃
      処理時間の違いから、秘密の情報を推測する攻撃。:doc:`07_secure_coding`\ を参照。

   耐量子計算機暗号
      量子コンピューターでも解読が困難と考えられる暗号方式。PQC（Post-Quantum Cryptography）とも呼びます。:doc:`03_cryptography`\ を参照。

   多層防御
      複数の対策を重ね、1 つの対策が破られても被害を防げるようにする考え方。:doc:`02_basic_concepts`\ を参照。

   多要素認証
      知識情報、所持情報、生体情報のうち、異なる要素を 2 つ以上組み合わせる認証。:doc:`04_authentication`\ を参照。

   中間者攻撃
      通信の当事者の間に入り込み、両者になりすまして通信を中継しながら盗聴や改ざんを行う攻撃。:doc:`05_network`\ を参照。

   デジタル署名
      秘密鍵で署名を作成し、公開鍵で検証することで、データの完全性と作成者を確認できる技術。:doc:`03_cryptography`\ を参照。

   同一オリジンポリシー
      あるオリジンのページで動く JavaScript が、別のオリジンのデータを読み取ることを制限する、ブラウザーの仕組み。:doc:`06_web_application`\ を参照。

   動的解析
      動作しているアプリケーションに攻撃を模したリクエストを送り、脆弱性を見つける手法。DAST とも呼びます。:doc:`11_testing_and_threat_modeling`\ を参照。

   認可
      認証された相手に、その操作を許可してよいかを判断すること。:doc:`04_authentication`\ を参照。

   認証
      相手が主張どおりの本人であるかを確認すること。:doc:`04_authentication`\ を参照。

   認証付き暗号
      暗号化と同時に改ざん検知用のタグを付ける暗号方式。AES-GCM が代表的です。:doc:`03_cryptography`\ を参照。

   パスキー
      FIDO2（WebAuthn）に基づき、パスワードの代わりに公開鍵暗号を使ってログインする仕組み。:doc:`04_authentication`\ を参照。

   パストラバーサル
      ``../`` などを含むファイル名を指定して、許可されたディレクトリの外にあるファイルにアクセスする攻撃。:doc:`06_web_application`\ を参照。

   パスワードリスト攻撃
      他のサービスから漏えいした ID とパスワードの組を使って、ログインを試みる攻撃。:doc:`04_authentication`\ を参照。

   ハッシュ関数
      任意の長さのデータから、固定長の値を計算する関数。:doc:`03_cryptography`\ を参照。

   ファイアウォール
      あらかじめ定めた規則に従って、通信を許可または遮断する仕組み。:doc:`05_network`\ を参照。

   ファジング
      ランダムな入力などを大量に与えて、異常な動作を引き起こす入力を探すテストの手法。:doc:`11_testing_and_threat_modeling`\ を参照。

   フィッシング
      実在する組織を装ったメールなどで偽のサイトに誘導し、パスワードなどを入力させる手口。:doc:`02_basic_concepts`\ を参照。

   プロンプトインジェクション
      細工した文章によって、LLM に開発者の意図しない動作をさせる攻撃。:doc:`10_ai_llm`\ を参照。

   ペネトレーションテスト
      専門家が攻撃者の視点で実際にシステムへの侵入を試み、脆弱性と被害を評価するテスト。:doc:`11_testing_and_threat_modeling`\ を参照。

   ランサムウェア
      データを暗号化して使えなくし、復旧と引き換えに金銭を要求するマルウェア。:doc:`02_basic_concepts`\ を参照。

   リスク
      脅威が脆弱性を悪用して損害が発生する可能性と、その影響の大きさ。:doc:`02_basic_concepts`\ を参照。
