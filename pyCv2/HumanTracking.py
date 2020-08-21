import cv2

#def get_points(frame):
#
#


def display_frame(cap):
    ret, frame = cap.read()
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
