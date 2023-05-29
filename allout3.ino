#include <Wire.h> //library scl sda
#include <Servo.h> //library servo
#include <Adafruit_MLX90614.h> //library sensor gy906
#include <LiquidCrystal_I2C.h> //library lcd i2c

String inBytes; //variabel menerima data dari serial
float ingy906; //variabel keluaran gy906
Adafruit_MLX90614 mlx = Adafruit_MLX90614(); //deklarasi gy906
int pinBuzzer = 6; //buzzer pin 6
Servo myservo; //servo
LiquidCrystal_I2C lcd(0x27, 16, 2); //lcd 16x2 alamat i2c 0x27
const int trigPin = 11, echoPin = 12; //pin trigger, echo hcsr 11,12
long duration; int distance; //variabel untuk jarak hcsr
int konter, trigkon = LOW; //counter orang lewat dan trigger counter

void setup(){
  Serial.begin(9600); //serial yg dipakai 9600
  myservo.attach(9); myservo.write(0); //servo pin 9, write 0' pada setup
  mlx.begin(); //gy906 begin
  lcd.begin(); //lcd begin
  pinMode(pinBuzzer, OUTPUT); //pin buzzer sbg output
  pinMode(trigPin, OUTPUT); pinMode(echoPin, INPUT); //pin trigger hcsr sbg output, echo sbg input
}

void loop(){
  //lcd.backlight();
  digitalWrite(trigPin, LOW); delayMicroseconds(2); 
  digitalWrite(trigPin, HIGH); delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH); //durasi ultrasonik dari trigger ke echo
  distance = duration * 0.034 / 2; //konversi dari durasi menjadi jarak
  if ((distance < 10) && (trigkon == LOW)) trigkon = HIGH; // jika jarak < 10 dan trigger low, maka trigger high
  else if ((distance > 11) && (trigkon == HIGH)){ //jika jarak > 11 dan trigger high
    konter++; //nilai konter + 1
    trigkon = LOW; //trigger kembali low
    myservo.write(0); //servo 0'
  }
  ingy906 = mlx.readObjectTempC(); //gy906 membaca suhu object (dalam 'C)
  
  if (ingy906 > 38) digitalWrite(pinBuzzer, HIGH); //jika suhu > 38' maka buzzer menyala
  if (Serial.available() > 0){ //jika ada serial masuk
    inBytes = Serial.readStringUntil('\n'); //baca serial hingga enter atau \n
    if ((inBytes == "on") && (ingy906 > 30)){ //jika serial masuk adalah "on" dan suhu > 30
      Serial.print(ingy906); //mengirim serial suhu skrg
      myservo.write(90); //servo 90'
    }
    else if ((inBytes == "off") && (ingy906 < 30)){ //jika serial masuk "off" dan suhu < 30
      Serial.print(ingy906); //mengirim serial suhu skrg
    }
    else {
      Serial.print(ingy906); //mengirim serial suhu skrg
    }
  }
  lcd.setCursor(0, 0); lcd.print("No:"); //set cursor dan print pada lcd
  lcd.setCursor(4, 0); lcd.print(konter);
  lcd.setCursor(6, 0); lcd.print("Suhu:");
  lcd.setCursor(12, 0); lcd.print(ingy906);
  lcd.setCursor(0, 1); lcd.print("14/01/2023");
}
