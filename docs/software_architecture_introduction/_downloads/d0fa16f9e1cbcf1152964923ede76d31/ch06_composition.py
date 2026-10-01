"""継承をコンポジションに置き換える例.

通知の送信を例にします。

* 悪い例: 「ログを残す」「再試行する」といった機能を継承で追加していくと、
  機能の組み合わせの数だけサブクラスが必要になります。
* 良い例: 送信先（Sender）と付加機能を別々の部品にし、組み合わせて使います。
  部品どうしは typing.Protocol で定めたインターフェースだけに依存します。

実行方法::

    python ch06_composition.py
"""

from typing import Protocol

# ---------------------------------------------------------------------------
# 悪い例: 継承で機能を追加する
# ---------------------------------------------------------------------------


class EmailNotifier:
    """メールで通知します."""

    def send(self, to: str, message: str) -> None:
        print(f"[email] to={to}: {message}")


class LoggingEmailNotifier(EmailNotifier):
    """ログを残してからメールで通知します."""

    def send(self, to: str, message: str) -> None:
        print(f"[log] send to {to}")
        super().send(to, message)


class SlackNotifier:
    """Slack で通知します."""

    def send(self, to: str, message: str) -> None:
        print(f"[slack] to={to}: {message}")


class LoggingSlackNotifier(SlackNotifier):
    """ログを残してから Slack で通知します.

    LoggingEmailNotifier とほぼ同じコードを、もう一度書くことになります。
    「再試行」を追加すると、さらに 2 つのクラスが必要になります。
    """

    def send(self, to: str, message: str) -> None:
        print(f"[log] send to {to}")
        super().send(to, message)


# ---------------------------------------------------------------------------
# 良い例: 部品を組み合わせる
# ---------------------------------------------------------------------------


class Sender(Protocol):
    """通知を送信する部品のインターフェースです."""

    def send(self, to: str, message: str) -> None:
        """to に message を送信します."""
        ...


class EmailSender:
    """メールで送信します."""

    def send(self, to: str, message: str) -> None:
        print(f"[email] to={to}: {message}")


class SlackSender:
    """Slack で送信します."""

    def send(self, to: str, message: str) -> None:
        print(f"[slack] to={to}: {message}")


class LoggingSender:
    """ログを残してから、内部に持つ Sender に送信を任せます."""

    def __init__(self, inner: Sender) -> None:
        self._inner = inner

    def send(self, to: str, message: str) -> None:
        print(f"[log] send to {to}")
        self._inner.send(to, message)


class RetryingSender:
    """送信に失敗したら、指定した回数まで再試行します."""

    def __init__(self, inner: Sender, max_attempts: int = 3) -> None:
        self._inner = inner
        self._max_attempts = max_attempts

    def send(self, to: str, message: str) -> None:
        for attempt in range(1, self._max_attempts + 1):
            try:
                self._inner.send(to, message)
                return
            except ConnectionError as error:
                print(f"[retry] attempt {attempt} failed: {error}")
        raise ConnectionError(f"failed after {self._max_attempts} attempts")


class FlakySender:
    """最初の数回だけ失敗する、動作確認用の Sender です."""

    def __init__(self, failures: int) -> None:
        self._failures = failures

    def send(self, to: str, message: str) -> None:
        if self._failures > 0:
            self._failures -= 1
            raise ConnectionError("network is unreachable")
        print(f"[flaky] to={to}: {message}")


class Notifier:
    """利用者向けの通知サービスです.

    どの Sender を使うかは知らず、渡された Sender に送信を任せます。
    """

    def __init__(self, sender: Sender) -> None:
        self._sender = sender

    def notify_shipped(self, user: str, order_id: str) -> None:
        """発送の通知を送信します."""
        self._sender.send(user, f"注文 {order_id} を発送しました。")


def main() -> None:
    """継承による実装と、部品の組み合わせによる実装を実行します."""
    print("--- 悪い例 ---")
    LoggingEmailNotifier().send("sato@example.com", "注文を発送しました。")
    LoggingSlackNotifier().send("#orders", "注文を発送しました。")

    print("--- 良い例 ---")
    Notifier(LoggingSender(EmailSender())).notify_shipped(
        "sato@example.com", "A-001")
    Notifier(LoggingSender(SlackSender())).notify_shipped("#orders", "A-002")
    # 再試行も、既存のクラスを変更せずに組み合わせで追加できる
    Notifier(RetryingSender(LoggingSender(FlakySender(failures=2)))
             ).notify_shipped("#orders", "A-003")


if __name__ == "__main__":
    main()
