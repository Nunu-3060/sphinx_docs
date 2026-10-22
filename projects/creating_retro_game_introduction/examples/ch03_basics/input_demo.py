"""第 3 章: キー入力の取得。

矢印キーで四角形を動かす (btn)。
スペースキーを押した回数 (btnp)、押し続けたときのリピート回数 (btnp の hold と repeat)、
離した回数 (btnr) を数えて表示する。
"""

import pyxel


class App:
    def __init__(self) -> None:
        self.x = 76
        self.y = 80
        self.press_count = 0
        self.repeat_count = 0
        self.release_count = 0

    def update(self) -> None:
        # btn: 押されている間、毎フレーム True になる
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 2

        # btnp: 押された瞬間のフレームだけ True になる
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.press_count += 1
        # hold と repeat を指定すると、押し続けたときに一定間隔で True になる
        if pyxel.btnp(pyxel.KEY_SPACE, hold=15, repeat=5):
            self.repeat_count += 1
        # btnr: 離された瞬間のフレームだけ True になる
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.release_count += 1

    def draw(self) -> None:
        pyxel.cls(1)
        pyxel.text(4, 4, "ARROW KEYS: MOVE", 7)
        pyxel.text(4, 16, f"btnp(SPACE)        : {self.press_count}", 7)
        pyxel.text(4, 24, f"btnp(SPACE, 15, 5) : {self.repeat_count}", 7)
        pyxel.text(4, 32, f"btnr(SPACE)        : {self.release_count}", 7)
        col = 10 if pyxel.btn(pyxel.KEY_SPACE) else 11
        pyxel.rect(self.x, self.y, 8, 8, col)


def main() -> None:
    pyxel.init(160, 120, title="Input Demo")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
