========================================
マルチブランチパイプライン
========================================

リポジトリ内の複数ブランチ・プルリクエストを自動的に検出し、それぞれに対して Pipeline を実行する仕組みを解説します。

.. note::
   サンプルリポジトリ ``sample-app`` の ``Jenkinsfile``\ （:download:`ダウンロード <../../sample-app/Jenkinsfile>`、全文は :doc:`05_pipeline_syntax` 末尾に掲載）は、``develop``/``main`` ブランチを想定した ``when { branch ... }`` による分岐を含んでいます。``sample-app/README.md`` の手順に従って両ブランチを作成し、Multibranch Pipeline ジョブとして読み込むと、本章の内容を実際に確認できます。

Multibranch Pipeline ジョブの概念
====================================

これまでの章で作成した「Pipeline」ジョブは、あらかじめ指定した 1 つのブランチだけを対象にしていました。しかし実際の開発では、機能開発用のブランチごとに CI を走らせたい場面がほとんどです。

**Multibranch Pipeline** ジョブは、リポジトリをスキャンし、``Jenkinsfile`` を含むブランチを自動的に検出して、ブランチごとにサブジョブを生成します。新しいブランチを push すれば、Jenkins 側で何も設定を追加しなくても、そのブランチ用のサブジョブが自動的に作られます。逆に、ブランチが削除されると、対応するサブジョブも自動的に破棄されます。

イメージとしては、1 つの ``Jenkinsfile`` というテンプレートに対して、ブランチという「実行コンテキスト」を渡しながら実体化している、と捉えるとよいでしょう。

ブランチ戦略との関係
========================

Multibranch Pipeline は、Git Flow や GitHub Flow といったブランチ戦略と組み合わせて使われます。

* **GitHub Flow**\ （``main`` + 機能ブランチ）を採用している場合、``main`` へのマージ前に各機能ブランチで CI を走らせ、マージ後に ``main`` ブランチ自体でデプロイ用の Pipeline を走らせる、という使い分けが典型的です。
* **Git Flow**\ （``develop``/``release``/``hotfix`` 等の複数ブランチ）を採用している場合、ブランチの種類ごとに実行する内容を変えたくなる場面が増えます。これは次項の「Jenkinsfile の共通化」で扱う ``when`` や環境変数による分岐で対応します。

ブランチ戦略そのものを Jenkins が強制するわけではなく、「どのブランチにどんな Pipeline を実行させたいか」というチームのルールを、Jenkinsfile 側の条件分岐で表現する、という関係になります。

プルリクエストビルド
========================

GitHub や GitLab と連携すると、プルリクエスト（マージリクエスト）そのものに対してもビルドを実行できます。これは「マージする前に CI を通す」という、レビューフローの安全性を高めるための仕組みです。

Multibranch Pipeline ジョブの設定で、対象に「Discover pull requests from origin」（GitHub の場合）を追加すると、プルリクエストごとにサブジョブが作られます。GitHub 側のステータスチェックと連携させれば、CI が通らないプルリクエストはマージボタンが無効化される、という運用も可能です。

.. note::
   フォークからのプルリクエストをビルドする場合、送られてきたコードがそのまま ``sh`` ステップ等で実行されることになります。Credentials の扱いには特に注意が必要です（:doc:`09_integration` 参照）。

Jenkinsfile の共通化
========================

ブランチや実行コンテキストが増えても、``Jenkinsfile`` 自体は 1 つのファイルを共通で使うのが基本です。ブランチごとの違いは、:doc:`05_pipeline_syntax` で扱った ``when`` ディレクティブや環境変数の分岐で吸収します。

.. code-block:: groovy

   pipeline {
       agent any

       stages {
           stage('Build & Test') {
               steps {
                   sh 'pytest'
               }
           }
           stage('Deploy to staging') {
               when { branch 'develop' }
               steps {
                   sh './deploy.sh staging'
               }
           }
           stage('Deploy to production') {
               when { branch 'main' }
               steps {
                   sh './deploy.sh production'
               }
           }
       }
   }

このように、「ビルドとテストはすべてのブランチで共通、デプロイ先だけブランチに応じて変える」という形にしておくと、ブランチが増えても ``Jenkinsfile`` を複製する必要がありません。共通処理の重複が増えてきた場合は、次章で扱う\ **共有ライブラリ**\ への切り出しを検討します。
