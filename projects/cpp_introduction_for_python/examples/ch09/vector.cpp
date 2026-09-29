#include <iostream>
#include <stdexcept>
#include <vector>

int main() {
    std::vector<int> v = {3, 1, 4};
    v.push_back(1);                 // Python: v.append(1)
    std::cout << v.size() << '\n';  // 4
    std::cout << v[0] << '\n';      // 3
    std::cout << v.back() << '\n';  // 1（Python: v[-1]）

    v.pop_back();  // 末尾の要素を削除する（削除した値は返さない）
    for (int x : v) {
        std::cout << x << ' ';
    }
    std::cout << '\n';

    try {
        std::cout << v.at(10) << '\n';  // 範囲外なので例外が送出される
    } catch (const std::out_of_range&) {
        std::cout << "out of range\n";
    }
    return 0;
}
