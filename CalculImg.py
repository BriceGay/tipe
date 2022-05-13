import cv2
import numpy as np
class Image:
    def __init__(self, path):
        print(path)
        self.img = cv2.imread(path)
        while self.img is None:
            self.img = cv2.imread(path)
        self.bw = np.array(cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY))
       # print(self.bw)
    def variance(self):
        return np.var(self.bw)

#i = Image("/home/brice/Bureau/Img_exp/IMG_0")