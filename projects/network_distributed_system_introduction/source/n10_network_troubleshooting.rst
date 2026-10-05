ネットワークの観察と障害対応
============================

この章では、ネットワークの状態を観察するための代表的なコマンドと、「つながらない」「遅い」といった問題が起きたときに原因を切り分ける考え方を説明します。ここまでの章で学んだリンク層、IP、TCP、DNS、HTTP の知識は、障害を調べるときにそのまま役立ちます。コマンドの例は Windows と Linux の両方を示し、章の最後に両者の対応表を載せます。

切り分けの考え方
----------------

ネットワークの障害は、ケーブルの抜けから DNS の設定の誤り、ファイアウォールの規則、アプリケーションの不具合まで、さまざまな層で起こります。しかも利用者から見える症状は、どれも「つながらない」の一言になりがちです。思い付いた箇所を順に疑うのではなく、層を下から順に確かめていくと、原因を効率よく絞り込めます。下の層が動いていなければ、上の層は必ず動かないからです。

.. list-table:: 層ごとの確認項目と主なコマンド
   :header-rows: 1
   :widths: 20 45 35

   * - 層
     - 確認すること
     - 主なコマンド
   * - リンク層
     - ケーブルや無線がつながっているか、インターフェースが有効か
     - ``ipconfig``、``ip link``
   * - インターネット層（自分）
     - IP アドレス、サブネットマスク、デフォルトゲートウェイが正しいか
     - ``ipconfig``、``ip addr``、``ip route``
   * - インターネット層（経路）
     - ゲートウェイや相手に IP のパケットが届くか、どこで止まるか
     - ``ping``、``tracert``、``traceroute``
   * - 名前解決
     - ホスト名から正しい IP アドレスが得られるか
     - ``nslookup``、``dig``
   * - トランスポート層
     - 相手のポートに TCP で接続できるか、自分のポートで待ち受けているか
     - ``Test-NetConnection``、``nc``、``netstat``、``ss``
   * - アプリケーション層
     - HTTP などのリクエストに正しいレスポンスが返るか
     - ``curl``

例えば「Web サイトが表示できない」という場合、まず自分の IP アドレスとデフォルトゲートウェイを確かめ、ゲートウェイに ``ping`` が届くかを見ます。届けば、次に名前解決ができるか、得られた IP アドレスの 443 番ポートに接続できるか、HTTP のレスポンスが返るか、と順に上がっていきます。どこまでが成功し、どこから失敗するかの境目に原因があります。

層とは別の軸として、範囲の切り分けも重要です。

* 他の端末から同じ宛先に接続しても失敗するか（自分の端末の問題か、共通の問題か）
* 同じ端末から他の宛先には接続できるか（宛先側の問題か、自分の側の問題か）
* いつから起きているか、その前後に何を変更したか（設定の変更、機器の交換、証明書の更新など）
* 常に起きるか、ときどき起きるか（ときどき起きる問題は、負荷、タイムアウト、特定のサーバーへの振り分けなどが原因であることが多いです）

調べた結果は、実行したコマンドとその出力をそのまま記録しておきます。「たぶん DNS は大丈夫」のような推測と、「``nslookup`` で正しいアドレスが返った」という事実を区別しておくと、後で見直すときや他の人に引き継ぐときに役立ちます。

自分の設定を確かめる
--------------------

最初に確かめるのは、自分のコンピューターのネットワーク設定です。Windows では ``ipconfig``、Linux では ``ip`` コマンドを使います。

.. code-block:: console
   :linenos:

   > ipconfig
   > ipconfig /all

Windows での ``ipconfig`` の出力例は次のとおりです。表示言語が英語の環境での例で、IP アドレスなどは文書用の値に置き換えています。日本語の環境では項目名が日本語で表示されます。

.. code-block:: text

   Windows IP Configuration


   Ethernet adapter イーサネット:

      Connection-specific DNS Suffix  . :
      Link-local IPv6 Address . . . . . : fe80::1234:5678:9abc:def0%4
      IPv4 Address. . . . . . . . . . . : 192.0.2.81
      Subnet Mask . . . . . . . . . . . : 255.255.255.0
      Default Gateway . . . . . . . . . : 192.0.2.1

``ipconfig /all`` では、MAC アドレス（Physical Address）、DHCP サーバー、DNS サーバーなども表示されます。確かめるべき点は次のとおりです。

* IPv4 アドレスが 169.254.x.x になっていないか。これは DHCP でアドレスを得られなかったときに OS が自動で割り当てるリンクローカルアドレスで、DHCP サーバーに届いていないことを示します。
* デフォルトゲートウェイが設定されているか、自分と同じサブネットにあるか。
* DNS サーバーが意図したものになっているか。
* 「Media disconnected」と表示される場合は、リンク層（ケーブルや無線の接続）の問題です。

Linux では、次のコマンドで同じ情報を確かめます。

.. code-block:: console
   :linenos:

   $ ip addr
   $ ip route
   $ ip neigh
   $ resolvectl status

``ip addr`` はインターフェースと IP アドレス、``ip route`` はルーティングテーブル（``default via`` の行がデフォルトゲートウェイ）、``ip neigh`` は ARP のテーブル（IP アドレスと MAC アドレスの対応）を表示します。DNS サーバーの設定は、systemd-resolved を使っている環境では ``resolvectl status`` で、そうでなければ ``/etc/resolv.conf`` で確かめます。Windows でルーティングテーブルと ARP のテーブルを見るには、``route print`` と ``arp -a`` を使います。

ping
----

``ping`` は、ICMP のエコー要求（Echo Request）を送り、相手からエコー応答（Echo Reply）が返ってくるかと、往復にかかった時間（RTT）を調べるコマンドです（ICMP は「:doc:`n04_internet_layer`」を参照）。IP のパケットが相手まで届き、戻ってこられることを確かめる、最も基本的な道具です。

.. code-block:: console
   :linenos:

   > ping -n 4 127.0.0.1
   $ ping -c 4 127.0.0.1

1 行目が Windows、2 行目が Linux です。送る回数を指定するオプションが異なり、Linux ではオプションを付けないと Ctrl+C で止めるまで送り続けます。Windows での実行結果は次のとおりです。

.. code-block:: text

   Pinging 127.0.0.1 with 32 bytes of data:
   Reply from 127.0.0.1: bytes=32 time<1ms TTL=128
   Reply from 127.0.0.1: bytes=32 time<1ms TTL=128
   Reply from 127.0.0.1: bytes=32 time<1ms TTL=128
   Reply from 127.0.0.1: bytes=32 time<1ms TTL=128

   Ping statistics for 127.0.0.1:
       Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
   Approximate round trip times in milli-seconds:
       Minimum = 0ms, Maximum = 0ms, Average = 0ms

127.0.0.1 は自分自身を指すループバックアドレスなので、これが失敗するなら OS のネットワーク機能そのものの問題です。続けて、自分の IP アドレス、デフォルトゲートウェイ、外部のホストの順に ``ping`` を送ると、どこまで届くかが分かります。

``time`` は RTT、``TTL`` は返ってきたパケットの TTL（Time To Live）の残りの値です。TTL はルーターを 1 つ通るごとに 1 減るので、相手の OS の初期値（「:doc:`n04_internet_layer`」を参照）が分かれば、返ってきた TTL からおおよその経由数を推測できます。``Lost`` は失われたパケットの割合で、0% でない場合は回線の品質や混雑の問題が疑われます。

``ping`` を使うときは、次の点に注意します。

* ``ping`` に応答がないことは、相手が停止していることを意味しません。ファイアウォールで ICMP を破棄しているサーバーやネットワークは珍しくありません。Windows も、既定のファイアウォールの設定では外部からの ``ping`` に応答しないことが多いです。
* 逆に、``ping`` が届いても、目的のサービス（TCP のポート）に接続できるとは限りません。
* RTT は ICMP の処理の速さを表すもので、ルーターによっては ICMP の処理を後回しにするため、実際の通信より遅く見えることがあります。

tracert と traceroute
---------------------

``tracert``\ （Windows）と ``traceroute``\ （Linux）は、宛先までに通過するルーターを順に表示するコマンドです。TTL を 1、2、3 と増やしながらパケットを送ると、TTL が 0 になったルーターが ICMP の時間超過（Time Exceeded）メッセージを返してくるので、その送信元から各段のルーターのアドレスが分かります。Windows の ``tracert`` は ICMP のエコー要求を、Linux の ``traceroute`` は既定で UDP のパケットを使います。

.. code-block:: console
   :linenos:

   > tracert -d -h 6 example.com
   $ traceroute -n -m 6 example.com

``-d``\ （Windows）と ``-n``\ （Linux）は、各ルーターのアドレスを名前に変換しない指定で、表示が速くなります。``-h`` と ``-m`` は最大の段数です。Windows での実行結果の例は次のとおりです（アドレスは文書用の値に置き換えています）。

.. code-block:: text

   Tracing route to example.com [198.51.100.10]
   over a maximum of 6 hops:

     1    <1 ms    <1 ms    <1 ms  192.0.2.1
     2     3 ms     3 ms     3 ms  198.51.100.148
     3     6 ms     5 ms     4 ms  198.51.100.146
     4     4 ms     5 ms     4 ms  203.0.113.11
     5   127 ms    25 ms    21 ms  203.0.113.245
     6     3 ms     3 ms     4 ms  203.0.113.221

   Trace complete.

各行は 1 つのルーターで、3 回の測定の RTT が並んでいます。結果を読むときは、次の点に注意します。

* ``*`` と表示される段は、そのルーターが時間超過メッセージを返さなかったことを示します。ICMP を返さない設定のルーターは多く、その先の段が表示されていれば問題ではありません。
* 途中の 1 つの段だけ RTT が大きくても（上の例の 5 段目）、それより先の段で小さく戻っていれば、そのルーターが ICMP の応答を後回しにしているだけです。ある段から先がすべて大きくなっている場合に、その付近の混雑や遠距離の回線を疑います。
* ある段から先がすべて ``*`` になる場合は、その付近で通信が止まっている可能性があります。ただし、宛先の手前のファイアウォールが探索用のパケットを破棄しているだけのこともあります。
* 表示されるのは行きの経路だけです。インターネットでは行きと帰りの経路が異なることも多く、帰りの経路の問題は見えません。

Windows の ``pathping`` や Linux の ``mtr`` は、``traceroute`` と ``ping`` を組み合わせて、各段でのパケットの損失率を一定時間測り続けるコマンドで、断続的な問題を調べるのに向いています。

nslookup と dig
---------------

名前解決の問題を調べるには、``nslookup``\ （Windows と Linux）や ``dig``\ （Linux など）を使います（DNS の仕組みは「:doc:`n06_dns`」を参照）。

.. code-block:: console
   :linenos:

   > nslookup example.com
   > nslookup example.com 192.0.2.53
   $ dig example.com
   $ dig @192.0.2.53 example.com AAAA
   $ dig +short example.com
   $ dig +trace example.com

2 行目と 4 行目のように DNS サーバーを指定すると、普段使っているフルリゾルバー以外に問い合わせて、結果を比べられます。``dig +trace`` は、ルートサーバーから順に反復問い合わせを行う様子を表示します。Windows での ``nslookup`` の実行結果の例は次のとおりです（アドレスは文書用の値に置き換えています）。

.. code-block:: text

   Server:  UnKnown
   Address:  192.0.2.53

   Non-authoritative answer:
   Name:    example.com
   Addresses:  2001:db8::10
             2001:db8::11
             198.51.100.10
             198.51.100.11

``Server`` は問い合わせた DNS サーバーで、``UnKnown`` はそのサーバーのアドレスの逆引きができなかったことを示すだけで、問題ではありません。``Non-authoritative answer`` は、権威サーバーではなく、フルリゾルバーのキャッシュなどから得た回答であることを示します。存在しない名前を問い合わせると、``Non-existent domain``\ （``dig`` では ``status: NXDOMAIN``）と表示されます。

名前解決の問題を調べるときは、次の点を確かめます。

* ``nslookup`` や ``dig`` は DNS サーバーに直接問い合わせますが、アプリケーションは OS のリゾルバーを使い、hosts ファイルや OS のキャッシュも参照します。両者の結果が異なる場合は、hosts ファイル（Windows は ``C:\Windows\System32\drivers\etc\hosts``、Linux は ``/etc/hosts``）を確かめます。
* DNS のレコードを変更した直後は、古いレコードが TTL の間キャッシュに残ります。Windows では ``ipconfig /displaydns`` で OS のキャッシュを表示し、``ipconfig /flushdns`` で消去できます。
* 社内のネットワークや VPN の接続中は、名前によって問い合わせ先の DNS サーバーが切り替わることがあります。

netstat と ss
-------------

``netstat``\ （Windows と Linux）と ``ss``\ （Linux）は、自分のコンピューターのソケットの状態を表示するコマンドです。サーバーが目的のポートで待ち受けているか、どのようなコネクションがどの状態にあるかを確かめられます。Linux では ``netstat`` は古いコマンドとされ、``ss`` が推奨されています。

.. code-block:: console
   :linenos:

   > netstat -ano
   > netstat -ano | findstr LISTENING
   $ ss -tlnp
   $ ss -tan state time-wait

Windows の ``-a`` はすべてのソケット、``-n`` はアドレスを数値で表示、``-o`` はプロセス ID の表示です。Linux の ``ss`` の ``-t`` は TCP、``-l`` は待ち受け中のもの、``-n`` は数値、``-p`` はプロセスの表示です。Windows での出力の一部を抜粋すると、次のとおりです（表示言語が英語の環境での例で、アドレスは文書用の値に置き換えています）。``127.0.0.1:50007`` を含む 2 行は、「:doc:`n09_socket_programming`」の ``tcp_echo_server.py`` を起動し、``tcp_echo_client.py`` を 1 回実行した直後のものです。

.. code-block:: text

   Active Connections

     Proto  Local Address          Foreign Address        State           PID
     TCP    0.0.0.0:135            0.0.0.0:0              LISTENING       1652
     TCP    0.0.0.0:445            0.0.0.0:0              LISTENING       4
     TCP    127.0.0.1:50007        0.0.0.0:0              LISTENING       20944
     TCP    127.0.0.1:60219        127.0.0.1:50007        TIME_WAIT       0
     TCP    192.0.2.81:52556       198.51.100.45:443      ESTABLISHED     18568
     TCP    192.0.2.81:53411       198.51.100.223:443     TIME_WAIT       0

``Local Address`` が ``0.0.0.0`` のものはすべてのインターフェースで、``127.0.0.1`` のものは同じコンピューターからの接続だけを待ち受けています。他のコンピューターから接続できないサーバーを調べるときは、待ち受けのアドレスが ``127.0.0.1`` になっていないかを確かめます。``127.0.0.1:60219`` の ``TIME_WAIT`` は、エコーのクライアント側のコネクションです。クライアントが ``shutdown()`` で先に FIN を送ったので、先に閉じた側であるクライアントに TIME_WAIT の状態が残っています。

コネクションの状態（「:doc:`n05_transport_layer`」を参照）からも、問題の手がかりが得られます。

.. list-table:: コネクションの状態から分かること
   :header-rows: 1
   :widths: 25 75

   * - 状態
     - 多数ある場合に考えられること
   * - ``SYN_SENT``
     - 接続先からの応答の欠如（ファイアウォールでの破棄、相手の停止など）
   * - ``SYN_RECEIVED``
     - ハンドシェイクの最後の ACK の未着。SYN を大量に送りつける攻撃（SYN フラッド。「:doc:`n08_network_security`」を参照）の可能性
   * - ``TIME_WAIT``
     - 短いコネクションの大量の生成と切断。コネクションの再利用（キープアライブやコネクションプール）を検討
   * - ``CLOSE_WAIT``
     - 相手は切断したのに、自分のアプリケーションがソケットを閉じていない状態（閉じ忘れの不具合）

特に ``CLOSE_WAIT`` が増え続ける場合は、ほぼ確実にアプリケーションの不具合で、ソケットを閉じ忘れている箇所を探します。

ポートへの接続を確かめる
------------------------

``ping`` が届いても、目的のサービスに接続できるとは限りません。TCP のポートに実際に接続を試みると、サービスが受け付けているかを直接確かめられます。Windows の PowerShell では ``Test-NetConnection``、Linux では ``nc``\ （netcat）を使います。

.. code-block:: console
   :linenos:

   PS> Test-NetConnection -ComputerName example.com -Port 443
   $ nc -vz -w 3 example.com 443

接続の失敗には、性質の異なる 3 つの種類があります。この区別は、原因を切り分けるうえで非常に重要です。

.. list-table:: 接続の失敗の種類
   :header-rows: 1
   :widths: 20 40 40

   * - 結果
     - 何が起きたか
     - 考えられる原因
   * - 名前解決失敗
     - ホスト名から IP アドレスを得られない状態
     - ホスト名の誤り、DNS の設定や障害
   * - 接続拒否
     - 相手のホストには届き、RST が返ってきた状態
     - サーバーのプログラムの停止、ポート番号の誤り、待ち受けのアドレスの誤り
   * - タイムアウト
     - 決めた時間内に何の応答もない状態
     - ファイアウォールでの破棄、経路の問題、相手のホストの停止

接続拒否は「相手のホストまでは届いている」ことの証拠で、調べる対象はそのホストの上のサービスに絞られます。タイムアウトは途中のどこかでパケットが失われていることを示し、ファイアウォールの設定や経路を調べます。

サンプルコード :download:`port_check.py <../examples/port_check.py>` は、タイムアウト付きの ``connect()`` で、成功とこの 3 種類の失敗を区別して表示します。引数を付けずに実行すると、localhost に一時的なサーバーを立てて、開いているポート、閉じているポート、存在しないホスト名を調べるデモになります。ソケットの使い方は「:doc:`n09_socket_programming`」を参照してください。

.. literalinclude:: ../examples/port_check.py
   :language: python
   :linenos:
   :caption: port_check.py

デモの実行結果は次のとおりです（ポート番号は実行のたびに変わります）。

.. code-block:: text

   一時サーバーを 127.0.0.1:62115 で起動しました
   127.0.0.1:62115 -> 成功（127.0.0.1）  [0.0 秒]
   127.0.0.1:62116 -> 接続拒否（127.0.0.1）  [2.0 秒]
   no-such-host.invalid:80 -> 名前解決失敗（getaddrinfo failed）  [0.0 秒]

``.invalid`` は、存在しないことが保証された予約済みのトップレベルドメインです（RFC 2606）。この結果は Windows で実行したもので、接続拒否と判定されるまでに約 2 秒かかっています。Windows は RST を受け取っても、すぐには失敗とせずに SYN を再送するためです。Linux では、接続拒否はすぐに判明します。

引数でホストとポート番号を指定することもできます。文書用のアドレス 192.0.2.1 の、使われていないポートを調べると、どこからも応答がないのでタイムアウトになります。

.. code-block:: console
   :linenos:

   > python port_check.py 192.0.2.1 12345 --timeout 2

.. code-block:: text

   192.0.2.1:12345 -> タイムアウト（192.0.2.1、2.0 秒）  [2.0 秒]

なお、同じアドレスの 80 番ポートを調べたところ、筆者の環境では「成功」と表示されました。80 番ポートへの通信を途中のプロキシやセキュリティ製品が代わりに受け付けていたためです。このように、途中の機器が接続を代理で受ける環境では、``connect()`` の成功は「本当の相手」に届いたことを意味しません。その場合は、次の ``curl`` のようにアプリケーション層まで確かめる必要があります。

curl
----

``curl`` は、HTTP などのリクエストを送り、レスポンスを表示するコマンドです。Windows 10 以降と多くの Linux のディストリビューションに標準で入っています。Windows の PowerShell では ``curl`` が別のコマンド（``Invoke-WebRequest``）の別名になっている場合があるので、``curl.exe`` と入力します。

.. code-block:: console
   :linenos:

   $ curl -v -o /dev/null https://example.com/
   $ curl -sS -o /dev/null -w "dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n" https://example.com/
   $ curl -v --resolve example.com:443:198.51.100.10 https://example.com/

1 行目の ``-v`` は、名前解決の結果、接続先、TLS のハンドシェイク、送ったリクエストのヘッダー（``>`` で始まる行）、受け取ったレスポンスのヘッダー（``<`` で始まる行）を詳しく表示します。実行結果の一部を抜粋すると、次のとおりです（アドレスは文書用の値に置き換えています）。

.. code-block:: text

   * Host example.com:443 was resolved.
   * IPv4: 198.51.100.10, 198.51.100.11
   *   Trying 198.51.100.10:443...
   * ALPN: curl offers http/1.1
   * ALPN: server accepted http/1.1
   > GET / HTTP/1.1
   > Host: example.com
   > User-Agent: curl/8.21.0
   > Accept: */*
   >
   < HTTP/1.1 200 OK
   < Content-Type: text/html; charset=utf-8
   < Connection: keep-alive

2 行目の ``-w`` は、処理の各段階が終わった時点までの経過時間（秒）を表示します。遅い原因がどの段階にあるかを切り分けるのに便利です。実行結果の例は次のとおりです。

.. code-block:: text

   dns=0.021206 connect=0.025370 tls=0.056672 ttfb=0.108509 total=0.108826

``dns`` が大きければ名前解決が、``connect`` と ``dns`` の差が大きければネットワークの遅延（TCP のハンドシェイクの往復）が、``ttfb``\ （最初の 1 バイトを受け取るまで）と ``tls`` の差が大きければサーバーの処理が遅いと分かります。3 行目の ``--resolve`` は、DNS を使わずに指定した IP アドレスに接続する指定で、ロードバランサーの配下にある特定のサーバーを直接試すときなどに使います。

``curl`` のエラーメッセージも、前の節の 3 種類の失敗に対応しています。

.. code-block:: text

   curl: (6) Could not resolve host: no-such-host.invalid
   curl: (7) Failed to connect to 127.0.0.1 port 50007 after 2033 ms: Couldn't connect to server
   curl: (28) Failed to connect to 192.0.2.1 port 12345 after 2000 ms: Timeout was reached

括弧の中の数字は ``curl`` の終了コードで、6 は名前解決の失敗、7 は接続の失敗（この例では接続拒否）、28 はタイムアウトです。

パケットキャプチャ
------------------

コマンドの結果だけでは原因が分からない場合は、実際に流れているパケットを記録して調べます。これをパケットキャプチャと呼びます。Linux では ``tcpdump``、Windows と Linux のどちらでも GUI の Wireshark がよく使われます。Windows には標準で ``pktmon`` というコマンドもあり、記録したファイルを ``pktmon etl2pcap`` で Wireshark で読める形式に変換できます。

.. code-block:: console
   :linenos:

   $ sudo tcpdump -i eth0 -nn 'tcp port 443'
   $ sudo tcpdump -i any -nn 'host 192.0.2.10 and port 53'
   $ sudo tcpdump -i eth0 -nn -w capture.pcap 'tcp port 8080'

1 行目はインターフェース ``eth0`` を通る TCP の 443 番ポートのパケットを表示し、2 行目はすべてのインターフェースで、特定のホストとの DNS の通信を表示します。3 行目は表示せずにファイルに保存し、後で Wireshark で開いて分析します。パケットキャプチャには管理者の権限が必要です。

Wireshark では、表示フィルターで見たいパケットを絞り込めます。障害の調査でよく使うフィルターを次の表に示します。

.. list-table:: Wireshark でよく使う表示フィルター
   :header-rows: 1
   :widths: 40 60

   * - フィルター
     - 表示されるもの
   * - ``ip.addr == 192.0.2.10``
     - 指定した IP アドレスとの通信
   * - ``tcp.port == 443``
     - 指定したポート番号の TCP の通信
   * - ``dns``
     - DNS の問い合わせと応答
   * - ``tcp.flags.syn == 1 && tcp.flags.ack == 0``
     - 接続の開始（SYN）だけ
   * - ``tcp.flags.reset == 1``
     - RST を含むパケット（接続拒否や強制切断）
   * - ``tcp.analysis.retransmission``
     - 再送されたパケット（パケットの損失の手がかり）

パケットキャプチャを読むときは、次の点を意識します。

* どこで記録したかが重要です。クライアントで SYN を送っているのにサーバーで SYN が見えなければ、途中で失われています。両端で同時に記録して比べると、問題の区間を特定できます。
* HTTPS などの TLS で暗号化された通信は、中身を読めません。それでも、TCP のハンドシェイク、再送、RST、TLS のハンドシェイクの成否、パケットの大きさとタイミングは分かります。
* パケットには個人情報やパスワードが含まれることがあります。記録したファイルの扱いには注意し、必要な範囲だけを記録します。

よくある症状と原因
------------------

ここまでのコマンドを使って、よくある症状の原因を切り分ける手順をまとめます。

.. list-table:: よくある症状と原因の候補
   :header-rows: 1
   :widths: 25 40 35

   * - 症状
     - 原因の候補
     - 確かめ方
   * - 名前解決の失敗
     - ホスト名の誤り、DNS サーバーの設定や障害、hosts ファイルの誤り、レコードの未登録や伝播待ち
     - ``nslookup`` で複数の DNS サーバーに問い合わせた結果の比較
   * - 接続の拒否
     - サーバーのプログラムの停止、ポート番号の誤り、``127.0.0.1`` だけでの待ち受け
     - サーバー側の ``netstat`` や ``ss`` による待ち受けの確認
   * - 接続のタイムアウト
     - ファイアウォールやセキュリティグループでの破棄、経路の問題、相手のホストの停止
     - ``tracert`` で止まる位置の確認、両端でのパケットキャプチャ
   * - 通信の遅さ
     - 名前解決の遅延、遠距離による遅延、パケットの損失と再送、サーバーの処理の遅延、帯域幅の不足
     - ``curl -w`` による段階ごとの時間の測定、``ping`` の損失率、キャプチャでの再送の確認
   * - 小さなデータは通るのに、大きなデータで止まる現象
     - MTU の不一致と、ICMP の破棄による Path MTU Discovery の失敗
     - 断片化禁止の ``ping`` で通る大きさの調査
   * - ときどきの失敗
     - 一部のサーバーやロードバランサーの配下の 1 台の不調、DNS のラウンドロビン、コネクションの上限
     - 失敗時の接続先の IP アドレスの記録と比較

遅い場合の考え方
~~~~~~~~~~~~~~~~

「遅い」には、1 回のリクエストの応答に時間がかかる（遅延の問題）場合と、大きなデータの転送に時間がかかる（スループットの問題）場合があります。遅延の問題は ``curl -w`` で段階ごとの時間を分けて、名前解決、接続、TLS、サーバーの処理のどこに時間がかかっているかを特定します。スループットの問題では、パケットの損失による再送と輻輳制御の働きや、帯域幅遅延積に対して小さすぎる TCP のウィンドウが原因になることがあります（「:doc:`n05_transport_layer`」を参照）。遠い相手との通信で 1 本のコネクションの速度が上がらない場合は、後者を疑います。

MTU の問題
~~~~~~~~~~

ログインの画面は表示されるのに大きなページで止まる、``ssh`` で接続できるのに大きなファイルの転送で止まる、といった症状は、MTU の問題の典型です。VPN やトンネルを通る経路では、ヘッダーが追加される分だけ MTU が小さくなります。このとき、途中のファイアウォールが Path MTU Discovery に必要な ICMP を破棄していると、大きなパケットだけが黙って失われ続けます（PMTUD ブラックホール。「:doc:`n04_internet_layer`」を参照）。

通る大きさは、断片化を禁止した ``ping`` で調べられます。

.. code-block:: console
   :linenos:

   > ping -f -l 1472 192.0.2.10
   $ ping -M do -s 1472 192.0.2.10

1 行目が Windows、2 行目が Linux です。1472 バイトは、Ethernet の MTU である 1500 バイトから、IP のヘッダー（20 バイト）と ICMP のヘッダー（8 バイト）を引いた値です。これで失敗し、大きさを小さくすると成功する場合は、経路のどこかの MTU が 1500 バイトより小さいことが分かります。対策としては、ICMP を破棄しないようにファイアウォールを設定する、ルーターで MSS クランプを行う、インターフェースの MTU を小さくする、などがあります。

Linux と Windows のコマンド対応表
---------------------------------

この章で紹介したコマンドを中心に、Linux と Windows で同じ目的に使うコマンドを次の表にまとめます。

.. list-table:: Linux と Windows のコマンドの対応
   :header-rows: 1
   :widths: 30 35 35

   * - 目的
     - Linux
     - Windows
   * - IP アドレスの確認
     - ``ip addr``
     - ``ipconfig``、``Get-NetIPAddress``
   * - 詳しい設定（DNS サーバーなど）
     - ``ip addr``、``resolvectl status``
     - ``ipconfig /all``
   * - ルーティングテーブル
     - ``ip route``
     - ``route print``、``Get-NetRoute``
   * - ARP のテーブル
     - ``ip neigh``
     - ``arp -a``、``Get-NetNeighbor``
   * - 疎通確認（ICMP）
     - ``ping -c 4``
     - ``ping -n 4``
   * - 経路の調査
     - ``traceroute``、``tracepath``
     - ``tracert``
   * - 経路と損失率の継続的な測定
     - ``mtr``
     - ``pathping``
   * - 名前解決
     - ``dig``、``nslookup``、``getent hosts``
     - ``nslookup``、``Resolve-DnsName``
   * - DNS のキャッシュの消去
     - ``resolvectl flush-caches``
     - ``ipconfig /flushdns``
   * - ソケットの状態
     - ``ss -tan``
     - ``netstat -ano``、``Get-NetTCPConnection``
   * - 待ち受け中のポート
     - ``ss -tlnp``
     - ``netstat -ano | findstr LISTENING``
   * - TCP のポートへの接続確認
     - ``nc -vz``
     - ``Test-NetConnection -Port``
   * - HTTP のリクエスト
     - ``curl``
     - ``curl.exe``
   * - パケットキャプチャ
     - ``tcpdump``、Wireshark
     - ``pktmon``、Wireshark
   * - MTU の確認（断片化禁止の ping）
     - ``ping -M do -s 1472``
     - ``ping -f -l 1472``

まとめ
------

* ネットワークの障害は、リンク層、IP、名前解決、トランスポート層、アプリケーション層と、下の層から順に確かめると効率よく切り分けられます。範囲（どの端末から、どの宛先へ）の切り分けも併せて行います。
* ``ping`` の応答がないことは相手の停止を意味せず、``ping`` が届くこともサービスへの接続を保証しません。サービスの確認には、TCP のポートへの接続や ``curl`` を使います。
* 接続の失敗は、名前解決失敗、接続拒否、タイムアウトに分けて考えます。接続拒否は相手のホストまで届いていることを、タイムアウトは途中でパケットが失われていることを示します。
* ``netstat`` や ``ss`` で見るコネクションの状態は手がかりになります。``CLOSE_WAIT`` が増え続けるのは、アプリケーションがソケットを閉じていない不具合です。
* 大きなデータだけが止まる場合は MTU の問題を、遅い場合は ``curl -w`` やパケットキャプチャで時間のかかっている段階を特定します。
