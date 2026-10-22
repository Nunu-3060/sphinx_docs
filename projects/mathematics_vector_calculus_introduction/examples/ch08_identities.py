"""ナブラを含む公式が成り立つことを、SymPy の記号計算で確かめる.

使い方: python ch08_identities.py
"""

import sympy as sp

import vc_plot

x, y, z = sp.symbols("x y z")
Vec = tuple[sp.Expr, sp.Expr, sp.Expr]


def grad(f: sp.Expr) -> Vec:
    """スカラー場 f の勾配."""
    return (sp.diff(f, x), sp.diff(f, y), sp.diff(f, z))


def div(a: Vec) -> sp.Expr:
    """ベクトル場 a の発散."""
    return sp.diff(a[0], x) + sp.diff(a[1], y) + sp.diff(a[2], z)


def curl(a: Vec) -> Vec:
    """ベクトル場 a の回転."""
    return (sp.diff(a[2], y) - sp.diff(a[1], z),
            sp.diff(a[0], z) - sp.diff(a[2], x),
            sp.diff(a[1], x) - sp.diff(a[0], y))


def laplacian(a: Vec) -> Vec:
    """ベクトル場 a のラプラシアン（直交座標では成分ごとのラプラシアン）."""
    return tuple(div(grad(c)) for c in a)


def dot(a: Vec, b: Vec) -> sp.Expr:
    """内積 a . b."""
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a: Vec, b: Vec) -> Vec:
    """外積 a x b."""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def directional(a: Vec, b: Vec) -> Vec:
    """(a . nabla) b：b の各成分を、a の向きに a の大きさを掛けて方向微分したもの."""
    return tuple(a[0] * sp.diff(c, x) + a[1] * sp.diff(c, y) + a[2] * sp.diff(c, z)
                 for c in b)


def add(*vectors: Vec) -> Vec:
    """ベクトルの和."""
    return tuple(sum(c, sp.Integer(0)) for c in zip(*vectors))


def scale(k: sp.Expr, a: Vec) -> Vec:
    """スカラー倍 k a."""
    return (k * a[0], k * a[1], k * a[2])


def is_zero(expr: sp.Expr | Vec) -> bool:
    """式（またはベクトルのすべての成分）を展開して 0 になるかを調べる."""
    parts = expr if isinstance(expr, tuple) else (expr,)
    return all(sp.expand(p) == 0 for p in parts)


def report() -> None:
    """任意のスカラー場 f, g と任意のベクトル場 F, G について、公式の両辺の差が 0 になるかを表示する."""
    f = sp.Function("f")(x, y, z)
    g = sp.Function("g")(x, y, z)
    big_f: Vec = tuple(sp.Function(f"F_{c}")(x, y, z) for c in "xyz")
    big_g: Vec = tuple(sp.Function(f"G_{c}")(x, y, z) for c in "xyz")
    minus = sp.Integer(-1)

    checks: list[tuple[str, sp.Expr | Vec]] = [
        ("grad(fg) = f grad g + g grad f",
         add(grad(f * g), scale(minus, add(scale(f, grad(g)), scale(g, grad(f)))))),
        ("div(fF) = grad f . F + f div F",
         div(scale(f, big_f)) - dot(grad(f), big_f) - f * div(big_f)),
        ("rot(fF) = grad f x F + f rot F",
         add(curl(scale(f, big_f)), scale(minus, add(cross(grad(f), big_f), scale(f, curl(big_f)))))),
        ("div(F x G) = G . rot F - F . rot G",
         div(cross(big_f, big_g)) - dot(big_g, curl(big_f)) + dot(big_f, curl(big_g))),
        ("rot(F x G) = F div G - G div F + (G . nabla)F - (F . nabla)G",
         add(curl(cross(big_f, big_g)),
             scale(minus, add(scale(div(big_g), big_f), scale(-div(big_f), big_g),
                              directional(big_g, big_f), scale(minus, directional(big_f, big_g)))))),
        ("grad(F . G) = (F . nabla)G + (G . nabla)F + F x rot G + G x rot F",
         add(grad(dot(big_f, big_g)),
             scale(minus, add(directional(big_f, big_g), directional(big_g, big_f),
                              cross(big_f, curl(big_g)), cross(big_g, curl(big_f)))))),
        ("rot(grad f) = 0", curl(grad(f))),
        ("div(rot F) = 0", div(curl(big_f))),
        ("rot(rot F) = grad(div F) - laplacian F",
         add(curl(curl(big_f)), scale(minus, add(grad(div(big_f)), scale(minus, laplacian(big_f)))))),
    ]
    for name, difference in checks:
        result = "成り立つ" if is_zero(difference) else "成り立たない"
        print(f"{name:66s} {result}")


def main() -> None:
    vc_plot.setup_font()
    report()


if __name__ == "__main__":
    main()
