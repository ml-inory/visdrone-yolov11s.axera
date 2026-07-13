# VisDrone YOLO11s Python SDK

基于 libdet.axera 的 VisDrone 航拍目标检测 Python SDK。

## 目录结构
```
python/
  example.py                         # 推理示例入口
  requirements.txt                   # Python 依赖
  visdrone_yolo11s_sdk/             # SDK 包
    __init__.py
    inference.py                     # VisDroneYOLODetector 类
    preprocess.py                    # 图像预处理
    postprocess.py                   # 检测结果绘制
    pydet/                           # libdet.axera Python 绑定
```

## 环境要求
- Python >= 3.8
- libopencv-dev（系统级，用于 libdet.axera 编译）
- AX 板端或 AX650 主机环境

## 安装步骤

### 1. 安装 Python 依赖
```bash
cd python
pip install -r requirements.txt
```

### 2. 安装 pyaxengine
```bash
git clone https://github.com/AXERA-TECH/pyaxengine.git
pip install ./pyaxengine
```

### 3. 编译 libdet.axera（后处理库）
```bash
git clone https://github.com/AXERA-TECH/libdet.axera.git
cd libdet.axera
sudo apt install libopencv-dev build-essential
./build.sh
export LD_LIBRARY_PATH=$(pwd)/build/lib:${LD_LIBRARY_PATH}
cd ..
```

## 快速运行
```bash
cd python
python example.py \
  --model ../models/model.axmodel \
  --image ../demo/demo_00.jpg
```

## API 说明

### VisDroneYOLODetector
```python
from visdrone_yolo11s_sdk import VisDroneYOLODetector

detector = VisDroneYOLODetector(
    model_path="model.axmodel",
    num_classes=10,
    threshold=0.25,
)
objects = detector.detect(image_rgb_uint8)
# objects: list of Object(box=[x,y,w,h], score=float, label=int)
```

## 输入预处理
- resize 到 640x640
- BGR → RGB 转换
- 保持 uint8 格式（不做归一化）
