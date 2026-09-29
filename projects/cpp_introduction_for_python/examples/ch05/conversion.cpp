#include <iostream>

int main() {
    int a = 7;
    int b = 2;
    std::cout << a / b << '\n';                       // 3
    std::cout << static_cast<double>(a) / b << '\n';  // 3.5

    double d = 3.99;
    int i = static_cast<int>(d);  // 小数部は切り捨てられる
    std::cout << i << '\n';       // 3
    return 0;
}
