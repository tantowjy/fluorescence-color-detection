import cv2
import numpy as np
from picamera2 import Picamera2
import time

def nothing(x):
    pass

def color_detection():
    # Initialize PiCamera2
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'BGR888', "size": (640, 480)}))
    picam2.start()

    time.sleep(0.1)  # Allow camera to warm up

    l_h, l_s, l_v = 127, 26, 0 
    u_h, u_s, u_v = 255, 177, 255

    while True:
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
                cv2.drawContours(image, [c], -1, (255, 0, 0), 3)
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.circle(image, (cx, cy), 7, (255, 255, 255), -1)
                    cv2.putText(image, "violet", (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        result = cv2.bitwise_and(image, image, mask=mask)

        cv2.imshow("Live Transmission", image)
        # cv2.imshow("Mask", mask)
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
    color_detection()
