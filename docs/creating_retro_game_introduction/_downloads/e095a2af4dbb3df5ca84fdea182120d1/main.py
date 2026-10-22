"""第 6 章 ステップ 1: 自機を表示して動かす。"""

import pyxel

SCREEN_W = 128
SCREEN_H = 160

KEYS_LEFT = [pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
KEYS_RIGHT = [pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT]
KEYS_UP = [pyxel.KEY_UP, pyxel.KEY_W, pyxel.GAMEPAD1_BUTTON_DPAD_UP]
KEYS_DOWN = [pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN]


def pressed(keys: list[int]) -> bool:
    """keys のいずれかが押されていれば True を返す。"""
    return any(pyxel.btn(key) for key in keys)


class Player:
    SPEED = 2

    def __init__(self) -> None:
        self.w = 16
        self.h = 16
        self.x: float = SCREEN_W / 2 - self.w / 2
        self.y: float = SCREEN_H - 32

    def update(self) -> None:
        # 右が押されていれば +1、左が押されていれば -1 (両方なら 0)
        dx = int(pressed(KEYS_RIGHT)) - int(pressed(KEYS_LEFT))
        dy = int(pressed(KEYS_DOWN)) - int(pressed(KEYS_UP))
        # 斜め移動が速くなりすぎないように、速さを 1/√2 倍にする
        speed = self.SPEED * (0.7071 if dx != 0 and dy != 0 else 1)
        # 画面の外に出ないように位置を制限する
        self.x = pyxel.clamp(self.x + dx * speed, 0, SCREEN_W - self.w)
        self.y = pyxel.clamp(self.y + dy * speed, 0, SCREEN_H - self.h)

    def draw(self) -> None:
        # 仮の見た目として三角形を描く
        pyxel.tri(self.x + 7, self.y, self.x, self.y + 15, self.x + 15, self.y + 15, 6)


class App:
    def __init__(self) -> None:
        self.player = Player()

    def update(self) -> None:
        self.player.update()

    def draw(self) -> None:
        pyxel.cls(0)
        self.player.draw()


def main() -> None:
    pyxel.init(SCREEN_W, SCREEN_H, title="COSMO RUSH - step1")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
