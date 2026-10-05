参考文献
========

本書の内容をさらに深く学ぶための文献と、本書で触れた主な論文や仕様書を挙げます。邦訳がある書籍は、原著の後に邦訳の書名を示しています。

教科書
------

#. D\. A. Patterson, J. L. Hennessy, *Computer Organization and Design RISC-V Edition: The Hardware/Software Interface*, 2nd ed., Morgan Kaufmann, 2020.

   命令セットアーキテクチャ、プロセッサの設計、パイプライン、メモリ階層を RISC-V を題材に解説する定番の教科書です。本書の「:doc:`06_isa`」から「:doc:`13_virtual_memory`」までの内容を詳しく学べます。MIPS を題材にした版の邦訳が『コンピュータの構成と設計』として日経 BP から出ています。

#. J\. L. Hennessy, D. A. Patterson, *Computer Architecture: A Quantitative Approach*, 6th ed., Morgan Kaufmann, 2017.（第 5 版の邦訳『コンピュータアーキテクチャ 定量的アプローチ 第 5 版』翔泳社）

   上の文献の発展的な内容を、定量的な評価を重視して扱う教科書です。命令レベル並列性、メモリ階層、並列アーキテクチャ、GPU、ドメイン特化型アーキテクチャを扱っています。

#. D\. Patterson, A. Waterman, *The RISC-V Reader: An Open Architecture Atlas*, Strawberry Canyon, 2017.（邦訳『RISC-V 原典 オープンアーキテクチャのススメ』日経 BP）

   RISC-V の設計者による ISA の解説書です。各命令の設計の理由が説明されています。「:doc:`appendix_riscv`」に関連します。

#. S\. L. Harris, D. Harris, *Digital Design and Computer Architecture: RISC-V Edition*, Morgan Kaufmann, 2021.

   論理回路から始めて、HDL で RISC-V プロセッサを設計するところまでを解説する教科書です。「:doc:`08_digital_logic`」と「:doc:`09_datapath`」に関連します。

#. R\. E. Bryant, D. R. O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed., Pearson, 2015.（第 2 版の邦訳『コンピュータ・システム プログラマの視点から』マイナビ出版）

   プログラマの視点から、データの表現、機械語、メモリ階層、仮想記憶などを解説する教科書です。「:doc:`05_data_representation`」「:doc:`07_machine_language`」「:doc:`12_memory_hierarchy`」に関連します。

#. D\. J. Sorin, M. D. Hill, D. A. Wood, *A Primer on Memory Consistency and Cache Coherence*, Morgan & Claypool, 2011.

   キャッシュコヒーレンスとメモリ一貫性モデルの解説書です。「:doc:`15_parallel`」に関連します。

#. W\. W. Hwu, D. B. Kirk, I. El Hajj, *Programming Massively Parallel Processors: A Hands-on Approach*, 4th ed., Morgan Kaufmann, 2022.

   CUDA を使った GPU プログラミングと、GPU のアーキテクチャを解説する教科書です。「:doc:`16_gpu`」に関連します。

歴史
----

8. J\. von Neumann, "First Draft of a Report on the EDVAC", Moore School of Electrical Engineering, University of Pennsylvania, 1945.

   プログラム内蔵方式の計算機の構成を記述した報告書です。「:doc:`03_history`」に関連します。

#. M\. V. Wilkes, "The Best Way to Design an Automatic Calculating Machine", Manchester University Computer Inaugural Conference, 1951.

   マイクロプログラム方式を提案した講演です。「:doc:`03_history`」と「:doc:`09_datapath`」に関連します。

#. G\. M. Amdahl, G. A. Blaauw, F. P. Brooks Jr., "Architecture of the IBM System/360", *IBM Journal of Research and Development*, Vol. 8, No. 2, 1964.

   「アーキテクチャ」という言葉を、実装と区別された計算機の仕様という意味で使った論文です。「:doc:`03_history`」に関連します。

#. F\. P. Brooks Jr., *The Mythical Man-Month*, Addison-Wesley, 1975.（邦訳『人月の神話』丸善出版）

   System/360 の OS の開発経験に基づく、ソフトウェア開発の古典です。

#. D\. A. Patterson, D. R. Ditzel, "The Case for the Reduced Instruction Set Computer", *ACM SIGARCH Computer Architecture News*, Vol. 8, No. 6, 1980.

   RISC の考え方を提唱した論文です。「:doc:`03_history`」と「:doc:`06_isa`」に関連します。

#. J\. L. Hennessy, D. A. Patterson, "A New Golden Age for Computer Architecture", *Communications of the ACM*, Vol. 62, No. 2, 2019.

   チューリング賞の受賞記念講演に基づく記事です。デナード・スケーリングの終わり、ドメイン特化型アーキテクチャ、オープンな ISA について論じています。「:doc:`03_history`」「:doc:`17_accelerators`」「:doc:`19_trends`」に関連します。

性能と技術の動向
----------------

14. G\. E. Moore, "Cramming More Components onto Integrated Circuits", *Electronics*, Vol. 38, No. 8, 1965.

    ムーアの法則のもとになった論文です。

#. R\. H. Dennard et al., "Design of Ion-Implanted MOSFET's with Very Small Physical Dimensions", *IEEE Journal of Solid-State Circuits*, Vol. 9, No. 5, 1974.

   デナード・スケーリングを示した論文です。「:doc:`04_performance`」と「:doc:`19_trends`」に関連します。

#. G\. M. Amdahl, "Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities", AFIPS Spring Joint Computer Conference, 1967.

   アムダールの法則のもとになった論文です。「:doc:`04_performance`」に関連します。

#. J\. L. Gustafson, "Reevaluating Amdahl's Law", *Communications of the ACM*, Vol. 31, No. 5, 1988.

   グスタフソンの法則を示した論文です。「:doc:`04_performance`」に関連します。

#. S\. Williams, A. Waterman, D. Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures", *Communications of the ACM*, Vol. 52, No. 4, 2009.

   ルーフラインモデルを提案した論文です。「:doc:`04_performance`」と「:doc:`16_gpu`」に関連します。

#. Wm. A. Wulf, S. A. McKee, "Hitting the Memory Wall: Implications of the Obvious", *ACM SIGARCH Computer Architecture News*, Vol. 23, No. 1, 1995.

   プロセッサとメモリの速度差（メモリウォール）を指摘した論文です。「:doc:`12_memory_hierarchy`」に関連します。

#. U\. Drepper, "What Every Programmer Should Know About Memory", Red Hat, 2007.

   DRAM、キャッシュ、NUMA の仕組みと、それを意識したプログラミングを解説する文書です。「:doc:`12_memory_hierarchy`」と「:doc:`15_parallel`」に関連します。

#. IEEE, *IEEE Standard for Floating-Point Arithmetic* (IEEE Std 754-2019), 2019.

   浮動小数点数の標準規格です。「:doc:`05_data_representation`」に関連します。

#. D\. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", *ACM Computing Surveys*, Vol. 23, No. 1, 1991.

   浮動小数点数の誤差と IEEE 754 の解説です。「:doc:`05_data_representation`」に関連します。

プロセッサの高速化と並列化
--------------------------

23. R\. M. Tomasulo, "An Efficient Algorithm for Exploiting Multiple Arithmetic Units", *IBM Journal of Research and Development*, Vol. 11, No. 1, 1967.

    Tomasulo のアルゴリズムを示した論文です。「:doc:`11_ilp`」に関連します。

#. J\. E. Smith, "A Study of Branch Prediction Strategies", Proceedings of the 8th Annual Symposium on Computer Architecture, 1981.

   2 ビット飽和カウンタなどの分岐予測の方式を評価した論文です。「:doc:`11_ilp`」に関連します。

#. S\. McFarling, "Combining Branch Predictors", DEC Western Research Laboratory, Technical Note TN-36, 1993.

   gshare 分岐予測器を示した技術報告です。「:doc:`11_ilp`」に関連します。

#. D\. M. Tullsen, S. J. Eggers, H. M. Levy, "Simultaneous Multithreading: Maximizing On-Chip Parallelism", Proceedings of the 22nd Annual International Symposium on Computer Architecture, 1995.

   同時マルチスレッディング（SMT）を提案した論文です。「:doc:`11_ilp`」に関連します。

#. M\. J. Flynn, "Very High-Speed Computing Systems", *Proceedings of the IEEE*, Vol. 54, No. 12, 1966.

   フリンの分類を示した論文です。「:doc:`15_parallel`」に関連します。

#. L\. Lamport, "How to Make a Multiprocessor Computer That Correctly Executes Multiprocess Programs", *IEEE Transactions on Computers*, Vol. C-28, No. 9, 1979.

   逐次一貫性を定義した論文です。「:doc:`15_parallel`」に関連します。

#. M\. S. Papamarcos, J. H. Patel, "A Low-Overhead Coherence Solution for Multiprocessors with Private Cache Memories", Proceedings of the 11th Annual International Symposium on Computer Architecture, 1984.

   MESI プロトコルの原型となった論文です。「:doc:`15_parallel`」に関連します。

GPU とアクセラレーター
----------------------

30. E\. Lindholm, J. Nickolls, S. Oberman, J. Montrym, "NVIDIA Tesla: A Unified Graphics and Computing Architecture", *IEEE Micro*, Vol. 28, No. 2, 2008.

    統合シェーダーアーキテクチャと SIMT による実行を解説した論文です。「:doc:`16_gpu`」に関連します。

#. A\. Krizhevsky, I. Sutskever, G. E. Hinton, "ImageNet Classification with Deep Convolutional Neural Networks", Advances in Neural Information Processing Systems 25, 2012.

   GPU で学習した深層ニューラルネットワーク（AlexNet）で画像認識の精度を大きく向上させた論文です。「:doc:`16_gpu`」に関連します。

#. H\. T. Kung, "Why Systolic Architectures?", *IEEE Computer*, Vol. 15, No. 1, 1982.

   シストリックアレイの考え方を解説した論文です。「:doc:`17_accelerators`」に関連します。

#. N\. P. Jouppi et al., "In-Datacenter Performance Analysis of a Tensor Processing Unit", Proceedings of the 44th Annual International Symposium on Computer Architecture, 2017.

   Google の初代 TPU の構成と性能を示した論文です。「:doc:`17_accelerators`」に関連します。

#. M\. Horowitz, "Computing's Energy Problem (and What We Can Do About It)", IEEE International Solid-State Circuits Conference, 2014.

   演算とメモリアクセスのエネルギーを比較し、データの移動のコストを示した講演です。「:doc:`17_accelerators`」に関連します。

#. A\. Putnam et al., "A Reconfigurable Fabric for Accelerating Large-Scale Datacenter Services", Proceedings of the 41st Annual International Symposium on Computer Architecture, 2014.

   データセンターでの FPGA の活用（Microsoft の Catapult）を示した論文です。「:doc:`17_accelerators`」に関連します。

セキュリティと信頼性
--------------------

36. R\. W. Hamming, "Error Detecting and Error Correcting Codes", *Bell System Technical Journal*, Vol. 29, No. 2, 1950.

    ハミング符号を示した論文です。「:doc:`18_security_reliability`」に関連します。

#. Y\. Yarom, K. Falkner, "FLUSH+RELOAD: A High Resolution, Low Noise, L3 Cache Side-Channel Attack", 23rd USENIX Security Symposium, 2014.

   Flush+Reload によるキャッシュタイミング攻撃を示した論文です。「:doc:`18_security_reliability`」に関連します。

#. Y\. Kim et al., "Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors", Proceedings of the 41st Annual International Symposium on Computer Architecture, 2014.

   Rowhammer を示した論文です。「:doc:`18_security_reliability`」に関連します。

#. M\. Lipp et al., "Meltdown: Reading Kernel Memory from User Space", 27th USENIX Security Symposium, 2018.

   Meltdown を示した論文です。「:doc:`18_security_reliability`」に関連します。

#. P\. Kocher et al., "Spectre Attacks: Exploiting Speculative Execution", IEEE Symposium on Security and Privacy, 2019.

   Spectre を示した論文です。「:doc:`18_security_reliability`」に関連します。

仕様書とマニュアル
------------------

41. RISC-V International, *The RISC-V Instruction Set Manual, Volume I: Unprivileged ISA*.

    RISC-V の基本命令セット、拡張、メモリモデル（RVWMO）を定める仕様書です。

#. RISC-V International, *The RISC-V Instruction Set Manual, Volume II: Privileged Architecture*.

   RISC-V の特権モード、CSR、ページテーブル（Sv32、Sv39 など）を定める仕様書です。

#. RISC-V International, *RISC-V ABIs Specification*.

   RISC-V の呼び出し規約と ELF の形式を定める仕様書です。「:doc:`07_machine_language`」に関連します。

#. Intel, *Intel 64 and IA-32 Architectures Software Developer's Manual*.

   x86-64 の命令セットとシステムアーキテクチャのマニュアルです。

#. Arm, *Arm Architecture Reference Manual for A-profile architecture*.

   AArch64 を含む Arm の A プロファイルのアーキテクチャのマニュアルです。

#. NVIDIA, *CUDA C++ Programming Guide*.

   CUDA のプログラミングモデルと、GPU のハードウェアの実装を解説するガイドです。「:doc:`16_gpu`」に関連します。
