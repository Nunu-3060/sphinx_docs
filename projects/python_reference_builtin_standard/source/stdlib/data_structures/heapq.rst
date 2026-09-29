heapq
=====

通常の ``list`` を二分ヒープとして扱うための関数群を提供するモジュール。
最小値を常に高速に取り出したい場合に使う、優先度付きキューの実装で
よく利用される。

heapq.heappush / heapq.heappop
---------------------------------

リストをヒープとして保ったまま要素を追加・取り出しする。``heappop`` は
常にヒープ中の最小値を取り出す。

.. code-block:: python

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

追加と取り出しを 1 回の操作で行いたい場合は、``heappush`` と ``heappop`` を個別に呼ぶよりも ``heapq.heapreplace`` （取り出してから追加）や ``heapq.heappushpop`` （追加してから取り出す）を使うほうが効率的。

.. code-block:: python

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

   >>> import heapq
   >>> data = [5, 1, 8, 3, 9, 2]
   >>> heapq.heapify(data)
   >>> data
   [1, 3, 2, 5, 9, 8]
   >>> heapq.heappop(data)
   1

heapq.nlargest / heapq.nsmallest
------------------------------------

イテラブルの中から上位 n 件・下位 n 件を取得する。``sorted(iterable)[:n]`` より効率的で、``key`` 引数で並び替えの基準を指定できる。

.. code-block:: python

   >>> import heapq
   >>> scores = [{"name": "a", "score": 80}, {"name": "b", "score": 95},
   ...           {"name": "c", "score": 70}]
   >>> heapq.nlargest(2, scores, key=lambda s: s["score"])
   [{'name': 'b', 'score': 95}, {'name': 'a', 'score': 80}]
   >>> heapq.nsmallest(1, [5, 1, 8, 3])
   [1]

優先度付きキューとしての利用
-------------------------------

タスクを優先度順に処理したい場合、``(優先度, データ)`` のタプルを
ヒープに積むことで簡易な優先度付きキューを実装できる。優先度の値が
小さいほど先に取り出される。

.. code-block:: python

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
