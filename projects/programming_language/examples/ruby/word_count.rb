# frozen_string_literal: true

# 文章中の単語の出現回数を数え、上位の単語を表示するサンプル

# 英単語を小文字にそろえて出現回数を数える。
def count_words(text)
  text.downcase.scan(/[a-z]+/).tally
end

# 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す。
def top_words(counts, limit)
  counts.sort_by { |word, count| [-count, word] }.first(limit)
end

text = 'The quick brown fox jumps over the lazy dog. The dog sleeps.'
top_words(count_words(text), 3).each do |word, count|
  puts "#{word}: #{count}"
end
