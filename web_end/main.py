from flask import Flask,render_template,jsonify
from mqtt_sub import Subscriber
import os
import sys
import time
from threading import Thread
import json
# start a sub thread to dealwith the data

temperature = list()

class mqtt_sub_thread(Thread):
    """
        thread for mqtt subscriber

        thread_name: `str` the name for thread \n
        topic: `str` the topic need to be subscribe
    """
    def __init__(self, thread_name, topic):
        Thread.__init__(self, name=thread_name)
        self.__topic__ = topic    
        self.__subscriber__ = Subscriber()
        self.__subscriber__.on_data = on_data

    def run(self):
        self.__subscriber__.subscribe(self.__topic__)
        
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

def on_data(data):
    """
    callback function for mqtt subscriber
    this function will be called after the subscriber recv data

    data: `json` the server sended info 
    """
    post_data = ClientPostData(data['topic'], data['time'], data['data'])
    if data['topic'] == 'temperature':
        temperature.append(post_data)
    

mqtt_sub_thread_ = mqtt_sub_thread("temperature_thread", "temperature")
mqtt_sub_thread_.start()

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
