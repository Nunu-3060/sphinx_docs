"""第 3 章: 速度と加速度による動き。

ボールに重力 (下向きの加速度) をかけ、壁と床で跳ね返らせる。
スペースキーで新しいボールを投げる。
"""

import pyxel

SCREEN_W = 160
SCREEN_H = 120
GRAVITY = 0.3
BOUNCE = 0.8
RADIUS = 4


class Ball:
    def __init__(self) -> None:
        self.x = 20.0
        self.y = 20.0
        self.vx = pyxel.rndf(1, 3)
        self.vy = pyxel.rndf(-3, 0)
        self.col = pyxel.rndi(8, 15)

    def update(self) -> None:
        # 加速度で速度を変え、速度で位置を変える
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        # 壁や床に当たったら、画面内に戻して速度の向きを反転させる
        if self.x < RADIUS:
            self.x = RADIUS
            self.vx = -self.vx
        if self.x > SCREEN_W - RADIUS:
            self.x = SCREEN_W - RADIUS
            self.vx = -self.vx
        if self.y > SCREEN_H - RADIUS:
            self.y = SCREEN_H - RADIUS
            self.vy = -self.vy * BOUNCE

    def draw(self) -> None:
        pyxel.circ(self.x, self.y, RADIUS, self.col)


class App:
    def __init__(self) -> None:
        self.balls = [Ball()]

    def update(self) -> None:
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.balls.append(Ball())
        for ball in self.balls:
            ball.update()

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.text(4, 4, "SPACE: THROW A BALL", 7)
        for ball in self.balls:
            ball.draw()


def main() -> None:
    pyxel.init(SCREEN_W, SCREEN_H, title="Motion Demo")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
