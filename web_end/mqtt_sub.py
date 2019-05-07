import paho.mqtt.client as client
import json
import time



class Subscriber:
    def __init__(self, topic):
        self.__host__ = '47.107.248.182'
        self.__port__ = 1883
        self.__client__ = client.Client()
        self.__on_data = None
        self.__topic__ = topic

    def subscribe(self):
        self.__client__.on_connect = self.__on_connect__
        self.__client__.on_message = self.__on_message__
        self.__client__.connect(self.__host__, self.__port__, 60)
        self.__client__.subscribe(self.__topic__)
        self.__client__.loop_forever()

    def __on_connect__(self,client, userdata, flags, rc ):
        print("connecting...")

    def __on_message__(self,client, userdata, msg):
        json_str = msg.payload.decode("utf-8")
        json_str = json.loads(json_str)
        self.__on_data(self.__topic__,json_str)

    @property
    def on_data(self):
        return self.__on_data

    @on_data.setter
    def on_data(self, func):
        self.__on_data = func