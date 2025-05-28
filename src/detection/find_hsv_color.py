import cv2
import numpy as np

def nothing(x):
    pass

def find_color_code():
    # Use 0 for the default camera
    cap = cv2.VideoCapture(0)

    cv2.namedWindow("Live Transmission", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Tracking")
    cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
    cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
    cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame from camera.")
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        l_h = cv2.getTrackbarPos("LH", "Tracking")
        l_s = cv2.getTrackbarPos("LS", "Tracking")
        l_v = cv2.getTrackbarPos("LV", "Tracking")

        u_h = cv2.getTrackbarPos("UH", "Tracking")
        u_s = cv2.getTrackbarPos("US", "Tracking")
        u_v = cv2.getTrackbarPos("UV", "Tracking")

        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(hsv, l_b, u_b)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow("Live Transmission", frame)
        cv2.imshow("Mask", mask)
        cv2.imshow("Result", result)

        # Check for ESC key
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # ESC key
            print("ESC pressed. Exiting.")
            break

        # Check if the window was closed with the X button
        if cv2.getWindowProperty("Live Transmission", cv2.WND_PROP_VISIBLE) < 1:
            print("Window closed by user.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    find_color_code()