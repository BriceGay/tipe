from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np


## fonction qui calcule le nb de pts de mesures en fonction des parametres

def nb_pts_3balayages(taille, precision_souhaitee, nbPts1, nbPts2):
    nbPts = nbPts1 + nbPts2 # ont fait les 2 1ers balayges
    intervalle = taille / (nbPts1-1)*2/(nbPts2)*2 # calcul de l'interval restant à balayer
    return nbPts + intervalle / precision_souhaitee # on ajoute le balayage de l'intervalle restant


##tracé de la courbe :

# parametrges matplotlib
fig = plt.figure()
ax = plt.axes(projection='3d')
fig = plt.figure()
ax = plt.axes(projection='3d')


# création des données
x = np.linspace(5, 50, 20)
y = np.linspace(5, 50, 20)
X, Y = np.meshgrid(x, y)
Z = nb_pts_3balayages(60., 0.1, X, Y)

# tracé
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')

# ajout légendes
ax.set_xlabel('Nb pts\nbalayage 1')
ax.set_ylabel('Nb pts\nbalayage 2')
ax.set_zlabel('Durée totale');

plt.show()  # affichage
