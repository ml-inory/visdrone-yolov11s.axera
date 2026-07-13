# VisDrone YOLO11s C++ SDK

基于 libdet.axera 的 VisDrone 航拍目标检测 C++ SDK。

## 环境要求

### 本机构建（仅验证编译）
- CMake >= 3.16
- gcc/g++ >= 9
- libopencv-dev

### 交叉编译（AX650 板端运行）
- AX650 BSP SDK V3.10.2
  - 下载: https://hf-mirror.com/AXERA-TECH/AX650-Community-Hub/resolve/main/sdk/edge-computing-AX650_SDK_V3.10.2/02.%20SDK/AX650_SDK_V3.10.2/AX650_SDK_V3.10.2_20260513151335.tgz

## 构建步骤

### 本机构建
```bash
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

### 交叉编译（AX650）
```bash
# 1. 安装 AX650 BSP SDK
wget <BSP_URL> -O AX650_SDK.tgz
tar xzf AX650_SDK.tgz -C /opt/

# 2. 编译
mkdir build_arm && cd build_arm
cmake .. \
  -DCMAKE_TOOLCHAIN_FILE=../toolchain-aarch64.cmake \
  -DAX_RUNTIME_ROOT=/opt/AX650_SDK_V3.10.2 \
  -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```

## 上板运行
```bash
scp build_arm/visdrone_detect user@board:~
scp model.axmodel user@board:~
ssh user@board
export LD_LIBRARY_PATH=/lib/firmware:$LD_LIBRARY_PATH
./visdrone_detect model.axmodel test.jpg 0.25
```

## API 说明

程序接收命令行参数:
```bash
./visdrone_detect <model.axmodel> <image.jpg> [threshold]
```

内部使用 libdet.axera C API (`ax_det_init` / `ax_det` / `ax_det_deinit`) 完成端到端检测。
libdet.axera 源码: https://github.com/AXERA-TECH/libdet.axera.git
