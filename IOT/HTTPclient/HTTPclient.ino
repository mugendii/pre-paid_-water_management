#include <WiFi.h>
#include <HTTPClient.h>
// 
//#include <WebServer.h>

int ledPin= 33;

const char *ssid = "4";
const char *password = "#defineOmaCollins'Net";
const char *serverIP = "192.168.0.102"; // Replace with your Django server's IP
const int serverPort = 8000; // Replace with your Django server's port
// 
//WebServer server(serverPort);

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  digitalWrite(ledPin, HIGH);
  if (WiFi.status() == WL_CONNECTED) {
    // 
    //server.on("/esp_1", HTTP_GET, [](){Serial.println("Hooo");});
    //server.begin();

    // Make a GET request to your Django server
    HTTPClient http;
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/esp_1/";
    
    http.begin(url);
    //http._followRedirects(true);
    int httpCode = http.GET();

    if (httpCode > 0) {
      String payload = http.getString();
      Serial.println("Response: " + payload);

      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
    } else {
      Serial.println("HTTP request failed");
    }

    http.end();
  }

  delay(5000); // Adjust delay as needed
}
