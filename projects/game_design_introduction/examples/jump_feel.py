"""ジャンプの操作感を比べるデモ（pygame-ce）。

次の 4 つの工夫を数字キーで個別に ON / OFF し、操作感の違いを確かめる。

* [1] コヨーテタイム : 足場から落ちた直後の数フレームはまだジャンプできる
* [2] 先行入力       : 着地の少し前に押したジャンプを覚えておき、着地した瞬間に跳ぶ
* [3] 可変ジャンプ   : ボタンを早く離すと低く跳ぶ
* [4] 落下を速くする : 落ちるときだけ重力を強くし、ふわふわした感じを減らす

操作: ←→ で移動、Space でジャンプ、Esc で終了。穴に落ちるとスタート地点に戻る。

実行例:
    python jump_feel.py                      # デモを起動する
    python jump_feel.py --plot jump.png      # ジャンプの軌跡をグラフにして保存する（ウィンドウは開かない）
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

TILE = 32
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FPS = 60

# 物理パラメータ（単位はピクセルとフレーム。y 軸は下向きが正）
GRAVITY = 0.5
FALL_GRAVITY_SCALE = 1.8  # [4] 落下中の重力の倍率
LOW_JUMP_GRAVITY_SCALE = 3.0  # [3] 上昇中にボタンを離したときの重力の倍率
JUMP_SPEED = 11.0
MAX_FALL_SPEED = 12.0
RUN_ACCEL = 0.8
RUN_SPEED = 5.0
FRICTION = 0.7
COYOTE_FRAMES = 6  # [1] 足場を離れてからジャンプを受け付けるフレーム数
BUFFER_FRAMES = 6  # [2] ジャンプの入力を覚えておくフレーム数

PLAYER_WIDTH = 24
PLAYER_HEIGHT = 30
EDGE = 1e-6  # 矩形の右端・下端の判定に使う微小量
START_POSITION = (2 * TILE, 12 * TILE - PLAYER_HEIGHT)

# '#' が壁と足場。下端の '.' は穴である。
LEVEL = [
    "#########################",
    "#.......................#",
    "#.......................#",
    "#.......................#",
    "#..####.................#",
    "#.......................#",
    "#.......................#",
    "#...........####........#",
    "#.......................#",
    "#.......................#",
    "#..................####.#",
    "#.......................#",
    "#.......................#",
    "######...#####...########",
    "######...#####...########",
]


@dataclass
class JumpSettings:
    """ON / OFF を切り替えられる 4 つの工夫。"""

    coyote_time: bool = True
    jump_buffer: bool = True
    variable_jump: bool = True
    heavy_fall: bool = True


@dataclass
class InputState:
    """1 フレーム分の入力。"""

    move: int = 0  # -1: 左, 0: なし, 1: 右
    jump_pressed: bool = False  # このフレームでジャンプボタンが押された
    jump_held: bool = False  # ジャンプボタンが押され続けている


def apply_gravity(vy: float, jump_held: bool, settings: JumpSettings) -> float:
    """1 フレーム分の重力を速度に加える。"""
    gravity = GRAVITY
    if vy > 0 and settings.heavy_fall:
        gravity *= FALL_GRAVITY_SCALE
    elif vy < 0 and settings.variable_jump and not jump_held:
        gravity *= LOW_JUMP_GRAVITY_SCALE
    return min(vy + gravity, MAX_FALL_SPEED)


def solid_tiles(level: list[str]) -> set[tuple[int, int]]:
    """壁と足場のタイル座標（列, 行）の集合を作る。"""
    return {(col, row) for row, line in enumerate(level) for col, char in enumerate(line) if char == "#"}


class Player:
    def __init__(self) -> None:
        self.respawn()

    def respawn(self) -> None:
        """スタート地点に戻す。"""
        self.x, self.y = float(START_POSITION[0]), float(START_POSITION[1])
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.air_frames = COYOTE_FRAMES + 1  # 足場を離れてからのフレーム数
        self.buffer_frames = 0  # 先行入力の残りフレーム数

    def update(self, inp: InputState, solids: set[tuple[int, int]], settings: JumpSettings) -> None:
        self._update_run(inp.move)
        self._update_jump(inp, settings)
        self.vy = apply_gravity(self.vy, inp.jump_held, settings)
        self._move_x(solids)
        self._move_y(solids)
        self.air_frames = 0 if self.on_ground else self.air_frames + 1
        if self.y > SCREEN_HEIGHT:
            self.respawn()  # 穴に落ちたらやり直す

    def _update_run(self, move: int) -> None:
        if move:
            self.vx = max(-RUN_SPEED, min(RUN_SPEED, self.vx + move * RUN_ACCEL))
        else:
            self.vx *= FRICTION
            if abs(self.vx) < 0.1:
                self.vx = 0.0

    def _update_jump(self, inp: InputState, settings: JumpSettings) -> None:
        if inp.jump_pressed:
            # 先行入力が OFF のときは、押したフレームだけ有効にする。
            self.buffer_frames = BUFFER_FRAMES if settings.jump_buffer else 1
        can_jump = self.on_ground or (settings.coyote_time and self.air_frames <= COYOTE_FRAMES)
        if self.buffer_frames > 0 and can_jump:
            self.vy = -JUMP_SPEED
            self.on_ground = False
            self.buffer_frames = 0
            self.air_frames = COYOTE_FRAMES + 1  # 空中でもう一度跳べないようにする
        self.buffer_frames = max(0, self.buffer_frames - 1)

    def _overlapping_tiles(self) -> list[tuple[int, int]]:
        """プレイヤーの矩形と重なるタイル座標を返す。右端と下端はわずかに内側で判定する。"""
        left, right = int(self.x // TILE), int((self.x + PLAYER_WIDTH - EDGE) // TILE)
        top, bottom = int(self.y // TILE), int((self.y + PLAYER_HEIGHT - EDGE) // TILE)
        return [(col, row) for row in range(top, bottom + 1) for col in range(left, right + 1)]

    def _move_x(self, solids: set[tuple[int, int]]) -> None:
        self.x += self.vx
        for col, _ in (tile for tile in self._overlapping_tiles() if tile in solids):
            if self.vx > 0:
                self.x = col * TILE - PLAYER_WIDTH
            elif self.vx < 0:
                self.x = (col + 1) * TILE
            self.vx = 0.0

    def _move_y(self, solids: set[tuple[int, int]]) -> None:
        self.y += self.vy
        self.on_ground = False
        for _, row in (tile for tile in self._overlapping_tiles() if tile in solids):
            if self.vy > 0:
                self.y = row * TILE - PLAYER_HEIGHT
                self.on_ground = True
            elif self.vy < 0:
                self.y = (row + 1) * TILE
            self.vy = 0.0


def run_demo(max_frames: int | None) -> None:
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ジャンプの操作感")
    font = pygame.font.SysFont("yugothic,meiryo,msgothic", 18)
    clock = pygame.time.Clock()
    solids = solid_tiles(LEVEL)
    settings = JumpSettings()
    player = Player()
    toggles = {
        pygame.K_1: "coyote_time",
        pygame.K_2: "jump_buffer",
        pygame.K_3: "variable_jump",
        pygame.K_4: "heavy_fall",
    }
    labels = {
        "coyote_time": "[1] コヨーテタイム",
        "jump_buffer": "[2] 先行入力",
        "variable_jump": "[3] 可変ジャンプ",
        "heavy_fall": "[4] 落下を速くする",
    }

    frame = 0
    running = True
    while running:
        inp = InputState()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inp.jump_pressed = True
            elif event.type == pygame.KEYDOWN and event.key in toggles:
                name = toggles[event.key]
                setattr(settings, name, not getattr(settings, name))
        keys = pygame.key.get_pressed()
        inp.move = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        inp.jump_held = bool(keys[pygame.K_SPACE])

        player.update(inp, solids, settings)

        screen.fill((30, 34, 48))
        for col, row in solids:
            pygame.draw.rect(screen, (120, 128, 150), (col * TILE, row * TILE, TILE, TILE))
        # 足場の上は水色、コヨーテタイムの猶予中は黄色、それ以外の空中は橙色で描く。
        if player.on_ground:
            color = (90, 200, 250)
        elif settings.coyote_time and player.air_frames <= COYOTE_FRAMES and player.vy >= 0:
            color = (250, 220, 80)
        else:
            color = (250, 140, 60)
        pygame.draw.rect(screen, color, (round(player.x), round(player.y), PLAYER_WIDTH, PLAYER_HEIGHT))
        for i, (name, label) in enumerate(labels.items()):
            state = "ON" if getattr(settings, name) else "OFF"
            screen.blit(font.render(f"{label}: {state}", True, (240, 240, 240)), (44, 40 + i * 24))
        screen.blit(font.render("←→: 移動  Space: ジャンプ  Esc: 終了", True, (200, 200, 200)), (44, 150))
        pygame.display.flip()
        clock.tick(FPS)

        frame += 1
        if max_frames is not None and frame >= max_frames:
            running = False
    pygame.quit()


def simulate_height(settings: JumpSettings, hold_frames: int) -> list[float]:
    """地面から跳んだときの、フレームごとの高さ（上向きが正）を返す。"""
    vy = -JUMP_SPEED
    y = 0.0
    heights = [0.0]
    frame = 0
    while True:
        vy = apply_gravity(vy, frame < hold_frames, settings)
        y += vy
        frame += 1
        if y >= 0:
            heights.append(0.0)
            return heights
        heights.append(-y)


def save_plot(output: str) -> None:
    import matplotlib.pyplot as plt

    long_press = 1000
    cases = [
        ("重力が一定", JumpSettings(variable_jump=False, heavy_fall=False), long_press),
        ("落下を速くする（長押し）", JumpSettings(variable_jump=True, heavy_fall=True), long_press),
        ("落下を速くする＋可変ジャンプ（6 フレームで離す）", JumpSettings(variable_jump=True, heavy_fall=True), 6),
    ]
    plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]
    fig, ax = plt.subplots(figsize=(7, 4))
    for label, settings, hold in cases:
        heights = simulate_height(settings, hold)
        ax.plot(range(len(heights)), heights, marker=".", label=f"{label}: {len(heights) - 1} フレーム")
    ax.set_xlabel("ジャンプしてからのフレーム数（60 fps）")
    ax.set_ylabel("高さ [ピクセル]")
    ax.set_title("ジャンプの軌跡")
    ax.set_ylim(0, 175)  # 凡例を曲線の上に置くための余白を取る
    ax.grid(alpha=0.3)
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(output, dpi=110)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--plot", metavar="OUTPUT", help="ジャンプの軌跡のグラフを保存して終了する")
    parser.add_argument("--frames", type=int, help="指定したフレーム数で自動的に終了する（動作確認用）")
    args = parser.parse_args()
    if args.plot:
        save_plot(args.plot)
    else:
        run_demo(args.frames)


if __name__ == "__main__":
    main()
