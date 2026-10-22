// 文章中の単語の出現回数を数え、上位の単語を表示するサンプル

/**
 * 英単語を小文字にそろえて出現回数を数える。
 * @param {string} text
 * @returns {Map<string, number>}
 */
function countWords(text) {
  const counts = new Map();
  for (const word of text.toLowerCase().match(/[a-z]+/g) ?? []) {
    counts.set(word, (counts.get(word) ?? 0) + 1);
  }
  return counts;
}

/**
 * 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。
 * @param {Map<string, number>} counts
 * @param {number} limit
 * @returns {[string, number][]}
 */
function topWords(counts, limit) {
  return [...counts]
    .sort(([w1, c1], [w2, c2]) => c2 - c1 || w1.localeCompare(w2))
    .slice(0, limit);
}

const text = "The quick brown fox jumps over the lazy dog. The dog sleeps.";
for (const [word, count] of topWords(countWords(text), 3)) {
  console.log(`${word}: ${count}`);
}
