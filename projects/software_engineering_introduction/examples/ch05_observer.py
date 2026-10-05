"""Observer パターンの例（第 5 章）.

温度センサー（Subject）の値が変わると、登録された観察者（Observer）に
自動的に通知する。センサーは観察者の具体的な型を知らないため、
表示や警告などの処理を自由に追加・削除できる。
"""

from collections.abc import Callable

Observer = Callable[[float], None]


class TemperatureSensor:
    """温度を保持し、変化を観察者に通知する."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._celsius = 0.0

    def subscribe(self, observer: Observer) -> None:
        """観察者を登録する."""
        self._observers.append(observer)

    def unsubscribe(self, observer: Observer) -> None:
        """観察者の登録を解除する."""
        self._observers.remove(observer)

    def update(self, celsius: float) -> None:
        """温度を更新し、すべての観察者に通知する."""
        self._celsius = celsius
        for observer in self._observers:
            observer(celsius)


def display(celsius: float) -> None:
    """現在の温度を表示する観察者."""
    print(f"現在の温度: {celsius:.1f} ℃")


def alert(celsius: float) -> None:
    """高温時に警告する観察者."""
    if celsius >= 30.0:
        print("警告: 高温である")


if __name__ == "__main__":
    sensor = TemperatureSensor()
    sensor.subscribe(display)
    sensor.subscribe(alert)
    sensor.update(25.0)
    sensor.update(31.5)
