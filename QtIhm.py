# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ihmSerialtest.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(772, 500)
        self.QuitButton = QtWidgets.QPushButton(Form)
        self.QuitButton.setGeometry(QtCore.QRect(150, 10, 101, 31))
        self.QuitButton.setObjectName("QuitButton")
        self.lcdNumber = QtWidgets.QLCDNumber(Form)
        self.lcdNumber.setGeometry(QtCore.QRect(180, 50, 211, 21))
        self.lcdNumber.setObjectName("lcdNumber")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(50, 50, 67, 17))
        self.label.setObjectName("label")
        self.StartButton = QtWidgets.QPushButton(Form)
        self.StartButton.setGeometry(QtCore.QRect(40, 10, 101, 31))
        self.StartButton.setObjectName("StartButton")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(50, 90, 691, 391))
        self.widget.setObjectName("widget")

        self.retranslateUi(Form)
        self.QuitButton.clicked.connect(Form.CloseApp)
        self.StartButton.clicked.connect(Form.Start)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Serial Test"))
        self.QuitButton.setText(_translate("Form", "QUIT"))
        self.label.setText(_translate("Form", "Output"))
        self.StartButton.setText(_translate("Form", "START"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
