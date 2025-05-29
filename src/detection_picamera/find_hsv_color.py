import cv2
import numpy as np
import time
from picamera2 import Picamera2

def nothing(x):
    pass

def find_color_code():
    # Initialize the Picamera2
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"size": (640, 480)})
    picam2.configure(config)
    picam2.start()
    
    # Allow camera to warm up
    time.sleep(0.1)

    cv2.namedWindow("Live Transmission", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Tracking")
    cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

    while True:
        # Capture frame as numpy array
        frame = picam2.capture_array()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("LH", "Tracking")
        l_s = cv2.getTrackbarPos("LS", "Tracking")
        l_v = cv2.getTrackbarPos("LV", "Tracking")
        u_h = cv2.getTrackbarPos("UH", "Tracking")
        u_s = cv2.getTrackbarPos("US", "Tracking")
        u_v = cv2.getTrackbarPos("UV", "Tracking")

        lower_bound = np.array([l_h, l_s, l_v])
        upper_bound = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Live Transmission", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Result", result)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # ESC key
            print("ESC pressed. Exiting.")
            break

        if cv2.getWindowProperty("Live Transmission", cv2.WND_PROP_VISIBLE) < 1:
            print("Window closed by user.")
            break

    cv2.destroyAllWindows()
    picam2.stop()

if __name__ == "__main__":
    find_color_code()
