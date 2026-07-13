#!/bin/bash
# Pulsar2 编译脚本: 将 model.onnx 编译为 model.axmodel
# 前置条件: Docker 已安装，Pulsar2 镜像已加载
# 用法: ./compile_pulsar2.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Pulsar2 编译 VisDrone YOLOv26s ==="

# 检查 Docker
if ! command -v docker &>/dev/null; then
    echo "ERROR: Docker not installed"
    exit 1
fi

# 检查 Pulsar2 镜像
PULSAR_IMAGE="pulsar2:6.0-lite"
if ! docker images -q "$PULSAR_IMAGE" >/dev/null 2>&1; then
    echo "Pulsar2 镜像未找到。请从 HuggingFace 下载并加载:"
    echo "  wget https://hf-mirror.com/AXERA-TECH/Pulsar2/resolve/main/6.0/ax_pulsar2_6.0.tar.gz"
    echo "  docker load < ax_pulsar2_6.0.tar.gz"
    exit 1
fi

# 检查输入文件
if [ ! -f "model.onnx" ]; then
    echo "ERROR: model.onnx not found. Run export_onnx.py first."
    exit 1
fi

if [ ! -f "calib_data.tar" ]; then
    echo "WARNING: calib_data.tar not found. Using random calibration data."
fi

# 运行编译
docker run --rm \
    -v "$(pwd):/workspace" \
    -w /workspace \
    "$PULSAR_IMAGE" \
    pulsar2 build --config pulsar2_config.json

echo ""
echo "=== Compilation Complete ==="
echo "Output: $(pwd)/compile/model.axmodel"
ls -lh compile/model.axmodel
