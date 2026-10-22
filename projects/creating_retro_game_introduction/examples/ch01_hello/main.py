"""第 1 章: Pyxel の最小構成のプログラム。

文字を表示し、円を左から右へ動かす。
"""

import pyxel

SCREEN_W = 160
SCREEN_H = 120


class App:
    def __init__(self) -> None:
        self.x = 0

    def update(self) -> None:
        """1 フレームごとに呼ばれ、ゲームの状態を更新する。"""
        self.x = (self.x + 1) % SCREEN_W

    def draw(self) -> None:
        """1 フレームごとに呼ばれ、画面を描画する。"""
        pyxel.cls(1)
        pyxel.text(54, 40, "Hello, Pyxel!", 7)
        pyxel.circ(self.x, 80, 8, 10)


def main() -> None:
    pyxel.init(SCREEN_W, SCREEN_H, title="Hello Pyxel")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
