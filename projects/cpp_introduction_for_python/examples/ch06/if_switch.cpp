#include <iostream>

int main() {
    int score = 75;

    if (score >= 80) {
        std::cout << "A\n";
    } else if (score >= 60) {
        std::cout << "B\n";
    } else {
        std::cout << "C\n";
    }

    int day = 3;
    switch (day) {
    case 0:
        std::cout << "Sunday\n";
        break;
    case 6:
        std::cout << "Saturday\n";
        break;
    default:
        std::cout << "Weekday\n";
        break;
    }
    return 0;
}
