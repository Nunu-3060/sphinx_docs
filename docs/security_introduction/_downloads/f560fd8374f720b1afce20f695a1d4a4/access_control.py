"""アクセス制御の不備（IDOR）とその対策のサンプル.

URL などに含まれる ID だけでデータを返すと、ID を書き換えるだけで
他人のデータを取得できてしまいます。データを返す前に、
ログイン中のユーザーにそのデータへの権限があるかを確認します。

実行方法:
    python access_control.py

必要なライブラリ:
    なし（標準ライブラリのみ）
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Invoice:
    """請求書."""

    invoice_id: int
    owner: str
    amount: int


@dataclass(frozen=True)
class User:
    """ログイン中のユーザー."""

    name: str
    role: str  # "customer" または "admin"


INVOICES = {
    1001: Invoice(1001, "alice", 12000),
    1002: Invoice(1002, "bob", 98000),
}


def get_invoice_unsafe(user: User, invoice_id: int) -> Invoice:
    """ID だけで請求書を返す（悪い例）."""
    return INVOICES[invoice_id]


def get_invoice_safe(user: User, invoice_id: int) -> Invoice:
    """所有者または管理者だけに請求書を返す（良い例）.

    存在しない ID と権限のない ID で同じ例外を返し、
    他人のデータが存在するかどうかも分からないようにする。
    """
    invoice = INVOICES.get(invoice_id)
    if invoice is None or (invoice.owner != user.name
                           and user.role != "admin"):
        raise LookupError(f"請求書 {invoice_id} は見つかりません")
    return invoice


def main() -> None:
    alice = User("alice", "customer")
    admin = User("carol", "admin")

    print("[悪い例] alice が ID を 1002 に書き換えた場合")
    print(f"  {get_invoice_unsafe(alice, 1002)}")

    print("[良い例]")
    print(f"  alice が自分の請求書を参照: {get_invoice_safe(alice, 1001)}")
    try:
        get_invoice_safe(alice, 1002)
    except LookupError as error:
        print(f"  alice が他人の請求書を参照: 拒否（{error}）")
    print(f"  管理者が参照: {get_invoice_safe(admin, 1002)}")


if __name__ == "__main__":
    main()
