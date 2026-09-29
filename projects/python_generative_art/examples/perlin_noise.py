"""NumPy を用いた自前の2Dパーリンノイズ実装。

外部のノイズ専用ライブラリには頼らず、Ken Perlin の
"Improving Noise" (2002) で示された改良版アルゴリズムを
ベクトル化して実装している。

アルゴリズムの流れ:

1. 平面を整数格子に区切り、各格子点に固定のランダムな勾配ベクトルを割り当てる
   （実際には勾配ベクトルの集合と、座標をその集合の添字に変換するための
   ハッシュ用の並び替えテーブル ``perm`` を用意する）。
2. 評価したい座標が属する格子セルの4隅について、格子点から座標までの
   変位ベクトルと勾配ベクトルの内積を取る。
3. 4つの内積値を、なめらかな補間曲線（fade関数）を使ったバイリニア補間で
   合成し、1点のノイズ値を得る。
"""

import numpy as np

# 2Dで使用する8方向の勾配ベクトル。
_GRADIENTS: np.ndarray = np.array(
    [
        [1, 1], [-1, 1], [1, -1], [-1, -1],
        [1, 0], [-1, 0], [0, 1], [0, -1],
    ],
    dtype=float,
)


def make_permutation(seed: int | None = None) -> np.ndarray:
    """0-255 をシャッフルした並び替えテーブルを、長さ512に複製して返す。

    座標を勾配ベクトルの添字に変換する際のハッシュ関数として使う。
    末尾で格子座標が +1 されてもインデックスが配列範囲を超えないよう、
    テーブルを2つ連結しておく（ラップアラウンドの簡易実装）。
    """
    rng: np.random.Generator = np.random.default_rng(seed)
    perm: np.ndarray = np.arange(256, dtype=np.int64)
    rng.shuffle(perm)
    return np.concatenate([perm, perm])


def _fade(t: np.ndarray) -> np.ndarray:
    """5次のイーズ曲線 6t^5 - 15t^4 + 10t^3 。

    両端で1階・2階微分が0になり、格子の継ぎ目が滑らかにつながる。
    """
    return t * t * t * (t * (t * 6 - 15) + 10)


def _lerp(t: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return a + t * (b - a)


def _gradient_dot(
    hash_value: np.ndarray, x: np.ndarray, y: np.ndarray
) -> np.ndarray:
    """ハッシュ値から勾配ベクトルを選び、変位ベクトル (x, y) との内積を返す。"""
    g: np.ndarray = _GRADIENTS[hash_value & 7]
    return g[..., 0] * x + g[..., 1] * y


def perlin2d(x: np.ndarray, y: np.ndarray, perm: np.ndarray) -> np.ndarray:
    """座標配列 x, y (任意の同じ形状) に対するパーリンノイズ値を返す。

    値のレンジはおおよそ -1〜1 に収まる。
    """
    xi: np.ndarray = np.floor(x).astype(np.int64) & 255
    yi: np.ndarray = np.floor(y).astype(np.int64) & 255
    xf: np.ndarray = x - np.floor(x)
    yf: np.ndarray = y - np.floor(y)

    u: np.ndarray = _fade(xf)
    v: np.ndarray = _fade(yf)

    # 格子セルの4隅のハッシュ値
    aa: np.ndarray = perm[perm[xi] + yi]
    ab: np.ndarray = perm[perm[xi] + yi + 1]
    ba: np.ndarray = perm[perm[xi + 1] + yi]
    bb: np.ndarray = perm[perm[xi + 1] + yi + 1]

    # 各隅について、勾配ベクトルと変位ベクトルの内積を計算
    x1: np.ndarray = _lerp(
        u, _gradient_dot(aa, xf, yf), _gradient_dot(ba, xf - 1, yf)
    )
    x2: np.ndarray = _lerp(
        u, _gradient_dot(ab, xf, yf - 1), _gradient_dot(bb, xf - 1, yf - 1)
    )
    return _lerp(v, x1, x2)


def fbm2d(
    x: np.ndarray,
    y: np.ndarray,
    perm: np.ndarray,
    octaves: int = 4,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
) -> np.ndarray:
    """複数のオクターブを重ね合わせた fBm (fractal Brownian motion)。

    周波数を ``lacunarity`` 倍、振幅を ``persistence`` 倍しながら
    ``octaves`` 回パーリンノイズを重ね、より複雑なディテールを加える。
    """
    total: np.ndarray = np.zeros_like(x, dtype=float)
    amplitude: float = 1.0
    frequency: float = 1.0
    max_amplitude: float = 0.0

    for _ in range(octaves):
        total += amplitude * perlin2d(x * frequency, y * frequency, perm)
        max_amplitude += amplitude
        amplitude *= persistence
        frequency *= lacunarity

    return total / max_amplitude


# 各ワープ段で q, r 用のノイズを評価する際に足しこむオフセット。
# 適当に離れた値にすることで、複数回評価するノイズどうしの相関を薄める。
_WARP_OFFSETS: np.ndarray = np.array(
    [
        [0.0, 0.0],
        [5.2, 1.3],
        [1.7, 9.2],
        [8.3, 2.8],
        [4.1, 6.6],
        [2.9, 7.4],
    ]
)


def domain_warp2d(
    x: np.ndarray,
    y: np.ndarray,
    perm: np.ndarray,
    octaves: int = 4,
    persistence: float = 0.5,
    lacunarity: float = 2.0,
    warp_strength: float = 4.0,
    iterations: int = 2,
) -> np.ndarray:
    """ドメインワーピング: fBmの評価座標そのものをノイズで歪める。

    通常の fBm ``fbm(p)`` に対し、まず座標をずらすためのベクトル場
    ``q(p) = (fbm(p + o0), fbm(p + o1))`` をノイズから作り、
    ``fbm(p + warp_strength * q(p))`` を評価する。これを繰り返し適用する
    （``iterations`` 回）ことで、格子状のfBmだけでは出せない、渦を巻いた
    ような有機的な模様が得られる（Inigo Quilez, "Domain Warping"）。
    """
    warped_x: np.ndarray = x
    warped_y: np.ndarray = y

    for i in range(iterations):
        offset_a: np.ndarray = _WARP_OFFSETS[(2 * i) % len(_WARP_OFFSETS)]
        offset_b: np.ndarray = _WARP_OFFSETS[(2 * i + 1) % len(_WARP_OFFSETS)]

        qx: np.ndarray = fbm2d(
            warped_x + offset_a[0], warped_y + offset_a[1],
            perm, octaves, persistence, lacunarity,
        )
        qy: np.ndarray = fbm2d(
            warped_x + offset_b[0], warped_y + offset_b[1],
            perm, octaves, persistence, lacunarity,
        )

        warped_x = x + warp_strength * qx
        warped_y = y + warp_strength * qy

    return fbm2d(warped_x, warped_y, perm, octaves, persistence, lacunarity)


def main() -> None:
    from PIL import Image

    width: int = 512
    height: int = 512
    scale: float = 0.02

    xs: np.ndarray
    ys: np.ndarray
    xs, ys = np.meshgrid(
        np.arange(width, dtype=float), np.arange(height, dtype=float)
    )
    perm: np.ndarray = make_permutation(seed=0)

    def save_grayscale(values: np.ndarray, path: str) -> None:
        normalized: np.ndarray = ((values + 1) / 2 * 255).clip(0, 255)
        Image.fromarray(normalized.astype(np.uint8), mode="L").save(path)

    fbm_values: np.ndarray = fbm2d(xs * scale, ys * scale, perm, octaves=5)
    save_grayscale(fbm_values, "perlin_noise.png")

    warped_values: np.ndarray = domain_warp2d(
        xs * scale, ys * scale, perm, octaves=5, warp_strength=4.0
    )
    save_grayscale(warped_values, "domain_warp.png")


if __name__ == "__main__":
    main()
