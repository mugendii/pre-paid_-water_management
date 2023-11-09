#include <WiFi.h>
#include <HTTPClient.h>
#include <WebServer.h>




#define redLedPin 2
#define yellowLedPin 22
#define greenLedPin 23
#define buzzerPin 18
#define FlowSensor 25
#define SolenoidPin 26


const char* ssid     = "iPIC-WIRELESS";
const char* password = "987654321jica";


volatile unsigned int pulseCount = 0;
float volume = 0.0; // in milliliters
const float calibrationFactor = 7.5; // You need to calibrate this value based on your sensor and setup


WiFiServer server(80);
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
    pinMode(redLedPin, OUTPUT);
    pinMode(yellowLedPin, OUTPUT);
    pinMode(greenLedPin, OUTPUT);      // set the LED pin mode
    pinMode(buzzerPin, OUTPUT);
    pinMode(FlowSensor, INPUT);
    pinMode(SolenoidPin, OUTPUT);
    delay(10);

    // We start by connecting to a WiFi network

    Serial.println();
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        digitalWrite(redLedPin, !digitalRead(redLedPin));
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected.");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  
  
  server.on("/", handle_root);
  server.begin();
  Serial.println("HTTP server started");
  delay(100); 
}

void loop() {
  server.handleClient();
  // put your main code here, to run repeatedly:
  digitalWrite(SolenoidPin, LOW);
  // Calculate the volume based on calibration factor
  volume = pulseCount * calibrationFactor;
  
  Serial.print("Volume: ");
  Serial.print(volume);
  Serial.println(" mL");
  
  if (volume > 1000.0) {
    pay();
  } else if(volume> 750) {
    lowlevel();
  }
  else if(volume> 500) {
    midlevel();
  }
  else  {
    high();
}
// Handle root url (/)
void handle_root() {
  server.send(200, "text/html", HTML);
}
void countPulse() {
  // Increment the pulse count when a pulse is detected
  pulseCount++;
}


void high(){
  digitalWrite(greenLedPin, HIGH);
}
void midlevel(){
  digitalWrite(yellowLedPin, HIGH);

}
void Lowlevel(){
  digitalWrite(redLedPin, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(1000);
  digitalWrite(redLedPin, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(1000);
  digitalWrite(redLedPin, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(1000);
  digitalWrite(redLedPin, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(1000);
  digitalWrite(redLedPin, HIGH);
  digitalWrite(buzzerPin, HIGH);
  delay(1000);

}
void pay(){
  digitalWrite(redLedPin, HIGH);
  digitalWrite(SolenoidPin, HIGH);

}
