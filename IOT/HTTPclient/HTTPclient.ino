#include <WiFi.h>
#include <HTTPClient.h>


#define ledPin 23

const char *ssid = "your-ssid";
const char *password = "your-password";
const char *serverIP = "192.168.x.x"; // Replace with your Django server's IP
const int serverPort = 8000; // Replace with your Django server's port

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    // Make a GET request to your Django server
    HTTPClient http;
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/your-api-endpoint";
    
    http.begin(url);
    int httpCode = http.GET();

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Response: " + payload);

      digitalWrite(ledPin HIGH);
    } else {
      Serial.println("HTTP request failed");
    }

    http.end();
  }

  delay(5000); // Adjust delay as needed
}
