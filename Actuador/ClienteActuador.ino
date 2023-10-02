#include <WiFi.h>
#include <WiFiClient.h>

const char* ssid = "Tigo Oswaldo";       // Cambia esto a tu SSID de red WiFi
const char* password = "FAMILIA_2022";  // Cambia esto a tu contraseña de red WiFi
const char* serverIP = "192.168.1.137";  // Cambia esto a la dirección IP del servidor
const int serverPort = 8080;             // Cambia esto al puerto del servidor

void setup() {
  Serial.begin(115200);
  delay(10);

  // Conéctate a la red WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conexión WiFi establecida");

  // Conéctate al servidor
  WiFiClient client;
  while (!client.connect(serverIP, serverPort)) {
    Serial.println("Error al conectar con el servidor. Reintentando...");
    delay(1000);
  }
  Serial.println("Conexión al servidor establecida");
}

void loop() {
  // Espera a recibir datos del servidor
  WiFiClient client;
  while (!client.connect(serverIP, serverPort)) {
    Serial.println("Error al conectar con el servidor. Reintentando...");
    delay(1000);
  }

  // Lee los datos del servidor
  String response = "";
  while (client.available()) {
    char c = client.read();
    response += c;
  }

  // Procesa los datos recibidos (asumiendo que la distancia se envía como texto)
  if (!response.isEmpty()) {
    Serial.print("Distancia recibida del servidor: ");
    Serial.println(response);
    // Aquí puedes realizar acciones en función de la distancia recibida
  }

  // Cierra la conexión
  client.stop();

  // Espera antes de hacer otra solicitud al servidor
  delay(5000);
}