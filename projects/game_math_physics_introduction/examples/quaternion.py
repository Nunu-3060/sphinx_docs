"""第 7 章: 3D の回転を表すクォータニオン Quat を自作する。

cube_demo.py から import して使う。

実行方法（ジンバルロックと球面線形補間の例を表示する）:
    py quaternion.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass

Vec3 = tuple[float, float, float]


def cross3(a: Vec3, b: Vec3) -> Vec3:
    """3 次元ベクトルの外積。"""
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def normalize3(v: Vec3) -> Vec3:
    """3 次元ベクトルを長さ 1 にする。"""
    n = math.sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)
    return (v[0] / n, v[1] / n, v[2] / n)


@dataclass(frozen=True)
class Quat:
    """クォータニオン w + xi + yj + zk。回転に使うときは長さ 1 に保つ。"""

    w: float = 1.0
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    @staticmethod
    def from_axis_angle(axis: Vec3, angle: float) -> Quat:
        """回転軸 axis の周りに angle ラジアン回す回転。"""
        ax, ay, az = normalize3(axis)
        s = math.sin(angle / 2)
        return Quat(math.cos(angle / 2), ax * s, ay * s, az * s)

    def __mul__(self, other: Quat) -> Quat:
        """積 self * other。ベクトルに適用すると、other で回してから self で回したことになる。"""
        return Quat(
            self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z,
            self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y,
            self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x,
            self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w,
        )

    def __neg__(self) -> Quat:
        return Quat(-self.w, -self.x, -self.y, -self.z)

    def conjugate(self) -> Quat:
        """共役。長さ 1 のクォータニオンでは逆回転を表す。"""
        return Quat(self.w, -self.x, -self.y, -self.z)

    def dot(self, other: Quat) -> float:
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def normalized(self) -> Quat:
        """長さを 1 にする。回転を何度も掛け合わせると誤差で長さがずれるので、ときどき呼ぶ。"""
        n = math.sqrt(self.dot(self))
        return Quat(self.w / n, self.x / n, self.y / n, self.z / n)

    def rotate(self, v: Vec3) -> Vec3:
        """ベクトル v を回転させる（q * v * q の共役）。"""
        r = self * Quat(0.0, *v) * self.conjugate()
        return (r.x, r.y, r.z)


def slerp(a: Quat, b: Quat, t: float) -> Quat:
    """a から b へ、一定の角速度で回転を補間する（球面線形補間）。"""
    cos_theta = a.dot(b)
    if cos_theta < 0:
        # q と -q は同じ回転を表す。近い側を選ばないと遠回りになる
        b, cos_theta = -b, -cos_theta
    if cos_theta > 0.9995:
        # ほとんど同じ向きのときは、0 に近い sin で割らないよう線形補間で代用する
        return Quat(a.w + (b.w - a.w) * t, a.x + (b.x - a.x) * t,
                    a.y + (b.y - a.y) * t, a.z + (b.z - a.z) * t).normalized()
    theta = math.acos(cos_theta)
    wa = math.sin((1 - t) * theta) / math.sin(theta)
    wb = math.sin(t * theta) / math.sin(theta)
    return Quat(wa * a.w + wb * b.w, wa * a.x + wb * b.x, wa * a.y + wb * b.y, wa * a.z + wb * b.z)


X_AXIS: Vec3 = (1.0, 0.0, 0.0)
Y_AXIS: Vec3 = (0.0, 1.0, 0.0)
Z_AXIS: Vec3 = (0.0, 0.0, 1.0)


def from_euler(yaw: float, pitch: float, roll: float) -> Quat:
    """オイラー角（度）から回転を作る。Z 軸（ロール）→ X 軸（ピッチ）→ Y 軸（ヨー）の順に回す。"""
    qy = Quat.from_axis_angle(Y_AXIS, math.radians(yaw))
    qx = Quat.from_axis_angle(X_AXIS, math.radians(pitch))
    qz = Quat.from_axis_angle(Z_AXIS, math.radians(roll))
    return qy * qx * qz


def format_vec(v: Vec3) -> str:
    return '(' + ', '.join(f'{c:6.3f}' for c in v) + ')'


def main() -> None:
    q = Quat.from_axis_angle(Z_AXIS, math.radians(90))
    print('z 軸の周りに 90 度回すと (1, 0, 0) ->', format_vec(q.rotate(X_AXIS)))

    print('--- ジンバルロック: ピッチが 90 度のとき、ヨーとロールが同じ軸の回転になる ---')
    for yaw, roll in ((30, 0), (0, -30), (60, 30)):
        r = from_euler(yaw, 90, roll)
        print(f'yaw={yaw:3d}, pitch=90, roll={roll:3d}: x 軸 -> {format_vec(r.rotate(X_AXIS))}, '
              f'y 軸 -> {format_vec(r.rotate(Y_AXIS))}')

    print('--- 球面線形補間: y 軸の周りに 0 度から 120 度へ ---')
    a = Quat()
    b = Quat.from_axis_angle(Y_AXIS, math.radians(120))
    for i in range(5):
        t = i / 4
        print(f't={t:.2f}: x 軸 -> {format_vec(slerp(a, b, t).rotate(X_AXIS))}')


if __name__ == '__main__':
    main()
