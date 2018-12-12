import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

RUNNING = True

green = 17
red = 27
blue = 22

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100

RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

RED.start(1)
GREEN.start(1)
BLUE.start(1)


def set_led(r,g,b):
    RED.ChangeDutyCycle(r)
    GREEN.ChangeDutyCycle(g)
    BLUE.ChangeDutyCycle(b)