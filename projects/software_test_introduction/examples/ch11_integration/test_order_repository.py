"""SQLite のインメモリデータベースを使って OrderRepository をテストする."""

import sqlite3
from collections.abc import Iterator

import pytest

from order_repository import OrderRepository


@pytest.fixture
def repo() -> Iterator[OrderRepository]:
    """テストごとに空のデータベースを用意し、終わったら閉じる."""
    conn = sqlite3.connect(":memory:")
    repository = OrderRepository(conn)
    repository.create_table()
    yield repository  # ここでテストが実行される
    conn.close()      # 後始末


def test_total_by_customer(repo: OrderRepository) -> None:
    repo.add(1, "佐藤", 1200)
    repo.add(2, "鈴木", 800)
    repo.add(3, "佐藤", 300)
    assert repo.total_by_customer() == {"佐藤": 1500, "鈴木": 800}


def test_empty_table(repo: OrderRepository) -> None:
    assert repo.total_by_customer() == {}


def test_duplicate_id_is_rejected(repo: OrderRepository) -> None:
    repo.add(1, "佐藤", 1200)
    with pytest.raises(sqlite3.IntegrityError):
        repo.add(1, "鈴木", 800)
    # 失敗した INSERT はロールバックされ、最初の注文だけが残る
    assert repo.total_by_customer() == {"佐藤": 1200}


def test_negative_amount_is_rejected(repo: OrderRepository) -> None:
    with pytest.raises(sqlite3.IntegrityError):
        repo.add(1, "佐藤", -100)
