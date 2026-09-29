# sample-app

「Jenkins & Jenkins Pipeline 入門」の本文で説明する Jenkinsfile を、
実際に動かして確認するためのサンプルリポジトリです。

シンプルな四則演算の Python パッケージ（`app/calculator.py`）と、
その `pytest` テストだけを持つ最小限のアプリケーションに対して、
複数の Jenkinsfile を用意しています。

## 構成

| ファイル / ディレクトリ | 対応する章 | 内容 |
| --- | --- | --- |
| `app/`, `tests/`, `requirements.txt` | — | サンプルアプリケーション本体 |
| `Jenkinsfile` | 第4・5・7・9・10章 | Declarative Pipeline のメイン例（options / parameters / parallel / when / input / post 等、および「よく使う Steps 一覧」の checkout / stash・unstash / archiveArtifacts / junit / isUnix / dir / deleteDir / readFile・writeFile / sleep / unstable / nodesByLabel） |
| `Jenkinsfile.scripted` | 第6章 | 同じアプリケーションに対する Scripted Pipeline での書き方 |
| `Jenkinsfile.with-shared-library` | 第8章 | 共有ライブラリ（`shared-library-example/`）を読み込む版 |
| `shared-library-example/` | 第8章 | 共有ライブラリのディレクトリ構成（`vars/`/`src/`/`resources/`）の実物サンプル。詳細は同ディレクトリの README を参照 |
| `deploy.sh` | 第9・10章 | デプロイ処理を模した最小のスクリプト |

## ローカルで試す

1. 第2章の手順で Jenkins を起動する。

   ```console
   $ docker run -d --name jenkins \
       -p 8080:8080 -p 50000:50000 \
       -v jenkins_home:/var/jenkins_home \
       jenkins/jenkins:lts
   ```

2. このディレクトリを Git リポジトリとして push する
   （GitHub 等のリモート、またはローカルの bare リポジトリでも構わない）。

3. Jenkins 上で「Multibranch Pipeline」ジョブを作成し、
   このリポジトリを指定する（第7章）。

4. `develop` ブランチと `main` ブランチを作成して push すると、
   `Jenkinsfile` の `when { branch ... }` による分岐
   （ステージング／本番の使い分け）を確認できる。

`Jenkinsfile.scripted` や `Jenkinsfile.with-shared-library` を試す場合は、
Multibranch Pipeline のジョブ設定で「Script Path」を
それぞれのファイル名に変更する。

## ローカルでのテスト実行

Jenkins を経由せず、アプリケーション自体の動作を確認する場合は
次のコマンドを使う。

```console
$ python -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
$ ruff check app tests
$ pytest
```

Jenkinsfile 内の各ステップは、このローカルでの手順をそのまま
`sh` ステップとして呼び出しているだけです。
