import random
import time

from PyQt5.QtCore import *


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    '''
    finished = pyqtSignal()
    progress = pyqtSignal(int)


class manualinterruption(Exception):
    pass


class Worker(QRunnable):
    '''
    Worker thread
    '''

    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()
        ''' flag to stop worker'''
        self.iskilled = False

    @pyqtSlot()
    def run(self):

        try:

            for n in range(100):
                value = random.randint(0, 10)
                self.signals.progress.emit(value)
                time.sleep(0.2)

                if self.iskilled:
                    raise manualinterruption

        except manualinterruption:
            print('THREAD stopped')

        self.signals.finished.emit()  # Done

    def kill(self):
        self.iskilled = True
