"""第 3 章: 乱数とタイマー。

10 フレームごとに、ランダムな位置と色の星を出現させる。
星は出現してから 60 フレーム (2 秒) たつと消える。
"""

import pyxel

SPAWN_INTERVAL = 10
LIFETIME = 60


class Star:
    def __init__(self) -> None:
        self.x = pyxel.rndi(0, 159)
        self.y = pyxel.rndi(12, 119)
        self.col = pyxel.rndi(8, 15)
        self.born = pyxel.frame_count

    def is_expired(self) -> bool:
        return pyxel.frame_count - self.born >= LIFETIME

    def draw(self) -> None:
        # 残り時間が短くなったら点滅させる
        remaining = LIFETIME - (pyxel.frame_count - self.born)
        if remaining < 20 and pyxel.frame_count % 4 < 2:
            return
        pyxel.circ(self.x, self.y, 2, self.col)


class App:
    def __init__(self) -> None:
        self.stars: list[Star] = []

    def update(self) -> None:
        if pyxel.frame_count % SPAWN_INTERVAL == 0:
            self.stars.append(Star())
        self.stars = [star for star in self.stars if not star.is_expired()]

    def draw(self) -> None:
        pyxel.cls(0)
        pyxel.text(4, 4, f"FRAME {pyxel.frame_count}  STARS {len(self.stars)}", 7)
        for star in self.stars:
            star.draw()


def main() -> None:
    pyxel.init(160, 120, title="Random Demo")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
