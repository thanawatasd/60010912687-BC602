#include <ESP8266WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>
#include <Servo.h>
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>

const uint16_t WAIT_TIME = 1000;

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4
#define CLK_PIN   D5 //สำหรับ NodeMcu
#define CS_PIN    D8 //สำหรับ NodeMcu
#define DATA_PIN  D7

Servo myservo; 
int buttonPin = D2;
int buttonState = 0;
int value = 0;
int IR = D0;// เข้า
int IR2 = D1;// ออก
//int servopin = D0;
#define wifi_ssid "OPPO F9"
#define wifi_password "12345678"
#define mqtt_server "34.87.70.171"
#define ir "sensor/ir"
#define irout "sensor/irout"
#define current "sensor/newir"
WiFiClient espClient;
PubSubClient client(espClient);

MD_Parola P = MD_Parola(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);

void setup() {
  Serial.begin(115200);
  pinMode(IR, INPUT);
   pinMode(IR2, INPUT);
    pinMode(buttonPin, INPUT_PULLUP);// กำหนดขา buttonPin เป็นโหมด INPUT
//  myservo.attach(servopin );
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  P.begin(0000);
}
String macToStr(const uint8_t* mac)
{
  String result;
  for (int i = 0; i < 6; ++i) {
    result += String(mac[i], 16);
    if (i < 5)
      result += ':';
  }
  return result;
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(wifi_ssid);
  WiFi.begin(wifi_ssid, wifi_password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}///
void reconnect() {
  while (!client.connected()) {
      Serial.print("Attempting MQTT connection...");
      String clientName;  
      clientName += "esp8266-";
      uint8_t mac[6];
      WiFi.macAddress(mac);
      clientName += macToStr(mac);
      clientName += "-";
      clientName += String(micros() & 0xff, 16);
      Serial.print("Connecting to ");
      Serial.print(mqtt_server);
      Serial.print(" as ");
      Serial.println(clientName);
  if (client.connect((char*) clientName.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
int newir;
//------------------------------------------------------------------
     int counts_now;
int counts = 0;
int count_status = 0;
//------------------------------------------------------------------
int counts_out;
int countsout = 0;
int count_out = 0;

void loop() {
 if (!client.connected()) {
        reconnect();
      }
      client.loop();
int sensorIN = analogRead(IR);
int sensorOUT = analogRead(IR2);
buttonState = digitalRead(buttonPin); // อ่านค่าสถานะขา3
P.print(newir);
 //Serial.println(sensorIR);
 if (buttonState == 1) {
  } else {
    newir = 0 ;
    counts = 0;
    countsout = 0;
    client.publish(current, String(newir).c_str(), true);
    Serial.println(String(counts).c_str());
    client.publish(ir, String(counts).c_str(), true);
    client.publish(irout, String(countsout).c_str(), true);
  }
if(counts_now!= counts){
  counts_now = counts;
  //Serial.print("counts_now = ");
  //Serial.println(counts);
}

if(counts_out!= countsout){
  counts_out = countsout;
}

 if ( sensorIN < 1000 ){
  
count_status = 1;

}
else{
   
    if(count_status == 1){
    count_status = 0;
    counts++;
     newir++;
     client.publish(current, String(newir).c_str(), true);
    Serial.println(String(counts).c_str());
    client.publish(ir, String(counts).c_str(), true);
  }
  
}
if ( sensorOUT< 1000 ){
  
count_out = 1;

}
else{
   
    if(count_out == 1){
    count_out = 0;
    countsout++;
    newir = counts - countsout;
    client.publish(current, String(newir).c_str(), true);
    Serial.println(String(countsout).c_str());
    client.publish(irout, String(countsout).c_str(), true);
  }
  
}
//client.publish(current, String(newir).c_str(), true);
  //Serial.println(String(counts).c_str());
      //client.publish(ir, String(counts).c_str(), true);

}
