#include <iostream>

int square(int x);  // 宣言

int main() {
    std::cout << square(5) << '\n';
    return 0;
}

int square(int x) {  // 定義
    return x * x;
}
