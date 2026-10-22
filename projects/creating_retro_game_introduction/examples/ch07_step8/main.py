"""第 7 章 ステップ 8: 効果音と BGM を鳴らす。"""

import pyxel

SCREEN_W = 128
SCREEN_H = 160
RESOURCE_FILE = "../assets/cosmo_rush.pyxres"
SPAWN_INTERVAL = 20
GAME_OVER_DELAY = 60

# サウンド番号 (効果音はチャンネル 3 で鳴らす)
SE_CHANNEL = 3
SE_SHOT = 0
SE_EXPLOSION = 1
SE_PLAYER_HIT = 2
SE_START = 3
SE_GAME_OVER = 5
MUSIC_TITLE = 0
MUSIC_STAGE = 1

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
        # イメージバンク 0 の (48, 0) から 8x8 を、黒 (0) を透明色として描く
        pyxel.blt(self.x, self.y, 0, 48, 0, 8, 8, 0)


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
            pyxel.play(SE_CHANNEL, SE_SHOT)
            return [PlayerBullet(self.x + 4, self.y - 4)]
        return []

    def draw(self) -> None:
        if self.invincible > 0 and pyxel.frame_count % 4 < 2:
            return
        # 2 フレームごとに (16, 0) と (32, 0) の絵を切り替えて、噴射の炎を揺らす
        u = 16 + pyxel.frame_count // 2 % 2 * 16
        pyxel.blt(self.x, self.y, 0, u, 0, 16, 16, 0)


class Enemy(Entity):
    """まっすぐ下へ進む敵。"""

    U = 0
    V = 16
    SCORE = 100

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, 16, 16, margin=2)

    def update(self) -> None:
        self.y += 1.5
        if self.y > SCREEN_H:
            self.alive = False

    def draw(self) -> None:
        # 8 フレームごとに 2 コマの絵を切り替える
        u = self.U + pyxel.frame_count // 8 % 2 * self.w
        pyxel.blt(self.x, self.y, 0, u, self.V, self.w, self.h, 0)


class Background:
    """タイルマップをループさせて縦スクロールする背景。"""

    MAP_HEIGHT = 512
    SPEED = 0.5

    def __init__(self) -> None:
        self.offset = 0.0
        # 手前を速く流れる星 (x, y, 速さ) で奥行きを出す
        self.stars = [(pyxel.rndf(0, SCREEN_W), pyxel.rndf(0, SCREEN_H), pyxel.rndf(1.5, 3)) for _ in range(12)]

    def update(self) -> None:
        self.offset = (self.offset + self.SPEED) % self.MAP_HEIGHT
        self.stars = [(x, (y + speed) % SCREEN_H, speed) for x, y, speed in self.stars]

    def draw(self) -> None:
        pyxel.cls(0)
        # 同じタイルマップを縦に 2 枚並べて描き、継ぎ目なくループさせる
        y = int(self.offset) - self.MAP_HEIGHT
        pyxel.bltm(0, y, 0, 0, 0, SCREEN_W, self.MAP_HEIGHT)
        pyxel.bltm(0, y + self.MAP_HEIGHT, 0, 0, 0, SCREEN_W, self.MAP_HEIGHT)
        for x, y_star, speed in self.stars:
            pyxel.pset(x, y_star, 7 if speed > 2.5 else 13)


class Scene:
    """シーン (画面) の基底クラス。update() は次のシーンを返す。"""

    def update(self) -> "Scene":
        return self

    def draw(self) -> None:
        pass


class TitleScene(Scene):
    def __init__(self, background: Background) -> None:
        self.background = background
        pyxel.playm(MUSIC_TITLE, loop=True)

    def update(self) -> Scene:
        self.background.update()
        if triggered(KEYS_START):
            pyxel.stop()
            pyxel.play(SE_CHANNEL, SE_START)
            return PlayScene(self.background)
        return self

    def draw(self) -> None:
        self.background.draw()
        # タイトルロゴはイメージバンク 1 に置いてある
        pyxel.blt(3, 40, 1, 0, 0, 121, 19, 0)
        draw_text_center(68, "- A TINY SPACE SHOOTER -", 6)
        if pyxel.frame_count % 30 < 20:
            draw_text_center(104, "PRESS SPACE KEY", 7)


class PlayScene(Scene):
    START_LIVES = 3

    def __init__(self, background: Background) -> None:
        self.background = background
        self.player = Player()
        self.player_bullets: list[PlayerBullet] = []
        self.enemies: list[Enemy] = []
        self.score = 0
        self.lives = self.START_LIVES
        self.frame = 0
        self.game_over_timer = 0
        pyxel.playm(MUSIC_STAGE, loop=True)

    def update(self) -> Scene:
        self.background.update()
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
                return GameOverScene(self.background, self.score)
        return self

    def check_collisions(self) -> None:
        for bullet in self.player_bullets:
            for enemy in self.enemies:
                if enemy.alive and overlaps(bullet, enemy):
                    bullet.alive = False
                    enemy.alive = False
                    self.score += Enemy.SCORE
                    pyxel.play(SE_CHANNEL, SE_EXPLOSION)
                    break

        if self.lives == 0 or self.player.invincible > 0:
            return
        for enemy in self.enemies:
            if overlaps(self.player, enemy):
                enemy.alive = False
                self.lives -= 1
                self.player.invincible = Player.INVINCIBLE_FRAMES
                if self.lives == 0:
                    pyxel.stop()
                pyxel.play(SE_CHANNEL, SE_PLAYER_HIT)
                return

    def draw(self) -> None:
        self.background.draw()
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.player_bullets:
            bullet.draw()
        if self.lives > 0:
            self.player.draw()
        pyxel.text(2, 2, f"SCORE {self.score:06}", 7)
        # 残機は自機の絵を半分の大きさで並べて表す
        for i in range(self.lives):
            pyxel.blt(i * 9 - 2, SCREEN_H - 14, 0, 16, 0, 16, 16, 0, scale=0.5)


class GameOverScene(Scene):
    WAIT_FRAMES = 60

    def __init__(self, background: Background, score: int) -> None:
        self.background = background
        self.score = score
        self.timer = 0
        pyxel.stop()
        pyxel.play(0, SE_GAME_OVER)

    def update(self) -> Scene:
        self.background.update()
        self.timer += 1
        # 直前の操作で誤って先へ進まないよう、しばらくは入力を受け付けない
        if self.timer >= self.WAIT_FRAMES and triggered(KEYS_START):
            return TitleScene(self.background)
        return self

    def draw(self) -> None:
        self.background.draw()
        draw_text_center(56, "GAME OVER", 8)
        draw_text_center(76, f"SCORE {self.score:06}", 7)
        if self.timer >= self.WAIT_FRAMES:
            draw_text_center(112, "PRESS SPACE KEY", 6)


class App:
    def __init__(self) -> None:
        self.scene: Scene = TitleScene(Background())

    def update(self) -> None:
        self.scene = self.scene.update()

    def draw(self) -> None:
        self.scene.draw()


def main() -> None:
    pyxel.init(SCREEN_W, SCREEN_H, title="COSMO RUSH - step8")
    pyxel.load(RESOURCE_FILE)
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
