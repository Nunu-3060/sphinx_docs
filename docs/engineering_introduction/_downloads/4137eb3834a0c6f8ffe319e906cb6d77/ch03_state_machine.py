"""第 3 章: 状態機械で電気ポットの制御をモデル化する。

電気ポットの制御を、状態 (待機・加熱・保温・異常) と、状態を変える
きっかけとなるイベントの組で表します。状態とイベントの組から次の
状態を決める表 (状態遷移表) を使うと、

* 想定していないイベントを確実に検出できる
* 「異常」からはリセット以外で抜けられない、といった性質を
  機械的に確かめられる

ことを示します。

実行例::

    python ch03_state_machine.py
"""

from __future__ import annotations

from enum import Enum


class State(Enum):
    """電気ポットの状態。"""

    IDLE = "待機"
    HEATING = "加熱"
    KEEP_WARM = "保温"
    ERROR = "異常"


class Event(Enum):
    """状態を変えるきっかけとなるイベント。"""

    START = "沸騰ボタン"
    BOILED = "沸騰を検出"
    COOLED = "設定温度を下回った"
    DRY = "空だきを検出"
    SENSOR_FAULT = "センサーの異常"
    RESET = "リセット"


# 状態遷移表: (現在の状態, イベント) -> 次の状態
TRANSITIONS: dict[tuple[State, Event], State] = {
    (State.IDLE, Event.START): State.HEATING,
    (State.HEATING, Event.BOILED): State.KEEP_WARM,
    (State.KEEP_WARM, Event.COOLED): State.HEATING,
    (State.KEEP_WARM, Event.START): State.HEATING,
    (State.ERROR, Event.RESET): State.IDLE,
}

# どの状態でも、安全に関わるイベントでは異常に移る
for _state in (State.IDLE, State.HEATING, State.KEEP_WARM):
    TRANSITIONS[(_state, Event.DRY)] = State.ERROR
    TRANSITIONS[(_state, Event.SENSOR_FAULT)] = State.ERROR


class InvalidTransition(Exception):
    """状態遷移表にないイベントを受け取ったときに送出する例外。"""


class KettleController:
    """状態遷移表に従って動く電気ポットのコントローラー。"""

    def __init__(self) -> None:
        self.state = State.IDLE

    def handle(self, event: Event) -> State:
        """イベントを処理し、遷移後の状態を返す。"""
        key = (self.state, event)
        if key not in TRANSITIONS:
            raise InvalidTransition(
                f"状態「{self.state.value}」では"
                f"イベント「{event.value}」を受け付けません")
        self.state = TRANSITIONS[key]
        return self.state

    def heater_on(self) -> bool:
        """ヒーターに通電するかどうかを返す (加熱中だけ通電する)。"""
        return self.state is State.HEATING


def check_properties() -> None:
    """状態遷移表が満たすべき性質を確かめる。"""
    # 異常状態から抜け出せるのはリセットだけ
    exits = [event for (state, event) in TRANSITIONS
             if state is State.ERROR]
    assert exits == [Event.RESET], exits
    # 空だきを検出したら、どの状態からでも異常に移る
    for state in State:
        if state is not State.ERROR:
            assert TRANSITIONS[(state, Event.DRY)] is State.ERROR
    print("状態遷移表の性質を確認しました。")


def main() -> None:
    check_properties()
    controller = KettleController()
    scenario = [Event.START, Event.BOILED, Event.COOLED, Event.BOILED,
                Event.DRY, Event.START, Event.RESET]
    for event in scenario:
        before = controller.state
        try:
            after = controller.handle(event)
        except InvalidTransition as error:
            print(f"拒否: {error}")
            continue
        heater = "ON" if controller.heater_on() else "OFF"
        print(f"{before.value:3s} --[{event.value}]--> {after.value:3s}"
              f"  ヒーター {heater}")


if __name__ == "__main__":
    main()
