#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> ages = {{"Alice", 30}, {"Bob", 25}};
    ages["Carol"] = 35;  // 要素を追加する

    std::cout << ages["Alice"] << '\n';  // 30
    std::cout << ages.size() << '\n';    // 3

    // Python: if "Dave" not in ages:
    if (ages.count("Dave") == 0) {
        std::cout << "Dave not found\n";
    }

    std::cout << ages["Dave"] << '\n';  // 0（値が 0 の要素が追加される）
    std::cout << ages.size() << '\n';   // 4

    for (const auto& [name, age] : ages) {  // 構造化束縛
        std::cout << name << ": " << age << '\n';
    }
    return 0;
}
