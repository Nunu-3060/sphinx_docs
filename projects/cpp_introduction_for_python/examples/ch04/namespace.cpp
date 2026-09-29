#include <iostream>

namespace geometry {

const double pi = 3.14159;

double circle_area(double r) {
    return pi * r * r;
}

}  // namespace geometry

int main() {
    std::cout << geometry::circle_area(2.0) << '\n';
    return 0;
}
