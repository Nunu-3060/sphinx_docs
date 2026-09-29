"""マンデルブロ集合・ジュリア集合の脱出時間アルゴリズム（NumPyでベクトル化）。

どちらも漸化式

    z_{n+1} = z_n^2 + c

を繰り返し適用し、``|z|`` がある閾値を超えて発散するまでの反復回数
（脱出時間）を画像の各画素に対応させて描画する。マンデルブロ集合と
ジュリア集合の違いは、この式のどちらを画素座標に対応させるかだけ。

- マンデルブロ集合: ``z0 = 0`` に固定し、``c`` を複素平面上の各画素の
  座標として走査する。
- ジュリア集合: ``c`` を1つの定数に固定し、``z0`` を複素平面上の各画素の
  座標として走査する。

ループ自体はPythonのfor文で回すが、各反復で行う計算は「まだ発散して
いない画素」全体に対するNumPy配列演算であり、画素ごとのPythonループは
発生しない（ブールマスクで発散済みの画素を以降の更新から除外する）。
"""

import numpy as np
from matplotlib import colormaps
from PIL import Image


def _escape_time(
    c: np.ndarray,
    z0: np.ndarray,
    max_iter: int,
    bailout: float = 2.0,
) -> np.ndarray:
    """漸化式 z_{n+1} = z_n^2 + c を反復し、各画素の脱出時間を返す。

    発散しなかった画素（集合の内部）には ``max_iter`` を割り当てる。
    """
    z: np.ndarray = z0.copy()
    iterations: np.ndarray = np.zeros(c.shape, dtype=np.int64)
    active: np.ndarray = np.ones(c.shape, dtype=bool)

    for i in range(max_iter):
        z[active] = z[active] ** 2 + c[active]
        escaped: np.ndarray = active & (np.abs(z) > bailout)
        iterations[escaped] = i
        active &= ~escaped
        if not active.any():
            break

    iterations[active] = max_iter
    return iterations


def _complex_grid(
    width: int,
    height: int,
    re_range: tuple[float, float],
    im_range: tuple[float, float],
) -> np.ndarray:
    re: np.ndarray = np.linspace(re_range[0], re_range[1], width)
    im: np.ndarray = np.linspace(im_range[0], im_range[1], height)
    re_grid: np.ndarray
    im_grid: np.ndarray
    re_grid, im_grid = np.meshgrid(re, im)
    return re_grid + 1j * im_grid


def mandelbrot_escape(
    width: int,
    height: int,
    re_range: tuple[float, float] = (-2.0, 0.7),
    im_range: tuple[float, float] = (-1.2, 1.2),
    max_iter: int = 200,
) -> np.ndarray:
    """マンデルブロ集合の脱出時間配列 (height, width) を返す。

    画素座標を ``c`` として使い、``z0 = 0`` から反復する。
    """
    c: np.ndarray = _complex_grid(width, height, re_range, im_range)
    z0: np.ndarray = np.zeros_like(c)
    return _escape_time(c, z0, max_iter)


def julia_escape(
    c_value: complex,
    width: int,
    height: int,
    re_range: tuple[float, float] = (-1.5, 1.5),
    im_range: tuple[float, float] = (-1.5, 1.5),
    max_iter: int = 200,
) -> np.ndarray:
    """ジュリア集合の脱出時間配列 (height, width) を返す。

    マンデルブロ集合とは役割が逆になり、``c`` は定数 ``c_value`` に
    固定し、画素座標を初期値 ``z0`` として反復する。
    """
    z0: np.ndarray = _complex_grid(width, height, re_range, im_range)
    c: np.ndarray = np.full(z0.shape, c_value, dtype=complex)
    return _escape_time(c, z0, max_iter)


def render_image(
    iterations: np.ndarray,
    max_iter: int,
    path: str,
    cmap_name: str = "inferno",
) -> None:
    """脱出時間配列をカラーマップで着色し、PNGとして保存する。

    反復回数をそのまま使うと外周の色変化が急なので、平方根を取って
    階調を引き伸ばす。集合の内部（発散しなかった画素）は黒で塗る。
    """
    normalized: np.ndarray = np.sqrt(iterations / max_iter)
    cmap = colormaps[cmap_name]
    rgba: np.ndarray = cmap(normalized)
    rgb: np.ndarray = (rgba[..., :3] * 255).astype(np.uint8)

    interior: np.ndarray = iterations >= max_iter
    rgb[interior] = 0

    Image.fromarray(rgb, mode="RGB").save(path)


def main() -> None:
    width: int = 800
    height: int = 640
    max_iter: int = 200

    mandelbrot_iters: np.ndarray = mandelbrot_escape(
        width, height, max_iter=max_iter
    )
    render_image(mandelbrot_iters, max_iter, "mandelbrot.png")

    julia_iters: np.ndarray = julia_escape(
        complex(-0.7, 0.27015), width, height, max_iter=max_iter
    )
    render_image(
        julia_iters, max_iter, "julia.png", cmap_name="twilight_shifted"
    )


if __name__ == "__main__":
    main()
