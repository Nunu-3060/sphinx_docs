"""第 10 章: ジャンプの高さと滞空時間から重力と初速を決め、ゲームらしい調整を加える。

足場の途中に穴がある。落ちると左端からやり直す。
ジャンプの軌跡を点で残し、目標の高さに線を引いている。

操作方法:
    左右キー: 走る
    スペースキー: ジャンプ（押す長さで高さが変わる）
    1 キー: 押す長さで高さを変える調整の有無を切り替える
    2 キー: 下降中に重力を強める調整の有無を切り替える
    3 キー: コヨーテタイムと先行入力の有無を切り替える
    Esc キー: 終了する
"""

from dataclasses import dataclass

import pygame

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GROUND_Y = 400.0
GROUND_SPANS = ((0.0, 300.0), (380.0, 640.0))  # 足場がある x の範囲（間は穴）
PLAYER_WIDTH = 24
PLAYER_HEIGHT = 32

JUMP_HEIGHT = 96.0  # ジャンプの最高点の高さ（ピクセル）
TIME_TO_APEX = 0.36  # 最高点に達するまでの時間（秒）
FALL_GRAVITY_SCALE = 2.0  # 下降中に重力を何倍にするか
JUMP_CUT_SCALE = 0.4  # 上昇中にボタンを離したとき、上向きの速さを初速の何倍までに抑えるか
MAX_FALL_SPEED = 900.0  # 落下の最高速度（ピクセル毎秒）
RUN_SPEED = 220.0  # 走る最高速度（ピクセル毎秒）
GROUND_ACCEL = 1800.0  # 地上で加速するときの加速度（ピクセル毎秒毎秒）
GROUND_DECEL = 2400.0  # 地上で入力を離したときの減速度（摩擦に相当）
AIR_ACCEL = 900.0  # 空中での加速度
COYOTE_TIME = 0.1  # 足場から離れた後もジャンプを受け付ける時間（秒）
JUMP_BUFFER_TIME = 0.1  # 着地前に押したジャンプを覚えておく時間（秒）


def jump_parameters(height: float, time_to_apex: float) -> tuple[float, float]:
    """最高点の高さ h と、そこに達するまでの時間 T から、重力加速度 g と初速 v0 を求める。

    v0 = g T、h = v0 T - g T^2 / 2 を解くと、g = 2h / T^2、v0 = 2h / T になる。
    """
    gravity = 2 * height / time_to_apex ** 2
    jump_speed = 2 * height / time_to_apex
    return gravity, jump_speed


GRAVITY, JUMP_SPEED = jump_parameters(JUMP_HEIGHT, TIME_TO_APEX)


def approach(current: float, target: float, max_delta: float) -> float:
    """current を target へ最大 max_delta だけ近づける。行き過ぎない。"""
    if current < target:
        return min(current + max_delta, target)
    return max(current - max_delta, target)


@dataclass
class Options:
    variable_height: bool = True
    fall_gravity: bool = True
    forgiveness: bool = True  # コヨーテタイムと先行入力


class Player:
    """位置は足元の中央。画面座標なので、y が大きいほど下にある。"""

    def __init__(self) -> None:
        self.position = pygame.Vector2(60, GROUND_Y)
        self.velocity = pygame.Vector2(0, 0)
        self.on_ground = True
        self.coyote_timer = 0.0  # 残りのコヨーテタイム
        self.buffer_timer = 0.0  # 先行入力の残り時間

    def update(self, dt: float, move: float, jump_pressed: bool, jump_held: bool, options: Options) -> bool:
        """1 フレーム進める。ジャンプしたら True を返す。"""
        # 横方向: 目標の速度へ、加速度の上限つきで近づける
        if self.on_ground:
            accel = GROUND_ACCEL if move != 0 else GROUND_DECEL
        else:
            accel = AIR_ACCEL
        self.velocity.x = approach(self.velocity.x, move * RUN_SPEED, accel * dt)

        # ジャンプの入力を受け付けるかどうか
        if jump_pressed and options.forgiveness:
            self.buffer_timer = JUMP_BUFFER_TIME
        wants_jump = jump_pressed or self.buffer_timer > 0
        can_jump = self.on_ground or self.coyote_timer > 0
        jumped = False
        if wants_jump and can_jump:
            self.velocity.y = -JUMP_SPEED
            self.on_ground = False
            self.coyote_timer = self.buffer_timer = 0.0
            jumped = True
        self.buffer_timer = max(0.0, self.buffer_timer - dt)
        self.coyote_timer = max(0.0, self.coyote_timer - dt)

        # 上昇中にボタンを離したら、上向きの速さを抑える（y は下向きが正なので、上昇中は負）
        if options.variable_height and not jump_held:
            self.velocity.y = max(self.velocity.y, -JUMP_SPEED * JUMP_CUT_SCALE)

        # 縦方向: 重力が一定とみなせる 1 フレームの間は、等加速度運動の式で正確に進める
        gravity = GRAVITY
        if options.fall_gravity and self.velocity.y > 0:
            gravity *= FALL_GRAVITY_SCALE
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt + 0.5 * gravity * dt * dt
        self.velocity.y = min(self.velocity.y + gravity * dt, MAX_FALL_SPEED)
        self.land_or_fall(options)
        return jumped

    def land_or_fall(self, options: Options) -> None:
        """足場の上なら着地させ、足場が無ければ落下を始める。"""
        over_ground = any(left <= self.position.x <= right for left, right in GROUND_SPANS)
        if over_ground and self.velocity.y >= 0 and GROUND_Y <= self.position.y <= GROUND_Y + 20:
            self.position.y = GROUND_Y
            self.velocity.y = 0
            self.on_ground = True
        elif self.on_ground:
            # 足場から歩いて離れた瞬間
            self.on_ground = False
            self.coyote_timer = COYOTE_TIME if options.forgiveness else 0.0


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Jump: gravity from height and time')
    font = pygame.font.Font(None, 22)
    clock = pygame.time.Clock()
    player = Player()
    options = Options()
    trail: list[tuple[float, float]] = []

    running = True
    while running:
        jump_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    jump_pressed = True
                elif event.key == pygame.K_1:
                    options.variable_height = not options.variable_height
                elif event.key == pygame.K_2:
                    options.fall_gravity = not options.fall_gravity
                elif event.key == pygame.K_3:
                    options.forgiveness = not options.forgiveness
        dt = min(clock.tick(60) / 1000, 1 / 30)
        keys = pygame.key.get_pressed()
        move = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        if player.update(dt, move, jump_pressed, keys[pygame.K_SPACE], options):
            trail.clear()
        if not player.on_ground:
            trail.append((player.position.x, player.position.y))
        player.position.x %= SCREEN_WIDTH
        if player.position.y > SCREEN_HEIGHT + 100:
            player = Player()

        screen.fill((20, 24, 36))
        pygame.draw.line(screen, (70, 80, 100), (0, GROUND_Y - JUMP_HEIGHT), (SCREEN_WIDTH, GROUND_Y - JUMP_HEIGHT))
        for left, right in GROUND_SPANS:
            pygame.draw.rect(screen, (90, 120, 170), (left, GROUND_Y, right - left, SCREEN_HEIGHT - GROUND_Y))
        for p in trail[::2]:
            pygame.draw.circle(screen, (240, 200, 90), p, 2)
        body = pygame.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
        body.midbottom = (round(player.position.x), round(player.position.y))
        pygame.draw.rect(screen, (240, 240, 240), body)
        lines = [
            f'g = {GRAVITY:.0f} px/s^2, v0 = {JUMP_SPEED:.0f} px/s (height {JUMP_HEIGHT:.0f}, apex {TIME_TO_APEX} s)',
            f'1: variable height {options.variable_height}   2: fall gravity {options.fall_gravity}',
            f'3: coyote time and jump buffer {options.forgiveness}',
        ]
        for i, text in enumerate(lines):
            screen.blit(font.render(text, True, (230, 230, 230)), (10, 10 + 20 * i))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
