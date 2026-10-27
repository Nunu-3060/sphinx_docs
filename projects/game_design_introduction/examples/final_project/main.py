"""『宝石と見張り』を遊ぶ（pygame-ce）。

操作:
    矢印キー / WASD : 移動
    Space           : その場で待つ
    Z               : 1 手戻す
    R               : レベルを最初からやり直す
    Enter           : （クリア後）次のレベルへ
    Esc             : 終了

遊んだ記録は playlog.csv に追記される（列: session, level, x, y, event）。
../playtest_heatmap.py に渡すと、プレイヤーが捕まった位置などをヒートマップにできる。

実行例:
    python main.py              # 最初のレベルから遊ぶ
    python main.py --level 3    # 3 番目のレベルから遊ぶ
    python main.py --no-log     # 記録を残さない
"""

from __future__ import annotations

import argparse
import csv
import time
from pathlib import Path

import pygame

from game_logic import DOWN, LEFT, RIGHT, UP, WAIT, Level, Pos, State, Status, load_levels
from solver import solve

TILE = 48
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
BOARD_TOP = 96  # 盤面の上に HUD を表示する
FPS = 30

COLORS = {
    "background": (28, 30, 40),
    "floor": (70, 74, 90),
    "wall": (130, 136, 156),
    "gem": (250, 210, 70),
    "exit_closed": (90, 90, 100),
    "exit_open": (80, 200, 120),
    "player": (90, 170, 250),
    "guard": (230, 80, 80),
    "text": (235, 235, 235),
    "sub_text": (170, 175, 190),
}

KEY_TO_MOVE: dict[int, Pos] = {
    pygame.K_UP: UP, pygame.K_w: UP,
    pygame.K_DOWN: DOWN, pygame.K_s: DOWN,
    pygame.K_LEFT: LEFT, pygame.K_a: LEFT,
    pygame.K_RIGHT: RIGHT, pygame.K_d: RIGHT,
    pygame.K_SPACE: WAIT,
}

HERE = Path(__file__).parent
LOG_PATH = HERE / "playlog.csv"


class PlayLog:
    """遊んだ記録を CSV に追記する。enabled が False なら何もしない。"""

    def __init__(self, path: Path, enabled: bool) -> None:
        self.path = path
        self.enabled = enabled
        self.session = int(time.time())

    def write(self, level: Level, pos: Pos, event: str) -> None:
        if not self.enabled:
            return
        is_new = not self.path.exists()
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(["session", "level", "x", "y", "event"])
            writer.writerow([self.session, level.name, pos[0], pos[1], event])


class Game:
    def __init__(self, levels: list[Level], start_index: int, log: PlayLog) -> None:
        self.levels = levels
        self.best = [len(moves) if (moves := solve(level).moves) else None for level in levels]
        self.log = log
        self.index = start_index
        self.history: list[State] = []
        self.message = ""
        self.load(start_index)

    @property
    def level(self) -> Level:
        return self.levels[self.index]

    @property
    def state(self) -> State:
        return self.history[-1]

    def load(self, index: int) -> None:
        self.index = index
        self.history = [self.level.initial]
        self.message = self.level.hint

    def handle_key(self, key: int) -> None:
        if key == pygame.K_z and len(self.history) > 1:
            self.history.pop()
            self.message = "1 手戻した"
            self.log.write(self.level, self.state.player, "undo")
        elif key == pygame.K_r:
            self.log.write(self.level, self.state.player, "restart")
            self.load(self.index)
        elif key == pygame.K_RETURN and self.state.status is Status.CLEARED:
            if self.index + 1 < len(self.levels):
                self.load(self.index + 1)
            else:
                self.message = "すべてのレベルをクリアした！ Esc で終了"
        elif key in KEY_TO_MOVE:
            self.move(KEY_TO_MOVE[key])

    def move(self, move: Pos) -> None:
        nxt = self.level.step(self.state, move)
        if nxt is None:
            return  # 壁に向かって動こうとした、またはクリアや捕まった後
        self.history.append(nxt)
        self.log.write(self.level, nxt.player, "wait" if move == WAIT else "move")
        if nxt.status is Status.CAUGHT:
            self.message = "見つかった！ Z で 1 手戻す / R でやり直す"
            self.log.write(self.level, nxt.player, "caught")
        elif nxt.status is Status.CLEARED:
            best = self.best[self.index]
            self.message = f"クリア！ {nxt.turn} 手（最短 {best} 手）  Enter で次へ"
            self.log.write(self.level, nxt.player, "clear")
        elif nxt.player == self.level.exit:
            self.message = f"宝石があと {len(nxt.gems)} 個残っている"
        else:
            self.message = ""

    def draw(self, screen: pygame.Surface, font: pygame.font.Font, small: pygame.font.Font) -> None:
        screen.fill(COLORS["background"])
        level, state = self.level, self.state
        left = (SCREEN_WIDTH - level.width * TILE) // 2

        def rect(pos: Pos, margin: int = 0) -> pygame.Rect:
            return pygame.Rect(left + pos[0] * TILE + margin, BOARD_TOP + pos[1] * TILE + margin,
                               TILE - 2 * margin, TILE - 2 * margin)

        for y in range(level.height):
            for x in range(level.width):
                color = COLORS["wall"] if (x, y) in level.walls else COLORS["floor"]
                pygame.draw.rect(screen, color, rect((x, y)))
        exit_color = COLORS["exit_open"] if not state.gems else COLORS["exit_closed"]
        pygame.draw.rect(screen, exit_color, rect(level.exit, 6), border_radius=6)
        for gem in state.gems:
            r = rect(gem, 12)
            pygame.draw.polygon(screen, COLORS["gem"], [r.midtop, r.midright, r.midbottom, r.midleft])
        for guard in state.guards:
            r = rect(guard.pos, 8)
            pygame.draw.ellipse(screen, COLORS["guard"], r)
            # 次に進む向きを白い線で示し、プレイヤーが動きを予測できるようにする。
            tip = (r.centerx + guard.direction[0] * TILE // 2, r.centery + guard.direction[1] * TILE // 2)
            pygame.draw.line(screen, COLORS["text"], r.center, tip, 3)
        pygame.draw.ellipse(screen, COLORS["player"], rect(state.player, 8))

        best = self.best[self.index]
        title = f"レベル {self.index + 1} / {len(self.levels)}：{level.name}"
        status = f"手数 {state.turn}　残りの宝石 {len(state.gems)}　最短 {best} 手"
        screen.blit(font.render(title, True, COLORS["text"]), (16, 12))
        screen.blit(small.render(status, True, COLORS["sub_text"]), (16, 44))
        screen.blit(small.render(self.message, True, COLORS["text"]), (16, 68))
        keys = "矢印: 移動  Space: 待つ  Z: 戻す  R: やり直し  Esc: 終了"
        screen.blit(small.render(keys, True, COLORS["sub_text"]), (16, SCREEN_HEIGHT - 32))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--level", type=int, default=1, help="最初に遊ぶレベルの番号（1 から数える）")
    parser.add_argument("--no-log", action="store_true", help="playlog.csv に記録しない")
    parser.add_argument("--frames", type=int, help="指定したフレーム数で自動的に終了する（動作確認用）")
    args = parser.parse_args()

    levels = load_levels(HERE / "levels")
    start = min(max(args.level, 1), len(levels)) - 1
    game = Game(levels, start, PlayLog(LOG_PATH, enabled=not args.no_log))

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("宝石と見張り")
    font = pygame.font.SysFont("yugothic,meiryo,msgothic", 24)
    small = pygame.font.SysFont("yugothic,meiryo,msgothic", 18)
    clock = pygame.time.Clock()

    frame = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == pygame.KEYDOWN:
                game.handle_key(event.key)
        game.draw(screen, font, small)
        pygame.display.flip()
        clock.tick(FPS)
        frame += 1
        if args.frames is not None and frame >= args.frames:
            running = False
    pygame.quit()


if __name__ == "__main__":
    main()
