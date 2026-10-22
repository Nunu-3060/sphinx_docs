# title: COSMO RUSH
# author: Nunu_3060
# desc: A tiny vertical scrolling shooter made with Pyxel
# license: MIT
# version: 1.0
"""COSMO RUSH: 本書の題材ゲームの完成版。

操作:
    矢印キー / WASD / 方向パッド : 移動
    Z / スペース / A ボタン      : ショット (押しっぱなしで連射)
    Enter / スペース / Z         : ゲーム開始
    Esc                          : 終了
"""

import json
from pathlib import Path

import pyxel

SCREEN_W = 128
SCREEN_H = 160
FPS = 30

RESOURCE_FILE = "cosmo_rush.pyxres"
VENDOR_NAME = "Nunu_3060"
APP_NAME = "COSMO RUSH"

# サウンド番号 (効果音はチャンネル 3 で鳴らす)
SE_CHANNEL = 3
SE_SHOT = 0
SE_EXPLOSION = 1
SE_PLAYER_HIT = 2
SE_START = 3
SE_WARNING = 4
SE_GAME_OVER = 5
SE_DAMAGE = 6
MUSIC_TITLE = 0
MUSIC_STAGE = 1

# ステージの進行 (フレーム数)
WARNING_FRAMES = 60
BOSS_FRAME = 45 * FPS
CLEAR_FRAMES = 120
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
    """文字列を画面の左右中央に影付きで描く。"""
    x = (SCREEN_W - len(s) * pyxel.FONT_WIDTH) // 2
    pyxel.text(x + 1, y + 1, s, 1)
    pyxel.text(x, y, s, col)


def load_high_score() -> int:
    """保存されたハイスコアを読み込む。読めなければ 0 を返す。"""
    try:
        path = Path(pyxel.user_data_dir(VENDOR_NAME, APP_NAME)) / "high_score.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        return int(data["high_score"])
    except (OSError, ValueError, KeyError, TypeError):
        return 0


def save_high_score(score: int) -> None:
    """ハイスコアを保存する。保存に失敗してもゲームは続ける。"""
    try:
        path = Path(pyxel.user_data_dir(VENDOR_NAME, APP_NAME)) / "high_score.json"
        path.write_text(json.dumps({"high_score": score}), encoding="utf-8")
    except OSError:
        pass


class Entity:
    """画面上に存在する物体の基底クラス。

    (x, y) は画像の左上の座標、(w, h) は画像の大きさを表す。
    当たり判定には、画像の周囲から margin だけ内側に縮めた矩形を使う。
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
        pyxel.blt(self.x, self.y, 0, 48, 0, 8, 8, 0)


class EnemyBullet(Entity):
    def __init__(self, cx: float, cy: float, vx: float, vy: float) -> None:
        super().__init__(cx - 4, cy - 4, 8, 8, margin=2)
        self.vx = vx
        self.vy = vy

    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy
        if self.is_outside():
            self.alive = False

    def draw(self) -> None:
        pyxel.blt(self.x, self.y, 0, 56, 0, 8, 8, 0)


def aimed_bullet(src: Entity, target: Entity, speed: float) -> EnemyBullet:
    """src の中心から target の中心へ向かう弾を作る。"""
    sx, sy = src.center()
    tx, ty = target.center()
    angle = pyxel.atan2(ty - sy, tx - sx)
    return EnemyBullet(sx, sy, pyxel.cos(angle) * speed, pyxel.sin(angle) * speed)


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
        # 無敵時間中は 2 フレームおきに描画を飛ばして点滅させる
        if self.invincible > 0 and pyxel.frame_count % 4 < 2:
            return
        u = 16 + pyxel.frame_count // 2 % 2 * 16
        pyxel.blt(self.x, self.y, 0, u, 0, 16, 16, 0)


class Enemy(Entity):
    """敵の基底クラス。まっすぐ下へ進む (敵 A)。"""

    U = 0
    V = 16
    HP = 1
    SCORE = 100

    def __init__(self, x: float, y: float, level: int) -> None:
        super().__init__(x, y, 16, 16, margin=2)
        self.level = level
        self.hp = self.HP
        self.age = 0
        self.flash = 0

    def update(self, player: Player) -> list[EnemyBullet]:
        """1 フレーム分動き、新しく撃った弾のリストを返す。"""
        self.age += 1
        if self.flash > 0:
            self.flash -= 1
        self.move()
        if self.y > SCREEN_H:
            self.alive = False
        return self.shoot(player)

    def move(self) -> None:
        self.y += 1.5 + 0.2 * self.level

    def shoot(self, player: Player) -> list[EnemyBullet]:
        return []

    def damage(self) -> bool:
        """弾が当たったときの処理。倒したら True を返す。"""
        self.hp -= 1
        self.flash = 3
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self) -> None:
        u = self.U + pyxel.frame_count // 8 % 2 * self.w
        if self.flash > 0:
            # 被弾した直後は全色を白に置き換えて光らせる
            for col in range(1, 16):
                pyxel.pal(col, 7)
        pyxel.blt(self.x, self.y, 0, u, self.V, self.w, self.h, 0)
        pyxel.pal()


class EnemyB(Enemy):
    """左右に揺れながら下へ進む敵。"""

    U = 32
    HP = 2
    SCORE = 200

    def __init__(self, x: float, y: float, level: int) -> None:
        super().__init__(x, y, level)
        self.base_x = pyxel.clamp(x, 24, SCREEN_W - 40)

    def move(self) -> None:
        self.y += 1.0 + 0.1 * self.level
        self.x = self.base_x + pyxel.sin(self.age * 6) * 24


class EnemyC(Enemy):
    """途中で止まって自機を狙い撃ちし、その後に去っていく敵。"""

    U = 64
    HP = 4
    SCORE = 300
    STOP_FRAMES = 90

    def __init__(self, x: float, y: float, level: int) -> None:
        super().__init__(x, y, level)
        self.stop_y = pyxel.rndi(24, 64)
        self.stop_timer = 0

    def move(self) -> None:
        if self.y < self.stop_y:
            self.y += 2
        elif self.stop_timer < self.STOP_FRAMES:
            self.stop_timer += 1
        else:
            self.y += 3

    def shoot(self, player: Player) -> list[EnemyBullet]:
        if self.stop_timer in (20, 60):
            return [aimed_bullet(self, player, 1.5 + 0.2 * self.level)]
        return []


class Boss(Enemy):
    """ステージの最後に現れる大型の敵。"""

    U = 0
    V = 32
    SCORE = 5000

    def __init__(self, level: int) -> None:
        super().__init__(SCREEN_W / 2 - 16, -32, level)
        self.w = 32
        self.h = 32
        self.margin = 4
        self.hp = self.max_hp = 50 + 20 * level
        self.angle = 0.0

    def move(self) -> None:
        if self.y < 16:
            self.y += 0.5
            return
        # 角度を少しずつ進めて左右に往復する。体力が半分を切ったら進め方を 2 倍にする
        self.angle += 2 if self.hp < self.max_hp / 2 else 1
        self.x = SCREEN_W / 2 - 16 + pyxel.sin(self.angle) * 40

    def shoot(self, player: Player) -> list[EnemyBullet]:
        if self.y < 16:
            return []
        bullets: list[EnemyBullet] = []
        cx, cy = self.center()
        if self.age % 45 == 0:
            # 扇状に 5 発
            for i in range(5):
                angle = 60 + i * 15
                bullets.append(EnemyBullet(cx, cy + 8, pyxel.cos(angle) * 1.5, pyxel.sin(angle) * 1.5))
        if self.hp < self.max_hp / 2 and self.age % 45 in (20, 26, 32):
            # 体力が半分を切ったら狙い撃ちを追加する
            bullets.append(aimed_bullet(self, player, 2.5))
        return bullets

    def draw(self) -> None:
        super().draw()
        # 体力ゲージ
        pyxel.rect(4, 12, (SCREEN_W - 8) * self.hp / self.max_hp, 2, 8)


class Explosion:
    FRAME_TIME = 3
    NUM_FRAMES = 4

    def __init__(self, cx: float, cy: float, delay: int = 0) -> None:
        self.x = cx - 8
        self.y = cy - 8
        self.delay = delay
        self.age = 0
        self.alive = True

    def update(self) -> None:
        if self.delay > 0:
            self.delay -= 1
            return
        self.age += 1
        if self.age >= self.FRAME_TIME * self.NUM_FRAMES:
            self.alive = False

    def draw(self) -> None:
        if self.delay > 0:
            return
        u = self.age // self.FRAME_TIME * 16
        pyxel.blt(self.x, self.y, 0, u, 64, 16, 16, 0)


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
        self.high_score = load_high_score()
        pyxel.playm(MUSIC_TITLE, loop=True)

    def update(self) -> Scene:
        self.background.update()
        if triggered(KEYS_START):
            pyxel.stop()
            pyxel.play(SE_CHANNEL, SE_START)
            return PlayScene(self.background, self.high_score)
        return self

    def draw(self) -> None:
        self.background.draw()
        pyxel.blt(3, 40, 1, 0, 0, 121, 19, 0)
        draw_text_center(68, "- A TINY SPACE SHOOTER -", 6)
        if pyxel.frame_count % 30 < 20:
            draw_text_center(104, "PRESS SPACE KEY", 7)
        draw_text_center(124, f"HI-SCORE {self.high_score:06}", 10)
        draw_text_center(146, "(C) 2026 NUNU_3060", 13)


class PlayScene(Scene):
    START_LIVES = 3

    def __init__(self, background: Background, high_score: int) -> None:
        self.background = background
        self.high_score = high_score
        self.player = Player()
        self.player_bullets: list[PlayerBullet] = []
        self.enemies: list[Enemy] = []
        self.enemy_bullets: list[EnemyBullet] = []
        self.explosions: list[Explosion] = []
        self.boss: Boss | None = None
        self.score = 0
        self.lives = self.START_LIVES
        self.level = 0
        self.frame = 0
        self.clear_timer = 0
        self.game_over_timer = 0
        self.shake = 0
        pyxel.playm(MUSIC_STAGE, loop=True)

    # --- 更新 ---------------------------------------------------------------

    def update(self) -> Scene:
        self.background.update()
        self.frame += 1
        if self.shake > 0:
            self.shake -= 1

        if self.lives > 0:
            self.player_bullets += self.player.update()
        self.spawn_enemies()
        for enemy in self.enemies:
            self.enemy_bullets += enemy.update(self.player)
        for bullet in self.player_bullets:
            bullet.update()
        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.update()
        for explosion in self.explosions:
            explosion.update()

        self.check_collisions()
        self.update_stage()

        # 消えた物体をリストから取り除く
        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemies = [e for e in self.enemies if e.alive]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]
        self.explosions = [e for e in self.explosions if e.alive]

        if self.lives == 0:
            self.game_over_timer += 1
            if self.game_over_timer >= GAME_OVER_DELAY:
                return GameOverScene(self.background, self.score)
        return self

    def spawn_enemies(self) -> None:
        """経過時間に応じて敵を出現させる。"""
        if self.frame >= BOSS_FRAME - WARNING_FRAMES:
            return
        interval = max(10, 30 - self.level * 5)
        if self.frame % interval != 0:
            return
        sec = self.frame // FPS
        kinds: list[type[Enemy]] = [Enemy]
        if sec >= 10:
            kinds.append(EnemyB)
        if sec >= 20:
            kinds.append(EnemyC)
        kind = kinds[pyxel.rndi(0, len(kinds) - 1)]
        self.enemies.append(kind(pyxel.rndi(0, SCREEN_W - 16), -16, self.level))

    def update_stage(self) -> None:
        """警告、ボスの出現、ステージクリアを管理する。"""
        if self.frame == BOSS_FRAME - WARNING_FRAMES:
            pyxel.play(SE_CHANNEL, SE_WARNING)
        if self.frame == BOSS_FRAME:
            self.boss = Boss(self.level)
            self.enemies.append(self.boss)
        if self.boss is not None and not self.boss.alive:
            self.boss = None
            self.clear_timer = CLEAR_FRAMES
        if self.clear_timer > 0:
            self.clear_timer -= 1
            if self.clear_timer == 0:
                self.level += 1
                self.frame = 0

    def check_collisions(self) -> None:
        # 自機の弾と敵
        for bullet in self.player_bullets:
            for enemy in self.enemies:
                if enemy.alive and overlaps(bullet, enemy):
                    bullet.alive = False
                    self.hit_enemy(enemy)
                    break

        if self.lives == 0 or self.player.invincible > 0:
            return
        # 自機と敵、自機と敵の弾
        for enemy in self.enemies:
            if overlaps(self.player, enemy):
                self.hit_player()
                return
        for enemy_bullet in self.enemy_bullets:
            if overlaps(self.player, enemy_bullet):
                enemy_bullet.alive = False
                self.hit_player()
                return

    def hit_enemy(self, enemy: Enemy) -> None:
        if not enemy.damage():
            pyxel.play(SE_CHANNEL, SE_DAMAGE)
            return
        self.add_score(enemy.SCORE)
        cx, cy = enemy.center()
        pyxel.play(SE_CHANNEL, SE_EXPLOSION)
        if isinstance(enemy, Boss):
            # ボスは時間差で何度も爆発させ、画面に残った弾を消す
            for i in range(12):
                self.explosions.append(Explosion(cx + pyxel.rndi(-16, 16), cy + pyxel.rndi(-16, 16), delay=i * 4))
            self.enemy_bullets.clear()
            self.shake = 30
        else:
            self.explosions.append(Explosion(cx, cy))

    def hit_player(self) -> None:
        self.lives -= 1
        self.shake = 10
        cx, cy = self.player.center()
        self.explosions.append(Explosion(cx, cy))
        if self.lives > 0:
            self.player.invincible = Player.INVINCIBLE_FRAMES
        else:
            pyxel.stop()
        pyxel.play(SE_CHANNEL, SE_PLAYER_HIT)

    def add_score(self, points: int) -> None:
        self.score += points
        self.high_score = max(self.high_score, self.score)

    # --- 描画 ---------------------------------------------------------------

    def draw(self) -> None:
        # 画面の揺れはカメラの位置をずらして表現する
        if self.shake > 0:
            pyxel.camera(pyxel.rndi(-2, 2), pyxel.rndi(-2, 2))
        self.background.draw()
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.player_bullets:
            bullet.draw()
        if self.lives > 0:
            self.player.draw()
        for enemy_bullet in self.enemy_bullets:
            enemy_bullet.draw()
        for explosion in self.explosions:
            explosion.draw()
        pyxel.camera()
        self.draw_hud()

    def draw_hud(self) -> None:
        pyxel.text(2, 2, f"SCORE {self.score:06}", 7)
        pyxel.text(70, 2, f"HI {self.high_score:06}", 10)
        for i in range(self.lives):
            pyxel.blt(i * 9 - 2, SCREEN_H - 14, 0, 16, 0, 16, 16, 0, scale=0.5)
        pyxel.text(SCREEN_W - 30, SCREEN_H - 8, f"STAGE {self.level + 1}", 6)
        warning_start = BOSS_FRAME - WARNING_FRAMES
        if warning_start <= self.frame < BOSS_FRAME and self.frame % 10 < 6:
            draw_text_center(70, "WARNING!", 8)
        if self.clear_timer > 0:
            draw_text_center(70, "STAGE CLEAR!", 10)


class GameOverScene(Scene):
    WAIT_FRAMES = 60

    def __init__(self, background: Background, score: int) -> None:
        self.background = background
        self.score = score
        self.is_new_record = score > load_high_score()
        if self.is_new_record:
            save_high_score(score)
        self.timer = 0
        pyxel.stop()
        pyxel.play(0, SE_GAME_OVER)

    def update(self) -> Scene:
        self.background.update()
        self.timer += 1
        if self.timer >= self.WAIT_FRAMES and triggered(KEYS_START):
            return TitleScene(self.background)
        return self

    def draw(self) -> None:
        self.background.draw()
        # ディザリングで背景を半分だけ暗くする
        pyxel.dither(0.5)
        pyxel.rect(0, 0, SCREEN_W, SCREEN_H, 0)
        pyxel.dither(1.0)
        draw_text_center(56, "GAME OVER", 8)
        draw_text_center(76, f"SCORE {self.score:06}", 7)
        if self.is_new_record and pyxel.frame_count % 20 < 14:
            draw_text_center(88, "NEW RECORD!", 10)
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
    pyxel.init(SCREEN_W, SCREEN_H, title=APP_NAME, fps=FPS)
    pyxel.load(RESOURCE_FILE)
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
