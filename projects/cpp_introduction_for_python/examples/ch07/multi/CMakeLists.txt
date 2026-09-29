cmake_minimum_required(VERSION 3.16)
project(geometry_demo LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(geometry_demo main.cpp geometry.cpp)

if(MSVC)
    target_compile_options(geometry_demo PRIVATE /W4 /utf-8)
else()
    target_compile_options(geometry_demo PRIVATE -Wall -Wextra)
endif()
