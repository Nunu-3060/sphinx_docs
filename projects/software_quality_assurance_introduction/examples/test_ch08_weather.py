"""ch08_weather.py のテストです。

スタブ（決まった値を返す偽物）とモック（呼び出され方を検証する偽物）の
両方の使い方を示します。
"""

from unittest.mock import Mock

import pytest

from ch08_weather import HttpWeatherSource, umbrella_advice


class StubWeatherSource:
    """決まった降水確率を返すスタブです。"""

    def __init__(self, probability: int) -> None:
        self._probability = probability

    def precipitation_probability(self, city: str) -> int:
        return self._probability


@pytest.mark.parametrize(
    ("probability", "expected"),
    [
        (0, "傘は不要です"),
        (29, "傘は不要です"),
        (30, "折りたたみ傘があると安心です"),
        (49, "折りたたみ傘があると安心です"),
        (50, "傘を持っていきましょう"),
        (100, "傘を持っていきましょう"),
    ],
)
def test_advice_by_probability(probability: int, expected: str) -> None:
    source = StubWeatherSource(probability)
    assert umbrella_advice(source, "東京") == expected


@pytest.mark.parametrize("probability", [-1, 101])
def test_invalid_probability_raises(probability: int) -> None:
    with pytest.raises(ValueError):
        umbrella_advice(StubWeatherSource(probability), "東京")


def test_source_is_called_with_city() -> None:
    source = Mock()
    source.precipitation_probability.return_value = 10
    umbrella_advice(source, "大阪")
    source.precipitation_probability.assert_called_once_with("大阪")


def test_network_error_returns_message() -> None:
    source = Mock()
    source.precipitation_probability.side_effect = OSError("接続できません")
    assert umbrella_advice(source, "札幌") == "天気情報を取得できませんでした"


def test_http_source_rejects_plain_http() -> None:
    with pytest.raises(ValueError):
        HttpWeatherSource("http://example.com/api")
