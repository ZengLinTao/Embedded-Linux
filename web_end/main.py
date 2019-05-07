from flask import Flask,render_template,jsonify, Response
from mqtt_sub import Subscriber
import os
import sys
import time
from threading import Thread
import json
from PIL import Image
import cv2
import base64
import numpy as np
import io

temperature = list()
light = list()
image = None

class mqtt_sub_thread(Thread):
    """
        thread for mqtt subscriber

        thread_name: `str` the name for thread \n
        topic: `str` the topic need to be subscribe
    """
    def __init__(self, thread_name, topic):
        Thread.__init__(self, name=thread_name)
        self.__topic__ = topic    
        self.__subscriber__ = Subscriber(topic)
        self.__subscriber__.on_data = on_data

    def run(self):
        self.__subscriber__.subscribe()
        
class ClientPostData:
    def __init__(self, topic, time, data):
        self.__topic__ = topic
        self.__time__ = time
        self.__data__ = data

    @property
    def topic(self):
        return self.__topic__
    
    @property
    def time(self):
        return self.__time__

    @property
    def data(self):
        return self.__data__

def post_data_2_json(obj):
    return {
        "topic":obj.topic,
        "time":obj.time,
        "data":obj.data
    }

def on_data(topic ,data):
    """
    callback function for mqtt subscriber
    this function will be called after the subscriber recv data

    data: `json` the server sended info 
    """
    if data['topic'] == 'temperature':
        post_data = ClientPostData(data['topic'], data['time'], data['data'])
        temperature.append(post_data)  
    if data['topic'] == 'light':
        post_data = ClientPostData(data['topic'], data['time'], data['data'])
        light.append(post_data)
    if data['topic'] == 'monitor':
        # decode image from b64
        im = base64.b64decode(data['data'])
        arr = np.fromstring(im, dtype=np.uint8)
        arr = np.reshape(arr, (480,960,3))
        global image
        image = Image.fromarray(arr)
mqtt_sub_thread_ = mqtt_sub_thread("temperature_thread", "temperature")
mqtt_sub_thread_.start()
light_mqtt_sub_thread = mqtt_sub_thread("light_thread", "light")
light_mqtt_sub_thread.start()
monitor_mqtt_sub_thread = mqtt_sub_thread('monitor_thread', "monitor")
monitor_mqtt_sub_thread.start()

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template('index.html', title="title")

@app.route("/temperature/realtime")
def RealTimeTemperature():
    data = temperature[len(temperature) - 1]
    return json.dumps(data, default=post_data_2_json)

@app.route("/temperature")
def Temperature():
    return json.dumps(temperature, default=post_data_2_json)

@app.route("/light/realtime")
def RealTimeLight():
    data = light[len(light) - 1]
    return json.dumps(data, default=post_data_2_json)

@app.route("/light")
def Light():
    return json.dumps(light, default=post_data_2_json)

@app.route('/monitor')
def Monitor():
    byte_io = io.BytesIO()
    image.save(byte_io,'PNG')
    byte_io.seek(0)
    return Response(byte_io, mimetype="image/png")