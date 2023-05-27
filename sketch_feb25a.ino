#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *motor4 = AFMS.getMotor(4);
Adafruit_DCMotor *motor3 = AFMS.getMotor(3);
Adafruit_DCMotor *motor2 = AFMS.getMotor(2);
Adafruit_DCMotor *motor1 = AFMS.getMotor(1);
int m1direction = 0;
// LEDs indicating direction
const int forwardsLED = 8;
const int backwardsLED = 9;
const int limitPin = 2;
// millis() returns an unsigned long value
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; adjust if we see shudder
int lastLimitState = HIGH;           // the previous state of the limit switch
unsigned long lastMessageTime = 0;   // Use the value of lastMessageTime to stop spamming the console

/*
 * limitCheck() tests if the limit switch has been activated and returns TRUE if it has or
 * FALSE otherwise.
 * 
 * The switch is considered active if the input has gone from LOW to HIGH and we've waited
 * for longer than the debounce time to ignore noise.
 * 
 * Based on code by David A. Mellis, Limor Fried, Mike Walters, and Arturo Guadalupi.
 * http://www.arduino.cc/en/Tutorial/Debounce
 */


bool limitCheck() {
  bool atLimit = false;
  int limitState = LOW;  // initialising to LOW means we can detect a wire break
  int reading;

  reading = digitalRead(limitPin);  // Get the current state of the switch
  if (reading != lastLimitState) {  // If the switch changed, due to noise or pressing:
    lastDebounceTime = millis();    // reset the debouncing timer
  }

  // If time has passed and the button state still hasn't changed, then we take it
  // that it really has been pressed.
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != limitState) {
      limitState = reading;
      if (limitState == HIGH) {  // we only care about a transition to HIGH
        atLimit = true;
        if ((millis() - lastMessageTime) > 1000) {   // Don't print another message on the console
          Serial.println("Limit switch activated");  // more than once a second
          lastMessageTime = millis();
        }
      }
    }
  }
  lastLimitState = reading;  // save the state for the next call

  return(atLimit);
}

int in1 = 5;
int in2 = 6;

void stopallmotors() {
  motor1->run(RELEASE);
  motor2->run(RELEASE);
  motor3->run(RELEASE);
  motor4->run(RELEASE);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}



void forward4() {
  motor4->run(FORWARD);
  delay(500);
  motor4->run(RELEASE);
  delay(500);

}

void forward5() {
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
  delay(100);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

void backward5() {
  digitalWrite(in2, HIGH);
  digitalWrite(in1, LOW);
  delay(100);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
}

void forward1() {
  motor1->run(FORWARD);
  if (m1direction == 1) {
    Serial.println("No Direction Change");
    delay(1000);
  }
  else { 
    Serial.println("Direction Change");
    m1direction = 1;
    delay(1000);

  }
  motor1->run(RELEASE);
  delay(500);
}

void backward1() {
  motor1->run(BACKWARD);
  if (m1direction == -1) {
    Serial.println("No Direction Change");
    delay(1000);
  }
  else { 
    Serial.println("Direction Change");
    m1direction = -1;
    delay(1000);
  }  
  motor1->run(RELEASE);
  delay(500);
}

void gohome() {
  motor1->run(BACKWARD);
  while (! limitCheck()) {
    Serial.print(".");
  }
    Serial.println("limitCheck true, stopping M1 backwards motion");
    stopallmotors();
}

void forward2() {
  motor2->run(FORWARD);
  delay(100);
  motor2->run(RELEASE);
  delay(100);
}

void forward3() {
  motor3->run(FORWARD);
  delay(500);
  motor3->run(RELEASE);
  delay(500);
}

void backward2() {
  motor2->run(BACKWARD);
  delay(100);
  motor2->run(RELEASE);
  delay(100);
}

void backward3() {
  motor3->run(BACKWARD);
  delay(1400);
  motor3->run(RELEASE);
  delay(1000);
}

void backward4() {
  motor4->run(BACKWARD);
  delay(500);
  motor4->run(RELEASE);
  delay(500);
}

void m1bigmove() {
  for(int i=1; i < 10; i++) {
    forward1();
  }
}

void m1bigmovebackward() {
  for(int i=1; i < 10; i++) {
    backward1();
  }
}

void col4() { 
  fullmove(20, 20);
}

void col3() { 
  fullmove(16, 16);
}

void col1() { 
  fullmove(10, 10);
}

void col2() { 
  fullmove(13, 13);
}

void col0() { 
  fullmove(8, 8);    
}

void col5() { 
  fullmove(22, 22);    
}

void col6() { 
  fullmove(26, 26);    
}

void fullmove(int fwd, int bck) { 
  //move from home position 
  motor1->run(FORWARD);
  if (m1direction == 1) {
    Serial.println("No Direction Change");
    delay(fwd*500);
  }
  else { 
    Serial.println("Direction Change");
    m1direction = 1;
    delay(fwd*500);

  }
  motor1->run(RELEASE);
  delay(500);
  
  //drop coin
  forward5();

  //move back to home
  gohome();
  /*
  motor1->run(BACKWARD);
  if (m1direction == -1) {
    Serial.println("No Direction Change");
    delay(bck*500);
  }
  else { 
    Serial.println("Direction Change");
    m1direction = 1;
    delay(bck*500);

  }
  motor1->run(RELEASE);
  delay(500);
  */

  //pick new coin
  backward5();
}

void setup() {
  // put your setup code here, to run once:
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(limitPin, INPUT_PULLUP);
  Serial.begin(9600);
  AFMS.begin();
  motor4->run(RELEASE);
  motor3->run(RELEASE);
  motor4->setSpeed(50);
  motor3->setSpeed(50);
  motor2->setSpeed(50);
  motor1->setSpeed(50);
  delay (2000);
  Serial.println("init");
  delay(100);
  Serial.println();
  Serial.print("Motor Number: ");
}

 
void controlmotor(int motor_number) {
  Serial.print("called: ");
  Serial.println(motor_number);
  //forward1();
  //forward2();
  //forward3();
  //forward4();
 if (motor_number == 0) {
   stopallmotors();
 }
 if (motor_number == 1) {
   forward1();
 }
  if (motor_number == 6) {
    backward1();
 }
 if (motor_number == 2) {
   forward2();
 }
 if (motor_number == 7) {
   backward2();
 }
 if (motor_number == 3) {
   forward3();
 }
 if (motor_number == 8) {
   backward3();
 }
 if (motor_number == 4) {
   forward4();
 }
 if (motor_number == 9) {
   backward4();
 }
 if (motor_number == 5) {
   forward5();
 }
 if (motor_number == 10) {
   backward5();
   
 }
 if (motor_number == 20) {
    motor1->run(FORWARD);
    if (m1direction == 1) {
      Serial.println("No Direction Change");
      delay(19*500);
    }
    else { 
      Serial.println("Direction Change");
      m1direction = 1;
      delay(19*500);

    }
    motor1->run(RELEASE);
    delay(500);
  }
 if (motor_number == 21) {
  motor1->run(BACKWARD);
  if (m1direction == -1) {
    Serial.println("No Direction Change");
    delay(22*500);
  }
  else { 
    Serial.println("Direction Change");
    m1direction = 1;
    delay(22*500);
  }
  motor1->run(RELEASE);
  delay(500);
 }
 if (motor_number == 34) {
   col4();
 }
 if (motor_number == 30) {
   col0();
 }
 if (motor_number == 33) {
   col3();
 }
 if (motor_number == 32) {
   col2();
 }
 if (motor_number == 31) {
   col1();
 }
 if (motor_number == 35) {
   col5();
 }
 if (motor_number == 36) {
   col6();
 }
 if (motor_number == 40) {
   gohome();
 }
}

void loop() {
  // put your main code here, to run repeatedly:
  int motor_number;
  while (Serial.available() > 0) {
    motor_number = Serial.parseInt();
    if (Serial.read() == '\n') {

      Serial.print("I read: ");
      Serial.println(motor_number);
      Serial.println("Motor number: ");
      controlmotor(motor_number);
    }
  }
}

