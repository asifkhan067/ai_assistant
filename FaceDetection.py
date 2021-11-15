import cv2
import sys
import numpy
import time
import joblib
import json
import pywt
model = ''
with open('face_recognition_model.pkl', 'rb') as f:
    model = joblib.load(f)
size = 4
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

name_to_id_dic = {}
with open("name_id.json", "r") as f:
    name_to_id = json.load(f)
    name_to_id_dic = {v: k for k, v in name_to_id.items()}


def w2d(img, mode='haar', level=1):
    imArray = img

    imArray = cv2.cvtColor(imArray, cv2.COLOR_RGB2GRAY)
    imArray = numpy.float32(imArray)
    imArray /= 255

    coeffs = pywt.wavedec2(imArray, mode, level=level)

    coeffs_H = list(coeffs)
    coeffs_H[0] *= 0

    imArray_H = pywt.waverec2(coeffs_H, mode)
    imArray_H *= 255
    imArray_H = numpy.uint8(imArray_H)

    return imArray_H


def get_name():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        time.sleep(1)
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face = frame[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(face)
            if len(eyes) >= 2:

                zoom_raw_image = cv2.resize(face, (32, 32))
                img_har = w2d(face, 'db1', 5)
                zoom_img_har = cv2.resize(img_har, (32, 32))
                test_img = numpy.vstack((zoom_raw_image.reshape(
                    32*32*3, 1), zoom_img_har.reshape(32*32, 1)))
                prediction = model.predict(test_img.reshape(1, -1))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.imshow('Video', frame)
                video_capture.release()
                cv2.destroyAllWindows()
                if prediction:
                    cv2.putText(frame, name_to_id_dic[prediction[0]], (x-10, y-10),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    return name_to_id_dic[prediction[0]]
                else:
                    cv2.putText(frame, 'not recognized',
                                (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    return None
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()


# get_name()
