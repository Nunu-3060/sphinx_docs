================================================
Scripted Pipeline と Groovy の基礎
================================================

Scripted Pipeline は Groovy スクリプトそのものであり、Declarative Pipeline よりも自由度の高い記述が可能です。

.. note::
   サンプルリポジトリの ``sample-app/Jenkinsfile.scripted`` は、``sample-app/Jenkinsfile``\ （Declarative 版）と同じアプリケーションを Scripted Pipeline で書き直したものです。両者を見比べながら読み進めると、記法の違いが具体的に把握できます。全文は本章末尾に掲載しているほか、:download:`ここから直接ダウンロード <../../sample-app/Jenkinsfile.scripted>` することもできます。

Groovy 入門（Python 経験者向け）
====================================

Groovy は JVM 上で動作するスクリプト言語で、Java との相互運用性を持ちながら、Python に近い簡潔な文法も備えています。ここでは Pipeline を読み書きするために最低限必要な範囲だけを、Python との対比で押さえます。

**変数宣言**

Groovy では型を書かずに ``def`` で変数を宣言できます。Python の変数がそのまま代入で使えるのと同じ感覚です。

.. code-block:: groovy

   def name = 'jenkins'
   def count = 3

**文字列補間（GString）**

ダブルクオートの文字列内では ``${...}`` で式を埋め込めます。Python の f-string（``f"hello {name}"``）に相当します。

.. code-block:: groovy

   def name = 'world'
   echo "hello, ${name}!"   // => hello, world!

シングルクオートの文字列では補間は行われない点も、Python の f-string と通常の文字列の違いに似ています。

**クロージャ**

波括弧 ``{ }`` で囲んだブロックはクロージャ（Python のラムダ式や関数オブジェクトに近いもの）として値を持てます。Pipeline の ``steps { ... }`` や ``stage('x') { ... }`` の ``{ ... }`` は、実はすべてこのクロージャです。

.. code-block:: groovy

   def greet = { n -> "hello, ${n}!" }
   echo greet('jenkins')

**リストとマップ**

.. code-block:: groovy

   def list = ['a', 'b', 'c']
   def map = [name: 'jenkins', version: 2]
   echo map.name       // => jenkins

Python のリスト・辞書とほぼ同じ感覚で使えます。

node と stage
================

Scripted Pipeline の基本構造は、``node`` ブロックと ``stage`` の組み合わせです。

.. code-block:: groovy

   node('linux') {
       stage('Build') {
           sh 'pip install -r requirements.txt'
       }
       stage('Test') {
           sh 'pytest'
       }
   }

``node`` は Declarative Pipeline の ``agent`` に相当し、どのエージェントで処理を実行するかを指定します。``node`` ブロックに入った時点でワークスペースが確保され、ブロックを抜けると解放されます。

``stage`` は Declarative Pipeline と同じく処理の単位を表しますが、Scripted Pipeline では ``steps`` ブロックを介さず、``stage`` の中に直接 Groovy のコードを書きます。この「決められた構造に従うか、自由に書くか」という違いが、両者の最大の違いです。

制御構文とループ
===================

Scripted Pipeline の中では、通常の Groovy と同じように ``if``/``for``/``while`` が使えます。

.. code-block:: groovy

   node {
       stage('Conditional deploy') {
           if (env.BRANCH_NAME == 'main') {
               sh './deploy.sh production'
           } else {
               echo 'main 以外のブランチではデプロイをスキップします'
           }
       }

       stage('Run per module') {
           def modules = ['api', 'worker', 'web']
           for (m in modules) {
               sh "pytest tests/${m}"
           }
       }
   }

Python の ``if``/``for`` とほぼ同じ見た目ですが、1 点大きな違いがあります。Jenkins は Pipeline の実行を **CPS（Continuation Passing Style）**\ という仕組みで変換し、途中経過をシリアライズして保存できるようにしています。これは、実行中の Pipeline が Jenkins の再起動をまたいで継続できるようにするための仕組みです。

この CPS 変換の制約により、通常の Groovy の標準ライブラリ（``List#each`` のような組み込みメソッドにクロージャを渡すもの等）がそのままでは動かない、あるいは ``@NonCPS`` アノテーションが必要になる場合があります。「基本的な if/for/while は問題なく使えるが、複雑な高階関数の使用は制約を受けることがある」という点を覚えておいてください。

try/catch によるエラーハンドリング
=====================================

Scripted Pipeline では、通常の Groovy と同じく ``try``/``catch``/``finally`` でエラーハンドリングを行います。

.. code-block:: groovy

   node {
       stage('Test') {
           try {
               sh 'pytest'
           } catch (err) {
               currentBuild.result = 'UNSTABLE'
               echo "テストが失敗しましたが、後続処理を続行します: ${err}"
           } finally {
               junit 'reports/*.xml'
           }
       }
   }

Python の ``try``/``except``/``finally`` とほぼ同じ役割です。``catch`` した例外を握りつぶすと、Jenkins のビルド自体は「成功」のまま終わってしまうため、``currentBuild.result`` を ``'UNSTABLE'`` や ``'FAILURE'`` に明示的に設定し、実際の状態をビルド結果に反映させるのが定石です。

Declarative との使い分け
============================

実務では、まず Declarative Pipeline で骨格を書き、Groovy の自由な記述力が必要な部分だけを ``script { }`` ブロックの中で Scripted な書き方に切り替える、という使い分けが一般的です。

.. code-block:: groovy

   pipeline {
       agent any
       stages {
           stage('Notify') {
               steps {
                   script {
                       def modules = ['api', 'worker']
                       for (m in modules) {
                           echo "module ${m} をチェックします"
                       }
                   }
               }
           }
       }
   }

``when`` や ``post`` のような Declarative Pipeline の定型的な仕組みでは表現しづらい、複雑な分岐やループだけを ``script { }`` に切り出すことで、可読性と自由度のバランスを取ることができます。「全体は Declarative、部分的に Scripted」という組み合わせが、最初に選ぶべき標準的なスタイルだと考えてください。

サンプル全体（sample-app/Jenkinsfile.scripted）
====================================================

:doc:`05_pipeline_syntax` 末尾の Declarative 版と同じアプリケーションに対する、Scripted Pipeline での実装全体です。:download:`sample-app/Jenkinsfile.scripted <../../sample-app/Jenkinsfile.scripted>` としてダウンロードできます。

.. literalinclude:: ../../sample-app/Jenkinsfile.scripted
   :language: groovy
   :linenos:
