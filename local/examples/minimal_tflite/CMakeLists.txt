cmake_minimum_required(VERSION 3.16)
project(minimal_tflite)

set(CMAKE_CXX_STANDARD 17)

# 查找LiteRT/TFLite依赖
find_package(TensorFlowLite REQUIRED)

add_executable(minimal_tflite minimal_tflite.cpp)
target_link_libraries(minimal_tflite tensorflow-lite)
