import socket
import threading


class SensorServer:
    def __init__(self, host='localhost', port=5000, threshold=6):
        self.host = host
        self.port = port
        self.threshold = threshold
        self.running = False
        self.sensor_data = {}

    def start(self):
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f'Server started on {self.host}:{self.port}')
        while self.running:
            conn, addr = self.server_socket.accept()
            print(f'New client connected: {addr}')
            threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def stop(self):
        self.running = False
        self.server_socket.close()
        print('Server stopped')

    def handle_client(self, conn, addr):
        while True:
            data = conn.recv(1024).decode()
            if not data:
                print(f'Client disconnected: {addr}')
                break
            print(f'Received data from client {addr}: {data}')
            sensor_id, sensor_data = self.parse_sensor_data(data)
            if sensor_id not in self.sensor_data:
                self.sensor_data[sensor_id] = []
            self.sensor_data[sensor_id].append(sensor_data)
            if len(self.sensor_data[sensor_id]) >= self.threshold:
                self.process_sensor_data(sensor_id, self.sensor_data[sensor_id])
                self.sensor_data[sensor_id] = []
        conn.close()

    def parse_sensor_data(self, data):
        sensor_id, sensor_data = data.split(':')
        return sensor_id, sensor_data

    def process_sensor_data(self, sensor_id, sensor_data):
        average_temperature = sum([float(data.split(',')[0].split('=')[1]) for data in sensor_data]) / len(sensor_data)
        average_humidity = sum([float(data.split(',')[1].split('=')[1]) for data in sensor_data]) / len(sensor_data)
        print(f'Sensor {sensor_id} data: average temperature={average_temperature}, average humidity={average_humidity}')