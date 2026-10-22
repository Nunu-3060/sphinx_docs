"""第 3 章: 図形と文字の描画。

パレットの 16 色と、主な描画命令の結果を並べて表示する。
"""

import pyxel


class App:
    def update(self) -> None:
        pass

    def draw(self) -> None:
        pyxel.cls(0)

        # パレットの 16 色を番号付きで並べる
        for col in range(16):
            x = 4 + col % 8 * 19
            y = 4 + col // 8 * 16
            pyxel.rect(x, y, 16, 8, col)
            pyxel.rectb(x, y, 16, 8, 13)
            pyxel.text(x + 1, y + 9, str(col), 7)

        # 主な描画命令
        pyxel.line(8, 48, 40, 72, 8)
        pyxel.text(8, 78, "line", 7)
        pyxel.rect(48, 48, 24, 24, 11)
        pyxel.text(48, 78, "rect", 7)
        pyxel.rectb(80, 48, 24, 24, 12)
        pyxel.text(80, 78, "rectb", 7)
        pyxel.circ(124, 60, 12, 9)
        pyxel.text(116, 78, "circ", 7)
        pyxel.circb(20, 100, 10, 14)
        pyxel.text(10, 113, "circb", 7)
        pyxel.tri(48, 110, 60, 88, 72, 110, 10)
        pyxel.text(52, 113, "tri", 7)
        for i in range(8):
            pyxel.pset(84 + i * 3, 100, 7)
        pyxel.text(84, 113, "pset", 7)
        pyxel.text(116, 96, "text", pyxel.frame_count % 15 + 1)


def main() -> None:
    pyxel.init(160, 120, title="Draw Demo")
    app = App()
    pyxel.run(app.update, app.draw)


if __name__ == "__main__":
    main()
