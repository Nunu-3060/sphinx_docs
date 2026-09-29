#include <iostream>
#include <limits>
#include <string>

int main() {
    int count = 10;
    double ratio = 0.5;
    bool ok = true;
    char initial = 'A';
    std::string name = "Alice";

    std::cout << count << ' ' << ratio << ' ' << ok << ' ' << initial << ' ' << name << '\n';

    std::cout << "sizeof(int): " << sizeof(int) << '\n';
    std::cout << "int max: " << std::numeric_limits<int>::max() << '\n';
    std::cout << "int min: " << std::numeric_limits<int>::min() << '\n';
    return 0;
}
