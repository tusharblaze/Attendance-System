import os
from PIL import Image
import numpy as np
import cv2
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image= os.path.join(BASE_DIR,"image")

face_cascade = cv2.CascadeClassifier(
        'C:\\Users\\Pawan\\PycharmProjects\\ImageRecognition\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')

recognizer=cv2.face.LBPHFaceRecognizer_create()

y_labels=[]
x_train = []
current_id=0
label_ids={}
image_array=[]

for root, dirs, files in os.walk(image):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("jpeg"):
            path = os.path.join(root,file)
            label =os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
            #print(label,path)
            if label in label_ids:
                pass
            else:
                label_ids[label] = current_id
                current_id+=1
            id_= label_ids[label]
            print(label_ids)
            #y_labels.append(label)
            #x_train.append(path)
            pil_image= Image.open(path).convert("L") #grayscale
            image_array= np.array(pil_image,"uint8")
            #print(image_array)

            face=face_cascade.detectMultiScale(image_array,1.3,5)

            for (x,y,w,h) in face:
                roi = image_array[y:y+h,x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

with open("labels.pickle","wb") as f:
    pickle.dump(label_ids,f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")