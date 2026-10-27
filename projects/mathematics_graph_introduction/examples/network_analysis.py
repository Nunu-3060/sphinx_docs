"""第 15 章 ネットワーク科学への入口.

空手クラブのネットワークで各種の中心性を計算し、ランダムグラフ・スモールワールド・
スケールフリーの 3 つのモデルを比較する。

実行方法:
    python network_analysis.py
"""

from typing import cast

import networkx as nx


def clustering_coefficient(g: "nx.Graph[int]", v: int) -> float:
    """頂点 v の局所クラスタ係数: 隣接頂点の組のうち、互いに隣接している組の割合。"""
    neighbors = list(g.neighbors(v))
    k = len(neighbors)
    if k < 2:
        return 0.0
    links = sum(1 for i in range(k) for j in range(i + 1, k) if g.has_edge(neighbors[i], neighbors[j]))
    return 2.0 * links / (k * (k - 1))


def top3(scores: dict[int, float]) -> list[tuple[int, float]]:
    """値の大きい順に上位 3 頂点を返す。"""
    return [(v, round(s, 3)) for v, s in sorted(scores.items(), key=lambda item: -item[1])[:3]]


def summarize(name: str, g: "nx.Graph[int]") -> None:
    """平均次数・最大次数・平均クラスタ係数・平均距離を表示する。"""
    n = g.number_of_nodes()
    degrees = [d for _, d in g.degree()]
    # 連結でない場合に備え、最大の連結成分で平均距離を計算する
    largest = g.subgraph(max(nx.connected_components(g), key=len))
    print(f"{name}: 平均次数 = {sum(degrees) / n:.2f}, 最大次数 = {max(degrees)}, "
          f"平均クラスタ係数 = {nx.average_clustering(g):.3f}, "
          f"平均距離 = {nx.average_shortest_path_length(largest):.2f}")


def main() -> None:
    karate = nx.karate_club_graph()
    print("空手クラブ: 頂点数 =", karate.number_of_nodes(), "辺数 =", karate.number_of_edges())
    print("頂点 0 のクラスタ係数:", round(clustering_coefficient(karate, 0), 3),
          "NetworkX:", round(cast(float, nx.clustering(karate, 0)), 3))
    print("次数中心性 上位:", top3(nx.degree_centrality(karate)))
    print("近接中心性 上位:", top3(nx.closeness_centrality(karate)))
    print("媒介中心性 上位:", top3(nx.betweenness_centrality(karate)))
    print("固有ベクトル中心性 上位:", top3(nx.eigenvector_centrality(karate)))

    # 頂点数 1000、平均次数 6 程度にそろえた 3 つのモデル
    n, seed = 1000, 1
    models: dict[str, nx.Graph[int]] = {
        "ER  (p = 0.006)": nx.erdos_renyi_graph(n, 6 / (n - 1), seed=seed),
        "WS  (k = 6, p = 0.1)": nx.watts_strogatz_graph(n, 6, 0.1, seed=seed),
        "BA  (m = 3)": nx.barabasi_albert_graph(n, 3, seed=seed),
    }
    for name, g in models.items():
        summarize(name, g)


if __name__ == "__main__":
    main()
