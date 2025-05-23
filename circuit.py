
import time
import RPi.GPIO as GPIO
from adafruit_htu21d import HTU21D
import busio

def controlLED(led, on_off):
    GPIO.output(led, on_off)

def measure_distance():
    GPIO.output(trig, 1)
    GPIO.output(trig, 0)

    while(GPIO.input(echo) == 0):
        pass

    pulse_start = time.time()
    while(GPIO.input(echo) == 1):
        pass

    pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    return pulse_duration*340*100/2

def getTemperature(sensor):
    return float(sensor.temperature)

trig = 20
echo = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

leds = [5, 6, 12, 18, 23, 24]
for led in leds:
    GPIO.setup(led, GPIO.OUT)

sda = 2
scl = 3
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c)
