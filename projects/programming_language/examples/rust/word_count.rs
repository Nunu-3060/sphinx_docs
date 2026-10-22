//! 文章中の単語の出現回数を数え、上位の単語を表示するサンプル

use std::collections::HashMap;

/// 英単語を小文字にそろえて出現回数を数える
fn count_words(text: &str) -> HashMap<String, usize> {
    let mut counts = HashMap::new();
    let words = text
        .split(|c: char| !c.is_ascii_alphabetic())
        .filter(|w| !w.is_empty());
    for word in words {
        *counts.entry(word.to_lowercase()).or_insert(0) += 1;
    }
    counts
}

/// 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す
fn top_words(counts: &HashMap<String, usize>, limit: usize) -> Vec<(&str, usize)> {
    let mut items: Vec<(&str, usize)> = counts.iter().map(|(w, &c)| (w.as_str(), c)).collect();
    items.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(b.0)));
    items.truncate(limit);
    items
}

fn main() {
    let text = "The quick brown fox jumps over the lazy dog. The dog sleeps.";
    let counts = count_words(text);
    for (word, count) in top_words(&counts, 3) {
        println!("{word}: {count}");
    }
}
