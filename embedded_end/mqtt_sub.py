import paho.mqtt.client as client
import json
import time

HOST = '47.107.248.182'
PORT = 1883

def on_connect(client, userdata, flags, rc ):
    print("connecting...")

def on_message(client, userdata, msg):
    json_str = msg.payload.decode('UTF-8')
    data = json.loads(json_str)
    print("topic: %s \t time: %s \t temperature: %f:" % (data['topic'], data['time'], data['temperature']))

client = client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(HOST, PORT, 60)
client.subscribe('temperature')
client.loop_forever()