__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import threading


class CUOAsyncTaskVideo:
    def __init__(self, video_colorizer):
        super().__init__()
        self.finished = False
        self._started = False
        self._thread = None
        self._result = None
        self._video_colorizer = video_colorizer

    def result(self):
        if self._result is not None:
            result_copy = self._result.copy()
            self._result = None
            return result_copy
        else:
            return None

    def run(self, color):
        self._thread = threading.Thread(target=self._thread_run, args=(color,))
        self._thread.daemon = True
        self._thread.start()

    def _thread_run(self, color):
        self._video_colorizer.colorize_video(color)
        self.finished = True
