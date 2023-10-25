#include <FlowSensor.h>


#define type YFS201
#define pin 22 // pin -> interrupt pin

FlowSensor Sensor(type, pin);
unsigned long timebefore = 0; // Same type as millis()

//Uncomment if use ESP8266 and ESP32
void IRAM_ATTR count()
{
  Sensor.count();
}

// // Comment if use ESP8266 and ESP32
// void count()
// {
// 	Sensor.count();
// }

void setup() {
	Serial.begin(115200);
	Sensor.begin(count);
}

void loop() {
	if (millis() - timebefore >= 1000)
	{
		Sensor.read();
		Serial.print("Flow rate (L/minute) : ");
		Serial.println(Sensor.getFlowRate_m());
		timebefore = millis();
	}
}
