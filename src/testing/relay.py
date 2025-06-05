import signal
import sys
import time
import RPi.GPIO as GPIO

RELAY = 17  # Define the relay GPIO pin

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY, GPIO.OUT)

# Define clean exit handler
def clean_exit(signum=None, frame=None):
    print("\nCleaning up GPIO and exiting...")
    GPIO.output(RELAY, GPIO.LOW)
    GPIO.cleanup()
    sys.exit(0)

# Handle Ctrl+C and Ctrl+Z
signal.signal(signal.SIGINT, clean_exit)   # Ctrl+C
signal.signal(signal.SIGTSTP, clean_exit)  # Ctrl+Z

# Main loop
try:
    while True:
        GPIO.output(RELAY, GPIO.LOW)
        print("Relay ON")
        time.sleep(2)
        GPIO.output(RELAY, GPIO.HIGH)
        print("Relay OFF")
        time.sleep(2)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    clean_exit()
