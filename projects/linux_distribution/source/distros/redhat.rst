Red Hat 系
==========

Red Hat 系は、Red Hat 社が開発する RHEL と、その上流・下流にあたるディストリビューションからなる系統である。パッケージ形式に RPM を、パッケージ管理ツールに DNF を使う。RHEL と互換性を持つディストリビューションを総称して EL（Enterprise Linux）系と呼ぶこともある。

Red Hat 系の開発は、Fedora、CentOS Stream、RHEL の順に流れる。新しい技術はまず Fedora に取り込まれ、RHEL の次期メジャーバージョンの開発時に Fedora の特定のバージョンから CentOS Stream が分岐する。CentOS Stream は RHEL の次のマイナーリリースに入る変更を先行して受け取り、それが RHEL としてリリースされる。Rocky Linux、AlmaLinux などのリビルドディストリビューションは、RHEL の下流に位置する。

Red Hat Enterprise Linux（RHEL）
--------------------------------

RHEL は、Red Hat 社が有償のサブスクリプションで提供する企業向けのディストリビューションである。長期のサポートと、ハードウェア・ソフトウェアベンダによる豊富な動作認証を特徴とする。

.. list-table:: RHEL の基本情報
   :header-rows: 0
   :widths: 30 70
   :stub-columns: 1

   * - 開発主体
     - Red Hat 社（2019 年から IBM の傘下）
   * - 初版
     - 2002 年（Red Hat Linux Advanced Server 2.1）
   * - 最新版
     - RHEL 10.2（2026 年 5 月）、RHEL 9.8（2026 年 5 月）
   * - パッケージ管理
     - RPM 形式、DNF
   * - リリースモデル
     - 固定リリース（メジャーバージョンは約 3 年ごと、マイナーバージョンは約 6 か月ごと）
   * - サポート期間
     - 10 年（Full Support 5 年と Maintenance Support 5 年）。追加契約により延長できる

**特徴**

* 多くの商用ソフトウェアやハードウェアが、サポート対象の OS として RHEL を挙げている。
* メジャーバージョン内では、アプリケーションの互換性（ABI 互換）が維持されるよう管理されている。
* RHEL 8 以降、OS の中核をなす BaseOS リポジトリと、言語処理系やデータベースなどを収録する AppStream リポジトリに分かれている。AppStream では、同じソフトウェアの複数のバージョンが提供されることがある。
* メジャーバージョン間のアップグレードには Leapp というツールが用意されている。
* RHEL 10 は、x86_64 では x86-64-v3 に対応した CPU（Intel Haswell 世代以降など）を前提としている。古い CPU を使う環境では注意が必要である。
* 個人の開発者は、Red Hat Developer Subscription for Individuals により無償で RHEL を利用できる（最大 16 台）。

**主な用途**

企業の基幹システムや、商用ソフトウェアの動作基盤として使われる。ベンダのサポートや動作認証が必要な場合の第一候補となる。

Fedora
------

Fedora は、Red Hat 社が支援するコミュニティ主体のディストリビューションである。新しい技術を積極的に採用し、RHEL の将来の機能の実験場の役割も担っている。

.. list-table:: Fedora の基本情報
   :header-rows: 0
   :widths: 30 70
   :stub-columns: 1

   * - 開発主体
     - Fedora Project（Red Hat 社が支援）
   * - 初版
     - 2003 年 11 月（Fedora Core 1）
   * - 最新版
     - Fedora 44（2026 年 4 月）。Fedora 45 は 2026 年 10 月下旬の公開を予定している
   * - パッケージ管理
     - RPM 形式、DNF（Fedora 41 から DNF5）
   * - リリースモデル
     - 固定リリース（約 6 か月ごと）
   * - サポート期間
     - 約 13 か月（2 つ後のバージョンが公開されてから約 1 か月後まで）

**特徴**

* systemd、Wayland、PipeWire など、多くの新技術を主要ディストリビューションの中で早い段階で採用してきた。
* 用途別に Workstation、Server、CoreOS、IoT、Cloud などのエディションを提供する。また、システム領域を読み取り専用とする Fedora Atomic Desktops（Silverblue、Kinoite など）もある。
* RHEL の上流であり、RHEL 10 は Fedora 40 から分岐した CentOS Stream 10 を基に開発された。
* サポート期間が短いため、長期間同じバージョンを使い続ける用途には向かない。

**主な用途**

開発者のデスクトップや、新しい技術の評価環境として使われる。RHEL の将来の機能を先取りして確認する用途にも向く。

CentOS Stream
-------------

CentOS Stream は、RHEL の次のマイナーリリースに入る変更を先行して提供するディストリビューションである。かつての CentOS Linux が RHEL の下流であったのに対し、CentOS Stream は RHEL の上流に位置する。

.. list-table:: CentOS Stream の基本情報
   :header-rows: 0
   :widths: 30 70
   :stub-columns: 1

   * - 開発主体
     - CentOS プロジェクト（Red Hat 社が主導）
   * - 初版
     - 2019 年 9 月（CentOS Stream 8）
   * - 最新版
     - CentOS Stream 10（2024 年 12 月）、CentOS Stream 9
   * - パッケージ管理
     - RPM 形式、DNF
   * - リリースモデル
     - メジャーバージョン内で継続的に更新される
   * - サポート期間
     - 対応する RHEL の Full Support の終了まで（約 5 年）。CentOS Stream 10 は 2030 年 5 月まで

**特徴**

* RHEL の開発の場であり、外部の開発者や企業も変更を提案できる。
* RHEL のマイナーリリースのような区切りがなく、更新が継続的に配信される。そのため、特定の状態で長期間固定して使う用途には向かない。
* AlmaLinux など、CentOS Stream のソースコードを基にするディストリビューションがある。

**主な用途**

RHEL の次期マイナーリリースに向けた動作検証や、RHEL の開発への貢献に使われる。継続的な更新を許容できるサーバにも使われる。

Rocky Linux
-----------

Rocky Linux は、CentOS Linux の終了を受けて立ち上がった RHEL 互換のディストリビューションである。名称は、CentOS の共同創設者の一人である故 Rocky McGaugh に由来する。

.. list-table:: Rocky Linux の基本情報
   :header-rows: 0
   :widths: 30 70
   :stub-columns: 1

   * - 開発主体
     - Rocky Enterprise Software Foundation（RESF）
   * - 初版
     - 2021 年 6 月（Rocky Linux 8.4）
   * - 最新版
     - Rocky Linux 10.2（2026 年 5 月）、Rocky Linux 9.8（2026 年 5 月）
   * - パッケージ管理
     - RPM 形式、DNF
   * - リリースモデル
     - RHEL のリリースに追従する
   * - サポート期間
     - RHEL に準じて 10 年（全面的なサポート 5 年と、セキュリティ修正 5 年）

**特徴**

* RHEL とのバグ互換（不具合も含めて同じ挙動となること）を目標としている。
* 2023 年に RHEL のソースコードの公開方針が変わった後も、RHEL 互換を維持する方針を続けている。
* 商用サポートは、創設者の Gregory Kurtzer が率いる CIQ 社などの第三者が提供する。
* RHEL 互換ディストリビューションのソースコードを共同で提供する OpenELA に参加している。

**主な用途**

RHEL と同等の環境を無償で利用したいサーバに使われる。CentOS Linux からの移行先としても採用が多い。

AlmaLinux
---------

AlmaLinux は、CentOS Linux の終了を受けて CloudLinux 社が立ち上げ、現在は非営利の財団が運営する RHEL 互換のディストリビューションである。

.. list-table:: AlmaLinux の基本情報
   :header-rows: 0
   :widths: 30 70
   :stub-columns: 1

   * - 開発主体
     - AlmaLinux OS Foundation（非営利団体）
   * - 初版
     - 2021 年 3 月（AlmaLinux 8.3）
   * - 最新版
     - AlmaLinux 10.2（2026 年 5 月）、AlmaLinux 9.8（2026 年 5 月）
   * - パッケージ管理
     - RPM 形式、DNF
   * - リリースモデル
     - RHEL のリリースに追従する
   * - サポート期間
     - RHEL に準じて 10 年（全面的なサポート 5 年と、セキュリティ修正 5 年）

**特徴**

* 2023 年以降、RHEL とのバグ互換ではなく ABI 互換を目標としている。CentOS Stream のソースコードを基にしており、セキュリティ修正などを RHEL より先に取り込むこともある。
* AlmaLinux 10 では、RHEL 10 がサポートしない x86-64-v2 世代の CPU 向けのビルドも提供している。
* CentOS Stream に相当する開発版として AlmaLinux OS Kitten を提供している。
* RHEL 系のディストリビューション間の移行やメジャーバージョンのアップグレードを支援する ELevate プロジェクトを運営している。

**主な用途**

Rocky Linux と同様に、RHEL と同等の環境を無償で利用したいサーバに使われる。

その他の Red Hat 系ディストリビューション
--------------------------------------------------------------

Oracle Linux
   Oracle 社が 2006 年から提供している RHEL 互換のディストリビューションである。RHEL 互換のカーネルに加え、Oracle 社独自の UEK（Unbreakable Enterprise Kernel）を選択できる。ダウンロードと更新は無償で、技術サポートは有償で提供される。最新版は Oracle Linux 10（2025 年 6 月）で、Premier Support は 2035 年 6 月までである。

Amazon Linux 2023
   AWS が自社のクラウド向けに提供するディストリビューションである。Fedora を基に独自に開発しており、RHEL 互換ではない。AWS 上では追加費用なしで利用でき、標準サポートは 2027 年 6 月まで、保守サポートは 2029 年 6 月までである。前の版である Amazon Linux 2 のサポートは 2026 年 6 月に終了した。
