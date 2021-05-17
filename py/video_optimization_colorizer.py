import math
import sys

import cv2
import numpy as np

from image_colorizer_multiprocess import ImageColorizerMultiprocess
from image_processing_toolkit import bgr_matrix_to_image, bgr_to_rgb
from singleton_config import SingletonConfig


class VideoOptimizationColorizer:
    def __init__(self, colorized_image_subject, video_path):
        config = SingletonConfig.get_instance()
        self.video_ended = False
        self._out = None
        self._cap = None
        self._current_frame = None
        self._previous_frame = None
        self._features_to_track = None
        self._marked_frame = None
        self._processed_frames = 0
        self._frames_to_process = config.max_video_frames_per_section
        self._video_path = video_path
        self._colorized_image_subject = colorized_image_subject
        self.get_frame_to_colorize()

    def colorize_video(self, m):
        if self.video_ended:
            return

        self.__find_features_to_track()
        # drawing on frame like on canvas .... start
        self._marked_frame = m
        # drawing on frame like on canvas .... stop
        self.__continuous_colorization()
        self._processed_frames = 0

        if self.video_ended:
            self._out.release()

    def force_save(self):
        self._out.release()

    def get_frame_to_colorize(self):
        if not self.__is_video_opened():
            self.__read_video(self._video_path)
            self.__init_out()
            self.__read_next_video_frame()
        return self._current_frame

    def __continuous_colorization(self):
        marked_pixels_new = []
        while self.__is_video_opened() and self._processed_frames < self._frames_to_process:
            self.__read_next_video_frame()
            current_colored_frame = self._current_frame.copy()

            new_points_position, status, err = self.__calculate_optical_flow()

            good_new_points = new_points_position[status == 1]
            good_old_points = self._features_to_track[status == 1]

            if self._processed_frames > 0:
                marked_pixels_current = np.array([i[0] for i in marked_pixels_new], dtype=np.float64)
                marked_pixels_new = []
            else:
                marked_pixels_current = self.__get_marked_pixels()

            points = {tuple(p0): p1 - p0 for p0, p1 in (zip(list(good_old_points), list(good_new_points)))}

            for index, pixel in enumerate(marked_pixels_current):
                min_distance = sys.maxsize
                min_distance_point = None
                color_point = self._marked_frame[int(pixel[0]), int(pixel[1])]
                for point in good_old_points:
                    current_distance = math.sqrt(((point[0] - pixel[0]) ** 2) + ((point[1] - pixel[1]) ** 2))
                    if current_distance < min_distance:
                        min_distance = current_distance
                        min_distance_point = point

                v0 = points[tuple(min_distance_point)]
                v0 = np.array([v0[1], v0[0]])
                marked_pixels_new.append((pixel + v0, color_point))

            for (pixel, color) in marked_pixels_new:
                frame_width = self.__get_frame_shape()[1]
                frame_height = self.__get_frame_shape()[0]
                if 0 <= pixel[0] < frame_height and 0 <= pixel[1] < frame_width:
                    current_colored_frame[int(pixel[0]), int(pixel[1])] = color.tolist()

            colorized_frame = self.__colorize_frame(current_colored_frame)

            self._colorized_image_subject.notify(result=bgr_to_rgb(colorized_frame))
            self.__append_frame_to_video(colorized_frame)

            self._marked_frame = current_colored_frame
            self._features_to_track = good_new_points.reshape(-1, 1, 2)
            self._processed_frames += 1

    def __append_frame_to_video(self, frame):
        self._out.write(frame)

    def __colorize_frame(self, marked_frame):
        colorizer = ImageColorizerMultiprocess(self._current_frame, marked_frame)
        result = colorizer.colorize()
        return bgr_matrix_to_image(result)

    def __get_marked_pixels(self):
        bw_current = cv2.cvtColor(self._previous_frame, cv2.COLOR_BGR2GRAY)
        bw_marked = cv2.cvtColor(self._marked_frame, cv2.COLOR_BGR2GRAY)
        bw_current_norm = cv2.normalize(bw_current.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
        marked_frame_norm = cv2.normalize(bw_marked.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)

        has_hint = abs(bw_current_norm - marked_frame_norm) > 0.03

        marked_pixels = []
        for i in range(has_hint.shape[0]):
            for j in range(has_hint.shape[1]):
                if has_hint[i, j]:
                    marked_pixels.append([i, j])
        return np.asarray(marked_pixels, dtype=np.float64)

    def __read_video(self, video_path):
        self._cap = cv2.VideoCapture(video_path)

    def __read_next_video_frame(self):
        self.__shift_last_frame()
        ret, frame = self._cap.read()
        self._current_frame = frame
        self.video_ended = not ret
        return ret

    def __shift_last_frame(self):
        if self._current_frame is None:
            self._previous_frame = None
        else:
            self._previous_frame = self._current_frame.copy()

    def __calculate_optical_flow(self):
        previous_frame_in_gray = cv2.cvtColor(self._previous_frame, cv2.COLOR_BGR2GRAY)
        current_frame_in_gray = cv2.cvtColor(self._current_frame, cv2.COLOR_BGR2GRAY)

        return cv2.calcOpticalFlowPyrLK(previous_frame_in_gray,
                                        current_frame_in_gray,
                                        self._features_to_track,
                                        None,
                                        winSize=(15, 15),
                                        maxLevel=2,
                                        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    def __find_features_to_track(self):
        current_frame_in_gray = cv2.cvtColor(self._current_frame, cv2.COLOR_BGR2GRAY)
        self._features_to_track = cv2.goodFeaturesToTrack(current_frame_in_gray,
                                                          mask=None,
                                                          maxCorners=100,
                                                          qualityLevel=0.3,
                                                          minDistance=7,
                                                          blockSize=7)

    def __is_video_opened(self):
        if self._cap is None:
            return False
        else:
            return self._cap.isOpened()

    def __get_frame_shape(self):
        return int(self._cap.get(4)), int(self._cap.get(3))

    def __init_out(self):
        self._out = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc(*'DIVX'), 25,
                                    (self.__get_frame_shape()[1], self.__get_frame_shape()[0]))
