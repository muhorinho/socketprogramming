import random
import socket
import threading
import time

from Server import SensorServer


class SensorClient:
    def __init__(self, host='localhost', port=5000, interval=60):
        self.host = host
        self.port = port
        self.interval = interval
        self.running = False
        self.sensor_id = None

    def start(self):
        self.running = True
        self.sensor_id = str(threading.get_ident())
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f'Connected to server {self.host}:{self.port}')
        while self.running:
            data = self.get_sensor_data()
            self.client_socket.sendall(f'{self.sensor_id}:{data}'.encode())
            print(f'Sent data to server: {data}')
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.client_socket.close()
        print('Client stopped')
        
    def get_sensor_data(self):
        temperature = round(random.uniform(15.0, 30.0), 2)
        humidity = round(random.uniform(30.0, 70.0), 2)
        return f'temperature={temperature},humidity={humidity}'

if __name__ == '__main__':
    # Create a SensorServer object and start it in a separate thread
    server = SensorServer()
    server_thread = threading.Thread(target=server.start)
    server_thread.start()

    # Create a SensorClient object and start it in a separate thread
    client = SensorClient()
    client_thread = threading.Thread(target=client.start)
    client_thread.start()

    # Wait for the server and client threads to complete
    server_thread.join()
    client_thread.join()