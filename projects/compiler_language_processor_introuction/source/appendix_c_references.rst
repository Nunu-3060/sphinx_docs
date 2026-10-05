################################################################
付録 C 参考文献
################################################################

書籍
================================================================

.. [Aho2006] Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman. *Compilers: Principles, Techniques, and Tools*, 2nd Edition. Addison-Wesley, 2006.

   「ドラゴンブック」と呼ばれるコンパイラの定番の教科書です。字句解析と構文解析の理論（有限オートマトン、LR 構文解析など）が特に詳しく書かれています。

.. [Appel1998] Andrew W. Appel. *Modern Compiler Implementation in ML*. Cambridge University Press, 1998.

   1 つのコンパイラを作りながら、SSA 形式、データフロー解析、レジスタ割り当て（グラフ彩色）、ガベージコレクションまでを扱います。C 版と Java 版もあります。

.. [Cooper2022] Keith D. Cooper, Linda Torczon. *Engineering a Compiler*, 3rd Edition. Morgan Kaufmann, 2022.

   コンパイラの後半（中間表現、最適化、命令選択、レジスタ割り当て）が詳しく、実装上の工夫も多く紹介されています。

.. [Nystrom2021] Robert Nystrom. *Crafting Interpreters*. Genever Benning, 2021. https://craftinginterpreters.com/

   小さな言語の木構造インタプリタ（Java）とバイトコード仮想マシン（C）を一から作る本です。Web 上で全文を読めます。

.. [Jones2023] Richard Jones, Antony Hosking, Eliot Moss. *The Garbage Collection Handbook: The Art of Automatic Memory Management*, 2nd Edition. CRC Press, 2023.

   ガベージコレクションの方式を網羅的に解説した本です。

論文
================================================================

.. [Pratt1973] Vaughan R. Pratt. Top Down Operator Precedence. In *Proceedings of the 1st Annual ACM SIGACT-SIGPLAN Symposium on Principles of Programming Languages (POPL)*, pp. 41–51, 1973.

.. [Cytron1991] Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman, F. Kenneth Zadeck. Efficiently Computing Static Single Assignment Form and the Control Dependence Graph. *ACM Transactions on Programming Languages and Systems*, 13(4), pp. 451–490, 1991.

.. [Wegman1991] Mark N. Wegman, F. Kenneth Zadeck. Constant Propagation with Conditional Branches. *ACM Transactions on Programming Languages and Systems*, 13(2), pp. 181–210, 1991.

.. [Poletto1999] Massimiliano Poletto, Vivek Sarkar. Linear Scan Register Allocation. *ACM Transactions on Programming Languages and Systems*, 21(5), pp. 895–913, 1999.

.. [Cooper2001] Keith D. Cooper, Timothy J. Harvey, Ken Kennedy. A Simple, Fast Dominance Algorithm. *Software: Practice and Experience*, 2001.

.. [Cheney1970] C. J. Cheney. A Nonrecursive List Compacting Algorithm. *Communications of the ACM*, 13(11), pp. 677–678, 1970.

Web 上の資料
================================================================

.. [PEP617] Guido van Rossum, Pablo Galindo, Lysandros Nikolaou. PEP 617 – New PEG parser for CPython. https://peps.python.org/pep-0617/

.. [PEP659] Mark Shannon. PEP 659 – Specializing Adaptive Interpreter. https://peps.python.org/pep-0659/

.. [PEP744] Brandt Bucher, Savannah Ostrowski. PEP 744 – JIT Compilation. https://peps.python.org/pep-0744/

.. [LSP] Language Server Protocol. https://microsoft.github.io/language-server-protocol/

本書で紹介した Python の標準ライブラリのモジュールと、関連するツールの文書です。

* `tokenize — Python ソースのためのトークナイザ <https://docs.python.org/ja/3/library/tokenize.html>`_
* `ast — 抽象構文木 <https://docs.python.org/ja/3/library/ast.html>`_
* `symtable — コンパイラの記号表へのアクセス <https://docs.python.org/ja/3/library/symtable.html>`_
* `dis — Python バイトコードの逆アセンブラ <https://docs.python.org/ja/3/library/dis.html>`_
* `LLVM Language Reference Manual <https://llvm.org/docs/LangRef.html>`_
* `Graphviz <https://graphviz.org/>`_
