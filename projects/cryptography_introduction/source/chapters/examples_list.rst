サンプルコード一覧
==================

本書のサンプルコードの一覧を示す。ファイル名のリンクからダウンロードできる。依存関係の列が「cryptography」のものは、``pip install cryptography`` でライブラリをインストールしてから実行する。

.. list-table:: サンプルコード一覧
   :header-rows: 1
   :widths: 28 10 44 18

   * - ファイル
     - 章
     - 内容
     - 依存関係
   * - :download:`caesar.py <../../examples/caesar.py>`
     - 2
     - シーザー暗号の暗号化・復号と全数探索
     - 標準ライブラリ
   * - :download:`vigenere.py <../../examples/vigenere.py>`
     - 2
     - ヴィジュネル暗号と、一致指数・カイ二乗値による解読
     - 標準ライブラリ
   * - :download:`one_time_pad.py <../../examples/one_time_pad.py>`
     - 2
     - ワンタイムパッドと鍵の再利用の危険性
     - 標準ライブラリ
   * - :download:`modular_arith.py <../../examples/modular_arith.py>`
     - 3
     - 拡張ユークリッド法、モジュラ逆元、繰り返し二乗法、中国剰余定理
     - 標準ライブラリ
   * - :download:`primality.py <../../examples/primality.py>`
     - 3
     - ミラー・ラビン素数判定法と素数の生成
     - 標準ライブラリ
   * - :download:`aes_modes.py <../../examples/aes_modes.py>`
     - 4
     - AES の ECB / CBC / CTR モードの比較
     - cryptography
   * - :download:`hash_demo.py <../../examples/hash_demo.py>`
     - 5
     - ハッシュ値の計算と雪崩効果
     - 標準ライブラリ
   * - :download:`birthday_attack.py <../../examples/birthday_attack.py>`
     - 5
     - 出力を切り詰めた SHA-256 に対する誕生日攻撃
     - 標準ライブラリ
   * - :download:`hmac_demo.py <../../examples/hmac_demo.py>`
     - 5
     - HMAC によるメッセージ認証
     - 標準ライブラリ
   * - :download:`password_hash.py <../../examples/password_hash.py>`
     - 5
     - scrypt によるパスワードの保存と検証
     - 標準ライブラリ
   * - :download:`aead_demo.py <../../examples/aead_demo.py>`
     - 6
     - AES-GCM と ChaCha20-Poly1305 による暗号化と改ざん検知
     - cryptography
   * - :download:`toy_rsa.py <../../examples/toy_rsa.py>`
     - 7
     - 教科書的 RSA のおもちゃ実装と、その問題点
     - 標準ライブラリ
   * - :download:`rsa_oaep.py <../../examples/rsa_oaep.py>`
     - 7
     - RSA-OAEP とハイブリッド暗号
     - cryptography
   * - :download:`toy_dh.py <../../examples/toy_dh.py>`
     - 8
     - Diffie-Hellman 鍵共有と中間者攻撃
     - 標準ライブラリ
   * - :download:`toy_ecc.py <../../examples/toy_ecc.py>`
     - 9
     - 有限体上の楕円曲線の点演算と ECDH
     - 標準ライブラリ
   * - :download:`x25519_demo.py <../../examples/x25519_demo.py>`
     - 9
     - X25519 鍵共有と HKDF
     - cryptography
   * - :download:`ecdsa_nonce_reuse.py <../../examples/ecdsa_nonce_reuse.py>`
     - 10
     - ECDSA とナンスの再利用による秘密鍵の復元
     - 標準ライブラリ
   * - :download:`signatures_demo.py <../../examples/signatures_demo.py>`
     - 10
     - RSA-PSS、ECDSA、Ed25519 による署名と検証
     - cryptography
   * - :download:`inspect_cert.py <../../examples/inspect_cert.py>`
     - 11
     - 証明書の生成と証明書チェーンの検証
     - cryptography
   * - :download:`secure_random.py <../../examples/secure_random.py>`
     - 12
     - ``random`` と ``secrets`` の違い
     - 標準ライブラリ
   * - :download:`timing_attack.py <../../examples/timing_attack.py>`
     - 12
     - 素朴な比較関数に対するタイミング攻撃
     - 標準ライブラリ
   * - :download:`padding_oracle.py <../../examples/padding_oracle.py>`
     - 12
     - AES-CBC に対するパディングオラクル攻撃
     - cryptography
   * - :download:`secret_sharing.py <../../examples/secret_sharing.py>`
     - 13
     - シャミアの秘密分散法
     - 標準ライブラリ

コードの検査
------------

サンプルコードは、flake8（PEP 8 への準拠の検査）と mypy（型ヒントの検査）で違反が検出されないことを確認している。検査の設定は、``examples`` フォルダ直下の ``setup.cfg`` に記述している。

.. literalinclude:: ../../examples/setup.cfg
   :language: ini
   :linenos:
   :caption: setup.cfg

:download:`setup.cfg をダウンロード <../../examples/setup.cfg>`

flake8 では 1 行の長さを 120 文字まで許容し、mypy では ``strict = True`` によって全ての関数に型ヒントを要求している。検査は ``examples`` フォルダで次のコマンドを実行して行う。

.. code-block:: console
   :linenos:

   pip install flake8 mypy cryptography
   python -m flake8 .
   python -m mypy .
