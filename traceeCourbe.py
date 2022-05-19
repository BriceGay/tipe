from CalculImg import Image
import cv2
import os
import re
import matplotlib.pyplot as plt

dossier = "/home/brice/Documents/Travail/PSI/TIPE/Mesure Champo/Img_moustique2_mieux"


def get_numbers_from_filename(filename):
    return int(re.search(r'\d+', filename).group(0))


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = Image(os.path.join(folder, filename), get_numbers_from_filename(filename))
        images.append(img)
    return images


img = load_images_from_folder(dossier)
img.sort(key=lambda x: x.id, reverse=False)
y = [e.variance() for e in img]
x = [e.id for e in img]

print(dossier + "\t ")
print("id\tvariance")
for i in range(len(img)):
    print(str(x[i]) + "\t" + str(y[i]))

plt.plot(x,y)
plt.show()


