"""第 7 章 ステップ 5: シーン (タイトル、プレイ、ゲームオーバー) の切り替え。"""

import pyxel

SCREEN_W = 128
SCREEN_H = 160
SPAWN_INTERVAL = 20
GAME_OVER_DELAY = 60

KEYS_LEFT = [pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT]
KEYS_RIGHT = [pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT]
KEYS_UP = [pyxel.KEY_UP, pyxel.KEY_W, pyxel.GAMEPAD1_BUTTON_DPAD_UP]
KEYS_DOWN = [pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN]
KEYS_SHOT = [pyxel.KEY_Z, pyxel.KEY_SPACE, pyxel.GAMEPAD1_BUTTON_A]
KEYS_START = [pyxel.KEY_RETURN, pyxel.KEY_SPACE, pyxel.KEY_Z, pyxel.GAMEPAD1_BUTTON_A, pyxel.GAMEPAD1_BUTTON_START]


def pressed(keys: list[int]) -> bool:
    """keys のいずれかが押されていれば True を返す。"""
    return any(pyxel.btn(key) for key in keys)


def triggered(keys: list[int]) -> bool:
    """keys のいずれかがこのフレームで押されたら True を返す。"""
    return any(pyxel.btnp(key) for key in keys)


def draw_text_center(y: int, s: str, col: int) -> None:
    """文字列を画面の左右中央に描く。"""
    x = (SCREEN_W - len(s) * pyxel.FONT_WIDTH) // 2
    pyxel.text(x, y, s, col)


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
    INVINCIBLE_FRAMES = 60

    def __init__(self) -> None:
        super().__init__(SCREEN_W / 2 - 8, SCREEN_H - 32, 16, 16, margin=5)
        self.shot_timer = 0
        self.invincible = 0

    def update(self) -> list[PlayerBullet]:
        """入力に応じて移動し、新しく撃った弾のリストを返す。"""
        dx = int(pressed(KEYS_RIGHT)) - int(pressed(KEYS_LEFT))
        dy = int(pressed(KEYS_DOWN)) - int(pressed(KEYS_UP))
        speed = self.SPEED * (0.7071 if dx != 0 and dy != 0 else 1)
        self.x = pyxel.clamp(self.x + dx * speed, 0, SCREEN_W - self.w)
        self.y = pyxel.clamp(self.y + dy * speed, 0, SCREEN_H - self.h)

        if self.invincible > 0:
            self.invincible -= 1

        if self.shot_timer > 0:
            self.shot_timer -= 1
        if pressed(KEYS_SHOT) and self.shot_timer == 0:
            self.shot_timer = self.SHOT_INTERVAL
            return [PlayerBullet(self.x + 4, self.y - 4)]
        return []

    def draw(self) -> None:
        if self.invincible > 0 and pyxel.frame_count % 4 < 2:
            return
        pyxel.tri(self.x + 7, self.y, self.x, self.y + 15, self.x + 15, self.y + 15, 6)


class Enemy(Entity):
    """まっすぐ下へ進む敵。"""

    SCORE = 100

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 16, 16, margin=2)

    def update(self) -> None:
        self.y += 1.5
        if self.y > SCREEN_H:
            self.alive = False

    def draw(self) -> None:
        pyxel.circ(self.x + 7, self.y + 7, 6, 8)


class Scene:
    """シーン (画面) の基底クラス。update() は次のシーンを返す。"""

    def update(self) -> "Scene":
        return self

    def draw(self) -> None:
        pass


class TitleScene(Scene):
    def update(self) -> Scene:
        if triggered(KEYS_START):
            return PlayScene()
        return self

    def draw(self) -> None:
        pyxel.cls(0)
        draw_text_center(50, "COSMO RUSH", 10)
        if pyxel.frame_count % 30 < 20:
            draw_text_center(104, "PRESS SPACE KEY", 7)


class PlayScene(Scene):
    START_LIVES = 3

    def __init__(self) -> None:
        self.player = Player()
        self.player_bullets: list[PlayerBullet] = []
        self.enemies: list[Enemy] = []
        self.score = 0
        self.lives = self.START_LIVES
        self.frame = 0
        self.game_over_timer = 0

    def update(self) -> Scene:
        self.frame += 1
        if self.lives > 0:
            self.player_bullets += self.player.update()
        if self.frame % SPAWN_INTERVAL == 0:
            self.enemies.append(Enemy(pyxel.rndi(0, SCREEN_W - 16), -16))
        for enemy in self.enemies:
            enemy.update()
        for bullet in self.player_bullets:
            bullet.update()

        self.check_collisions()

        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemies = [e for e in self.enemies if e.alive]

        # 残機がなくなったら、少し待ってからゲームオーバー画面に移る
        if self.lives == 0:
            self.game_over_timer += 1
            if self.game_over_timer >= GAME_OVER_DELAY:
                return GameOverScene(self.score)
        return self

    def check_collisions(self) -> None:
        for bullet in self.player_bullets:
            for enemy in self.enemies:
                if enemy.alive and overlaps(bullet, enemy):
                    bullet.alive = False
                    enemy.alive = False
                    self.score += Enemy.SCORE
                    break

        if self.lives == 0 or self.player.invincible > 0:
            return
        for enemy in self.enemies:
            if overlaps(self.player, enemy):
                enemy.alive = False
                self.lives -= 1
                self.player.invincible = Player.INVINCIBLE_FRAMES
                return

    def draw(self) -> None:
        pyxel.cls(0)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.player_bullets:
            bullet.draw()
        if self.lives > 0:
            self.player.draw()
        pyxel.text(2, 2, f"SCORE {self.score:06}", 7)
        pyxel.text(2, SCREEN_H - 8, f"LIVES {self.lives}", 7)


class GameOverScene(Scene):
    WAIT_FRAMES = 60

    def __init__(self, score: int) -> None:
        self.score = score
        self.timer = 0

    def update(self) -> Scene:
        self.timer += 1
        # 直前の操作で誤って先へ進まないよう、しばらくは入力を受け付けない
        if self.timer >= self.WAIT_FRAMES and triggered(KEYS_START):
            return TitleScene()
        return self

    def draw(self) -> None:
        pyxel.cls(0)
        draw_text_center(56, "GAME OVER", 8)
        draw_text_center(76, f"SCORE {self.score:06}", 7)
        if self.timer >= self.WAIT_FRAMES:
            draw_text_center(112, "PRESS SPACE KEY", 6)


class App:
    def __init__(self) -> None:
        self.scene: Scene = TitleScene()

    def update(self) -> None:
        self.scene = self.scene.update()

    def draw(self) -> None:
        self.scene.draw()


def main() -> None:
    pyxel.init(SCREEN_W, SCREEN_H, title="COSMO RUSH - step5")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
