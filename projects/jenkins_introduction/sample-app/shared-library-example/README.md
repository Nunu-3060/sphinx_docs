# shared-library-example

「Jenkins & Jenkins Pipeline 入門」第8章「共有ライブラリ」で解説する
ディレクトリ構成（`vars/` / `src/` / `resources/`）の実物サンプルです。

## 実際に使うには

Jenkins の Shared Library はそれ自体が独立した Git リポジトリである
ことを前提とした仕組みです。このサンプルを実際に動かす場合は、

1. このディレクトリの内容を、単独の Git リポジトリとして
   別途 push する（例: `sample-shared-library` という名前のリポジトリ）。
2. Jenkins の「Manage Jenkins > System > Global Trusted Pipeline
   Libraries」に、そのリポジトリを名前 `sample-shared-library` として登録する。
3. `sample-app/Jenkinsfile.with-shared-library` のように、
   `@Library('sample-shared-library@main') _` で読み込む。

という手順が必要です。`sample-app` リポジトリの中に置いているのは、
あくまで構成を確認しやすくするためであり、`sample-app` の
`Jenkinsfile`／`Jenkinsfile.scripted` はこのディレクトリに依存せず
単体で動作します。

## ファイル対応表

| ファイル | 対応する本文 |
| --- | --- |
| `vars/deployApp.groovy` | 「グローバル変数（vars）の作成」 |
| `vars/notifySlack.groovy` | 第9章「通知連携（Slack / メール）」のスタブ実装 |
| `src/org/example/pipeline/Deployer.groovy` | `src/` 配下のクラスと Pipeline ステップの関係 |
| `resources/org/example/templates/notification.txt` | `libraryResource` で読み込む静的リソースの例 |
