import cv2
import numpy as np

## La classe Image gère les opérations sur les images avec la librairie CV2
class Image:
    def __init__(self, path, i=0):
        #print(path)
        self.img = cv2.imread(path)
        while self.img is None:
            self.img = cv2.imread(path)
        self.bw = np.array(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))
        self.id = i # identifiant de l'image (pour le programme de post-traitement)

    # print(self.bw)
    def variance(self):
        return np.var(self.bw)

# i = Image("/home/brice/Bureau/Img_exp/IMG_0")
