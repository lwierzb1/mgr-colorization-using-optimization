#!/usr/bin/env python
"""General purpose functions useful for image processing.
"""

import cv2
import numpy as np

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def gaussian_blur(image):
    return cv2.GaussianBlur(image, (11, 11), 0)


def write_image(image, path):
    cv2.imwrite(path, image)


def read_image(path):
    return cv2.imread(path)


def bgr_as_float_matrix(bgr):
    """Returns float matrix representation of image specified with path.
    Normalization will help to remove distortions caused by lights and shadows in an image.

    path: Path to image. data. It can be absolute or relative.
    """

    return bgr.astype(np.float32) / 255.


def bgr_to_yuv_channels(matrix):
    """Returns YUV space channels representation of matrix in BGR space.

    matrix: matrix of float in BGR color space.
    """
    yuv_matrix = cv2.cvtColor(matrix, cv2.COLOR_BGR2YUV)
    return cv2.split(yuv_matrix)


def yuv_channels_to_bgr_image(y_channel, u_channel, v_channel):
    """Returns image in BGR space created from YUV channels.

    y_channel: luminance channel.
    u_channel: color channel.
    v_channel: color channel.
    """
    yuv_image = cv2.merge((y_channel.astype(np.float32), u_channel.astype(np.float32), v_channel.astype(np.float32)))
    bgr_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)
    return bgr_image


def rgb_matrix_to_image(matrix):
    """Returns rgb image representation of float matrix.

    matrix: float matrix.
    """
    matrix = np.clip(matrix, 0, 1)
    rgb_image = (matrix * 255).astype("uint8")
    return rgb_image
