# Sample

import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QApplication

import QtIhm
from Measure import Worker
from plot import LoadGraph


class Myframe(QtWidgets.QMainWindow, QtIhm.Ui_Form):
    def __init__(self):
        super(Myframe, self).__init__()
        self.setupUi(self)
        self.onInit()

    def onInit(self):
        # promote QWidget in PyQTGraph PlotWidget
        self.plotXY = LoadGraph(self.widget, labelY="Y values", labelX="X values")

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

    def thread_complete(self):
        print("THREAD COMPLETE!")
        self.StartButton.setText("START")

    def updateIHM(self, n):
        self.CurrentTime = time.time() - self.starttime
        self.lcdNumber.display(n)
        self.plotXY.adddata(self.CurrentTime, n)
        self.plotXY.updateplot()

    @pyqtSlot()
    def Start(self):
        if self.StartButton.text() == "START":
            self.StartButton.setText("STOP")
            self.starttime = time.time()
            self.plotXY.resetgraph()

            self.readdata = Worker()
            self.readdata.signals.finished.connect(self.thread_complete)
            self.readdata.signals.progress.connect(self.updateIHM)
            self.threadpool.start(self.readdata)

        else:
            self.readdata.kill()
            self.StartButton.setText("START")

    @pyqtSlot()
    def CloseApp(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Myframe()
    form.show()
    app.exec_()
    # sys.exit(app.exec_())
