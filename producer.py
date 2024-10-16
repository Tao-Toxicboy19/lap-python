from paho.mqtt import client as mqtt_client
import random
import time
import json

DeviceID = 100014
broker = 'localhost'  # หรือใช้ '127.0.0.1' ก็ได้
port = 11014
topic = "pico_sensor"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    client = mqtt_client.Client(client_id)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client):
    while True:
        time.sleep(1)
        temp = round(random.uniform(15, 50), 4)
        humi = int(random.randint(30, 70))
        data = [DeviceID, humi, temp]
        msg = json.dumps(data)
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"{topic}:{msg}")
        else:
            print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()