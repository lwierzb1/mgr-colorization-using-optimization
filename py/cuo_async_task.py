from threading import Thread

from image_colorizer_multiprocess import ImageColorizerMultiprocess


class CUOAsyncTask:
    def __init__(self):
        super().__init__()
        self._finished = False
        self._started = False
        self._thread = None
        self._result = None

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
        colorizer = ImageColorizerMultiprocess(input_matrices[0], input_matrices[1])
        self._result = colorizer.colorize()
