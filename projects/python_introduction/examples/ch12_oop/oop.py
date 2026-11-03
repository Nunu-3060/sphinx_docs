"""クラスと継承の基本的な使い方を示すサンプル。"""


class BankAccount:
    """銀行口座を表すクラス。"""

    def __init__(self, owner: str, balance: int = 0) -> None:
        """口座の名義人と残高を初期化する。"""
        self.owner: str = owner
        self.balance: int = balance

    def deposit(self, amount: int) -> None:
        """口座に指定した金額を入金する。"""
        self.balance += amount

    def withdraw(self, amount: int) -> None:
        """口座から指定した金額を出金する。残高が不足している場合は出金しない。"""
        if amount > self.balance:
            print("残高が不足しているため、出金できません。")
            return
        self.balance -= amount

    def __str__(self) -> str:
        """口座の情報を文字列として返す。"""
        return f"{self.owner} の口座残高: {self.balance} 円"


class SavingsAccount(BankAccount):
    """BankAccount を継承し、利息を計算する機能を追加した貯蓄口座のクラス。"""

    def __init__(self, owner: str, balance: int = 0, interest_rate: float = 0.01) -> None:
        """口座の名義人、残高、利率を初期化する。"""
        super().__init__(owner, balance)
        self.interest_rate: float = interest_rate

    def add_interest(self) -> None:
        """利率に応じた利息を残高に追加する。"""
        self.balance += int(self.balance * self.interest_rate)


def main() -> None:
    """口座クラスの使用例を表示する。"""
    account: BankAccount = BankAccount("伊藤", 1000)
    account.deposit(500)
    account.withdraw(200)
    print(account)

    savings: SavingsAccount = SavingsAccount("渡辺", 10000, 0.05)
    savings.add_interest()
    print(savings)


if __name__ == "__main__":
    main()
