# VisDrone YOLO11s — AX650 目标检测模型

基于 YOLO11s 架构，[VisDrone2019-DET](https://hf-mirror.com/datasets/Voxel51/VisDrone2019-DET) 数据集训练，编译为 AX650 AXMODEL。

预编译二进制和模型下载：[HuggingFace](https://hf-mirror.com/AXERA-TECH/visdrone-yolov11s) | [GitHub Releases](../../releases)

![Detection Result](result.jpg)

## 模型信息

| 项目 | 值 |
|------|-----|
| 架构 | YOLO11s |
| 类别数 | 11 (含背景) |
| 类别 | pedestrian, people, bicycle, car, van, truck, tricycle, awning-tricycle, bus, motor |
| 输入 | 640×640 BGR → [0,1] float |
| 芯片 | AX650N (NPU3) |
| 量化 | INT8 |
| AXMODEL | 10.2 MB |
| 精度 | Cosine >0.99999, MSE <0.006 |

## 目录

```
models/             AXMODEL
demo/               测试图
cpp/                C++ 源码 + CMake (FetchContent → libdet.axera)
python/             Python SDK (pydet)
model_convert/      模型转换脚本 & 配置
reports/            编译/仿真/板端报告
```

## 快速开始

### 预编译二进制 (推荐)

从 [GitHub Releases](../../releases) 或 [HuggingFace](https://hf-mirror.com/AXERA-TECH/visdrone-yolov11s) 下载 `visdrone_detect` 和 `libdet.so`，直接在板上运行：

```bash
LD_LIBRARY_PATH=./lib:/soc/lib ./visdrone_detect model.axmodel demo_00.jpg
```

### 从源码编译

```bash
cd cpp
mkdir build && cd build
cmake .. -DCMAKE_TOOLCHAIN_FILE=../toolchain-aarch64.cmake \
         -DAX_RUNTIME_ROOT=/path/to/AX650_SDK
make -j$(nproc)
# 产出: libdet.so + visdrone_detect
```

### Python

```bash
cd python
pip install -r requirements.txt
python example.py --model ../models/model.axmodel --image ../demo/demo_00.jpg
```

### 重编译模型

参见 `model_convert/` 目录。

## 精度

| 输出层 | Cosine | MSE |
|--------|--------|-----|
| output0 (80×80) | 0.99999 | 0.005 |
| output1 (40×40) | 1.00000 | 0.004 |
| output2 (20×20) | 0.99999 | 0.004 |

## 限制

- 输入固定 640×640, batch=1
- 需 AX650 BSP SDK 3.10.2+ 运行时
