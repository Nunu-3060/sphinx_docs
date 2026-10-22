動作確認と負荷テスト
====================

本章では、組み上がった PC が仕様どおりに認識され、高い負荷をかけても安定して動作するかを確認する方法を説明する。

起動して普段使いができても、高い負荷をかけたときにだけ不安定になる問題は珍しくない。販売店の初期不良の対応期間内に問題を見つけるため、組み立て後に一通りの確認を行う。

認識状況を確認する
------------------

OS 上で、各パーツが仕様どおりに認識されているかを確認する。

.. list-table:: 確認する項目
   :header-rows: 1
   :widths: 25 75

   * - 項目
     - 確認する内容
   * - CPU
     - 型番、コア数、スレッド数が仕様と一致しているか。
   * - メモリ
     - 容量が合計と一致しているか。プロファイルを有効にした場合は、速度が定格と一致しているか。
   * - ストレージ
     - 全てのストレージが認識され、健康状態に問題が無いか。
   * - GPU
     - 型番と VRAM 容量が仕様と一致しているか。PCIe のリンク幅が x16 になっているか。

Windows
^^^^^^^

タスクマネージャーの「パフォーマンス」タブで、CPU、メモリ（速度を含む）、ストレージ、GPU の概要を確認できる。より詳しく確認するには、HWiNFO などのハードウェア情報ツールを使う。ストレージの健康状態は CrystalDiskInfo で確認できる。

PowerShell では次のコマンドで情報を確認できる。

.. code-block:: powershell
   :linenos:
   :caption: Windows（PowerShell）で認識状況を確認する

   # CPU の型番、コア数、スレッド数
   Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors
   # メモリの容量と動作速度（1 枚ずつ表示される）
   Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity, ConfiguredClockSpeed
   # ストレージの一覧と健康状態
   Get-PhysicalDisk | Select-Object FriendlyName, MediaType, Size, HealthStatus

Linux
^^^^^

Linux では次のコマンドで情報を確認できる。温度の確認には lm-sensors、ストレージの健康状態の確認には smartmontools のパッケージが必要となる。

.. code-block:: bash
   :linenos:
   :caption: Linux で認識状況を確認する

   # 必要なパッケージをインストールする（Ubuntu の場合）
   sudo apt install lm-sensors smartmontools
   # CPU の型番、コア数、スレッド数
   lscpu
   # メモリの容量
   free -h
   # メモリの動作速度（1 枚ずつ表示される）
   sudo dmidecode -t memory | grep -i speed
   # ストレージの一覧
   lsblk
   # NVMe SSD の健康状態
   sudo smartctl -a /dev/nvme0n1
   # CPU などの温度
   sensors
   # NVIDIA の GPU の状態
   nvidia-smi

GPU の PCIe のリンク幅と速度は、lspci コマンドで確認できる。LnkSta の行に現在の値が表示される。GPU は何もしていないときに省電力のため速度を下げることがあるため、負荷をかけた状態で確認する。

.. code-block:: bash
   :linenos:
   :caption: Linux で GPU の PCIe のリンク状態を確認する

   # GPU のアドレス（例：01:00.0）を確認する
   lspci | grep -i vga
   # 確認したアドレスを指定してリンク状態を表示する
   sudo lspci -vv -s 01:00.0 | grep -E "LnkCap|LnkSta"

負荷テスト
----------

各パーツに高い負荷を一定時間かけ、エラーや停止が起きないかを確認する。代表的なテストとツールを次の表に示す。

.. list-table:: 負荷テストの種類とツール
   :header-rows: 1
   :widths: 15 30 20 20 15

   * - 対象
     - 目的
     - Windows のツール
     - Linux のツール
     - 時間の目安
   * - CPU
     - 高い負荷で計算結果に誤りが無いか、温度が許容範囲か。
     - OCCT、Prime95
     - stress-ng、Prime95
     - 30 分から 1 時間
   * - メモリ
     - 読み書きの誤りが無いか。
     - MemTest86（USB メモリから起動する）、OCCT
     - MemTest86、memtester
     - 1 パス以上（数時間）
   * - GPU
     - 高い負荷で表示の乱れや停止が無いか、温度が許容範囲か。
     - OCCT、実際に使うゲームやアプリケーション
     - 実際に使うアプリケーション
     - 30 分から 1 時間
   * - 電源ユニット
     - CPU と GPU に同時に負荷をかけても停止しないか。
     - OCCT（電源のテスト）
     - CPU と GPU のテストを同時に実行する。
     - 30 分程度
   * - ストレージ
     - 健康状態に問題が無いか。
     - CrystalDiskInfo
     - smartctl
     - 数分

MemTest86 は OS とは別に USB メモリから起動して実行するため、Windows と Linux のどちらの環境でも使える。メモリのプロファイルを有効にした場合は、特にメモリのテストを入念に行う。

Linux で CPU に負荷をかけるには、stress-ng を使う。次のコマンドは、全ての CPU に 30 分間負荷をかける。

.. code-block:: bash
   :linenos:
   :caption: stress-ng で CPU に負荷をかける

   sudo apt install stress-ng
   # --cpu 0 は全ての CPU を使うことを意味する
   stress-ng --cpu 0 --timeout 30m --metrics-brief

負荷テストの実行中は、温度を監視する。Windows では HWiNFO、Linux では sensors コマンドを使う。次のように watch コマンドと組み合わせると、一定間隔で表示を更新できる。

.. code-block:: bash
   :linenos:
   :caption: Linux で温度を 2 秒ごとに表示する

   watch -n 2 sensors

温度の目安
----------

温度の目安を次の表に示す。上限の値は製品によって異なるため、各メーカーの仕様を確認すること。

.. list-table:: 温度の目安
   :header-rows: 1
   :widths: 20 25 55

   * - 対象
     - 高負荷時の目安
     - 備考
   * - CPU
     - 95 ℃ 未満
     - 最近の CPU は、性能を引き出すため上限近くまで温度が上がる設計の製品がある。上限に達すると、CPU は自動的に動作周波数を下げて温度を抑える（:term:`サーマルスロットリング`）。
   * - GPU
     - 85 ℃ 未満
     - GPU のメーカーの管理ツールで、温度と動作周波数を確認できる。
   * - NVMe SSD
     - 70 ℃ 未満
     - 70 ℃ 前後から速度を下げ始める製品が多い。ヒートシンクで冷却する。

温度が高すぎる場合は、次の順に確認する。

1. CPU クーラーの底面の保護フィルムを剥がしたか、CPU クーラーが傾かずに固定されているか。
2. CPU クーラーのファン、ケースファンが回っているか。風の向きは正しいか。
3. ケースの吸気口がふさがれていないか。フィルターにホコリが詰まっていないか。
4. UEFI のファンの制御設定で、回転数が低く抑えられすぎていないか。

合格の判断
----------

次の条件を全て満たせば、PC は安定して動作していると判断できる。

* 全ての負荷テストを、エラー、停止、再起動なく完了した。
* 高負荷時の温度が目安の範囲内に収まった。
* OS のログにハードウェアのエラーが記録されていない。

Windows では、イベントビューアーの「Windows ログ」の「システム」で、ソースが WHEA-Logger のエラーが記録されていないかを確認する。WHEA-Logger は、CPU やメモリなどのハードウェアのエラーを記録する仕組みである。

Linux では、次のコマンドでカーネルのエラーを確認できる。「Hardware Error」や「Machine Check」を含むメッセージが無いかを確認する。

.. code-block:: bash
   :linenos:
   :caption: Linux でカーネルのエラーを確認する

   sudo journalctl -k -p err

問題が見つかった場合は、:doc:`troubleshooting` を参照する。メモリのプロファイルを有効にしている場合は、まず無効にして再びテストする。
