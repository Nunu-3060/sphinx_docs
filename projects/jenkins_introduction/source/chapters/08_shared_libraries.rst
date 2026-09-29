====================
共有ライブラリ
====================

複数の Jenkinsfile にまたがる重複コードを、再利用可能なライブラリとして切り出す方法を解説します。

.. note::
   サンプルリポジトリの ``sample-app/shared-library-example/`` に、本章で説明する ``vars``/``src``/``resources`` の構成を実際に確認できるサンプルを収録しています。単独リポジトリとして Jenkins に登録した上で読み込む例は :download:`sample-app/Jenkinsfile.with-shared-library <../../sample-app/Jenkinsfile.with-shared-library>`\ （全文は本章末尾に掲載）を、登録手順は :download:`shared-library-example/README.md <../../sample-app/shared-library-example/README.md>` を参照してください。

共有ライブラリとは
====================

前章までの内容だけでも、複数のリポジトリ・複数の ``Jenkinsfile`` を運用していると、同じような ``stage`` 定義や通知処理をコピー＆ペーストする場面が出てきます。これは Python で言えば、複数のスクリプトに同じ関数を毎回書き写しているような状態です。

**Shared Library（共有ライブラリ）**\ は、この重複を解消するための仕組みです。Groovy のコードを専用のリポジトリにまとめておき、各プロジェクトの ``Jenkinsfile`` からライブラリとして読み込みます。Python における自作パッケージを ``pip install`` して ``import`` するのと同じ関係だと考えるとわかりやすいでしょう。

ディレクトリ構成
====================

共有ライブラリ用のリポジトリは、次のような決められたディレクトリ構成を持ちます。

.. code-block:: text

   (root)
   ├── vars/
   │   ├── deployApp.groovy
   │   └── notifySlack.groovy
   ├── src/
   │   └── org/example/pipeline/
   │       └── Deployer.groovy
   └── resources/
       └── org/example/templates/
           └── notification.txt

* ``vars/`` ── ``Jenkinsfile`` から直接呼び出せる「グローバル変数（カスタムステップ）」を置く場所です。ファイル名がそのままステップ名になります。Python でいう、トップレベルに定義された関数に近いイメージです。
* ``src/`` ── 通常の Groovy のクラス定義を置く場所です。パッケージ構成に従ったディレクトリ階層を持ちます。Python のパッケージ内のモジュール（クラス定義を含む ``.py`` ファイル）に相当します。
* ``resources/`` ── ``libraryResource`` 経由で読み込む、テキストファイルなどの静的リソースを置く場所です。

グローバル変数（vars）の作成
================================

``vars/deployApp.groovy`` に次のように定義すると、``Jenkinsfile`` から ``deployApp(...)`` という 1 つのステップとして呼び出せます（:download:`ダウンロード <../../sample-app/shared-library-example/vars/deployApp.groovy>`）。

.. literalinclude:: ../../sample-app/shared-library-example/vars/deployApp.groovy
   :language: groovy
   :caption: vars/deployApp.groovy

これは Python の関数定義 ``def deploy_app(target_env): ...`` を、別モジュールとして切り出して ``import`` しているのと同じ関係です。``call`` という名前のメソッドを定義しておくことで、呼び出し側は関数のようにそのまま呼び出せる、という Groovy 特有の約束事です。

ライブラリの読み込みと運用
================================

``Jenkinsfile`` 側では、``@Library`` アノテーションでライブラリを読み込みます。

.. code-block:: groovy

   @Library('my-shared-library@v1.2.0') _

   pipeline {
       agent any
       stages {
           stage('Deploy') {
               steps {
                   deployApp('production')
               }
           }
       }
   }

``@Library('name@version')`` の ``version`` には、ライブラリ側のリポジトリのタグやブランチ名を指定できます。バージョンを固定しておくと、ライブラリ側の変更が、それを利用する全プロジェクトへ意図せず即時反映されてしまう事態を防げます。これは、依存パッケージのバージョンを ``requirements.txt`` で固定するのと同じ考え方です。

運用上のベストプラクティスとしては、次のような点が挙げられます。

* ライブラリはタグでバージョンを切り、利用側は明示的にバージョンを指定します（``@Library('name@master')`` のような可変参照は避けます）。
* ライブラリ自体にもテスト（Groovy の単体テストフレームワークを使ったステップの検証）を用意し、変更が既存の利用者を壊さないことを確認します。
* Jenkins の管理画面（Manage Jenkins > System）で、組織内の Global Trusted Pipeline Library として登録しておくと、各プロジェクト側で読み込み先リポジトリを個別に指定する必要がなくなります。

サンプル全体（sample-app/Jenkinsfile.with-shared-library）
================================================================

``sample-app/shared-library-example/`` を共有ライブラリとして読み込む場合の Jenkinsfile 全体です。実際に動かす手順は :download:`shared-library-example/README.md <../../sample-app/shared-library-example/README.md>` を参照してください。

.. literalinclude:: ../../sample-app/Jenkinsfile.with-shared-library
   :language: groovy
   :linenos:
