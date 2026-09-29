#include <algorithm>
#include <iostream>
#include <numeric>
#include <vector>

void print(const std::vector<int>& v) {
    for (int x : v) {
        std::cout << x << ' ';
    }
    std::cout << '\n';
}

int main() {
    std::vector<int> v = {5, 3, 8, 1, 9, 2};

    std::sort(v.begin(), v.end());
    print(v);  // 1 2 3 5 8 9

    std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
    print(v);  // 9 8 5 3 2 1

    int total = std::accumulate(v.begin(), v.end(), 0);
    std::cout << total << '\n';  // 28

    auto it = std::find_if(v.begin(), v.end(), [](int x) { return x < 4; });
    if (it != v.end()) {
        std::cout << *it << '\n';  // 3
    }

    bool has_even = std::any_of(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    std::cout << std::boolalpha << has_even << '\n';  // true

    std::vector<int> squares(v.size());
    std::transform(v.begin(), v.end(), squares.begin(), [](int x) { return x * x; });
    print(squares);  // 81 64 25 9 4 1
    return 0;
}
