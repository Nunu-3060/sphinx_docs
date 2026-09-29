#include <iostream>

int main() {
    int x = 10;
    int* p = &x;  // x のアドレスを p に格納する

    std::cout << *p << '\n';  // 10
    *p = 20;                  // p が指す先（x）を変更する
    std::cout << x << '\n';   // 20

    int& r = x;  // r は x の別名
    r = 30;
    std::cout << x << '\n';  // 30

    int* q = nullptr;  // 何も指していない
    if (q == nullptr) {
        std::cout << "q is null\n";
    }
    return 0;
}
