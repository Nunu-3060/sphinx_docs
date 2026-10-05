"""トライと Union-Find のサンプル。

前半では、単語をトライに格納し、接頭辞で始まる単語を列挙する
（オートコンプリートの基本となる操作）。後半では、Union-Find
（素集合データ構造）で辺を順に併合し、頂点同士が連結かを判定する。

実行方法: python ch04_trie_unionfind.py
関連する章: 第 4 章「データ構造」
"""


class TrieNode:
    """トライのノード。子ノードを文字ごとに辞書で持つ。"""

    def __init__(self) -> None:
        """子を持たず、単語の終わりでないノードを作る。"""
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class Trie:
    """文字列の集合を格納するトライ。"""

    def __init__(self) -> None:
        """根だけを持つ空のトライを作る。"""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """単語を 1 文字ずつたどり、無いノードは作りながら格納する。"""
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def starts_with(self, prefix: str) -> list[str]:
        """接頭辞 prefix で始まる単語を辞書順にすべて返す。"""
        node = self.root
        for ch in prefix:  # 接頭辞の長さだけたどる
            if ch not in node.children:
                return []
            node = node.children[ch]
        result: list[str] = []
        self._collect(node, prefix, result)
        return result

    def _collect(self, node: TrieNode, path: str, out: list[str]) -> None:
        """node 以下の単語を深さ優先で out に集める。"""
        if node.is_word:
            out.append(path)
        for ch in sorted(node.children):
            self._collect(node.children[ch], path + ch, out)


class UnionFind:
    """経路圧縮とランクによる併合を行う Union-Find。"""

    def __init__(self, n: int) -> None:
        """0 から n-1 までの要素を、それぞれ 1 要素の集合として作る。"""
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        """x が属する集合の代表（根）を返し、経路を圧縮する。"""
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:  # たどった要素を根に直接つなぐ
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a: int, b: int) -> bool:
        """a と b の集合を併合する。すでに同じ集合なら False を返す。"""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:  # 低い木を高い木の下につなぐ
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def main() -> None:
    """トライの接頭辞検索と Union-Find の連結判定を実行する。"""
    trie = Trie()
    for word in ["car", "card", "care", "cat", "dog", "do", "carbon"]:
        trie.insert(word)
    for prefix in ["car", "do", "ca", "x"]:
        print(f"'{prefix}' で始まる単語: {trie.starts_with(prefix)}")

    uf = UnionFind(6)
    edges = [(0, 1), (2, 3), (1, 2), (4, 5), (0, 3)]
    for a, b in edges:
        merged = uf.union(a, b)
        status = "併合した" if merged else "すでに連結（閉路になる辺）"
        print(f"辺 ({a}, {b}): {status}")
    for a, b in [(0, 3), (0, 4), (4, 5)]:
        print(f"{a} と {b} は連結か: {uf.find(a) == uf.find(b)}")
    groups: dict[int, list[int]] = {}
    for v in range(6):
        groups.setdefault(uf.find(v), []).append(v)
    print(f"連結成分: {list(groups.values())}")


if __name__ == "__main__":
    main()
