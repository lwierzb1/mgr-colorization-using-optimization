from threading import Thread

from color_transfer import ColorTransfer


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
        self._thread = Thread(target=lambda: self._thread_run(ref, bw))
        self._thread.daemon = True
        self._thread.start()

    def _thread_run(self, ref, bw):
        self._result = self._colorizer.transfer(ref, bw)
