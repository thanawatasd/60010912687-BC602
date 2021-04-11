
#include <Wire.h>
#include <Adafruit_MLX90614.h>
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

const uint16_t WAIT_TIME = 1000;


#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define  CLK_PIN   18  // จองขา LED DOT
#define CS_PIN    19  // จองขา LED DOT
#define DATA_PIN  23 // จองขา LED DOT

MD_Parola P = MD_Parola(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);
 
int calibrate_Value = 0;
String temp;

boolean b = true;
boolean a = true;
char userInput;

//**********************************************************************
void setup()
{ 
  
  Serial.begin(115200);  
  mlx.begin(); 
  P.begin(000);
  //P.print("************");
  pinMode(25, INPUT_PULLUP); 
  a = true; 
  b = true; 
}

void loop() 
{ 
  //int sensorIN = analogRead(25);
    
if(digitalRead(25)== 1){ 
    a = true; 
    b = true; 
    delay(1000);
   // Serial.print(digitalRead(25));
   P.print("************");
   
}
if(a == true){
if(digitalRead(25)== 0){ 
  delay(20);

  if(digitalRead(25)== 0){ 
  a = false;   
  
   
  calibrate_Value = analogRead(32);
  calibrate_Value = map(calibrate_Value, 0, 4095, 0, 100);
  float valf = calibrate_Value/100.0;
  float newval = mapf(valf, 0.0, 1.0, 0.0, 10.0);   
  temp = mlx.readObjectTempC()+newval;
  Serial.print(5);  

 P.print(temp);

  
 
  
  }
} 
}
if(Serial.available()>0){
  userInput = Serial.read();
  if((userInput =='g')&&(b == true)){
      b = false;                
      Serial.print(temp);        
    }
 }  
}
  
double mapf(double val, double in_min, double in_max, double out_min, double out_max) {
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
//***************************************************************
