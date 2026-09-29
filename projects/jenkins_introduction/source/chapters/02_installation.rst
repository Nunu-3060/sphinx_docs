==========================
インストールとセットアップ
==========================

Jenkins を動かすための環境構築手順を解説します。

インストール方法の選択肢
========================

Jenkins の導入方法には、大きく次のような選択肢があります。

* **Docker コンテナ** ── 公式イメージ ``jenkins/jenkins`` を使う方法。環境をコード（``docker run`` のコマンドや ``docker-compose.yml``）として再現できるため、検証環境の構築や本書の学習用途には最も手軽です。本章でもこの方法を採用します。
* **パッケージマネージャ（apt/yum 等）** ── Debian/Ubuntu の ``apt``、RHEL 系の ``yum``/``dnf`` などで OS に直接インストールする方法。systemd のサービスとして管理できるため、長期運用する専用サーバーに向いています。
* **WAR ファイルの直接実行** ── ``java -jar jenkins.war`` のように、Java さえあれば OS を問わず起動できる方法。動作原理を理解する上では最もシンプルです。
* **クラウドのマネージドサービス** ── AWS Marketplace で利用できる CloudBees CI、Azure の Jenkins テンプレートなど、インフラ管理を委ねられる選択肢です。学習目的というよりは、すでに Jenkins の運用方針が固まった組織向けです。

どの方法でも、Jenkins 自体は Java プロセスとして動作するという点は共通しています。以降は Docker を用いた最小構成で進めます。

Docker で Jenkins を起動する
=============================

公式イメージを使うと、次のコマンドだけで Jenkins を起動できます。

.. code-block:: console

   $ docker run -d --name jenkins \
       -p 8080:8080 -p 50000:50000 \
       -v jenkins_home:/var/jenkins_home \
       jenkins/jenkins:lts

各オプションの意味は次のとおりです。``-p``\ （\ ``--publish``\ ）はホスト側とコンテナ側のポートを 1 組だけ指定するオプションであり、複数のポートを公開する場合は、この例のように ``-p`` をポートの数だけ繰り返します。

* ``-p 8080:8080`` ── Jenkins の Web UI が公開されるポート。ブラウザで ``http://localhost:8080`` にアクセスして操作します。
* ``-p 50000:50000`` ── JNLP 方式のエージェントがコントローラーへ接続する際に使うポート（「エージェント（ノード）の基礎」で後述）。
* ``-v jenkins_home:/var/jenkins_home`` ── Jenkins の設定・ジョブ定義・ビルド履歴はすべて ``/var/jenkins_home`` 以下に保存されます。ここを Docker のボリュームとして永続化しないと、コンテナを削除した瞬間にすべてのジョブ定義が消えてしまうので注意してください。

.. warning::
   ``-v`` を省略してコンテナを作り直すと、これまでに作成したジョブやプラグイン設定はすべて失われます。学習用の使い捨て環境であれば問題ありませんが、その点を理解した上で利用してください。

初期設定ウィザード
==================

初回起動時は、いくつかの初期設定を行う必要があります。

#. **アンロック** ── コンテナのログに出力される初期パスワードを使ってロックを解除します。

   .. code-block:: console

      $ docker logs jenkins
      ...
      Please use the following password to proceed to installation:
      <ここに表示される文字列を使う>

#. **推奨プラグインのインストール** ── ウィザードの案内に従って「推奨プラグインをインストール」を選ぶと、Git 連携やパイプライン機能など、以降の章で使う基本的なプラグインがまとめて導入されます。

#. **管理者ユーザーの作成** ── 初期パスワードでの運用を続けないよう、最初のログイン用ユーザーを作成します。以降はこのユーザーで Jenkins にアクセスします。

ここまで完了すると、ジョブを作成できる状態になります。

エージェント（ノード）の基礎
=============================

Jenkins は、ジョブの管理と UI を提供する\ **コントローラー**\ （旧称 Master）と、実際にビルドを実行する\ **エージェント**\ （旧称 Slave）を分離できる分散アーキテクチャを持っています。

最もシンプルな構成は、コントローラー自身がビルドも実行する「コントローラー上で直接実行」ですが、これは検証用途に限られます。実運用では、OS やハードウェア要件の異なる複数のエージェントを用意し、ジョブごとにどのエージェントで実行するかをラベルで指定するのが一般的です（ラベルによる指定方法は :doc:`05_pipeline_syntax` の ``agent`` ディレクティブで扱います）。

エージェントの接続方式には、主に次の 2 つがあります。

* **SSH 接続** ── コントローラーが SSH でエージェントにログインし、エージェント用のプログラムを起動する方式。エージェント側からの通信を許可する必要がなく、多くの環境で標準的に使われます。
* **JNLP（インバウンドエージェント）** ── エージェント側からコントローラーへ接続する方式。コントローラーへ直接 SSH で入れないファイアウォール環境や、一時的に立ち上げるビルド専用マシンなどで使われます。

本書のハンズオンでは、コントローラー自身をエージェントとしても使う最小構成のまま進めますが、実運用を見据えて SSH 接続によるエージェント追加の手順も押さえておきましょう。

SSH エージェントを追加する
----------------------------

Docker Hub には、SSH 接続を受け付けるエージェント専用の公式イメージ ``jenkins/ssh-agent`` が用意されています。コントローラーと同じネットワーク上にこのイメージのコンテナを立てるだけで、エージェントとして登録できる状態を作れます。

.. code-block:: console

   $ ssh-keygen -t ed25519 -f agent_key -N ""
   $ docker network create jenkins-net
   $ docker network connect jenkins-net jenkins
   $ docker run -d --name agent1 --network jenkins-net \
       -e "JENKINS_AGENT_SSH_PUBKEY=$(cat agent_key.pub)" \
       jenkins/ssh-agent:latest

上記では、コントローラー（``jenkins``）と同じ Docker ネットワークにエージェント用コンテナ ``agent1`` を接続し、事前に生成した鍵ペアの公開鍵をエージェント側に登録しています。

続いて、Jenkins の管理画面から次の手順でこのエージェントを登録します。

#. 「Manage Jenkins」→「Nodes」→「New Node」を開き、ノード名（例: ``agent1``）を入力して「Permanent Agent」を選択します。
#. 「Remote root directory」に ``/home/jenkins/agent`` を、「Labels」に ``linux`` のような任意のラベルを指定します。
#. 「Launch method」で「Launch agents via SSH」を選び、「Host」にコンテナ名（同じ Docker ネットワーク内であれば ``agent1`` で名前解決できる）を指定します。
#. 「Credentials」で「Add」から、ユーザー名 ``jenkins`` と、先ほど生成した秘密鍵（``agent_key``）を使う「SSH Username with private key」を新規登録します。
#. 「Host Key Verification Strategy」は検証用途であれば「Non verifying Verification Strategy」を選び、保存します。

保存すると、コントローラーが SSH でエージェントに接続し、自動的にエージェント用プログラム（``agent.jar``）を起動します。Nodes の一覧でエージェントのアイコンが有効になっていれば接続成功です。登録したラベルは、:doc:`05_pipeline_syntax` で扱う ``agent { label 'linux' }`` のようにジョブ側から指定して利用します。

JNLP エージェントを追加する
----------------------------

SSH 接続では「コントローラーがエージェントへ SSH でログインする」のに対し、JNLP（インバウンドエージェント）は逆に「エージェント側がコントローラーへ接続しにいく」方式です。そのため、コントローラーからエージェントへ直接 SSH できない環境（エージェントが NAT の内側にある、ファイアウォールで着信が制限されているなど）でも利用できます。

まず、Jenkins の管理画面でエージェントを登録します。

#. 「Manage Jenkins」→「Nodes」→「New Node」を開き、ノード名（例: ``agent2``）を入力して「Permanent Agent」を選択します。
#. 「Remote root directory」と「Labels」を SSH の場合と同様に指定します。
#. 「Launch method」で「Launch agent by connecting it to the controller」を選び、保存します。

保存すると、そのノードの詳細画面に「エージェントの起動コマンド」と、接続に必要な **Secret**\ （トークン）が表示されます。この Secret とコントローラーの URL を使って、エージェント側で ``agent.jar`` を起動すると接続が確立します。公式イメージ ``jenkins/inbound-agent`` を使うと、次のように 1 コマンドで起動できます。

.. code-block:: console

   $ docker run -d --name agent2 --network jenkins-net \
       -e JENKINS_URL=http://jenkins:8080 \
       -e JENKINS_AGENT_NAME=agent2 \
       -e JENKINS_SECRET=<Nodes 画面に表示された Secret> \
       jenkins/inbound-agent:latest

SSH 方式と異なり、コントローラー側から見ると「いつ・どのエージェントが接続してくるか」を制御できないため、Secret の値そのものが認証情報になります。使い捨てのビルド専用マシンや CI 専用のクラウドインスタンスなど、都度起動してジョブが終わったら破棄するような用途と相性が良い方式です。

台数が増えてくると、この手作業での登録は煩雑になります。実運用では、Kubernetes プラグインやクラウドの Auto Scaling と連携し、ビルド需要に応じてエージェントを動的に起動・破棄する構成が一般的です（:doc:`10_best_practices` 参照）。多くのクラウド向けプラグインは、内部的にはこの JNLP 方式でエージェントを使い捨てで接続させています。
