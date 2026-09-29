#include <iostream>
#include <string>

template <typename T>
T max_value(T a, T b) {
    return (a > b) ? a : b;
}

template <typename T>
class Box {
public:
    Box(T value) : value_(value) {}
    T get() const { return value_; }

private:
    T value_;
};

int main() {
    std::cout << max_value(3, 7) << '\n';      // 7
    std::cout << max_value(2.5, 1.5) << '\n';  // 2.5
    std::cout << max_value(std::string("apple"), std::string("banana")) << '\n';  // banana

    Box<int> b1(42);
    Box<std::string> b2("hello");
    std::cout << b1.get() << ' ' << b2.get() << '\n';  // 42 hello
    return 0;
}
