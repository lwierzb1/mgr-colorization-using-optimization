__author__ = "Lukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Lukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import cv2


def read_video(video_path):
    return cv2.VideoCapture(video_path)
