#include <iostream>
#include <vector>

constexpr int max_users = 100;  // コンパイル時に値が確定する

int main() {
    auto x = 42;                         // int
    auto y = 3.14;                       // double
    auto v = std::vector<int>{1, 2, 3};  // std::vector<int>

    const int limit = x + 1;  // 実行時に決まる値でもよい
    // limit = 20;            // エラー: const 変数には代入できない

    std::cout << x << ' ' << y << ' ' << v.size() << ' ' << limit << ' ' << max_users << '\n';
    return 0;
}
