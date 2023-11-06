const int sensorPin = 2;
const int ledPin = 7;
volatile unsigned int pulseCount = 0;
float volume = 0.0; // in milliliters
const float calibrationFactor = 7.5; // You need to calibrate this value based on your sensor and setup

void setup() {
  pinMode(sensorPin, INPUT);
  pinMode(ledPin, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(sensorPin), countPulse, RISING);
  Serial.begin(9600);
}

void loop() {
  // Calculate the volume based on calibration factor
  volume = pulseCount * calibrationFactor;
  
  Serial.print("Volume: ");
  Serial.print(volume);
  Serial.println(" mL");
  
  if (volume > 500.0) {
    digitalWrite(ledPin, HIGH);
  } else {
    digitalWrite(ledPin, LOW);
  }
}

void countPulse() {
  // Increment the pulse count when a pulse is detected
  pulseCount++;
}
