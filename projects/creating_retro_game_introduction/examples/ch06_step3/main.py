"""第 6 章 ステップ 3: 敵を出現させ、弾との当たり判定を行う。"""

import pyxel

SCREEN_W = 128
SCREEN_H = 160
SPAWN_INTERVAL = 20

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
    当たり判定には、周囲から margin だけ内側に縮めた矩形を使う。
    """

    def __init__(self, x: float, y: float, w: int, h: int, margin: int = 0) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.margin = margin
        self.alive = True

    def center(self) -> tuple[float, float]:
        return self.x + self.w / 2, self.y + self.h / 2

    def hitbox(self) -> tuple[float, float, float, float]:
        m = self.margin
        return self.x + m, self.y + m, self.w - m * 2, self.h - m * 2

    def is_outside(self) -> bool:
        return self.x + self.w < 0 or self.x > SCREEN_W or self.y + self.h < 0 or self.y > SCREEN_H


def overlaps(a: Entity, b: Entity) -> bool:
    """2 つの物体の当たり判定の矩形が重なっていれば True を返す (AABB 判定)。"""
    ax, ay, aw, ah = a.hitbox()
    bx, by, bw, bh = b.hitbox()
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


class PlayerBullet(Entity):
    SPEED = 5

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 8, 8, margin=2)

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
        super().__init__(SCREEN_W / 2 - 8, SCREEN_H - 32, 16, 16, margin=5)
        self.shot_timer = 0

    def update(self) -> list[PlayerBullet]:
        """入力に応じて移動し、新しく撃った弾のリストを返す。"""
        dx = int(pressed(KEYS_RIGHT)) - int(pressed(KEYS_LEFT))
        dy = int(pressed(KEYS_DOWN)) - int(pressed(KEYS_UP))
        speed = self.SPEED * (0.7071 if dx != 0 and dy != 0 else 1)
        self.x = pyxel.clamp(self.x + dx * speed, 0, SCREEN_W - self.w)
        self.y = pyxel.clamp(self.y + dy * speed, 0, SCREEN_H - self.h)

        if self.shot_timer > 0:
            self.shot_timer -= 1
        if pressed(KEYS_SHOT) and self.shot_timer == 0:
            self.shot_timer = self.SHOT_INTERVAL
            return [PlayerBullet(self.x + 4, self.y - 4)]
        return []

    def draw(self) -> None:
        pyxel.tri(self.x + 7, self.y, self.x, self.y + 15, self.x + 15, self.y + 15, 6)


class Enemy(Entity):
    """まっすぐ下へ進む敵。"""

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 16, 16, margin=2)

    def update(self) -> None:
        self.y += 1.5
        if self.y > SCREEN_H:
            self.alive = False

    def draw(self) -> None:
        pyxel.circ(self.x + 7, self.y + 7, 6, 8)


class App:
    def __init__(self) -> None:
        self.player = Player()
        self.player_bullets: list[PlayerBullet] = []
        self.enemies: list[Enemy] = []

    def update(self) -> None:
        self.player_bullets += self.player.update()
        # 一定間隔で、画面の上端のランダムな位置に敵を出す
        if pyxel.frame_count % SPAWN_INTERVAL == 0:
            self.enemies.append(Enemy(pyxel.rndi(0, SCREEN_W - 16), -16))
        for enemy in self.enemies:
            enemy.update()
        for bullet in self.player_bullets:
            bullet.update()

        self.check_collisions()

        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemies = [e for e in self.enemies if e.alive]

    def check_collisions(self) -> None:
        for bullet in self.player_bullets:
            for enemy in self.enemies:
                if enemy.alive and overlaps(bullet, enemy):
                    bullet.alive = False
                    enemy.alive = False
                    break

    def draw(self) -> None:
        pyxel.cls(0)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.player_bullets:
            bullet.draw()
        self.player.draw()


def main() -> None:
    pyxel.init(SCREEN_W, SCREEN_H, title="COSMO RUSH - step3")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
