"""第 4 章: 2 次元ベクトルのクラス Vec2 を自作する。

仕組みを理解するための実装である。実際のゲームでは pygame.Vector2 など、ライブラリーのものを使えばよい。

実行方法:
    py vec2.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass

EPSILON = 1e-9  # これより短いベクトルは長さ 0 とみなす


@dataclass(frozen=True)
class Vec2:
    """2 次元ベクトル。演算は新しい Vec2 を返し、元のベクトルは変更しない。"""

    x: float
    y: float

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, k: float) -> Vec2:
        return Vec2(self.x * k, self.y * k)

    def __rmul__(self, k: float) -> Vec2:
        return self * k

    def __truediv__(self, k: float) -> Vec2:
        return Vec2(self.x / k, self.y / k)

    def __neg__(self) -> Vec2:
        return Vec2(-self.x, -self.y)

    def length(self) -> float:
        """長さ（大きさ）。"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def length_squared(self) -> float:
        """長さの 2 乗。平方根を計算しないので、長さの比較だけなら速い。"""
        return self.x * self.x + self.y * self.y

    def normalized(self) -> Vec2:
        """同じ向きで長さ 1 のベクトル（単位ベクトル）。長さ 0 のベクトルは向きが無いので、そのまま返す。"""
        n = self.length()
        if n < EPSILON:
            return Vec2(0.0, 0.0)
        return self / n

    def dot(self, other: Vec2) -> float:
        """内積。"""
        return self.x * other.x + self.y * other.y

    def cross(self, other: Vec2) -> float:
        """2 次元の外積（z 成分だけを取り出したスカラー値）。"""
        return self.x * other.y - self.y * other.x

    def project_onto(self, other: Vec2) -> Vec2:
        """other の方向への射影（self のうち other と同じ向きの成分）。"""
        return other * (self.dot(other) / other.length_squared())

    def reflect(self, normal: Vec2) -> Vec2:
        """単位ベクトル normal を法線とする面で反射させたベクトル。"""
        return self - normal * (2 * self.dot(normal))

    def rotated(self, angle: float) -> Vec2:
        """原点を中心に angle ラジアン回転させたベクトル（第 5 章で説明する）。"""
        c, s = math.cos(angle), math.sin(angle)
        return Vec2(self.x * c - self.y * s, self.x * s + self.y * c)


def main() -> None:
    a = Vec2(3, 4)
    b = Vec2(1, 0)
    print('a =', a, ' b =', b)
    print('a + b =', a + b)
    print('a - b =', a - b)
    print('a * 2 =', a * 2)
    print('|a| =', a.length())
    print('a の単位ベクトル =', a.normalized())
    print('a・b =', a.dot(b))
    print('a×b =', a.cross(b))
    print('a の b 方向への射影 =', a.project_onto(b))
    print('(1, -1) を床（法線 (0, 1)）で反射 =', Vec2(1, -1).reflect(Vec2(0, 1)))


if __name__ == '__main__':
    main()
