"""注文の発送を顧客にメールで知らせる."""

from typing import Protocol


class CustomerDirectory(Protocol):
    """顧客情報を調べる機能."""

    def email_of(self, customer_id: int) -> str | None:
        """顧客のメールアドレスを返す（登録がなければ None を返す）."""
        ...


class MailSender(Protocol):
    """メールを送信する機能."""

    def send(self, to: str, subject: str, body: str) -> None:
        """メールを送信する（失敗したら OSError を送出する）."""
        ...


class OrderNotifier:
    """発送の通知を担当するクラス."""

    def __init__(self, directory: CustomerDirectory,
                 sender: MailSender) -> None:
        self._directory = directory
        self._sender = sender

    def notify_shipped(self, customer_id: int, order_id: int) -> bool:
        """発送の通知メールを送る.

        Returns:
            送信できたら True、メールアドレスが未登録か送信に失敗したら False。
        """
        email = self._directory.email_of(customer_id)
        if email is None:
            return False
        subject = f"ご注文（注文番号 {order_id}）を発送しました"
        body = "商品の到着まで今しばらくお待ちください。"
        try:
            self._sender.send(email, subject, body)
        except OSError:
            return False
        return True
