"""第 8 章 平面グラフ.

NetworkX の平面性判定で平面グラフかどうかを調べ、平面埋め込みの面の数から
オイラーの公式 n - m + f = 2 を確かめる。

実行方法:
    python planarity.py
"""

import networkx as nx


def count_faces(embedding: "nx.PlanarEmbedding[int]") -> int:
    """平面埋め込みの面の数を数える。

    各辺は 2 つの向き (u, v), (v, u) を持ち、それぞれちょうど 1 つの面の境界になる。
    向き付きの辺を順にたどって面を 1 つずつ数える。
    """
    visited: set[tuple[int, int]] = set()
    faces = 0
    for u, v in embedding.edges():
        if (u, v) not in visited:
            embedding.traverse_face(u, v, mark_half_edges=visited)
            faces += 1
    return faces


def main() -> None:
    graphs: dict[str, nx.Graph[int]] = {
        "K4": nx.complete_graph(4),
        "K5": nx.complete_graph(5),
        "K3,3": nx.complete_bipartite_graph(3, 3),
        "立方体 Q3": nx.convert_node_labels_to_integers(nx.hypercube_graph(3)),
        "正十二面体": nx.dodecahedral_graph(),
        "ピーターセン": nx.petersen_graph(),
    }
    for name, g in graphs.items():
        n, m = g.number_of_nodes(), g.number_of_edges()
        is_planar, embedding = nx.check_planarity(g)
        if is_planar and isinstance(embedding, nx.PlanarEmbedding):
            f = count_faces(embedding)
            print(f"{name}: 平面的, n = {n}, m = {m}, f = {f}, n - m + f = {n - m + f}")
        else:
            # 単純な平面グラフでは m <= 3n - 6 が成り立つ
            print(f"{name}: 非平面的, n = {n}, m = {m}, 3n - 6 = {3 * n - 6}")


if __name__ == "__main__":
    main()
