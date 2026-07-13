#!/usr/bin/env python3
"""Export VisDrone YOLOv26s (YOLO11 architecture) to static ONNX with 3 feature map outputs.

Outputs: 3 tensors in NHWC format [1, H, W, 15] where 15 = 4 (bbox) + 11 (classes).
This format is compatible with libdet.axera (model_type=3, ax_det_model_type_yolo11).

Usage:
    python export-static-onnx.py --weights best.pt --output model.onnx
"""
import argparse, os, torch, onnx, numpy as np
from ultralytics import YOLO
import onnxslim

class YOLO11DetectHeadExport(torch.nn.Module):
    """Export YOLO11 with 3 separate detection head outputs in NHWC format."""
    def __init__(self, model):
        super().__init__()
        self.layers = list(model.model)
        self.save = model.save
        self.detect_idx = len(self.layers) - 1
        self.detect = self.layers[-1]

    def forward(self, x):
        y = []
        for i, m in enumerate(self.layers):
            if i == self.detect_idx:
                x = [y[fi] for fi in m.f]
                outputs = []
                for j in range(self.detect.nl):
                    bbox = self.detect.cv2[j](x[j])
                    cls = self.detect.cv3[j](x[j])
                    out = torch.cat([bbox, cls], dim=1)
                    out = out.permute(0, 2, 3, 1)
                    outputs.append(out)
                return tuple(outputs)
            if m.f != -1:
                x = y[m.f] if isinstance(m.f, int) else [x if j == -1 else y[j] for j in m.f]
            x = m(x)
            y.append(x if i in self.save else None)
        return x

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', required=True, help='Path to best.pt')
    parser.add_argument('--output', default='model.onnx', help='Output ONNX path')
    parser.add_argument('--imgsz', type=int, default=640, help='Input size')
    args = parser.parse_args()

    model = YOLO(args.weights)
    orig = model.model
    orig.eval()
    export_model = YOLO11DetectHeadExport(orig)

    dummy = torch.randn(1, 3, args.imgsz, args.imgsz)
    with torch.no_grad():
        _ = export_model(dummy)

    torch.onnx.export(
        export_model, dummy, args.output,
        input_names=['images'],
        output_names=['output0', 'output1', 'output2'],
        opset_version=18,
        do_constant_folding=True,
        dynamic_axes={},
    )

    m = onnx.load(args.output)
    m = onnxslim.slim(m)
    onnx.save(m, args.output)

    onnx.checker.check_model(args.output)
    print(f"Exported: {args.output} ({os.path.getsize(args.output)/1024/1024:.1f} MB)")

if __name__ == '__main__':
    main()
