import serial
import time

# la classe moteur permet de communiquer avec la carte Arduino
class Moteur:
    def __init__(self, p):
        self.arduino = serial.Serial(port=p, baudrate=115200, timeout=.1)
        print("NO ARDUINO")

    def write(self, pos):
        self.arduino.write(bytes(" " + str(pos), 'utf-8'))
        time.sleep(0.05)
        return self.arduino.readline()

    def read(self):
        self.arduino.write(bytes("x", 'utf-8'))
        time.sleep(0.05)
        return int(self.arduino.readline())


def test():  # fonction pour tester la classe Moteur
    m = Moteur('/dev/ttyACM0')
    while True:
        num = input("Enter a number: ")  # Taking input from user
        value = m.write(num)
        print(value, m.read())  # printing the value
"""
m = Moteur('/dev/ttyACM0')
while(True):
    m.write(str(1))
    time.sleep(1)
    m.write(str(180))
    time.sleep(1)"""