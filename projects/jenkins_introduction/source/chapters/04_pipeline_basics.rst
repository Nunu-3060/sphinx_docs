================================
Jenkins Pipeline の基礎
================================

Jenkins Pipeline は、ビルド・テスト・デプロイの流れをコードとして記述する仕組みです。本章では Declarative Pipeline を中心に基礎を解説します。

.. note::
   本書には、実際に動かして確認できるサンプルリポジトリ ``sample-app`` が付属しています。本章で示す最小構成の Jenkinsfile よりも実践的な完全版は :download:`sample-app/Jenkinsfile <../../sample-app/Jenkinsfile>` としてダウンロードでき、全文は :doc:`05_pipeline_syntax` の末尾に掲載しています。ファイルを個別にではなく一括で入手したい場合は :download:`sample-app 一式（zip） <../../sample-app.zip>` を参照してください。

Pipeline as Code という考え方
================================

前章で見た Freestyle ジョブの限界は、「ビルド手順が Jenkins の内部にしか存在しない」ことに起因していました。Pipeline は、このビルド手順を **Jenkinsfile** というテキストファイルに記述し、アプリケーションのソースコードと同じリポジトリに含めることでこの問題を解決します。

これは、インフラ構成を Terraform や Ansible のようなコードで管理する **IaC（Infrastructure as Code）**\ と同じ発想です。IaC がサーバーの構成をコード化するのに対し、Pipeline as Code は「ビルド・テスト・デプロイの手順」をコード化します。コード化することで、次のような利点が得られます。

* **バージョン管理** ── ビルド手順の変更履歴が Git の履歴として残り、``git blame`` で「いつ・誰が・なぜ」変更したかを追跡できます。
* **レビュー可能性** ── Jenkinsfile の変更を、アプリケーションコードと同じプルリクエストでレビューできます。
* **再現性** ── 同じ Jenkinsfile を別の Jenkins 環境に持ち込めば、同じビルド手順を再現できます。UI 上の設定のようにコピー漏れが起きません。

Declarative Pipeline と Scripted Pipeline
============================================

Jenkinsfile の記法には、**Declarative Pipeline** と **Scripted Pipeline** の 2 種類があります。

* **Declarative Pipeline** ── ``pipeline { ... }`` から始まる、あらかじめ決められた構造（ディレクティブ）に従って記述する方式です。書ける内容には制約がありますが、その分構文が統一されており、可読性やエラー検出のしやすさに優れます。多くのプロジェクトでは、まずこの方式で十分な表現力が得られます。
* **Scripted Pipeline** ── ``node { ... }`` から始まる、Groovy スクリプトそのものです。制約がなく自由度は高い一方、可読性やメンテナンス性は書き手に委ねられます。

比喩的に言えば、Declarative Pipeline は「決められたキーワードを埋めていく設定ファイル（YAML に条件分岐や関数呼び出しが少し混ざったようなもの）」、Scripted Pipeline は「Pipeline 専用の API が用意された汎用スクリプト言語」に近いイメージです。

本書では、まず本章と :doc:`05_pipeline_syntax` で Declarative Pipeline を扱い、:doc:`06_scripted_pipeline` で Scripted Pipeline と、その基盤となる Groovy の文法を扱います。実務では基本的に Declarative Pipeline で記述し、その内部の一部だけを Scripted な書き方（``script { }`` ブロック）で補うという使い分けが一般的です。

最小構成の Jenkinsfile
=========================

次のコードは、Declarative Pipeline の最小構成です。

.. code-block:: groovy

   pipeline {
       agent any

       stages {
           stage('Hello') {
               steps {
                   echo 'Hello, Jenkins Pipeline!'
               }
           }
       }
   }

それぞれのキーワードは次のような役割を持ちます。

* ``pipeline { ... }`` ── Declarative Pipeline 全体を表すトップレベルのブロックです。Jenkinsfile はこのブロック 1 つだけを持ちます。
* ``agent any`` ── この Pipeline をどこで実行するかを指定するディレクティブです。``any`` は「利用可能な任意のエージェントで実行する」という意味です。詳細は :doc:`05_pipeline_syntax` で扱います。
* ``stages { ... }`` ── Pipeline を構成する一連の ``stage`` をまとめるブロックです。関数の中に書かれた一連の処理のまとまり、と捉えると理解しやすいです。
* ``stage('Hello') { ... }`` ── 1 つの処理単位です。名前（ここでは ``'Hello'``）はステージビューなどの UI 上でそのまま表示され、パイプラインの実行状況を可視化する際の単位になります（ステージビューについては後述します）。
* ``steps { ... }`` ── その ``stage`` の中で実際に実行する処理（ステップ）を並べるブロックです。``echo`` はメッセージをログに出力するだけの単純なステップです。

Pipeline ジョブの作成と実行
==============================

この Jenkinsfile を実行するには、ダッシュボードから「新しいジョブを作成」し、ジョブタイプとして「Pipeline」を選択します。

設定画面の「Pipeline」セクションには、次の 2 つの入力方法があります。

* **Pipeline script** ── Jenkinsfile の内容を Jenkins の UI に直接貼り付ける方法です。動作確認には便利ですが、コードがリポジトリと分離してしまうため、Pipeline as Code の利点が失われます。
* **Pipeline script from SCM** ── リポジトリの URL とブランチ、そして Jenkinsfile のパス（通常はリポジトリルートの ``Jenkinsfile``）を指定する方法です。実運用ではこちらを使います。

「Pipeline script from SCM」を選び、リポジトリと Jenkinsfile のパスを指定して保存したら、「ビルド実行」で動作を確認してみましょう。

ステージビューでの可視化
========================================

Pipeline の実行結果は、通常のコンソールログに加えて、ステージごとの実行状況を視覚的に確認できる UI でも参照できます。

ジョブの画面には、各ビルドについて ``stage`` 単位の進行状況を横並びのボックスで表示する「ステージビュー」が表示されます。どのステージで時間がかかっているか、どのステージで失敗したかが一目でわかるため、複数ステージを持つ Pipeline のデバッグに役立ちます。本書では、この標準のステージビューを前提に説明を進めます。

.. note::
   より高度な可視化を行う "Blue Ocean" プラグインがかつて提供されていましたが、開発は終了しており非推奨です。新しく学ぶ場合は、後継として提供されている Pipeline Graph View プラグインや、標準のステージビューを使うのが現在の標準的な選択肢です。古い記事やチュートリアルで Blue Ocean への言及を見かけた場合は、開発が終了している点に注意してください。
