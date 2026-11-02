"""状態を持たない乱数（ハッシュ関数）。

整数の座標とシードから、決まった 32 bit の整数を返す。同じ入力には必ず同じ値を
返すので、どの順番で、どの場所から評価しても結果が変わらない。GLSL のシェーダーでも
同じ式をそのまま使える（examples/glsl の各ファイルを参照）。
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike

from common import FloatArray, UIntArray


def to_uint32(values: ArrayLike) -> UIntArray:
    """負の数を含む整数を、下位 32 bit を残して符号なし 32 bit 整数にする。"""
    return (np.asarray(values, dtype=np.int64) & 0xFFFFFFFF).astype(np.uint32)


def hash_u32(values: ArrayLike) -> UIntArray:
    """32 bit 整数を混ぜ合わせる関数（PCG ハッシュ。Jarzynski と Olano による）。

    線形合同法で 1 歩進めた値を、値そのものに応じた量だけシフトして混ぜる。
    入力が 1 違うだけでも、出力は無関係に見える値になる。
    """
    x = to_uint32(values)
    # 桁あふれした上位の bit を捨て、下位 32 bit だけを残すのが意図どおりの動作なので、警告を出さない。
    with np.errstate(over="ignore"):
        state = x * np.uint32(747796405) + np.uint32(2891336453)
        word = ((state >> ((state >> 28) + np.uint32(4))) ^ state) * np.uint32(277803737)
        result = ((word >> 22) ^ word).astype(np.uint32)
    return result


def hash2(ix: ArrayLike, iy: ArrayLike, seed: int = 0) -> UIntArray:
    """2 次元の整数座標とシードから 32 bit のハッシュ値を作る。"""
    with np.errstate(over="ignore"):
        h = hash_u32(to_uint32(seed))
        h = hash_u32(to_uint32(iy) + h)
        return hash_u32(to_uint32(ix) + h)


def hash3(ix: ArrayLike, iy: ArrayLike, iz: ArrayLike, seed: int = 0) -> UIntArray:
    """3 次元の整数座標とシードから 32 bit のハッシュ値を作る。"""
    with np.errstate(over="ignore"):
        h = hash_u32(to_uint32(seed))
        h = hash_u32(to_uint32(iz) + h)
        h = hash_u32(to_uint32(iy) + h)
        return hash_u32(to_uint32(ix) + h)


def to_unit(h: UIntArray) -> FloatArray:
    """32 bit のハッシュ値を 0 以上 1 未満の実数にする。"""
    return h.astype(np.float64) / 4294967296.0


def random2(ix: ArrayLike, iy: ArrayLike, seed: int = 0) -> FloatArray:
    """整数座標ごとに決まる、0 以上 1 未満の乱数。"""
    return to_unit(hash2(ix, iy, seed))


def random3(ix: ArrayLike, iy: ArrayLike, iz: ArrayLike, seed: int = 0) -> FloatArray:
    """3 次元の整数座標ごとに決まる、0 以上 1 未満の乱数。"""
    return to_unit(hash3(ix, iy, iz, seed))
