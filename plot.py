import pyqtgraph as pg
from PyQt5 import QtCore
from pyqtgraph import PlotWidget


class LoadGraph(PlotWidget):

    def __init__(self, parent=None, labelX="X", labelY="Y", maxpts=20):
        super(LoadGraph, self).__init__(parent)
        self.setGeometry(QtCore.QRect(0, 0, parent.width(), parent.height()))

        self.maxpts = maxpts
        self.xdata = []
        self.ydata = []

        self.getPlotItem().setContentsMargins(20, 20, 20, 20)
        self.setBackground('w')
        self.setLabel('left', labelY, color='red', size=30)
        self.setLabel('bottom', labelX, color='red', size=30)
        self.showGrid(x=True, y=True)
        pen = pg.mkPen(color=(255, 0, 0), width=2, style=QtCore.Qt.NoPen)
        self.data_line = self.plot(pen=pen, symbol='o', symbolSize=10, symbolBrush=('b'))

    def updateplot(self):
        self.data_line.setData(self.xdata, self.ydata)

    def resetgraph(self):
        self.xdata.clear()
        self.ydata.clear()

    def adddata(self, x, y):
        if len(self.xdata) > self.maxpts:
            self.xdata = self.xdata[1:]
            self.ydata = self.ydata[1:]

        self.xdata.append(x)
        self.ydata.append(y)
