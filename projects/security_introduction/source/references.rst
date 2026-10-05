参考文献
========

本書の執筆にあたって参照した資料と、さらに学ぶための資料を掲載します。Web 上の資料は、2026 年 10 月時点の URL です。

公的機関の資料
--------------

* IPA「`安全なウェブサイトの作り方 <https://www.ipa.go.jp/security/vuln/websecurity/about.html>`__」
* IPA「`情報セキュリティ10大脅威 <https://www.ipa.go.jp/security/10threats/index.html>`__」
* IPA「`脆弱性関連情報の届出受付 <https://www.ipa.go.jp/security/todokede/vuln/index.html>`__」
* IPA「`情報処理安全確保支援士試験 <https://www.ipa.go.jp/shiken/kubun/sc.html>`__」
* `JVN（Japan Vulnerability Notes） <https://jvn.jp/>`__
* `JPCERT コーディネーションセンター <https://www.jpcert.or.jp/>`__
* CRYPTREC「`CRYPTREC 暗号リスト <https://www.cryptrec.go.jp/list.html>`__」
* `個人情報保護委員会 <https://www.ppc.go.jp/>`__
* CISA「`Known Exploited Vulnerabilities Catalog <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>`__」

NIST の資料
-----------

* `NIST SP 800-63B: Digital Identity Guidelines - Authentication and Authenticator Management <https://pages.nist.gov/800-63-4/sp800-63b.html>`__
* `NIST SP 800-207: Zero Trust Architecture <https://csrc.nist.gov/pubs/sp/800/207/final>`__
* `NIST Cybersecurity Framework <https://www.nist.gov/cyberframework>`__
* `FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard <https://csrc.nist.gov/pubs/fips/203/final>`__
* `FIPS 204: Module-Lattice-Based Digital Signature Standard <https://csrc.nist.gov/pubs/fips/204/final>`__
* `FIPS 205: Stateless Hash-Based Digital Signature Standard <https://csrc.nist.gov/pubs/fips/205/final>`__

OWASP の資料
------------

* `OWASP Top 10:2025 <https://top10.owasp.org/2025/>`__
* `OWASP API Security Top 10 2023 <https://api-security.owasp.org/editions/2023/en/0x11-t10/>`__
* `OWASP Top 10 for LLM Applications <https://genai.owasp.org/llm-top-10/>`__
* `OWASP Cheat Sheet Series <https://cheatsheetseries.owasp.org/>`__
* `OWASP Password Storage Cheat Sheet <https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html>`__
* `OWASP Juice Shop <https://owasp.org/projects/juice-shop>`__

RFC
---

.. list-table:: 本書で参照した RFC
   :header-rows: 1
   :widths: 20 80

   * - 番号
     - 題名
   * - `RFC 4226 <https://www.rfc-editor.org/rfc/rfc4226>`__
     - HOTP: An HMAC-Based One-Time Password Algorithm
   * - `RFC 6238 <https://www.rfc-editor.org/rfc/rfc6238>`__
     - TOTP: Time-Based One-Time Password Algorithm
   * - `RFC 6749 <https://www.rfc-editor.org/rfc/rfc6749>`__
     - The OAuth 2.0 Authorization Framework
   * - `RFC 6797 <https://www.rfc-editor.org/rfc/rfc6797>`__
     - HTTP Strict Transport Security (HSTS)
   * - `RFC 7519 <https://www.rfc-editor.org/rfc/rfc7519>`__
     - JSON Web Token (JWT)
   * - `RFC 7636 <https://www.rfc-editor.org/rfc/rfc7636>`__
     - Proof Key for Code Exchange by OAuth Public Clients
   * - `RFC 8446 <https://www.rfc-editor.org/rfc/rfc8446>`__
     - The Transport Layer Security (TLS) Protocol Version 1.3
   * - `RFC 8996 <https://www.rfc-editor.org/rfc/rfc8996>`__
     - Deprecating TLS 1.0 and TLS 1.1
   * - `RFC 9106 <https://www.rfc-editor.org/rfc/rfc9106>`__
     - Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications
   * - `RFC 9116 <https://www.rfc-editor.org/rfc/rfc9116>`__
     - A File Format to Aid in Security Vulnerability Disclosure

脆弱性情報とサプライチェーン
----------------------------

* `CVE <https://www.cve.org/>`__
* FIRST「`Common Vulnerability Scoring System <https://www.first.org/cvss/>`__」
* FIRST「`Exploit Prediction Scoring System <https://www.first.org/epss/>`__」
* `CycloneDX <https://cyclonedx.org/>`__
* `SPDX <https://spdx.dev/>`__
* `SLSA <https://slsa.dev/>`__
* `Sigstore <https://www.sigstore.dev/>`__

認証
----

* FIDO Alliance「`Passkeys <https://fidoalliance.org/passkeys/>`__」
* `security.txt <https://securitytxt.org/>`__

Python とライブラリのドキュメント
----------------------------------

* `secrets --- 機密を扱うために安全な乱数を生成する <https://docs.python.org/ja/3/library/secrets.html>`__
* `hmac --- メッセージ認証のための鍵付きハッシュ化 <https://docs.python.org/ja/3/library/hmac.html>`__
* `ssl --- ソケットオブジェクトに対する TLS/SSL ラッパー <https://docs.python.org/ja/3/library/ssl.html>`__
* `cryptography <https://cryptography.io/>`__
* `argon2-cffi <https://argon2-cffi.readthedocs.io/>`__
* `PyJWT <https://pyjwt.readthedocs.io/>`__
* `Flask <https://flask.palletsprojects.com/>`__
* `Bandit <https://bandit.readthedocs.io/>`__
* `pip-audit <https://github.com/pypa/pip-audit>`__
