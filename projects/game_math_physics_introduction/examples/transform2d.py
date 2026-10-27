"""第 6 章: 同次座標を使った 2 次元のアフィン変換の行列 Mat3。

3 行 3 列の行列のうち、最後の行は常に (0, 0, 1) なので、上の 2 行の 6 つの値だけを持つ。

    | a  b  c |   | x |   | a*x + b*y + c |
    | d  e  f | @ | y | = | d*x + e*y + f |
    | 0  0  1 |   | 1 |   |       1       |

arm_demo.py と camera_demo.py から import して使う。

実行方法（変換の順序による違いを表示する）:
    py transform2d.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Mat3:
    """2 次元のアフィン変換を表す 3×3 行列。"""

    a: float = 1.0
    b: float = 0.0
    c: float = 0.0
    d: float = 0.0
    e: float = 1.0
    f: float = 0.0

    @staticmethod
    def translation(tx: float, ty: float) -> Mat3:
        """平行移動。"""
        return Mat3(1, 0, tx, 0, 1, ty)

    @staticmethod
    def rotation(angle: float) -> Mat3:
        """原点を中心とする回転（angle はラジアン）。"""
        c, s = math.cos(angle), math.sin(angle)
        return Mat3(c, -s, 0, s, c, 0)

    @staticmethod
    def scaling(sx: float, sy: float) -> Mat3:
        """原点を中心とする拡大縮小。"""
        return Mat3(sx, 0, 0, 0, sy, 0)

    def __matmul__(self, other: Mat3) -> Mat3:
        """行列の積 self @ other。点に適用すると、other を先に、self を後に適用したことになる。"""
        return Mat3(
            self.a * other.a + self.b * other.d,
            self.a * other.b + self.b * other.e,
            self.a * other.c + self.b * other.f + self.c,
            self.d * other.a + self.e * other.d,
            self.d * other.b + self.e * other.e,
            self.d * other.c + self.e * other.f + self.f,
        )

    def apply(self, x: float, y: float) -> tuple[float, float]:
        """点 (x, y) を変換する。"""
        return self.a * x + self.b * y + self.c, self.d * x + self.e * y + self.f

    def apply_vector(self, x: float, y: float) -> tuple[float, float]:
        """向き (x, y) を変換する。向きは位置を持たないので、平行移動の成分は使わない（同次座標の 3 番目が 0）。"""
        return self.a * x + self.b * y, self.d * x + self.e * y

    def inverse(self) -> Mat3:
        """逆行列。拡大率が 0 の変換（行列式が 0）には逆行列が無い。"""
        det = self.a * self.e - self.b * self.d
        if abs(det) < 1e-12:
            raise ValueError('この変換には逆変換が無い')
        ia, ib = self.e / det, -self.b / det
        id_, ie = -self.d / det, self.a / det
        return Mat3(ia, ib, -(ia * self.c + ib * self.f), id_, ie, -(id_ * self.c + ie * self.f))


def main() -> None:
    point = (10.0, 0.0)
    rotate = Mat3.rotation(math.radians(90))
    move = Mat3.translation(100, 0)
    # 行列は右から順に適用される
    print('回転してから移動 (move @ rotate):', (move @ rotate).apply(*point))
    print('移動してから回転 (rotate @ move):', (rotate @ move).apply(*point))
    m = move @ rotate @ Mat3.scaling(2, 2)
    p = m.apply(*point)
    print('拡大・回転・移動した点:', p)
    print('逆変換で元に戻した点:', m.inverse().apply(*p))


if __name__ == '__main__':
    main()
