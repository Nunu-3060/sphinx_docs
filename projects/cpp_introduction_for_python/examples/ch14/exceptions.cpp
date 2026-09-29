#include <iostream>
#include <stdexcept>
#include <string>

double divide(double a, double b) {
    if (b == 0.0) {
        throw std::invalid_argument("division by zero");
    }
    return a / b;
}

int main() {
    try {
        std::cout << divide(10.0, 4.0) << '\n';  // 2.5
        std::cout << divide(1.0, 0.0) << '\n';   // 例外が送出される
    } catch (const std::invalid_argument& e) {
        std::cout << "error: " << e.what() << '\n';
    }

    try {
        int n = std::stoi("abc");  // 変換できないので例外が送出される
        std::cout << n << '\n';
    } catch (const std::exception&) {
        std::cout << "cannot convert\n";
    }
    return 0;
}
