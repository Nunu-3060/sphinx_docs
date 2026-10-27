"""ゲーム画面の状態遷移を表す有限状態機械のサンプル。

タイトル → プレイ → ポーズ → ゲームオーバー → タイトル という画面の流れを、
「状態」と「イベント」と「遷移表」で表す。遷移表に無い組み合わせのイベントは無視する。

実行例:
    python state_machine.py
"""

from __future__ import annotations

from enum import Enum, auto


class Scene(Enum):
    """ゲーム画面（状態）。"""

    TITLE = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class Event(Enum):
    """状態を変えるきっかけ（イベント）。"""

    START = auto()
    PAUSE = auto()
    RESUME = auto()
    PLAYER_DIED = auto()
    CONFIRM = auto()


# (現在の状態, イベント) → 次の状態
TRANSITIONS: dict[tuple[Scene, Event], Scene] = {
    (Scene.TITLE, Event.START): Scene.PLAYING,
    (Scene.PLAYING, Event.PAUSE): Scene.PAUSED,
    (Scene.PAUSED, Event.RESUME): Scene.PLAYING,
    (Scene.PLAYING, Event.PLAYER_DIED): Scene.GAME_OVER,
    (Scene.GAME_OVER, Event.CONFIRM): Scene.TITLE,
}


class SceneMachine:
    """遷移表に従って現在の画面を切り替える。"""

    def __init__(self, initial: Scene = Scene.TITLE) -> None:
        self.current = initial

    def handle(self, event: Event) -> bool:
        """イベントを処理する。状態が変わったら True を返す。"""
        next_scene = TRANSITIONS.get((self.current, event))
        if next_scene is None:
            return False
        self.current = next_scene
        return True


def main() -> None:
    machine = SceneMachine()
    # プレイ中でないのに PLAYER_DIED が届く、といった不正なイベントも混ぜておく。
    events = [
        Event.PLAYER_DIED,
        Event.START,
        Event.PAUSE,
        Event.PLAYER_DIED,
        Event.RESUME,
        Event.PLAYER_DIED,
        Event.CONFIRM,
    ]
    print(f"開始: {machine.current.name}")
    for event in events:
        before = machine.current
        changed = machine.handle(event)
        result = f"{before.name} -> {machine.current.name}" if changed else f"{before.name} のまま（無視）"
        print(f"{event.name:12s}: {result}")


if __name__ == "__main__":
    main()
