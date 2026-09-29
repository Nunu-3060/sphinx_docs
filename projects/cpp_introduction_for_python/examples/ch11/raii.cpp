#include <iostream>
#include <string>

class Resource {
public:
    Resource(const std::string& name) : name_(name) {
        std::cout << "acquire " << name_ << '\n';
    }
    ~Resource() {
        std::cout << "release " << name_ << '\n';
    }

private:
    std::string name_;
};

int main() {
    Resource a("a");
    {
        Resource b("b");
        std::cout << "inside block\n";
    }  // ここで b のデストラクターが呼ばれる
    std::cout << "end of main\n";
    return 0;
}  // ここで a のデストラクターが呼ばれる
