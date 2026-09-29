"""静止画の生成コードからアニメーション GIF を書き出す。

本資料の作例は、どれも「パラメータや状態を受け取って 1 枚の画像を返す
関数」として書かれている。これを時刻ごとに繰り返し呼び出して得た
画像の列(フレーム)を順に並べれば、そのままアニメーションになる。
ここでは Pillow の GIF 書き出し機能だけを使い、次の 2 通りの作り方を示す。

- 状態を 1 ステップずつ更新し、各ステップの状態を 1 フレームにする
  (ライフゲームの世代の進行)。
- 時刻 ``t`` をパラメータとして描画関数に渡し、``t`` を 1 周期分
  動かす(リサージュ曲線の位相の変化)。
"""

import math

import numpy as np
from PIL import Image

from automata import render_grid, simulate_life
from lissajous import lissajous_points
from spirograph import render_curve


def save_gif(
    frames: list[Image.Image], path: str, frame_duration_ms: int = 50
) -> None:
    """フレームの列をアニメーション GIF として保存する。

    ``loop=0`` は無限に繰り返すことを表す。GIF は 256 色までしか
    扱えないため、各フレームはパレット形式 ("P") に変換してから渡す。
    """
    palette_frames: list[Image.Image] = [
        frame.convert("P", palette=Image.Palette.ADAPTIVE) for frame in frames
    ]
    palette_frames[0].save(
        path,
        save_all=True,
        append_images=palette_frames[1:],
        duration=frame_duration_ms,
        loop=0,
    )


def life_frames(
    grid_size: int = 90, num_steps: int = 120, scale: int = 3, seed: int = 2
) -> list[Image.Image]:
    """ライフゲームを世代ごとに描いたフレームの列を作る。

    ``simulate_life`` が返す履歴の 1 世代分を、そのまま 1 フレームとして
    描画する。静止画の作例 (``render_life_trail``) が同じ履歴を
    1 枚に重ね合わせていたのに対し、こちらは時間方向に並べる。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    initial: np.ndarray = rng.random((grid_size, grid_size)) < 0.25
    history: np.ndarray = simulate_life(initial, num_steps)
    size: tuple[int, int] = (grid_size * scale, grid_size * scale)
    return [
        render_grid(grid).resize(size, resample=Image.Resampling.NEAREST)
        for grid in history
    ]


def lissajous_loop_frames(
    num_frames: int = 60, size: int = 240
) -> list[Image.Image]:
    """位相を 1 周期分ずらしながら描いたリサージュ曲線のフレームの列を作る。

    位相は ``2*pi`` を周期とするため、最後のフレームの次に最初の
    フレームへ戻っても変化がなめらかにつながり、継ぎ目のない
    ループアニメーションになる。
    """
    frames: list[Image.Image] = []
    for index in range(num_frames):
        t: float = index / num_frames
        phase: float = 2.0 * math.pi * t
        points: np.ndarray = lissajous_points(
            freq_x=3, freq_y=2, phase=phase, num_points=1000
        )
        frames.append(
            render_curve(points, size, size, color=(60, 120, 180))
        )
    return frames


def main() -> None:
    save_gif(life_frames(), "animation_life.gif", frame_duration_ms=80)
    save_gif(lissajous_loop_frames(), "animation_lissajous.gif")


if __name__ == "__main__":
    main()
