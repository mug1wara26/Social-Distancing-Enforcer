from __future__ import print_function
from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2

def get_points(frame):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    image = imutils.resize(frame, width=min(400, frame.shape[1]))
    orig = image.copy()
    (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),
                                            padding=(8, 8), scale=1.05)
    # draw the original bounding boxes
    for (x, y, w, h) in rects:
        cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
    pick = non_max_suppression(rects, probs=None, overlapThresh=0.5)
    # draw the final bounding boxes
    print(pick)
    centres = []
    for (xA, yA, wA, hA) in pick:
        centres.append([int((xA + wA) / 2), int((yA + hA) / 2)])
    return centres


def display_frame(cap):
    ret, frame = cap.read()
    for(x, y) in get_points(frame):
        cv2.circle(frame, (x, y), 1, (0, 0, 0), 1)
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
