#include <WiFi.h>
#include <WiFiClient.h>

//configuracion de la red wifi
const char * WIFI_SSID = "TECHLAB";
const char * WIFI_PASS = "catolica11";

//configuracion del socket del cliente
WiFiClient client;
const char* server_ip = "192.168.68.65";
const int server_port = 8080;

//configuracion de los pines de los LEDs
const int blue=26;
const int white=32;
const int red=33;

void setup(){
    Serial.begin(115200);

    //conexion a la red wifi
    WiFi.begin(WIFI_SSID,WIFI_PASS);
    while(WiFi.status()!=WL_CONNECTED){
        delay(1000);
        Serial.println("Conectando a la red WIFI...");
    }
    Serial.println("Conexion a la red establecida");
    //configuracion de los pines
    pinMode(blue, OUTPUT);
    pinMode(white, OUTPUT);
    pinMode(red, OUTPUT);
}

void TurnOnLed(int on,int off,int off2)
{
  digitalWrite(on, HIGH);
  digitalWrite(off, LOW);
  digitalWrite(off2, LOW);
}

void TurnOffAllLeds()
{
  digitalWrite(blue, LOW);
  digitalWrite(white, LOW);
  digitalWrite(red, LOW);
}

void loop(){
    // Establecer la conexión con el servidor
  WiFiClient client;
  if (client.connect(server_ip, server_port)) {
    Serial.println("Conectado al servidor");

    while (client.connected()) {
      client.println("Hola desde ESP32");
      Serial.println("Esperando mensaje del servidor...");

    // Leer datos del servidor
    String message = client.readStringUntil('\n');
    Serial.print("Mensaje recibido del servidor: ");
    Serial.println(message);
    if(message=="BLUE"){
      TurnOnLed(blue,white,red);
    }
    if(message=="WHITE"){
      TurnOnLed(white,blue,red);
    }
    if(message=="RED"){
      TurnOnLed(red,blue,white);
    }
    if(message=="OFF"){
      TurnOffAllLeds();
    }
    }
    

  } else {
    Serial.println("Error de conexión al servidor");
  }

  delay(2000);  // Esperar 5 segundos antes de hacer la próxima conexión
}