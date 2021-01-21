#!/usr/bin/env python
"""General purpose functions useful for image processing.
"""

import cv2
import numpy as np

__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"


def read_as_float_matrix(path):
    """Returns float matrix representation of image specified with path.
    Normalization will help to remove distortions caused by lights and shadows in an image.

    path: Path to image. data. It can be absolute or relative.
    """

    bgr_image = cv2.imread(path)
    return bgr_image.astype(np.float32) / 255.


def bgr_to_yuv_channels(matrix):
    """Returns YUV space channels representation of matrix in BGR space.

    matrix: matrix of float in BGR color space.
    """
    yuv_matrix = cv2.cvtColor(matrix, cv2.COLOR_BGR2YUV)
    return cv2.split(yuv_matrix)


def yuv_channels_to_rgb_image(y_channel, u_channel, v_channel):
    """Returns image in RGB space created from YUV channels.

    y_channel: luminance channel.
    u_channel: color channel.
    v_channel: color channel.
    """
    yuv_image = cv2.merge((y_channel.astype(np.float32), u_channel.astype(np.float32), v_channel.astype(np.float32)))
    rgb_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)
    return rgb_image


def rgb_matrix_to_image(matrix):
    """Returns rgb image representation of float matrix.

    matrix: float matrix.
    """

    rgb_image = (matrix * 255).astype(np.int)
    return rgb_image
