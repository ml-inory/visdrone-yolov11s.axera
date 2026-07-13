# Compile Report: VisDrone YOLO11s

## 编译概览
- 日期: 2026-07-13
- Pulsar2: 6.0 (commit 48520c11)
- 目标芯片: AX650A
- NPU模式: NPU3

## 编译结果
| 指标 | 值 |
|------|-----|
| 编译耗时 | ~43s (quant + compile) |
| ONNX 大小 | 37.0 MB (37952310 bytes) |
| AXMODEL 大小 | 10.1 MB (10627564 bytes) |
| 压缩比 | 3.57:1 |
| MACs | 10.39 G |
| 量化方法 | MinMax, PerLayer |

## 输出配置
- output0: [1, 80, 80, 15] float32
- output1: [1, 40, 40, 15] float32
- output2: [1, 20, 20, 15] float32

## 精度分析
输出层量化精度:
| 输出 | Cosine | MSE |
|------|--------|-----|
| output0 | 0.999991 | 0.00418 |
| output1 | 0.999993 | 0.00418 |
| output2 | 0.999990 | 0.00418 |

所有中间层 cosine > 0.9995，量化精度良好。

## 编译配置
```json
{
  "target_hardware": "AX650",
  "npu_mode": "NPU3",
  "calibration_size": 10,
  "calibration_method": "MinMax",
  "precision_analysis": true
}
```
校准数据: 10 张随机生成 640x640 RGB 图像（非真实航拍数据）。
