# Run-on-Board Report: VisDrone YOLO11s

## 板端信息
- 板子: 10.168.232.116 (ax650, AX650N_CHIP)
- 引擎版本: 2.10.1s
- 工具版本: 2.5.0a

## Smoke Check (ax_run_model)

### 加载验证
- axmodel 成功加载
- 类型: 3 Core
- CMM 大小: 10,625,057 bytes (~10.1 MB)

### 推理延迟
| 指标 | 值 |
|------|-----|
| Min | 3.252 ms |
| Max | 3.271 ms |
| Avg | 3.262 ms |
| 重复次数 | 10 (warmup=3) |

## 备注
- ax_run_model smoke check 仅验证模型可正常加载和推理
- 完整 SDK 推理验证将在 PACKAGE 阶段板端自验证中执行
- Python/C++ SDK 延迟预期与 smoke check 相近
