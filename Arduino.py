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


## Fin de code utile
def test():  # fonction pour tester la classe Moteur
    m = Moteur('/dev/ttyACM0')
    while True:
        num = input("Enter a number: ")  # Taking input from user
        value = m.write(num)
        print(value, m.read())  # printing the value


class Moteur2:
    def __init__(self, p):  # initie la communication
        return

    def write(self, pos):  # envoie une instruction et retourne la réponse d'Arduino
        time.sleep(0.05)
        return pos

    def read(self):  # envoie une instruction vide et retourne la réponse d'Arduino
        time.sleep(0.05)
        return 0


"""
m = Moteur('/dev/ttyACM0')
while(True):
    m.write(str(1))
    time.sleep(1)
    m.write(str(180))
    time.sleep(1)"""
