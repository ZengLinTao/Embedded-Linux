from temperature import Temperature
import time

if __name__ == "__main__":
    while True:
        temperature = Temperature()
        temperature.pub_temperature()
        time.sleep(1)