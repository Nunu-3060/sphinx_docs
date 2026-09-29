#include <iostream>
#include <vector>

int main() {
    // Python: for i in range(5):
    for (int i = 0; i < 5; ++i) {
        std::cout << i << ' ';
    }
    std::cout << '\n';

    // Python: for x in values:
    std::vector<int> values = {10, 20, 30};
    for (int x : values) {
        std::cout << x << ' ';
    }
    std::cout << '\n';

    int n = 1;
    while (n < 100) {
        n *= 2;
    }
    std::cout << n << '\n';

    for (int i = 0; i < 10; ++i) {
        if (i % 2 == 0) {
            continue;  // 偶数は飛ばす
        }
        if (i > 7) {
            break;     // 7 より大きくなったら終了する
        }
        std::cout << i << ' ';
    }
    std::cout << '\n';
    return 0;
}
