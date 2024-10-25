''''
Training Multiple Faces stored on a DataBase:
	==> Each face should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model will be saved on trainer/ directory. (if it does not exist, pls create one)
	==> for using PIL, install pillow library with "pip install pillow"

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18   

'''

import cv2
import numpy as np
from PIL import Image
import os

# Path for face image database
path = 'dataset'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("cascades//haarcascade_frontalface_default.xml");


# function to get the images and label data
def getImagesAndLabels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path)]
    face_samples = []
    face_ids = []

    for image_path in image_paths:
        PIL_img = Image.open(image_path).convert('L')  # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')

        face_id = int(os.path.split(image_path)[-1].split(".")[1])
        faces = detector.detectMultiScale(img_numpy)

        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y + h, x:x + w])
            face_ids.append(face_id)

    return face_samples, face_ids


print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces, face_ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(face_ids))

# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml')  # recognizer.save() worked on Mac, but not on Pi

# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(face_ids))))
