import threading

import image_colorizer_multiprocess


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
        self._thread = threading.Thread(target=self._thread_run, args=(input_matrices,))
        self._thread.daemon = True
        self._thread.start()

    def _thread_run(self, input_matrices):
        colorizer = image_colorizer_multiprocess.ImageColorizerMultiprocess(input_matrices[0], input_matrices[1])
        self._result = colorizer.colorize()
