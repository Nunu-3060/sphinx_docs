用語集
======

本書で使う主な用語を、読みの五十音順（英字の用語は末尾）に並べる。括弧内は英語の表記である。

.. glossary::

   暗号化
      平文を、鍵を使って暗号文に変換する操作（encryption）。

   暗号文
      暗号化された後のデータ（ciphertext）。

   暗号利用モード
      ブロック暗号を繰り返し使って、任意の長さのデータを暗号化する方法（mode of operation）。ECB、CBC、CTR、GCM などがある。

   暗号論的擬似乱数生成器
      出力を観測しても以降の出力を予測できない擬似乱数生成器（cryptographically secure pseudorandom number generator、CSPRNG）。Python では ``secrets`` モジュールや ``os.urandom()`` が該当する。

   オラクル
      攻撃者の問い合わせに対して、特定の情報（復号できたか、パディングが正しいかなど）を答える存在（oracle）。

   鍵
      暗号化、復号、署名などの処理を決める秘密の（または公開の）パラメータ（key）。

   鍵導出関数
      共有秘密やパスワードなどから、暗号に使う鍵を生成する関数（key derivation function、KDF）。HKDF、PBKDF2 などがある。

   完全秘匿性
      暗号文を見ても、平文について一切の情報が得られないという性質（perfect secrecy）。ワンタイムパッドが満たす。

   関連データ
      AEAD において、暗号化はしないが改ざんの検知の対象とするデータ（associated data）。

   共通鍵暗号
      暗号化と復号に同じ鍵を使う暗号（symmetric-key cryptography）。対称鍵暗号とも呼ぶ。

   ケルクホフスの原理
      暗号方式の安全性は、鍵の秘密性だけに依存すべきであり、アルゴリズムの秘密性に依存してはならないという原則（Kerckhoffs's principle）。

   公開鍵
      公開鍵暗号やデジタル署名で、誰に公開してもよい鍵（public key）。

   公開鍵暗号
      暗号化と復号に異なる鍵を使い、暗号化に使う鍵を公開できる暗号（public-key cryptography）。非対称鍵暗号とも呼ぶ。

   公開鍵証明書
      公開鍵とその持ち主の情報に、認証局がデジタル署名したもの（public key certificate）。インターネットでは X.509 形式が使われる。

   サイドチャネル攻撃
      処理時間、消費電力、電磁波など、暗号処理に付随して漏れる情報を利用する攻撃（side-channel attack）。

   衝突
      ハッシュ関数において、異なる入力が同じハッシュ値になること（collision）。

   初期化ベクトル
      CBC モードなどで、最初のブロックの処理に使う値（initialization vector、IV）。

   ストリーム暗号
      鍵から生成した擬似乱数列（鍵ストリーム）と平文の排他的論理和を取って暗号化する暗号（stream cipher）。ChaCha20 などがある。

   ストレッチング
      パスワードのハッシュ値の計算を意図的に遅くして、総当たり攻撃のコストを上げる手法（stretching）。

   セキュリティビット
      最良の攻撃に必要な計算量が :math:`2^s` のとき、その暗号方式の強度を :math:`s` ビットと表したもの（security strength）。安全性のビット数とも呼ぶ。

   前方秘匿性
      長期的に使う秘密鍵が漏洩しても、過去の通信の安全性が保たれる性質（forward secrecy）。

   ソルト
      パスワードのハッシュ値を計算する際に、利用者ごとに加えるランダムな値（salt）。

   耐量子暗号
      量子計算機を使っても効率よく解読できないと考えられている暗号（post-quantum cryptography、PQC）。ML-KEM、ML-DSA などがある。

   楕円曲線離散対数問題
      楕円曲線上の点 :math:`G` と :math:`Q = dG` から :math:`d` を求める問題（elliptic curve discrete logarithm problem、ECDLP）。

   中間者攻撃
      通信する 2 者の間に入り込み、双方になりすまして通信を盗聴・改ざんする攻撃（man-in-the-middle attack）。

   デジタル署名
      秘密鍵で作成し、公開鍵で検証する署名（digital signature）。完全性、認証、否認防止を提供する。

   トラップドア一方向性関数
      順方向の計算は容易だが、逆方向の計算は特別な情報（トラップドア）を知らなければ困難な関数（trapdoor one-way function）。

   ナンス
      同じ鍵の下で 1 回だけ使う値（nonce、number used once）。必ずしも秘密や乱数である必要はないが、重複してはならない。

   認証局
      公開鍵証明書を発行し、公開鍵とその持ち主の対応を保証する機関（certification authority、CA）。

   認証付き暗号
      機密性と完全性を同時に提供する暗号方式（authenticated encryption）。関連データも扱えるものを AEAD と呼ぶ。AES-GCM、ChaCha20-Poly1305 などがある。

   ハイブリッド暗号
      データを共通鍵暗号で暗号化し、その共通鍵を公開鍵暗号で暗号化して送る方式（hybrid encryption）。

   ハッシュ関数
      任意の長さの入力から固定長の値を計算する関数（hash function）。暗号学的ハッシュ関数には原像計算困難性、第二原像計算困難性、衝突困難性が求められる。

   パディング
      データの長さを規定の長さに揃えるために付け加える詰め物（padding）。

   秘密鍵
      公開鍵暗号やデジタル署名で、持ち主だけが秘密に保持する鍵（private key）。

   復号
      正当な受信者が、鍵を使って暗号文を平文に戻す操作（decryption）。

   ブロック暗号
      固定長のブロック単位で暗号化する共通鍵暗号（block cipher）。AES などがある。

   平文
      暗号化される前のデータ（plaintext）。

   離散対数問題
      :math:`g` と :math:`y = g^x \bmod p` から :math:`x` を求める問題（discrete logarithm problem、DLP）。

   ワンタイムパッド
      平文と同じ長さの一様ランダムな鍵との排他的論理和で暗号化し、鍵を 1 回しか使わない暗号（one-time pad）。

   HMAC
      ハッシュ関数を使って構成した MAC（hash-based message authentication code）。RFC 2104 で規定されている。

   MAC
      共通鍵を使ってメッセージのタグを計算し、改ざんを検知する仕組み（message authentication code、メッセージ認証コード）。
