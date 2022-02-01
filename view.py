
1
1

I have been trying to read frames from webcam, using OpenCV and PyQt. I know there are a lot of examples. But I would like to use MVC (model-view-controller).

OpenCV handles controller, i created models.py for model and views.py for GUI.

I don't see any error before run the code, when i run the code GUI opens, then i press open webcam and i see this warning and error:

[ WARN:0] global C:\projects\opencv-python\opencv\modules\videoio\src\cap_msmf.cpp (674) SourceReaderCB::~SourceReaderCB terminating async callback

Process finished with exit code 1

Here is views.py

from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox
from models import Camera

class UI_Window(QWidget):

    def __init__(self, camera = None):
        super().__init__()
        self.camera = camera

        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(Camera.nextFrameSlot)

        # Create a layout.
        layout = QVBoxLayout()

        # Add a button
        button_layout = QHBoxLayout()

        btnCamera = QPushButton("Open camera")
        btnCamera.clicked.connect(Camera.openCamera)
        button_layout.addWidget(btnCamera)
        layout.addLayout(button_layout)

        # Add a label
        self.label = QLabel()
        self.label.setFixedSize(640, 640)

        layout.addWidget(self.label)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("First GUI with QT")
        self.setFixedSize(800, 800)

    # https://stackoverflow.com/questions/1414781/prompt-on-exit-in-pyqt-application

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

models.py

import cv2
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage

class Camera:

    def __init__(self, camera):
        self.camera = camera
        self.cap = None

    def openCamera(self):
        self.vc = cv2.VideoCapture(0)
        # vc.set(5, 30)  #set FPS
        self.vc.set(3, 640)  # set width
        self.vc.set(4, 480)  # set height

        if not self.vc.isOpened():
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

        self.timer.start(1000. / 24)

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def nextFrameSlot(self):
        rval, frame = self.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)

    def initialize(self):
        self.cap = cv2.VideoCapture(self.camera)

start.py

from PyQt5.QtWidgets import QApplication

from models import Camera
from views import UI_Window

camera = Camera(0)
camera.initialize()

app = QApplication([])
start_window = UI_Window(camera)
start_window.show()
app.exit(app.exec_())

python
opencv
model-view-controller
pyqt
pyqt5
Share
Improve this question
Follow
asked Jan 21 '20 at 14:21
beyblade41
7511 silver badge77 bronze badges

    did you search cap_msmf.cpp (674) SourceReaderCB::~SourceReaderCB terminating async callback in Google? What did you find? –
    furas
    Jan 21 '20 at 14:23

at start you use initialize() which uses cv2.VideoCapture(self.camera) but you have also button which runs Camera.openCamera which use self.vc = cv2.VideoCapture(0) - so you create access two times but you not releasing first access. –
furas
Jan 21 '20 at 14:30
yes . but it didn't work (answer to your first comment) –
beyblade41
Jan 21 '20 at 14:35

    is this full error message ? Don't you have more lines in error? Maybe there are other useful information - ie. in which line is problem. –
    furas
    Jan 21 '20 at 14:39
    unfortunately it is full message –
    beyblade41
    Jan 21 '20 at 14:44

Show 6 more comments
2 Answers
3

This code works for me. For test I put all in one file.

I removed

camera.initialize()

I moved nextFrameSlot from Camera to UI_Window

I also created start() in UI_Windows to move self.timer.start() from Camera to UI_Window

import cv2
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage

class Camera:

    def __init__(self, camera):
        self.camera = camera
        self.cap = None

    def openCamera(self):
        self.vc = cv2.VideoCapture(0)
        # vc.set(5, 30)  #set FPS
        self.vc.set(3, 640)  # set width
        self.vc.set(4, 480)  # set height

        if not self.vc.isOpened():
            print('failure')
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def initialize(self):
        self.cap = cv2.VideoCapture(self.camera)



from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox
#from models import Camera

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
        self.setFixedSize(800, 800)

    def start(self):
        camera.openCamera()
        self.timer.start(1000. / 24)

    def nextFrameSlot(self):
        rval, frame = camera.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)


    # https://stackoverflow.com/questions/1414781/prompt-on-exit-in-pyqt-application

class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)

#if __name__ == '__main__':
#    app = QApplication([])
#    window = UI_Window()
#    window.show()

#start.py

from PyQt5.QtWidgets import QApplication

#from models import Camera
#from views import UI_Window

camera = Camera(0)
#camera.initialize()
print('test')
app = QApplication([])
start_window = UI_Window(camera)
start_window.show()
app.exit(app.exec_())

EDIT: code tested in separated files.

I also added read_gray() and negative colors read(negative=True), read_gray(negative=True)

BTW: I many places I check if frame is not empty - but it can't be used if not frame but if frame is not None because frame is numpy.array and if not numpy.array: may give wrong result.

All GUI widgets I moved to from model to view.

models.py

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

    def read_gray(self, negative=False):
        rval, frame = self.vc.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            if negative:
                frame = cv2.bitwise_not(frame)
            return frame

views.py

from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from models import Camera

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

        self.timer.start(1000. / 24)

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
