#include <WiFi.h>
#include <HTTPClient.h>


#define redLedPin 2
#define yellowLedPin 22
#define greenLedPin 23
#define buzzerPin 18
#define FlowSensor 25
#define SolenoidPin 26


const char* ssid     = "iPIC-WIRELESS";
const char* password = "987654321jica";
const char *serverIP = "192.168.x.x"; // Replace with your Django server's IP
const int serverPort = 8000; // Replace with your Django server's port

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

    //server.begin();

}

void countPulse() {
  // Increment the pulse count when a pulse is detected
  pulseCount++;
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

/*void runHTTPserver(){
  WiFiClient client = server.available();   // listen for incoming clients

  if(client){
    Serial.println("New Client.");
    while (client.connected()){
      String request;
      if(client.available()){ //receive client request
        request = client.readString();
        Serial.println(request);
      }
      String identifier = "Command: ";
      String command;
      if(request.indexOf(identifier)>0){
        //extract actual command
        int charIndex = request.indexOf(identifier)+identifier.length();
        while(request.charAt(charIndex)!='\r'){
          command+=request.charAt(charIndex);
          charIndex++;
        }
        //send response
        client.println("HTTP/1.1 200 OK");
        client.println("Content-type:text/json");
        client.println();//end of header
        
        if(command=="Test")
          client.print("{\"Test\":\"Hello server\"}");
        else if(command=="OFF"){
          client.print("{\"Response\":\"Light OFF\"}");
        }
        else
          client.print("{\"Error\":\"Command does not exist\"}");
        
        client.println();//end of response
        break;
      }
    }
    
  }
}*/

void one(){
  
  digitalWrite(SolenoidPin, LOW);
  // Calculate the volume based on calibration factor
  volume = pulseCount * calibrationFactor;
  
  Serial.print("Volume: ");
  Serial.print(volume);
  Serial.println(" mL");
  
  if (volume > 1000.0) {
    pay();
  } else if(volume> 750) {
    Lowlevel();
  }
  else if(volume> 500) {
    digitalWrite(yellowLedPin, HIGH);
  }
  else  {
    digitalWrite(greenLedPin, HIGH);
  }
}
void two(){
  // put your main code here, to run repeatedly:
  digitalWrite(SolenoidPin, LOW);
  // Calculate the volume based on calibration factor
  volume = pulseCount * calibrationFactor;
  
  Serial.print("Volume: ");
  Serial.print(volume);
  Serial.println(" mL");
  
  if (volume > 2000.0) {
    pay();
  } else if(volume> 1750) {
    Lowlevel();
  }
  else if(volume> 1000) {
    digitalWrite(yellowLedPin, HIGH);
  }
  else  {
    digitalWrite(greenLedPin, HIGH);
  }
}
void three(){
  // put your main code here, to run repeatedly:
  digitalWrite(SolenoidPin, LOW);
  // Calculate the volume based on calibration factor
  volume = pulseCount * calibrationFactor;
  
  Serial.print("Volume: ");
  Serial.print(volume);
  Serial.println(" mL");
  
  if (volume > 3000.0) {
    pay();
  } else if(volume> 2750) {
    Lowlevel();
  }
  else if(volume> 1500) {
    digitalWrite(yellowLedPin, HIGH);
  }
  else  {
    digitalWrite(greenLedPin, HIGH);
  }
}

void loop() {
  //runHTTPserver();
  // put your main code here, to run repeatedly:
  if (WiFi.status() == WL_CONNECTED) {
    // Make a GET request to your Django server
    HTTPClient http;
    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/one";
    
    http.begin(url);
    int httpCode1 = http.GET();

    if (httpCode1 > 0) {
      String payload = http.getString();
      Serial.println("Response: " + payload);

      one();
    } else {
      Serial.println("HTTP request failed");
    }

    http.end();
 
    // Make a GET request to your Django server
    //HTTPClient http;
    String url2 = "http://" + String(serverIP) + ":" + String(serverPort) + "/two";
    
    http.begin(url2);
    int httpCode2 = http.GET();

    if (httpCode2 > 0) {
      String payload = http.getString();
      Serial.println("Response: " + payload);

      two();
    } else {
      Serial.println("HTTP request failed");
    }

    http.end();
  
    // Make a GET request to your Django server
    //HTTPClient http;
    String url3 = "http://" + String(serverIP) + ":" + String(serverPort) + "/three";
    
    http.begin(url3);
    int httpCode3 = http.GET();

    if (httpCode3 > 0) {
      String payload = http.getString();
      Serial.println("Response: " + payload);

      three();
    } else {
      Serial.println("HTTP request failed");
    }

    http.end();
  }
}
