import cv2
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import numpy as np


def predict_values(frame, faceCascade, model):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=4,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
    faces_list=[]
    preds=[]
    for (x, y, w, h) in faces:
        face_frame = frame[y:y+h,x:x+w]
        face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
        face_frame = cv2.resize(face_frame, (224, 224))
        face_frame = img_to_array(face_frame)
        face_frame = np.expand_dims(face_frame, axis=0)
        face_frame = preprocess_input(face_frame)
        faces_list.append(face_frame)
        if len(faces_list)>0:
            preds = model.predict(faces_list)
        for (mask, noMask) in preds:
            if mask > noMask:
                label = "Mask"
                color = (0, 255, 0)
            else:
                label = "No Mask"
                color = (0, 0, 255)
            label = "{}: {:.2f}%".format(label, max(mask, noMask) * 100)
            cv2.putText(frame, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
    return frame


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
    mask_model = load_model("mask_recog_ver2 (1).h5")
    while True:
        ret, frame = cap.read()

        cv2.imshow('Mask Prediction', predict_values(frame, face_cascade, mask_model))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
