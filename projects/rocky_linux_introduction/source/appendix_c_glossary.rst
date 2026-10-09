.. _appendix-glossary:

付録 C 用語集
=============

本書で使用した主な用語を、アルファベット順、五十音順に説明します。

.. glossary::

   Anaconda
      Rocky Linux や RHEL のインストーラーです。GUI での対話的なインストールと、Kickstart による自動インストールに対応しています。

   AppStream
      Rocky Linux の標準のリポジトリの 1 つです。アプリケーション、言語処理系、データベースなどのパッケージを提供します。

   BaseOS
      Rocky Linux の標準のリポジトリの 1 つです。カーネルや systemd など、OS の中核となるパッケージを提供します。

   CDI
      Container Device Interface の略です。GPU などのデバイスをコンテナから使うために必要な設定を記述する、コンテナエンジン共通の仕様です。Podman は CDI に対応しています。

   CentOS Stream
      RHEL の次のマイナーバージョンの開発版に当たるディストリビューションです。RHEL より先に変更が反映されます。

   chrony
      NTP を使って時刻を同期するソフトウェアです。サービス名は ``chronyd``、操作するコマンドは ``chronyc`` です。

   Cockpit
      Web ブラウザーからサーバーの状態の確認や管理作業を行えるツールです。既定では 9090 番ポートで待ち受けます。

   CRB
      CodeReady Linux Builder の略です。開発用のライブラリやツールを提供するリポジトリで、既定では無効になっています。EPEL を使う場合に有効にします。

   crypto-policies
      OpenSSL や OpenSSH などが使用できる暗号方式を、システム全体でまとめて管理する仕組みです。``update-crypto-policies`` コマンドで操作します。

   CUDA
      NVIDIA の GPU で汎用の計算を行うためのプラットフォームです。機械学習のフレームワークなどが利用しています。

   DKMS
      Dynamic Kernel Module Support の略です。カーネルに含まれていない外部のカーネルモジュールをソースコードからビルドし、カーネルが更新されるたびに自動でビルドし直す仕組みです。

   DNF
      RPM パッケージを、依存関係を解決しながら導入・更新・削除するパッケージ管理ツールです。``yum`` の後継です。

   EPEL
      Extra Packages for Enterprise Linux の略です。Fedora プロジェクトが提供する、RHEL 系のディストリビューション向けの追加パッケージのリポジトリです。

   firewalld
      ゾーンという単位で通信の許可と拒否を管理するファイアウォールです。``firewall-cmd`` コマンドで操作します。

   Flatpak
      OS から独立した形式でデスクトップ用のアプリケーションを配布・実行する仕組みです。主な配布元は Flathub です。

   GNOME
      Rocky Linux の標準のデスクトップ環境です。

   GPU
      Graphics Processing Unit の略です。画面の描画を高速に行うための装置で、多数の計算を並列に処理できるため、機械学習などの計算にも使われます。

   GRUB 2
      Rocky Linux のブートローダーです。起動メニューを表示し、カーネルと initramfs を読み込んでカーネルを起動します。

   initramfs
      起動時にカーネルと一緒に読み込まれる、一時的なルートファイルシステムです。本来のルートファイルシステムをマウントするために必要なドライバーなどを含みます。

   journald
      systemd に含まれるログの仕組みです。ログはバイナリ形式で保存され、``journalctl`` コマンドで検索・表示します。

   keyfile
      NetworkManager の接続の設定を保存するファイルの形式です。INI ファイルに似た形式で、``/etc/NetworkManager/system-connections/`` に保存されます。

   Kickstart
      Anaconda で行うインストールの設定をテキストファイルに記述し、インストールを自動化する仕組みです。

   Let's Encrypt
      無償でサーバー証明書を発行する認証局です。証明書の発行と更新は ``certbot`` などのツールで自動化できます。

   LVM
      Logical Volume Manager の略です。複数のディスクをまとめて 1 つの領域として扱い、必要な大きさの論理ボリュームを切り出して使う仕組みです。

   MOK
      Machine Owner Key の略です。Secure Boot が有効なマシンで、マシンの管理者が独自に登録する署名の鍵です。DKMS でビルドしたカーネルモジュールを読み込むために使います。

   NetworkManager
      Rocky Linux のネットワークの設定を管理するサービスです。``nmcli`` や ``nmtui`` で操作します。

   nouveau
      Linux のカーネルに含まれている、NVIDIA の GPU 用のオープンソースのドライバーです。NVIDIA のドライバーを使う場合は無効にします。

   PID
      Process ID の略です。プロセスごとに割り当てられる番号で、PID が 1 のプロセスは systemd です。

   Podman
      Docker と互換性のあるコマンド体系を持つコンテナエンジンです。デーモンを必要とせず、一般ユーザーの権限でコンテナを実行できます。

   Quadlet
      Podman のコンテナの設定を ``.container`` ファイルに記述し、systemd のサービスとして管理する仕組みです。

   RDP
      Remote Desktop Protocol の略で、リモートデスクトップのためのプロトコルです。Rocky Linux 10 の GNOME は RDP によるリモートデスクトップに対応しています。

   RESF
      Rocky Enterprise Software Foundation の略です。Rocky Linux を運営する、公益を目的とする法人です。

   RHEL
      Red Hat Enterprise Linux の略です。Red Hat が開発・販売する商用の Linux ディストリビューションで、Rocky Linux はこれとの互換性を目標としています。

   rootless コンテナ
      root ではなく一般ユーザーの権限で実行するコンテナです。コンテナが乗っ取られた場合の影響を小さくできます。

   RPM
      Rocky Linux や RHEL で使われるパッケージの形式です。また、それを扱う ``rpm`` コマンドを指します。

   Secure Boot
      署名されたブートローダーやカーネルだけを起動できるようにする UEFI の機能です。有効な場合、カーネルモジュールにも有効な署名が必要です。

   SELinux
      Security-Enhanced Linux の略です。プロセスがアクセスできるファイルやポートを、ポリシーに従って制限する仕組みです。

   sos report
      障害の調査に必要なシステムの情報を収集し、1 つのファイルにまとめるツールです。``sos`` パッケージに含まれています。

   sudo
      許可されたユーザーが、他のユーザー（通常は root）の権限でコマンドを実行するためのコマンドです。

   systemd
      起動時に最初に実行されるプロセス（PID 1）で、サービス、ログ、マウントなど、システム全体を管理します。

   tuned
      サーバーの用途に合わせて、カーネルやデバイスの設定をプロファイル単位でまとめて調整するサービスです。

   venv
      プロジェクトごとに独立した Python の環境（仮想環境）を作成する、Python の標準の機能です。

   Wayland
      画面の描画とウィンドウの管理を行うためのプロトコルです。Rocky Linux 10 では、X11 に代わって唯一のディスプレイサーバーの方式となりました。

   x86-64-v3
      x86_64 の CPU の命令セットの水準を表す規格の 1 つで、AVX2 などの命令を含みます。Rocky Linux 10 の x86_64 版の動作に必要です。

   XFS
      Rocky Linux の標準のファイルシステムです。大容量のファイルやディスクの扱いに優れていますが、容量を縮小できません。

   Xwayland
      Wayland の上で X11 のアプリケーションを動作させるための仕組みです。

   カーネル
      OS の中核となるプログラムです。ハードウェアの制御、プロセスやメモリの管理などを行います。

   コンテナイメージ
      アプリケーションとその実行に必要なライブラリや設定をまとめたものです。コンテナはイメージから作成されます。

   ゾーン
      firewalld で、通信の許可と拒否の規則をまとめる単位です。インターフェイスや送信元の IP アドレスをゾーンに割り当てて使います。

   ユニット
      systemd が管理する対象（サービス、タイマー、マウントなど）の単位です。種類はユニットファイルの拡張子で区別します。
