#include <iostream>

int main() {
    auto square = [](int x) { return x * x; };
    std::cout << square(5) << '\n';  // 25

    int offset = 10;
    auto add_offset = [offset](int x) { return x + offset; };  // 値キャプチャー

    int counter = 0;
    auto count_up = [&counter]() { ++counter; };  // 参照キャプチャー

    std::cout << add_offset(1) << '\n';  // 11
    count_up();
    count_up();
    std::cout << counter << '\n';  // 2
    return 0;
}
