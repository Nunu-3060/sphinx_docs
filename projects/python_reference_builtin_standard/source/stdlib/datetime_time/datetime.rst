datetime
========

日付・時刻を扱うための型（``date``、``time``、``datetime``、``timedelta`` など）を提供するモジュール。カレンダー計算やタイムゾーンを考慮した日時処理を、文字列や秒数を直接扱うよりも安全かつ簡潔に記述できる。

datetime.now / datetime.today
------------------------------

現在時刻を表す ``datetime`` オブジェクトを取得する。

.. code-block:: python

   >>> from datetime import datetime
   >>> now = datetime.now()
   >>> now  # doctest: +SKIP
   datetime.datetime(2026, 9, 16, 13, 45, 30, 123456)
   >>> now.year, now.month, now.day
   (2026, 9, 16)
   >>> now.hour, now.minute, now.second
   (13, 45, 30)

date / time / datetime
-----------------------

``date`` は年月日、``time`` は時分秒、``datetime`` はその両方を保持するクラス。それぞれコンストラクタに数値を渡して直接生成できる。

.. code-block:: python

   >>> from datetime import date, time, datetime
   >>> d = date(2026, 9, 16)
   >>> t = time(9, 30, 0)
   >>> dt = datetime.combine(d, t)
   >>> dt
   datetime.datetime(2026, 9, 16, 9, 30)
   >>> d.weekday()  # 0=月曜
   2

strftime / strptime
--------------------

``strftime`` は ``datetime`` オブジェクトを書式文字列に変換し、``strptime`` は逆に文字列を解析して ``datetime`` オブジェクトを生成する。

.. code-block:: python

   >>> from datetime import datetime
   >>> dt = datetime(2026, 9, 16, 13, 45)
   >>> dt.strftime("%Y-%m-%d %H:%M:%S")
   '2026-09-16 13:45:00'
   >>> datetime.strptime("2026-09-16 13:45", "%Y-%m-%d %H:%M")
   datetime.datetime(2026, 9, 16, 13, 45)

timedelta による日付の計算
----------------------------

``timedelta`` は日時の差分・加減算に使う。日付や時刻同士を足し引きすることで、「n 日後」「n 時間前」といった計算を簡単に行える。

.. code-block:: python

   >>> from datetime import datetime, timedelta
   >>> dt = datetime(2026, 9, 16)
   >>> dt + timedelta(days=7)
   datetime.datetime(2026, 9, 23, 0, 0)
   >>> later = datetime(2026, 12, 25)
   >>> diff = later - dt
   >>> diff.days
   100

isoformat / fromisoformat
----------------------------

``isoformat()`` は ``datetime`` を ISO 8601 形式の文字列に変換し、``fromisoformat()`` はその逆に文字列から ``datetime`` を復元する。JSON や API のレスポンス、ログなどで日時をやり取りする際の標準的なシリアライズ方法。

.. code-block:: python

   >>> from datetime import datetime
   >>> dt = datetime(2026, 9, 16, 13, 45, 30)
   >>> s = dt.isoformat()
   >>> s
   '2026-09-16T13:45:30'
   >>> datetime.fromisoformat(s)
   datetime.datetime(2026, 9, 16, 13, 45, 30)

タイムゾーン付き datetime
----------------------------

``tzinfo`` を持たない ``datetime``（naive）は、タイムゾーンの情報を持たない単なる日時の値である。``timezone.utc`` などを指定することで、タイムゾーンを意識した（aware な）``datetime`` を扱える。

.. code-block:: python

   >>> from datetime import datetime, timezone, timedelta
   >>> utc_now = datetime.now(timezone.utc)
   >>> utc_now.tzinfo
   datetime.timezone.utc
   >>> jst = timezone(timedelta(hours=9))
   >>> utc_now.astimezone(jst)  # doctest: +SKIP
   datetime.datetime(2026, 9, 16, 22, 45, 30, 123456, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))

.. note::

   異なるタイムゾーンの ``datetime`` 同士を比較・演算する際は、両方を aware な ``datetime`` に統一しておく必要がある。naive と aware を混在させると ``TypeError`` が発生する。
