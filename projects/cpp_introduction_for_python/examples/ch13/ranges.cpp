// C++20
#include <algorithm>
#include <iostream>
#include <ranges>
#include <vector>

int main() {
    std::vector<int> v = {5, 3, 8, 1, 9, 2};
    std::ranges::sort(v);

    // Python: (x * x for x in v if x % 2 == 1)
    auto odd_squares = v
        | std::views::filter([](int x) { return x % 2 == 1; })
        | std::views::transform([](int x) { return x * x; });

    for (int x : odd_squares) {
        std::cout << x << ' ';
    }
    std::cout << '\n';  // 1 9 25 81
    return 0;
}
