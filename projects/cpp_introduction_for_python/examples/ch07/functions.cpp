#include <iostream>
#include <string>

int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {  // 引数の型が異なる同名の関数（オーバーロード）
    return a + b;
}

void greet(const std::string& name, const std::string& greeting = "Hello") {
    std::cout << greeting << ", " << name << '\n';
}

void increment_copy(int x) {  // 値渡し
    x += 1;
}

void increment_ref(int& x) {  // 参照渡し
    x += 1;
}

int main() {
    std::cout << add(1, 2) << '\n';       // int 版が呼ばれる
    std::cout << add(1.5, 2.25) << '\n';  // double 版が呼ばれる
    greet("Alice");
    greet("Bob", "Hi");

    int n = 0;
    increment_copy(n);
    std::cout << n << '\n';  // 0
    increment_ref(n);
    std::cout << n << '\n';  // 1
    return 0;
}
