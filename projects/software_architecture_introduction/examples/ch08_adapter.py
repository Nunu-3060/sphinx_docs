"""Adapter パターンの例.

アプリケーションが期待するインターフェース（TemperatureSource）と、
外部のライブラリが提供するインターフェース（LegacyThermometer）が
異なる場合に、変換を受け持つクラス（Adapter）を間に挟みます。

実行方法::

    python ch08_adapter.py
"""

from typing import Protocol


class TemperatureSource(Protocol):
    """アプリケーションが期待する、気温の取得のインターフェースです."""

    def celsius(self) -> float:
        """摂氏の気温を返します."""
        ...


class LegacyThermometer:
    """外部のライブラリのクラスとします（変更できない）.

    華氏の気温を、10 倍した整数で返します。
    """

    def read_fahrenheit_x10(self) -> int:
        return 770  # 77.0 °F


class LegacyThermometerAdapter:
    """LegacyThermometer を TemperatureSource として使えるようにします."""

    def __init__(self, thermometer: LegacyThermometer) -> None:
        self._thermometer = thermometer

    def celsius(self) -> float:
        fahrenheit = self._thermometer.read_fahrenheit_x10() / 10
        return (fahrenheit - 32) * 5 / 9


def describe(source: TemperatureSource) -> str:
    """気温の説明を返します. 取得元の種類は知りません."""
    value = source.celsius()
    feeling = "暑い" if value >= 25 else "過ごしやすい"
    return f"{value:.1f} °C（{feeling}）"


def main() -> None:
    """外部のクラスを、Adapter を通して使います."""
    print(describe(LegacyThermometerAdapter(LegacyThermometer())))


if __name__ == "__main__":
    main()
