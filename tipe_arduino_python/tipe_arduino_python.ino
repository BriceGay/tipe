// Code Arduino
// Ce code est l'adaptation d'un exemple trouvé sur arduino.cc

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
int pos = 0;    // variable to store the servo position

void setup() {
  
  Serial.begin(115200); // ouvre canal de communication avec l'ordinateur
  Serial.setTimeout(1);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  
}

String msg;
int newPos;

void loop() {
  
  while (!Serial.available()); // attend un msg
  
  msg = Serial.readString(); // lit le msg
  
  if (msg[0] == ' ') { // si le format du mesage est correct (commence par un espace)
    
    newPos = msg.toInt()%181; // consigne entre 0 et 180
    pos = newPos; // mise à jour consigne
    myservo.write(pos); // pilotage servomoteur
    
  }
  Serial.print(myservo.read()); // renvoie la postion du servomoteur
  Serial.print("\n");
  
}
