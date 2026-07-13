"""后处理模块: 在图像上绘制检测结果"""

import cv2
from typing import List

# VisDrone 2019 类别
CLASS_NAMES = [
    "pedestrian", "people", "bicycle", "car", "van",
    "truck", "tricycle", "awning-tricycle", "bus", "motor"
]

COLORS = [
    (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (128, 0, 128), (128, 128, 0),
    (0, 128, 128), (128, 0, 0)
]


def draw_detections(image_bgr, objects: List, threshold: float = 0.25) -> None:
    """在 BGR 图像上绘制检测框和标签（原地修改）。

    Args:
        image_bgr: BGR 格式图像 (numpy array)
        objects: AXDet.detect() 返回的 Object 列表
        threshold: 最低置信度阈值
    """
    for obj in objects:
        if obj.score < threshold:
            continue
        box = obj.box
        label = obj.label
        name = CLASS_NAMES[label] if label < len(CLASS_NAMES) else f"cls_{label}"
        color = COLORS[label % len(COLORS)]

        x1, y1, w, h = box
        x2, y2 = x1 + w, y1 + h

        cv2.rectangle(image_bgr, (x1, y1), (x2, y2), color, 2)
        text = f"{name} {obj.score:.2f}"
        cv2.putText(image_bgr, text, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
