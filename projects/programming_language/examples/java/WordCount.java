import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.function.Function;
import java.util.regex.MatchResult;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/** 文章中の単語の出現回数を数え、上位の単語を表示するサンプル。 */
public final class WordCount {
  private static final Pattern WORD_PATTERN = Pattern.compile("[a-z]+");

  private WordCount() {}

  /** 英単語を小文字にそろえて出現回数を数える。 */
  static Map<String, Long> countWords(String text) {
    return WORD_PATTERN
        .matcher(text.toLowerCase(Locale.ROOT))
        .results()
        .map(MatchResult::group)
        .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
  }

  /** 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。 */
  static List<Map.Entry<String, Long>> topWords(Map<String, Long> counts, int limit) {
    Comparator<Map.Entry<String, Long>> order =
        Map.Entry.<String, Long>comparingByValue()
            .reversed()
            .thenComparing(Map.Entry.comparingByKey());
    return counts.entrySet().stream().sorted(order).limit(limit).toList();
  }

  public static void main(String[] args) {
    String text = "The quick brown fox jumps over the lazy dog. The dog sleeps.";
    for (Map.Entry<String, Long> entry : topWords(countWords(text), 3)) {
      System.out.println(entry.getKey() + ": " + entry.getValue());
    }
  }
}
