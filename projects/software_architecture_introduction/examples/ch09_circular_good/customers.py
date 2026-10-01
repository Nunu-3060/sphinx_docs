"""顧客を表すモジュール. ほかのモジュールに依存しません."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Customer:
    """顧客です. 注文の一覧は持ちません."""

    customer_id: str
    name: str
