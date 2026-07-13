# Model Convert: VisDrone YOLO11s

本文档指导从 ONNX 导出到 AXMODEL 编译的完整复现流程。

## 概述
- 模型: VisDrone YOLO11s (YOLO11 架构)
- 目标芯片: AX650 (NPU3 模式)
- 输入: 640x640 RGB 图像, NHWC uint8
- 类别: 10 (VisDrone 2019-DET)

## 前置条件
- Python >= 3.8
- Docker
- 磁盘空间: ~5 GB

## 1. 环境准备

### Python 环境
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Pulsar2 环境
从 HuggingFace 下载 Pulsar2 Docker 镜像并通过 docker load 导入:
```bash
# 镜像列表: https://hf-mirror.com/AXERA-TECH/Pulsar2/tree/main
wget https://hf-mirror.com/AXERA-TECH/Pulsar2/resolve/main/6.0/ax_pulsar2_6.0.tar.gz
docker load < ax_pulsar2_6.0.tar.gz
```

验证环境:
```bash
python --version
docker --version
docker images | grep pulsar2
pip list | grep onnx
```

## 2. ONNX 导出

从原始 PyTorch 权重导出 ONNX:
```bash
# 下载原始模型权重
# wget https://hf-mirror.com/dronefreak/visdrone-yolo11s/resolve/main/best.pt

python export_onnx.py --weights best.pt --output model.onnx
```

验证导出:
```bash
ls -lh model.onnx
python -c "import onnx; onnx.checker.check_model('model.onnx'); print('OK')"
```

## 3. 校准数据准备

```bash
# 校准数据需为 640x640 PNG 格式 RGB 图像
# 推荐使用 VisDrone 真实航拍图像
tar cf calib_data.tar /path/to/calib/images/*.png
```

如使用随机数据:
```bash
python -c "
import numpy as np
from PIL import Image
import tarfile, os
os.makedirs('calib_tmp', exist_ok=True)
for i in range(10):
    img = Image.fromarray(np.random.randint(0, 256, (640, 640, 3), dtype=np.uint8))
    img.save(f'calib_tmp/calib_{i:04d}.png')
with tarfile.open('calib_data.tar', 'w') as tar:
    for f in os.listdir('calib_tmp'):
        tar.add(f'calib_tmp/{f}')
"
```

## 4. Pulsar2 编译

```bash
./compile_pulsar2.sh
```

关键配置项 (pulsar2_config.json):
- target_hardware: AX650
- npu_mode: NPU3
- calibration_method: MinMax
- 校准数据输入: NHWC uint8, mean=[0,0,0], std=[1,1,1]

预期产物: compile/model.axmodel (~10 MB)

## 5. 产物检查
| 文件 | 用途 | 预期大小 |
|------|------|----------|
| model.onnx | 浮点 ONNX 模型 | ~36 MB |
| compile/model.axmodel | 芯片可部署模型 | ~10 MB |

## 6. 常见问题

**编译失败: unsupport archive format**
→ 确保 calib_data.tar 包含 PNG 格式图像

**Docker 未启动**
```bash
sudo systemctl start docker
```

**Pulsar2 镜像不存在**
```bash
wget https://hf-mirror.com/AXERA-TECH/Pulsar2/resolve/main/6.0/ax_pulsar2_6.0.tar.gz
docker load < ax_pulsar2_6.0.tar.gz
```

**OOM 错误**
→ 减小 calibration_size 或增加 Docker 内存限制
