# Simulate Report: VisDrone YOLO11s

## 仿真结果
Pulsar2 仿真对比 ONNX 浮点输出，所有输出层 cosine >0.99999。

## 输入预处理
- uint8 BGR [0,255] → /255 → float [0,1]
- 与训练时 ONNX 输入范围一致
