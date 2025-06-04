import RPi.GPIO as GPIO
import time
import signal
import sys

# Pin configuration
TRIG = 23
ECHO = 24
RELAY = 17

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(RELAY, GPIO.OUT)

def setup():
    GPIO.output(TRIG, False)
    print("Waiting for sensor to settle...")
    time.sleep(2)

def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

def clean_exit(signum=None, frame=None):
    print("\nCleaning up GPIO and exiting...")
    GPIO.cleanup()
    sys.exit(0)

# Register signal handlers for Ctrl+C and Ctrl+Z
signal.signal(signal.SIGINT, clean_exit)   # Ctrl+C
signal.signal(signal.SIGTSTP, clean_exit)  # Ctrl+Z

def main():
    setup()
    while True:
        distance = measure_distance()
        print(f"Distance: {distance} cm")

        if 10 <= distance <= 15:
            GPIO.output(RELAY, GPIO.LOW)
            print("Relay ON")
        else:
            GPIO.output(RELAY, GPIO.HIGH)
            print("Relay OFF")

        time.sleep(1)

if __name__ == "__main__":
    main()
