heapq
=====

通常の ``list`` を二分ヒープとして扱うための関数群を提供するモジュール。最小値を常に高速に取り出したい場合に使う、優先度付きキューの実装でよく利用される。

heapq.heappush / heapq.heappop
---------------------------------

リストをヒープとして保ったまま要素を追加・取り出しする。``heappop`` は常にヒープ中の最小値を取り出す。

.. code-block:: python
   :linenos:

   >>> import heapq
   >>> heap = []
   >>> heapq.heappush(heap, 5)
   >>> heapq.heappush(heap, 1)
   >>> heapq.heappush(heap, 3)
   >>> heap
   [1, 5, 3]
   >>> heapq.heappop(heap)
   1
   >>> heap
   [3, 5]

追加と取り出しを 1 回の操作で行いたい場合は、``heappush`` と ``heappop`` を個別に呼ぶよりも ``heapq.heapreplace``\ （取り出してから追加）や ``heapq.heappushpop``\ （追加してから取り出す）を使うほうが効率的。

.. code-block:: python
   :linenos:

   >>> heap = [1, 5, 3]
   >>> heapq.heapreplace(heap, 2)  # 1 を取り出し、2 を追加
   1
   >>> heap
   [2, 5, 3]
   >>> heapq.heappushpop(heap, 0)  # 0 を追加してから最小値を取り出す
   0

heapq.heapify
---------------

既存のリストをその場（in-place）でヒープ構造に並べ替える。ゼロから ``heappush`` するより効率的にヒープを構築できる。

.. code-block:: python
   :linenos:

   >>> import heapq
   >>> data = [5, 1, 8, 3, 9, 2]
   >>> heapq.heapify(data)
   >>> data
   [1, 3, 2, 5, 9, 8]
   >>> heapq.heappop(data)
   1

heapq.nlargest / heapq.nsmallest
------------------------------------

イテラブルの中から上位 n 件・下位 n 件を取得する。n が全体の件数に比べて小さい場合は、全体をソートしてから先頭を切り出すより効率的である。``key`` 引数で並び替えの基準を指定できる。なお、1 件だけ欲しい場合は組み込みの ``min()`` / ``max()`` を、n が大きい場合は ``sorted()`` を使うほうが速い。

.. code-block:: python
   :linenos:

   >>> import heapq
   >>> scores = [{"name": "a", "score": 80}, {"name": "b", "score": 95},
   ...           {"name": "c", "score": 70}]
   >>> heapq.nlargest(2, scores, key=lambda s: s["score"])
   [{'name': 'b', 'score': 95}, {'name': 'a', 'score': 80}]
   >>> heapq.nsmallest(1, [5, 1, 8, 3])
   [1]

優先度付きキューとしての利用
-------------------------------

タスクを優先度順に処理したい場合、``(優先度, データ)`` のタプルをヒープに積むことで簡易な優先度付きキューを実装できる。優先度の値が小さいほど先に取り出される。

.. code-block:: python
   :linenos:

   >>> import heapq
   >>> queue = []
   >>> heapq.heappush(queue, (2, "回収作業"))
   >>> heapq.heappush(queue, (1, "緊急対応"))
   >>> heapq.heappush(queue, (3, "定例会議"))
   >>> while queue:
   ...     priority, task = heapq.heappop(queue)
   ...     print(priority, task)
   ...
   1 緊急対応
   2 回収作業
   3 定例会議

優先度が同じ要素が複数あると、タプルの 2 番目の要素同士が比較される。データ部分が比較できない型（辞書など）の場合は ``TypeError`` になるため、``(優先度, 連番, データ)`` のように一意な連番を挟むとよい。

.. note::

   ``heapq`` の基本関数は最小ヒープとして動作する。最大値を先に取り出したい場合、Python 3.13 以前では値の符号を反転して（``-priority`` のように）格納するのが定番だった。Python 3.14 以降では、最大ヒープ用の ``heapify_max``、``heappush_max``、``heappop_max``、``heappushpop_max``、``heapreplace_max`` が追加されている。

   .. code-block:: python
      :linenos:

      >>> import heapq
      >>> heap = []
      >>> for x in [5, 1, 3]:
      ...     heapq.heappush_max(heap, x)
      ...
      >>> heapq.heappop_max(heap)
      5
