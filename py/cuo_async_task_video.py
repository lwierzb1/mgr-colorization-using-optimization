from threading import Thread


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
        self._thread = Thread(
            target=lambda: self._thread_run(color))
        self._thread.daemon = True
        self._thread.start()

    def _thread_run(self, color):
        self._video_colorizer.colorize_video(color)
        self.finished = True
