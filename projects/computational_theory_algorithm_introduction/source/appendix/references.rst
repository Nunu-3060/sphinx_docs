参考文献
========

本書の執筆にあたって参考にした文献と、さらに学ぶための文献を挙げる。

教科書
------

アルゴリズム
^^^^^^^^^^^^

* T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein: *Introduction to Algorithms*, 4th ed., MIT Press, 2022.

  アルゴリズムの標準的な教科書。データ構造、整列、グラフアルゴリズム、動的計画法から NP 完全性、近似アルゴリズムまで網羅している。第 3 版の邦訳『アルゴリズムイントロダクション』が近代科学社から出版されている。

* J. Kleinberg, É. Tardos: *Algorithm Design*, Pearson, 2005.

  問題からアルゴリズムを設計する過程を丁寧に説明している。貪欲法の正しさの証明や、NP 完全性の扱いが詳しい。邦訳『アルゴリズムデザイン』が共立出版から出版されている。

計算理論
^^^^^^^^

* M. Sipser: *Introduction to the Theory of Computation*, 3rd ed., Cengage Learning, 2012.

  オートマトン、計算可能性、計算複雑性を扱う計算理論の標準的な教科書。本書第 3 部の構成と多くの証明はこの本に倣っている。邦訳『計算理論の基礎』が共立出版から出版されている。

* J. E. Hopcroft, R. Motwani, J. D. Ullman: *Introduction to Automata Theory, Languages, and Computation*, 3rd ed., Pearson, 2006.

  オートマトンと形式言語の理論を詳しく扱っている。邦訳『オートマトン 言語理論 計算論』がサイエンス社から出版されている。

* S. Arora, B. Barak: *Computational Complexity: A Modern Approach*, Cambridge University Press, 2009.

  計算複雑性理論の発展的な教科書。本書第 11 章の先を学びたい読者に向く。

* M. R. Garey, D. S. Johnson: *Computers and Intractability: A Guide to the Theory of NP-Completeness*, W. H. Freeman, 1979.

  NP 完全性の古典的な解説書。巻末に数百の NP 完全問題の一覧がある。

近似アルゴリズム
^^^^^^^^^^^^^^^^

* V. V. Vazirani: *Approximation Algorithms*, Springer, 2001.

  近似アルゴリズムの体系的な教科書。本書第 12 章の頂点被覆や巡回セールスマン問題の近似アルゴリズムを詳しく扱っている。

論文
----

* A. M. Turing: On Computable Numbers, with an Application to the Entscheidungsproblem, *Proceedings of the London Mathematical Society*, s2-42(1), pp. 230-265, 1937.

  チューリング機械を導入し、停止問題に相当する問題の決定不能性を示した論文（第 10 章）。

* S. A. Cook: The Complexity of Theorem-Proving Procedures, *Proceedings of the 3rd Annual ACM Symposium on Theory of Computing*, pp. 151-158, 1971.

  NP 完全性の概念を導入し、SAT の NP 完全性を示した論文（第 11 章）。

* R. M. Karp: Reducibility among Combinatorial Problems, in *Complexity of Computer Computations*, Plenum Press, pp. 85-103, 1972.

  21 個の問題の NP 完全性を示した論文（第 11 章）。

* M. Agrawal, N. Kayal, N. Saxena: PRIMES is in P, *Annals of Mathematics*, 160(2), pp. 781-793, 2004.

  素数判定が多項式時間で行えることを示した論文（第 11 章、第 12 章）。

Web 上の資料
------------

* Python Software Foundation: `Python 標準ライブラリ <https://docs.python.org/ja/3/library/index.html>`_

  本書のサンプルコードで使っている ``heapq``\ 、\ ``bisect``\ 、\ ``collections``\ 、\ ``functools``\ 、\ ``re`` などのモジュールの公式ドキュメント。

* Python Wiki: `TimeComplexity <https://wiki.python.org/moin/TimeComplexity>`_

  CPython の組み込み型の操作の計算量の一覧（第 3 章）。
