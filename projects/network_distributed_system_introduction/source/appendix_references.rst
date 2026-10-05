参考文献
========

本書の内容をさらに深く学ぶための文献と、本書で触れた主な RFC と論文を挙げます。邦訳がある書籍は、原著の後に邦訳の書名を示しています。

ネットワークの教科書
--------------------

#. J. F. Kurose, K. W. Ross, *Computer Networking: A Top-Down Approach*, Pearson.

   アプリケーション層から下の層へ向かって、インターネットのプロトコルを解説する定番の教科書です。第 1 部の全体に関連します。

#. A. S. Tanenbaum, N. Feamster, D. J. Wetherall, *Computer Networks*, Pearson.（邦訳『コンピュータネットワーク』日経 BP）

   物理層から順にネットワークを解説する定番の教科書です。第 1 部の全体に関連します。

#. W. R. Stevens, K. R. Fall, *TCP/IP Illustrated, Volume 1: The Protocols*, Addison-Wesley.（邦訳『詳解 TCP/IP Vol.1 プロトコル』ピアソン・エデュケーション）

   パケットキャプチャの実例を使って、TCP/IP の各プロトコルの動きを詳しく解説した書籍です。「:doc:`n03_link_layer`」から「:doc:`n05_transport_layer`」に関連します。

#. 竹下隆史、村山公保、荒井透、苅田幸雄『マスタリング TCP/IP 入門編』オーム社

   TCP/IP の全体像を解説した日本語の入門書です。第 1 部の全体に関連します。

#. W. R. Stevens, B. Fenner, A. M. Rudoff, *UNIX Network Programming, Volume 1: The Sockets Networking API*, Addison-Wesley.（邦訳『UNIX ネットワークプログラミング』ピアソン・エデュケーション）

   ソケット API を使ったプログラミングの定番の書籍です。「:doc:`n09_socket_programming`」に関連します。

分散システムの教科書
--------------------

6. M. Kleppmann, *Designing Data-Intensive Applications*, O'Reilly Media, 2017.（邦訳『データ指向アプリケーションデザイン』オライリー・ジャパン）

   レプリケーション、パーティショニング、一貫性、合意などを、実際のデータベースの設計と結び付けて解説した書籍です。第 2 部の全体に関連します。

#. M. van Steen, A. S. Tanenbaum, *Distributed Systems*.（第 2 版の邦訳『分散システム 原理とパラダイム』ピアソン・エデュケーション）

   分散システムの定番の教科書です。「:doc:`d01_distributed_overview`」の定義はこの書籍によります。著者の Web サイトで、最新版の電子版が無償で公開されています。

#. B. Beyer, C. Jones, J. Petoff, N. R. Murphy（編）, *Site Reliability Engineering: How Google Runs Production Systems*, O'Reilly Media, 2016.（邦訳『SRE サイトリライアビリティエンジニアリング』オライリー・ジャパン）

   Google の運用の実践をまとめた書籍です。SLO、エラーバジェット、過負荷への対処などを扱っています。「:doc:`d09_reliability`」に関連します。

#. M. T. Nygard, *Release It!*, Pragmatic Bookshelf.（邦訳『Release It! 本番用ソフトウェア製品の設計とデプロイのために』オーム社）

   サーキットブレーカーやバルクヘッドなど、本番環境で障害に耐えるための設計パターンを紹介した書籍です。「:doc:`d09_reliability`」に関連します。

主な RFC
--------

RFC は、RFC Editor の Web サイト（https://www.rfc-editor.org/）で誰でも無償で読めます。新しい RFC によって古い RFC が置き換えられている場合があるので、読むときは最新のものを確認してください。

.. list-table:: 本書で触れた主な RFC
   :header-rows: 1
   :widths: 12 58 10 20

   * - 番号
     - 題名
     - 年
     - 関連する章
   * - RFC 768
     - User Datagram Protocol
     - 1980
     - :doc:`n05_transport_layer`
   * - RFC 791
     - Internet Protocol
     - 1981
     - :doc:`n04_internet_layer`
   * - RFC 792
     - Internet Control Message Protocol
     - 1981
     - :doc:`n04_internet_layer`
   * - RFC 826
     - An Ethernet Address Resolution Protocol
     - 1982
     - :doc:`n03_link_layer`
   * - RFC 1034
     - Domain Names - Concepts and Facilities
     - 1987
     - :doc:`n06_dns`
   * - RFC 1035
     - Domain Names - Implementation and Specification
     - 1987
     - :doc:`n06_dns`
   * - RFC 1191
     - Path MTU Discovery
     - 1990
     - :doc:`n04_internet_layer`
   * - RFC 1918
     - Address Allocation for Private Internets
     - 1996
     - :doc:`n04_internet_layer`
   * - RFC 2131
     - Dynamic Host Configuration Protocol
     - 1997
     - :doc:`n04_internet_layer`
   * - RFC 3022
     - Traditional IP Network Address Translator (Traditional NAT)
     - 2001
     - :doc:`n04_internet_layer`
   * - RFC 4033
     - DNS Security Introduction and Requirements
     - 2005
     - :doc:`n06_dns`
   * - RFC 4271
     - A Border Gateway Protocol 4 (BGP-4)
     - 2006
     - :doc:`n04_internet_layer`
   * - RFC 4632
     - Classless Inter-domain Routing (CIDR)
     - 2006
     - :doc:`n04_internet_layer`
   * - RFC 5681
     - TCP Congestion Control
     - 2009
     - :doc:`n05_transport_layer`
   * - RFC 5737
     - IPv4 Address Blocks Reserved for Documentation
     - 2010
     - :doc:`introduction`
   * - RFC 5905
     - Network Time Protocol Version 4
     - 2010
     - :doc:`d03_time_and_order`
   * - RFC 6265
     - HTTP State Management Mechanism
     - 2011
     - :doc:`n07_http`
   * - RFC 6298
     - Computing TCP's Retransmission Timer
     - 2011
     - :doc:`n05_transport_layer`
   * - RFC 6455
     - The WebSocket Protocol
     - 2011
     - :doc:`n07_http`
   * - RFC 6585
     - Additional HTTP Status Codes
     - 2012
     - :doc:`d09_reliability`
   * - RFC 6797
     - HTTP Strict Transport Security (HSTS)
     - 2012
     - :doc:`n08_network_security`
   * - RFC 7541
     - HPACK: Header Compression for HTTP/2
     - 2015
     - :doc:`n07_http`
   * - RFC 7858
     - Specification for DNS over Transport Layer Security (TLS)
     - 2016
     - :doc:`n06_dns`
   * - RFC 8200
     - Internet Protocol, Version 6 (IPv6) Specification
     - 2017
     - :doc:`n04_internet_layer`
   * - RFC 8446
     - The Transport Layer Security (TLS) Protocol Version 1.3
     - 2018
     - :doc:`n08_network_security`
   * - RFC 8484
     - DNS Queries over HTTPS (DoH)
     - 2018
     - :doc:`n06_dns`
   * - RFC 8555
     - Automatic Certificate Management Environment (ACME)
     - 2019
     - :doc:`n08_network_security`
   * - RFC 9000
     - QUIC: A UDP-Based Multiplexed and Secure Transport
     - 2021
     - :doc:`n05_transport_layer`
   * - RFC 9110
     - HTTP Semantics
     - 2022
     - :doc:`n07_http`
   * - RFC 9111
     - HTTP Caching
     - 2022
     - :doc:`n07_http`
   * - RFC 9112
     - HTTP/1.1
     - 2022
     - :doc:`n07_http`
   * - RFC 9113
     - HTTP/2
     - 2022
     - :doc:`n07_http`
   * - RFC 9114
     - HTTP/3
     - 2022
     - :doc:`n07_http`
   * - RFC 9293
     - Transmission Control Protocol (TCP)
     - 2022
     - :doc:`n05_transport_layer`
   * - RFC 9438
     - CUBIC for Fast and Long-Distance Networks
     - 2023
     - :doc:`n05_transport_layer`

ネットワークの論文
------------------

10. P. Baran, "On Distributed Communications", RAND Corporation, 1964.

    パケット交換の発想の源の 1 つとなった報告書です。「:doc:`n02_network_history`」に関連します。

#. V. G. Cerf, R. E. Kahn, "A Protocol for Packet Network Intercommunication", *IEEE Transactions on Communications*, 1974.

   異なるネットワークを相互に接続するためのプロトコルを提案した論文で、TCP/IP の出発点です。「:doc:`n02_network_history`」に関連します。

#. R. M. Metcalfe, D. R. Boggs, "Ethernet: Distributed Packet Switching for Local Computer Networks", *Communications of the ACM*, 1976.

   Ethernet を発表した論文です。「:doc:`n02_network_history`」と「:doc:`n03_link_layer`」に関連します。

#. W. Diffie, M. E. Hellman, "New Directions in Cryptography", *IEEE Transactions on Information Theory*, 1976.

   公開鍵暗号と鍵交換の考え方を発表した論文です。「:doc:`n08_network_security`」に関連します。

#. V. Jacobson, "Congestion Avoidance and Control", *ACM SIGCOMM*, 1988.

   輻輳崩壊の経験をもとに、TCP の輻輳制御を提案した論文です。「:doc:`n02_network_history`」と「:doc:`n05_transport_layer`」に関連します。

#. N. Cardwell, Y. Cheng, C. S. Gunn, S. H. Yeganeh, V. Jacobson, "BBR: Congestion-Based Congestion Control", *ACM Queue*, 2016.

   損失ではなく帯域幅と RTT の推定に基づく輻輳制御の BBR を紹介した記事です。「:doc:`n05_transport_layer`」に関連します。

分散システムの論文
------------------

16. L. Lamport, "Time, Clocks, and the Ordering of Events in a Distributed System", *Communications of the ACM*, 1978.

    happened-before 関係と論理時計を導入した論文です。「:doc:`d03_time_and_order`」に関連します。

#. L. Lamport, R. Shostak, M. Pease, "The Byzantine Generals Problem", *ACM Transactions on Programming Languages and Systems*, 1982.

   任意の誤った振る舞いをするノードがある場合の合意の問題を定式化した論文です。「:doc:`d01_distributed_overview`」と「:doc:`d02_distributed_history`」に関連します。

#. A. D. Birrell, B. J. Nelson, "Implementing Remote Procedure Calls", *ACM Transactions on Computer Systems*, 1984.

   RPC の実装を示した論文です。「:doc:`d02_distributed_history`」と「:doc:`d04_communication`」に関連します。

#. M. J. Fischer, N. A. Lynch, M. S. Paterson, "Impossibility of Distributed Consensus with One Faulty Process", *Journal of the ACM*, 1985.

   FLP 不可能性を証明した論文です。「:doc:`d08_consensus`」に関連します。

#. H. Garcia-Molina, K. Salem, "Sagas", *ACM SIGMOD*, 1987.

   長いトランザクションを補償可能な処理の列に分ける Saga を提案した論文です。「:doc:`d08_consensus`」に関連します。

#. M. P. Herlihy, J. M. Wing, "Linearizability: A Correctness Condition for Concurrent Objects", *ACM Transactions on Programming Languages and Systems*, 1990.

   線形化可能性を定義した論文です。「:doc:`d06_consistency`」に関連します。

#. D. Karger ほか, "Consistent Hashing and Random Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web", *ACM STOC*, 1997.

   コンシステントハッシュを提案した論文です。「:doc:`d07_partitioning`」に関連します。

#. L. Lamport, "The Part-Time Parliament", *ACM Transactions on Computer Systems*, 1998.

   Paxos を発表した論文です。より平易な解説として、同じ著者の "Paxos Made Simple"（*ACM SIGACT News*, 2001）があります。「:doc:`d08_consensus`」に関連します。

#. S. Gilbert, N. Lynch, "Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services", *ACM SIGACT News*, 2002.

   ブリューワーの予想を定式化し、CAP 定理として証明した論文です。「:doc:`d06_consistency`」に関連します。

#. S. Ghemawat, H. Gobioff, S.-T. Leung, "The Google File System", *ACM SOSP*, 2003.

   汎用のサーバーを束ねた大規模な分散ファイルシステムの論文です。「:doc:`d02_distributed_history`」に関連します。

#. J. Dean, S. Ghemawat, "MapReduce: Simplified Data Processing on Large Clusters", *USENIX OSDI*, 2004.

   大規模なデータの並列処理の枠組みを示した論文です。「:doc:`d02_distributed_history`」に関連します。

#. G. DeCandia ほか, "Dynamo: Amazon's Highly Available Key-value Store", *ACM SOSP*, 2007.

   リーダーレスレプリケーション、クォーラム、コンシステントハッシュを組み合わせたデータストアの論文です。「:doc:`d05_replication`」と「:doc:`d07_partitioning`」に関連します。

#. P. Hunt, M. Konar, F. P. Junqueira, B. Reed, "ZooKeeper: Wait-free Coordination for Internet-scale Systems", *USENIX ATC*, 2010.

   分散システムの協調のためのサービスである ZooKeeper の論文です。「:doc:`d08_consensus`」に関連します。

#. J. C. Corbett ほか, "Spanner: Google's Globally-Distributed Database", *USENIX OSDI*, 2012.

   TrueTime を使って世界規模で一貫性のあるトランザクションを実現したデータベースの論文です。「:doc:`d03_time_and_order`」と「:doc:`d08_consensus`」に関連します。

#. E. Brewer, "CAP Twelve Years Later: How the "Rules" Have Changed", *IEEE Computer*, 2012.

   CAP 定理の提唱者自身が、その正しい理解と誤解を解説した記事です。「:doc:`d06_consistency`」に関連します。

#. D. Abadi, "Consistency Tradeoffs in Modern Distributed Database System Design", *IEEE Computer*, 2012.

   PACELC をまとめた記事です。「:doc:`d06_consistency`」に関連します。

#. J. Dean, L. A. Barroso, "The Tail at Scale", *Communications of the ACM*, 2013.

   大規模なシステムで裾の遅延が問題になる理由と対策を論じた記事です。「:doc:`d09_reliability`」に関連します。

#. D. Ongaro, J. Ousterhout, "In Search of an Understandable Consensus Algorithm", *USENIX ATC*, 2014.

   Raft を発表した論文です。Raft の Web サイト（https://raft.github.io/）には、論文や動作を確かめられる可視化が公開されています。「:doc:`d08_consensus`」に関連します。
