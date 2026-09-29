====================
外部ツールとの連携
====================

実際の開発現場で頻繁に組み合わされるツール群との連携方法を紹介します。

.. note::
   ``sample-app/deploy.sh``\ （:download:`ダウンロード <../../sample-app/deploy.sh>`、全文は「デプロイ先との連携」に掲載）は、そこで説明するデプロイ処理を模した最小のスクリプトです。また、通知連携のスタブ実装は :download:`sample-app/shared-library-example/vars/notifySlack.groovy <../../sample-app/shared-library-example/vars/notifySlack.groovy>` に収録しています。

ビルドエージェントとしての Docker
========================================

.. note::
   :doc:`02_installation` で扱った「Jenkins 自体を Docker で動かす」話とは異なり、ここでは Docker を\ **ビルド・テストの実行環境**\ として使う方法を扱います。

``agent`` ディレクティブに ``docker`` を指定すると、ステージ実行時に指定したイメージのコンテナが起動され、その中で ``steps`` が実行されます。

.. code-block:: groovy

   pipeline {
       agent none

       stages {
           stage('Test with Python 3.12') {
               agent {
                   docker { image 'python:3.12-slim' }
               }
               steps {
                   sh 'pip install -r requirements.txt'
                   sh 'pytest'
               }
           }
       }
   }

エージェント上に Python や特定のバージョンのツールチェインをインストールしておく代わりに、必要なイメージをその場で使い捨てることができます。CI 環境を「毎回同じイメージから作り直す」ことで、「自分の環境だけでは動く」問題を減らせるのが最大の利点です。

コンテナの中からさらに Docker コマンドを使いたい場合（アプリケーションのコンテナイメージをビルドする場合など）は、Docker in Docker（DinD）または、ホストの Docker デーモンをソケット経由でそのまま使う方法（DooD, Docker outside of Docker）が必要になります。DinD は独立性が高い一方でオーバーヘッドが大きく、DooD は手軽な一方でホストの Docker デーモンを共有するためセキュリティ上の分離が弱くなる、というトレードオフがあります。

認証情報（Credentials）の管理
================================

パスワードや API トークン、SSH の秘密鍵といった秘密情報を Jenkinsfile に直接書き込むと、リポジトリの履歴にそのまま残ってしまいます。**Credentials プラグイン**\ （多くの配布に標準で含まれます）は、こうした秘密情報を Jenkins 側で暗号化して保管し、ID を通じて参照する仕組みを提供します。

Credentials は「Manage Jenkins > Credentials」から登録します。主な種類は次のとおりです。

* **Username with password** — 単純な ID/パスワードの組
* **SSH Username with private key** — Git の SSH アクセス等に使う秘密鍵
* **Secret text** — API トークンなど単一の文字列
* **Secret file** — 設定ファイルなど、ファイルとして扱いたい秘密情報

Pipeline から利用する際は、``withCredentials`` ステップで「その処理の間だけ」環境変数として展開します。

.. code-block:: groovy

   pipeline {
       agent any
       stages {
           stage('Deploy') {
               steps {
                   withCredentials([
                       usernamePassword(
                           credentialsId: 'deploy-user',
                           usernameVariable: 'DEPLOY_USER',
                           passwordVariable: 'DEPLOY_PASS'
                       )
                   ]) {
                       sh './deploy.sh --user "$DEPLOY_USER" --pass "$DEPLOY_PASS"'
                   }
               }
           }
       }
   }

``credentialsId`` に指定するのは、UI で登録した際に割り振られる識別子であり、値そのものではありません。値は Jenkins が管理するストア内にのみ保存され、Jenkinsfile やコンソールログには（マスキングされた状態でしか）現れません。

.. warning::
   ``echo "$DEPLOY_PASS"`` のように、値をそのままログへ出力するコードを書くと、Jenkins によるマスキングが効かない場合があります。秘密情報をシェル変数として直接組み立てる際は、値がログに残らないか常に確認してください。

通知連携（Slack / メール）
================================

ビルド結果をチームに通知することで、失敗にすぐ気づける状態を作れます。Slack 通知には ``Slack Notification`` プラグインを使うのが一般的です。Slack 側で Jenkins 用の Webhook（または Bot トークン）を発行し、Credentials として登録した上で、``post`` セクションから呼び出します。

.. code-block:: groovy

   pipeline {
       agent any
       stages {
           stage('Test') {
               steps { sh 'pytest' }
           }
       }
       post {
           failure {
               slackSend(
                   channel: '#ci-alerts',
                   color: 'danger',
                   message: "ビルド失敗: ${env.JOB_NAME} #${env.BUILD_NUMBER} (${env.BUILD_URL})"
               )
           }
       }
   }

メール通知も同様に、``post`` セクションから ``mail`` ステップ（または ``emailext`` プラグインの拡張版）を呼び出す形で組み込めます。いずれの場合も、:doc:`05_pipeline_syntax` の ``post`` セクションで扱った ``always``/``failure``/``changed`` といった条件と組み合わせ、「失敗した時だけ通知する」「ステータスが変化した時だけ通知する」など、通知過多にならないよう調整するのが実践上のポイントです。

テスト結果・成果物の管理
================================

``junit``/``archiveArtifacts`` 自体の文法は :doc:`05_pipeline_syntax` を参照。ここでは複数ジョブ・複数言語にまたがる実践的な運用パターンを扱います。

**複数のテストレポートを集約する**

言語やツールが異なると、テストレポートも別々のディレクトリに出力されることがあります。``junit`` はパターンにマッチするすべてのファイルを 1 回の呼び出しで集約できます。

.. code-block:: groovy

   post {
       always {
           junit 'reports/**/*.xml'
       }
   }

**成果物の保持ポリシー**

``archiveArtifacts`` で保存した成果物は、:doc:`05_pipeline_syntax` の ``options`` で扱った ``buildDiscarder`` の設定に従って、古いビルドが削除される際に一緒に破棄されます。大きなバイナリを毎ビルド保存すると、保持世代数分のディスク容量が必要になる点に注意してください。

.. code-block:: groovy

   options {
       buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '5'))
   }

上記では、ビルド履歴自体は 20 件、成果物は直近 5 件分だけを残すよう分けて設定しています。

**ステージ間でのファイル受け渡し（stash/unstash）**

複数のエージェントに処理を分散する場合、あるステージで生成したファイルを別のエージェント上のステージに引き渡すには ``stash``/``unstash`` を使います。

.. code-block:: groovy

   stage('Build') {
       steps {
           sh 'python -m build'
           stash name: 'dist', includes: 'dist/**'
       }
   }
   stage('Publish') {
       agent { label 'publish-node' }
       steps {
           unstash 'dist'
           sh './publish.sh dist/*'
       }
   }

``archiveArtifacts`` はビルド結果に永続的に添付するための仕組み、``stash``/``unstash`` は同一ビルド内でステージ間にファイルを一時的に受け渡すための仕組みという役割の違いを押さえておいてください。

デプロイ先との連携
====================

Pipeline の最終段では、多くの場合何らかのデプロイ先へ結果を反映します。代表的な連携先は次のとおりです。

* **Kubernetes** ── ``kubectl`` を実行できるエージェント（または専用の Docker イメージ）から ``kubectl apply``/``kubectl rollout status`` を呼び出す方法が最も直接的です。より高度な運用では、Kubernetes 用の CLI プラグインや、Helm チャートの適用をステップ化して扱います。
* **クラウドサービス（AWS/GCP/Azure 等）** ── 各クラウドの CLI（``aws``/``gcloud``/``az``）を、「Credentials の管理」で扱ったシークレットとともに呼び出すのが基本パターンです。多くのクラウドは専用の Jenkins プラグインも提供していますが、内部的には CLI 呼び出しをラップしているだけの場合が多く、まず CLI ベースの呼び出しを理解しておくと見通しが立てやすいです。

どの連携先であっても、「デプロイ処理自体はシェルスクリプトや CLI コマンドとして書き、Jenkinsfile 側はそれを適切なタイミング・適切な認証情報で呼び出すだけ」という薄い責務にとどめておくと、デプロイ処理自体をローカルでも実行・検証しやすくなります。サンプルリポジトリの ``deploy.sh``\ （:download:`ダウンロード <../../sample-app/deploy.sh>`）は、この考え方を反映した最小のスクリプトです。

.. literalinclude:: ../../sample-app/deploy.sh
   :language: bash
   :caption: deploy.sh
