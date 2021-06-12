import threading
import image_processing_toolkit


class CTAsyncTaskVideo:
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

    def run(self, image_ref):
        self._thread = threading.Thread(target=self._thread_run, args=(image_ref,))
        self._thread.daemon = True
        self._thread.start()

    def _thread_run(self, image_ref):
        self._video_colorizer.colorize_video(image_processing_toolkit.read_image(image_ref))
        self.finished = True
