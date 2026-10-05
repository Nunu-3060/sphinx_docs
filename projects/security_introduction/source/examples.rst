サンプルコード一覧
==================

本書で使用したサンプルコードの一覧です。ファイル名のリンクからダウンロードできます。各サンプルのソースコードと実行結果は、「掲載箇所」の章で閲覧できます。

実行方法
--------

サンプルコードは、ダウンロードしたディレクトリで次のように実行します。

.. code-block:: console
   :linenos:

   python -m pip install -r requirements.txt
   python sql_injection.py

1 行目は、追加ライブラリを使うサンプルを実行する場合に必要です。最初に一度だけ実行します。動作確認環境は\ :doc:`01_introduction`\ を参照してください。

.. warning::

   サンプルコードには、脆弱性の仕組みを示すために、意図的に脆弱な実装（悪い例）が含まれています。悪い例のコードを実際のアプリケーションに使わないでください。

ライブラリの一覧
----------------

* :download:`requirements.txt <../examples/requirements.txt>`

一覧
----

.. list-table:: サンプルコードの一覧
   :header-rows: 1
   :widths: 30 22 30 18

   * - ファイル
     - 掲載箇所
     - 内容
     - 追加ライブラリ
   * - :download:`encoding_is_not_encryption.py <../examples/encoding_is_not_encryption.py>`
     - :doc:`03_cryptography`
     - エンコード・暗号化・ハッシュの違い
     - なし
   * - :download:`ecb_pattern.py <../examples/ecb_pattern.py>`
     - :doc:`03_cryptography`
     - ECB モードの問題点
     - cryptography
   * - :download:`aes_gcm.py <../examples/aes_gcm.py>`
     - :doc:`03_cryptography`
     - AES-GCM による暗号化と改ざん検知
     - cryptography
   * - :download:`hash_and_hmac.py <../examples/hash_and_hmac.py>`
     - :doc:`03_cryptography`
     - ハッシュ値と HMAC の違い
     - なし
   * - :download:`digital_signature.py <../examples/digital_signature.py>`
     - :doc:`03_cryptography`
     - Ed25519 によるデジタル署名
     - cryptography
   * - :download:`secure_random.py <../examples/secure_random.py>`
     - :doc:`03_cryptography`
     - random モジュールと secrets モジュールの違い
     - なし
   * - :download:`password_hashing.py <../examples/password_hashing.py>`
     - :doc:`04_authentication`
     - Argon2id によるパスワードの保存
     - argon2-cffi
   * - :download:`login_throttle.py <../examples/login_throttle.py>`
     - :doc:`04_authentication`
     - ログイン試行の制限
     - なし
   * - :download:`totp.py <../examples/totp.py>`
     - :doc:`04_authentication`
     - TOTP の実装
     - なし
   * - :download:`jwt_verification.py <../examples/jwt_verification.py>`
     - :doc:`04_authentication`
     - JWT の発行と安全な検証
     - PyJWT
   * - :download:`tls_certificate_check.py <../examples/tls_certificate_check.py>`
     - :doc:`05_network`
     - TLS 接続と証明書の確認（インターネット接続が必要）
     - なし
   * - :download:`access_control.py <../examples/access_control.py>`
     - :doc:`06_web_application`
     - アクセス制御の不備（IDOR）と対策
     - なし
   * - :download:`sql_injection.py <../examples/sql_injection.py>`
     - :doc:`06_web_application`
     - SQL インジェクションと対策
     - なし
   * - :download:`command_injection.py <../examples/command_injection.py>`
     - :doc:`06_web_application`
     - OS コマンドインジェクションと対策
     - なし
   * - :download:`xss_escape.py <../examples/xss_escape.py>`
     - :doc:`06_web_application`
     - XSS と出力のエスケープ
     - なし
   * - :download:`ssrf_url_check.py <../examples/ssrf_url_check.py>`
     - :doc:`06_web_application`
     - SSRF を防ぐための URL の検証（名前解決あり）
     - なし
   * - :download:`path_traversal.py <../examples/path_traversal.py>`
     - :doc:`06_web_application`
     - パストラバーサルと対策
     - なし
   * - :download:`flask_security_demo.py <../examples/flask_security_demo.py>`
     - :doc:`06_web_application`
     - Flask による XSS・CSRF 対策、Cookie の属性、セキュリティヘッダー
     - Flask
   * - :download:`unsafe_deserialization.py <../examples/unsafe_deserialization.py>`
     - :doc:`07_secure_coding`
     - pickle の危険性
     - なし
   * - :download:`constant_time_compare.py <../examples/constant_time_compare.py>`
     - :doc:`07_secure_coding`
     - タイミング攻撃と定数時間比較
     - なし
   * - :download:`redos.py <../examples/redos.py>`
     - :doc:`07_secure_coding`
     - 正規表現によるサービス拒否（ReDoS）
     - なし
   * - :download:`log_masking.py <../examples/log_masking.py>`
     - :doc:`07_secure_coding`
     - ログの機密情報の伏せ字化
     - なし
   * - :download:`iam_policy_check.py <../examples/iam_policy_check.py>`
     - :doc:`09_cloud_and_container`
     - IAM ポリシーの過剰な権限の検出
     - なし
   * - :download:`prompt_injection.py <../examples/prompt_injection.py>`
     - :doc:`10_ai_llm`
     - 間接プロンプトインジェクションと権限設計
     - なし
   * - :download:`simple_fuzzer.py <../examples/simple_fuzzer.py>`
     - :doc:`11_testing_and_threat_modeling`
     - 簡単なファザー
     - なし
   * - :download:`auth_log_monitor.py <../examples/auth_log_monitor.py>`
     - :doc:`12_operations`
     - 認証ログからの不審なアクセスの検知
     - なし

第 8 章と第 11 章では、bandit と pip-audit をコマンドラインツールとして使用しています。これらも requirements.txt に含まれています。
