参考文献
========

本書の内容をさらに深く学ぶための文献と、本書で触れた主な論文を挙げます。邦訳がある書籍は、原著の後に邦訳の書名を示しています。

OS の教科書
-----------

#. R. H. Arpaci-Dusseau, A. C. Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, Arpaci-Dusseau Books.

   仮想化（CPU とメモリ）、並行性、永続性の 3 つの柱で OS を解説する教科書です。Web で無償で公開されています（https://pages.cs.wisc.edu/~remzi/OSTEP/）。本書の全体に関連します。

#. A. S. Tanenbaum, H. Bos, *Modern Operating Systems*, Pearson.（邦訳『モダンオペレーティングシステム』ピアソン・エデュケーション）

   OS の定番の教科書の 1 つです。歴史や事例の紹介も豊富です。本書の全体に関連します。

#. A. Silberschatz, P. B. Galvin, G. Gagne, *Operating System Concepts*, Wiley.（邦訳『オペレーティングシステムの概念』培風館）

   OS の定番の教科書の 1 つです。スケジューリングやデッドロックなどの理論的な内容を詳しく扱っています。

Linux と Windows
----------------

4. M. Kerrisk, *The Linux Programming Interface*, No Starch Press.（邦訳『Linux プログラミングインタフェース』オライリー・ジャパン）

   Linux のシステムコールと C 標準ライブラリの使い方を網羅的に解説した書籍です。「:doc:`05_process`」から「:doc:`11_network`」に関連します。

#. D. P. Bovet, M. Cesati, *Understanding the Linux Kernel*, O'Reilly Media.（邦訳『詳解 Linux カーネル』オライリー・ジャパン）

   Linux カーネルの内部の実装を解説した書籍です。

#. 武内覚『［試して理解］Linux のしくみ』技術評論社

   プロセス、メモリ、ストレージなどの Linux の仕組みを、実験しながら学べる入門書です。「:doc:`14_practice`」に関連します。

#. P. Yosifovich, A. Ionescu, M. E. Russinovich, D. A. Solomon, *Windows Internals*, Microsoft Press.（邦訳『インサイド Windows』日経 BP）

   Windows の内部の仕組みを詳しく解説した書籍です。

#. B. Gregg, *Systems Performance: Enterprise and the Cloud*, Addison-Wesley.（邦訳『詳解 システム・パフォーマンス』オライリー・ジャパン）

   OS を中心とした性能分析の方法を解説した書籍です。USE メソッドもここで解説されています。「:doc:`14_practice`」に関連します。

歴史
----

9. F. P. Brooks, Jr., *The Mythical Man-Month: Essays on Software Engineering*, Addison-Wesley.（邦訳『人月の神話』丸善出版）

   OS/360 の開発の経験をもとにした、ソフトウェア開発の古典です。「:doc:`03_history`」に関連します。

#. L. Torvalds, D. Diamond, *Just for Fun: The Story of an Accidental Revolutionary*, HarperBusiness.（邦訳『それがぼくには楽しかったから』小学館プロダクション）

   Linux の作者による自伝です。Linux の誕生の経緯が語られています。「:doc:`03_history`」に関連します。

論文
----

11. F. J. Corbató, M. Merwin-Daggett, R. C. Daley, "An Experimental Time-Sharing System", *Proceedings of the AFIPS Spring Joint Computer Conference*, 1962.

    CTSS についての論文です。「:doc:`03_history`」に関連します。

#. E. W. Dijkstra, "The Structure of the 'THE'-Multiprogramming System", *Communications of the ACM*, Vol. 11, No. 5, 1968.

   階層構造の OS である THE についての論文です。「:doc:`03_history`」と「:doc:`06_thread`」に関連します。

#. L. A. Belady, R. A. Nelson, G. S. Shedler, "An Anomaly in Space-Time Characteristics of Certain Programs Running in a Paging Machine", *Communications of the ACM*, Vol. 12, No. 6, 1969.

   FIFO でフレーム数を増やすとページフォールトが増える現象（ビレイディの異常）を示した論文です。「:doc:`08_memory`」に関連します。

#. E. G. Coffman, M. J. Elphick, A. Shoshani, "System Deadlocks", *ACM Computing Surveys*, Vol. 3, No. 2, 1971.

   デッドロックの 4 条件を示した論文です。「:doc:`06_thread`」に関連します。

#. C. L. Liu, J. W. Layland, "Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment", *Journal of the ACM*, Vol. 20, No. 1, 1973.

   レートモノトニックと EDF を解析した論文です。「:doc:`07_scheduling`」に関連します。

#. D. M. Ritchie, K. Thompson, "The UNIX Time-Sharing System", *Communications of the ACM*, Vol. 17, No. 7, 1974.

   UNIX を初めて広く紹介した論文です。「:doc:`03_history`」に関連します。

#. G. J. Popek, R. P. Goldberg, "Formal Requirements for Virtualizable Third Generation Architectures", *Communications of the ACM*, Vol. 17, No. 7, 1974.

   効率よく仮想化できる計算機の条件を示した論文です。「:doc:`03_history`」と「:doc:`13_virtualization`」に関連します。

Web サイト
----------

18. The Linux man-pages project, https://man7.org/linux/man-pages/

    Linux のシステムコールやコマンドのマニュアルです。

#. The Linux Kernel documentation, https://docs.kernel.org/

   Linux カーネルの公式ドキュメントです。

#. The Open Group, POSIX.1-2024, https://pubs.opengroup.org/onlinepubs/9799919799/

   POSIX の規格の本文です。

#. Python ドキュメント「os --- 雑多なオペレーティングシステムインターフェース」, https://docs.python.org/ja/3/library/os.html

   本書のサンプルコードで使っている ``os`` モジュールの解説です。

#. Microsoft Learn「Sysinternals」, https://learn.microsoft.com/ja-jp/sysinternals/

   Process Explorer や Process Monitor などの、Windows の観察用のツールの解説です。「:doc:`14_practice`」に関連します。

#. B. Gregg, "The USE Method", https://www.brendangregg.com/usemethod.html

   USE メソッドの解説です。「:doc:`14_practice`」に関連します。

#. D. Kegel, "The C10K problem", http://www.kegel.com/c10k.html

   C10K 問題を提起した文書です。「:doc:`10_io_and_device`」に関連します。

#. MIT PDOS, xv6, https://github.com/mit-pdos/xv6-riscv

   教育用の小さな UNIX 系 OS である xv6 のソースコードです。「:doc:`15_summary`」に関連します。
