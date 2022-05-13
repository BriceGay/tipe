import sys, numpy as np
import time
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication

from Arduino import Moteur
from CalculImg import Image
from camera import CameraWindow

ID_CAM = 1
PORT = "/dev/ttyACM1"
NOM = "IMG_"

def run(cam, moteur):
    MIN = 0
    MAX = 180
    pas = 1
    contrast, positions = [], []
    for i in range(MIN, MAX+1, pas):
        print(i)
        moteur.write(i)
        time.sleep(1)
        img = cam.click_photo(NOM + str(i))
        time.sleep(0.5)

        contrast.append(Image(img).variance())
        positions.append(i)
    plt.scatter(positions, contrast)
    bestId = np.argmax(contrast)
    print(positions[bestId], contrast[bestId])
    moteur.write(positions[bestId])
    plt.show()




App = QApplication(sys.argv)

# create the instance of our Window
myMot=Moteur(PORT)
window = CameraWindow(run, myMot, ID_CAM)


# start the app
sys.exit(App.exec())