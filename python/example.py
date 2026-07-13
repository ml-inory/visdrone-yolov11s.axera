#!/usr/bin/env python3
"""VisDrone YOLOv26s 检测示例。

用法:
    python example.py --model ../models/model.axmodel --image ../demo/demo_00.jpg
"""

import argparse
import sys
import cv2

from visdrone_yolov26s_sdk import VisDroneYOLODetector
from visdrone_yolov26s_sdk.preprocess import preprocess_image
from visdrone_yolov26s_sdk.postprocess import draw_detections


def main():
    parser = argparse.ArgumentParser(description="VisDrone YOLOv26s Detection Demo")
    parser.add_argument("--model", required=True, help="Path to model.axmodel")
    parser.add_argument("--image", required=True, help="Path to input image")
    parser.add_argument("--threshold", type=float, default=0.25, help="Detection threshold")
    parser.add_argument("--output", default="result.jpg", help="Output image path")
    args = parser.parse_args()

    print(f"Loading image: {args.image}")
    img_rgb = preprocess_image(args.image, target_size=640)

    print(f"Loading model: {args.model}")
    detector = VisDroneYOLODetector(
        model_path=args.model,
        num_classes=10,
        threshold=args.threshold,
    )

    print("Running detection...")
    objects = detector.detect(img_rgb)

    print(f"Found {len(objects)} objects")
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    draw_detections(img_bgr, objects, threshold=args.threshold)

    cv2.imwrite(args.output, img_bgr)
    print(f"Result saved to: {args.output}")

    for obj in objects:
        if obj.score >= args.threshold:
            print(f"  [{obj.label}] {obj.score:.3f} box={obj.box}")


if __name__ == "__main__":
    main()
