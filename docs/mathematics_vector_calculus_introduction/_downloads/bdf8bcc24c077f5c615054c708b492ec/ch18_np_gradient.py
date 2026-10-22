"""格子上の値から、差分で発散・回転・ラプラシアンを求め、厳密な値と比べる.

使い方: python ch18_np_gradient.py
"""

import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]


def divergence(fx: Array, fy: Array, dx: float, dy: float) -> Array:
    """2 次元のベクトル場 (fx, fy) の発散. 配列の軸 0 が y、軸 1 が x に対応する."""
    dfx_dx = np.gradient(fx, dx, axis=1, edge_order=2)
    dfy_dy = np.gradient(fy, dy, axis=0, edge_order=2)
    return dfx_dx + dfy_dy


def curl_z(fx: Array, fy: Array, dx: float, dy: float) -> Array:
    """2 次元のベクトル場 (fx, fy) の回転の z 成分 dFy/dx - dFx/dy."""
    dfy_dx = np.gradient(fy, dx, axis=1, edge_order=2)
    dfx_dy = np.gradient(fx, dy, axis=0, edge_order=2)
    return dfy_dx - dfx_dy


def laplacian(f: Array, dx: float, dy: float) -> Array:
    """5 点差分によるラプラシアン. 外周の格子点では求めず 0 とする."""
    lap = np.zeros_like(f)
    lap[1:-1, 1:-1] = ((f[1:-1, 2:] - 2.0 * f[1:-1, 1:-1] + f[1:-1, :-2]) / dx**2
                       + (f[2:, 1:-1] - 2.0 * f[1:-1, 1:-1] + f[:-2, 1:-1]) / dy**2)
    return lap


def max_errors(n: int) -> tuple[float, float, float]:
    """[0, 2] x [0, 2] を n x n の格子に分けたときの、発散・回転・ラプラシアンの最大誤差を返す."""
    x = np.linspace(0.0, 2.0, n)
    y = np.linspace(0.0, 2.0, n)
    xx, yy = np.meshgrid(x, y)  # xx[i, j] = x[j], yy[i, j] = y[i]
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    # F = (sin x cos y, sin x sin y)、f = sin x cos y
    fx = np.sin(xx) * np.cos(yy)
    fy = np.sin(xx) * np.sin(yy)
    div_exact = np.cos(xx) * np.cos(yy) + np.sin(xx) * np.cos(yy)
    curl_exact = np.cos(xx) * np.sin(yy) + np.sin(xx) * np.sin(yy)
    lap_exact = -2.0 * fx

    err_div = np.max(np.abs(divergence(fx, fy, dx, dy) - div_exact))
    err_curl = np.max(np.abs(curl_z(fx, fy, dx, dy) - curl_exact))
    inner = (slice(1, -1), slice(1, -1))
    err_lap = np.max(np.abs(laplacian(fx, dx, dy)[inner] - lap_exact[inner]))
    return float(err_div), float(err_curl), float(err_lap)


def report() -> None:
    """格子を細かくしていったときの最大誤差を表にする."""
    print("   n   発散の誤差   回転の誤差   ラプラシアンの誤差")
    for n in (21, 41, 81, 161):
        e_div, e_curl, e_lap = max_errors(n)
        print(f"{n:4d}  {e_div:11.3e}  {e_curl:11.3e}  {e_lap:11.3e}")


def main() -> None:
    report()


if __name__ == "__main__":
    main()
