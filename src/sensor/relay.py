#Import all neccessary features to code.
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

try:
    GPIO.output(17, GPIO.HIGH)
    print("Relay ON")
    GPIO.output(17, GPIO.LOW)
    print("Relay OFF")
    GPIO.cleanup()

except KeyboardInterrupt:
    pass