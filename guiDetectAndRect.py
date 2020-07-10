from tkinter import *
from PIL import ImageTk,Image
import cv2
import pickle
from datetime import datetime
import sqlite3 as sk


def startRecognition():
    count = 0
    dbs = sk.connect('mDatabase.db')
    db = dbs.cursor()
    '''db.execute("""CREATE TABLE student(

                      ID_NUMBER INTEGER,
                       STUDENT_NAME TEXT,
                       ENTRANCE_TIME TEXT,
                       ENTRANCE_DATE TEXT)""")

    dbs.commit()'''
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(
        'C:\\Users\\Pawan\\PycharmProjects\\ImageRecognition\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')
    recognizer.read("trainner.yml")
    labels = {}
    idNumber = list()
    rig = list()
    n = list()
    name_= list()
    datedect = list()
    timedect = list()
    with open("labels.pickle", "rb") as f:
        og_labels = pickle.load(f)
        labels = {v: k for k, v in og_labels.items()}

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
                name = labels[id_]
                registration = int(id_)
                now = datetime.now()
                date = now.strftime("%d/%m/%Y")
                time = now.strftime("%I:%M:%S")
                cv2.putText(img, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 255), lineType=cv2.LINE_AA)
                if id_ not in idNumber:
                    idNumber.append(registration)
                    n.append(labels[registration])
                    datedect.append(date)
                    timedect.append(time)
                rig.append(registration)
                name_.append(labels[registration])
                count += 1
                if count == 15:
                    break



        cv2.imshow('img', img)

        k = cv2.waitKey(30) & 0xff
        if k == 27 or count == 10:
            break



    name = most_frequent(name_)
    reg = most_frequent(rig)
    print("Name-> {} \nRegistration-> {}".format(name,reg))
    CT =checkConfig(reg,name)
    d = datetime.now()
    with open('Attendance.txt', 'a+', encoding='utf-8') as f:
        f.write('\nDATE:-{}\n{}  :   {}   :    {}    :    {}\n'.format(d.strftime("%d/%m/%Y"), "ID_NO", "NAME","ENTRANCE_TIME", "ENTRANCE_DATE"))
    if CT:
        index_ = n.index(name)
        date = datedect[index_]
        time = timedect[index_]
        with open('Attendance.txt', 'a+', encoding='utf-8') as f:
            f.write('  {}       {}         {}           {}\n'.format(reg, name, time, date))
            db.execute("INSERT INTO student(ID_NUMBER,STUDENT_NAME,ENTRANCE_TIME,ENTRANCE_DATE)VALUES(?,?,?,?)",
                       (reg, name, time, date))
            # z = d.strftime("%d/%m/%Y")
        db.execute("SELECT * FROM student")
        print(db.fetchall())

    dbs.commit()
    cap.release()
    dbs.close()
    cv2.destroyAllWindows()

def most_frequent(ls):
    maximum = 0
    res = ls[0]
    for i in ls:
        freq = ls.count(i)
        if freq >= maximum:
            maximum = freq
            res = i
    return(res)
def checkConfig(id_val,name_val):
    name = sa.get()
    reg = sb.get()

    if name == name_val and int(reg) == id_val:
        print(f"Student's Name is: {sa.get()}")
        print(f"Registration ID is: {sb.get()}")
        print(f"Branch is: {sc.get()}")
        return(True)
    else:
        return(False)
root = Tk()


root.title('Attendace System')
root.geometry ("{0}x{1}".format(700, 500))


# create all of the main frames
top_frame = Frame(root, bg='gray', width=690, height=100, pady=3)
top_frame.pack(side=RIGHT,fill="x")
center = Frame(root, bg='lavender', width=690, height=100, padx=70, pady=90)

# layout all of the main frames
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
top_frame.grid(row=0, sticky="ew")
center.grid(row=1, sticky="nsew")

# create the widgets for the top frame
name_label = Label(top_frame, text='ATTENDANCE SYSTEM',fg="black",font="Helvetica 25 bold",bg='orange red',borderwidth=15,relief=SUNKEN)
name_label.grid(padx=160,pady=0)
#name_label.pack(padx=10)
#deviding centre_frame (student/teacher)
ctr_left = Frame(center, bg='yellow', width=350, height=300, padx=0, pady=25)
ctr_right = Frame(center, bg='lavender', width=350, height=200, padx=3, pady=3)
# create the center_left widgets(students)
sa=StringVar()
sb=StringVar()
sc=StringVar()

#writing student on top
student_label = Label(ctr_left, text='	STUDENT INFORMATION	  ',fg="blue",font=("Times New Roman",20,"bold"),bg="lavender")
student_label.grid(row=1,columnspan=2)
student_label2 = Label(ctr_right, text='	WEBCAM VIEWER  ',fg="blue",font=("Times New Roman",20,"bold"),bg="lavender")
student_label2.grid(row=1,columnspan=2)


#creating i
# nput labels
name_label = Label(ctr_left, text='First Name',fg="black",font=("Bahnschrift Condensed",18,"bold"),bg='yellow')
roll_label = Label(ctr_left, text='ID Number',fg="black",font=("Bahnschrift Condensed",18,"bold"),bg='yellow')
class_label = Label(ctr_left, text='Branch ',fg="black",font=("Bahnschrift Condensed",18,"bold"),bg='yellow')

#creating entries
entry_name_s = Entry(ctr_left, background="white",font=("Helvetica",18,"bold"),textvariable=sa)
entry_roll_s = Entry(ctr_left,background="white",font=("Helvetica",18,"bold"),textvariable=sb,)
entry_class_s = Entry(ctr_left, background="white",font=("Helvetica",18,"bold"),textvariable=sc)
#finally grid
name_label.grid(row=4, column=0,sticky=E)
entry_name_s.grid(row=4, column=1)
roll_label.grid(row=6, column=0,sticky=E)
entry_roll_s.grid(row=6, column=1)
class_label.grid(row=7, column=0,sticky=E)
entry_class_s.grid(row=7, column=1)
#creating buttons
buttonstudent=Button(ctr_left,text="START RECOGNITION",width=20,fg="dark blue",bg="grey",borderwidth=6,font="Helvetica 15 bold",command=startRecognition)#,command=get_data_student
buttonstudent.grid(row=10,column=1)

ctr_left.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="nsew")

cv2.destroyAllWindows()


root.mainloop()
