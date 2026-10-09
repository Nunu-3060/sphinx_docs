"""相関係数と散布図の形.

相関係数 r の異なる 4 組のデータと、r がほぼ 0 でも強い関係を持つ
2 組のデータを散布図で描く。

使い方: python ch05_correlation.py
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

import jpfont

SIZE = 200


def correlated(rng: np.random.Generator,
               rho: float) -> tuple[np.ndarray, np.ndarray]:
    """相関係数がおよそ rho になる 2 変数のデータを作る."""
    x = rng.normal(0, 1, SIZE)
    y = rho * x + np.sqrt(1 - rho ** 2) * rng.normal(0, 1, SIZE)
    return x, y


def create_figure() -> Figure:
    """6 組のデータの散布図を、相関係数とともに描く."""
    rng = np.random.default_rng(7)
    datasets = [correlated(rng, rho) for rho in (0.95, 0.6, 0.0, -0.8)]
    # 2 次関数の関係（r はほぼ 0）
    x = rng.uniform(-2, 2, SIZE)
    datasets.append((x, x ** 2 + rng.normal(0, 0.2, SIZE)))
    # 円周上の関係（r はほぼ 0）
    theta = rng.uniform(0, 2 * np.pi, SIZE)
    datasets.append((np.cos(theta) + rng.normal(0, 0.05, SIZE),
                     np.sin(theta) + rng.normal(0, 0.05, SIZE)))

    fig, axes = plt.subplots(2, 3, figsize=(9, 5.5))
    for ax, (x, y) in zip(axes.flat, datasets):
        r = np.corrcoef(x, y)[0, 1]
        ax.scatter(x, y, s=8, color="C0", alpha=0.6)
        ax.set_title(f"r = {r:.2f}")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    return fig


def main() -> None:
    jpfont.setup()
    create_figure()
    plt.show()


if __name__ == "__main__":
    main()
