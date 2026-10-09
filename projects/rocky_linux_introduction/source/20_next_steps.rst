.. _ch-next-steps:

次のステップ
============

本書では、Rocky Linux のサーバーを 1 台構築し、運用するための基本を説明しました。この章では、本書の内容を踏まえて、次に学ぶとよいテーマを紹介します。

構成管理ツール（Ansible）
-------------------------

サーバーの台数が増えると、同じ設定を手作業で繰り返すのは非効率で、誤りの原因にもなります。Ansible は、サーバーのあるべき状態を YAML 形式のファイル（Playbook）に記述し、SSH を使って複数のサーバーにまとめて適用する構成管理ツールです。サーバー側に専用のソフトウェアを導入する必要がなく、本書で設定した SSH の公開鍵認証をそのまま使えます。

例えば、本書の「:ref:`ch-nginx`」で行った作業は、次のような Playbook で記述できます。

.. code-block:: yaml
   :linenos:

   - name: Web サーバーを構築する
     hosts: web
     become: true
     tasks:
       - name: nginx を導入する
         ansible.builtin.dnf:
           name: nginx
           state: present
       - name: nginx を起動し、自動起動を有効にする
         ansible.builtin.systemd_service:
           name: nginx
           state: started
           enabled: true
       - name: HTTP を許可する
         ansible.posix.firewalld:
           service: http
           permanent: true
           immediate: true
           state: enabled

Playbook は何度実行しても同じ結果になるように作られるため、サーバーの構築手順の記録としても使えます。「:ref:`sec-upgrade-policy`」で説明したメジャーバージョンの移行の際にも、新しいサーバーを素早く同じ構成で構築できます。

自動インストール（Kickstart）
-----------------------------

「:ref:`ch-installation`」で紹介した Kickstart と、PXE ブート（ネットワーク経由での起動）を組み合わせると、物理サーバーへの OS のインストールを完全に自動化できます。Kickstart で OS をインストールし、Ansible で設定を行う、という組み合わせがよく使われます。

コンテナオーケストレーション（Kubernetes）
------------------------------------------

「:ref:`ch-container`」では、1 台のサーバーでコンテナを動かす方法を説明しました。多数のサーバーで多数のコンテナを動かし、負荷に応じた台数の調整や、障害時の自動復旧を行うには、Kubernetes などのコンテナオーケストレーションの仕組みを使います。Podman には、コンテナの設定を Kubernetes の形式で出力する ``podman kube generate`` コマンドがあり、Kubernetes への移行の入り口として利用できます。Kubernetes で GPU を使う場合は、ドライバーや NVIDIA Container Toolkit（「:ref:`ch-gpu`」を参照）の導入と管理を自動化する NVIDIA GPU Operator がよく使われます。

資格試験
--------

体系的に知識を身につけたい場合は、資格試験の学習が役に立ちます。Rocky Linux は RHEL と互換性があるため、RHEL の資格試験の学習環境として使えます。

.. list-table:: 主な資格試験
   :header-rows: 1
   :widths: 35 65

   * - 資格
     - 内容
   * - RHCSA（Red Hat Certified System Administrator）
     - RHEL のシステム管理の基本。本書の内容の多くが出題範囲に含まれる。実技試験
   * - RHCE（Red Hat Certified Engineer）
     - Ansible による RHEL の管理の自動化。実技試験
   * - LinuC / LPIC
     - ディストリビューションに依存しない Linux の技術者認定

本書で扱わなかったトピック
--------------------------

本書では、入門書としての分量を考慮して、次のトピックは扱いませんでした。必要に応じて、「:ref:`appendix-references`」に挙げた資料を参照してください。

.. list-table:: 本書で扱わなかったトピック
   :header-rows: 1
   :widths: 35 65

   * - トピック
     - 主なソフトウェア
   * - DNS サーバーの構築
     - BIND（``bind`` パッケージ）
   * - メールサーバーの構築
     - Postfix、Dovecot
   * - データベースサーバーの構築
     - PostgreSQL、MariaDB、MySQL
   * - Windows とのファイル共有
     - Samba
   * - 高度なストレージ管理
     - Stratis、iSCSI、RAID（``mdadm``）
   * - クラスタリング
     - Pacemaker
   * - 仮想化基盤の構築
     - KVM、libvirt、Cockpit の仮想マシン管理機能
