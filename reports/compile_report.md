# Compile Report: VisDrone YOLO11s

## 编译概览
- 量化: INT8 (PerLayer MinMax)
- 校准: 33张 VisDrone 真实航拍图
- 校准归一化: mean=[0,0,0], std=[255,255,255] → ONNX 输入 [0,1]
- MACs: 20.66G
- AXMODEL: 10.2 MB

## 精度
| 输出层 | Cosine | MSE |
|--------|--------|-----|
| output0 (80×80) | 0.99999 | 0.005 |
| output1 (40×40) | 1.00000 | 0.004 |
| output2 (20×20) | 0.99999 | 0.004 |
