"""Python SOP に貼り付けて使うコード。波打つ面をポイントとポリゴンから作る。

build_python_sop.py が、このファイルの中身を Python SOP の Python Code
パラメーターに設定する。Python SOP の中では、hou.pwd() がその Python SOP
自身を表す。
"""

from __future__ import annotations

import math

import hou

COLUMNS = 40      # x 方向のポイント数
ROWS = 40         # z 方向のポイント数
SIZE = 4.0        # 面の一辺の長さ
AMPLITUDE = 0.2   # 波の高さ

node = hou.pwd()
geo = node.geometry()       # このノードが出力するジオメトリ（最初は空）
phase = hou.frame() * 0.1   # フレームが進むと波が動く

# ポイントを作る。i が z 方向、j が x 方向の番号である。
positions = []
for i in range(ROWS):
    for j in range(COLUMNS):
        x = (j / (COLUMNS - 1) - 0.5) * SIZE
        z = (i / (ROWS - 1) - 0.5) * SIZE
        y = AMPLITUDE * math.sin(3.0 * x + phase) * math.cos(2.0 * z)
        positions.append(hou.Vector3(x, y, z))
points = geo.createPoints(positions)

# 隣り合う 4 つのポイントを結んで四角形のポリゴンを作る。Houdini では、
# 表から見て時計回りにポイントを並べると、その面が表（法線の向き）になる。
quads = []
for i in range(ROWS - 1):
    for j in range(COLUMNS - 1):
        a = i * COLUMNS + j
        quads.append((points[a], points[a + 1], points[a + COLUMNS + 1], points[a + COLUMNS]))
geo.createPolygons(quads)
