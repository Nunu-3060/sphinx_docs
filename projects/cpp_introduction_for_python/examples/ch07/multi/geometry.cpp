#include "geometry.h"

constexpr double pi = 3.141592653589793;

double circle_area(double radius) {
    return pi * radius * radius;
}

double rectangle_area(double width, double height) {
    return width * height;
}
