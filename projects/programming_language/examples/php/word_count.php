<?php

declare(strict_types=1);

// 文章中の単語の出現回数を数え、上位の単語を表示するサンプル

/**
 * 英単語を小文字にそろえて出現回数を数える。
 *
 * @return array<string, int>
 */
function countWords(string $text): array
{
    preg_match_all('/[a-z]+/', strtolower($text), $matches);
    return array_count_values($matches[0]);
}

/**
 * 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。
 *
 * @param array<string, int> $counts
 * @return array<string, int>
 */
function topWords(array $counts, int $limit): array
{
    uksort($counts, fn(string $a, string $b): int => [$counts[$b], $a] <=> [$counts[$a], $b]);
    return array_slice($counts, 0, $limit, true);
}

$text = 'The quick brown fox jumps over the lazy dog. The dog sleeps.';
foreach (topWords(countWords($text), 3) as $word => $count) {
    echo "{$word}: {$count}\n";
}
