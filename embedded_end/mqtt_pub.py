import paho.mqtt.publish as publish

HOST = '47.107.248.182'
PORT = 1883

def pub_info(topic, payload):
    publish.single(topic, payload=payload,hostname= HOST, port= PORT )