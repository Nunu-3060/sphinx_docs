"""サンプルゲームをヘッドレスモードで自動操作し、指定したフレームの画面を PNG で保存する。

使い方:
    python capture.py SCRIPT OUTPUT_PREFIX FRAME [FRAME ...] [--idle] [--mortal]

SCRIPT (ディレクトリを指定した場合はその中の main.py) を読み込み、App を生成して 1 フレームずつ進める。
既定では自機は弾を撃ちながら左右に動き続け、残機は減らない (撮影用)。
--idle を付けると何も入力しない (タイトル画面の撮影用)。
--mortal を付けると残機を補充しない (ゲームオーバー画面の撮影用)。
--passive を付けるとゲーム開始のキーだけを押し、自機を操作しない (--mortal と併用する)。
"""

import argparse
import importlib.util
from pathlib import Path
from types import ModuleType

import pyxel

ASSETS = Path(__file__).resolve().parents[2] / "examples" / "assets" / "cosmo_rush.pyxres"


def load_game(script: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("game_main", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_key_states: dict[int, bool] = {}


def set_key(key: int, state: bool) -> None:
    """キーの状態が変わったときだけ set_btn() を呼ぶ (毎回呼ぶと押し直しと見なされる)。"""
    if _key_states.get(key, False) != state:
        pyxel.set_btn(key, state)
        _key_states[key] = state


def press(frame: int, idle: bool, passive: bool) -> None:
    if idle:
        return
    if passive:
        set_key(pyxel.KEY_SPACE, frame == 5)
        return
    set_key(pyxel.KEY_SPACE, frame % 40 > 2)
    set_key(pyxel.KEY_Z, frame % 40 > 2)
    go_left = (frame // 45) % 2 == 0
    set_key(pyxel.KEY_LEFT, go_left)
    set_key(pyxel.KEY_RIGHT, not go_left)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("script")
    parser.add_argument("prefix")
    parser.add_argument("frames", nargs="+", type=int)
    parser.add_argument("--idle", action="store_true")
    parser.add_argument("--mortal", action="store_true")
    parser.add_argument("--passive", action="store_true")
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    script = Path(args.script).resolve()
    if script.is_dir():
        script = script / "main.py"
    game = load_game(script)
    width = getattr(game, "SCREEN_W", 160)
    height = getattr(game, "SCREEN_H", 120)
    pyxel.init(width, height, headless=True)
    if hasattr(game, "RESOURCE_FILE"):
        pyxel.load(str(ASSETS))
    pyxel.rseed(args.seed)
    app = game.App()
    last = max(args.frames)
    for frame in range(last + 1):
        press(frame, args.idle, args.passive)
        app.update()
        target = getattr(app, "scene", app)
        if not args.mortal and 0 < getattr(target, "lives", 0) < 3:
            target.lives = 3
        app.draw()
        if frame in args.frames:
            pyxel.screen.save(f"{args.prefix}_{frame}", 2)
        pyxel.flip()


if __name__ == "__main__":
    main()
