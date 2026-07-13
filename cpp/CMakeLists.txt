cmake_minimum_required(VERSION 3.16)
project(visdrone_yolov11s LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# OpenCV
find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs)

# libdet shared library
set(LIBDET_SOURCES
    libdet/src/ax_devices.cpp
    libdet/src/libdet.cpp
    libdet/src/models/ax_model_base.cpp
    libdet/src/runner/ax650/ax_model_runner_ax650.cpp
    libdet/src/runner/axcl/ax_model_runner_axcl.cpp
    libdet/src/runner/axcl/axcl_manager.cpp
    libdet/src/utils/enum_devices.cpp
)

add_library(det SHARED ${LIBDET_SOURCES})
target_include_directories(det PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/include
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/src
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/src/models
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/src/runner
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/src/runner/ax650
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/src/runner/axcl
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/src/runner/ax_type_header
    ${CMAKE_CURRENT_SOURCE_DIR}/libdet/src/utils
    ${OpenCV_INCLUDE_DIRS}
)
target_link_libraries(det ${OpenCV_LIBS} pthread dl)

# Example binary
add_executable(visdrone_detect examples/visdrone_detect.cpp)
target_link_libraries(visdrone_detect det ${OpenCV_LIBS})

# Install
install(TARGETS det LIBRARY DESTINATION lib)
install(TARGETS visdrone_detect RUNTIME DESTINATION bin)
install(FILES
    libdet/include/libdet.h
    libdet/include/ax_devices.h
    DESTINATION include)
