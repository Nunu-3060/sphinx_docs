"""為替レートを Web API から取得する."""

import httpx


class ExchangeRateError(Exception):
    """為替レートを取得できなかったときに送出する例外."""


class ExchangeClient:
    """為替レートの API のクライアント.

    API は GET /rates?base=USD&target=JPY に対して
    {"base": "USD", "target": "JPY", "rate": 150.5} の形の JSON を返すものとする。
    """

    def __init__(self, client: httpx.Client) -> None:
        self._client = client

    def rate(self, base: str, target: str) -> float:
        """base 通貨 1 単位が target 通貨でいくらになるかを返す.

        Raises:
            ExchangeRateError: API がエラーを返した場合。
        """
        try:
            response = self._client.get(
                "/rates", params={"base": base, "target": target})
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise ExchangeRateError(f"{base}/{target} を取得できません") from e
        return float(response.json()["rate"])

    def convert(self, amount: float, base: str, target: str) -> float:
        """金額を換算し、小数第 2 位に丸めて返す."""
        return round(amount * self.rate(base, target), 2)
