"""反応拡散系 (Gray-Scott モデル) による有機的な模様の生成。

セルオートマトンが「離散的な状態(生/死など)を持つ格子」を扱うのに
対し、反応拡散系は「連続的な濃度を持つ格子」を扱う。2つの化学物質
U・Vが格子上を拡散しながら、Vが自分自身を複製してUを消費する
反応を起こすと、条件次第でヒョウ柄・サンゴ状・迷路状といった、
生物の模様によく似た自己組織化パターンが現れる。
"""

import numpy as np
from PIL import Image


def laplacian(field: np.ndarray) -> np.ndarray:
    """5点ステンシルによる離散ラプラシアン(周期境界)。

    上下左右の隣接セルとの差の合計であり、値がまわりより低い場所
    ほど正、高い場所ほど負になる、拡散の向きと強さを表す量になる。
    """
    return (
        np.roll(field, 1, axis=0)
        + np.roll(field, -1, axis=0)
        + np.roll(field, 1, axis=1)
        + np.roll(field, -1, axis=1)
        - 4.0 * field
    )


def gray_scott_step(
    u: np.ndarray,
    v: np.ndarray,
    feed: float,
    kill: float,
    diffusion_u: float = 0.16,
    diffusion_v: float = 0.08,
    dt: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Gray-Scottモデルによる反応拡散を1ステップ分進める。

    U はどこにでも一定の割合 ``feed`` で補充され続け、V は
    ``feed + kill`` の割合で取り除かれ続ける。U と V が同じ場所に
    あるとVがUを消費して自分を複製する(``u * v**2`` の反応項)ため、
    Vが少し存在する場所を種にして模様が広がっていく。
    """
    reaction: np.ndarray = u * v * v
    next_u: np.ndarray = (
        u + (diffusion_u * laplacian(u) - reaction + feed * (1.0 - u)) * dt
    )
    next_v: np.ndarray = (
        v + (diffusion_v * laplacian(v) + reaction - (feed + kill) * v) * dt
    )
    return next_u, next_v


def simulate_gray_scott(
    width: int,
    height: int,
    feed: float,
    kill: float,
    num_steps: int,
    rng: np.random.Generator,
    num_seeds: int = 12,
    seed_radius: int = 6,
) -> np.ndarray:
    """一様なU場にVの種を複数箇所ランダムに撒き、num_steps ステップ反復する。

    種を1箇所だけに置くと、模様が完全に対称なまま育ってしまい、
    パラメータによっては単一の安定した塊で成長が止まってしまう
    ことがある。ランダムな位置に複数の種を撒くことで対称性を崩し、
    パラメータ本来の模様（迷路状・水玉状・ミミズ状など）が
    キャンバス全体に広がりやすくなる。戻り値は最終ステップの V 場
    （形状 ``(height, width)``）。
    """
    u: np.ndarray = np.ones((height, width), dtype=float)
    v: np.ndarray = np.zeros((height, width), dtype=float)

    for _ in range(num_seeds):
        cy: int = int(rng.integers(seed_radius, height - seed_radius))
        cx: int = int(rng.integers(seed_radius, width - seed_radius))
        y0: int = cy - seed_radius
        y1: int = cy + seed_radius
        x0: int = cx - seed_radius
        x1: int = cx + seed_radius
        v[y0:y1, x0:x1] = 1.0
        u[y0:y1, x0:x1] = 0.5

    v = np.clip(v + rng.uniform(-0.05, 0.05, size=v.shape), 0.0, 1.0)

    for _ in range(num_steps):
        u, v = gray_scott_step(u, v, feed, kill)

    return v


def render_field(
    field: np.ndarray, color: tuple[int, int, int] = (20, 90, 140)
) -> Image.Image:
    """濃度場を、最小値を白・最大値を指定色とした濃淡画像に変換する。"""
    field_min: float = float(field.min())
    field_max: float = float(field.max())
    span: float = field_max - field_min
    normalized: np.ndarray = (
        (field - field_min) / span if span > 0 else np.zeros_like(field)
    )

    background: np.ndarray = np.full(field.shape + (3,), 255.0)
    fg: np.ndarray = np.array(color, dtype=float)
    pixels: np.ndarray = (
        background + (fg - background) * normalized[..., np.newaxis]
    )
    return Image.fromarray(pixels.round().astype(np.uint8))


def main() -> None:
    width: int = 200
    height: int = 200
    rng: np.random.Generator = np.random.default_rng(seed=0)

    # feed(補充率)・kill(除去率)の組み合わせで模様のタイプが変わる。
    presets: dict[str, tuple[float, float, tuple[int, int, int]]] = {
        "coral": (0.0545, 0.062, (20, 90, 140)),
        "mitosis": (0.0367, 0.0649, (140, 40, 90)),
        "worms": (0.078, 0.061, (30, 110, 60)),
    }

    for name, (feed, kill, color) in presets.items():
        v_field: np.ndarray = simulate_gray_scott(
            width,
            height,
            feed,
            kill,
            num_steps=20000,
            rng=rng,
            num_seeds=30,
            seed_radius=5,
        )
        path: str = f"reaction_diffusion_{name}.png"
        render_field(v_field, color=color).save(path)


if __name__ == "__main__":
    main()
