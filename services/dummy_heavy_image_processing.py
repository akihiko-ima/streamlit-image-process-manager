import cv2
import numpy as np
import time


def dummy_heavy_image_processing(image: np.ndarray) -> np.ndarray:
    """dummyの重たい画像処理をソーベルフィルターとタイマーで実装"""
    time.sleep(5)

    image = cv2.medianBlur(image, 5)
    sobel_x = cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3)

    sobel_x = cv2.convertScaleAbs(sobel_x)
    sobel_y = cv2.convertScaleAbs(sobel_y)

    sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)

    return sobel_combined
