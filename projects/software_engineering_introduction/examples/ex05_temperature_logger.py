"""演習問題 5-2 の解答例: 温度の履歴を記録する観察者の追加（第 5 章）.

観察者は「温度を 1 つ受け取る呼び出し可能なもの」であればよいため、
状態（履歴）を持つ観察者はクラスのメソッドとして実装できる。
``TemperatureSensor`` は変更していない。
"""

from ch05_observer import TemperatureSensor, display


class TemperatureLogger:
    """受け取った温度を履歴として記録する."""

    def __init__(self) -> None:
        self.history: list[float] = []

    def record(self, celsius: float) -> None:
        """温度を履歴に追加する."""
        self.history.append(celsius)

    def average(self) -> float:
        """記録した温度の平均を返す。記録がなければ 0.0 を返す."""
        if not self.history:
            return 0.0
        return sum(self.history) / len(self.history)


if __name__ == "__main__":
    sensor = TemperatureSensor()
    logger = TemperatureLogger()
    sensor.subscribe(display)
    sensor.subscribe(logger.record)
    for value in (22.0, 25.5, 27.0):
        sensor.update(value)
    print(f"履歴: {logger.history}")
    print(f"平均: {logger.average():.1f} ℃")
