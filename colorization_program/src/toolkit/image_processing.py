__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

"""General purpose functions useful for image processing.
"""

import tkinter.filedialog as tk_file

import cv2
import imageio
import numpy as np

from colorization_program.src.toolkit.color_conv import rgb2yuv, yuv2rgb


def write_image(image, path):
    cv2.imwrite(path, image)


def read_image(path):
    return rgb_to_bgr(imageio.imread(path))


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
    rgb = cv2.cvtColor(matrix, cv2.COLOR_BGR2RGB)
    yuv_matrix = rgb2yuv(rgb)
    return cv2.split(yuv_matrix)


def yuv_channels_to_bgr_matrix(y_channel, u_channel, v_channel):
    """Returns image in BGR space created from YUV channels.

    y_channel: luminance channel.
    u_channel: color channel.
    v_channel: color channel.
    """
    yuv_image = cv2.merge((y_channel.astype(np.float32), u_channel.astype(np.float32), v_channel.astype(np.float32)))
    rgb_image = yuv2rgb(yuv_image)
    bgr_image = cv2.cvtColor(rgb_image.astype(np.float32), cv2.COLOR_RGB2BGR)
    return bgr_image


def bgr_matrix_to_image(matrix):
    """Returns rgb image representation of float matrix.

    matrix: float matrix.
    """
    matrix = np.clip(matrix, 0, 1)
    bgr_image = (matrix * 255).astype(np.uint8)
    return bgr_image


def hex_to_bgr(value):
    hex_val = value.lstrip('#')
    rgb = list(int(hex_val[i:i + 2], 16) for i in (0, 2, 4))
    rgb.reverse()
    return rgb


def browse_for_image(title):
    filename = tk_file.askopenfilename(initialdir="/",
                                       title=title,
                                       filetypes=[("BMP Files", "*.bmp")])
    if filename:
        return filename
    else:
        return None


def browse_for_video():
    filename = tk_file.askopenfilename(initialdir="/",
                                       title="Select an video",
                                       filetypes=[("AVI Files", "*.avi")])
    if filename:
        return filename
    else:
        return None


def bgr_to_rgb(matrix):
    return cv2.cvtColor(matrix, cv2.COLOR_BGR2RGB)


def rgb_to_bgr(matrix):
    return cv2.cvtColor(matrix, cv2.COLOR_RGB2BGR)
