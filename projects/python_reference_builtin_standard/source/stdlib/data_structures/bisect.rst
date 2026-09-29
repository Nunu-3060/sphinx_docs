bisect
======

ソート済みリストに対して、二分探索を用いた挿入位置の検索・挿入を行う
関数群を提供するモジュール。線形探索より高速に、順序を保ったまま
要素を追加できる。

bisect.bisect_left / bisect.bisect_right
--------------------------------------------

ソート済みリストに値を挿入する場合の位置を二分探索で求める。同じ値がすでに存在する場合、``bisect_left`` はその左側、``bisect_right`` （``bisect`` の別名）はその右側の位置を返す。

.. code-block:: python

   >>> import bisect
   >>> data = [1, 3, 3, 5, 7]
   >>> bisect.bisect_left(data, 3)
   1
   >>> bisect.bisect_right(data, 3)
   3
   >>> bisect.bisect_left(data, 4)
   3

bisect.insort
---------------

値を挿入すべき位置を探し、実際にリストへ挿入するところまでを一度に行う。``list.append`` してから ``list.sort`` するより効率的にソート順を維持できる。

.. code-block:: python

   >>> import bisect
   >>> data = [1, 3, 5, 7]
   >>> bisect.insort(data, 4)
   >>> data
   [1, 3, 4, 5, 7]

``insort`` は ``insort_right`` の別名であり、``bisect_right`` と同じ基準（同じ値が既に存在する場合はその右側）で挿入位置を決める。左側に挿入したい場合の対となる関数として ``insort_left`` （``bisect_left`` を使う版）も用意されている。

ソート済みリストを利用した二分探索
--------------------------------------

``bisect_left`` は、値がリスト中に存在するかどうかを二分探索で確認する
用途にも使える。存在確認だけでなく、区間の境界を求める処理（成績の
ランク分けなど）にも応用できる。

.. code-block:: python

   >>> import bisect
   >>> def grade(score, breakpoints=[60, 70, 80, 90], grades="FDCBA"):
   ...     i = bisect.bisect(breakpoints, score)
   ...     return grades[i]
   ...
   >>> [grade(s) for s in [55, 65, 85, 95]]
   ['F', 'D', 'B', 'A']
