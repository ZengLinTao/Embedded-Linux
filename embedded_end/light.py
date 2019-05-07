import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
import mqtt_pub

class Light:
    def __init__(self, pin, chn):
        self.__light__ = 0
        self.__topic__ = "light"
        self.__pin__ = pin
        self.__chn__ = chn

    def setup(self ):
	    GPIO.setup(self.__pin__, GPIO.IN)

    def read_light(self):
        self.__light__ = abs(255 - ADC.read(0x48,self.__chn__))

    def pub_light(self):
        self.read_light()
        json_str =  '{"topic":"%s","time":%f, "data":%s}' % (self.__topic__, time.time(), self.__light__)
        mqtt_pub.pub_info(self.__topic__, json_str)