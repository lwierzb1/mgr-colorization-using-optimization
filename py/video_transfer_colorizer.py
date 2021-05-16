import cv2

from color_transfer import ColorTransfer


class VideoTransferColorizer:
    def __init__(self, colorized_image_subject, video_path):
        self.video_ended = False
        self._out = None
        self._current_frame = None
        self._marked_frame = None
        self._processed_frames = 0
        self._video_path = video_path
        self._colorized_image_subject = colorized_image_subject
        self._color_transfer = ColorTransfer()

    def colorize_video(self, example):
        self.__read_video(self._video_path)
        self.__init_out()
        if self.video_ended:
            return

        # drawing on frame like on canvas .... start
        self._marked_frame = example
        # drawing on frame like on canvas .... stop
        self.__continuous_colorization()
        if self.video_ended:
            self._out.release()

    def force_save(self):
        self._out.release()

    def get_first_frame(self):
        cap = cv2.VideoCapture(self._video_path)
        ret, frame = cap.read()
        cap.release()
        return frame

    def __continuous_colorization(self):
        while self.__read_next_video_frame():
            result = self.__colorize_frame()
            # self._colorized_image_subject.notify(fill=True, result=bgr_to_rgb(result))
            self.__append_frame_to_video(result)

    def __append_frame_to_video(self, frame):
        self._out.write(frame)

    def __colorize_frame(self):
        result = self._color_transfer.transfer(self._marked_frame, self._current_frame)
        return result

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

    def __get_frame_shape(self):
        return int(self._cap.get(4)), int(self._cap.get(3))

    def __init_out(self):
        self._out = cv2.VideoWriter('out.avi', cv2.VideoWriter_fourcc(*'DIVX'), 25,
                                    (self.__get_frame_shape()[1], self.__get_frame_shape()[0]))
