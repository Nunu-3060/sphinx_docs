// C++20
#include <concepts>
#include <iostream>

template <typename T>
concept Number = std::integral<T> || std::floating_point<T>;

template <Number T>
T twice(T x) {
    return x * 2;
}

int main() {
    std::cout << twice(21) << '\n';   // 42
    std::cout << twice(1.5) << '\n';  // 3
    // twice("abc");  // エラー: const char* は Number を満たさない
    return 0;
}
