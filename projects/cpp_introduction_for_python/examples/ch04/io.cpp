#include <iostream>
#include <string>

int main() {
    std::string name;
    std::cout << "Name: ";
    std::getline(std::cin, name);  // 1 行を読み込む

    int age = 0;
    std::cout << "Age: ";
    std::cin >> age;               // 整数として読み込む

    std::cout << "Hello, " << name << " (" << age << ")" << '\n';
    return 0;
}
