.. _ch-gpu:

GPU の利用
==========

この章では、Rocky Linux で :term:`GPU` を使うために必要なドライバーの導入方法を説明します。現在の PC やサーバーには、NVIDIA 製の GPU が搭載されていることが多くあります。NVIDIA の GPU を、画面の表示（デスクトップ環境）と、:term:`CUDA` による計算（機械学習など）の両方で使えるようにすることが、この章の目標です。

.. important::

   この章の手順には、NVIDIA の GPU を搭載した物理マシンが必要です。本書の他の章で想定している仮想マシンからは、通常は GPU を利用できません（GPU を仮想マシンに割り当てる PCI パススルーなどの設定が必要です）。

   また、ドライバーのバージョン（ブランチ）や、対応する GPU の世代は頻繁に変わります。この章に記載したバージョンなどは執筆時点（2026 年 10 月）の情報です。導入する前に、「:ref:`appendix-references`」に挙げた NVIDIA と Rocky Linux の公式資料で最新の情報を確認してください。

GPU とドライバーの基礎
----------------------

GPU の用途
~~~~~~~~~~

GPU は、もともと画面の描画を高速に行うための装置です。現在では、多数の計算を並列に処理できる性質を生かして、機械学習、科学技術計算、動画の変換など、画面の表示以外の計算にも広く使われています。

.. list-table:: GPU の主な用途
   :header-rows: 1
   :widths: 25 75

   * - 用途
     - 内容
   * - 表示用途
     - デスクトップ環境の描画、動画の再生支援、3D グラフィックス（OpenGL、Vulkan）
   * - 計算用途
     - CUDA などを使った汎用の計算。機械学習の学習と推論、科学技術計算など

GPU を搭載したサーバーでは、画面を接続せずに計算用途だけで使うことも多くあります。

ドライバーの構成
~~~~~~~~~~~~~~~~

GPU のドライバーは、次の 2 つの部分で構成されています。

.. list-table:: GPU のドライバーの構成
   :header-rows: 1
   :widths: 30 70

   * - 部分
     - 役割
   * - カーネルモジュール
     - カーネルの中で動作し、GPU のハードウェアを直接制御する（「:ref:`ch-boot-kernel`」を参照）。NVIDIA のドライバーでは ``nvidia.ko`` などが該当する
   * - ユーザー空間のライブラリ
     - アプリケーションから GPU を使うためのライブラリ。表示用途の OpenGL や Vulkan、計算用途の CUDA のライブラリなど

カーネルモジュールとライブラリは、同じバージョンの組み合わせで使う必要があります。このため、ドライバーは個々のファイルではなく、パッケージとしてまとめて管理します。

GPU の確認
~~~~~~~~~~

搭載されている GPU と、現在使われているカーネルモジュールは、``lspci`` コマンドで確認できます。最小構成では ``lspci`` が含まれていないため、``pciutils`` パッケージを導入します。

.. code-block:: console
   :linenos:

   $ sudo dnf install pciutils
   $ lspci -nnk | grep -A 3 -E "VGA|3D controller"
   01:00.0 VGA compatible controller [0300]: NVIDIA Corporation AD104GL [RTX 4000 SFF Ada Generation] [10de:27b0] (rev a1)
           Subsystem: NVIDIA Corporation Device [10de:16fa]
           Kernel driver in use: nouveau
           Kernel modules: nouveau

``Kernel driver in use`` の行が、この GPU を現在制御しているカーネルモジュールです。この例では、Rocky Linux に標準で含まれる :term:`nouveau` が使われています。計算用途の GPU は、``VGA compatible controller`` ではなく ``3D controller`` と表示される場合があります。

メーカーごとの状況
------------------

GPU のメーカーによって、ドライバーの導入の要否が異なります。

.. list-table:: GPU のメーカーごとのドライバーの状況
   :header-rows: 1
   :widths: 15 40 45

   * - メーカー
     - 表示用途
     - 計算用途
   * - Intel
     - カーネルに含まれるドライバー（``i915``、``xe``）で動作する。作業は不要
     - oneAPI などのツールキットを別途導入する
   * - AMD
     - カーネルに含まれるドライバー（``amdgpu``）で動作する。作業は不要
     - ROCm を別途導入する
   * - NVIDIA
     - nouveau で最低限の表示はできるが、性能と機能が限られる
     - NVIDIA のドライバーの導入が必要。nouveau では CUDA を使えない

Intel と AMD の GPU は、表示用途であれば Rocky Linux をインストールするだけで使えます。NVIDIA の GPU を本来の性能で使うには、NVIDIA が提供するドライバーを導入する必要があります。本章の以降の節では、NVIDIA の GPU について説明します。Intel と AMD の計算用途のツールキットについては、各社の資料を参照してください。

NVIDIA ドライバーの導入方法の選択肢
-----------------------------------

NVIDIA のドライバーは Rocky Linux の標準のリポジトリには含まれていないため、外部から導入します。主な方法は次のとおりです。

.. list-table:: NVIDIA のドライバーの導入方法
   :header-rows: 1
   :widths: 25 75

   * - 方法
     - 特徴
   * - NVIDIA の公式リポジトリ
     - NVIDIA が Rocky Linux 向けに提供する RPM パッケージを ``dnf`` で導入する。NVIDIA と Rocky Linux の両方の公式資料が推奨する方法。本書ではこの方法を使う
   * - RPM Fusion
     - コミュニティが提供するリポジトリ。古い GPU 向けのドライバーが充実している
   * - ELRepo
     - RHEL 系向けのハードウェアのドライバーを提供するコミュニティのリポジトリ
   * - ``.run`` インストーラー
     - NVIDIA の Web サイトで配布されている実行形式のインストーラー。パッケージ管理の外でシステムのファイルを上書きするため、問題が起きやすく、推奨されない

``.run`` インストーラーで導入したドライバーは ``dnf`` で管理できず、カーネルの更新のたびに手作業での対応が必要になります。特別な理由がない限り、公式リポジトリから導入してください。

導入前の確認
------------

GPU の世代とドライバーの対応
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NVIDIA のドライバーは、「ブランチ」と呼ばれる系列（580、590 など）ごとに公開されています。また、カーネルモジュールには、ソースコードが公開されている「オープンなカーネルモジュール」と、従来の「独自のカーネルモジュール」の 2 種類があります。執筆時点では、GPU の世代によって、使えるブランチとカーネルモジュールが次のように異なります。

.. list-table:: GPU の世代と使えるドライバー（執筆時点）
   :header-rows: 1
   :widths: 35 30 35

   * - GPU の世代
     - 製品の例
     - 使えるドライバー
   * - Turing 以降（Turing、Ampere、Ada Lovelace、Hopper、Blackwell など）
     - GeForce RTX 20 シリーズ以降、RTX A シリーズ以降
     - 最新のブランチの、オープンなカーネルモジュール
   * - Maxwell、Pascal、Volta
     - GeForce GTX 900 / 10 シリーズ、Quadro GV100 など
     - 580 ブランチまで。独自のカーネルモジュールが必要

オープンなカーネルモジュールは、ドライバーの 560 以降で標準になりました。RTX 50 シリーズなどの新しい GPU は、オープンなカーネルモジュールにしか対応していません。一方、ブランチ 590 以降は Maxwell、Pascal、Volta 世代に対応していないため、これらの GPU では 580 ブランチを使い続ける必要があります（「:ref:`sec-gpu-old`」を参照）。

使っている GPU の世代は、「GPU の確認」で表示された製品名を NVIDIA の資料で調べて確認します。

Secure Boot の状態の確認
~~~~~~~~~~~~~~~~~~~~~~~~

:term:`Secure Boot` は、UEFI の機能の 1 つで、署名されたブートローダーやカーネルだけを起動できるようにする仕組みです。Secure Boot が有効な場合、カーネルが読み込むカーネルモジュールにも有効な署名が必要です。NVIDIA のドライバーのカーネルモジュールは、手元のマシンでビルドされるため（次の節を参照）、その署名に使う鍵をマシンに登録する必要があります。

Secure Boot の状態は、次のコマンドで確認します。

.. code-block:: console
   :linenos:

   $ mokutil --sb-state
   SecureBoot enabled

``SecureBoot enabled`` と表示された場合は、「:ref:`sec-gpu-secureboot`」の作業が必要です。``SecureBoot disabled`` の場合は不要です。

DKMS の仕組み
~~~~~~~~~~~~~

NVIDIA の公式リポジトリから導入するドライバーのカーネルモジュールは、:term:`DKMS` （Dynamic Kernel Module Support）という仕組みで管理されます。DKMS は、カーネルに含まれていない外部のカーネルモジュールを、手元のマシンでソースコードからビルドし、カーネルが更新されるたびに自動でビルドし直す仕組みです。

ビルドには、使用中のカーネルと同じバージョンの ``kernel-devel`` パッケージ（カーネルのヘッダーファイルなど）と、コンパイラーが必要です。

.. note::

   RHEL では、Red Hat が署名したビルド済みのカーネルモジュールが提供されており、DKMS や Secure Boot の鍵の登録が不要です。ただし、このパッケージは RHEL のサブスクリプションが必要なリポジトリで提供されているため、Rocky Linux では使えません。

NVIDIA ドライバーの導入
-----------------------

ここでは、Turing 以降の GPU に、オープンなカーネルモジュールのドライバーを導入する手順を説明します。古い GPU の場合は、手順 4 の代わりに「:ref:`sec-gpu-old`」の手順を実行してください。

1. システムを最新の状態に更新し、再起動します。カーネルが更新された状態のまま次の手順に進むと、使用中のカーネルとビルドに使うカーネルのバージョンが一致しなくなるためです。

   .. code-block:: console
      :linenos:

      $ sudo dnf upgrade --refresh
      $ sudo systemctl reboot

2. CRB と EPEL を有効にし、ビルドに必要なパッケージを導入します（「:ref:`sec-epel`」を参照）。DKMS などの依存パッケージは EPEL で提供されています。

   .. code-block:: console
      :linenos:

      $ sudo dnf config-manager --set-enabled crb
      $ sudo dnf install epel-release
      $ sudo dnf group install "Development Tools"
      $ sudo dnf install kernel-devel-matched kernel-headers

   ``kernel-devel-matched`` は、使用中のカーネルと同じバージョンの ``kernel-devel`` を導入するためのパッケージです。

3. NVIDIA の公式リポジトリを追加します。

   .. code-block:: console
      :linenos:

      $ sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel10/x86_64/cuda-rhel10.repo
      $ sudo dnf clean expire-cache

   Rocky Linux 10 は RHEL 10 と互換性があるため、RHEL 10 向けのリポジトリ（``rhel10``）を使います。

4. ドライバーを導入します。用途に応じて、次のいずれかを実行します。

   .. code-block:: console
      :linenos:

      $ sudo dnf install nvidia-open
      $ sudo dnf install nvidia-driver-cuda kmod-nvidia-open-dkms
      $ sudo dnf install nvidia-driver kmod-nvidia-open-dkms

   .. list-table:: 導入するパッケージの選び方
      :header-rows: 1
      :widths: 15 25 60

      * - 行
        - 用途
        - 内容
      * - 1 行目
        - 表示用途と計算用途
        - すべての機能を導入する。迷った場合はこれを選ぶ
      * - 2 行目
        - 計算用途のみ
        - 画面を接続しない計算用のサーバー向け。表示用のライブラリを導入しない
      * - 3 行目
        - 表示用途のみ
        - デスクトップ用の PC 向け。CUDA のライブラリを導入しない

   導入の際に、DKMS によってカーネルモジュールがビルドされます。ビルドには数分かかります。

5. nouveau を無効にします。nouveau と NVIDIA のドライバーが同時に GPU を使おうとすると競合するため、起動時に nouveau が読み込まれないようにカーネルパラメーターを設定します（「:ref:`sec-kernel-param`」を参照）。

   .. code-block:: console
      :linenos:

      $ sudo grubby --update-kernel=ALL --args="nouveau.modeset=0 rd.driver.blacklist=nouveau"

6. Secure Boot が有効な場合は、ここで「:ref:`sec-gpu-secureboot`」の手順 1 を実行します。

7. 再起動します。Secure Boot が有効な場合は、再起動の途中で「:ref:`sec-gpu-secureboot`」の手順 2 の操作が必要です。

   .. code-block:: console
      :linenos:

      $ sudo systemctl reboot

.. _sec-gpu-secureboot:

Secure Boot への対応
--------------------

Secure Boot が有効なマシンでは、DKMS がカーネルモジュールの署名に使う鍵を、:term:`MOK` （Machine Owner Key）としてファームウェアに登録します。DKMS は、最初にカーネルモジュールをビルドするときに、署名用の鍵のペアを ``/var/lib/dkms/`` に自動で作成します。

1. 再起動の前に、DKMS の公開鍵を登録する予約をします。

   .. code-block:: console
      :linenos:

      $ sudo mokutil --import /var/lib/dkms/mok.pub
      input password:
      input password again:

   ここで入力するパスワードは、次の手順 2 で 1 回だけ使う一時的なものです。忘れないようにしてください。

2. 再起動すると、OS が起動する前に「MOK management」という青い画面が表示されます。次の順に操作します。

   1. 「Enroll MOK」を選びます。
   2. 「Continue」を選び、続けて「Yes」を選びます。
   3. 手順 1 で設定したパスワードを入力します。
   4. 「Reboot」を選びます。

   この画面は一定時間操作しないと自動で先に進み、鍵が登録されないまま起動します。その場合は、手順 1 からやり直してください。

鍵が登録されたかどうかは、次のコマンドで確認できます。

.. code-block:: console
   :linenos:

   $ mokutil --test-key /var/lib/dkms/mok.pub
   /var/lib/dkms/mok.pub is already enrolled

鍵の登録は 1 回だけ行えば十分です。ドライバーやカーネルを更新しても、同じ鍵で署名されるため、再度登録する必要はありません。

動作確認
--------

再起動したら、ドライバーが正しく読み込まれていることを確認します。

.. code-block:: console
   :linenos:

   $ lsmod | grep nvidia
   $ cat /proc/driver/nvidia/version
   $ nvidia-smi
   $ nvidia-smi -L
   GPU 0: NVIDIA RTX 4000 SFF Ada Generation (UUID: GPU-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

``lsmod`` で ``nvidia`` から始まるモジュールが表示され、``nvidia-smi`` で GPU の一覧と状態が表示されれば、ドライバーは正しく動作しています。``lspci -nnk`` を実行すると、``Kernel driver in use`` が ``nvidia`` に変わっていることも確認できます。

``nvidia-smi`` は、GPU の温度、使用率、メモリの使用量、GPU を使っているプロセスなどを表示するコマンドです。``nvidia-smi -l 5`` のように実行すると、5 秒ごとに表示を更新します。

デスクトップ環境を使っている場合は、GUI のログイン画面が表示され、ログイン後に「設定」→「システム」→「情報」（「このシステムについて」）で、グラフィックスの項目に NVIDIA の GPU の名前が表示されることを確認します。

GPU の状態を確認するスクリプト
------------------------------

``nvidia-smi`` には、指定した項目を CSV 形式で出力する機能があり、スクリプトから GPU の状態を取得するのに便利です。

.. code-block:: console
   :linenos:

   $ nvidia-smi --query-gpu=index,name,temperature.gpu,memory.used,memory.total --format=csv,noheader,nounits
   0, NVIDIA RTX 4000 SFF Ada Generation, 41, 512, 20475

この機能を使って、GPU の温度、使用率、メモリの使用量を一覧表示し、しきい値を超えた場合に警告するスクリプトの例を示します。「:ref:`ch-python`」のサンプルと同じ方針で書いています。

.. literalinclude:: ../examples/python/gpu_status.py
   :language: python
   :linenos:
   :caption: gpu_status.py

:download:`gpu_status.py をダウンロード <../examples/python/gpu_status.py>`

.. code-block:: console
   :linenos:

   $ python3 gpu_status.py
   GPU NAME                    DRIVER      TEMP  UTIL        MEMORY (MiB)
   0   NVIDIA RTX 4000 SFF Ada 615.71.09   41 C    3%    512/20475 (2.5%)

しきい値を超えた GPU があると ``WARNING`` の行を表示し、終了コード 1 で終了します。「:ref:`sec-systemd-timer`」で説明したタイマーから定期的に実行すると、簡易的な監視の仕組みになります。

CUDA Toolkit の導入
-------------------

ドライバーを導入すると、CUDA を使うアプリケーションを実行できるようになります。CUDA を使うプログラムを自分で開発する場合は、コンパイラー（``nvcc``）やライブラリを含む CUDA Toolkit も導入します。CUDA Toolkit は、ドライバーと同じ NVIDIA の公式リポジトリで提供されています。

.. code-block:: console
   :linenos:

   $ sudo dnf install cuda-toolkit
   $ /usr/local/cuda/bin/nvcc --version

CUDA Toolkit は ``/usr/local/cuda/`` に導入されます。``nvcc`` などのコマンドを名前だけで実行するには、``PATH`` に ``/usr/local/cuda/bin`` を追加します（「:ref:`sec-env-vars`」を参照）。

なお、機械学習のフレームワーク（PyTorch など）の多くは、必要な CUDA のライブラリを同梱して配布されています。これらを使うだけであれば、CUDA Toolkit の導入は不要で、ドライバーだけで動作します。

.. note::

   CUDA Toolkit のバージョン 13 以降は、Maxwell、Pascal、Volta 世代の GPU に対応していません。これらの GPU で開発する場合は、CUDA 12 系の CUDA Toolkit（例えば ``cuda-toolkit-12-9``）を指定して導入してください。

ドライバーの更新
----------------

カーネルの更新と DKMS
~~~~~~~~~~~~~~~~~~~~~

``sudo dnf upgrade`` でカーネルが更新されると、DKMS が新しいカーネル向けにカーネルモジュールを自動でビルドします。このとき、新しいカーネルに対応する ``kernel-devel`` が必要です。``kernel-devel-matched`` を導入していれば、カーネルと一緒に自動で更新されます。

カーネルの更新後に GUI が起動しない、``nvidia-smi`` がエラーになる、といった場合は、カーネルモジュールのビルドに失敗している可能性があります。次のコマンドで状態を確認します。

.. code-block:: console
   :linenos:

   $ dkms status
   nvidia/615.71.09, 6.12.0-211.13.1.el10_2.x86_64, x86_64: installed
   nvidia/615.71.09, 6.12.0-211.16.1.el10_2.x86_64, x86_64: installed

使用中のカーネル（``uname -r`` で確認）に対して ``installed`` と表示されていれば、ビルドは成功しています。表示されていない場合の対処方法は、「:ref:`ch-troubleshooting`」で説明します。

ドライバーの更新
~~~~~~~~~~~~~~~~

ドライバーも、他のパッケージと同じく ``sudo dnf upgrade`` で更新されます。Rocky Linux 10 では、特に設定しなければ、最新のブランチのドライバーに更新されます。ドライバーを更新した後は、新しいカーネルモジュールを読み込むために再起動が必要です。

特定のブランチを使い続けたい場合は、``dnf versionlock`` でブランチを固定します。``versionlock`` は ``dnf`` のプラグインで、指定したパッケージの更新を、条件に一致するバージョンに制限します。

.. code-block:: console
   :linenos:

   $ sudo dnf install python3-dnf-plugin-versionlock
   $ sudo dnf versionlock add '*nvidia*610*'
   $ dnf versionlock list

2 行目は、名前に ``nvidia`` を含むパッケージを、610 ブランチ（バージョンが 610 で始まるもの）に固定します。固定を解除するには ``sudo dnf versionlock delete`` で該当する行を削除するか、``sudo dnf versionlock clear`` ですべての固定を解除します。

.. _sec-gpu-old:

古い GPU を使う場合
~~~~~~~~~~~~~~~~~~~

Maxwell、Pascal、Volta 世代の GPU には、580 ブランチの、独自のカーネルモジュールのドライバーを使います。最新のドライバーを導入すると、エラーは出ずに導入できますが、再起動後に対応する GPU が見つからず、カーネルモジュールが読み込まれません。

この章の「NVIDIA ドライバーの導入」の手順 4 の代わりに、次のように実行します。

.. code-block:: console
   :linenos:

   $ sudo dnf install python3-dnf-plugin-versionlock
   $ sudo dnf versionlock add '*nvidia*580*'
   $ sudo dnf install nvidia-driver nvidia-driver-cuda kmod-nvidia-latest-dkms

2 行目で、ドライバーに関するパッケージを 580 ブランチに固定してから、3 行目で導入しています。``kmod-nvidia-latest-dkms`` が、独自のカーネルモジュールを DKMS で管理するパッケージです。固定しないまま ``dnf upgrade`` を実行すると、580 ブランチに対応していない新しいブランチに更新されてしまうため、固定は必ず行ってください。

NVIDIA は、最新のブランチでは独自のカーネルモジュールの提供を終了しています。580 ブランチのサポートの終了時期は、NVIDIA の資料で確認してください。

コンテナからの GPU の利用
-------------------------

機械学習などの計算環境は、コンテナで配布されることが多くあります。Podman のコンテナから GPU を使うには、NVIDIA Container Toolkit を導入します（コンテナについては「:ref:`ch-container`」を参照）。

NVIDIA Container Toolkit は、GPU を使うために必要なデバイスファイルやライブラリを、:term:`CDI` （Container Device Interface）という標準の形式で記述した設定ファイルを作成します。Podman は CDI に対応しているため、この設定ファイルを使って、ホストの GPU とドライバーのライブラリをコンテナに渡せます。コンテナのイメージには、ドライバーを含める必要はありません。

1. NVIDIA Container Toolkit のリポジトリを追加して導入します。

   .. code-block:: console
      :linenos:

      $ curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo | sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo
      $ sudo dnf install nvidia-container-toolkit

2. CDI の設定ファイルが作成されたことを確認します。設定ファイル（``/var/run/cdi/nvidia.yaml``）は、``nvidia-cdi-refresh`` というサービスによって、導入時やドライバーの更新時、OS の起動時に自動で作成・更新されます。

   .. code-block:: console
      :linenos:

      $ nvidia-ctk cdi list
      INFO[0000] Found 3 CDI devices
      nvidia.com/gpu=0
      nvidia.com/gpu=GPU-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
      nvidia.com/gpu=all

3. コンテナから GPU を使えることを確認します。一般ユーザーで実行できます（rootless コンテナ）。

   .. code-block:: console
      :linenos:

      $ podman run --rm --device nvidia.com/gpu=all --security-opt=label=disable docker.io/library/ubuntu:24.04 nvidia-smi -L
      GPU 0: NVIDIA RTX 4000 SFF Ada Generation (UUID: GPU-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)

   ``--device nvidia.com/gpu=all`` は、すべての GPU をコンテナに渡す指定です。特定の GPU だけを渡す場合は、``nvidia.com/gpu=0`` のように番号を指定します。ホストと同じ GPU の一覧が表示されれば成功です。

``--security-opt=label=disable`` は、このコンテナについて SELinux によるコンテナの分離（「:ref:`sec-selinux`」を参照）を無効にする指定です。NVIDIA の資料では、GPU のデバイスファイルにアクセスするためにこの指定を使っています。コンテナの分離が弱まるため、信頼できるイメージだけで使ってください。

Quadlet（「:ref:`ch-container`」を参照）でサービスとして動かす場合は、``.container`` ファイルの ``[Container]`` セクションに次のように記述します。

.. code-block:: ini
   :linenos:

   [Container]
   AddDevice=nvidia.com/gpu=all
   SecurityLabelDisable=true
