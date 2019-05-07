from temperature import Temperature
from light import Light
from cam import Camera
import time
import RPi.GPIO as GPIO

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    camera = Camera("pub_monitor_thread")
    camera.start()
    while True:
        # get and pub temperature
        temperature = Temperature()
        temperature.pub_temperature()
        # get and pub light
        light = Light(17, 0)
        light.pub_light()
        time.sleep(1)