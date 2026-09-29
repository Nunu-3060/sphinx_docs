#include <iostream>

class Point {
public:
    Point(double x, double y) : x_(x), y_(y) {}  // コンストラクター

    double x() const { return x_; }
    double y() const { return y_; }

    void move(double dx, double dy) {
        x_ += dx;
        y_ += dy;
    }

    Point operator+(const Point& other) const {
        return Point(x_ + other.x_, y_ + other.y_);
    }

private:
    double x_;
    double y_;
};

std::ostream& operator<<(std::ostream& os, const Point& p) {
    return os << "(" << p.x() << ", " << p.y() << ")";
}

int main() {
    Point p(1.0, 2.0);
    p.move(0.5, 0.5);
    Point q = p + Point(10.0, 10.0);
    std::cout << p << ' ' << q << '\n';  // (1.5, 2.5) (11.5, 12.5)
    return 0;
}
