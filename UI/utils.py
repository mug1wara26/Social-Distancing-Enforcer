import cv2


def create_circle(frame, x, y):
    cv2.circle(frame, (x, y), 2, (0, 255, 0), 2)
