import numpy as np
import imutils
import cv2

def get_boundaries(oriframe, threshold):
    net = cv2.dnn.readNetFromCaffe("../Model/MobileNetSSD_deploy.prototxt.txt",
                                   "../Model/MobileNetSSD_deploy.caffemodel")

    #ret, innerframe = cap.read()
    innerframe = imutils.resize(oriframe, width=400)

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
    #print(dimensions)
    for dimension in dimensions:
        startX = dimension[0]
        startY = dimension[1]
        endX = dimension[2]
        endY = dimension[3]
        confidence = dimension[4]

        cv2.rectangle(innerframe, (startX*2, startY*2), (endX*2, endY*2),
                      (0, 255, 0), 2)
        y = startY - 15 if startY - 15 > 15 else startY + 15
        # draw the prediction on the frame
        label = "{}: {:.2f}%".format("Person",
                                     confidence * 100)
        cv2.putText(innerframe, label, (startX*2, y*2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return cv2.cvtColor(innerframe, cv2.COLOR_RGB2BGR)

def transformInfo(corners, knownHeight, knownWidth, offset):
    # offset is meant for coordinates on the warped image
    # transformations performed with this matrix are relative to the offset point
    # will not affect euclidean distance
    (c1, c2, c3, c4) = corners
    widthA = np.sqrt(((c3[0] - c4[0]) ** 2) + ((c3[1] - c4[1]) ** 2))
    widthB = np.sqrt(((c2[0] - c1[0]) ** 2) + ((c2[1] - c1[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((c2[0] - c3[0]) ** 2) + ((c2[1] - c3[1]) ** 2))
    heightB = np.sqrt(((c1[0] - c4[0]) ** 2) + ((c1[1] - c4[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    if maxWidth/maxHeight > knownWidth/knownHeight:
        maxWidth = maxHeight * knownWidth/knownHeight
    dst = np.array([
        [offset, offset],
        [offset + maxWidth - 1, offset],
        [offset + maxWidth - 1 , offset + maxHeight - 1],
        [500, offset + maxHeight - 1]], dtype="float32")
    hMatrix, M = cv2.findHomography(corners, dst)
    return knownHeight/maxHeight, knownWidth/maxWidth, hMatrix

def bottomCentres(points):
    bc = []
    for p in points:
        bc.append((2*int((p[0]+p[2])/2),2*int(p[3])))
    return bc

def transformPoints(points, hMatrix):
    if(len(points) == 0):
        return np.array([])
    return cv2.perspectiveTransform(np.float32(points).reshape(-1, 1, 2), hMatrix)

def getDistance(a, b, h, w):
    return np.sqrt(((a[0][0] - b[0][0]) * w) ** 2 + ((a[0][1] -b[0][1])*h) ** 2)

def dbscan(epsilon, minPts, points, height, width, clusterIndex):
    cluster = 0
    for i in range(len(points)):
        if clusterIndex[i] != 0:
            continue
        neighbours = []
        for j in range(len(points)):
            if(i != j):
                if(getDistance(points[i], points[j], height, width) <= epsilon):
                    print(i, j, getDistance(points[i], points[j], height, width), getDistance(points[j], points[i], height, width))
                    neighbours.append(j)
        if(len(neighbours) < minPts):
            clusterIndex[i] = -1
            continue
        cluster += 1
        clusterIndex[i] = cluster
        while(len(neighbours) != 0):
            q = neighbours[0]
            neighbours.pop(0)
            if(clusterIndex[q] == -1):
                clusterIndex[q] = cluster
            if(clusterIndex[q] != 0):
                continue
            clusterIndex[q] = cluster
            newNeighbours = []
            for j in range(len(points)):
                if (q != j):
                    if (getDistance(points[q], points[j], height, width) <= epsilon):
                        newNeighbours.append(j)
            if(len(newNeighbours) >= minPts):
                neighbours += newNeighbours

def transformedImage(image, points, x, y, hMatrix, height, width, originalPoints):
    warped = cv2.warpPerspective(image, hMatrix, (x, y))
    for i in range(len(points)):
        cv2.circle(warped, (int(points[i][0][0]), int(points[i][0][1])), radius=3, color=(0, 0, 255), thickness=-1)
        for j in range(len(points)):
            #print(np.sqrt(((points[i][0][0] - points[j][0][0]) * width) ** 2 + ((points[i][0][1] - points[j][0][0])*height) ** 2))
            #print(abs(points[i][0][0] - points[j][0][0]) * width)
            if(3  > getDistance(points[i], points[j], height, width)):#np.sqrt(((points[i][0][0] - points[j][0][0]) * width) ** 2 + ((points[i][0][1] - points[j][0][1])*height) ** 2)):
                cv2.line(image, (originalPoints[i][0], originalPoints[i][1]), (originalPoints[j][0], originalPoints[j][1]), (0, 0, 0), thickness=3)

    return warped

if __name__ == "__main__":
    cap = cv2.VideoCapture("../resources/View_001/frame_%04d.jpg", cv2.CAP_IMAGES)
    hasDanger = 0
    while True:
        ret, oriframe = cap.read()
        innerframe, dimensions = get_boundaries(oriframe, 0.1)
        trc = bottomCentres(dimensions)
        frame = display_frame(oriframe, dimensions)
        points = np.array([[53, 248], [87, 198], [141, 205], [117, 257]]) #pass 4 points here
        height, width, hMatrix = transformInfo(points, 5, 5, 500) #pass width, height where 5, 5 is
        newTrc = transformPoints(trc, hMatrix)
        warped = transformedImage(frame, newTrc, 1500, 1500, hMatrix, height, width, trc)
        clusterIndex = [0] * len(trc)
        dbscan(3, 1, newTrc, height, width, clusterIndex)
        #cv2.imshow("Warped", warped)
        vals = [(0, 0, 255), (0, 0, 0), (255, 0, 0), (255, 255, 0), (0, 255, 255), (255, 255, 255)]
        toIncrement = 0
        for i in range(len(clusterIndex)):
            if(clusterIndex.count(clusterIndex[i]) >= 2 and clusterIndex[i] != -1):
                toIncrement += 1
            cv2.circle(frame, (trc[i][0], trc[i][1]), radius=3, color=vals[clusterIndex[i]], thickness=-1)
        if(toIncrement != 0):
            hasDanger += toIncrement
        else:
            hasDanger = 0
            print("no more AAAA")
        cv2.imshow("Frame", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        if(hasDanger > 6):
            print("AAAA")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
