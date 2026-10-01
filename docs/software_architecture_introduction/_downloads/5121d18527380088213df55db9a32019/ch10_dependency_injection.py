"""依存性注入（DI）の例.

天気の情報から、朝の案内の文章を作るサービスを例にします。

* 悪い例: サービスの内部で HTTP 通信と現在時刻の取得を直接行う
* 良い例: 天気の取得元と時計をコンストラクターで受け取る

良い例では、オブジェクトの組み立てを build_service 関数（コンポジション
ルート）の 1 か所にまとめます。設定値は環境変数から読み込み、Settings
クラスにまとめて渡します。

実行方法::

    python ch10_dependency_injection.py

環境変数 WEATHER_API_URL を設定しない場合は、ネットワークに接続せず、
固定の天気を返す取得元を使います。
"""

import json
import os
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol

# ---------------------------------------------------------------------------
# 悪い例: 依存するものを内部で直接作る
# ---------------------------------------------------------------------------


class BadMorningGreeter:
    """朝の案内を作ります（悪い例）.

    通信先の URL と現在時刻が内部で決まるので、テストのたびに実際に
    通信が発生し、結果も実行した時刻によって変わります。
    """

    def message(self) -> str:
        with urllib.request.urlopen("https://example.com/weather") as res:
            weather = json.load(res)["weather"]
        hour = datetime.now().hour
        greeting = "おはようございます" if hour < 12 else "こんにちは"
        return f"{greeting}。今日の天気は「{weather}」です。"


# ---------------------------------------------------------------------------
# 良い例: 依存するものを外から受け取る
# ---------------------------------------------------------------------------


class WeatherClient(Protocol):
    """天気の取得元のインターフェースです."""

    def today(self) -> str:
        """今日の天気を返します."""
        ...


Clock = Callable[[], datetime]


class MorningGreeter:
    """朝の案内を作ります（良い例）."""

    def __init__(self, weather: WeatherClient, clock: Clock) -> None:
        self._weather = weather
        self._clock = clock

    def message(self) -> str:
        hour = self._clock().hour
        greeting = "おはようございます" if hour < 12 else "こんにちは"
        return f"{greeting}。今日の天気は「{self._weather.today()}」です。"


class HttpWeatherClient:
    """Web API から天気を取得します."""

    def __init__(self, url: str, timeout: float) -> None:
        self._url = url
        self._timeout = timeout

    def today(self) -> str:
        with urllib.request.urlopen(self._url, timeout=self._timeout) as res:
            return str(json.load(res)["weather"])


class FixedWeatherClient:
    """常に同じ天気を返します（開発用、テスト用）."""

    def __init__(self, weather: str) -> None:
        self._weather = weather

    def today(self) -> str:
        return self._weather


@dataclass(frozen=True)
class Settings:
    """アプリケーションの設定です."""

    weather_api_url: str | None
    timeout: float

    @classmethod
    def from_env(cls) -> "Settings":
        """環境変数から設定を読み込みます."""
        return cls(
            weather_api_url=os.environ.get("WEATHER_API_URL"),
            timeout=float(os.environ.get("WEATHER_API_TIMEOUT", "5")),
        )


def build_service(settings: Settings) -> MorningGreeter:
    """設定に従ってオブジェクトを組み立てます（コンポジションルート）."""
    weather: WeatherClient
    if settings.weather_api_url:
        weather = HttpWeatherClient(settings.weather_api_url,
                                    settings.timeout)
    else:
        weather = FixedWeatherClient("晴れ")
    return MorningGreeter(weather, datetime.now)


def main() -> None:
    """組み立てたサービスと、時計を固定したサービスを実行します."""
    print(build_service(Settings.from_env()).message())

    # テストでは、取得元と時計を固定した値に差し替えられる
    fixed = MorningGreeter(FixedWeatherClient("雨"),
                           lambda: datetime(2026, 4, 1, 15, 0))
    print(fixed.message())


if __name__ == "__main__":
    main()
