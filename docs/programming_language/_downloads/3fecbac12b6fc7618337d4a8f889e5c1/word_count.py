"""文章中の単語の出現回数を数え、上位の単語を表示するサンプル."""

import re
from collections import Counter

TEXT = "The quick brown fox jumps over the lazy dog. The dog sleeps."


def count_words(text: str) -> Counter[str]:
    """英単語を小文字にそろえて出現回数を数える."""
    return Counter(re.findall(r"[a-z]+", text.lower()))


def top_words(counts: Counter[str], limit: int) -> list[tuple[str, int]]:
    """出現回数の降順、同数なら単語の昇順で上位 limit 件を返す."""
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]


def main() -> None:
    """サンプルの文章を集計して上位 3 件を表示する."""
    for word, count in top_words(count_words(TEXT), 3):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()
