====================================
Declarative Pipeline 構文の詳細
====================================

Declarative Pipeline の主要なディレクティブを、プログラミング言語の構文要素になぞらえながら解説します。

.. note::
   本章で扱う ``agent``/``options``/``triggers``/``parameters``/``when``/``post``/``parallel``/``input`` のうち、``triggers`` 以外はサンプルリポジトリの ``sample-app/Jenkinsfile`` に一通り実例として含まれています（``triggers`` を使わない理由は該当節で説明します）。手元で動かしながら読み進めると理解しやすくなります。ファイル全体は本章末尾に掲載しているほか、:download:`ここから直接ダウンロード <../../sample-app/Jenkinsfile>` することもできます。

agent ディレクティブ
======================

``agent`` は、Pipeline（またはステージ単位）をどこで実行するかを指定するディレクティブです。

.. code-block:: groovy

   pipeline {
       agent { label 'linux && docker' }
       // ...
   }

主な指定方法は次のとおりです。

* ``agent any`` ── 利用可能な任意のエージェントで実行します。
* ``agent none`` ── トップレベルでは実行環境を確保せず、各 ``stage`` 側で個別に ``agent`` を指定することを強制します。ステージごとに異なる実行環境（OS やコンテナ）を使い分けたい場合に使います。
* ``agent { label 'xxx' }`` ── 指定したラベルを持つエージェントで実行します。ラベルは :doc:`02_installation` で触れたエージェント側に設定する任意の文字列で、``linux``、``gpu`` のように実行環境の特徴を表すことが多いです。
* ``agent { docker { image 'python:3.12' } }`` ── 指定した Docker イメージをコンテナとして起動し、その中で実行します。詳細は :doc:`09_integration` で扱います。

options ディレクティブ
==========================

``options`` は、個々のステップではなく Pipeline 全体の挙動を設定するディレクティブです。関数のデコレータに近い位置づけと考えるとイメージしやすいでしょう。

.. code-block:: groovy

   pipeline {
       agent any

       options {
           timeout(time: 30, unit: 'MINUTES')
           retry(2)
           disableConcurrentBuilds()
           buildDiscarder(logRotator(numToKeepStr: '30'))
       }
       // ...
   }

* ``timeout(time: 30, unit: 'MINUTES')`` ── Pipeline 全体の実行時間に上限を設けます。ハングしたビルドがエージェントを占有し続けるのを防ぎます。
* ``retry(2)`` ── 失敗した場合に、指定回数まで自動的に再実行します。ネットワークの一時的な不調など、リトライで解決する問題に有効です。
* ``disableConcurrentBuilds()`` ── 同じジョブの複数ビルドが同時に走らないようにします。デプロイ先を共有するジョブなど、並行実行が競合を招く場合に使います。
* ``buildDiscarder(logRotator(numToKeepStr: '30'))`` ── 古いビルド履歴を自動的に削除します。指定しない場合、ビルド履歴とそのログ・成果物が無制限に蓄積され、ディスクを圧迫します。

triggers ディレクティブ
==========================

``triggers`` は、:doc:`03_basic_usage` で扱った Freestyle ジョブの「ビルドトリガーの種類」を、Declarative Pipeline の中で宣言的に記述するためのディレクティブです。

.. code-block:: groovy

   pipeline {
       agent any

       triggers {
           cron('H 2 * * *')
           pollSCM('H/15 * * * *')
       }
       // ...
   }

* ``cron(...)`` ── 指定した cron 形式のスケジュールで、変更の有無にかかわらず定期的にビルドを起動します。夜間バッチのように、コミットの有無とは無関係に毎日決まった時刻に実行したい処理に向いています。
* ``pollSCM(...)`` ── 指定した間隔でリポジトリをポーリングし、新しいコミットがあった場合にのみビルドを起動します。:doc:`03_basic_usage` で触れた「SCM ポーリング」の Pipeline 版です。

:doc:`07_multibranch` で扱う Multibranch Pipeline では、リポジトリのスキャン自体が Webhook あるいは定期スキャンによって行われるため、多くの場合 ``triggers`` を明示的に書く必要はありません。``triggers`` が主に役立つのは、単一の Jenkinsfile を対象とする通常の Pipeline ジョブで、Webhook を設定できない環境において定期的な確認や夜間バッチを組みたい場合です。サンプルリポジトリ ``sample-app`` は Multibranch Pipeline を前提としているため、``sample-app/Jenkinsfile`` には ``triggers`` の実例を含めていません。

environment と parameters
============================

``environment`` と ``parameters`` は、いずれも Pipeline に値を渡すための仕組みですが、役割が異なります。関数における「デフォルト値付きの内部変数」と「呼び出し時に渡す引数」の違いに近いイメージです。

.. code-block:: groovy

   pipeline {
       agent any

       parameters {
           string(name: 'TARGET_ENV', defaultValue: 'staging', description: 'デプロイ先')
           choice(name: 'LOG_LEVEL', choices: ['INFO', 'DEBUG'], description: 'ログレベル')
           booleanParam(name: 'SKIP_TESTS', defaultValue: false, description: 'テストをスキップする')
       }

       environment {
           APP_ENV = "${params.TARGET_ENV}"
       }

       stages {
           stage('Show env') {
               steps {
                   echo "Deploying to ${env.APP_ENV} (log level: ${params.LOG_LEVEL})"
               }
           }
       }
   }

* ``parameters`` は、ビルド実行時にユーザーが値を選択・入力できるようにするディレクティブです。「ビルド実行」ボタンを押す前にフォームが表示され、そこで指定した値が ``params.<名前>`` として参照できます。
* ``environment`` は、Pipeline 内で使う環境変数を定義します。値は ``env.<名前>`` または単に ``<名前>`` として参照でき、``sh`` ステップで実行するシェルコマンドにも自動的に環境変数として引き渡されます。

stages と steps
==================

``stages`` は 1 つ以上の ``stage`` をまとめるブロックで、Pipeline の処理を「ビルド」「テスト」「デプロイ」のような意味のある単位に分割します。各 ``stage`` の中の ``steps`` に、実際に実行する処理を並べます。

.. code-block:: groovy

   stages {
       stage('Build') {
           steps {
               sh 'pip install -r requirements.txt'
           }
       }
       stage('Test') {
           steps {
               sh 'pytest'
           }
       }
       stage('Deploy') {
           steps {
               sh './deploy.sh'
           }
       }
   }

制御構造として見ると、``stages`` は関数本体、``stage`` はその中の意味のある処理ブロック（コメントで区切っていた部分を明示的な単位にしたもの）に相当します。この単位ごとに、実行時間や成否がステージビュー（:doc:`04_pipeline_basics` 参照）に記録されます。

条件分岐: when ディレクティブ
================================

``when`` は、特定の条件を満たす場合にのみ ``stage`` を実行するディレクティブです。``if`` 文に相当しますが、Declarative Pipeline では条件を専用の構文で表現します。

.. code-block:: groovy

   stage('Deploy to production') {
       when {
           branch 'main'
           expression { params.SKIP_TESTS == false }
       }
       steps {
           sh './deploy.sh production'
       }
   }

主な条件は次のとおりです。

* ``branch 'main'`` ── 実行中のブランチが ``main`` の場合にのみ実行します。
* ``expression { ... }`` ── 任意の Groovy 式を評価し、``true`` の場合にのみ実行します。``if`` 文の条件式そのものに近い書き方です。
* ``changeset "**/*.py"`` ── 指定したパターンに一致するファイルが変更されている場合にのみ実行します。
* ``environment name: 'APP_ENV', value: 'production'`` ── 指定した環境変数が特定の値を持つ場合にのみ実行します。

``when`` ブロック内に複数の条件を並べると、デフォルトではすべての条件を満たした場合（AND）に実行されます。``anyOf { ... }`` を使うと OR 条件を表現できます。

post セクション（後処理）
============================

``post`` は、``stage`` または Pipeline 全体の結果に応じて実行する後処理を定義します。``try``/``finally`` に相当する仕組みです。

.. code-block:: groovy

   pipeline {
       agent any
       stages {
           stage('Test') {
               steps {
                   sh 'pytest'
               }
           }
       }
       post {
           always {
               echo 'このブロックは成否にかかわらず必ず実行される'
           }
           success {
               echo 'ビルドが成功した場合のみ実行される'
           }
           failure {
               echo 'ビルドが失敗した場合のみ実行される'
           }
           changed {
               echo '前回の結果からステータスが変化した場合のみ実行される'
           }
       }
   }

* ``always`` は、Python の ``finally`` ブロックのように、成否を問わず必ず実行したい処理（一時ファイルの削除、通知など）に使います。
* ``success``/``failure`` は、それぞれ正常終了時の処理／``except`` に相当します。
* ``changed`` は、「前回は失敗していたが今回は成功した」（またはその逆）といったステータスの変化を検知したい場合に便利です。連続失敗時に毎回通知が飛ぶのを避けたいケースで使われます。

並列実行: parallel と matrix
===============================

複数のステージを並列に実行したい場合は ``parallel`` を使います。

.. code-block:: groovy

   stage('Test') {
       parallel {
           stage('Unit tests') {
               steps { sh 'pytest tests/unit' }
           }
           stage('Lint') {
               steps { sh 'ruff check .' }
           }
       }
   }

``matrix`` は、複数の軸（例: OS × Python バージョン）の組み合わせを自動的に展開し、それぞれを並列実行する仕組みです。

.. code-block:: groovy

   stage('Cross test') {
       matrix {
           axes {
               axis {
                   name 'PYTHON_VERSION'
                   values '3.11', '3.12', '3.13'
               }
               axis {
                   name 'OS'
                   values 'linux', 'windows'
               }
           }
           stages {
               stage('Test') {
                   steps {
                       sh "tox -e py${PYTHON_VERSION}"
                   }
               }
           }
       }
   }

上記の例では 3 × 2 = 6 通りの組み合わせが自動的に生成され、それぞれが並列に実行されます。テストマトリクスを手で ``parallel`` として書き並べる代わりに、軸の定義だけで組み合わせを表現できます。

手動承認: input ステップ
============================

本番環境へのデプロイなど、自動化の途中に人間の承認を挟みたい場合は ``input`` ステップを使います。実行が一時停止し、Jenkins の UI 上で承認（または入力）が行われるまで待機します。

.. code-block:: groovy

   stage('Approval') {
       steps {
           timeout(time: 1, unit: 'HOURS') {
               input message: '本番環境へデプロイしますか？', ok: 'Deploy'
           }
       }
   }

   stage('Deploy to production') {
       steps {
           sh './deploy.sh production'
       }
   }

.. tip::
   ``input`` は実行中のエージェントを確保したまま待機するため、``timeout`` と組み合わせて無期限の待機を避けるのが定石です。また、``input`` は Groovy の値を戻り値として受け取れるため、承認時に追加の選択（デプロイ先の指定など）を求めることもできます。

よく使う Steps 一覧
=======================

``steps`` の中で使う代表的なステップを一覧にまとめます。文法・用途はリファレンスとして押さえておき、実践的な使い方は該当章で扱います。

.. list-table::
   :header-rows: 1

   * - ステップ
     - 用途
   * - ``sh`` / ``bat``
     - シェルコマンド（Linux/macOS は ``sh``、Windows は ``bat``）を実行する。
   * - ``checkout scm``
     - ジョブに設定されたリポジトリからソースコードを取得する。
   * - ``stash`` / ``unstash``
     - あるステージで生成したファイルを、別のステージ（別のエージェント上でも）に引き渡す。複数エージェントを跨ぐビルドで使う。
   * - ``archiveArtifacts``
     - 生成物（ビルド済みバイナリ、レポート等）をビルド結果に添付して保存する。
   * - ``junit``
     - JUnit 形式のテストレポートを読み込み、Jenkins の UI 上で成功/失敗件数として集計・表示する。
   * - ``isUnix``
     - 実行中のエージェントが Unix 系 OS かどうかを判定する。``if (isUnix()) { sh '...' } else { bat '...' }`` のように、OS に応じて ``sh``/``bat`` を切り替える際に使う。
   * - ``dir``
     - ブロック内でのカレントディレクトリを一時的に変更する。``dir('subdir') { sh '...' }`` のように使う。
   * - ``deleteDir``
     - カレントディレクトリの中身を再帰的に削除する。ワークスペースのクリーンアップに使う。
   * - ``readFile`` / ``writeFile``
     - ワークスペース内のファイルをテキストとして読み書きする。設定値の受け渡しなどに使う。
   * - ``sleep``
     - 指定した時間だけ処理を一時停止する。外部システムが安定するまでの待機やデバッグに使う。
   * - ``unstable``
     - ビルドを失敗させずに、明示的に「不安定（``UNSTABLE``）」として終了させる。
   * - ``nodesByLabel``
     - 指定したラベルを持つ、現在利用可能なノード名の一覧を取得する。``parallel`` と組み合わせて、動的にステージを生成する場合などに使う。

``archiveArtifacts`` と ``junit`` の基本文法はここで押さえ、複数ジョブ・複数言語のレポートを扱う実践的な活用パターンは :doc:`09_integration` で扱います。この表に挙げたステップは、本章末尾に掲載する ``sample-app/Jenkinsfile`` の中でひととおり実際に使われています。

サンプル全体（sample-app/Jenkinsfile）
==========================================

ここまでで個別に説明してきたディレクティブを組み合わせた、実際に動作する Jenkinsfile 全体です。:download:`sample-app/Jenkinsfile <../../sample-app/Jenkinsfile>` としてダウンロードし、手元の Jenkins でそのまま試すこともできます。

.. literalinclude:: ../../sample-app/Jenkinsfile
   :language: groovy
   :linenos:
