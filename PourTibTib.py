import serial
import time


## la classe Moteur permet de communiquer avec la carte Arduino
class Moteur:
    def __init__(self, p):  # initie la communication
        self.arduino = serial.Serial(port=p, baudrate=115200, timeout=.1)

    def write(self, pos):  # envoie une instruction et retourne la réponse d'Arduino
        self.arduino.write(bytes(" " + str(pos), 'utf-8'))
        time.sleep(0.05)
        return self.arduino.readline()

    def read(self):  # envoie une instruction vide et retourne la réponse d'Arduino
        self.arduino.write(bytes("x", 'utf-8'))
        time.sleep(0.05)
        return int(self.arduino.readline())

myMot = Moteur("COM0") #à modifier

myMot.write(0)
myMot.write(180)