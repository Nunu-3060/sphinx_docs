SUSE 系
=======

SUSE 系は、SUSE 社が開発する SLES と、コミュニティ版の openSUSE からなる系統である。Red Hat 系と同じく RPM 形式のパッケージを使うが、パッケージ管理ツールには独自の zypper を使う。

SUSE Linux Enterprise Server（SLES）
------------------------------------

SLES は、SUSE 社が有償のサブスクリプションで提供する企業向けのディストリビューションである。欧州で広く使われており、SAP 製品の動作基盤としての実績が多い。

.. list-table:: SLES の基本情報
   :header-rows: 0
   :widths: 30 70
   :stub-columns: 1

   * - 開発主体
     - SUSE 社
   * - 初版
     - 2000 年
   * - 最新版
     - SLES 16.0（2025 年 11 月）、SLES 15 SP7（2025 年 6 月）
   * - パッケージ管理
     - RPM 形式、zypper
   * - リリースモデル
     - 固定リリース（SLES 16 ではマイナーバージョンを毎年公開する）
   * - サポート期間
     - SLES 16 は一般サポートが 2035 年 11 月まで（約 10 年）、追加契約の LTS により 2038 年 11 月まで延長できる

**特徴**

* SAP 製品向けに最適化した SLES for SAP Applications があり、SAP HANA の動作基盤として多く採用されている。
* x86_64、arm64 に加え、IBM Z（メインフレーム）と IBM Power をサポートしている。
* ルートファイルシステムに Btrfs を採用し、Snapper によるスナップショットを使って更新前の状態に戻せる。
* SLES 16 では大きな変更が行われた。インストーラが Agama に、システム管理ツールが YaST から Cockpit などに置き換えられ、ネットワーク設定は wicked から NetworkManager に、標準のセキュリティ機構は AppArmor から SELinux に変わった。
* SLES 15 の一般サポートは 2031 年 7 月まで、LTSS は 2034 年 7 月までである。

**主な用途**

企業の基幹システム、特に SAP 製品の動作基盤やメインフレーム上の Linux として使われる。

openSUSE
--------

openSUSE は、SUSE 社が支援するコミュニティのプロジェクトであり、固定リリースの Leap と、ローリングリリースの Tumbleweed の 2 つのディストリビューションを提供する。

.. list-table:: openSUSE の基本情報
   :header-rows: 0
   :widths: 30 70
   :stub-columns: 1

   * - 開発主体
     - openSUSE プロジェクト（SUSE 社が支援）
   * - 初版
     - 2005 年
   * - 最新版
     - openSUSE Leap 16.0（2025 年 10 月）、openSUSE Tumbleweed（ローリングリリース）
   * - パッケージ管理
     - RPM 形式、zypper
   * - リリースモデル
     - Leap は固定リリース、Tumbleweed はローリングリリース
   * - サポート期間
     - Leap 16.0 は 2027 年 10 月まで（約 2 年）。Tumbleweed は常に最新の状態のみをサポートする

**特徴**

* Leap は SLES とソースコードやバイナリパッケージを共有しており、SLES とほぼ同じ環境を無償で利用できる。SLES への移行も容易である。
* Tumbleweed は、自動テストシステム openQA による検証を通過したスナップショット単位で更新される。ローリングリリースでありながら安定性に定評がある。
* Tumbleweed を基盤とし、システム領域を読み取り専用とするイミュータブル OS の MicroOS も提供している。

**主な用途**

Leap は SLES と互換性のある無償のサーバやデスクトップに、Tumbleweed は新しいソフトウェアを使いたい開発者のデスクトップに使われる。
