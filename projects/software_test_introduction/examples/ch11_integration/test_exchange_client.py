"""httpx.MockTransport で API の応答を差し替えて ExchangeClient をテストする."""

from collections.abc import Iterator

import httpx
import pytest

from exchange_client import ExchangeClient, ExchangeRateError


def fake_api(request: httpx.Request) -> httpx.Response:
    """本物の API の代わりに応答を返す関数."""
    if request.url.path != "/rates":
        return httpx.Response(404)
    base = request.url.params["base"]
    target = request.url.params["target"]
    if (base, target) == ("USD", "JPY"):
        return httpx.Response(
            200, json={"base": base, "target": target, "rate": 150.5})
    return httpx.Response(400, json={"error": "unsupported currency"})


@pytest.fixture
def client() -> Iterator[ExchangeClient]:
    """ネットワークに接続しないクライアント."""
    http = httpx.Client(transport=httpx.MockTransport(fake_api),
                        base_url="https://api.example.com")
    yield ExchangeClient(http)
    http.close()


def test_rate(client: ExchangeClient) -> None:
    assert client.rate("USD", "JPY") == 150.5


def test_convert(client: ExchangeClient) -> None:
    assert client.convert(12.34, "USD", "JPY") == 1857.17


def test_error_response_raises(client: ExchangeClient) -> None:
    with pytest.raises(ExchangeRateError):
        client.rate("USD", "XXX")


def test_request_parameters() -> None:
    # 送信されたリクエストを記録して、パラメーターを検証する
    requests: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"rate": 0.0067})

    with httpx.Client(transport=httpx.MockTransport(handler),
                      base_url="https://api.example.com") as http:
        ExchangeClient(http).rate("JPY", "USD")

    assert len(requests) == 1
    assert requests[0].url.params["base"] == "JPY"
    assert requests[0].url.params["target"] == "USD"
