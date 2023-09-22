#include <WiFi.h>
#include <WiFiClient.h>

//configuracion de la red wifi
const char * WIFI_SSID = "FLIA BOLEA ";
const char * WIFI_PASS = "BRUNOMAT";

// const char * SERVER_ADDRESS = "example.com";
// const int SERVER_PORT = 1000; //YOUR_PORT

//configuracion del socket del cliente
WiFiClient client;
const char* server_ip = "0.0.0.0";
const int server_port = 55555;

//configuracion de los pines de los LEDs
const int led1_pin=1;
const int led1_pin=2;
const int led1_pin=3;

void setup(){
    serial.begin(15200);

    //conexion a la red wifi
    WiFi.begin(WIFI_SSID,WIFI_PASS);
    while(WiFi.status()!=WL_CONNECTED){
        delay(1000);
        Serial.print("Conectando a la red WIFI...");
    }
    Serial.print("Conexion a la red establecida");
    //cconfiguracion de los pines
    pinMode(led1_pin, OUTPUT);
    pinMode(led2_pin, OUTPUT);
    pinMode(led3_pin, OUTPUT);
}

void loop(){
    //conecxion al servidor y recepcion de temperatura
    if(client.connect(server_ip, server_port))
    {
        string temperature_str= client.readStringUntil('\n');
        client.stop();
        if(temperature_str!="")
        {
            Serial.print("Temperatura recibida: ");
            Serial.println(temperature_str);
        }

        float temperature = temperature_srl.toFloat();
        //codigo para encender o apagar los LEDs
    }
}
