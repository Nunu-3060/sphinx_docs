"""テストダブルを使って OrderNotifier をテストする."""

from unittest.mock import Mock

from order_notifier import CustomerDirectory, MailSender, OrderNotifier


# ---- ダミー: 引数を埋めるためだけに渡し、使われないことを前提とする ----
class DummySender:
    def send(self, to: str, subject: str, body: str) -> None:
        raise AssertionError("このテストでは呼ばれないはず")


# ---- スタブ: 決まった値を返して、テスト対象への入力を制御する ----
class StubDirectory:
    def __init__(self, email: str | None) -> None:
        self._email = email

    def email_of(self, customer_id: int) -> str | None:
        return self._email


# ---- スパイ: 呼び出しを記録して、テスト対象からの出力を検証する ----
class SpySender:
    def __init__(self) -> None:
        self.sent: list[tuple[str, str, str]] = []

    def send(self, to: str, subject: str, body: str) -> None:
        self.sent.append((to, subject, body))


# ---- フェイク: 本物と同じように動く簡易な実装 ----
class InMemoryDirectory:
    def __init__(self) -> None:
        self._emails: dict[int, str] = {}

    def register(self, customer_id: int, email: str) -> None:
        self._emails[customer_id] = email

    def email_of(self, customer_id: int) -> str | None:
        return self._emails.get(customer_id)


def test_unregistered_customer_is_not_notified() -> None:
    notifier = OrderNotifier(StubDirectory(None), DummySender())
    assert notifier.notify_shipped(customer_id=1, order_id=100) is False


def test_mail_is_sent_to_registered_address() -> None:
    spy = SpySender()
    notifier = OrderNotifier(StubDirectory("sato@example.com"), spy)

    assert notifier.notify_shipped(customer_id=1, order_id=100) is True
    assert len(spy.sent) == 1
    to, subject, _ = spy.sent[0]
    assert to == "sato@example.com"
    assert "100" in subject


def test_with_fake_directory() -> None:
    directory = InMemoryDirectory()
    directory.register(1, "sato@example.com")
    spy = SpySender()
    notifier = OrderNotifier(directory, spy)

    assert notifier.notify_shipped(customer_id=1, order_id=100) is True
    assert notifier.notify_shipped(customer_id=2, order_id=101) is False
    assert [to for to, _, _ in spy.sent] == ["sato@example.com"]


def test_with_mock() -> None:
    # spec を指定すると、MailSender にない属性を使ったときにエラーになる
    sender = Mock(spec=MailSender)
    directory = Mock(spec=CustomerDirectory)
    directory.email_of.return_value = "sato@example.com"
    notifier = OrderNotifier(directory, sender)

    notifier.notify_shipped(customer_id=1, order_id=100)

    directory.email_of.assert_called_once_with(1)
    sender.send.assert_called_once_with(
        "sato@example.com",
        "ご注文（注文番号 100）を発送しました",
        "商品の到着まで今しばらくお待ちください。",
    )


def test_send_failure_returns_false() -> None:
    # side_effect に例外を指定すると、呼び出したときにその例外を送出する
    sender = Mock(spec=MailSender)
    sender.send.side_effect = ConnectionError("接続できません")
    notifier = OrderNotifier(StubDirectory("sato@example.com"), sender)

    assert notifier.notify_shipped(customer_id=1, order_id=100) is False
