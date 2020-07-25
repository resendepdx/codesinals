# decompyle3 version 3.3.2
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.7.7 (default, May  6 2020, 11:45:54) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: models\ThreadOperacion.py
# Compiled at: 2019-07-08 19:24:18
import sys, time, threading

class StopThread(StopIteration):
    pass


threading.SystemExit = (
 SystemExit, StopThread)

class ThreadOper(threading.Thread):

    def stop(self):
        self._ThreadOper__stop = True

    def _bootstrap(self):
        if threading._trace_hook is not None:
            raise ValueError('Não é possível executar o segmento com rastreamento!')
        self._ThreadOper__stop = False
        self.daemon = True
        sys.settrace(self._ThreadOper__trace)
        super()._bootstrap()

    def __trace(self, frame, event, arg):
        if self._ThreadOper__stop:
            raise StopThread()
        return self._ThreadOper__trace