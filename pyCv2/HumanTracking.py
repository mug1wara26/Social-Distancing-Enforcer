from __future__ import print_function
from imutils.object_detection import non_max_suppression
import numpy as np
import imutils
import cv2
from time import sleep


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
    # draw the centres of the people
    return pick


def display_frame(cap):
    ret, frame = cap.read()
    for (xA, yA, wA, hA) in get_points(frame):
        cv2.rectangle(frame, (xA, yA), (wA, hA), (0, 255, 0), 2)
    if ret:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


<<<<<<< HEAD

=======
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        cv2.imshow('frame', display_frame(cap))
>>>>>>> 4ed3f34e4b826662f18b70f892cd9bba323586fd

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
