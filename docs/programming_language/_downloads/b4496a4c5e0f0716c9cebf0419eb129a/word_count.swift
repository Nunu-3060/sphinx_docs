// 文章中の単語の出現回数を数え、上位の単語を表示するサンプル

/// 英単語を小文字にそろえて出現回数を数える。
func countWords(in text: String) -> [String: Int] {
    var counts: [String: Int] = [:]
    for word in text.lowercased().split(whereSeparator: { !$0.isLetter }) {
        counts[String(word), default: 0] += 1
    }
    return counts
}

/// 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。
func topWords(_ counts: [String: Int], limit: Int) -> [(word: String, count: Int)] {
    let sorted = counts.sorted { lhs, rhs in
        lhs.value != rhs.value ? lhs.value > rhs.value : lhs.key < rhs.key
    }
    return sorted.prefix(limit).map { (word: $0.key, count: $0.value) }
}

let text = "The quick brown fox jumps over the lazy dog. The dog sleeps."
for (word, count) in topWords(countWords(in: text), limit: 3) {
    print("\(word): \(count)")
}
