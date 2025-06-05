import RPi.GPIO as GPIO
import time
import signal
import sys
import cv2
import os
import numpy as np
from picamera2 import Picamera2
from playsound3 import playsound

# GPIO Pins
TRIG = 23
ECHO = 24
RELAY = 17

# Audio paths
base_dir = os.path.dirname(os.path.abspath(__file__))

CLEAN_AUDIO = os.path.abspath(os.path.join(base_dir, 'audio', 'clean.mp3'))
DIRTY_AUDIO = os.path.abspath(os.path.join(base_dir, 'audio', 'dirty.mp3'))

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

def detect_fluorescence_with_visual(picam2):
    # HSV bounds for fluorescence
    l_h, l_s, l_v = 127, 26, 0 
    u_h, u_s, u_v = 255, 177, 255

    detected = False
    start_time = time.time()

    while time.time() - start_time < 3:  # Show for 3 seconds
        frame = picam2.capture_array()
        image = frame.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, l_b, u_b)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            area = cv2.contourArea(c)
            if area > 500:
                detected = True
                cv2.drawContours(image, [c], -1, (255, 0, 0), 3)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.circle(image, (cx, cy), 7, (255, 255, 255), -1)
                    cv2.putText(image, "fluorescence", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        result = cv2.bitwise_and(image, image, mask=mask)

        cv2.imshow("Live Transmission", image)
        cv2.imshow("Result", result)

        k = cv2.waitKey(1) & 0xFF
        if k == 27 or cv2.getWindowProperty("Live Transmission", cv2.WND_PROP_VISIBLE) < 1:
            print("Window closed by user or ESC pressed.")
            print("\nCleaning up GPIO and exiting...")
            GPIO.output(RELAY, GPIO.LOW)
            GPIO.cleanup()
            break

        if detected:
            break

    # time delay
    time.sleep(2)
    cv2.destroyAllWindows()
    return detected

def clean_exit(signum=None, frame=None):
    print("\nCleaning up GPIO and exiting...")
    GPIO.output(RELAY, GPIO.LOW)
    GPIO.cleanup()
    sys.exit(0)

# Handle Ctrl+C and Ctrl+Z
signal.signal(signal.SIGINT, clean_exit)
signal.signal(signal.SIGTSTP, clean_exit)

def main():
    setup()
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)}))
    picam2.start()
    time.sleep(0.1)

    try:
        while True:
            distance = measure_distance()
            print(f"Distance: {distance} cm")

            if 10 <= distance <= 15:
                GPIO.output(RELAY, GPIO.LOW)
                print("Relay ON - checking for fluorescence")

                detected = detect_fluorescence_with_visual(picam2)

                GPIO.output(RELAY, GPIO.HIGH)
                print("Relay OFF")

                if detected:
                    print("Fluorescence detected: DIRTY")
                    playsound(DIRTY_AUDIO)
                else:
                    print("No fluorescence: CLEAN")
                    playsound(CLEAN_AUDIO)

            time.sleep(1)
    except KeyboardInterrupt:
        clean_exit()

if __name__ == "__main__":
    main()
