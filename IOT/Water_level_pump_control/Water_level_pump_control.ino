#include <WiFi.h>

#define trig_pin 23 // ESP32 pin GIOP23 connected to Ultrasonic Sensor's TRIG pin
#define Echo_pin 22 // ESP32 pin GIOP22 connected to Ultrasonic Sensor's ECHO pin
#define pump_pin 17


float duration_us, distance_cm;

const char* ssid     = "iPIC-WIRELESS";
const char* password = "987654321jica";


WiFiServer server(80);
void setup() {
  // put your setup code here, to run once:
   Serial.begin (115200);

  // configure the trigger pin to output mode
  pinMode(trig_pin, OUTPUT);
  // configure the echo pin to input mode
  pinMode(echo_pin, INPUT);








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
}

void loop() {
  // put your main code here, to run repeatedly:
 digitalWrite(TRIG_PIN, HIGH);
 delay(10);
// measure duration of pulse from ECHO pin
  duration_us = pulseIn(ECHO_PIN, HIGH);

  // calculate the distance
  distance_cm = 0.017 * duration_us;

  if (distance_cm > 40) {
    digitalWrite(pump_pin, HIGH);
  } else {
    digitalWrite(pump_pin, LOW);
    lcd.println(distance_cm);
  }

}
