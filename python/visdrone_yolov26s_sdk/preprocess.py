"""预处理模块: BGR图像 -> RGB uint8 numpy array"""

import cv2
import numpy as np


def preprocess_image(image_path: str, target_size: int = 640) -> np.ndarray:
    """加载图像并转换为 RGB uint8 格式。

    Args:
        image_path: 图像文件路径
        target_size: resize 目标尺寸 (宽高相等)

    Returns:
        RGB uint8 numpy array, shape (target_size, target_size, 3)
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")
    img = cv2.resize(img, (target_size, target_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img
