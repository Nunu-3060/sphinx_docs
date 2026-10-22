"""第 6 章 ステップ 2: 弾を撃つ。"""

import pyxel

SCREEN_W = 128
SCREEN_H = 160

KEYS_LEFT = [pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
KEYS_RIGHT = [pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT]
KEYS_UP = [pyxel.KEY_UP, pyxel.KEY_W, pyxel.GAMEPAD1_BUTTON_DPAD_UP]
KEYS_DOWN = [pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN]
KEYS_SHOT = [pyxel.KEY_Z, pyxel.KEY_SPACE, pyxel.GAMEPAD1_BUTTON_A]


def pressed(keys: list[int]) -> bool:
    """keys のいずれかが押されていれば True を返す。"""
    return any(pyxel.btn(key) for key in keys)


class Entity:
    """画面上に存在する物体の基底クラス。

    (x, y) は左上の座標、(w, h) は大きさを表す。
    alive が False になった物体は、そのフレームの最後にリストから取り除かれる。
    """

    def __init__(self, x: float, y: float, w: int, h: int) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alive = True

    def is_outside(self) -> bool:
        return self.x + self.w < 0 or self.x > SCREEN_W or self.y + self.h < 0 or self.y > SCREEN_H


class PlayerBullet(Entity):
    SPEED = 5

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 8, 8)

    def update(self) -> None:
        self.y -= self.SPEED
        if self.is_outside():
            self.alive = False

    def draw(self) -> None:
        pyxel.rect(self.x + 3, self.y + 1, 2, 6, 10)


class Player(Entity):
    SPEED = 2
    SHOT_INTERVAL = 5

    def __init__(self) -> None:
        super().__init__(SCREEN_W / 2 - 8, SCREEN_H - 32, 16, 16)
        self.shot_timer = 0

    def update(self) -> list[PlayerBullet]:
        """入力に応じて移動し、新しく撃った弾のリストを返す。"""
        dx = int(pressed(KEYS_RIGHT)) - int(pressed(KEYS_LEFT))
        dy = int(pressed(KEYS_DOWN)) - int(pressed(KEYS_UP))
        speed = self.SPEED * (0.7071 if dx != 0 and dy != 0 else 1)
        self.x = pyxel.clamp(self.x + dx * speed, 0, SCREEN_W - self.w)
        self.y = pyxel.clamp(self.y + dy * speed, 0, SCREEN_H - self.h)

        # 連射の間隔を空けるため、撃ったあとは shot_timer が 0 になるまで撃てない
        if self.shot_timer > 0:
            self.shot_timer -= 1
        if pressed(KEYS_SHOT) and self.shot_timer == 0:
            self.shot_timer = self.SHOT_INTERVAL
            return [PlayerBullet(self.x + 4, self.y - 4)]
        return []

    def draw(self) -> None:
        pyxel.tri(self.x + 7, self.y, self.x, self.y + 15, self.x + 15, self.y + 15, 6)


class App:
    def __init__(self) -> None:
        self.player = Player()
        self.player_bullets: list[PlayerBullet] = []

    def update(self) -> None:
        self.player_bullets += self.player.update()
        for bullet in self.player_bullets:
            bullet.update()
        # 消えた弾をリストから取り除く
        self.player_bullets = [b for b in self.player_bullets if b.alive]

    def draw(self) -> None:
        pyxel.cls(0)
        for bullet in self.player_bullets:
            bullet.draw()
        self.player.draw()
        pyxel.text(2, 2, f"BULLETS {len(self.player_bullets)}", 7)


def main() -> None:
    pyxel.init(SCREEN_W, SCREEN_H, title="COSMO RUSH - step2")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
