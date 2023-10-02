#include <WiFi.h>
#include <NewPing.h>

const char * ssid = "TECHLAB";
const char * password = "catolica11";

const char * server_ip = "192.168.68.65";
const int server_port = 8080; //YOUR_PORT

#define TRIGGER_PIN 12  // Pin connected to the sensor's trigger
#define ECHO_PIN 13     // Pin connected to the sensor's echo
#define MAX_DISTANCE 200 // Maximum distance to measure (adjust as needed)

NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

void setup() {

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

}

void loop() {
  delay(5000);
  // Measure distance with the ultrasonic sensor
  unsigned int distance = sonar.ping_cm();

  if (distance != NO_ECHO) {
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.println(" cm");

    // Prepare the distance data as a string
    String distanceData = "SENSOR UltrasonicSensor01 DATA " + String(distance);

    // Send the data to the server
    sendDataToServer(distanceData);
  } else {
    Serial.println("Failed to read distance from the sensor");
  }
}

void sendDataToServer(String data) {
  WiFiClient client;

  if (!client.connected()) {
    if (client.connect(server_ip, server_port)) {
      Serial.println("Connected to server");
    } else {
      Serial.println("Failed to connect to server");
      return;  // Exit the function if the connection fails
    }
  }

  // Send the data to the server
  client.println(data);
}