"""リサージュ曲線とハーモノグラフ。

x軸・y軸それぞれに異なる周波数の正弦振動を与えると、その軌跡は
周波数比に応じて様々な閉曲線 (**リサージュ曲線**) を描く。振幅が
時間とともに指数的に減衰する効果を加えると、実際に2つの振り子を
直交させてペン先の軌跡を記録する「ハーモノグラフ」という装置と
同じ軌跡が再現できる。
"""

import math

import numpy as np

from spirograph import render_curve


def lissajous_points(
    freq_x: float,
    freq_y: float,
    phase: float,
    num_points: int,
    revolutions: float = 1.0,
    amplitude: float = 1.0,
) -> np.ndarray:
    """リサージュ曲線
    :math:`x = \\sin(f_x t + \\phi)`, :math:`y = \\sin(f_y t)` 上の点列。

    ``freq_x`` / ``freq_y`` が整数比であれば、``t`` が ``2*pi`` だけ
    進む間に曲線はちょうど1周して閉じる。
    """
    t: np.ndarray = np.linspace(
        0.0, 2.0 * math.pi * revolutions, num_points
    )
    x: np.ndarray = amplitude * np.sin(freq_x * t + phase)
    y: np.ndarray = amplitude * np.sin(freq_y * t)
    return np.stack([x, y], axis=-1)


def harmonograph_points(
    freq_x: float,
    freq_y: float,
    phase: float,
    damping: float,
    num_points: int,
    duration: float,
) -> np.ndarray:
    """振幅が指数的に減衰するリサージュ曲線(ハーモノグラフ)の軌跡。

    ``damping`` が大きいほど早く振幅が小さくなり、渦を巻きながら
    中心に収束していく軌跡になる。周波数をわずかに整数比からずらす
    (例えば3ではなく3.01にする) と、実際の振り子が持つわずかな
    誤差を模した、より有機的な軌跡になる。
    """
    t: np.ndarray = np.linspace(0.0, duration, num_points)
    envelope: np.ndarray = np.exp(-damping * t)
    x: np.ndarray = envelope * np.sin(freq_x * t + phase)
    y: np.ndarray = envelope * np.sin(freq_y * t)
    return np.stack([x, y], axis=-1)


def main() -> None:
    width: int = 480
    height: int = 480

    lissajous: np.ndarray = lissajous_points(
        freq_x=3, freq_y=2, phase=math.pi / 2.0, num_points=2000
    )
    render_curve(lissajous, width, height, color=(60, 120, 180)).save(
        "lissajous.png"
    )

    harmonograph: np.ndarray = harmonograph_points(
        freq_x=3.01,
        freq_y=2.0,
        phase=math.pi / 2.0,
        damping=0.02,
        num_points=6000,
        duration=80.0,
    )
    render_curve(harmonograph, width, height, color=(140, 70, 150)).save(
        "harmonograph.png"
    )


if __name__ == "__main__":
    main()
