"""依存性逆転の原則（DIP）の例.

悪い例では、上位の方針（パスワードの再設定の手順）が、下位の詳細
（SMTP によるメール送信）を直接生成して使っています。メールの送信方法を
変えるたびに上位のクラスを変更する必要があり、テストでも本物のメールが
送られてしまいます。

良い例では、上位のクラスが必要とするインターフェース（MessageSender）を
上位の側で定め、下位のクラスはそれを実装します。依存の矢印が
「上位 → 下位」から「下位 → 抽象 ← 上位」に逆転します。

実行方法::

    python ch07_dip.py
"""

from typing import Protocol

# ---------------------------------------------------------------------------
# 悪い例: 上位のクラスが下位の具体的なクラスに依存する
# ---------------------------------------------------------------------------


class SmtpMailer:
    """SMTP でメールを送信します（ここでは表示するだけ）."""

    def send_mail(self, address: str, subject: str, body: str) -> None:
        print(f"[smtp] {address} / {subject} / {body}")


class BadPasswordReset:
    """パスワードの再設定（悪い例）."""

    def __init__(self) -> None:
        self._mailer = SmtpMailer()  # 具体的なクラスを直接生成している

    def request(self, address: str) -> None:
        token = "abc123"
        self._mailer.send_mail(address, "パスワードの再設定",
                               f"確認コード: {token}")


# ---------------------------------------------------------------------------
# 良い例: 上位のクラスが定めた抽象に、下位のクラスが従う
# ---------------------------------------------------------------------------


class MessageSender(Protocol):
    """パスワードの再設定が必要とする、メッセージ送信の抽象です."""

    def send(self, to: str, title: str, body: str) -> None:
        ...


class PasswordReset:
    """パスワードの再設定（良い例）. 抽象だけに依存します."""

    def __init__(self, sender: MessageSender) -> None:
        self._sender = sender

    def request(self, address: str) -> None:
        token = "abc123"
        self._sender.send(address, "パスワードの再設定",
                          f"確認コード: {token}")


class SmtpSender:
    """SMTP による MessageSender の実装です（ここでは表示するだけ）."""

    def send(self, to: str, title: str, body: str) -> None:
        print(f"[smtp] {to} / {title} / {body}")


class RecordingSender:
    """送信内容を記録するだけの MessageSender です（テスト用）."""

    def __init__(self) -> None:
        self.sent: list[tuple[str, str, str]] = []

    def send(self, to: str, title: str, body: str) -> None:
        self.sent.append((to, title, body))


def main() -> None:
    """本番用とテスト用の MessageSender を差し替えて使います."""
    BadPasswordReset().request("sato@example.com")

    PasswordReset(SmtpSender()).request("sato@example.com")

    recorder = RecordingSender()
    PasswordReset(recorder).request("sato@example.com")
    print("記録された送信内容:", recorder.sent)


if __name__ == "__main__":
    main()
