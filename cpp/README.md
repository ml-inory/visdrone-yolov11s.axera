# VisDrone YOLO11s C++ SDK

预编译的 C++ 推理库和可执行程序，基于 libdet.axera。

## 文件说明
```
bin/visdrone_detect    可执行程序（aarch64，开箱即用）
lib/libdet.so          共享库（aarch64，OpenCV 静态链接）
include/libdet.h       C API 头文件
include/ax_devices.h   设备枚举头文件
```

## 运行依赖
板端运行时库（板端已预装）:
- `/soc/lib/libax_engine.so`
- `/soc/lib/libax_sys.so`

## 用法

### 直接运行
```bash
chmod +x bin/visdrone_detect
LD_LIBRARY_PATH=/soc/lib ./bin/visdrone_detect model.axmodel image.jpg 0.25
```

### 集成到自己的项目
```cpp
#include "libdet.h"

ax_det_init_t init = {};
init.dev_type = axcl_device;
init.model_type = ax_det_model_type_yolo11;
sprintf(init.model_path, "model.axmodel");
init.num_classes = 10;
init.threshold = 0.25f;

ax_det_handle_t handle;
ax_det_init(&init, &handle);

// 加载 cv::Mat 图像 (RGB uint8), resize 到 640x640
ax_det_img_t img = {.data = rgb_data, .width = 640, .height = 640,
                    .channels = 3, .stride = 640 * 3};
ax_det_result_t result;
ax_det(handle, &img, &result);

ax_det_deinit(handle);
```

编译:
```bash
aarch64-none-linux-gnu-g++ -std=c++17 \
  -I include -L lib -o my_detect my_detect.cpp \
  -ldet -lpthread -ldl
```

## 编译（如需）
源码和 CMakeLists.txt 见: https://github.com/ml-inory/visdrone-yolov11s.axera
交叉编译依赖:
- AX650 BSP SDK V3.10.2（OpenCV 4.5.5 aarch64）
- aarch64-none-linux-gnu-g++ 9.2+
