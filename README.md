# VisDrone YOLO11s — AX650 目标检测模型

基于 YOLO11 架构的航拍目标检测模型，在 VisDrone2019-DET 数据集上训练，部署于 AX650 NPU 芯片。

## 模型概述
| 项目 | 说明 |
|------|------|
| 任务类型 | 目标检测 (object-detection) |
| 目标芯片 | AX650 (NPU3) |
| 输入 | 640x640 RGB 图像, NHWC uint8 |
| 输出 | 检测框 (x,y,w,h), 类别, 置信度 |
| 类别 | pedestrian, people, bicycle, car, van, truck, tricycle, awning-tricycle, bus, motor |
| 推理延迟 | ~3.3 ms (AX650) |

## 目录说明
```
models/          AXMODEL 编译产物
demo/            5 张 VisDrone 真实航拍测试图像
python/          Python SDK (基于 libdet.axera)
cpp/             C++ SDK (基于 libdet.axera)
model_convert/   从零复现模型转换的完整脚本和配置
reports/         编译、仿真、板端测试报告
```

## 快速开始

### 路径 A: 直接用 AXMODEL 推理

测试图像: `demo/` 目录下有 5 张 VisDrone 真实航拍图像。

#### Python
```bash
cd python

# 1. 安装依赖
pip install -r requirements.txt

# 2. 安装 pyaxengine
git clone https://github.com/AXERA-TECH/pyaxengine.git
pip install ./pyaxengine

# 3. 编译 libdet.axera (后处理库)
git clone https://github.com/AXERA-TECH/libdet.axera.git
cd libdet.axera
sudo apt install libopencv-dev build-essential
./build.sh
export LD_LIBRARY_PATH=$(pwd)/build/lib:${LD_LIBRARY_PATH}
cd ..

# 4. 运行
python example.py \
  --model ../models/model.axmodel \
  --image ../demo/demo_00.jpg
```

#### C++
```bash
cd cpp

# 本机构建 (仅验证编译)
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# 交叉编译 (AX650, 需 BSP SDK)
mkdir build_arm && cd build_arm
cmake .. \
  -DCMAKE_TOOLCHAIN_FILE=../toolchain-aarch64.cmake \
  -DAX_RUNTIME_ROOT=/opt/AX650_SDK_V3.10.2 \
  -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)

# 上板运行
scp visdrone_detect root@board:~/
scp ../../models/model.axmodel root@board:~/
scp ../../demo/demo_00.jpg root@board:~/
ssh root@board
export LD_LIBRARY_PATH=/lib/firmware:$LD_LIBRARY_PATH
./visdrone_detect model.axmodel demo_00.jpg 0.25
```

### 路径 B: 从零复现模型转换
参见 [model_convert/README.md](model_convert/README.md)

## 性能摘要
参见 [reports/performance_report.md](reports/performance_report.md)
- 推理延迟: ~3.3 ms (AX650)
- AXMODEL 大小: 10.1 MB
- MACs: 10.4 G
- 校准数据: 10 张 VisDrone 真实航拍图像

## 已知限制
- 输入分辨率固定为 640x640
- batch size 固定为 1
