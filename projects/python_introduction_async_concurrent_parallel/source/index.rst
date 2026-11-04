Python による非同期処理・並行処理・並列処理
============================================

本書は、Python の知識があるエンジニアを対象に、非同期処理・並行処理・並列処理の考え方と実装方法を解説する資料である。スレッド、プロセス、``asyncio`` のそれぞれがどのような処理に向いているのかを理解し、場面に応じて適切な手法を選んで実装できるようになることを目指す。

本書は Python 3.11 以降を対象としており、サンプルコードは Python 3.14 で動作を確認している。サンプルコードは標準ライブラリだけで動作する。各章のサンプルコードは、本文中のファイル名のリンクからダウンロードできる。

.. toctree::
   :maxdepth: 2
   :caption: 目次

   chapters/01_introduction
   chapters/02_concepts
   chapters/03_gil
   chapters/04_choosing
   chapters/05_threads
   chapters/06_processes
   chapters/07_futures
   chapters/08_asyncio_basics
   chapters/09_asyncio_practice
   chapters/10_new_options
   chapters/11_debugging
   chapters/12_case_studies
   chapters/13_summary
   chapters/14_glossary
   chapters/15_references
