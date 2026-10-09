"""第 15 章のケーススタディで使う、架空の Web API のアクセスログ.

1 週間（168 時間）分のリクエストについて、受け付けた時刻、
エンドポイント、応答時間を作る。次の性質を持たせている。

* 昼間はリクエストが多く、夜間は少ない
* /products はキャッシュに当たると速く、外れると遅い（山が 2 つ）
* /search はリクエストが多い時間帯ほど遅くなる
* 4 日目の 8 時から 3 時間、障害で全体が遅くなる
"""

import numpy as np

ENDPOINTS = ["/products", "/search", "/checkout"]
HOURS = 7 * 24
REQUESTS = 50000
INCIDENT_START = 3 * 24 + 8  # 4 日目の 8 時
INCIDENT_HOURS = 3


def hourly_load() -> np.ndarray:
    """時間帯ごとのリクエストの多さ（最大 1）を、168 時間分返す."""
    hour_of_day = np.arange(HOURS) % 24
    # 14 時頃に最大、2 時頃に最小となる日周期
    return 0.55 + 0.45 * np.cos((hour_of_day - 14) / 24 * 2 * np.pi)


def make_log() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """受付時刻（時間）、エンドポイントの番号、応答時間（ミリ秒）を返す."""
    rng = np.random.default_rng(15)
    load = hourly_load()
    hours = rng.choice(HOURS, REQUESTS, p=load / load.sum())
    times = hours + rng.uniform(0, 1, REQUESTS)
    endpoints = rng.choice(len(ENDPOINTS), REQUESTS, p=[0.6, 0.3, 0.1])

    response = np.empty(REQUESTS)
    products = endpoints == 0
    cache_hit = rng.uniform(0, 1, REQUESTS) < 0.8
    response[products & cache_hit] = rng.lognormal(
        np.log(30), 0.3, np.sum(products & cache_hit))
    response[products & ~cache_hit] = rng.lognormal(
        np.log(180), 0.3, np.sum(products & ~cache_hit))
    search = endpoints == 1
    response[search] = (rng.lognormal(np.log(90), 0.4, np.sum(search))
                        * (1 + 2.0 * load[hours[search]]))
    checkout = endpoints == 2
    response[checkout] = rng.lognormal(np.log(250), 0.3, np.sum(checkout))

    incident = ((times >= INCIDENT_START)
                & (times < INCIDENT_START + INCIDENT_HOURS))
    response[incident] *= 4
    return times, endpoints, response
