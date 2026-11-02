"""第 11 章「レベルとダンジョン」: 部屋のグラフに鍵と扉を置き、到達できるかを検証する。

* lock_key_map.png: BSP のダンジョンに鍵と扉を置いた地図（扉で区切られた区域ごとに色分け）
* lock_key_graph.dot: 部屋のグラフ（Graphviz の形式。本文の graphviz ディレクティブで読み込む）
* verification.txt: 正しい配置と誤った配置を検証した結果
"""

from __future__ import annotations

from collections import deque
from pathlib import Path

import numpy as np

from common import IntArray, output_dir, save_figure, setup_matplotlib
from dungeon_bsp import MAP_HEIGHT, MAP_WIDTH, Rect, carve_corridor, generate, map_image, setup_map_axes

Edge = frozenset[int]
Graph = dict[int, set[int]]


def build_graph(rooms: list[Rect], links: list[tuple[int, int]], grid: IntArray, extra: int = 2) -> Graph:
    """通路で結んだ部屋の組からグラフを作る。さらに近い部屋どうしを extra 本の通路で結んで、輪（ループ）を作る。

    BSP の通路だけでは部屋のつながりが木の形になり、行き止まりばかりになる。輪があると、
    プレイヤーが別の道を選べるようになる。追加した通路は grid にも掘る。
    """
    graph: Graph = {index: set() for index in range(len(rooms))}
    for a, b in links:
        graph[a].add(b)
        graph[b].add(a)
    candidates = []
    for a in range(len(rooms)):
        for b in range(a + 1, len(rooms)):
            if b not in graph[a]:
                (ax, ay), (bx, by) = rooms[a].center(), rooms[b].center()
                candidates.append((float(np.hypot(ax - bx, ay - by)), a, b))
    for _, a, b in sorted(candidates)[:extra]:
        graph[a].add(b)
        graph[b].add(a)
        carve_corridor(grid, rooms[a].center(), rooms[b].center(), True)
    return graph


def bfs(graph: Graph, start: int, blocked: set[Edge]) -> dict[int, int]:
    """幅優先探索。blocked の辺（閉じた扉）を通らずに start から行ける部屋と、そこまでの歩数を返す。"""
    distance = {start: 0}
    queue = deque([start])
    while queue:
        room = queue.popleft()
        for neighbor in graph[room]:
            if neighbor not in distance and frozenset((room, neighbor)) not in blocked:
                distance[neighbor] = distance[room] + 1
                queue.append(neighbor)
    return distance


def shortest_path(graph: Graph, start: int, goal: int, blocked: set[Edge]) -> list[int]:
    """start から goal への最短経路の部屋の列（幅優先探索の歩数を goal からさかのぼる）。"""
    distance = bfs(graph, start, blocked)
    path = [goal]
    while path[-1] != start:
        room = path[-1]
        path.append(next(n for n in graph[room] if distance.get(n) == distance[room] - 1
                         and frozenset((room, n)) not in blocked))
    return path[::-1]


def place_lock_and_key(graph: Graph, start: int, target: int, locked: set[Edge]) -> tuple[Edge, int]:
    """start から target へ行く途中に扉を 1 枚置き、その鍵を置く部屋を決める。

    扉は、それを閉じると target へ行けなくなる辺（迂回路の無い辺）から選ぶ。迂回路があると、
    鍵を取らずに先へ進めてしまうからである。そのような辺のうち target に最も近いものを選び、
    扉の手前で探索できる範囲を広くする。鍵は、扉を閉じたままでも start から行ける部屋の
    うち、start から最も遠い部屋に置く（プレイヤーに探索させるため）。
    """
    path = shortest_path(graph, start, target, locked)
    doors = []
    for a, b in zip(path, path[1:]):
        edge = frozenset((a, b))
        if target not in bfs(graph, start, locked | {edge}):
            doors.append(edge)
    if not doors:
        raise ValueError("迂回路の無い辺が無いので、扉を置けない")
    door = doors[-1]
    reachable = bfs(graph, start, locked | {door})
    farthest = max(reachable.values())
    key_room = min(room for room, steps in reachable.items() if steps == farthest)
    return door, key_room


def verify(graph: Graph, start: int, goal: int, doors: dict[Edge, str], keys: dict[int, str]) -> tuple[bool, list[str]]:
    """プレイヤーの行動をまねて、ゴールに着けるかを調べる。

    鍵の無い扉を閉じたまま行ける範囲を幅優先探索で求め、その範囲にある鍵をすべて拾う。
    拾った鍵で開く扉を開け、新しい鍵が拾えなくなるまで繰り返す。
    """
    held: set[str] = set()
    log = []
    while True:
        blocked = {edge for edge, name in doors.items() if name not in held}
        reachable = bfs(graph, start, blocked)
        if goal in reachable:
            log.append(f"ゴール R{goal} に到達できる（持っている鍵: {', '.join(sorted(held)) or 'なし'}）")
            return True, log
        found = {name for room, name in keys.items() if room in reachable} - held
        if not found:
            log.append(f"行ける部屋 {sorted(reachable)} に新しい鍵が無い。ゴールに到達できない")
            return False, log
        for name in sorted(found):
            room = next(r for r, n in keys.items() if n == name)
            log.append(f"R{room} で鍵 {name} を拾う（行ける部屋の数: {len(reachable)}）")
        held |= found


def zones(graph: Graph, start: int, doors: dict[Edge, str], order: list[str]) -> dict[int, int]:
    """鍵を order の順に手に入れたとき、各部屋が何本目の鍵で行けるようになるか（区域の番号）。"""
    zone: dict[int, int] = {}
    for count in range(len(order) + 1):
        blocked = {edge for edge, name in doors.items() if name not in order[:count]}
        for room in bfs(graph, start, blocked):
            zone.setdefault(room, count)
    return zone


ZONE_COLORS = ["#eef3fb", "#e8f4e4", "#fdf0e6", "#f6e3f0"]


def graph_dot(graph: Graph, start: int, goal: int, doors: dict[Edge, str], keys: dict[int, str],
              zone: dict[int, int]) -> str:
    """部屋のグラフを Graphviz の dot 形式にする。扉は赤い辺、鍵のある部屋は名前を添える。"""
    lines = [
        "graph G {",
        "    rankdir=LR;",
        '    node [shape=box, style="rounded,filled", color="#4c72b0", fontsize=11];',
        '    edge [color="#777777"];',
    ]
    for room in sorted(graph):
        label = f"R{room}"
        if room == start:
            label += "\\nスタート"
        if room == goal:
            label += "\\nゴール"
        if room in keys:
            label += f"\\n鍵 {keys[room]}"
        lines.append(f'    r{room} [label="{label}", fillcolor="{ZONE_COLORS[zone[room]]}"];')
    for a in sorted(graph):
        for b in sorted(graph[a]):
            if a < b:
                name = doors.get(frozenset((a, b)))
                style = f' [color="#c44e52", penwidth=2.5, label="扉 {name}", fontcolor="#c44e52"]' if name else ""
                lines.append(f"    r{a} -- r{b}{style};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def draw_map(file_name: str, rooms: list[Rect], grid: IntArray, start: int, goal: int, keys: dict[int, str],
             zone: dict[int, int]) -> None:
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle

    figure, ax = plt.subplots(figsize=(8, 5.2))
    ax.imshow(map_image(grid), extent=(0, MAP_WIDTH, MAP_HEIGHT, 0), interpolation="nearest")
    for index, room in enumerate(rooms):
        ax.add_patch(Rectangle((room.x, room.y), room.w, room.h, color=ZONE_COLORS[zone[index]]))
        label = f"R{index}"
        if index == start:
            label += "\nスタート"
        if index == goal:
            label += "\nゴール"
        if index in keys:
            label += f"\n鍵 {keys[index]}"
        ax.text(room.x + room.w / 2.0, room.y + room.h / 2.0, label, ha="center", va="center", fontsize=9,
                color="#333333")
    setup_map_axes(ax)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    out = output_dir(__file__)
    _, rooms, links, grid = generate(7)
    graph = build_graph(rooms, links, grid)
    start = 0
    distance = bfs(graph, start, set())
    goal = max(distance, key=lambda room: (distance[room], room))  # スタートから最も遠い部屋

    # ゴールの手前に扉 A、その鍵 A の手前に扉 B を置く（鍵 B を取る → 扉 B → 鍵 A → 扉 A → ゴール）
    door_a, key_a = place_lock_and_key(graph, start, goal, set())
    door_b, key_b = place_lock_and_key(graph, start, key_a, {door_a})
    doors = {door_a: "A", door_b: "B"}
    keys = {key_a: "A", key_b: "B"}
    zone = zones(graph, start, doors, ["B", "A"])

    report = ["正しい配置:"]
    report += ["  " + line for line in verify(graph, start, goal, doors, keys)[1]]
    # 誤った配置の例: 鍵 A を、扉 A の向こう側（ゴールの部屋）に置く
    report.append(f"誤った配置（鍵 A を扉 A の向こうの R{goal} に置いた）:")
    report += ["  " + line for line in verify(graph, start, goal, doors, {goal: "A", key_b: "B"})[1]]
    Path(out / "verification.txt").write_text("\n".join(report) + "\n", encoding="utf-8")

    draw_map("lock_key_map.png", rooms, grid, start, goal, keys, zone)
    Path(out / "lock_key_graph.dot").write_text(graph_dot(graph, start, goal, doors, keys, zone), encoding="utf-8")


if __name__ == "__main__":
    main()
