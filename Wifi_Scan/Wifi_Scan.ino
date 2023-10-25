#include "WiFi.h"

#define redLedPin 2
#define yellowLedPin 22
#define blueLedPin 23

void setup(){
  pinMode(redLedPin, OUTPUT);
  pinMode(blueLedPin, OUTPUT);
  pinMode(yellowLedPin, OUTPUT);

  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(1000);
}


void loop(){
  Serial.println("Scanning available networks...");
  digitalWrite(redLedPin, HIGH);
  digitalWrite(blueLedPin, LOW);
  int n = WiFi.scanNetworks();
  if (n!= 0){
    digitalWrite(redLedPin, LOW);
    digitalWrite(blueLedPin, HIGH);
    Serial.print(n);
    Serial.println("networks found");
    for (int i=0;i<n;++n){
      Serial.print("network "); Serial.print(i + 1); Serial.print(":");
      Serial.print(WiFi.SSID(i));
      Serial.print(WiFi.RSSI(i));
      Serial.println((WiFi.encryptionType(i) ==  WIFI_AUTH_OPEN)? "open":"***");
      delay (50);

    }
  }
  else{
    Serial.println("no available networks");
    digitalWrite(redLedPin, LOW);
    digitalWrite(blueLedPin, LOW);
    digitalWrite(yellowLedPin, HIGH);
  }
  Serial.println("\n________________________________________________________________________________________________________\n");
  delay(5000);
}
