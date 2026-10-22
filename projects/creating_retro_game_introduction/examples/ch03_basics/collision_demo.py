"""第 3 章: 当たり判定。

矢印キーで動かす四角形と円が、固定された四角形と円に重なると色が変わる。
四角形どうしは AABB 判定、円どうしは中心間の距離で判定する。
"""

import pyxel


def rects_overlap(
    x1: float, y1: float, w1: float, h1: float,
    x2: float, y2: float, w2: float, h2: float,
) -> bool:
    """2 つの矩形が重なっていれば True を返す (AABB 判定)。"""
    return x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1


def circles_overlap(x1: float, y1: float, r1: float, x2: float, y2: float, r2: float) -> bool:
    """2 つの円が重なっていれば True を返す。平方根を避けるため 2 乗どうしで比べる。"""
    dx = x2 - x1
    dy = y2 - y1
    return dx * dx + dy * dy < (r1 + r2) * (r1 + r2)


class App:
    def __init__(self) -> None:
        self.x = 50.0
        self.y = 40.0

    def update(self) -> None:
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1.5
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1.5
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 1.5
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1.5

    def draw(self) -> None:
        pyxel.cls(1)
        pyxel.text(4, 4, "ARROW KEYS: MOVE", 7)

        # 四角形どうし: 動かす四角形 (self.x, self.y, 16, 16) と固定の四角形
        rect_hit = rects_overlap(self.x, self.y, 16, 16, 60, 30, 24, 16)
        pyxel.rect(60, 30, 24, 16, 8 if rect_hit else 13)
        pyxel.rectb(self.x, self.y, 16, 16, 10)

        # 円どうし: 動かす円 (四角形の中心、半径 6) と固定の円
        cx = self.x + 8
        cy = self.y + 8
        circle_hit = circles_overlap(cx, cy, 6, 110, 80, 14)
        pyxel.circ(110, 80, 14, 8 if circle_hit else 13)
        pyxel.circb(cx, cy, 6, 11)

        rect_label = "HIT" if rect_hit else "---"
        circle_label = "HIT" if circle_hit else "---"
        pyxel.text(4, 110, f"RECT: {rect_label}  CIRCLE: {circle_label}", 7)


def main() -> None:
    pyxel.init(160, 120, title="Collision Demo")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
