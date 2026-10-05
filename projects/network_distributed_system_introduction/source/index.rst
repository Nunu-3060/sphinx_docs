ネットワーク・分散システム入門
==============================

本書は、エンジニアを対象にネットワークと分散システムの仕組みを解説する入門資料です。第 1 部ではネットワークを取り上げ、データがケーブルや電波を通じて相手のプログラムに届くまでの仕組みを、階層ごとに説明します。第 2 部では分散システムを取り上げ、ネットワークでつながった複数のコンピューターが協調して 1 つのサービスを提供するための考え方と技術を説明します。各章には Python のサンプルコードを用意しており、仕組みを手元で確かめながら読み進められます。

.. toctree::
   :maxdepth: 2
   :caption: はじめに

   introduction

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: 第 1 部 ネットワーク

   n01_network_overview
   n02_network_history
   n03_link_layer
   n04_internet_layer
   n05_transport_layer
   n06_dns
   n07_http
   n08_network_security
   n09_socket_programming
   n10_network_troubleshooting

.. toctree::
   :maxdepth: 2
   :numbered:
   :caption: 第 2 部 分散システム

   d01_distributed_overview
   d02_distributed_history
   d03_time_and_order
   d04_communication
   d05_replication
   d06_consistency
   d07_partitioning
   d08_consensus
   d09_reliability

.. toctree::
   :maxdepth: 2
   :caption: おわりに

   summary

.. toctree::
   :maxdepth: 1
   :caption: 付録

   appendix_glossary
   appendix_references
   appendix_examples
