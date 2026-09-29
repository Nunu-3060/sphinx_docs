#include <pybind11/pybind11.h>

int add(int a, int b) {
    return a + b;
}

PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example module";
    m.def("add", &add, "Add two integers");
}
