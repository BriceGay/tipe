## INUTILE

# import the opencv library
import cv2, threading, time


class mCamera():
    def __init__(self, idCam):
        self.intervalle = 0.1
        self.vid = cv2.VideoCapture(idCam)
    def afficherFlux(self):
        self.afficher = True
        self.flux()

    def flux(self):
        self.getImg(True)
        print("f")
        if self.afficher:
            print("g")
            threading.Timer(1, self.flux).start()
            print("ok")

    def stopperFlux(self):
        self.afficher = False

    def getImg(self, afficher):
        ret, frame = self.vid.read()
        if afficher:
            cv2.imshow('frame', frame)
        return frame

    def kill(self):
        # After the loop release the cap object
        self.vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 2
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 6: # if there are more than 5 non working ports stop the testing.
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
            print("Port %s is not working." %dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                print("Port %s is working and reads images (%s x %s)" %(dev_port,h,w))
                working_ports.append(dev_port)
            else:
                print("Port %s for camera ( %s x %s) is present but does not reads." %(dev_port,h,w))
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports
#print(list_ports())

cam = mCamera(2)
#cam.afficherFlux()
cam.getImg(afficher=True)
while cv2.getWindowProperty('frame', 0) >= 0:
    cam.getImg(afficher=True)
    if cv2.waitKey(1) and 0xFF == ord('q'):
        break
print("out")

cam.kill()