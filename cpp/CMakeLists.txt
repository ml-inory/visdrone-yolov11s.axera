cmake_minimum_required(VERSION 3.16)
project(visdrone_yolov26s_sdk LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# libdet.axera integration via FetchContent
include(FetchContent)
FetchContent_Declare(
    libdet
    GIT_REPOSITORY https://github.com/AXERA-TECH/libdet.axera.git
    GIT_TAG main
)
FetchContent_MakeAvailable(libdet)

# Example application
add_executable(visdrone_detect examples/visdrone_detect.cpp)
target_link_libraries(visdrone_detect det ${OpenCV_LIBS})

# Install
install(TARGETS visdrone_detect DESTINATION bin)
