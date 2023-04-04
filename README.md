# Muhammed Buğa -19070963
# Sensor Client and Server

This is a simple implementation of a client-server application to handle sensor data.

## SensorClient Class

The `SensorClient` class is responsible for sending sensor data to a server.

### Parameters

- `host`: the IP address or hostname of the server. Default is `localhost`.
- `port`: the port number of the server. Default is `5000`.
- `interval`: the interval in seconds between data transmissions. Default is `60`.

### Methods

- `start()`: starts the client.
- `stop()`: stops the client.
- `get_sensor_data()`: generates random sensor data.

## SensorServer Class

The `SensorServer` class is responsible for receiving and processing sensor data from clients.

### Parameters

- `host`: the IP address or hostname of the server. Default is `localhost`.
- `port`: the port number of the server. Default is `5000`.
- `threshold`: the number of data points required to process the data. Default is `6`.

### Methods

- `start()`: starts the server.
- `stop()`: stops the server.
- `handle_client()`: handles data received from clients.
- `parse_sensor_data()`: extracts sensor ID and data from received messages.
- `process_sensor_data()`: processes sensor data.

## Usage

To use the `SensorClient` and `SensorServer` classes, simply create an instance of each class and call the `start()` method.

```python
client = SensorClient(host='localhost', port=5000, interval=60)
server = SensorServer(host='localhost', port=5000, threshold=6)

server_thread = threading.Thread(target=server.start)
server_thread.start()

client_thread = threading.Thread(target=client.start)
client_thread.start()

time.sleep(300)

client.stop()
server.stop()

client_thread.join()
server_thread.join()
