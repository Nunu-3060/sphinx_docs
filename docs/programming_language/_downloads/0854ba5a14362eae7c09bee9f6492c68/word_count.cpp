// 文章中の単語の出現回数を数え、上位の単語を表示するサンプル
#include <algorithm>
#include <cctype>
#include <cstddef>
#include <cstdlib>
#include <exception>
#include <iostream>
#include <map>
#include <regex>
#include <string>
#include <utility>
#include <vector>

namespace {

using WordCount = std::pair<std::string, int>;

// 英単語を小文字にそろえて出現回数を数える
std::map<std::string, int> count_words(std::string text) {
    std::ranges::transform(text, text.begin(),
                           [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
    std::map<std::string, int> counts;
    const std::regex word_pattern("[a-z]+");
    for (auto it = std::sregex_iterator(text.begin(), text.end(), word_pattern);
         it != std::sregex_iterator(); ++it) {
        ++counts[it->str()];
    }
    return counts;
}

// 出現回数の降順、同数なら単語の昇順で上位 limit 件を返す
std::vector<WordCount> top_words(const std::map<std::string, int> &counts, std::size_t limit) {
    std::vector<WordCount> items(counts.begin(), counts.end());
    std::ranges::sort(items, [](const WordCount &a, const WordCount &b) {
        return a.second != b.second ? a.second > b.second : a.first < b.first;
    });
    if (items.size() > limit) {
        items.resize(limit);
    }
    return items;
}

} // namespace

int main() {
    try {
        const std::string text = "The quick brown fox jumps over the lazy dog. The dog sleeps.";
        for (const auto &[word, count] : top_words(count_words(text), 3)) {
            std::cout << word << ": " << count << '\n';
        }
    } catch (const std::exception &e) {
        std::cerr << "error: " << e.what() << '\n';
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}
