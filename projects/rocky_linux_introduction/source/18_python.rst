.. _ch-python:

Python によるシステム管理の自動化
=================================

この章では、Python を使ってシステム管理の作業を自動化する方法を説明します。シェルスクリプトでは書きにくい、データの集計や条件の複雑な処理も、Python を使うと読みやすく書けます。

Rocky Linux の Python
---------------------

Rocky Linux 10 には Python 3.12 が含まれており、``python3`` コマンドで実行できます。この Python は、``dnf`` をはじめとする OS のツールも使っている「システムの Python」です。

.. code-block:: console
   :linenos:

   $ python3 --version
   Python 3.12.9

システムの Python に ``sudo pip install`` で直接ライブラリを導入すると、``dnf`` で導入したライブラリと衝突し、OS のツールが動かなくなるおそれがあります。外部のライブラリを使う場合は、次に説明する仮想環境を使ってください。

仮想環境（venv）
----------------

:term:`venv` は、プロジェクトごとに独立した Python の環境（仮想環境）を作る標準の機能です。仮想環境の中で導入したライブラリは、システムの Python や他の仮想環境に影響しません。

.. code-block:: console
   :linenos:

   $ python3 -m venv ~/venvs/tools
   $ source ~/venvs/tools/bin/activate
   (tools) $ pip install --upgrade pip
   (tools) $ pip install flake8 mypy
   (tools) $ deactivate

1 行目で ``~/venvs/tools`` に仮想環境を作成し、2 行目で有効にしています。有効にすると、プロンプトの先頭に仮想環境の名前が表示され、``python`` や ``pip`` がこの仮想環境のものになります。5 行目の ``deactivate`` で元に戻ります。

仮想環境を有効にせずに、仮想環境の Python を直接指定して実行することもできます。systemd のサービスやタイマーから実行する場合は、この方法が便利です。

.. code-block:: console
   :linenos:

   $ ~/venvs/tools/bin/python3 script.py

本章のサンプルは標準ライブラリだけで書かれているため、仮想環境を使わずにシステムの ``python3`` で実行できます。

サンプル 1: サーバー情報の収集
------------------------------

OS のバージョン、カーネル、CPU、メモリ、ディスクの使用量を 1 画面にまとめて表示するスクリプトです。``/etc/os-release`` や ``/proc/meminfo`` など、これまでの章で扱ったファイルから情報を読み取っています。

.. literalinclude:: ../examples/python/system_info.py
   :language: python
   :linenos:
   :caption: system_info.py

:download:`system_info.py をダウンロード <../examples/python/system_info.py>`

.. code-block:: console
   :linenos:

   $ python3 system_info.py
   ホスト名      : web01.example.com
   OS            : Rocky Linux 10.2 (Red Quartz)
   カーネル      : 6.12.0-211.16.1.el10_2.x86_64 (x86_64)
   CPU 数        : 2
   メモリ        : 2.8 GiB 利用可能 / 3.6 GiB
   稼働時間      : 26.3 時間
   ディスク      :
     /              3.1 GiB 使用 /    34.4 GiB (9.0%)
     /boot          0.4 GiB 使用 /     1.0 GiB (40.0%)
     /home          3.1 GiB 使用 /    34.4 GiB (9.0%)
     /var           3.1 GiB 使用 /    34.4 GiB (9.0%)
   $ python3 system_info.py --json

``--json`` を指定すると JSON 形式で出力するため、複数のサーバーの情報を収集して別のプログラムで集計する、といった使い方ができます。この例では ``/home`` と ``/var`` は ``/`` と同じファイルシステムにあるため、同じ値が表示されています。

サンプル 2: ログの集計
----------------------

journald のログを発生元と優先度ごとに集計し、エラーや警告の多い発生元を一覧表示するスクリプトです。``journalctl -o json`` の出力（「:ref:`ch-log-monitoring`」を参照）を 1 行ずつ JSON として解析しています。

.. literalinclude:: ../examples/python/journal_summary.py
   :language: python
   :linenos:
   :caption: journal_summary.py

:download:`journal_summary.py をダウンロード <../examples/python/journal_summary.py>`

.. code-block:: console
   :linenos:

   $ sudo python3 journal_summary.py --since "24 hours ago"
      COUNT  PRIORITY    SOURCE
         42  warning     kernel
         15  err         sshd
          3  warning     NetworkManager

``subprocess.run`` で ``journalctl`` を実行し、その出力を処理しています。外部のコマンドを実行する場合は、この例のように引数をリストで渡してください。文字列で渡して ``shell=True`` を指定すると、引数に含まれる記号がシェルに解釈され、意図しないコマンドが実行される危険があります。

サンプル 3: サービスの監視
--------------------------

指定した systemd のサービスが稼働しているかを確認し、停止しているサービスがあれば終了コード 1 で終了するスクリプトです。``--restart`` を指定すると、停止しているサービスの再起動を試みます。

.. literalinclude:: ../examples/python/service_monitor.py
   :language: python
   :linenos:
   :caption: service_monitor.py

:download:`service_monitor.py をダウンロード <../examples/python/service_monitor.py>`

.. code-block:: console
   :linenos:

   $ python3 service_monitor.py sshd chronyd nginx
   OK  sshd                    active
   OK  chronyd                 active
   NG  nginx                   inactive
   WARNING: 停止しているサービス: nginx
   $ echo $?
   1

このスクリプトを「:ref:`sec-systemd-timer`」で説明したタイマーから定期的に実行すると、簡易的な監視の仕組みになります。終了コードが 0 以外の場合、サービスは「失敗」として記録されるため、``systemctl --failed`` や ``journalctl`` で確認できます。

コードの品質の確認
------------------

Python のコードは、PEP 8 というスタイルガイドに従って書くと、他の人にも読みやすくなります。本章のサンプルは、次のツールで問題がないことを確認しています。

.. list-table:: コードの品質を確認するツール
   :header-rows: 1
   :widths: 20 80

   * - ツール
     - 内容
   * - flake8
     - PEP 8 への違反や、使っていない変数などの問題を検出する
   * - mypy
     - 型ヒントに基づいて、型の誤りを検出する

.. code-block:: console
   :linenos:

   $ source ~/venvs/tools/bin/activate
   (tools) $ flake8 system_info.py journal_summary.py service_monitor.py
   (tools) $ mypy --strict system_info.py journal_summary.py service_monitor.py
   Success: no issues found in 3 source files

``--strict`` は、型ヒントの付け忘れなども含めて厳しく検査するオプションです。運用で使うスクリプトは長期間にわたって使われ、多くの人が修正することになるため、型ヒントを付けて検査しておくと、修正による誤りを早期に発見できます。
