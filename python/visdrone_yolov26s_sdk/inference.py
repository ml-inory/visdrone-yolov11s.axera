"""推理模块: 封装 libdet.axera 的 AXDet + 设备管理"""

import os
import numpy as np
from typing import List

from .pydet import AXDet, ModelType
from .pydet.pyaxdev import enum_devices, sys_init, sys_deinit, AxDeviceType


class VisDroneYOLODetector:
    """VisDrone YOLOv26s (YOLO11) 目标检测器。

    使用 libdet.axera 实现端到端推理（加载 AXMODEL + 推理 + decode/NMS）。

    Args:
        model_path: AXMODEL 文件路径
        num_classes: 类别数 (默认 10, VisDrone)
        threshold: 置信度阈值
    """

    def __init__(self, model_path: str, num_classes: int = 10,
                 threshold: float = 0.25):
        self.model_path = model_path
        self.num_classes = num_classes
        self.threshold = threshold
        self._detector = None
        self._dev_type = None
        self._dev_id = -1
        self._init_device()
        self._init_detector()

    def _init_device(self):
        devices_info = enum_devices()
        if devices_info['host']['available']:
            sys_init(AxDeviceType.host_device, -1)
            self._dev_type = AxDeviceType.host_device
            self._dev_id = -1
        elif devices_info['devices']['count'] > 0:
            sys_init(AxDeviceType.axcl_device, 0)
            self._dev_type = AxDeviceType.axcl_device
            self._dev_id = 0
        else:
            raise RuntimeError("No available AX device found")

    def _init_detector(self):
        self._detector = AXDet(
            model_path=self.model_path,
            model_type=ModelType.ax_det_model_type_yolo11,
            num_classes=self.num_classes,
            threshold=self.threshold,
            dev_type=self._dev_type,
            devid=self._dev_id,
        )

    def detect(self, image_rgb: np.ndarray) -> List:
        """对 RGB uint8 图像执行目标检测。

        Args:
            image_rgb: RGB 格式 uint8 numpy array, shape (H, W, 3)

        Returns:
            Object 列表，每个 Object 有 box=[x,y,w,h], score, label
        """
        return self._detector.detect(image_rgb)

    def __del__(self):
        if self._detector:
            del self._detector
        if self._dev_type is not None:
            sys_deinit(self._dev_type, self._dev_id)
