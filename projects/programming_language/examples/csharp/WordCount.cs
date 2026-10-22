// 文章中の単語の出現回数を数え、上位の単語を表示するサンプル
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace WordCountSample;

public static class Program
{
    /// <summary>英単語を小文字にそろえて出現回数を数える。</summary>
    public static Dictionary<string, int> CountWords(string text) =>
        Regex.Matches(text.ToLowerInvariant(), "[a-z]+")
            .GroupBy(match => match.Value)
            .ToDictionary(group => group.Key, group => group.Count());

    /// <summary>出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。</summary>
    public static List<KeyValuePair<string, int>> TopWords(Dictionary<string, int> counts, int limit) =>
        counts.OrderByDescending(pair => pair.Value)
            .ThenBy(pair => pair.Key, StringComparer.Ordinal)
            .Take(limit)
            .ToList();

    public static void Main()
    {
        const string text = "The quick brown fox jumps over the lazy dog. The dog sleeps.";
        foreach (var (word, count) in TopWords(CountWords(text), 3))
        {
            Console.WriteLine($"{word}: {count}");
        }
    }
}
