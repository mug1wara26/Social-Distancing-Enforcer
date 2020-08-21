import numpy as np
import imutils
import cv2
import os


def display_frame(cap, threshold):
    net = cv2.dnn.readNetFromCaffe(os.getcwd() + "/Model/MobileNetSSD_deploy.prototxt.txt", os.getcwd() + "/Model/MobileNetSSD_deploy.caffemodel")

    ret, frame = cap.read()
    frame = imutils.resize(frame, width=400)

    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                 0.007843, (300, 300), 127.5)

    net.setInput(blob)
    detections = net.forward()

    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]
        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > threshold:
            # extract the index of the class label from the
            # `detections`, then compute the (x, y)-coordinates of
            # the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            # draw the prediction on the frame
            label = "{}: {:.2f}%".format("Person",
                                         confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        frame = display_frame(cap, 0.7)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
