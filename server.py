import socket

SENSOR_DATA_FORMAT = "SENSOR: {} TIMESTAMP: {} DATA: {}"
ACTUATOR_COMMAND_FORMAT = "ACTUATOR: {} COMMAND: {}"

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.counter = 0

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
    def __init__(self, socket, server):
        self.socket = socket
        self.server = server

    def start(self):
        with self.socket:
            while True:
                data = self.socket.recv(1024).decode("utf-8")
                if not data:
                    break

                if data.startswith("SET"):
                    value = int(data[4:])
                    self.server.counter = value
                    print(f"Counter set to {value}")
                elif data.startswith("SENSOR"):
                    # Parse sensor data message
                    parts = data.split()
                    sensor_id = parts[1]
                    sensor_reading = parts[-1]
                    
                    # Check temperature and control LED
                    if "TemperatureSensor01" in sensor_id:
                        temperature = float(sensor_reading)
                        if temperature > 30.0:  # Adjust the threshold as needed
                            # Send command to turn on LED
                            led_command = ACTUATOR_COMMAND_FORMAT.format("LED01", "ON")
                            self.socket.send(led_command.encode("utf-8"))
                        else:
                            # Send command to turn off LED
                            led_command = ACTUATOR_COMMAND_FORMAT.format("LED01", "OFF")
                            self.socket.send(led_command.encode("utf-8"))
                elif data.startswith("GET"):
                    response = str(self.server.counter)
                    self.socket.send(response.encode("utf-8"))
                else:
                    print(f"Command not found: {data}")
          

if __name__ == "__main__":
    host = "127.0.0.1"  # Use your desired host IP
    port = 1000  # Use the desired port

    server = Server(host, port)
    server.run()
