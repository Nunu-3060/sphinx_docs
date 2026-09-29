"""ストレンジアトラクター: 単一の非線形写像を反復して得られる軌跡。

IFSのカオスゲーム（複数の変換からランダムに1つを選んで適用する）とは
違い、ここではただ1つの決定論的な写像を延々と反復するだけである。
それにもかかわらず、初期値のごくわずかな違いが反復のたびに指数的に
拡大していく「初期値鋭敏性」（カオス）を持つため、点をわずかに
ばらけた初期位置から出発させて並行に反復すると、点群全体としては
再現性のある一定の形（アトラクター）を描き出す。
"""

import numpy as np

from ifs import render_density


def clifford_attractor(
    a: float,
    b: float,
    c: float,
    d: float,
    num_points: int,
    num_steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Clifford attractor。

    x' = sin(a*y) + c*cos(a*x), y' = sin(b*x) + d*cos(b*y) を反復する。
    """
    x: np.ndarray = rng.uniform(-0.1, 0.1, size=num_points)
    y: np.ndarray = rng.uniform(-0.1, 0.1, size=num_points)
    trail: np.ndarray = np.empty((num_steps, num_points, 2), dtype=float)

    for step in range(num_steps):
        next_x: np.ndarray = np.sin(a * y) + c * np.cos(a * x)
        next_y: np.ndarray = np.sin(b * x) + d * np.cos(b * y)
        x, y = next_x, next_y
        trail[step, :, 0] = x
        trail[step, :, 1] = y

    return trail


def de_jong_attractor(
    a: float,
    b: float,
    c: float,
    d: float,
    num_points: int,
    num_steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """De Jong attractor。

    x' = sin(a*y) - cos(b*x), y' = sin(c*x) - cos(d*y) を反復する。
    """
    x: np.ndarray = rng.uniform(-0.1, 0.1, size=num_points)
    y: np.ndarray = rng.uniform(-0.1, 0.1, size=num_points)
    trail: np.ndarray = np.empty((num_steps, num_points, 2), dtype=float)

    for step in range(num_steps):
        next_x: np.ndarray = np.sin(a * y) - np.cos(b * x)
        next_y: np.ndarray = np.sin(c * x) - np.cos(d * y)
        x, y = next_x, next_y
        trail[step, :, 0] = x
        trail[step, :, 1] = y

    return trail


def _gumowski_mira_g(x: np.ndarray, mu: float) -> np.ndarray:
    return mu * x + (2.0 * (1.0 - mu) * x**2) / (1.0 + x**2)


def gumowski_mira_attractor(
    a: float,
    b: float,
    mu: float,
    num_points: int,
    num_steps: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Gumowski-Mira map。

    補助関数 ``g(x) = mu*x + 2*(1-mu)*x^2/(1+x^2)`` を使い、
    ``x' = y + a*(1 - b*y^2)*y + g(x)``、``y' = -x + g(x')``
    という写像を反復する（``x'`` は上式で求めた新しい x）。
    """
    x: np.ndarray = rng.uniform(-0.5, 0.5, size=num_points)
    y: np.ndarray = rng.uniform(-0.5, 0.5, size=num_points)
    trail: np.ndarray = np.empty((num_steps, num_points, 2), dtype=float)

    for step in range(num_steps):
        next_x: np.ndarray = y + a * (1.0 - b * y**2) * y + _gumowski_mira_g(
            x, mu
        )
        next_y: np.ndarray = -x + _gumowski_mira_g(next_x, mu)
        x, y = next_x, next_y
        trail[step, :, 0] = x
        trail[step, :, 1] = y

    return trail


def main() -> None:
    rng: np.random.Generator = np.random.default_rng(seed=0)

    clifford_trail: np.ndarray = clifford_attractor(
        a=-1.4,
        b=1.6,
        c=1.0,
        d=0.7,
        num_points=2000,
        num_steps=2000,
        rng=rng,
    )
    render_density(
        clifford_trail, height=480, color=(160, 40, 120), warmup=50
    ).save("attractor_clifford.png")

    de_jong_trail: np.ndarray = de_jong_attractor(
        a=1.4,
        b=-2.3,
        c=2.4,
        d=-2.1,
        num_points=2000,
        num_steps=2000,
        rng=rng,
    )
    render_density(
        de_jong_trail, height=480, color=(30, 100, 160), warmup=50
    ).save("attractor_de_jong.png")

    gumowski_mira_trail: np.ndarray = gumowski_mira_attractor(
        a=0.008,
        b=0.05,
        mu=-0.7,
        num_points=2000,
        num_steps=2000,
        rng=rng,
    )
    render_density(
        gumowski_mira_trail, height=480, color=(40, 130, 90), warmup=50
    ).save("attractor_gumowski_mira.png")


if __name__ == "__main__":
    main()
