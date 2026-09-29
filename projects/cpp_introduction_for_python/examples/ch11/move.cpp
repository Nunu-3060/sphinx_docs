#include <iostream>
#include <string>
#include <utility>
#include <vector>

int main() {
    std::vector<std::string> names;
    std::string first = "Alice";
    std::string second = "Bob";

    names.push_back(first);              // コピー: first の値はそのまま残る
    names.push_back(std::move(second));  // ムーブ: second の中身が names に移される

    std::cout << first << '\n';         // Alice
    std::cout << names.size() << '\n';  // 2
    // ムーブ後の second の値は未規定なので、再代入するまで使わない
    return 0;
}
