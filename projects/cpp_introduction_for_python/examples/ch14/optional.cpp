#include <iostream>
#include <optional>
#include <string>
#include <vector>

std::optional<std::size_t> find_index(const std::vector<std::string>& names,
                                      const std::string& target) {
    for (std::size_t i = 0; i < names.size(); ++i) {
        if (names[i] == target) {
            return i;
        }
    }
    return std::nullopt;  // Python の return None に相当
}

int main() {
    std::vector<std::string> names = {"Alice", "Bob"};

    if (auto index = find_index(names, "Bob")) {
        std::cout << "found at " << *index << '\n';  // found at 1
    }

    auto missing = find_index(names, "Carol");
    std::cout << std::boolalpha << missing.has_value() << '\n';  // false
    std::cout << missing.value_or(999) << '\n';                  // 999
    return 0;
}
