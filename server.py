import socket
import threading

SENSOR_DATA_FORMAT = "SENSOR: {}  DATA: {}"
# ACTUATOR_COMMAND_FORMAT = "ACTUATOR: {} COMMAND: {}"

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.clients_lock = threading.Lock()  # Cerradura para sincronización

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")

                with self.clients_lock:
                    self.clients.append(client_socket)

                # Create a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()

    def handle_client(self, client_socket):
        sensor_id = ""
        with client_socket:
            while True:
                try:
                    data = client_socket.recv(1024).decode("utf-8")
                    if not data:
                        break
                    if data.startswith("SENSOR"):
                        parts = data.split()
                        sensor_id = parts[1]
                        sensor_reading = parts[-1]
                        if "UltrasonicSensor01" in sensor_id:
                            CONECCTED=True
                            distance = int(sensor_reading)
                            print(f"Received ultrasonic sensor data: {distance} cm")
                            print(f"enviando distancia al actuador: {distance}")
                            self.send_distance_to_actuators(distance)
                except (socket.error, ValueError) as e:
                    print(f"Error handling client data: {e}")
                    break

        with self.clients_lock:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
                print("Cliente desconectado")
            client_socket.close()
            # Cerrar el socket después de desconectar

    def send_distance_to_actuators(self, distance):
        with self.clients_lock:
            for client_socket in self.clients:
                try:
                    if distance is not None and 0 <= distance <= 30:
                        if distance <= 10:
                            message = 'BLUE'
                        elif distance <= 20:
                            message = 'WHITE'
                        elif distance <= 30:
                            message = 'RED'
                        
                    else:
                        print(f"-----: ",distance)
                        message = 'OFF'

                    client_socket.send(message.encode("utf-8"))
                    print(f"mensaje enviado : {message}")

                except Exception as e:
                    print(f"Error sending distance to client: {e}")

if __name__ == "__main__":
    host = "192.168.68.65"
    port = 8080

    server = Server(host, port)
    server.run()
