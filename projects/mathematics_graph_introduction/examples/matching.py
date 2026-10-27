"""第 10 章 マッチング.

増加路法で二部グラフの最大マッチングを求め、ケーニッヒの定理に従って最小頂点被覆を構成する。
また、ゲール・シャプレー法で安定マッチングを求める。

実行方法:
    python matching.py
"""

import networkx as nx


def max_bipartite_matching(left: list[str], adj: dict[str, list[str]]) -> dict[str, str]:
    """増加路法で二部グラフの最大マッチングを求める。

    adj[u] は左側の頂点 u に隣接する右側の頂点のリスト。
    戻り値は右側の頂点 -> 左側の頂点 の対応。
    """
    match_of: dict[str, str] = {}

    def try_augment(u: str, visited: set[str]) -> bool:
        """u から始まる増加路を深さ優先探索で探し、見つかればマッチングを更新する。"""
        for v in adj[u]:
            if v in visited:
                continue
            visited.add(v)
            # v が未マッチ、または v の相手が別の右側頂点に付け替えられるなら増加路がある
            if v not in match_of or try_augment(match_of[v], visited):
                match_of[v] = u
                return True
        return False

    for u in left:
        try_augment(u, set())
    return match_of


def min_vertex_cover(left: list[str], adj: dict[str, list[str]], match_of: dict[str, str]) -> set[str]:
    """ケーニッヒの定理の証明に沿って、最大マッチングから最小頂点被覆を作る。

    左側の未マッチ頂点から交互路（非マッチ辺で右へ、マッチ辺で左へ）で到達できる頂点を Z とすると、
    (左側 - Z) ∪ (右側 ∩ Z) が最小頂点被覆になる。
    """
    matched_left = set(match_of.values())
    reached = {u for u in left if u not in matched_left}
    stack = list(reached)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in reached:
                reached.add(v)
                w = match_of.get(v)
                if w is not None and w not in reached:
                    reached.add(w)
                    stack.append(w)
    right = {v for vs in adj.values() for v in vs}
    return (set(left) - reached) | (right & reached)


def gale_shapley(proposer_pref: dict[str, list[str]], acceptor_pref: dict[str, list[str]]) -> dict[str, str]:
    """ゲール・シャプレー法（受け入れ保留方式）で安定マッチングを求める。

    戻り値は 受け入れ側 -> 提案側 の対応。
    """
    rank = {a: {p: i for i, p in enumerate(prefs)} for a, prefs in acceptor_pref.items()}
    next_index = {p: 0 for p in proposer_pref}  # 次に提案する相手の順位
    engaged: dict[str, str] = {}
    free = list(proposer_pref)
    while free:
        p = free.pop()
        a = proposer_pref[p][next_index[p]]
        next_index[p] += 1
        current = engaged.get(a)
        if current is None:
            engaged[a] = p
        elif rank[a][p] < rank[a][current]:
            engaged[a] = p
            free.append(current)  # 振られた側は再び提案する
        else:
            free.append(p)
    return engaged


def main() -> None:
    # 作業者 (左側) と担当できるタスク (右側)
    left = ["Aoki", "Baba", "Chiba", "Doi", "Endo"]
    adj = {
        "Aoki": ["t1", "t2"],
        "Baba": ["t1"],
        "Chiba": ["t2", "t3", "t4"],
        "Doi": ["t2"],
        "Endo": ["t4", "t5"],
    }
    match_of = max_bipartite_matching(left, adj)
    print("最大マッチング:", sorted((u, v) for v, u in match_of.items()))
    cover = min_vertex_cover(left, adj, match_of)
    print("最小頂点被覆:", sorted(cover), "大きさ =", len(cover))

    g: nx.Graph[str] = nx.Graph()
    g.add_nodes_from(left, bipartite=0)
    g.add_edges_from((u, v) for u, vs in adj.items() for v in vs)
    nx_matching = nx.bipartite.maximum_matching(g, top_nodes=left)
    print("NetworkX の最大マッチングの大きさ:", len(nx_matching) // 2)

    # 安定マッチング（提案側 m1..m3、受け入れ側 w1..w3）
    men = {"m1": ["w1", "w2", "w3"], "m2": ["w1", "w3", "w2"], "m3": ["w2", "w1", "w3"]}
    women = {"w1": ["m3", "m2", "m1"], "w2": ["m1", "m3", "m2"], "w3": ["m1", "m2", "m3"]}
    print("安定マッチング:", sorted((p, a) for a, p in gale_shapley(men, women).items()))


if __name__ == "__main__":
    main()
