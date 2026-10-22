"""真空中の平面電磁波がマクスウェル方程式を満たすことを SymPy で確かめる.

使い方: python ch17_em_wave.py
"""

import sympy as sp

x, y, z, t = sp.symbols("x y z t", real=True)
E0, k, eps0, mu0 = sp.symbols("E_0 k epsilon_0 mu_0", positive=True)
COORDS = (x, y, z)


def div(field: sp.Matrix) -> sp.Expr:
    """ベクトル場 field（3 行 1 列）の発散を返す."""
    return sum(sp.diff(field[i], COORDS[i]) for i in range(3))


def curl(field: sp.Matrix) -> sp.Matrix:
    """ベクトル場 field（3 行 1 列）の回転を返す."""
    fx, fy, fz = field
    return sp.Matrix([
        sp.diff(fz, y) - sp.diff(fy, z),
        sp.diff(fx, z) - sp.diff(fz, x),
        sp.diff(fy, x) - sp.diff(fx, y),
    ])


def report() -> None:
    """z 方向に進む平面波を代入し、マクスウェル方程式の各式の「左辺 - 右辺」を表示する."""
    c = 1 / sp.sqrt(eps0 * mu0)  # 光速
    omega = c * k  # 角周波数（分散関係 omega = c k）
    phase = k * z - omega * t
    e_field = sp.Matrix([E0 * sp.sin(phase), 0, 0])
    b_field = sp.Matrix([0, E0 / c * sp.sin(phase), 0])

    print("div E =", sp.simplify(div(e_field)))
    print("div B =", sp.simplify(div(b_field)))
    print("rot E + dB/dt =", sp.simplify(curl(e_field) + sp.diff(b_field, t)).T)
    print("rot B - mu0 eps0 dE/dt =", sp.simplify(curl(b_field) - mu0 * eps0 * sp.diff(e_field, t)).T)

    # 電場の x 成分が波動方程式を満たすことも確かめる
    ex = e_field[0]
    wave = sp.diff(ex, x, 2) + sp.diff(ex, y, 2) + sp.diff(ex, z, 2) - mu0 * eps0 * sp.diff(ex, t, 2)
    print("波動方程式の左辺 =", sp.simplify(wave))


def main() -> None:
    report()


if __name__ == "__main__":
    main()
