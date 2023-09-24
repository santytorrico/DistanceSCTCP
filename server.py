import socket

SENSOR_DATA_FORMAT = "SENSOR: {}  DATA: {}"
ACTUATOR_COMMAND_FORMAT = "ACTUATOR: {} COMMAND: {}"

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Accepted connection from {client_address}")
                client_handler = ClientHandler(client_socket, self)
                client_handler.start()

class ClientHandler:
    def __init__(self, socket):
        self.socket = socket

    def start(self):
        with self.socket:
            while True:
                data = self.socket.recv(1024).decode("utf-8")
                if not data:
                    break
                if data.startswith("SENSOR"):
                    # Parse sensor data message
                    parts = data.split()
                    sensor_id = parts[1]
                    sensor_reading = parts[-1]
                    
                    # Process ultrasonic sensor data
                    if "UltrasonicSensor01" in sensor_id:
                        distance = int(sensor_reading)
                        print(f"Received ultrasonic sensor data: {distance} cm")

if __name__ == "__main__":
    host = "192.168.1.137" 
    port = 8080  

    server = Server(host, port)
    server.run()
