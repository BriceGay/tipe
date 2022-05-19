# importing required libraries
import os
import sys
import time

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *


## La classe CameraWindow gère l'interface graphique et la caméra
# Ce code est l'adaptation d'un exemple trouvé sur Stackoverflow
class CameraWindow(QMainWindow):

    # création de l'interface au démarrage
    def __init__(self, f, moteur, icam):
        super().__init__()
        self.setGeometry(100, 100,
                         800, 600)
        self.setStyleSheet("background : lightgrey;") # modifie le style
        self.available_cameras = QCameraInfo.availableCameras() # liste des caméras connectées

        if not self.available_cameras: # msg d'erreur si pas de camera dispo
            # exit the code
            print("PAS DE CAMERA TROUVEES -> EXIT")
            sys.exit()

        # dossier pour sauvegarder les images :
        self.save_path = "/home/brice/Bureau/Img_exp"

        # crée l'interface graphique :
        # crée la bar d'état
        self.status = QStatusBar()
        self.status.setStyleSheet("background : white;")
        self.setStatusBar(self.status)

        # crée l'affichage de la camera
        self.viewfinder = QCameraViewfinder()
        self.viewfinder.show()
        self.setCentralWidget(self.viewfinder)

        self.select_camera(icam) # selectionne une camera

        # crée la bar d'outil
        toolbar = QToolBar("Camera Tool Bar")
        self.addToolBar(toolbar)

        # cree les boutons
        click_action = QAction("Sauvegarder", self)
        click_run = QAction("Autofocus", self)
        change_folder_action = QAction("Changer de dossier",self)

        # ajoute les boutons à la bar d'outil
        toolbar.addAction(change_folder_action)
        toolbar.addAction(click_action)
        toolbar.addAction(click_run )

        # cree la liste pour choisir la camera
        camera_selector = QComboBox()
        camera_selector.setToolTipDuration(2500)
        camera_selector.addItems([camera.description() for camera in self.available_cameras])
        toolbar.addWidget(camera_selector)

        # connecte les boutons aux fonctions correspondantes
        change_folder_action.triggered.connect(self.change_folder)
        camera_selector.currentIndexChanged.connect(self.select_camera)
        click_action.triggered.connect(self.click_photo)
        click_run.triggered.connect(lambda : f(self, moteur))

        self.setWindowTitle("Autofocus Brice - Thibault") # change le titre

        self.show() # affiche la fenetre

    # Change la camera utilisee
    def select_camera(self, i):
        #parametre la camera :
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.start()
        self.capture = QCameraImageCapture(self.camera)
        self.current_camera_name = self.available_cameras[i].description()

    # Enregistre l'image actuelle et retourne l'endroit où elle est enregisrée
    def click_photo(self, name):
        self.capture.capture(os.path.join(self.save_path,name))
        return self.save_path + "/" + name + ".jpg"

    # Quand l'utilisateur veut changer de dossier d'enregistrement
    def change_folder(self):
        #ouvre une fenetre pour choisir un nouveau dossier
        path = QFileDialog.getExistingDirectory(self, "Picture Location", "")

        if path: # si un dossier est choisi :
            self.save_path = path