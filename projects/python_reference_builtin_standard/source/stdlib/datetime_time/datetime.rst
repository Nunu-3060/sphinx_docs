datetime
========

日付・時刻を扱うための型（``date``、``time``、``datetime``、``timedelta`` など）を提供するモジュール。カレンダー計算やタイムゾーンを考慮した日時処理を、文字列や秒数を直接扱うよりも安全かつ簡潔に記述できる。

datetime.now / datetime.today
------------------------------

現在のローカル日時を表す ``datetime`` オブジェクトを取得する。引数なしの ``now()`` と ``today()`` はどちらもタイムゾーン情報を持たない（naive な）ローカル日時を返す。``now()`` には ``now(timezone.utc)`` のようにタイムゾーンを渡せるため、通常は ``now()`` を使う（後述の「タイムゾーン付き datetime」を参照）。

.. code-block:: python
   :linenos:

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

``date`` は年月日、``time`` は時分秒（とマイクロ秒）、``datetime`` はその両方を保持するクラスである。それぞれコンストラクタに数値を渡して直接生成でき、``datetime.combine()`` で ``date`` と ``time`` から ``datetime`` を組み立てられる。

.. code-block:: python
   :linenos:

   >>> from datetime import date, time, datetime
   >>> d = date(2026, 9, 16)
   >>> t = time(9, 30, 0)
   >>> dt = datetime.combine(d, t)
   >>> dt
   datetime.datetime(2026, 9, 16, 9, 30)
   >>> d.weekday()  # 月曜が 0、日曜が 6
   2

strftime / strptime
--------------------

``strftime`` は ``datetime`` オブジェクトを書式文字列に変換し、``strptime`` は逆に文字列を解析して ``datetime`` オブジェクトを生成する。

.. code-block:: python
   :linenos:

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
   :linenos:

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

``isoformat()`` は ``datetime`` を ISO 8601 形式の文字列に変換し、``fromisoformat()`` はその逆に文字列から ``datetime`` を復元する。JSON や API のレスポンス、ログなどで日時をやり取りする際の標準的なシリアライズ方法である。Python 3.11 以降の ``fromisoformat()`` は、UTC を表す末尾の ``Z`` など ISO 8601 の一般的な表記のほとんどを解析できる（3.10 以前は ``isoformat()`` が出力する形式しか受け付けなかった）。

.. code-block:: python
   :linenos:

   >>> from datetime import datetime
   >>> dt = datetime(2026, 9, 16, 13, 45, 30)
   >>> s = dt.isoformat()
   >>> s
   '2026-09-16T13:45:30'
   >>> datetime.fromisoformat(s)
   datetime.datetime(2026, 9, 16, 13, 45, 30)
   >>> datetime.fromisoformat("2026-09-16T13:45:30Z")
   datetime.datetime(2026, 9, 16, 13, 45, 30, tzinfo=datetime.timezone.utc)

タイムゾーン付き datetime
----------------------------

``tzinfo`` を持たない ``datetime``\ （naive）は、タイムゾーンの情報を持たない単なる日時の値である。``timezone.utc`` などを指定することで、タイムゾーンを意識した（aware な）``datetime`` を扱える。``astimezone()`` で別のタイムゾーンに変換できる。

.. code-block:: python
   :linenos:

   >>> from datetime import datetime, timezone, timedelta
   >>> utc_now = datetime.now(timezone.utc)
   >>> utc_now.tzinfo
   datetime.timezone.utc
   >>> jst = timezone(timedelta(hours=9))
   >>> utc_now.astimezone(jst)  # doctest: +SKIP
   datetime.datetime(2026, 9, 16, 22, 45, 30, 123456, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))

.. note::

   異なるタイムゾーンの ``datetime`` 同士を比較・演算する際は、両方を aware な ``datetime`` に統一しておく必要がある。naive と aware を混在させると、大小比較や減算では ``TypeError`` が発生する（``==`` による比較は例外にならず、常に ``False`` になる）。

.. warning::

   現在の UTC 日時を得る ``datetime.utcnow()`` や、エポック秒から UTC 日時を得る ``datetime.utcfromtimestamp()`` は Python 3.12 で非推奨になった。これらは UTC の日時を naive な ``datetime`` として返すため、ローカル日時と取り違えやすい。代わりに ``datetime.now(timezone.utc)`` や ``datetime.fromtimestamp(ts, timezone.utc)`` を使い、aware な ``datetime`` を得る。

zoneinfo による地域名のタイムゾーン
--------------------------------------

``timezone`` は UTC からの固定のオフセットしか表せないため、夏時間（サマータイム）のある地域を正しく扱えない。``"Asia/Tokyo"`` や ``"America/New_York"`` のような IANA タイムゾーン名で指定したい場合は、標準ライブラリの ``zoneinfo`` モジュールの ``ZoneInfo`` を使う。

.. code-block:: python
   :linenos:

   >>> from datetime import datetime
   >>> from zoneinfo import ZoneInfo
   >>> dt = datetime(2026, 7, 1, 12, 0, tzinfo=ZoneInfo("America/New_York"))
   >>> dt.utcoffset()
   datetime.timedelta(days=-1, seconds=72000)
   >>> dt.astimezone(ZoneInfo("Asia/Tokyo"))
   datetime.datetime(2026, 7, 2, 1, 0, tzinfo=zoneinfo.ZoneInfo(key='Asia/Tokyo'))

.. note::

   ``zoneinfo`` は OS のタイムゾーンデータベースを利用する。Windows などデータベースを持たない環境では、PyPI の ``tzdata`` パッケージをインストールする必要がある。
