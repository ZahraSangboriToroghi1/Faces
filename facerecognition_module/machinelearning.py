import numpy as np
import cv2
import sklearn
import pickle
from django.conf import settings
import os

STATIC_DIR = settings.STATIC_DIR

# face detection
face_detector_model = cv2.dnn.readNetFromCaffe(
    os.path.join(STATIC_DIR, 'models/deploy.prototxt.txt'),
    os.path.join(STATIC_DIR, 'models/res10_300x300_ssd_iter_140000_fp16.caffemodel'))
# feature extraction
face_feature_model = cv2.dnn.readNetFromTorch(os.path.join(STATIC_DIR, 'models/openface.nn4.small2.v1.t7'))

# face recognition
face_recognition_model = pickle.load(open(os.path.join(STATIC_DIR, 'models/ml_face_person_identity.pkl'), mode='rb'))


def pipeline_model(path):
    img = cv2.imread(path)

    image = img.copy()
    h, w = img.shape[:2]
    img_blob = cv2.dnn.blobFromImage(img, 1, (300, 300), (104, 177, 123), swapRB=False, crop=False)
    face_detector_model.setInput(img_blob)
    detections = face_detector_model.forward()

    machinelearning_results = dict(
        face_detect_score=[],
        face_name=[],
        face_name_score=[],
        count=[]
    )

    count = 1

    if len(detections) > 0:
        for i, confidence in enumerate(detections[0, 0, :, 2]):
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                startx, starty, endx, endy = box.astype('int')
                cv2.rectangle(image, (startx, starty), (endx, endy), (0, 255, 0))

                # feature extraction
                face_roi = img[starty:endy, startx:endx]
                face_blob = cv2.dnn.blobFromImage(face_roi, 1 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=True)
                face_feature_model.setInput(face_blob)
                verctors = face_feature_model.forward()

                # predict with machine learning
                face_name = face_recognition_model.predict(verctors)
                face_score = face_recognition_model.predict_proba(verctors).max()

                text_face = '{} : {:.0f} %'.format(face_name, 100 * face_score)
                cv2.putText(image, text_face, (startx, starty), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

                cv2.imwrite(os.path.join(settings.MEDIA_ROOT, 'ml_output/process.jpg'), image)
                cv2.imwrite(os.path.join(settings.MEDIA_ROOT, 'ml_output/roi_{}.jpg'.format(count)), face_roi)

                machinelearning_results['count'].append(count)
                machinelearning_results['face_detect_score'].append(confidence)
                machinelearning_results['face_name'].append(face_name)
                machinelearning_results['face_name_score'].append(face_score)

                count += 1

    return machinelearning_results
