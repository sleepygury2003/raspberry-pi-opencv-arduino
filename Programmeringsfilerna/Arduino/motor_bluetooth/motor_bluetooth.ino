#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
int r = 0;
char bt = "S";
void setup()
{
  Serial.begin(9600);
 
  motor1.setSpeed(150);
  motor2.setSpeed(150);
  motor3.setSpeed(150);
  motor4.setSpeed(150);
  Stop();
}


void loop() {
bt=Serial.read();
motor1.setSpeed(150);
  motor2.setSpeed(150);
  motor3.setSpeed(150);
  motor4.setSpeed(150);

if(bt=='F') 
{
 forward(); 
 if (r > 0){
  r = r-1;
 }
}

if((bt=='B'))
{
 backward(); 
}

if((bt=='L'))
{
 left(); 
}

if((bt=='R'))
{
 right(); 
}

if((bt=='S'))
{
 Stop();
 if (r > 0){
  r = r-1;
 }
} 
if((bt=='s'))
{
 if (r == 0){
 Stop();
 delay(3000);
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
rightforward() ;
delay(1300);
r = 5;
}
}
 
if((bt=='I'))
{
 leftforward();
}
if((bt=='G'))
{
  motor1.setSpeed(255);
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
rightforward() ;
}
}
void forward()
{
  motor1.run(BACKWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(BACKWARD);
}

void backward()
{
  motor1.run(FORWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(FORWARD);
}
void right()
{
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}
void left()
{
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}
void Stop()
{
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
}


void leftforward()
{
  motor1.run(BACKWARD);
  motor2.run(FORWARD);
  motor3.run(FORWARD);
  motor4.run(BACKWARD);
}
void rightforward()
{
  motor1.run(FORWARD);
  motor2.run(BACKWARD);
  motor3.run(BACKWARD);
  motor4.run(FORWARD);
}
