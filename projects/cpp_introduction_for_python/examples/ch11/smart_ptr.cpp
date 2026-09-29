#include <iostream>
#include <memory>
#include <utility>

struct Data {
    int value = 0;
};

int main() {
    std::unique_ptr<Data> p = std::make_unique<Data>();
    p->value = 42;
    // std::unique_ptr<Data> q = p;          // エラー: コピーできない
    std::unique_ptr<Data> q = std::move(p);  // 所有権を q に移す
    std::cout << (p == nullptr) << ' ' << q->value << '\n';  // 1 42

    std::shared_ptr<Data> s1 = std::make_shared<Data>();
    {
        std::shared_ptr<Data> s2 = s1;        // 所有権を共有する
        std::cout << s1.use_count() << '\n';  // 2
    }
    std::cout << s1.use_count() << '\n';      // 1
    return 0;
}  // 所有者がいなくなった時点で、オブジェクトは自動的に解放される
