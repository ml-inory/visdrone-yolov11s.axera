# Performance Report: VisDrone YOLO11s

## 流水线耗时
| 阶段 | 耗时 |
|------|------|
| ACQUIRE | ~32s |
| EXPORT | ~12s |
| COMPILE | ~91s |
| SIMULATE | ~58s |
| RUNONBOARD | ~3s |
| PACKAGE | ~5s |

## 模型效率
- ONNX 大小: 37.0 MB
- AXMODEL 大小: 10.1 MB
- 压缩比: 3.57:1
- MACs: 10.39 G

## 推理延迟
| 方法 | 延迟 |
|------|------|
| 板端 ax_run_model | 3.26 ms (avg, 10 runs) |

## 板端内存
- CMM 占用: 10.1 MB

## 精度汇总
| 输出层 | 精度分析 Cosine |
|--------|----------------|
| output0 | 0.99993 |
| output1 | 0.99998 |
| output2 | 0.99998 |

校准数据: 10 张 VisDrone 真实航拍图像
