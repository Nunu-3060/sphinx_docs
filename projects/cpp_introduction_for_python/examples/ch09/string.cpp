#include <iostream>
#include <string>

int main() {
    std::string s = "Hello";
    s += ", World";                   // 連結
    std::cout << s << '\n';           // Hello, World
    std::cout << s.size() << '\n';    // 12
    std::cout << s.substr(0, 5) << '\n';  // Hello

    std::size_t pos = s.find("World");
    if (pos != std::string::npos) {
        std::cout << pos << '\n';     // 7
    }

    s[0] = 'J';                       // 文字列を直接変更できる
    std::cout << s << '\n';           // Jello, World

    int n = std::stoi("42");                // 文字列から整数へ変換する
    std::string t = std::to_string(n + 1);  // 整数から文字列へ変換する
    std::cout << t << '\n';                 // 43
    return 0;
}
