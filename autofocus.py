## Imports
import numpy as np
import sys
import time

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication

from Arduino import Moteur
from CalculImg import Image
from camera import CameraWindow

ID_CAM = 0
PORT = "/dev/ttyACM1"
NOM = "IMG_"


def autofocus(cam, moteur):
    MIN, MAX = 0, 180  # plage de positions à balayer (en degrés)
    pas = 10
    contrast, positions = [], []  # pour sauvegarder
    while pas > 1:
        # balaye entre MIN et MAX
        for i in range(MIN, MAX + 1, pas):
            print(i)
            moteur.write(i)  # commande le servomateur
            time.sleep(1)  # attente (temps de réaction moteur et camera)
            img = cam.click_photo(NOM + str(i))  # enregistre la photo
            time.sleep(0.5)  # attend que la photo soit effectivement enregistree (car cela est fait en arrière plan)
            curContrast = Image(img).variance()  # calcule la variance
            # ajoute un point dans nos graphiques
            contrast.append(curContrast)
            positions.append(i)
        bestId = np.argmax(contrast)  # trouve le contrast maximal dans ce qui a déjà été vu
        bestPos = positions[bestId]

        # parametre le balayage suivant :
        MAX = bestPos + pas
        MIN = bestPos - pas
        pas = pas // 2

    # affiche la meilleur position
    bestId = np.argmax(contrast)
    print(positions[bestId], contrast[bestId])

    moteur.write(positions[bestId])  # positionne le microscope sur la meilleure position

    # affiche le contrast en fonction de la position
    plt.scatter(positions, contrast)
    plt.show()


# Lance l'application
myMot = Moteur(PORT)  # classe pour commander le moteur
window = CameraWindow(autofocus, myMot, ID_CAM)  # classe pour gérer la webcam

# execute l'appli :
App = QApplication(sys.argv)
sys.exit(App.exec())
