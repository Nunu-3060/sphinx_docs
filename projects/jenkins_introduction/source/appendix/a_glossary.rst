========
用語集
========

.. glossary::

   Controller（コントローラー）
      Jenkins 本体のプロセス。ジョブのスケジューリングや UI 提供を担う。旧称は Master。

   Agent（エージェント）
      実際にビルドを実行するワーカーノード。旧称は Slave。

   Job（ジョブ）
      Jenkins 上で実行される一連のタスクの定義。

   Build（ビルド）
      ジョブを 1 回実行したインスタンス。

   Pipeline
      ビルド・テスト・デプロイの一連の流れをコードとして記述したもの、またはその実行機構。

   Jenkinsfile
      Pipeline の定義を記述したテキストファイル。通常はリポジトリのルートに配置する。

   Declarative Pipeline
      定型的な構造に沿って Pipeline を記述する方式。

   Scripted Pipeline
      Groovy スクリプトとして自由に Pipeline を記述する方式。

   Stage / Step
      Pipeline を構成する処理のまとまり（Stage）と、その中で実行される個々の操作（Step）。

   Workspace（ワークスペース）
      ジョブの実行時にエージェント上に用意される作業用ディレクトリ。ソースコードのチェックアウトやビルドの中間生成物が置かれる。

   Credentials（認証情報）
      パスワードや API トークン、SSH 鍵などの秘密情報を Jenkins が暗号化して保管する仕組み。ID を通じて Pipeline から参照する。

   Multibranch Pipeline
      リポジトリ内の複数ブランチ・プルリクエストを自動検出し、それぞれに対して Pipeline を実行するジョブの種類。

   Shared Library（共有ライブラリ）
      複数の Jenkinsfile から再利用できる Groovy コードをまとめたリポジトリ。

   CPS（Continuation Passing Style）
      Pipeline の実行状態をシリアライズ可能な形に変換する仕組み。Jenkins の再起動をまたいで実行を継続できるようにするために使われる。
