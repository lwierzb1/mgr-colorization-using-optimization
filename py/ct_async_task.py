import threading
import color_transfer


class CTAsyncTask:
    def __init__(self):
        super().__init__()
        self._finished = False
        self._started = False
        self._thread = None
        self._result = None
        self._colorizer = color_transfer.ColorTransfer()

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
