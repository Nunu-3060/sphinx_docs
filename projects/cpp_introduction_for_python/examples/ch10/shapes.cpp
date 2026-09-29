#include <iostream>

class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;  // 純粋仮想関数
};

class Rectangle : public Shape {
public:
    Rectangle(double w, double h) : w_(w), h_(h) {}
    double area() const override { return w_ * h_; }

private:
    double w_;
    double h_;
};

class Circle : public Shape {
public:
    Circle(double r) : r_(r) {}
    double area() const override { return 3.141592653589793 * r_ * r_; }

private:
    double r_;
};

void print_area(const Shape& shape) {
    std::cout << shape.area() << '\n';  // 実際の型に応じた area が呼ばれる
}

int main() {
    Rectangle r(2.0, 3.0);
    Circle c(1.0);
    print_area(r);  // 6
    print_area(c);  // 3.14159
    return 0;
}
