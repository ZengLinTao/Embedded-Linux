import mqtt_pub
import time
from w1thermsensor import W1ThermSensor

class Temperature:
    def __init__(self):
        self.__sensor__ = W1ThermSensor()   
        self.__topic__ = "temperature"
        self.__temperature__ = 0

    def get_temperature(self):
        self.__temperature__ = self.__sensor__.get_temperature()

    def pub_temperature(self):
        self.get_temperature()
        json_str = '{"topic":"%s","time":%f, "temperature":%s}' % (self.__topic__, time.time(), self.__temperature__)
        mqtt_pub.pub_info(self.__topic__, json_str)