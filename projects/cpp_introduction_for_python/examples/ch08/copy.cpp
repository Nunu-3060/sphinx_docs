#include <iostream>
#include <vector>

int main() {
    std::vector<int> a = {1, 2, 3};
    std::vector<int> b = a;  // 要素がすべてコピーされる
    b.push_back(4);
    std::cout << a.size() << ' ' << b.size() << '\n';  // 3 4

    std::vector<int>& c = a;  // c は a の別名
    c.push_back(4);
    std::cout << a.size() << ' ' << c.size() << '\n';  // 4 4
    return 0;
}
