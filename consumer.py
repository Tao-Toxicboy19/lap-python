from paho.mqtt import client as mqtt_client
import json
import random
from pymongo import MongoClient

# การตั้งค่า MQTT Broker
broker = '127.0.0.1'  # หรือ IP ที่ใช้เชื่อมต่อ
port = 11014
topic = "pico_sensor"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# การตั้งค่า MongoDB
url = "mongodb://root:example@localhost:27017/examdb?authSource=admin"
try:
    client = MongoClient(url)
    db = client["examdb"]
    collection = db["examdata"]
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# เชื่อมต่อกับ MQTT Broker
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

# ฟังก์ชันสำหรับการรับข้อความ
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        data = json.loads(message)
        print(f"Received `{data}` from topic `{msg.topic}`")
        
        # แทรกข้อมูลลง MongoDB
        try:
            collection.insert_one({"DeviceID": data[0], "Humidity": data[1], "Temperature": data[2]})
            print("Inserted message into MongoDB successfully!")
        except Exception as e:
            print(f"Failed to insert message into MongoDB: {e}")
    
    client.subscribe(topic)
    client.on_message = on_message

# ฟังก์ชันหลักสำหรับการรัน Consumer
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()