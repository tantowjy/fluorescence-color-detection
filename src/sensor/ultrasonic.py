import RPi.GPIO as GPIO
import numpy as np
import time

# Pin configuration
TRIG = 23
ECHO = 24

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    print("Waiting for sensor to settle...")
    time.sleep(2)

def measure_distance():
    # Send trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10 microseconds
    GPIO.output(TRIG, False)

    # Wait for echo response
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound * time / 2
    return round(distance, 2)

def main():
    setup()
    try:
        while True:
            distance = measure_distance()
            print("Distance:", distance, "cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped by User")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()