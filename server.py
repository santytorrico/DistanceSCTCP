import socket

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
