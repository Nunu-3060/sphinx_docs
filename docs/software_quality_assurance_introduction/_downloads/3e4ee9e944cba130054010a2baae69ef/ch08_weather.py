"""第 8 章のサンプル: 降水確率から傘の要否を助言します。

天気情報の取得元を引数で受け取る（依存性の注入）ことで、
テストでは外部 API の代わりにテストダブルを使えるようにしています。
"""

import json
import urllib.parse
import urllib.request
from typing import Protocol


class WeatherSource(Protocol):
    """天気情報の取得元が満たすべきインターフェースです。"""

    def precipitation_probability(self, city: str) -> int:
        """都市の降水確率（%）を返します。"""
        ...


class HttpWeatherSource:
    """HTTP の API から降水確率を取得する実装です。"""

    def __init__(self, base_url: str, timeout: float = 5.0) -> None:
        if not base_url.startswith("https://"):
            raise ValueError("base_url には https の URL を指定してください")
        self._base_url = base_url
        self._timeout = timeout

    def precipitation_probability(self, city: str) -> int:
        query = urllib.parse.urlencode({"city": city})
        url = f"{self._base_url}?{query}"
        with urllib.request.urlopen(url, timeout=self._timeout) as response:
            data = json.load(response)
        return int(data["precipitation_probability"])


def umbrella_advice(source: WeatherSource, city: str) -> str:
    """降水確率に応じた助言を返します。

    Raises:
        ValueError: 取得した降水確率が 0 以上 100 以下でない場合に送出します。
    """
    try:
        probability = source.precipitation_probability(city)
    except OSError:
        return "天気情報を取得できませんでした"
    if not 0 <= probability <= 100:
        raise ValueError(f"降水確率が不正です: {probability}")
    if probability >= 50:
        return "傘を持っていきましょう"
    if probability >= 30:
        return "折りたたみ傘があると安心です"
    return "傘は不要です"
