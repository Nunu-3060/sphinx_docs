"""WebGL のサンプルで使う頂点データを JavaScript のコードとして出力する。

使い方:
    python gen_vertices.py cube
    python gen_vertices.py cube --size 2 --name BIG_CUBE
    python gen_vertices.py sphere --radius 1 --segments 32 --rings 16
    python gen_vertices.py sphere -o sphere.js

出力される JavaScript のオブジェクトは次のプロパティーを持つ。

    positions : 頂点座標 (x, y, z)
    colors    : 頂点カラー (r, g, b)。立方体のみ。面ごとに色が異なる
    normals   : 法線ベクトル (x, y, z)
    uvs       : テクスチャ座標 (u, v)
    indices   : インデックス（3 つで 1 つの三角形。反時計回りが表面）
"""

from __future__ import annotations

import argparse
import io
import math
import sys
from dataclasses import dataclass, field

Vec3 = tuple[float, float, float]


@dataclass
class Mesh:
    """頂点属性ごとに平らな配列で保持したメッシュ。"""

    positions: list[float] = field(default_factory=list)
    colors: list[float] = field(default_factory=list)
    normals: list[float] = field(default_factory=list)
    uvs: list[float] = field(default_factory=list)
    indices: list[int] = field(default_factory=list)

    @property
    def vertex_count(self) -> int:
        return len(self.positions) // 3


# 立方体の各面の定義: (法線, 面の右方向 u, 面の上方向 v, 面の色)
# u × v = 法線 となるように選んでいるので、
# 左下 → 右下 → 右上 の順に並べると外側から見て反時計回りになる。
CUBE_FACES: list[tuple[Vec3, Vec3, Vec3, Vec3]] = [
    ((1, 0, 0), (0, 0, -1), (0, 1, 0), (0.90, 0.30, 0.30)),   # +X 赤
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0), (0.30, 0.85, 0.85)),   # -X 水色
    ((0, 1, 0), (1, 0, 0), (0, 0, -1), (0.35, 0.80, 0.35)),   # +Y 緑
    ((0, -1, 0), (1, 0, 0), (0, 0, 1), (0.85, 0.35, 0.85)),   # -Y 紫
    ((0, 0, 1), (1, 0, 0), (0, 1, 0), (0.35, 0.45, 0.90)),    # +Z 青
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0), (0.90, 0.85, 0.30)),  # -Z 黄
]

# 面の 4 隅: (u 方向の係数, v 方向の係数, テクスチャ座標 u, v)
FACE_CORNERS: list[tuple[float, float, float, float]] = [
    (-0.5, -0.5, 0.0, 0.0),  # 左下
    (0.5, -0.5, 1.0, 0.0),   # 右下
    (0.5, 0.5, 1.0, 1.0),    # 右上
    (-0.5, 0.5, 0.0, 1.0),   # 左上
]


def make_cube(size: float) -> Mesh:
    """1 辺が size の立方体を作る。面ごとに頂点を分けるので頂点数は 24。"""
    mesh = Mesh()
    for normal, u_axis, v_axis, color in CUBE_FACES:
        base = mesh.vertex_count
        for cu, cv, tu, tv in FACE_CORNERS:
            for axis in range(3):
                center = normal[axis] * 0.5
                offset = u_axis[axis] * cu + v_axis[axis] * cv
                mesh.positions.append((center + offset) * size)
            mesh.colors.extend(color)
            mesh.normals.extend(normal)
            mesh.uvs.extend((tu, tv))
        # 四角形を 2 つの三角形に分ける
        mesh.indices.extend(
            (base, base + 1, base + 2, base, base + 2, base + 3)
        )
    return mesh


def make_sphere(radius: float, segments: int, rings: int) -> Mesh:
    """緯度・経度で分割した球を作る。

    segments は経度方向（横）の分割数、rings は緯度方向（縦）の分割数。
    テクスチャの継ぎ目を表現するため、経度 0 度と 360 度の頂点は別に持つ。
    """
    mesh = Mesh()
    for i in range(rings + 1):
        theta = math.pi * i / rings          # 北極 0 → 南極 π
        for j in range(segments + 1):
            phi = 2.0 * math.pi * j / segments
            nx = math.sin(theta) * math.sin(phi)
            ny = math.cos(theta)
            nz = math.sin(theta) * math.cos(phi)
            mesh.positions.extend((nx * radius, ny * radius, nz * radius))
            mesh.normals.extend((nx, ny, nz))
            mesh.uvs.extend((j / segments, 1.0 - i / rings))
    for i in range(rings):
        for j in range(segments):
            a = i * (segments + 1) + j   # 左上
            b = a + segments + 1         # 左下
            mesh.indices.extend((a, b, a + 1, a + 1, b, b + 1))
    return mesh


def format_number(value: float) -> str:
    """小数点以下 4 桁に丸め、余分な 0 と負のゼロを取り除く。"""
    rounded = round(value, 4)
    if rounded == 0:
        return "0"
    return f"{rounded:.4f}".rstrip("0").rstrip(".")


def format_array(
    values: list[float] | list[int], per_line: int, indent: str
) -> str:
    """数値の配列を per_line 個ずつ改行した文字列にする。"""
    lines = []
    for start in range(0, len(values), per_line):
        chunk = values[start:start + per_line]
        lines.append(indent + ", ".join(format_number(v) for v in chunk) + ",")
    return "\n".join(lines)


def to_javascript(mesh: Mesh, name: str, command: str) -> str:
    """メッシュを JavaScript の const 宣言として出力する。"""
    indent = "    "
    parts = [
        f"// python gen_vertices.py {command} で生成"
        f"（頂点数 {mesh.vertex_count}、"
        f"三角形数 {len(mesh.indices) // 3}）",
        f"const {name} = {{",
    ]
    attributes: list[tuple[str, list[float], int]] = [
        ("positions", mesh.positions, 3),
        ("colors", mesh.colors, 3),
        ("normals", mesh.normals, 3),
        ("uvs", mesh.uvs, 2),
    ]
    for prop, values, size in attributes:
        if not values:
            continue
        parts.append(f"  {prop}: new Float32Array([")
        parts.append(format_array(values, size * 4, indent))
        parts.append("  ]),")
    parts.append("  indices: new Uint16Array([")
    parts.append(format_array(mesh.indices, 6, indent))
    parts.append("  ]),")
    parts.append("};")
    return "\n".join(parts) + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="頂点データを JavaScript のコードとして出力します。"
    )
    parser.add_argument(
        "-o", "--output", help="出力先のファイル（省略時は標準出力）"
    )
    parser.add_argument(
        "--name", help="JavaScript の定数名（省略時は CUBE または SPHERE）"
    )
    sub = parser.add_subparsers(dest="shape", required=True)

    cube = sub.add_parser("cube", help="立方体")
    cube.add_argument("--size", type=float, default=1.0, help="1 辺の長さ")

    sphere = sub.add_parser("sphere", help="球")
    sphere.add_argument("--radius", type=float, default=0.5, help="半径")
    sphere.add_argument(
        "--segments", type=int, default=24, help="経度方向の分割数"
    )
    sphere.add_argument(
        "--rings", type=int, default=12, help="緯度方向の分割数"
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    command = " ".join(argv)
    if args.shape == "cube":
        mesh = make_cube(args.size)
        name = args.name or "CUBE"
    else:
        if args.segments < 3 or args.rings < 2:
            print("segments は 3 以上、rings は 2 以上を指定してください。",
                  file=sys.stderr)
            return 1
        mesh = make_sphere(args.radius, args.segments, args.rings)
        name = args.name or "SPHERE"

    if mesh.vertex_count > 65536:
        print("頂点数が Uint16Array の上限 (65536) を超えています。",
              file=sys.stderr)
        return 1

    code = to_javascript(mesh, name, command)
    if args.output:
        with open(args.output, "w", encoding="utf-8", newline="\n") as f:
            f.write(code)
    else:
        # Windows でリダイレクトしても UTF-8 で出力されるようにする
        if isinstance(sys.stdout, io.TextIOWrapper):
            sys.stdout.reconfigure(encoding="utf-8", newline="\n")
        sys.stdout.write(code)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
