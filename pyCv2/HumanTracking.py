import numpy as np
import imutils
import cv2

def get_boundaries(cap, threshold):
    net = cv2.dnn.readNetFromCaffe("/Model/MobileNetSSD_deploy.prototxt.txt",
                                   "/Model/MobileNetSSD_deploy.caffemodel")

    ret, innerframe = cap.read()
    innerframe = imutils.resize(innerframe, width=400)

    (h, w) = innerframe.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(innerframe, (300, 300)),
                                 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    dimensions = []

    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the prediction
        confidence = detections[0, 0, i, 2]
        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence > threshold:
            # compute the (x, y)-coordinates of
            # the bounding box for the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            idx = int(detections[0, 0, i, 1])
            if(idx == 15):
                dimensions.append([startX, startY, endX, endY, confidence])

    return innerframe, dimensions


def display_frame(innerframe, dimensions):
    print(dimensions)
    for dimension in dimensions:
        startX = dimension[0]
        startY = dimension[1]
        endX = dimension[2]
        endY = dimension[3]
        confidence = dimension[4]

        cv2.rectangle(innerframe, (startX, startY), (endX, endY),
                      (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        # draw the prediction on the frame
        label = "{}: {:.2f}%".format("Person",
                                     confidence * 100)
        cv2.putText(innerframe, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return cv2.cvtColor(innerframe, cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    cap = cv2.VideoCapture("../resources/OneLeaveShop1front.mpg")

    while True:
        innerframe, dimensions = get_boundaries(cap, 0.7)
        frame = display_frame(innerframe, dimensions)
        cv2.imshow("Frame", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
