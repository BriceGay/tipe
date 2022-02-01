import cv2

class Camera:
    def __init__(self, camera):
        self.camera = camera
        self.vp = None
    def open(self, width=640, height=480, fps=30):
        self.vc = cv2.VideoCapture(self.camera)

        self.width = width
        self.height = height
        self.fps = fps
        # vc.set(5, fps)  #set FPS
        self.vc.set(3, width)   # set width
        self.vc.set(4, height)  # set height
        return self.vc.isOpened()

    def read(self, negative=False):
        rval, frame = self.vc.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if negative:
                frame = cv2.bitwise_not(frame)
            return frame

from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage

class UI_Window(QWidget):

    def __init__(self, camera = None):
        super().__init__()
        self.camera = camera
        print('UI')
        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        # Create a layout.
        layout = QVBoxLayout()

        # Add a button
        button_layout = QHBoxLayout()

        btnCamera = QPushButton("Open camera")
        btnCamera.clicked.connect(self.start)
        button_layout.addWidget(btnCamera)
        layout.addLayout(button_layout)

        # Add a label
        self.label = QLabel()
        self.label.setFixedSize(640, 640)

        layout.addWidget(self.label)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("First GUI with QT")
        #self.setFixedSize(800, 800)

    def start(self):
        if not self.camera.open():
            print('failure')
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return
        self.timer.start(1000 / 24)

    def nextFrameSlot(self):
        frame = self.camera.read()
        #frame = self.camera.read_gray()
        if frame is not None:
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(pixmap)


class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)

if __name__ == '__main__':
    app = QApplication([])
    window = UI_Window()
    window.show()


from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    camera = Camera(0)

    app = QApplication([])
    start_window = UI_Window(camera)
    start_window.show()
    #app.exit(app.exec_())

import sys
from PyQt5.QtCore import Qt, QSize, QTimer, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
import cv2

def main():
    app = QApplication([])

    window = QWidget()
    window.setLayout(QGridLayout(window))
    window.setMinimumSize(QSize(640, 480))

    label = QLabel()
    label.setFixedSize(640, 640)
    window.layout().addWidget(label, 0, 0)

    window.show()

    vc = cv2.VideoCapture(0)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    timer = QTimer()
    timer.timeout.connect(lambda: nextFrameSlot(vc, label))
    timer.start(1000. / 24)

    return

def nextFrameSlot(vc: cv2.VideoCapture, label: QLabel):
    rval, frame = vc.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(image)
    label.setPixmap(pixmap)

