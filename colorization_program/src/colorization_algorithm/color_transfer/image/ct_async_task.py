__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

import threading

from colorization_program.src.colorization_algorithm.color_transfer.image.color_transfer import ColorTransfer


class CTAsyncTask:
    def __init__(self):
        super().__init__()
        self._finished = False
        self._started = False
        self._thread = None
        self._result = None
        self._colorizer = ColorTransfer()

    def result(self):
        if self._result is not None:
            result_copy = self._result.copy()
            self._result = None
            return result_copy
        else:
            return None

    def run(self, ref, bw):
        self._thread = threading.Thread(target=self._thread_run, args=(ref, bw,))
        self._thread.daemon = True
        self._thread.start()

    def _thread_run(self, ref, bw):
        self._result = self._colorizer.transfer(ref, bw)
