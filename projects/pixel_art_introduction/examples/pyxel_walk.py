"""スプライトシートを Pyxel で読み込み、歩行アニメーションを再生する。

先に sprite_sheet.py を実行して output/hero_walk_sheet.png を作っておくこと。
Esc キーで終了する。

使い方::

    python sprite_sheet.py
    python pyxel_walk.py
"""

from pathlib import Path

import pyxel

SHEET_PATH = Path("output/hero_walk_sheet.png")
FRAME_SIZE = 16     # 1 フレームの幅と高さ（ピクセル）
FRAME_COUNT = 4     # フレーム数
FRAME_TICKS = 5     # 1 フレームを表示する期間（30 fps なので 5 / 30 秒）
BACKGROUND = 0xE8ECF0


class App:
    def __init__(self) -> None:
        pyxel.init(64, 40, title="Walk", fps=30)
        # include_colors=True にすると、画像の色がそのまま Pyxel のパレットになる。
        # 透明ピクセルはパレットの 0 番（黒）になるので、描画時に colkey=0 で透過させる。
        self.sheet = pyxel.Image.from_image(str(SHEET_PATH), include_colors=True)
        pyxel.colors.append(BACKGROUND)
        self.background = len(pyxel.colors) - 1
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        pass

    def draw(self) -> None:
        pyxel.cls(self.background)
        frame = (pyxel.frame_count // FRAME_TICKS) % FRAME_COUNT
        # 上段：アニメーション、下段：スプライトシート全体
        pyxel.blt(24, 2, self.sheet, frame * FRAME_SIZE, 0, FRAME_SIZE, FRAME_SIZE, colkey=0)
        pyxel.blt(0, 22, self.sheet, 0, 0, FRAME_SIZE * FRAME_COUNT, FRAME_SIZE, colkey=0)


def main() -> None:
    if not SHEET_PATH.exists():
        raise SystemExit(f"{SHEET_PATH} が無い。先に sprite_sheet.py を実行すること。")
    App()


if __name__ == "__main__":
    main()
