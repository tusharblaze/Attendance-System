import cv2
import pickle
from datetime import datetime
import sqlite3 as sk

dbs = sk.connect('mDatabase.db')
db= dbs.cursor()
'''db.execute("""CREATE TABLE student(

                  ID_NUMBER INTEGER,
                   STUDENT_NAME TEXT,
                   ENTRANCE_TIME TEXT,
                   ENTRANCE_DATE TEXT)""")'''

dbs.commit()
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade = cv2.CascadeClassifier('C:\\Users\\Pawan\\PycharmProjects\\ImageRecognition\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
recognizer.read("trainner.yml")
labels = {}
idNumber = list()
datedect = list()
timedect = list()
with open("labels.pickle","rb") as f:
    og_labels = pickle.load(f)
    labels = {v : k for k, v in og_labels.items()}

cap = cv2.VideoCapture(0)

while 1:
    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 4)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]

        id_, conf = recognizer.predict(roi_gray)
        if conf >= 35 and conf <= 75:
            print(id_)
            print(labels[id_])
            name= labels[id_]
            registration = int(id_)
            now = datetime.now()
            date= now.strftime("%d/%m/%Y")
            time = now.strftime("%I:%M:%S")
            cv2.putText(img, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), lineType=cv2.LINE_AA)
            if id_ not in idNumber:
                idNumber.append(registration)
                datedect.append(date)
                timedect.append(time)
                db.execute("INSERT INTO student(ID_NUMBER,STUDENT_NAME,ENTRANCE_TIME,ENTRANCE_DATE)VALUES(?,?,?,?)", (registration, name, time,date,))
    dbs.commit()
    cv2.imshow('img', img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
d = datetime.now()
with open('Attendance.txt','a+',encoding='utf-8') as f:
    f.write('\nDATE:-{}\n{}  :   {}   :    {}    :    {}\n'.format(d.strftime("%d/%m/%Y"),"ID_NO","NAME","ENTRANCE_TIME","ENTRANCE_DATE"))
    for i,j,k in zip(idNumber,datedect,timedect):
        f.write('  {}       {}         {}           {}\n'.format(i, labels[i], k, j))
#z = d.strftime("%d/%m/%Y")
db.execute("SELECT * FROM student")
print(db.fetchall())
dbs.commit()
cap.release()
dbs.close()
cv2.destroyAllWindows()