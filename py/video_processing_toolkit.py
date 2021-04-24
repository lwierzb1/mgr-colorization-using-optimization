import cv2


def read_video(video_path):
    return cv2.VideoCapture(video_path)
