#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *motor4 = AFMS.getMotor(4);
Adafruit_DCMotor *motor3 = AFMS.getMotor(3);
Adafruit_DCMotor *motor2 = AFMS.getMotor(2);
Adafruit_DCMotor *motor1 = AFMS.getMotor(1);

void forward4() {
  motor4->run(FORWARD);
  delay(500);
  motor4->run(RELEASE);
  delay(500);
}

void forward1() {
  motor1->run(FORWARD);
  delay(500);
  motor1->run(RELEASE);
  delay(500);
}

void backward1() {
  motor1->run(FORWARD);
  delay(500);
  motor1->run(RELEASE);
  delay(500);
}

void forward2() {
  motor2->run(FORWARD);
  delay(500);
  motor2->run(RELEASE);
  delay(500);
}



void forward3() {
  motor3->run(FORWARD);
  delay(500);
  motor3->run(RELEASE);
  delay(500);
}

void backward2() {
  motor2->run(BACKWARD);
  delay(500);
  motor2->run(RELEASE);
  delay(500);
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



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  AFMS.begin();
  motor4->run(RELEASE);
  motor3->run(RELEASE);
  motor4->setSpeed(50);
  motor3->setSpeed(50);
  motor2->setSpeed(50);
  delay (2000);
  Serial.println("Stopped");
  delay(100);
  Serial.println();
  Serial.print("Motor Number: ");
}

void loop() {
  // put your main code here, to run repeatedly:
  int i;
  int motor_number;
  String serial_chars;

  while (Serial.available() == 0) {  }
  serial_chars = Serial.readStringUntil('\n');
  //say what you got
  Serial.print("I received");
  Serial.println(serial.chars);
  motor_number = serial_chars.toInt();
  
  Serial.println();
  Serial.print("Motor number: ");
}
