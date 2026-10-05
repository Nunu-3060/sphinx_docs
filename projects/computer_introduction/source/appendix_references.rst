参考文献
========

本書の内容をさらに深く学ぶための文献と、本書で触れた主な論文を挙げます。邦訳がある書籍は、原著の後に邦訳の書名を示しています。

計算機全般
----------

#. C. Petzold, *Code: The Hidden Language of Computer Hardware and Software*, Microsoft Press.（邦訳『CODE コードから見たコンピュータのからくり』日経 BP ソフトプレス）

   電球とスイッチから始めて、論理回路、CPU、ソフトウェアまでを順に解説する読み物です。本書の全体と関連します。

#. N. Nisan, S. Schocken, *The Elements of Computing Systems: Building a Modern Computer from First Principles*, MIT Press.（邦訳『コンピュータシステムの理論と実装』オライリー・ジャパン）

   NAND ゲートから CPU、アセンブラ、コンパイラ、OS までを、自分で作りながら学ぶ教科書です。「:doc:`06_logic_circuits`」から「:doc:`08_software`」に関連します。

計算機アーキテクチャ
--------------------

3. D. A. Patterson, J. L. Hennessy, *Computer Organization and Design: The Hardware/Software Interface*, Morgan Kaufmann.（邦訳『コンピュータの構成と設計』日経 BP）

   計算機の構成についての定番の教科書です。「:doc:`07_architecture`」に関連します。

#. J. L. Hennessy, D. A. Patterson, *Computer Architecture: A Quantitative Approach*, Morgan Kaufmann.

   上の文献の発展的な内容を扱う教科書です。並列処理やドメイン特化型アーキテクチャも扱っています。「:doc:`09_modern_computers`」に関連します。

#. J. L. Hennessy, D. A. Patterson, "A New Golden Age for Computer Architecture", *Communications of the ACM*, Vol. 62, No. 2, 2019.

   チューリング賞の受賞記念講演に基づく記事です。デナード・スケーリングの終わりとドメイン特化型アーキテクチャについて論じています。

計算の理論
----------

6. M. Sipser, *Introduction to the Theory of Computation*, Cengage Learning.（邦訳『計算理論の基礎』共立出版）

   オートマトン、計算可能性、計算量の理論の定番の教科書です。「:doc:`04_theory`」に関連します。

#. A. M. Turing, "On Computable Numbers, with an Application to the Entscheidungsproblem", *Proceedings of the London Mathematical Society*, Series 2, Vol. 42, 1936.

   チューリングマシンと停止問題を示した論文です。

オペレーティングシステム
------------------------

8. A. S. Tanenbaum, H. Bos, *Modern Operating Systems*, Pearson.

   オペレーティングシステムの定番の教科書です。「:doc:`08_software`」に関連します。

情報の表現
----------

9. D. Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic", *ACM Computing Surveys*, Vol. 23, No. 1, 1991.

   浮動小数点数の性質と誤差を詳しく解説した論文です。「:doc:`05_information`」に関連します。

#. Python Software Foundation, 「浮動小数点演算、その問題と制限」, Python チュートリアル, https://docs.python.org/ja/3/tutorial/floatingpoint.html

   Python の float で生じる誤差の原因と対処法を解説しています。

#. The Unicode Consortium, https://home.unicode.org/

   Unicode の規格を定める団体の Web サイトです。

歴史的な文献
------------

12. J. von Neumann, "First Draft of a Report on the EDVAC", 1945.

    プログラム内蔵方式の計算機の構成を記述した報告書の草稿です。「:doc:`03_history`」に関連します。

#. C. E. Shannon, "A Symbolic Analysis of Relay and Switching Circuits", *Transactions of the American Institute of Electrical Engineers*, Vol. 57, No. 12, 1938.

   スイッチ回路とブール代数の対応を示した論文です。

#. G. E. Moore, "Cramming More Components onto Integrated Circuits", *Electronics*, Vol. 38, No. 8, 1965.

   ムーアの法則の元になった記事です。

#. R. H. Dennard et al., "Design of Ion-Implanted MOSFET's with Very Small Physical Dimensions", *IEEE Journal of Solid-State Circuits*, Vol. 9, No. 5, 1974.

   デナード・スケーリングを示した論文です。

#. G. M. Amdahl, "Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities", *AFIPS Spring Joint Computer Conference*, 1967.

   アムダールの法則の元になった論文です。

現代の計算機
------------

17. M. A. Nielsen, I. L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press.

    量子計算と量子情報の定番の教科書です。

#. P. W. Shor, "Algorithms for Quantum Computation: Discrete Logarithms and Factoring", *Proceedings of the 35th Annual Symposium on Foundations of Computer Science*, 1994.

   ショアのアルゴリズムを示した論文です。

#. TOP500, https://www.top500.org/

   スーパーコンピュータの性能ランキングを公開している Web サイトです。

#. NIST, Post-Quantum Cryptography, https://csrc.nist.gov/projects/post-quantum-cryptography

   アメリカ国立標準技術研究所による耐量子計算機暗号の標準化プロジェクトの Web サイトです。

#. RISC-V International, https://riscv.org/

   RISC-V の命令セットアーキテクチャの仕様を公開している団体の Web サイトです。
