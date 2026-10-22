// 文章中の単語の出現回数を数え、上位の単語を表示するサンプル

/** 英単語を小文字にそろえて出現回数を数える。 */
fun countWords(text: String): Map<String, Int> =
    Regex("[a-z]+").findAll(text.lowercase())
        .groupingBy { it.value }
        .eachCount()

/** 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。 */
fun topWords(counts: Map<String, Int>, limit: Int): List<Pair<String, Int>> =
    counts.toList()
        .sortedWith(compareByDescending<Pair<String, Int>> { it.second }.thenBy { it.first })
        .take(limit)

fun main() {
    val text = "The quick brown fox jumps over the lazy dog. The dog sleeps."
    for ((word, count) in topWords(countWords(text), 3)) {
        println("$word: $count")
    }
}
