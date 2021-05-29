import math
import sys
from threading import Thread

from image_colorizer_multiprocess import ImageColorizerMultiprocess
import numpy as np

from py.image_processing_toolkit import bgr_to_rgb


class CUOAsyncTaskVideo:
    def __init__(self):
        super().__init__()
        self._finished = False
        self._started = False
        self._thread = None
        self._result = None
        self._video_cap = None
        self._processed_frames = 0

    def result(self):
        if self._result is not None:
            result_copy = self._result.copy()
            self._result = None
            return result_copy
        else:
            return None

    def run(self, input_matrices):
        self._thread = Thread(target=lambda: self._thread_run(input_matrices))
        self._thread.daemon = True
        self._thread.start()

    def _thread_run(self, input_matrices):
        marked_pixels_new = []
        while self.__is_video_opened() and self._processed_frames < self._frames_to_process:
            if self.video_ended:
                return
            else:
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
                point_to_add = pixel + v0
                if point_to_add[0] < self._current_frame.shape[0] and point_to_add[1] < self._current_frame.shape[
                    1]:
                    marked_pixels_new.append((point_to_add, color_point))

            for pixel, color in marked_pixels_new:
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
